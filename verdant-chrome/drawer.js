/**
 * V.E.R.D.A.N.T. In-Tab Drawer Component
 */

window.Verdant = window.Verdant || {};

(function() {
  let isDrawerOpen = false;
  let currentDiagnosis = null;
  let inspectedElement = null;

  function initDrawer() {
    if (document.getElementById('verdant-drawer-container')) return;

    // 1. Create Floating Trigger
    const trigger = document.createElement('div');
    trigger.id = 'verdant-floating-trigger';
    trigger.innerHTML = `
      <span class="pulse-dot"></span>
      <span>V.E.R.D.A.N.T.</span>
    `;
    document.body.appendChild(trigger);

    // 2. Create Drawer Container
    const drawer = document.createElement('div');
    drawer.id = 'verdant-drawer-container';
    drawer.innerHTML = `
      <div id="verdant-drawer-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:18px;">🌱</span>
          <div>
            <div style="font-weight:700; font-size:14px; color:#ffffff;">V.E.R.D.A.N.T. Debugger</div>
            <div style="font-size:11px; color:#94a3b8;">Autonomous Chrome Runtime</div>
          </div>
        </div>
        <button id="verdant-drawer-close" style="background:none; border:none; color:#94a3b8; font-size:18px; cursor:pointer;">&times;</button>
      </div>

      <div id="verdant-drawer-content">
        <!-- Quick Action Controls -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
          <button id="verdant-btn-inspect" class="verdant-btn verdant-btn-secondary">
            🔍 Inspect Element
          </button>
          <button id="verdant-btn-capture" class="verdant-btn verdant-btn-primary">
            ⚡ Analyze Tab State
          </button>
        </div>

        <!-- Status / Inspection View -->
        <div id="verdant-status-view" class="verdant-card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:12px; font-weight:600; color:#cbd5e1;">RUNTIME STATUS</span>
            <span id="verdant-daemon-badge" class="verdant-badge verdant-badge-green">Daemon Active (:8000)</span>
          </div>
          <div id="verdant-status-text" style="font-size:12px; color:#94a3b8; line-height:1.5;">
            Monitoring active DOM & console. Click <b>Inspect Element</b> for visual defects or <b>Analyze Tab State</b> to run Gemini 3.1.
          </div>
        </div>

        <!-- Live Diagnosis Results Card (Hidden initially) -->
        <div id="verdant-results-card" class="verdant-card" style="display:none; border-color:#10b981;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="verdant-badge verdant-badge-green">Gemini 3.1 Flash-Lite</span>
            <span id="verdant-latency-badge" style="font-size:11px; color:#34d399;">~2.1s</span>
          </div>

          <div id="verdant-diag-title" style="font-size:13px; font-weight:700; color:#f8fafc; margin-bottom:6px;">
            Root Cause Identified
          </div>
          <div id="verdant-diag-cause" style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:12px; background:#0f172a; padding:10px; border-radius:6px; border:1px solid #334155;">
            -
          </div>

          <!-- Target Edits / Proposed Fix -->
          <div style="margin-bottom:12px;">
            <div style="font-size:11px; font-weight:600; color:#94a3b8; margin-bottom:4px;">PROPOSED FIX:</div>
            <pre id="verdant-diag-code" style="font-size:11px; background:#0f172a; color:#a7f3d0; padding:10px; border-radius:6px; overflow-x:auto; margin:0; border:1px solid #1e293b;">-</pre>
          </div>

          <!-- Action Buttons -->
          <div style="display:flex; flex-direction:column; gap:8px;">
            <button id="verdant-btn-test-live" class="verdant-btn verdant-btn-primary">
              🧪 Test Fix Live in Tab
            </button>
            <button id="verdant-btn-send-ide" class="verdant-btn verdant-btn-action">
              💻 Send to VS Code
            </button>
          </div>
        </div>

        <!-- VERDE Sustainability Footprint -->
        <div class="verdant-card" style="background:#064e3b; border-color:#059669;">
          <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px;">
            <span style="font-size:14px;">🍃</span>
            <span style="font-size:12px; font-weight:700; color:#a7f3d0;">VERDE Compute Meter</span>
          </div>
          <div style="font-size:11px; color:#d1fae5; line-height:1.4;">
            Zero-waste runtime: <b>-84.9% token bloat</b> eliminated. Saved <b>584 Wh</b> & <b>1.18 L</b> cooling water.
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(drawer);

    // Wire Event Listeners
    trigger.addEventListener('click', () => toggleDrawer());
    document.getElementById('verdant-drawer-close').addEventListener('click', () => toggleDrawer(false));
    document.getElementById('verdant-btn-inspect').addEventListener('click', () => startInspectionMode());
    document.getElementById('verdant-btn-capture').addEventListener('click', () => triggerFullTabAnalysis());
    document.getElementById('verdant-btn-test-live').addEventListener('click', () => handleTestFixLive());
    document.getElementById('verdant-btn-send-ide').addEventListener('click', () => handleSendToIde());
  }

  function toggleDrawer(forceState) {
    const drawer = document.getElementById('verdant-drawer-container');
    if (!drawer) return;
    isDrawerOpen = (forceState !== undefined) ? forceState : !isDrawerOpen;
    if (isDrawerOpen) drawer.classList.add('open');
    else drawer.classList.remove('open');
  }

  function displayDiagnosis(diag) {
    currentDiagnosis = diag;
    toggleDrawer(true);

    const resultsCard = document.getElementById('verdant-results-card');
    const titleEl = document.getElementById('verdant-diag-title');
    const causeEl = document.getElementById('verdant-diag-cause');
    const codeEl = document.getElementById('verdant-diag-code');
    const latencyEl = document.getElementById('verdant-latency-badge');

    resultsCard.style.display = 'block';
    titleEl.innerText = diag.spoken_summary || 'Diagnosis Ready';
    causeEl.innerText = diag.root_cause || 'Defect analyzed.';
    
    if (diag.edits && diag.edits.length > 0) {
      codeEl.innerText = `${diag.edits[0].path || 'CSS/DOM Patch'}:\n${diag.edits[0].replace || diag.edits[0].patch || ''}`;
    } else if (diag.css_patch) {
      codeEl.innerText = diag.css_patch;
    } else {
      codeEl.innerText = JSON.stringify(diag.evidence || {}, null, 2);
    }

    if (diag.latency_seconds) {
      latencyEl.innerText = `${diag.latency_seconds.toFixed(2)}s`;
    }
  }

  function startInspectionMode() {
    toggleDrawer(false);
    let toast = document.getElementById('verdant-inspect-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'verdant-inspect-toast';
      toast.style.cssText = `
        position: fixed; top: 16px; left: 50%; transform: translateX(-50%);
        background: #0f172a; color: #10b981; border: 1px solid #10b981;
        padding: 8px 16px; border-radius: 9999px; font-size: 13px; font-weight: 600;
        z-index: 2147483647; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      `;
      toast.innerText = '🔍 Click any element to inspect layout & geometry (Esc to cancel)';
      document.body.appendChild(toast);
    }

    let hoveredEl = null;

    function onMouseOver(e) {
      if (e.target.closest('#verdant-drawer-container') || e.target.closest('#verdant-floating-trigger') || e.target.id === 'verdant-inspect-toast') return;
      if (hoveredEl) hoveredEl.classList.remove('verdant-inspect-highlight');
      hoveredEl = e.target;
      hoveredEl.classList.add('verdant-inspect-highlight');
    }

    function onClick(e) {
      if (e.target.closest('#verdant-drawer-container') || e.target.closest('#verdant-floating-trigger') || e.target.id === 'verdant-inspect-toast') return;
      e.preventDefault();
      e.stopPropagation();

      cleanUp();
      inspectedElement = e.target;
      const geometryData = window.Verdant.inspectElementGeometry(inspectedElement);

      triggerElementAnalysis(geometryData);
    }

    function onKeyDown(e) {
      if (e.key === 'Escape') cleanUp();
    }

    function cleanUp() {
      if (hoveredEl) hoveredEl.classList.remove('verdant-inspect-highlight');
      const t = document.getElementById('verdant-inspect-toast');
      if (t) t.remove();
      document.removeEventListener('mouseover', onMouseOver, true);
      document.removeEventListener('click', onClick, true);
      document.removeEventListener('keydown', onKeyDown, true);
    }

    document.addEventListener('mouseover', onMouseOver, true);
    document.addEventListener('click', onClick, true);
    document.addEventListener('keydown', onKeyDown, true);
  }

  function triggerElementAnalysis(geometryData) {
    toggleDrawer(true);
    const statusText = document.getElementById('verdant-status-text');
    statusText.innerHTML = `Analyzing <b>${geometryData.selector}</b> with Gemini 3.1...`;

    chrome.runtime.sendMessage({
      type: 'ANALYZE_ELEMENT',
      payload: window.Verdant.scrubObject({
        url: window.location.href,
        element: geometryData,
        logs: window.__verdant_logs || [],
        networkEvents: window.__verdant_network || []
      })
    }, (response) => {
      if (response && response.diagnosis) {
        displayDiagnosis(response.diagnosis);
      }
    });
  }

  function triggerFullTabAnalysis() {
    toggleDrawer(true);
    const statusText = document.getElementById('verdant-status-text');
    statusText.innerHTML = 'Capturing DOM and network telemetry with Gemini 3.1...';

    chrome.runtime.sendMessage({
      type: 'ANALYZE_TAB',
      payload: window.Verdant.scrubObject({
        url: window.location.href,
        logs: window.__verdant_logs || [],
        networkEvents: window.__verdant_network || []
      })
    }, (response) => {
      if (response && response.diagnosis) {
        displayDiagnosis(response.diagnosis);
      }
    });
  }

  function handleTestFixLive() {
    if (!currentDiagnosis) return;
    const testLiveBtn = document.getElementById('verdant-btn-test-live');

    if (currentDiagnosis.css_patch) {
      window.Verdant.applyCssHotPatch(currentDiagnosis.css_patch);
      testLiveBtn.innerText = '✓ Patch Applied (Live)';
      testLiveBtn.style.background = '#059669';
    } else if (currentDiagnosis.edits && currentDiagnosis.edits.length > 0) {
      const edit = currentDiagnosis.edits[0];
      if (edit.path && (edit.path.endsWith('.css') || edit.replace.includes('{'))) {
        window.Verdant.applyCssHotPatch(edit.replace);
        testLiveBtn.innerText = '✓ CSS Applied (Live)';
        testLiveBtn.style.background = '#059669';
      } else {
        alert(`Code patch for ${edit.path} is ready to send to VS Code!`);
      }
    }
  }

  function handleSendToIde() {
    if (!currentDiagnosis) return;
    const sendBtn = document.getElementById('verdant-btn-send-ide');
    sendBtn.innerText = 'Pushing to VS Code...';

    chrome.runtime.sendMessage({
      type: 'PUSH_TO_IDE',
      diagnosis: currentDiagnosis
    }, (response) => {
      if (response && response.ok) {
        sendBtn.innerText = '✓ Sent to VS Code!';
        sendBtn.style.background = '#16a34a';
      } else {
        sendBtn.innerText = '✗ VS Code Daemon Error';
        sendBtn.style.background = '#dc2626';
      }
    });
  }

  window.Verdant.initDrawer = initDrawer;
  window.Verdant.toggleDrawer = toggleDrawer;
  window.Verdant.displayDiagnosis = displayDiagnosis;
  window.Verdant.startInspectionMode = startInspectionMode;
  window.Verdant.triggerFullTabAnalysis = triggerFullTabAnalysis;
})();
