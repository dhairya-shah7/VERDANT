from playwright.sync_api import sync_playwright
import os

os.makedirs("demo_clips", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="demo_clips/",
        record_video_size={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    page.goto("http://127.0.0.1:8000")
    page.wait_for_timeout(3000)
    page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
    page.wait_for_timeout(2000)
    context.close()
    browser.close()

print("Playwright video recording test complete. Files in demo_clips:")
for f in os.listdir("demo_clips"):
    print(" -", f)
