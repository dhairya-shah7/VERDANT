"""
Engine A - Google Gemini Multimodal Diagnostic Interface
Sends structured event context & logs to Google Gemini, receiving typed JSON diagnostics.
No hardcoded fallbacks or mock responses: strictly model-driven inference.
"""
import os
import json
from typing import Dict, Any, List
from google import genai
from google.genai import types, errors
from ..config import CONFIG

def get_genai_client() -> genai.Client:
    """Initializes official Google GenAI client with configured API key."""
    api_key = CONFIG.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. Please provide a valid Gemini API key in .env or environment variables."
        )
    return genai.Client(api_key=api_key)

def analyze_defect_with_gemini(
    timeline_events: List[Dict[str, Any]],
    network_errors: List[Dict[str, Any]],
    console_errors: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Invokes Google Gemini with structured JSON output enforcement.
    Uses verified active models (gemini-3.5-flash and gemini-3.5-flash-lite).
    Throws exception on total failure to guarantee zero synthetic/hardcoded mock data.
    """
    client = get_genai_client()
    
    prompt_text = (
        "You are V.E.R.D.A.N.T., an elite autonomous debugging agent developed for Google DeepMind & Google Cloud.\n"
        "Analyze the following timeline events, console errors, and network logs to diagnose the defect.\n\n"
        f"Timeline Events: {json.dumps(timeline_events, indent=2)}\n"
        f"Network Failures: {json.dumps(network_errors, indent=2)}\n"
        f"Console Errors: {json.dumps(console_errors, indent=2)}\n\n"
        "Return a valid JSON object matching this schema exactly:\n"
        "{\n"
        '  "bug_detected": true,\n'
        '  "user_action_attempted": true,\n'
        '  "intent": "<Concise description of user intent>",\n'
        '  "category": "<Exact failure category, e.g. API_ENDPOINT_FAILURE, AUTH_TOKEN_EXPIRED, STATE_SYNC_ERROR>",\n'
        '  "suspect_file": "<Repo-relative filepath causing the issue>",\n'
        '  "suggested_fix_diff": "<Unified diff or code replacement showing the surgical fix>",\n'
        '  "explanation": "<Clear technical root cause analysis explaining why the error occurred>"\n'
        "}"
    )

    models_to_try = [CONFIG.GEMINI_MODEL, CONFIG.GEMINI_FAST_MODEL]
    # Filter out empty or duplicate model names
    models_to_try = [m for i, m in enumerate(models_to_try) if m and m not in models_to_try[:i]]

    last_exception = None

    for model_name in models_to_try:
        try:
            config = types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json"
            )
            response = client.models.generate_content(
                model=model_name,
                contents=prompt_text,
                config=config
            )
            
            if not response.text:
                raise ValueError(f"Model {model_name} returned an empty response")
                
            raw_text = response.text.strip()
            # Clean possible markdown wrapping if returned
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

            parsed = json.loads(raw_text)
            
            # Validate required keys
            required_keys = ["bug_detected", "intent", "category", "suspect_file", "suggested_fix_diff", "explanation"]
            for key in required_keys:
                if key not in parsed:
                    raise ValueError(f"Model response missing required key '{key}'")
                    
            print(f"[V.E.R.D.A.N.T. Live AI] Successfully diagnosed by {model_name}")
            return parsed

        except errors.APIError as e:
            print(f"[DEBUG] Google Gemini API error with model {model_name}: {e}")
            last_exception = e
            continue
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[DEBUG] Parsing error with model {model_name}: {e}")
            last_exception = e
            continue
        except Exception as e:
            print(f"[DEBUG] Unexpected error with model {model_name}: {e}")
            last_exception = e
            continue

    raise RuntimeError(
        f"All live Google Gemini model attempts failed. Last error: {last_exception}. "
        "No fallback mock data will be used."
    )
