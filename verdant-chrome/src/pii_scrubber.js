/**
 * V.E.R.D.A.N.T. Client-Side PII & Secret Scrubber
 * Ensures zero credentials, keys, or personal identifiers ever leave the user's browser.
 */

const PII_PATTERNS = [
  // 1. Bearer / JWT Tokens
  { regex: /Bearer\s+[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_=]*/gi, replacement: 'Bearer [REDACTED_JWT]' },
  // 2. AWS Keys
  { regex: /\bAKIA[0-9A-Z]{16}\b/g, replacement: '[REDACTED_AWS_KEY]' },
  // 3. GitHub PATs
  { regex: /\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}\b/g, replacement: '[REDACTED_GITHUB_PAT]' },
  // 4. Google API Keys
  { regex: /\bAIza[0-9A-Za-z\-_]{35}\b/g, replacement: '[REDACTED_GOOGLE_KEY]' },
  // 5. Generic Secrets & Passwords in Strings
  { regex: /((?:api[_-]?key|secret|token|password|passwd|auth)["']?\s*[:=]\s*["'])([^"']+)(["'])/gi, replacement: '$1[REDACTED_SECRET]$3' },
  // 6. Basic Auth in URLs
  { regex: /(https?:\/\/)([^:\s/@]+):([^@\s/]+)@/gi, replacement: '$1$2:[REDACTED_SECRET]@' },
  // 7. Credit Cards
  { regex: /\b(?:\d{4}[ -]?){3}\d{4}\b/g, replacement: '[REDACTED_CARD_NUMBER]' },
  // 8. Emails
  { regex: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b/g, replacement: '[REDACTED_EMAIL]' },
  // 9. Phone Numbers
  { regex: /\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/g, replacement: '[REDACTED_PHONE]' }
];

export function scrubText(text) {
  if (!text || typeof text !== 'string') return text || '';
  let sanitized = text;
  for (const { regex, replacement } of PII_PATTERNS) {
    sanitized = sanitized.replace(regex, replacement);
  }
  return sanitized;
}

export function scrubObject(obj) {
  if (!obj) return obj;
  if (typeof obj === 'string') return scrubText(obj);
  if (Array.isArray(obj)) return obj.map(scrubObject);
  if (typeof obj === 'object') {
    const clean = {};
    for (const [k, v] of Object.entries(obj)) {
      const lower = k.toLowerCase();
      if (lower.includes('password') || lower.includes('token') || lower.includes('secret') || lower.includes('auth') || lower.includes('cookie') || lower.includes('apikey')) {
        clean[k] = '[REDACTED_SENSITIVE_FIELD]';
      } else {
        clean[k] = scrubObject(v);
      }
    }
    return clean;
  }
  return obj;
}
