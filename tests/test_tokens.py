import os, sys, time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from google import genai
from google.genai import types
from src.config import CONFIG

client = genai.Client(api_key=CONFIG.GEMINI_API_KEY)

short_prompt = """
You are V.E.R.D.A.N.T. systems engine.
Inspect this UI defect: div.pricing-card > h3 (width 280px, scrollWidth 420px, text overflows container).
Return concise JSON:
{
  "action_type": "fix",
  "confidence": 0.98,
  "spoken_summary": "1 sentence spoken summary",
  "root_cause": "1 sentence technical root cause",
  "css_patch": "direct CSS rule",
  "edits": [{"path": "src/PricingCard.tsx", "search": "old", "replace": "new"}]
}
"""

t0 = time.time()
cfg = types.GenerateContentConfig(
    temperature=0.1,
    max_output_tokens=400,
    response_mime_type="application/json"
)
resp = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=short_prompt,
    config=cfg
)
dur = time.time() - t0
print(f"gemini-3.5-flash-lite with token limit: {dur:.2f}s")
print(resp.text)
