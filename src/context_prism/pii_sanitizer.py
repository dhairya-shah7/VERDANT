"""
ContextPrism - PII & Secret Sanitizer
Removes authorization tokens, passwords, API keys, and sensitive data before model ingestion.
"""
import re

PATTERNS = [
    # Bearer tokens & JWTs
    (re.compile(r'Bearer\s+[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_=]*', re.IGNORECASE), "Bearer [REDACTED_JWT]"),
    # Passwords in URLs or JSON
    (re.compile(r'(password["\']?\s*[:=]\s*["\'])([^"\']+)(["\'])', re.IGNORECASE), r'\1[REDACTED_SECRET]\3'),
    # Generic API Keys / Secrets
    (re.compile(r'(api[_-]?key["\']?\s*[:=]\s*["\'])([^"\']+)(["\'])', re.IGNORECASE), r'\1[REDACTED_KEY]\3'),
    # Credit Card Numbers
    (re.compile(r'\b(?:\d{4}[ -]?){3}\d{4}\b'), "[REDACTED_CARD_NUMBER]")
]

def sanitize_text(raw_text: str) -> str:
    """Sanitizes text, removing credentials and PII."""
    if not raw_text:
        return ""
    sanitized = raw_text
    for pattern, replacement in PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized
