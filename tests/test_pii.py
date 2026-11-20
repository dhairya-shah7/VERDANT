"""
Unit test suite for enterprise PII and Secret Sanitization.
"""
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import unittest
from src.context_prism.pii_sanitizer import sanitize_text, sanitize_data

class TestPIISanitizer(unittest.TestCase):
    def test_jwt_redaction(self):
        raw = "User logged in with Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.doNotLeakThisToken"
        sanitized = sanitize_text(raw)
        self.assertNotIn("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", sanitized)
        self.assertIn("Bearer [REDACTED_JWT]", sanitized)

    def test_aws_key_redaction(self):
        raw = "Error connecting to S3 with key AKIAIOSFODNN7EXAMPLE"
        sanitized = sanitize_text(raw)
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", sanitized)
        self.assertIn("[REDACTED_AWS_KEY]", sanitized)

    def test_github_pat_redaction(self):
        raw = "git clone https://ghp_123456789012345678901234567890123456@github.com/repo"
        sanitized = sanitize_text(raw)
        self.assertNotIn("ghp_123456789012345678901234567890123456", sanitized)
        self.assertIn("[REDACTED_GITHUB_PAT]", sanitized)

    def test_credit_card_and_email(self):
        raw = "Contact alice@company.org or use card 4532-1488-2931-9921 for transaction."
        sanitized = sanitize_text(raw)
        self.assertNotIn("alice@company.org", sanitized)
        self.assertNotIn("4532-1488-2931-9921", sanitized)
        self.assertIn("[REDACTED_EMAIL]", sanitized)
        self.assertIn("[REDACTED_CARD_NUMBER]", sanitized)

    def test_nested_data_sanitization(self):
        payload = {
            "user": "john_doe",
            "email": "john@test.com",
            "auth_token": "secret_abc_123",
            "profile": {
                "password": "SuperSecretPassword123!",
                "notes": "Called at 555-867-5309"
            }
        }
        sanitized = sanitize_data(payload)
        self.assertEqual(sanitized["auth_token"], "[REDACTED_SENSITIVE_FIELD]")
        self.assertEqual(sanitized["profile"]["password"], "[REDACTED_SENSITIVE_FIELD]")
        self.assertIn("[REDACTED_PHONE]", sanitized["profile"]["notes"])
        self.assertIn("[REDACTED_EMAIL]", sanitized["email"])

if __name__ == "__main__":
    unittest.main()
