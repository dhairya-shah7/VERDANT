from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="demo_clips/",
        record_video_size={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    page.goto("http://127.0.0.1:8000")
    page.wait_for_timeout(1000)

    # Inject drawer CSS and JS
    with open("verdant-chrome/drawer.css", "r", encoding="utf-8") as f:
        drawer_css = f.read()
    page.add_style_tag(content=drawer_css)

    with open("verdant-chrome/src/visual_crawler.js", "r", encoding="utf-8") as f:
        vc_js = f.read()
    page.add_script_tag(content=vc_js)

    with open("verdant-chrome/src/in_tab_patcher.js", "r", encoding="utf-8") as f:
        itp_js = f.read()
    page.add_script_tag(content=itp_js)

    with open("verdant-chrome/drawer.js", "r", encoding="utf-8") as f:
        drawer_js = f.read()
    page.add_script_tag(content=drawer_js)

    page.wait_for_timeout(500)
    page.evaluate("window.Verdant.toggleDrawer(true)")
    page.wait_for_timeout(2000)

    # Simulate triggering analysis
    page.evaluate("""
        window.Verdant.displayDiagnosis({
            spoken_summary: 'Layout Overflow Detected on Navigation Bar',
            root_cause: 'The brand logo container overflows by 38px on viewport boundaries, pushing interactive nav links off-screen.',
            action_type: 'fix',
            confidence: 'HIGH',
            model_used: 'gemini-3.5-flash-lite',
            css_patch: 'header nav { overflow: hidden !important; max-width: 100% !important; }',
            edits: [{
                path: 'src/components/Header.css',
                replace: 'header nav { overflow: hidden; max-width: 100%; }'
            }],
            energy_saved_wh: 124.5,
            water_saved_ml: 236.8
        });
    """)
    page.wait_for_timeout(2500)

    # Click Test Fix Live
    page.click("#verdant-btn-test-live")
    page.wait_for_timeout(2500)

    context.close()
    browser.close()

print("Drawer record test complete!")
