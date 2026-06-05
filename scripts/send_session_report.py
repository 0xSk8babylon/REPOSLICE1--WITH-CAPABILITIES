#!/usr/bin/env python3
"""Manually send a session closeout report file to the configured recipient."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from session_report_email import SessionReportEmailError, send_session_report_email


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send an ops-only session closeout report email.")
    parser.add_argument("report_file", type=Path, help="Path to a markdown or text session report file.")
    parser.add_argument(
        "--subject",
        help="Email subject. Defaults to 'Session closeout report: <filename>'.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_file = args.report_file
    if not report_file.exists():
        print(f"Session report file not found: {report_file}", file=sys.stderr)
        return 2
    if not report_file.is_file():
        print(f"Session report path is not a file: {report_file}", file=sys.stderr)
        return 2

    try:
        report_text = report_file.read_text(encoding="utf-8")
        subject = args.subject or f"Session closeout report: {report_file.name}"
        result = send_session_report_email(report_text=report_text, subject=subject)
    except OSError as exc:
        print(f"Unable to read session report file: {exc}", file=sys.stderr)
        return 2
    except SessionReportEmailError as exc:
        print(f"Unable to send session report email: {exc}", file=sys.stderr)
        return 1

    message_ref = result.message_id or f"HTTP {result.status_code}"
    print(f"Session report email sent: {message_ref}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
