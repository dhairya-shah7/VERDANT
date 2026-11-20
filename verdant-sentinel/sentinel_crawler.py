"""
V.E.R.D.A.N.T. Autonomous Sentinel — Headless Synthetic Crawler
Powered by Playwright (Chromium).
Acts as an autonomous 'Ghost User' crawling staging/production builds in CI/CD.
Monitors:
- Uncaught runtime exceptions & console errors
- HTTP 4xx / 5xx network drops
- Responsive layout overflows (scrollWidth > clientWidth) across Desktop and Mobile viewports
"""
import asyncio
import json
import base64
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, Page, Browser


VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 667}
}


class SentinelCrawler:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.console_logs: List[Dict[str, Any]] = []
        self.network_errors: List[Dict[str, Any]] = []
        self.detected_defects: List[Dict[str, Any]] = []

    async def audit_url(self, path: str = "/", viewports: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Launches headless browser and scans the given path across specified viewports.
        """
        if viewports is None:
            viewports = ["desktop", "mobile"]

        target_url = f"{self.base_url}{path}" if path.startswith("/") else path
        print(f"[V.E.R.D.A.N.T. Sentinel] 🚀 Launching headless audit on: {target_url}")

        async with async_playwright() as p:
            browser: Browser = await p.chromium.launch(headless=True)
            
            for vp_name in viewports:
                vp = VIEWPORTS.get(vp_name, VIEWPORTS["desktop"])
                print(f"[V.E.R.D.A.N.T. Sentinel] 📱 Testing viewport: {vp_name.upper()} ({vp['width']}x{vp['height']})")
                
                context = await browser.new_context(
                    viewport={"width": vp["width"], "height": vp["height"]},
                    user_agent="Mozilla/5.0 (V.E.R.D.A.N.T. Autonomous Sentinel Bot)"
                )
                page: Page = await context.new_page()

                # Attach listeners
                page.on("console", lambda msg: self._handle_console(msg))
                page.on("pageerror", lambda err: self._handle_page_error(err, target_url, vp_name))
                page.on("response", lambda resp: self._handle_response(resp, target_url))

                try:
                    await page.goto(target_url, wait_until="networkidle", timeout=15000)
                except Exception as e:
                    # In case of network timeout, continue with DOM inspection
                    print(f"[V.E.R.D.A.N.T. Sentinel] Navigation note: {e}")

                # Give dynamic client scripts 1.5s to render
                await page.wait_for_timeout(1500)

                # Inspect DOM for Layout Overflows & Broken Elements
                overflow_elements = await self._scan_dom_entropy(page, vp_name)
                for el in overflow_elements:
                    # Capture screenshot of the defect
                    screenshot_bytes = await page.screenshot(full_page=False)
                    el["screenshot_b64"] = base64.b64encode(screenshot_bytes).decode("utf-8")
                    el["viewport"] = vp_name
                    el["url"] = target_url
                    self.detected_defects.append(el)

                await context.close()

            await browser.close()

        print(f"[V.E.R.D.A.N.T. Sentinel] ✅ Audit complete: {len(self.detected_defects)} defects found across {len(viewports)} viewports.")
        return self.detected_defects

    def _handle_console(self, msg):
        if msg.type in ["error", "warning"]:
            self.console_logs.append({
                "type": msg.type,
                "text": msg.text,
                "location": msg.location
            })

    def _handle_page_error(self, err, url: str, viewport: str):
        self.detected_defects.append({
            "type": "RUNTIME_CRASH",
            "message": str(err),
            "url": url,
            "viewport": viewport,
            "severity": "CRITICAL"
        })

    def _handle_response(self, resp, url: str):
        if resp.status >= 400:
            self.network_errors.append({
                "url": resp.url,
                "status": resp.status,
                "statusText": resp.status_text
            })

    async def _scan_dom_entropy(self, page: Page, vp_name: str) -> List[Dict[str, Any]]:
        """
        Executes in-browser JavaScript evaluation to mathematically identify layout clipping and overflow.
        """
        scan_script = """
        () => {
            const defects = [];
            const allElements = document.querySelectorAll('*');
            
            for (const el of allElements) {
                // Ignore script, style, SVG interiors, and invisible elements
                if (['SCRIPT', 'STYLE', 'SVG', 'PATH', 'HEAD', 'META'].includes(el.tagName)) continue;
                const rect = el.getBoundingClientRect();
                if (rect.width === 0 || rect.height === 0) continue;
                
                const style = window.getComputedStyle(el);
                if (style.display === 'none' || style.visibility === 'hidden') continue;

                // Mathematical Layout Overflow Test
                const scrollWidth = Math.ceil(el.scrollWidth);
                const clientWidth = Math.ceil(el.clientWidth);
                const hasOverflow = scrollWidth > (clientWidth + 2) && style.overflowX !== 'scroll' && style.overflowX !== 'auto';

                if (hasOverflow) {
                    defects.push({
                        type: 'LAYOUT_OVERFLOW',
                        tagName: el.tagName.toLowerCase(),
                        selector: el.id ? '#' + el.id : (el.className ? '.' + el.className.split(' ').filter(Boolean).join('.') : el.tagName.toLowerCase()),
                        textPreview: (el.innerText || '').substring(0, 80).trim(),
                        htmlSnippet: el.outerHTML.substring(0, 500),
                        geometry: {
                            width: Math.round(rect.width),
                            height: Math.round(rect.height),
                            scrollWidth: scrollWidth,
                            clientWidth: clientWidth,
                            overflowPixels: scrollWidth - clientWidth
                        },
                        computedStyles: {
                            display: style.display,
                            position: style.position,
                            overflow: style.overflow,
                            boxSizing: style.boxSizing,
                            whiteSpace: style.whiteSpace
                        }
                    });
                }
            }
            return defects.slice(0, 3); // Return top 3 layout defects per viewport
        }
        """
        return await page.evaluate(scan_script)
