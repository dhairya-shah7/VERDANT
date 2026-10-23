const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const http = require('http');
const { spawn } = require('child_process');

let mainWindow = null;
let backendProcess = null;

// Helper to check if backend is already listening
function checkBackendAlive() {
  return new Promise((resolve) => {
    const req = http.get('http://127.0.0.1:8000/api/health', (res) => {
      resolve(res.statusCode === 200);
    });
    req.on('error', () => resolve(false));
    req.setTimeout(1000, () => {
      req.destroy();
      resolve(false);
    });
  });
}

async function ensureBackend() {
  const isAlive = await checkBackendAlive();
  if (isAlive) {
    console.log('[VERDANT] Backend server is already running on 127.0.0.1:8000. Reusing active instance.');
    return;
  }

  console.log('[VERDANT] Backend not detected on port 8000. Starting backend process...');
  const backendDir = path.join(__dirname, 'backend');
  try {
    // shell: false prevents DEP0190 deprecation warning
    backendProcess = spawn('python', ['-m', 'uvicorn', 'server:app', '--host', '127.0.0.1', '--port', '8000'], {
      cwd: backendDir,
      shell: false,
      stdio: 'ignore'
    });

    backendProcess.on('error', (err) => {
      console.log('[VERDANT] Failed to spawn backend (might already be running):', err.message);
    });
  } catch (err) {
    console.log('[VERDANT] Backend start skipped or handled:', err);
  }
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1360,
    height: 860,
    minWidth: 1024,
    minHeight: 700,
    title: 'VERDANT — Alexa+ Smart Companion Display (Echo Show 15 OS)',
    backgroundColor: '#070b14',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false // Enables seamless local API fetch across file:// and localhost
    }
  });

  Menu.setApplicationMenu(null); // Frameless smart-display feel

  // Load the polished Echo Show frontend
  const frontendPath = path.join(__dirname, 'frontend', 'index.html');
  mainWindow.loadFile(frontendPath);

  mainWindow.on('closed', () => {
    mainWindow = null;
    if (backendProcess) {
      try {
        backendProcess.kill();
      } catch (e) {}
    }
  });
}

// Enforce single instance lock
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });

  app.whenReady().then(async () => {
    await ensureBackend();
    createWindow();

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
  });

  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit();
    }
  });
}
