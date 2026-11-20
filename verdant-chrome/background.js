/**
 * V.E.R.D.A.N.T. Service Worker (Background Script)
 * Manages tab screenshots, communication with Google Cloud Run & local daemon, and IDE dispatch.
 */

const CLOUD_DAEMON_API = 'https://verdant-server-1042112525098.us-central1.run.app';
const LOCAL_DAEMON_API = 'http://localhost:8000';
let ACTIVE_DAEMON_API = CLOUD_DAEMON_API;

async function getActiveDaemonApi() {
  try {
    const res = await fetch(`${LOCAL_DAEMON_API}/health`, { method: 'GET', signal: AbortSignal.timeout(600) });
    if (res.ok) {
      ACTIVE_DAEMON_API = LOCAL_DAEMON_API;
      return LOCAL_DAEMON_API;
    }
  } catch {}
  ACTIVE_DAEMON_API = CLOUD_DAEMON_API;
  return CLOUD_DAEMON_API;
}

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

  const apiUrl = await getActiveDaemonApi();
  const response = await fetch(`${apiUrl}/api/extension/ingest`, {
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
  const apiUrl = await getActiveDaemonApi();
  const response = await fetch(`${apiUrl}/api/extension/push-ide`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(diagnosis)
  });

  return { ok: response.ok };
}

async function checkDaemonHealth() {
  // 1. Try local dev daemon first
  try {
    const res = await fetch(`${LOCAL_DAEMON_API}/health`, { method: 'GET', signal: AbortSignal.timeout(600) });
    if (res.ok) {
      ACTIVE_DAEMON_API = LOCAL_DAEMON_API;
      return { connected: true, server: ':8000' };
    }
  } catch {}

  // 2. Try live Google Cloud Run deployment
  try {
    const res = await fetch(`${CLOUD_DAEMON_API}/health`, { method: 'GET', signal: AbortSignal.timeout(2500) });
    if (res.ok) {
      ACTIVE_DAEMON_API = CLOUD_DAEMON_API;
      return { connected: true, server: 'Cloud Run' };
    }
  } catch {}

  return { connected: false, server: 'Offline' };
}
