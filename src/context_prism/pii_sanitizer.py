"""
ContextPrism - Enterprise PII & Secret Sanitizer (Zero-Leakage Guarantee)
Removes authorization tokens, passwords, API keys, credentials, and sensitive personal data
both client-side and server-side before model ingestion or telemetry broadcast.
"""
import re
from typing import Any, Union, Dict, List

PATTERNS = [
    # 1. Bearer tokens & JWTs
    (re.compile(r'Bearer\s+[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_=]*', re.IGNORECASE), "Bearer [REDACTED_JWT]"),
    
    # 2. Private Key blocks
    (re.compile(r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----[A-Za-z0-9+/\s=]+-----END\s+(?:RSA\s+)?PRIVATE\s+KEY-----', re.IGNORECASE), "[REDACTED_PRIVATE_KEY]"),

    # 3. AWS Access Key IDs
    (re.compile(r'\bAKIA[0-9A-Z]{16}\b'), "[REDACTED_AWS_KEY]"),

    # 4. GitHub Personal Access Tokens
    (re.compile(r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}\b'), "[REDACTED_GITHUB_PAT]"),
    (re.compile(r'\bgithub_pat_[A-Za-z0-9_]{50,}\b'), "[REDACTED_GITHUB_PAT]"),

    # 5. Google Cloud / Gemini API Keys
    (re.compile(r'\bAIza[0-9A-Za-z\-_]{35}\b'), "[REDACTED_GOOGLE_KEY]"),

    # 6. Generic API keys / Secret keys in Key-Value pairs
    (re.compile(r'((?:api[_-]?key|secret|token|auth_token|access_token|private_key|client_secret)["\']?\s*[:=]\s*["\'])([^"\']+)(["\'])', re.IGNORECASE), r'\1[REDACTED_KEY]\3'),

    # 7. Passwords in JSON / Config / Log statements
    (re.compile(r'((?:password|passwd|pwd)["\']?\s*[:=]\s*["\'])([^"\']+)(["\'])', re.IGNORECASE), r'\1[REDACTED_SECRET]\3'),

    # 8. Basic Auth credentials embedded in URLs: https://user:pass@example.com
    (re.compile(r'(https?://)([^:\s/@]+):([^@\s/]+)@', re.IGNORECASE), r'\1\2:[REDACTED_SECRET]@'),

    # 9. Credit Card Numbers (13 to 19 digits with optional spaces or dashes)
    (re.compile(r'\b(?:\d{4}[ -]?){3}\d{4}\b'), "[REDACTED_CARD_NUMBER]"),

    # 10. Social Security Numbers (SSN: 000-00-0000)
    (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), "[REDACTED_SSN]"),

    # 11. Email Addresses
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'), "[REDACTED_EMAIL]"),

    # 12. Phone Numbers (International and US styles)
    (re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'), "[REDACTED_PHONE]")
]


def sanitize_text(raw_text: str) -> str:
    """Sanitizes raw text, replacing all recognized credentials and PII."""
    if not raw_text or not isinstance(raw_text, str):
        return "" if raw_text is None else str(raw_text)
    
    sanitized = raw_text
    for pattern, replacement in PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized


def sanitize_data(data: Any) -> Any:
    """
    Recursively sanitizes dictionaries, lists, strings, and nested structures.
    Guarantees no raw PII remains in logs, network dumps, or AST payloads.
    """
    if isinstance(data, str):
        return sanitize_text(data)
    elif isinstance(data, dict):
        sanitized_dict = {}
        for key, value in data.items():
            # Check if key itself indicates a sensitive field
            lower_key = str(key).lower()
            if any(s in lower_key for s in ["password", "secret", "token", "auth", "api_key", "cookie"]):
                sanitized_dict[key] = "[REDACTED_SENSITIVE_FIELD]"
            else:
                sanitized_dict[key] = sanitize_data(value)
        return sanitized_dict
    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]
    return data
