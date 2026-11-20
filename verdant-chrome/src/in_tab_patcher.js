/**
 * V.E.R.D.A.N.T. In-Tab Live Hot Patcher
 * Enables instant validation of synthesized CSS and DOM fixes inside the active browser tab.
 */

window.Verdant = window.Verdant || {};

(function() {
  const STYLE_TAG_ID = 'verdant-hot-patch-style';

  function applyCssHotPatch(cssString) {
    if (!cssString) return false;
    let styleEl = document.getElementById(STYLE_TAG_ID);
    if (!styleEl) {
      styleEl = document.createElement('style');
      styleEl.id = STYLE_TAG_ID;
      document.head.appendChild(styleEl);
    }
    styleEl.textContent = cssString;
    console.log('[V.E.R.D.A.N.T.] Applied live in-tab CSS hot-patch:', cssString);
    return true;
  }

  function removeCssHotPatch() {
    const styleEl = document.getElementById(STYLE_TAG_ID);
    if (styleEl) {
      styleEl.remove();
      console.log('[V.E.R.D.A.N.T.] Reverted live in-tab CSS hot-patch.');
      return true;
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
  window.Verdant.applyMockNetworkPatch = applyMockNetworkPatch;
})();
