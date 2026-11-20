/**
 * V.E.R.D.A.N.T. Content Script
 * Receives page telemetry from the main world interceptor, monitors DOM layout,
 * and coordinates the in-tab debugger drawer.
 */

window.Verdant = window.Verdant || {};
window.__verdant_logs = window.__verdant_logs || [];
window.__verdant_network = window.__verdant_network || [];

function isVerdantInternal(str) {
  if (!str) return false;
  const s = String(str);
  return s.includes('[V.E.R.D.A.N.T.]') || s.includes('verdant-') || s.includes('chrome-extension://');
}

function pushLog(type, message, stack) {
  if (isVerdantInternal(message) || isVerdantInternal(stack)) return;
  window.__verdant_logs.push({
    timestamp: new Date().toISOString(),
    type,
    message: String(message).slice(0, 500),
    stack: stack ? String(stack).slice(0, 1000) : null
  });
  if (window.__verdant_logs.length > 40) window.__verdant_logs.shift();
}

function pushNetwork(method, url, status, statusText) {
  if (isVerdantInternal(url) || (url && url.includes(':8000'))) return;
  window.__verdant_network.push({
    timestamp: new Date().toISOString(),
    method: method || 'GET',
    url: String(url).slice(0, 300),
    status,
    statusText: statusText || `HTTP ${status}`
  });
  if (window.__verdant_network.length > 25) window.__verdant_network.shift();
}

// 1. Receive Main World Real Telemetry from page_interceptor.js
window.addEventListener('message', (event) => {
  if (event.source !== window || !event.data || event.data.source !== '__VERDANT_PAGE_TELEMETRY__') return;
  const item = event.data.data;
  if (!item) return;

  if (item.category === 'log') {
    pushLog(item.type, item.message, item.stack);
  } else if (item.category === 'network') {
    pushNetwork(item.method, item.url, item.status, item.statusText);
  }
});

// 2. Inject Page Interceptor Script into Page DOM (fallback & immediate hooking)
function injectPageInterceptor() {
  if (document.getElementById('verdant-page-interceptor-script')) return;
  try {
    const s = document.createElement('script');
    s.id = 'verdant-page-interceptor-script';
    s.src = chrome.runtime.getURL('src/page_interceptor.js');
    s.onload = () => s.remove();
    (document.head || document.documentElement).appendChild(s);
  } catch (_) {}
}
injectPageInterceptor();

// 3. Isolated World Catchers (Fallback)
if (!window.__verdant_isolated_hooked) {
  window.__verdant_isolated_hooked = true;

  window.addEventListener('error', (event) => {
    if (!isVerdantInternal(event.message)) {
      pushLog('uncaught_error', event.message, event.error?.stack);
    }
  }, true);

  window.addEventListener('unhandledrejection', (event) => {
    const msg = event.reason?.message || String(event.reason);
    if (!isVerdantInternal(msg)) {
      pushLog('unhandled_rejection', msg, event.reason?.stack);
    }
  }, true);
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
