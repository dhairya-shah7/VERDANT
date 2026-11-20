import time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from google import genai
from google.genai import types
from src.config import CONFIG

client = genai.Client(api_key=CONFIG.GEMINI_API_KEY)

test_prompt = """
Diagnose and synthesize a verified fix for an incident on: http://localhost:5173/products (Store Products).
VISUAL / LAYOUT DEFECT DETECTED ON ELEMENT:
- Selector: div.pricing-card > h3.plan-title
- Text: 'Enterprise Platinum Plus Tier Subscription Plan Annual Billing'
- Geometry: width=280px, height=65px, scrollWidth=420px, clientWidth=280px
- Overflow Flags: horizontal_overflow=True, vertical_overflow=False
- Computed CSS: display=flex, overflow=visible
REQUIREMENT: Return JSON with action_type, spoken_summary, root_cause, css_patch, edits.
"""

# Let's test the active models one by one:
for m in ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.8-flash"]:
    print(f"Testing {m}...", flush=True)
    t0 = time.time()
    try:
        cfg = types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json"
        )
        resp = client.models.generate_content(
            model=m,
            contents=test_prompt,
            config=cfg
        )
        elapsed = time.time() - t0
        print(f"[{m}] SUCCESS in {elapsed:.2f}s | Response: {resp.text[:80]}...", flush=True)
    except Exception as e:
        elapsed = time.time() - t0
        print(f"[{m}] FAILED in {elapsed:.2f}s: {e}", flush=True)
