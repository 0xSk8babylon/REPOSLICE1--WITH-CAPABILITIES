"""Ops-only helper for sending session closeout reports through Resend."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


RESEND_EMAILS_URL = "https://api.resend.com/emails"
DEFAULT_TIMEOUT_SECONDS = 20
USER_AGENT = "residential-energy-planner-session-reporter/0.1"


class SessionReportEmailError(RuntimeError):
    """Raised when the session report email cannot be sent."""


@dataclass(frozen=True)
class SessionReportEmailSettings:
    api_key: str
    sender: str
    recipient: str
    endpoint: str = RESEND_EMAILS_URL


@dataclass(frozen=True)
class SessionReportEmailResult:
    message_id: Optional[str]
    status_code: int
    response: Mapping[str, Any]


UrlOpener = Callable[..., Any]


def settings_from_env(env: Optional[Mapping[str, str]] = None) -> SessionReportEmailSettings:
    values = env if env is not None else os.environ
    missing = [
        name
        for name in ("RESEND_API_KEY", "SESSION_REPORT_EMAIL_FROM", "SESSION_REPORT_EMAIL_TO")
        if not values.get(name)
    ]
    if missing:
        raise SessionReportEmailError("Missing required env var(s): " + ", ".join(missing))

    return SessionReportEmailSettings(
        api_key=values["RESEND_API_KEY"],
        sender=values["SESSION_REPORT_EMAIL_FROM"],
        recipient=values["SESSION_REPORT_EMAIL_TO"],
    )


def send_session_report_email(
    *,
    report_text: str,
    subject: str,
    settings: Optional[SessionReportEmailSettings] = None,
    opener: Optional[UrlOpener] = None,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> SessionReportEmailResult:
    """Send a plaintext session report email through the Resend email API."""

    if not report_text.strip():
        raise SessionReportEmailError("Session report file is empty.")
    if not subject.strip():
        raise SessionReportEmailError("Email subject is required.")

    email_settings = settings or settings_from_env()
    payload = {
        "from": email_settings.sender,
        "to": [email_settings.recipient],
        "subject": subject,
        "text": report_text,
    }
    request = Request(
        email_settings.endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {email_settings.api_key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )

    try:
        response = (opener or urlopen)(request, timeout=timeout_seconds)
        with response:
            status_code = getattr(response, "status", getattr(response, "code", 200))
            response_body = response.read().decode("utf-8")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SessionReportEmailError(f"Resend API returned HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise SessionReportEmailError(f"Unable to reach Resend API: {exc.reason}") from exc
    except OSError as exc:
        raise SessionReportEmailError(f"Unable to send session report email: {exc}") from exc

    parsed_response: Mapping[str, Any]
    if response_body:
        try:
            parsed_json = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise SessionReportEmailError("Resend API returned a non-JSON response.") from exc
        if not isinstance(parsed_json, dict):
            raise SessionReportEmailError("Resend API returned an unexpected JSON response.")
        parsed_response = parsed_json
    else:
        parsed_response = {}

    message_id = parsed_response.get("id") if isinstance(parsed_response, dict) else None
    return SessionReportEmailResult(
        message_id=message_id,
        status_code=int(status_code),
        response=parsed_response,
    )
