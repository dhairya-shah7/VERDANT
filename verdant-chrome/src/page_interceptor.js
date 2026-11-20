/**
 * V.E.R.D.A.N.T. Page Interceptor
 * Runs in the MAIN WORLD of the inspected web page to capture real runtime events:
 * console.error, console.warn, uncaught exceptions, unhandled promise rejections,
 * fetch 4xx/5xx drops, and XMLHttpRequest failures.
 */

(function() {
  if (window.__verdant_page_interceptor_active) return;
  window.__verdant_page_interceptor_active = true;

  function isVerdantInternal(str) {
    if (!str) return false;
    const s = String(str);
    return s.includes('[V.E.R.D.A.N.T.]') || s.includes('verdant-') || s.includes('chrome-extension://');
  }

  function emitToContentScript(payload) {
    try {
      window.postMessage({
        source: '__VERDANT_PAGE_TELEMETRY__',
        data: payload
      }, '*');
    } catch (_) {}
  }

  // 1. Hook console.error
  const origConsoleError = console.error;
  console.error = function(...args) {
    const rawMsg = args.map(a => {
      if (a instanceof Error) return a.message + (a.stack ? '\n' + a.stack : '');
      if (typeof a === 'object') {
        try { return JSON.stringify(a); } catch(_) { return String(a); }
      }
      return String(a);
    }).join(' ');

    if (!isVerdantInternal(rawMsg)) {
      emitToContentScript({
        category: 'log',
        type: 'console_error',
        message: rawMsg.slice(0, 1000),
        timestamp: new Date().toISOString()
      });
    }
    origConsoleError.apply(console, args);
  };

  // 2. Hook console.warn
  const origConsoleWarn = console.warn;
  console.warn = function(...args) {
    const rawMsg = args.map(a => {
      if (typeof a === 'object') {
        try { return JSON.stringify(a); } catch(_) { return String(a); }
      }
      return String(a);
    }).join(' ');

    if (!isVerdantInternal(rawMsg)) {
      emitToContentScript({
        category: 'log',
        type: 'console_warn',
        message: rawMsg.slice(0, 800),
        timestamp: new Date().toISOString()
      });
    }
    origConsoleWarn.apply(console, args);
  };

  // 3. Uncaught Window Errors
  window.addEventListener('error', function(event) {
    const msg = event.message || 'Script runtime exception';
    if (!isVerdantInternal(msg) && !isVerdantInternal(event.filename)) {
      emitToContentScript({
        category: 'log',
        type: 'uncaught_error',
        message: msg,
        stack: event.error ? String(event.error.stack).slice(0, 1000) : null,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        timestamp: new Date().toISOString()
      });
    }
  }, true);

  // 4. Unhandled Promise Rejections
  window.addEventListener('unhandledrejection', function(event) {
    const reason = event.reason;
    const msg = reason ? (reason.message || String(reason)) : 'Unhandled rejection';
    if (!isVerdantInternal(msg)) {
      emitToContentScript({
        category: 'log',
        type: 'unhandled_rejection',
        message: msg,
        stack: reason && reason.stack ? String(reason.stack).slice(0, 1000) : null,
        timestamp: new Date().toISOString()
      });
    }
  }, true);

  // 5. Hook Fetch API for 4xx/5xx or Network Drops
  const origFetch = window.fetch;
  if (typeof origFetch === 'function') {
    window.fetch = async function(...args) {
      const url = typeof args[0] === 'string' ? args[0] : (args[0]?.url || '');
      const method = args[1]?.method || 'GET';

      // Ignore local daemon or chrome internal
      if (url.includes(':8000') || url.includes('chrome-extension://')) {
        return origFetch.apply(this, args);
      }

      try {
        const res = await origFetch.apply(this, args);
        if (!res.ok) {
          emitToContentScript({
            category: 'network',
            method,
            url: url.slice(0, 300),
            status: res.status,
            statusText: res.statusText || `HTTP ${res.status}`,
            timestamp: new Date().toISOString()
          });
        }
        return res;
      } catch (err) {
        emitToContentScript({
          category: 'network',
          method,
          url: url.slice(0, 300),
          status: 0,
          statusText: err.message || 'Network Fetch Failed',
          timestamp: new Date().toISOString()
        });
        throw err;
      }
    };
  }

  // 6. Hook XMLHttpRequest for 4xx/5xx
  const origXhrOpen = XMLHttpRequest.prototype.open;
  const origXhrSend = XMLHttpRequest.prototype.send;

  XMLHttpRequest.prototype.open = function(method, url) {
    this._verdant_method = method;
    this._verdant_url = url;
    return origXhrOpen.apply(this, arguments);
  };

  XMLHttpRequest.prototype.send = function() {
    this.addEventListener('load', function() {
      if (this.status >= 400 && this._verdant_url && !this._verdant_url.includes(':8000')) {
        emitToContentScript({
          category: 'network',
          method: this._verdant_method || 'GET',
          url: String(this._verdant_url).slice(0, 300),
          status: this.status,
          statusText: this.statusText || `HTTP ${this.status}`,
          timestamp: new Date().toISOString()
        });
      }
    });

    this.addEventListener('error', function() {
      if (this._verdant_url && !this._verdant_url.includes(':8000')) {
        emitToContentScript({
          category: 'network',
          method: this._verdant_method || 'GET',
          url: String(this._verdant_url).slice(0, 300),
          status: 0,
          statusText: 'XHR Network Failure',
          timestamp: new Date().toISOString()
        });
      }
    });

    return origXhrSend.apply(this, arguments);
  };
})();
