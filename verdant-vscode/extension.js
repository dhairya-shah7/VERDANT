/**
 * V.E.R.D.A.N.T. VS Code Extension
 * Connects to ws://localhost:8000/ws/ide
 * Receives defect events from Chrome Extension, jumps to suspect lines, renders diffs, and runs Playwright reproducers.
 */
const vscode = require('vscode');
const path = require('path');
const fs = require('fs');
const http = require('http');

let wsClient = null;
let statusBarItem = null;
let currentDiagnosis = null;
let reconnectTimer = null;

const CLOUD_WS = 'wss://verdant-server-1042112525098.us-central1.run.app/ws/ide';
const LOCAL_WS = 'ws://localhost:8000/ws/ide';
let activeWsUrl = CLOUD_WS;

function activate(context) {
  console.log('[V.E.R.D.A.N.T. IDE] Activating Autonomous Bridge...');

  // 1. Status Bar Indicator
  statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  statusBarItem.command = 'verdant.connect';
  statusBarItem.text = '$(sync~spin) V.E.R.D.A.N.T.: Connecting...';
  statusBarItem.tooltip = 'Click to reconnect to V.E.R.D.A.N.T. Cloud Run Daemon';
  statusBarItem.show();
  context.subscriptions.push(statusBarItem);

  // 2. Register Commands
  context.subscriptions.push(
    vscode.commands.registerCommand('verdant.connect', () => {
      connectToDaemon();
    }),
    vscode.commands.registerCommand('verdant.applyPatch', async () => {
      await applyCurrentPatch();
    }),
    vscode.commands.registerCommand('verdant.runPlaywright', () => {
      runPlaywrightRepro();
    })
  );

  // 3. Auto Connect
  connectToDaemon();
}

function connectToDaemon() {
  if (reconnectTimer) clearTimeout(reconnectTimer);

  try {
    const WS = globalThis.WebSocket || (typeof WebSocket !== 'undefined' ? WebSocket : null);
    if (!WS) {
      statusBarItem.text = '$(plug) V.E.R.D.A.N.T.: Ready';
      statusBarItem.tooltip = 'WebSocket not natively bundled in current environment';
      return;
    }

    if (wsClient) {
      try { wsClient.close(); } catch(e) {}
    }

    // Try connecting to Cloud Run or Local
    wsClient = new WS(activeWsUrl);

    wsClient.onopen = () => {
      const isCloud = activeWsUrl.includes('run.app');
      const label = isCloud ? 'Cloud Run' : ':8000';
      console.log('[V.E.R.D.A.N.T. IDE] Connected to daemon at ' + activeWsUrl);
      statusBarItem.text = `$(beaker) V.E.R.D.A.N.T.: Connected (${label})`;
      statusBarItem.tooltip = `Listening for incoming Chrome bugs & visual defects via ${label}`;
      vscode.window.showInformationMessage(`🌱 V.E.R.D.A.N.T. Autonomous IDE Bridge Connected (${label})`);
    };

    wsClient.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        handleIncomingMessage(msg);
      } catch (e) {
        console.error('[V.E.R.D.A.N.T. IDE] Parse error:', e);
      }
    };

    wsClient.onclose = () => {
      statusBarItem.text = '$(circle-slash) V.E.R.D.A.N.T.: Reconnecting...';
      statusBarItem.tooltip = 'Daemon connection closed. Reconnecting in 5 seconds...';
      // Toggle between Cloud Run and Local on reconnect
      activeWsUrl = (activeWsUrl === CLOUD_WS) ? LOCAL_WS : CLOUD_WS;
      reconnectTimer = setTimeout(connectToDaemon, 5000);
    };

    wsClient.onerror = () => {
      statusBarItem.text = '$(circle-slash) V.E.R.D.A.N.T.: Offline';
    };

  } catch (err) {
    console.warn('[V.E.R.D.A.N.T. IDE] Connection error:', err.message);
    reconnectTimer = setTimeout(connectToDaemon, 5000);
  }
}

