/**
 * V.E.R.D.A.N.T. Content Script
 * Captures console errors, network 4xx/5xx drops, and injects the interactive debugger drawer.
 */

window.Verdant = window.Verdant || {};
window.__verdant_logs = window.__verdant_logs || [];
window.__verdant_network = window.__verdant_network || [];

function pushLog(type, message, stack) {
  window.__verdant_logs.push({
    timestamp: new Date().toISOString(),
    type,
    message: String(message).slice(0, 500),
    stack: stack ? String(stack).slice(0, 1000) : null
  });
  if (window.__verdant_logs.length > 30) window.__verdant_logs.shift();
}

function pushNetwork(method, url, status, statusText) {
  window.__verdant_network.push({
    timestamp: new Date().toISOString(),
    method,
    url,
    status,
    statusText
  });
  if (window.__verdant_network.length > 20) window.__verdant_network.shift();
}

// 1. Intercept console.error & console.warn
if (!window.__verdant_console_hooked) {
  window.__verdant_console_hooked = true;
  const originalConsoleError = console.error;
  console.error = function(...args) {
    pushLog('error', args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '));
    originalConsoleError.apply(console, args);
  };

  const originalConsoleWarn = console.warn;
  console.warn = function(...args) {
    pushLog('warn', args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '));
    originalConsoleWarn.apply(console, args);
  };

  // 2. Intercept window errors & rejections
  window.addEventListener('error', (event) => {
    pushLog('uncaught_error', event.message, event.error?.stack);
  });

  window.addEventListener('unhandledrejection', (event) => {
    pushLog('unhandled_rejection', event.reason?.message || String(event.reason), event.reason?.stack);
  });

  // 3. Intercept Fetch API for failures
  const originalFetch = window.fetch;
  window.fetch = async function(...args) {
    const url = typeof args[0] === 'string' ? args[0] : args[0]?.url;
    const method = args[1]?.method || 'GET';
    try {
      const res = await originalFetch.apply(this, args);
      if (!res.ok) {
        pushNetwork(method, url, res.status, res.statusText);
      }
      return res;
    } catch (err) {
      pushNetwork(method, url, 0, 'Fetch Network Failure');
      throw err;
    }
  };
}

// 4. Message Dispatcher for Toolbar Popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'START_INSPECTION') {
    if (window.Verdant && window.Verdant.startInspectionMode) {
      window.Verdant.startInspectionMode();
      sendResponse({ ok: true });
    } else {
      sendResponse({ ok: false, error: 'Inspection module not initialized' });
    }
    return true;
  }

  if (request.action === 'TRIGGER_ANALYSIS') {
    if (window.Verdant && window.Verdant.triggerFullTabAnalysis) {
      window.Verdant.triggerFullTabAnalysis();
      sendResponse({ ok: true });
    } else {
      sendResponse({ ok: false, error: 'Analysis module not initialized' });
    }
    return true;
  }
});

// 5. Initialize Drawer UI
function bootDrawer() {
  if (window.Verdant && window.Verdant.initDrawer) {
    window.Verdant.initDrawer();
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootDrawer);
} else {
  bootDrawer();
}
