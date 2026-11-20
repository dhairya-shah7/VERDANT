/**
 * V.E.R.D.A.N.T. Visual & DOM Layout Crawler
 * Extracts element geometry, computed CSS, overflow defects, and hierarchy.
 */

window.Verdant = window.Verdant || {};

(function() {
  function inspectElementGeometry(el) {
    if (!el || !(el instanceof Element)) return null;

    const rect = el.getBoundingClientRect();
    const computed = window.getComputedStyle(el);

    const hasHorizontalOverflow = el.scrollWidth > Math.ceil(el.clientWidth) + 1;
    const hasVerticalOverflow = el.scrollHeight > Math.ceil(el.clientHeight) + 1;

    // Build clean CSS selector
    let selector = el.tagName.toLowerCase();
    if (el.id) {
      selector += `#${el.id}`;
    } else if (el.classList && el.classList.length > 0) {
      selector += '.' + Array.from(el.classList).slice(0, 3).join('.');
    }

    // Parent context
    let parentSelector = null;
    if (el.parentElement) {
      parentSelector = el.parentElement.tagName.toLowerCase();
      if (el.parentElement.id) parentSelector += `#${el.parentElement.id}`;
      else if (el.parentElement.classList?.length) parentSelector += '.' + Array.from(el.parentElement.classList).slice(0, 2).join('.');
    }

    return {
      selector,
      parentSelector,
      tagName: el.tagName.toLowerCase(),
      textPreview: (el.innerText || el.textContent || '').trim().slice(0, 160),
      geometry: {
        x: Math.round(rect.x),
        y: Math.round(rect.y),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
        scrollWidth: el.scrollWidth,
        clientWidth: el.clientWidth,
        scrollHeight: el.scrollHeight,
        clientHeight: el.clientHeight,
        hasHorizontalOverflow,
        hasVerticalOverflow
      },
      computedStyles: {
        display: computed.display,
        position: computed.position,
        flexDirection: computed.flexDirection,
        justifyContent: computed.justifyContent,
        alignItems: computed.alignItems,
        overflow: computed.overflow,
        overflowX: computed.overflowX,
        overflowY: computed.overflowY,
        boxSizing: computed.boxSizing,
        margin: computed.margin,
        padding: computed.padding,
        width: computed.width,
        maxWidth: computed.maxWidth,
        minWidth: computed.minWidth,
        zIndex: computed.zIndex
      },
      htmlSnippet: el.outerHTML.slice(0, 500)
    };
  }

  function findActiveLayoutAnomalies() {
    const anomalies = [];
    const allElements = document.querySelectorAll('*');
    
    for (const el of allElements) {
      if (el.offsetWidth > 0 && el.offsetHeight > 0) {
        if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 40) {
          const computed = window.getComputedStyle(el);
          if (computed.overflowX !== 'scroll' && computed.overflowX !== 'auto') {
            anomalies.push({
              type: 'TEXT_OR_CHILD_OVERFLOW',
              selector: el.tagName.toLowerCase() + (el.className ? '.' + el.className.split(' ')[0] : ''),
              scrollWidth: el.scrollWidth,
              clientWidth: el.clientWidth,
              message: `Element overflows container by ${el.scrollWidth - el.clientWidth}px without scrolling.`
            });
          }
        }
      }
      if (anomalies.length >= 5) break;
    }
    return anomalies;
  }

  window.Verdant.inspectElementGeometry = inspectElementGeometry;
  window.Verdant.findActiveLayoutAnomalies = findActiveLayoutAnomalies;
})();
