"""
ContextPrism - Log & Network HAR Parser
Normalizes raw browser console output and HTTP archive logs into structured forensic events.
"""
import json
from typing import List, Dict, Any
from .pii_sanitizer import sanitize_text

def parse_console_logs(raw_logs: str) -> List[Dict[str, Any]]:
    """
    Extracts uncaught exceptions, 500s, and runtime errors from console dumps.
    """
    events = []
    if not raw_logs:
        return events
        
    lines = raw_logs.strip().split("\n")
    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        is_error = any(kw in line.lower() for kw in ["error", "exception", "failed", "uncaught", "typeerror"])
        if is_error:
            events.append({
                "type": "CONSOLE_ERROR",
                "line_number": idx + 1,
                "message": sanitize_text(line),
                "severity": "HIGH" if "uncaught" in line.lower() else "MEDIUM"
            })
    return events

def parse_har_network(har_data: Any) -> List[Dict[str, Any]]:
    """
    Extracts failed HTTP requests (4xx, 5xx) from Network HAR data.
    """
    failures = []
    if isinstance(har_data, str):
        try:
            har_data = json.loads(har_data)
        except Exception:
            return failures

    entries = har_data.get("log", {}).get("entries", []) if isinstance(har_data, dict) else []
    for entry in entries:
        req = entry.get("request", {})
        resp = entry.get("response", {})
        status = resp.get("status", 0)
        
        # Flag HTTP 4xx or 5xx failures
        if status >= 400:
            failures.append({
                "type": "NETWORK_FAILURE",
                "url": sanitize_text(req.get("url", "")),
                "method": req.get("method", "GET"),
                "status": status,
                "status_text": resp.get("statusText", ""),
                "time_ms": entry.get("time", 0)
            })
    return failures
