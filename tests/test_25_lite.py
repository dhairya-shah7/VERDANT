import os, sys, time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from google import genai
from google.genai import types
from src.config import CONFIG

client = genai.Client(api_key=CONFIG.GEMINI_API_KEY)

for m in ["gemini-2.5-flash-lite", "gemini-3.5-flash-lite"]:
    t0 = time.time()
    try:
        r = client.models.generate_content(
            model=m,
            contents='Return JSON: {"ok": true}',
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        print(f"[{m}] SUCCESS in {time.time()-t0:.2f}s -> {r.text.strip()}")
    except Exception as e:
        print(f"[{m}] FAILED in {time.time()-t0:.2f}s -> {e}")
