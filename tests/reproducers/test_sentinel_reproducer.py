"""
Auto-generated Playwright Reproducer Test
Synthesized by V.E.R.D.A.N.T. Autonomous Sentinel
Protocol: RED -> GREEN Verification
"""
import pytest
from playwright.sync_api import Page, expect

def test_verify_layout_overflow(page: Page):
    # 1. Navigate to target URL
    page.goto("https://verdant-server-1042112525098.us-central1.run.app")
    page.wait_for_timeout(1000)

    # 2. Locate target element
    el = page.locator(".relative.w-full.overflow-hidden").first
    expect(el).to_be_visible()

    # 3. Assert zero horizontal overflow
    overflow_px = el.evaluate("""(node) => {
        return Math.max(0, node.scrollWidth - node.clientWidth);
    }""")

    assert overflow_px == 0, f"Layout overflow defect present: exceeded by {overflow_px}px"
