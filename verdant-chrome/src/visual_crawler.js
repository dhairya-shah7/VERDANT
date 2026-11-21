/**
 * V.E.R.D.A.N.T. Visual & DOM Layout Crawler
 * Extracts element geometry, computed CSS, overflow defects, DOM hierarchy, and semantic skeletons.
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
      htmlSnippet: el.outerHTML.slice(0, 800)
    };
  }

  function findActiveLayoutAnomalies() {
    const anomalies = [];
    const allElements = document.querySelectorAll('*');
    
    for (const el of allElements) {
      if (el.id === 'verdant-drawer-container' || (el.closest && el.closest('#verdant-drawer-container'))) continue;
      if (el.offsetWidth > 0 && el.offsetHeight > 0) {
        if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 40) {
          const computed = window.getComputedStyle(el);
          if (computed.overflowX !== 'scroll' && computed.overflowX !== 'auto') {
            anomalies.push({
              type: 'LAYOUT_OVERFLOW',
              selector: el.tagName.toLowerCase() + (el.id ? '#' + el.id : (el.className ? '.' + el.className.toString().split(' ')[0] : '')),
              scrollWidth: el.scrollWidth,
              clientWidth: el.clientWidth,
              overflowPx: el.scrollWidth - el.clientWidth,
              message: `Element overflows container horizontally by ${el.scrollWidth - el.clientWidth}px.`
            });
          }
        }
      }
      if (anomalies.length >= 6) break;
    }
    return anomalies;
  }

  function buildDomSkeleton(el, depth, maxDepth) {
    if (!el || depth > maxDepth) return '';
    const tag = el.tagName ? el.tagName.toLowerCase() : '';
    if (!tag || ['script', 'style', 'svg', 'noscript', 'iframe'].includes(tag)) return '';
    if (el.id === 'verdant-drawer-container' || (el.closest && el.closest('#verdant-drawer-container'))) return '';

    const indent = '  '.repeat(depth);
    let idAttr = el.id ? `#${el.id}` : '';
    let classAttr = el.classList && el.classList.length > 0 ? `.${Array.from(el.classList).slice(0, 2).join('.')}` : '';
    let text = (el.childNodes.length === 1 && el.childNodes[0].nodeType === 3) ? ` "${el.textContent.trim().slice(0, 30)}"` : '';

    let result = `${indent}<${tag}${idAttr}${classAttr}>${text}\n`;

    if (depth < maxDepth && el.children) {
      const childCount = Math.min(el.children.length, 6);
      for (let i = 0; i < childCount; i++) {
        result += buildDomSkeleton(el.children[i], depth + 1, maxDepth);
      }
      if (el.children.length > 6) {
        result += `${indent}  <!-- +${el.children.length - 6} more child nodes -->\n`;
      }
    }
    return result;
  }

  function extractPageDomSummary() {
    const allEls = document.querySelectorAll('*');
    const totalNodes = allEls.length;
    
    // Landmark Regions
    const landmarks = {};
    const header = document.querySelector('header, [role="banner"], .header, .navbar');
    if (header) landmarks.header = { tag: header.tagName.toLowerCase(), id: header.id, class: header.className?.toString().slice(0, 40) };
    
    const nav = document.querySelector('nav, [role="navigation"], .nav, .menu');
    if (nav) landmarks.nav = { tag: nav.tagName.toLowerCase(), linkCount: nav.querySelectorAll('a').length };
    
    const main = document.querySelector('main, [role="main"], #main, .main-content, #content, [id*="content"]');
    if (main) landmarks.main = { tag: main.tagName.toLowerCase(), id: main.id, childCount: main.children.length };
    
    const footer = document.querySelector('footer, [role="contentinfo"], .footer');
    if (footer) landmarks.footer = { tag: footer.tagName.toLowerCase(), id: footer.id };

    // Interactive element counts
    const forms = document.querySelectorAll('form').length;
    const buttons = document.querySelectorAll('button, [role="button"], input[type="submit"], input[type="button"]').length;
    const inputs = document.querySelectorAll('input:not([type="hidden"]), select, textarea').length;
    const links = document.querySelectorAll('a[href]').length;
    const images = document.querySelectorAll('img').length;

    // Detect broken images
    const brokenImages = [];
    document.querySelectorAll('img').forEach(img => {
      if (img.complete && (img.naturalWidth === 0 || img.naturalHeight === 0) && img.src && !img.src.startsWith('data:')) {
        brokenImages.push({ src: img.src.slice(0, 100), alt: img.alt || '' });
      }
    });

    // Detect empty interactive buttons without label
    const emptyButtons = [];
    document.querySelectorAll('button, a[role="button"]').forEach(btn => {
      if (!btn.innerText?.trim() && !btn.getAttribute('aria-label') && !btn.querySelector('svg, img')) {
        emptyButtons.push(btn.outerHTML.slice(0, 100));
      }
    });

    // ContextPrism Pruned DOM Skeleton
    const rootTarget = main || document.body;
    const domSkeleton = rootTarget ? buildDomSkeleton(rootTarget, 0, 4) : '';

    return {
      totalNodes,
      landmarks,
      stats: { forms, buttons, inputs, links, images },
      brokenImages: brokenImages.slice(0, 5),
      emptyButtons: emptyButtons.slice(0, 3),
      domSkeleton: domSkeleton.slice(0, 2000)
    };
  }

  window.Verdant.inspectElementGeometry = inspectElementGeometry;
  window.Verdant.findActiveLayoutAnomalies = findActiveLayoutAnomalies;
  window.Verdant.extractPageDomSummary = extractPageDomSummary;
})();
