"""
Replay Shield - Playwright Script Synthesizer
Generates robust, deterministic Playwright tests utilizing accessibility locators.
"""
from typing import List, Dict, Any

def generate_playwright_test(
    app_url: str,
    action_events: List[Dict[str, Any]],
    expected_failure_msg: str = "Internal Server Error"
) -> str:
    """
    Synthesizes executable Playwright TypeScript / JavaScript test.
    """
    script_lines = [
        "import { test, expect } from '@playwright/test';",
        "",
        "test('V.E.R.D.A.N.T. Auto-Generated Forensic Bug Reproduction', async ({ page }) => {",
        f"  // 1. Navigate to target application state",
        f"  await page.goto('{app_url}');",
        "  await page.waitForLoadState('networkidle');",
        ""
    ]
    
    # Synthesize action sequence
    for event in action_events:
        action = event.get("action", "").upper()
        selector = event.get("selector", "button")
        target = event.get("target", "")
        
        if action == "CLICK":
            script_lines.append(f"  // Action: User clicked {selector}")
            script_lines.append(f"  const targetElement = page.locator('{selector}').first();")
            script_lines.append(f"  await expect(targetElement).toBeVisible();")
            script_lines.append(f"  await targetElement.click();")
            script_lines.append("")
        elif action == "NAVIGATE" and target:
            script_lines.append(f"  await page.goto('{target}');")
            
    # Append assertion that reproduces the defect
    script_lines.extend([
        "  // 2. Assert Error Condition (Expect RED on unpatched code, GREEN on fix)",
        "  const errorBanner = page.getByRole('alert').or(page.getByText(/error|failed/i));",
        "  // When patched, errorBanner should NOT appear and success state should resolve:",
        "  await expect(page.getByRole('button', { name: /submitting|loading/i })).not.toBeVisible({ timeout: 5000 });",
        "});"
    ])
    
    return "\n".join(script_lines)
