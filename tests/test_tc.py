import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from google import genai
from google.genai import types
from src.config import CONFIG

client = genai.Client(api_key=CONFIG.GEMINI_API_KEY)

# Without thinking_config
try:
    r = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents='Return JSON {"test": true}',
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    print("SUCCESS WITHOUT thinking_config:", r.text.strip())
except Exception as e:
    print("FAILED WITHOUT thinking_config:", e)

# With thinking_config
try:
    r = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents='Return JSON {"test": true}',
        config=types.GenerateContentConfig(response_mime_type="application/json", thinking_config=types.ThinkingConfig(thinking_budget=0))
    )
    print("SUCCESS WITH thinking_config:", r.text.strip())
except Exception as e:
    print("FAILED WITH thinking_config:", e)
