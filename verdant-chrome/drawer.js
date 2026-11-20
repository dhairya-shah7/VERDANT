/**
 * V.E.R.D.A.N.T. In-Tab Drawer Component - Modern White Aesthetic
 */

window.Verdant = window.Verdant || {};

(function() {
  let isDrawerOpen = false;
  let currentDiagnosis = null;
  let inspectedElement = null;

  function initDrawer() {
    if (document.getElementById('verdant-drawer-container')) return;

    // Create Drawer Container (No persistent floating pill on the page)
    const drawer = document.createElement('div');
    drawer.id = 'verdant-drawer-container';
    drawer.innerHTML = `
      <div id="verdant-drawer-header">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:36px; height:36px; border-radius:10px; background:#dcfce7; display:flex; align-items:center; justify-content:center; font-size:20px;">🌱</div>
          <div>
            <div style="font-weight:800; font-size:16px; color:#0f172a; letter-spacing:-0.02em;">V.E.R.D.A.N.T. Debugger</div>
            <div style="font-size:12px; color:#64748b; font-weight:500;">Autonomous Chrome Runtime</div>
          </div>
        </div>
        <button id="verdant-drawer-close" style="background:#f1f5f9; border:none; width:32px; height:32px; border-radius:8px; color:#64748b; font-size:20px; font-weight:700; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:all 0.15s;">&times;</button>
      </div>

      <div id="verdant-drawer-content">
        <!-- Action Buttons -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
          <button id="verdant-btn-inspect" class="verdant-btn verdant-btn-secondary">
            🔍 Inspect Element
          </button>
          <button id="verdant-btn-capture" class="verdant-btn verdant-btn-primary">
            ⚡ Analyze Tab State
          </button>
        </div>

        <!-- Status View Card -->
        <div id="verdant-status-view" class="verdant-card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:12px; font-weight:700; color:#475569; letter-spacing:0.04em;">RUNTIME STATUS</span>
            <span id="verdant-daemon-badge" class="verdant-badge verdant-badge-green">Daemon Active (:8000)</span>
          </div>
          <div id="verdant-status-text" style="font-size:14px; color:#475569; line-height:1.6;">
            Active on current tab. Click <b>Inspect Element</b> for layout/formatting defects or <b>Analyze Tab State</b> to run Gemini.
          </div>
        </div>

        <!-- Live Diagnosis Results Card (Hidden initially) -->
        <div id="verdant-results-card" class="verdant-card" style="display:none; border:2px solid #10b981;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <span id="verdant-model-badge" class="verdant-badge verdant-badge-green" style="font-size:13px; padding:5px 12px;">Gemini 3.5 Flash-Lite</span>
            <span id="verdant-latency-badge" style="font-size:13px; font-weight:700; color:#059669;">~2.1s</span>
          </div>

          <div id="verdant-diag-title" style="font-size:15px; font-weight:800; color:#0f172a; margin-bottom:8px; line-height:1.4;">
            Root Cause Identified
          </div>
          <div id="verdant-diag-cause" style="font-size:14px; color:#334155; line-height:1.6; margin-bottom:16px; background:#f8fafc; padding:14px; border-radius:10px; border:1px solid #e2e8f0;">
            -
          </div>

          <!-- Proposed Fix Preview -->
          <div style="margin-bottom:16px;">
            <div style="font-size:12px; font-weight:700; color:#64748b; margin-bottom:6px; letter-spacing:0.03em;">PROPOSED SURGICAL FIX:</div>
            <pre id="verdant-diag-code" style="font-size:13px; font-family:ui-monospace,SFMono-Regular,Consolas,monospace; background:#0f172a; color:#34d399; padding:14px; border-radius:10px; overflow-x:auto; margin:0; line-height:1.5;">-</pre>
          </div>

          <!-- Dynamic Eco-Pruning Meter -->
          <div id="verdant-dynamic-eco" style="display:none; margin: 12px 0; padding: 12px; background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 12px; font-size: 12px; color: #065f46;">
            <div style="font-weight: 700; display:flex; justify-content:space-between; margin-bottom: 4px;">
              <span>🌱 ContextPrism Dynamic Pruning</span>
              <span id="verdant-eco-pct" style="color:#059669; font-weight:800;">-0%</span>
            </div>
            <div style="color: #047857; font-size: 11px;" id="verdant-eco-details">
              Saved: 0.0 Wh · 0.0 mL Datacenter Cooling Water
            </div>
          </div>

          <!-- Action Buttons -->
          <div style="display:flex; flex-direction:column; gap:10px;">
            <button id="verdant-btn-test-live" class="verdant-btn verdant-btn-primary" style="font-size:15px; padding:14px;">
              🧪 Test Fix Live in Tab
            </button>
            <button id="verdant-btn-send-ide" class="verdant-btn verdant-btn-action" style="font-size:15px; padding:14px;">
              💻 Send to VS Code
            </button>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(drawer);

    // Wire Event Listeners
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
    const modelEl = document.getElementById('verdant-model-badge');

    resultsCard.style.display = 'block';
    if (modelEl && diag.model_used) {
      modelEl.innerText = diag.model_used.replace('models/', '');
    }
    titleEl.innerText = diag.spoken_summary || 'Diagnosis Ready';
    causeEl.innerText = diag.root_cause || 'Defect analyzed.';
    
    if (diag.edits && diag.edits.length > 0) {
      codeEl.innerText = `${diag.edits[0].path || 'Source Patch'}:\n${diag.edits[0].replace || diag.edits[0].patch || ''}`;
    } else if (diag.css_patch) {
      codeEl.innerText = diag.css_patch;
    } else {
      codeEl.innerText = JSON.stringify(diag.evidence || {}, null, 2);
    }

    if (diag.latency_seconds) {
      latencyEl.innerText = `${diag.latency_seconds.toFixed(2)}s`;
    }

    // Dynamic Eco-Audit Population (Zero Hardcoding)
    const ecoContainer = document.getElementById('verdant-dynamic-eco');
    const ecoPct = document.getElementById('verdant-eco-pct');
    const ecoDetails = document.getElementById('verdant-eco-details');
    if (ecoContainer && diag.eco_audit) {
      ecoContainer.style.display = 'block';
      const pct = diag.eco_audit.compression_ratio_pct || 0;
      ecoPct.innerText = `-${pct.toFixed(1)}% Tokens`;
      const wh = diag.eco_audit.energy_saved_wh || 0;
      const ml = diag.eco_audit.water_saved_ml || 0;
      const savedTokens = diag.eco_audit.tokens_saved || 0;
      ecoDetails.innerText = `Pruned ${savedTokens} tokens · Saved ${wh.toFixed(3)} Wh & ${ml.toFixed(2)} mL cooling water`;
    } else if (ecoContainer) {
      ecoContainer.style.display = 'none';
    }
  }

  function startInspectionMode() {
    toggleDrawer(false);
    let toast = document.getElementById('verdant-inspect-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'verdant-inspect-toast';
      toast.style.cssText = `
        position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
        background: #ffffff; color: #0f172a; border: 2px solid #10b981;
        padding: 10px 22px; border-radius: 9999px; font-size: 14px; font-weight: 700;
        z-index: 2147483647; box-shadow: 0 12px 30px rgba(0,0,0,0.15);
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
    statusText.innerHTML = 'Capturing DOM and network telemetry with Gemini 3.5...';

    // Scan for actual layout anomalies on the page
    const layoutAnomalies = window.Verdant.findActiveLayoutAnomalies ? window.Verdant.findActiveLayoutAnomalies() : [];

    chrome.runtime.sendMessage({
      type: 'ANALYZE_TAB',
      payload: window.Verdant.scrubObject({
        url: window.location.href,
        pageTitle: document.title,
        logs: window.__verdant_logs || [],
        networkEvents: window.__verdant_network || [],
        layoutAnomalies: layoutAnomalies
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
