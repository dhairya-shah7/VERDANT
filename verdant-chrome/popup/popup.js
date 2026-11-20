document.addEventListener('DOMContentLoaded', async () => {
  const statusPill = document.getElementById('status-pill');
  const bufferSummary = document.getElementById('buffer-summary');
  const btnInspect = document.getElementById('btn-inspect-element');
  const btnAnalyze = document.getElementById('btn-analyze-active');

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
  if (activeTab) {
    bufferSummary.innerHTML = `Active Tab: <b style="color:#e2e8f0;">${activeTab.title?.slice(0, 30) || 'Untitled'}</b><br><span style="font-size:10px; color:#64748b;">${activeTab.url?.slice(0, 45)}...</span>`;
  }

  async function ensureScriptsInjected(tabId) {
    try {
      await chrome.scripting.insertCSS({
        target: { tabId },
        files: ['drawer.css']
      });
      await chrome.scripting.executeScript({
        target: { tabId },
        files: [
          'src/pii_scrubber.js',
          'src/visual_crawler.js',
          'src/in_tab_patcher.js',
          'drawer.js',
          'content.js'
        ]
      });
    } catch (e) {
      console.warn('Script injection skipped or failed:', e);
    }
  }

  btnInspect.addEventListener('click', async () => {
    if (!activeTab?.id) return;
    try {
      await ensureScriptsInjected(activeTab.id);
      chrome.tabs.sendMessage(activeTab.id, { action: 'START_INSPECTION' }, (res) => {
        window.close();
      });
    } catch (err) {
      console.error(err);
      window.close();
    }
  });

  btnAnalyze.addEventListener('click', async () => {
    if (!activeTab?.id) return;
    try {
      await ensureScriptsInjected(activeTab.id);
      chrome.tabs.sendMessage(activeTab.id, { action: 'TRIGGER_ANALYSIS' }, (res) => {
        window.close();
      });
    } catch (err) {
      console.error(err);
      window.close();
    }
  });
});
