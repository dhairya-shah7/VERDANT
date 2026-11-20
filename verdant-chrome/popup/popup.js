document.addEventListener('DOMContentLoaded', async () => {
  const statusPill = document.getElementById('status-pill');
  const bufferSummary = document.getElementById('buffer-summary');
  const btnInspect = document.getElementById('btn-inspect-element');
  const btnAnalyze = document.getElementById('btn-analyze-active');

  const CLOUD_PORTAL_URL = 'https://verdant-server-1042112525098.us-central1.run.app';

  // Check Daemon Health (Local or Cloud Run)
  chrome.runtime.sendMessage({ type: 'CHECK_DAEMON_STATUS' }, (res) => {
    if (res && res.connected) {
      statusPill.innerText = `Connected (${res.server || 'Cloud Run'})`;
      statusPill.className = 'badge badge-green';
    } else {
      statusPill.innerText = 'Offline';
      statusPill.className = 'badge badge-red';
    }
  });

  // Query Active Tab
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });

  function isRestrictedUrl(url) {
    if (!url) return true;
    return (
      url.startsWith('chrome://') ||
      url.startsWith('chrome-extension://') ||
      url.startsWith('edge://') ||
      url.startsWith('about:') ||
      url.startsWith('devtools://') ||
      url.startsWith('view-source:') ||
      url.includes('chromewebstore.google.com') ||
      url.includes('chrome.google.com/webstore')
    );
  }

  const restricted = !activeTab || isRestrictedUrl(activeTab.url);

  if (activeTab) {
    if (restricted) {
      bufferSummary.innerHTML = `
        <div style="color:#f59e0b; font-weight:700; margin-bottom:4px;">⚠️ Chrome Internal Page</div>
        <div style="font-size:11px; color:#cbd5e1; line-height:1.4;">
          Chrome restricts extensions on <code>${activeTab.url?.slice(0, 28) || 'internal'}...</code>.
          Please switch to any website or web app to inspect elements.
        </div>
        <div style="margin-top:8px;">
          <a href="${CLOUD_PORTAL_URL}" target="_blank" style="display:inline-block; padding:6px 12px; background:#059669; color:#fff; font-size:11px; font-weight:700; border-radius:6px; text-decoration:none;">Open Portal Tab ↗</a>
        </div>
      `;
    } else {
      bufferSummary.innerHTML = `Active Tab: <b style="color:#e2e8f0;">${activeTab.title?.slice(0, 30) || 'Untitled'}</b><br><span style="font-size:10px; color:#64748b;">${activeTab.url?.slice(0, 45)}...</span>`;
    }
  }

  async function sendTabAction(actionName) {
    if (restricted) {
      alert(`Chrome restricts extension scripts from running on internal browser pages (${activeTab?.url?.slice(0, 30)}).\n\nPlease switch to any normal website or click "Open Central Portal" below to test!`);
      return;
    }

    if (!activeTab?.id) return;

    // 1. Try pinging first to see if scripts are already active
    try {
      const pingRes = await new Promise((resolve) => {
        chrome.tabs.sendMessage(activeTab.id, { action: 'PING' }, (res) => {
          if (chrome.runtime.lastError || !res) resolve(null);
          else resolve(res);
        });
      });

      if (!pingRes) {
        // Tab needs injection (e.g. was open before extension reloaded)
        await chrome.scripting.insertCSS({
          target: { tabId: activeTab.id },
          files: ['drawer.css']
        });
        await chrome.scripting.executeScript({
          target: { tabId: activeTab.id },
          files: [
            'src/pii_scrubber.js',
            'src/visual_crawler.js',
            'src/in_tab_patcher.js',
            'drawer.js',
            'content.js'
          ]
        });
        await new Promise(r => setTimeout(r, 60));
      }

      // 2. Dispatch action
      chrome.tabs.sendMessage(activeTab.id, { action: actionName }, (res) => {
        if (chrome.runtime.lastError) {
          console.warn('[V.E.R.D.A.N.T.] Action dispatch note:', chrome.runtime.lastError.message);
        }
        window.close();
      });
    } catch (err) {
      console.warn('[V.E.R.D.A.N.T.] Script injection error:', err);
      chrome.tabs.sendMessage(activeTab.id, { action: actionName }, () => {
        window.close();
      });
    }
  }

  btnInspect.addEventListener('click', () => sendTabAction('START_INSPECTION'));
  btnAnalyze.addEventListener('click', () => sendTabAction('TRIGGER_ANALYSIS'));
});
