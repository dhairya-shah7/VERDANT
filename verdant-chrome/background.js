/**
 * V.E.R.D.A.N.T. Service Worker (Background Script)
 * Manages tab screenshots, communication with the local V.E.R.D.A.N.T. daemon (:8000), and IDE dispatch.
 */

const DAEMON_API = 'http://localhost:8000';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'ANALYZE_ELEMENT' || request.type === 'ANALYZE_TAB') {
    handleAnalysis(request, sender)
      .then(res => sendResponse(res))
      .catch(err => sendResponse({ ok: false, error: err.message }));
    return true; // Keep channel open for async response
  }

  if (request.type === 'PUSH_TO_IDE') {
    handlePushToIde(request.diagnosis)
      .then(res => sendResponse(res))
      .catch(err => sendResponse({ ok: false, error: err.message }));
    return true;
  }

  if (request.type === 'CHECK_DAEMON_STATUS') {
    checkDaemonHealth()
      .then(status => sendResponse(status))
      .catch(err => sendResponse({ connected: false, error: err.message }));
    return true;
  }
});

async function handleAnalysis(request, sender) {
  let screenshot = null;
  try {
    screenshot = await chrome.tabs.captureVisibleTab(null, { format: 'jpeg', quality: 70 });
  } catch (e) {
    console.warn('[V.E.R.D.A.N.T.] Screenshot capture omitted:', e.message);
  }

  const payload = {
    ...request.payload,
    screenshotBase64: screenshot ? screenshot.replace(/^data:image\/[a-z]+;base64,/, '') : null,
    tabId: sender.tab?.id,
    pageTitle: sender.tab?.title
  };

  const response = await fetch(`${DAEMON_API}/api/extension/ingest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Daemon returned HTTP ${response.status}`);
  }

  const data = await response.json();
  return { ok: true, diagnosis: data };
}

async function handlePushToIde(diagnosis) {
  const response = await fetch(`${DAEMON_API}/api/extension/push-ide`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(diagnosis)
  });

  return { ok: response.ok };
}

async function checkDaemonHealth() {
  try {
    const res = await fetch(`${DAEMON_API}/health`, { method: 'GET' });
    return { connected: res.ok };
  } catch {
    return { connected: false };
  }
}
