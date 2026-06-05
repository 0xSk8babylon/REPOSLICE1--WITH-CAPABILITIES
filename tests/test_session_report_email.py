import json
import unittest
from pathlib import Path
from urllib.error import HTTPError

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from session_report_email import (  # noqa: E402
    RESEND_EMAILS_URL,
    SessionReportEmailError,
    SessionReportEmailSettings,
    USER_AGENT,
    send_session_report_email,
    settings_from_env,
)


class FakeResponse:
    status = 200

    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self.body

    def close(self):
        return None


class SessionReportEmailTests(unittest.TestCase):
    def test_settings_from_env_requires_all_expected_values(self):
        with self.assertRaisesRegex(SessionReportEmailError, "RESEND_API_KEY"):
            settings_from_env({})

    def test_send_session_report_email_posts_plaintext_report_to_resend(self):
        captured = {}

        def fake_opener(request, timeout):
            captured["request"] = request
            captured["timeout"] = timeout
            return FakeResponse(b'{"id":"email_123"}')

        settings = SessionReportEmailSettings(
            api_key="test_key",
            sender="agent@example.com",
            recipient="matt@example.com",
        )
        result = send_session_report_email(
            report_text="# Closeout\n\nDone.",
            subject="Session closeout",
            settings=settings,
            opener=fake_opener,
            timeout_seconds=7,
        )

        request = captured["request"]
        payload = json.loads(request.data.decode("utf-8"))

        self.assertEqual("email_123", result.message_id)
        self.assertEqual(200, result.status_code)
        self.assertEqual(RESEND_EMAILS_URL, request.full_url)
        self.assertEqual("POST", request.get_method())
        self.assertEqual("Bearer test_key", request.headers["Authorization"])
        self.assertEqual(USER_AGENT, request.headers["User-agent"])
        self.assertEqual("agent@example.com", payload["from"])
        self.assertEqual(["matt@example.com"], payload["to"])
        self.assertEqual("Session closeout", payload["subject"])
        self.assertEqual("# Closeout\n\nDone.", payload["text"])
        self.assertEqual(7, captured["timeout"])

    def test_send_session_report_email_rejects_empty_report(self):
        with self.assertRaisesRegex(SessionReportEmailError, "empty"):
            send_session_report_email(
                report_text=" ",
                subject="Session closeout",
                settings=SessionReportEmailSettings(
                    api_key="test_key",
                    sender="agent@example.com",
                    recipient="matt@example.com",
                ),
            )

    def test_send_session_report_email_wraps_resend_http_errors_without_api_key(self):
        def fake_opener(request, timeout):
            raise HTTPError(
                request.full_url,
                401,
                "Unauthorized",
                hdrs=None,
                fp=FakeResponse(b'{"message":"invalid api key"}'),
            )

        with self.assertRaises(SessionReportEmailError) as exc:
            send_session_report_email(
                report_text="Closeout",
                subject="Session closeout",
                settings=SessionReportEmailSettings(
                    api_key="secret_test_key",
                    sender="agent@example.com",
                    recipient="matt@example.com",
                ),
                opener=fake_opener,
            )

        self.assertIn("HTTP 401", str(exc.exception))
        self.assertNotIn("secret_test_key", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
