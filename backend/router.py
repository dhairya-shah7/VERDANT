import os
import re
try:
    import boto3
except ImportError:
    boto3 = None
from typing import Dict, Any, Tuple

class HybridAlexaBrain:
    """
    Intelligently routes every spoken utterance into either:
    1. EVERYDAY_QUERY: News, weather, sports, general knowledge, media, definitions.
    2. CONSEQUENTIAL_ACTION: Schedule mutations, cloud operations, service shutdowns, file edits.
    """
    def __init__(self):
        # Optional AWS Bedrock integration for live LLM reasoning when credentials exist
        self.bedrock_available = False
        try:
            if boto3 and (os.getenv("AWS_ACCESS_KEY_ID") or os.path.exists(os.path.expanduser("~/.aws/credentials"))):
                self.bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
                self.bedrock_available = True
        except Exception:
            self.bedrock_available = False

    def classify_and_extract(self, utterance: str) -> Dict[str, Any]:
        text = utterance.strip().lower()

        # 1. Check for Consequential System / Cloud Actions
        if any(w in text for w in ["close", "shutdown", "stop", "offline", "terminate", "kill", "reboot", "restart"]) and \
           any(w in text for w in ["db", "database", "server", "gateway", "cluster", "service", "node", "queue"]):
            target = "db_primary_eu" if any(w in text for w in ["eu", "db", "database"]) else "api_gateway_us"
            return {
                "route": "CONSEQUENTIAL_ACTION",
                "action": "SHUTDOWN",
                "target_id": target,
                "param": 0.0,
                "domain": "cloud_infrastructure",
                "raw_text": utterance
            }

        # 2. Check for Consequential Schedule / Calendar Actions
        if any(w in text for w in ["schedule", "block", "focus", "calendar", "cancel meeting", "clear my afternoon", "book"]):
            # Extract time parameter if present (defaulting to 14.5 = 2:30 PM)
            hour_param = 14.5
            if "2" in text or "2:00" in text or "2:30" in text:
                hour_param = 14.5
            elif "3" in text or "3:00" in text or "3:30" in text:
                hour_param = 15.5
            return {
                "route": "CONSEQUENTIAL_ACTION",
                "action": "SCHEDULE_BLOCK",
                "target_id": "personal_calendar",
                "param": hour_param,
                "domain": "schedule_commitment",
                "raw_text": utterance
            }

        # 3. Check for Consequential Simulation / Latency Shock
        if "what happens if" in text or "simulate" in text:
            return {
                "route": "CONSEQUENTIAL_ACTION",
                "action": "LATENCY_SPIKE",
                "target_id": "api_gateway_us",
                "param": 300.0,
                "domain": "cloud_infrastructure",
                "raw_text": utterance
            }

        # 4. Check for Everyday News
        if any(w in text for w in ["news", "headline", "briefing", "what's happening"]):
            return {
                "route": "EVERYDAY_QUERY",
                "sub_type": "NEWS",
                "topic": "technology",
                "raw_text": utterance
            }

        # 5. Check for Everyday Weather (Dynamic Location Extraction)
        if any(w in text for w in ["weather", "temperature", "forecast", "rain", "sunny"]):
            # Extract target location (e.g. "weather of India", "weather in Tokyo")
            loc_match = re.search(r'(?:weather|temperature|forecast|rain|sunny)(?:\s+(?:of|in|at|for))?\s+([a-zA-Z\s]+)', text)
            if loc_match and loc_match.group(1).strip():
                city = loc_match.group(1).strip()
                # Clean filler words
                for filler in ["today", "tomorrow", "now", "like", "please", "alexa"]:
                    city = re.sub(r'\b' + filler + r'\b', '', city, flags=re.I).strip()
            else:
                city = "Seattle"
            
            return {
                "route": "EVERYDAY_QUERY",
                "sub_type": "WEATHER",
                "city": city or "Seattle",
                "raw_text": utterance
            }

        # 6. All Other Queries (General Knowledge, Math, Sports, History, Conversation)
        return {
            "route": "EVERYDAY_QUERY",
            "sub_type": "KNOWLEDGE",
            "raw_text": utterance
        }