async function handleIncomingMessage(msg) {
  if (msg.type !== 'DEFECT_INGESTED') return;

  const diag = msg.diagnosis;
  currentDiagnosis = diag;
  const url = msg.url || 'Web App';
  const suspectFile = diag.evidence?.suspect_file || (diag.edits?.[0]?.path) || 'Unknown File';
  const lineNo = diag.evidence?.line_numbers?.[0] || 1;

  // Notification with quick actions
  const action = await vscode.window.showWarningMessage(
    `🌱 V.E.R.D.A.N.T.: Defect detected on ${url} (${suspectFile}:${lineNo})\n${diag.spoken_summary}`,
    'Review Fix & Jump to Line',
    'Accept Patch Now',
    'Dismiss'
  );

  if (action === 'Review Fix & Jump to Line') {
    await jumpToFileAndLine(suspectFile, lineNo);
    showProposedDiff(diag);
  } else if (action === 'Accept Patch Now') {
    await applyCurrentPatch();
  }
}

async function jumpToFileAndLine(relPath, lineNo) {
  const workspaceFolders = vscode.workspace.workspaceFolders;
  if (!workspaceFolders || workspaceFolders.length === 0) return;

  const rootPath = workspaceFolders[0].uri.fsPath;
  const fullPath = path.isAbsolute(relPath) ? relPath : path.join(rootPath, relPath);

  if (!fs.existsSync(fullPath)) {
    console.warn('[V.E.R.D.A.N.T. IDE] File does not exist locally:', fullPath);
    return;
  }

  const doc = await vscode.workspace.openTextDocument(fullPath);
  const editor = await vscode.window.showTextDocument(doc, { preview: false });

  const position = new vscode.Position(Math.max(0, lineNo - 1), 0);
  editor.selection = new vscode.Selection(position, position);
  editor.revealRange(new vscode.Range(position, position), vscode.TextEditorRevealType.InCenter);
}

function showProposedDiff(diag) {
  if (!diag.edits || diag.edits.length === 0) {
    vscode.window.showInformationMessage(`Root Cause: ${diag.root_cause}`);
    return;
  }

  const edit = diag.edits[0];
  vscode.window.showInformationMessage(
    `Proposed Edit for ${edit.path}:\nSearch: ${edit.search}\nReplace: ${edit.replace}`,
    'Accept & Apply',
    'Cancel'
  ).then(selection => {
    if (selection === 'Accept & Apply') {
      applyCurrentPatch();
    }
  });
}

async function applyCurrentPatch() {
  if (!currentDiagnosis) {
    vscode.window.showErrorMessage('No active V.E.R.D.A.N.T. patch loaded.');
    return;
  }

  const payload = JSON.stringify({
    edits: currentDiagnosis.edits || [],
    test_spec: currentDiagnosis.test_spec || null
  });

  const req = http.request(`${DAEMON_HTTP}/api/ide/apply-patch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload)
    }
  }, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
      try {
        const result = JSON.parse(data);
        if (result.ok) {
          vscode.window.showInformationMessage(
            `✓ V.E.R.D.A.N.T.: Patch applied successfully! (${result.modified_files.length} files updated)`,
            'Run Playwright Test'
          ).then(choice => {
            if (choice === 'Run Playwright Test') {
              runPlaywrightRepro();
            }
          });
        }
      } catch(e) {
        vscode.window.showErrorMessage('Failed to apply patch.');
      }
    });
  });

  req.on('error', (err) => {
    vscode.window.showErrorMessage('Daemon communication error: ' + err.message);
  });

  req.write(payload);
  req.end();
}

function runPlaywrightRepro() {
  const terminal = vscode.window.createTerminal('V.E.R.D.A.N.T. Repro');
  terminal.show();

  if (currentDiagnosis?.test_spec?.path) {
    terminal.sendText(`npx playwright test ${currentDiagnosis.test_spec.path} --headed`);
  } else {
    terminal.sendText(`npx playwright test`);
  }
}

function deactivate() {
  if (wsClient) {
    try { wsClient.close(); } catch(e) {}
  }
}

module.exports = {
  activate,
  deactivate
};
