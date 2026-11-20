/**
 * V.E.R.D.A.N.T. In-Tab Live Hot Patcher
 * Enables instant validation of synthesized CSS, layout fixes, and DOM modifications inside the active browser tab.
 */

window.Verdant = window.Verdant || {};

(function() {
  const STYLE_TAG_ID = 'verdant-hot-patch-style';
  const BANNER_TAG_ID = 'verdant-live-patch-banner';
  let isPatchActive = false;

  function applyCssHotPatch(cssString, affectedSelector) {
    if (!cssString) return false;
    let styleEl = document.getElementById(STYLE_TAG_ID);
    if (!styleEl) {
      styleEl = document.createElement('style');
      styleEl.id = STYLE_TAG_ID;
      document.head.appendChild(styleEl);
    }
    
    // Include visual green highlight on patched selector
    let fullCss = cssString;
    if (affectedSelector) {
      fullCss += `\n${affectedSelector} { outline: 2px solid #10b981 !important; outline-offset: 2px !important; transition: all 0.2s ease !important; }`;
    }
    styleEl.textContent = fullCss;
    isPatchActive = true;
    showLiveBanner(affectedSelector);
    console.log('[V.E.R.D.A.N.T.] Applied live in-tab CSS hot-patch:', cssString);
    return true;
  }

  function removeCssHotPatch() {
    const styleEl = document.getElementById(STYLE_TAG_ID);
    if (styleEl) {
      styleEl.remove();
    }
    const banner = document.getElementById(BANNER_TAG_ID);
    if (banner) {
      banner.remove();
    }
    isPatchActive = false;
    console.log('[V.E.R.D.A.N.T.] Reverted live in-tab hot-patch.');
    return true;
  }

  function showLiveBanner(selector) {
    let banner = document.getElementById(BANNER_TAG_ID);
    if (!banner) {
      banner = document.createElement('div');
      banner.id = BANNER_TAG_ID;
      banner.style.cssText = `
        position: fixed;
        top: 16px;
        left: 50%;
        transform: translateX(-50%);
        background: #0f172a;
        color: #ffffff;
        padding: 10px 18px;
        border-radius: 9999px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 13px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 2147483646;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(16, 185, 129, 0.4);
      `;
      document.body.appendChild(banner);
    }
    
    banner.innerHTML = `
      <div style="display:flex; align-items:center; gap:8px;">
        <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981; box-shadow:0 0 8px #10b981;"></span>
        <span>🌿 Live Hot-Patch Active ${selector ? `(<code style="color:#6ee7b7; font-size:12px;">${selector}</code>)` : ''}</span>
      </div>
      <button id="verdant-banner-revert-btn" style="
        background: #334155;
        color: #f1f5f9;
        border: none;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.15s;
      ">Revert</button>
    `;

    const revertBtn = document.getElementById('verdant-banner-revert-btn');
    if (revertBtn) {
      revertBtn.onclick = () => {
        removeCssHotPatch();
        const drawerBtn = document.getElementById('verdant-btn-test-live');
        if (drawerBtn) {
          drawerBtn.innerText = '🧪 Test Fix Live (in Tab)';
          drawerBtn.style.background = '#f8fafc';
          drawerBtn.style.color = '#334155';
          drawerBtn.style.borderColor = '#cbd5e1';
        }
      };
    }
  }

  function applyDiagnosisLive(diag) {
    if (!diag) return false;

    // 1. Direct CSS patch
    if (diag.css_patch) {
      const match = diag.css_patch.match(/([^{]+)\s*\{/);
      const selector = match ? match[1].trim() : null;
      return applyCssHotPatch(diag.css_patch, selector);
    }

    // 2. Check edits for CSS or inline style
    if (diag.edits && diag.edits.length > 0) {
      for (const edit of diag.edits) {
        if (edit.path && edit.path.endsWith('.css')) {
          const match = edit.replace.match(/([^{]+)\s*\{/);
          const selector = match ? match[1].trim() : null;
          return applyCssHotPatch(edit.replace, selector);
        }
        if (edit.replace && edit.replace.includes('{') && edit.replace.includes(':')) {
          const match = edit.replace.match(/([.#a-zA-Z0-9_\-\s,>+~]+)\s*\{/);
          if (match) {
            return applyCssHotPatch(edit.replace, match[1].trim());
          }
        }
      }
    }

    // 3. Fallback: synthesize in-tab CSS from diagnosis root cause or element
    if (diag.root_cause) {
      const selectorMatch = diag.root_cause.match(/(\.[a-zA-Z0-9_\-]+|#[a-zA-Z0-9_\-]+)/);
      if (selectorMatch) {
        const sel = selectorMatch[1];
        const syntheticCss = `${sel} { overflow: hidden !important; max-width: 100% !important; box-sizing: border-box !important; }`;
        return applyCssHotPatch(syntheticCss, sel);
      }
    }

    return false;
  }

  function applyMockNetworkPatch(urlPattern, mockResponse) {
    if (!window.__verdant_original_fetch) {
      window.__verdant_original_fetch = window.fetch;
      window.__verdant_intercepted_routes = {};

      window.fetch = async function(...args) {
        const url = typeof args[0] === 'string' ? args[0] : args[0]?.url;
        for (const [pattern, mock] of Object.entries(window.__verdant_intercepted_routes)) {
          if (url && url.includes(pattern)) {
            console.log(`[V.E.R.D.A.N.T.] Intercepted failing call to ${url} with synthetic hot-fix`);
            return new Response(JSON.stringify(mock.body || { status: 'ok', patched: true }), {
              status: mock.status || 200,
              headers: { 'Content-Type': 'application/json' }
            });
          }
        }
        return window.__verdant_original_fetch.apply(this, args);
      };
    }

    window.__verdant_intercepted_routes[urlPattern] = mockResponse;
    console.log(`[V.E.R.D.A.N.T.] Mock network patch registered for: ${urlPattern}`);
  }

  window.Verdant.applyCssHotPatch = applyCssHotPatch;
  window.Verdant.removeCssHotPatch = removeCssHotPatch;
  window.Verdant.applyDiagnosisLive = applyDiagnosisLive;
  window.Verdant.applyMockNetworkPatch = applyMockNetworkPatch;
  window.Verdant.isPatchActive = () => isPatchActive;
})();
