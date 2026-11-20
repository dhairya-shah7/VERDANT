document.addEventListener('DOMContentLoaded', async () => {
  const statusPill = document.getElementById('status-pill');
  const bufferSummary = document.getElementById('buffer-summary');
  const btnInspect = document.getElementById('btn-inspect-element');
  const btnAnalyze = document.getElementById('btn-analyze-active');

  // Check Local Daemon Health
  chrome.runtime.sendMessage({ type: 'CHECK_DAEMON_STATUS' }, (res) => {
    if (res && res.connected) {
      statusPill.innerText = 'Connected (:8000)';
      statusPill.className = 'badge badge-green';
    } else {
      statusPill.innerText = 'Offline (:8000)';
      statusPill.className = 'badge badge-red';
    }
  });

  // Query Active Tab
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (activeTab) {
    bufferSummary.innerHTML = `Active Tab: <b style="color:#e2e8f0;">${activeTab.title?.slice(0, 30) || 'Untitled'}</b><br><span style="font-size:10px; color:#64748b;">${activeTab.url?.slice(0, 45)}...</span>`;
  }

  btnInspect.addEventListener('click', () => {
    if (!activeTab?.id) return;
    chrome.tabs.sendMessage(activeTab.id, { action: 'START_INSPECTION' });
    window.close();
  });

  btnAnalyze.addEventListener('click', () => {
    if (!activeTab?.id) return;
    chrome.tabs.sendMessage(activeTab.id, { action: 'TRIGGER_ANALYSIS' });
    window.close();
  });
});
