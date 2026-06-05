#!/usr/bin/env bash
set -e

cd "${HOME}/residential-energy-planner"

if [ ! -f ".env" ]; then
  echo ".env is missing" >&2
  echo "Missing required env var: SESSION_REPORT_EMAIL_FROM" >&2
  echo "Missing required env var: SESSION_REPORT_EMAIL_TO" >&2
  echo "Missing required env var: RESEND_API_KEY" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

echo "FROM=${SESSION_REPORT_EMAIL_FROM:-}"
echo "TO=${SESSION_REPORT_EMAIL_TO:-}"
test -n "${RESEND_API_KEY:-}" && echo "RESEND_API_KEY is loaded" || echo "RESEND_API_KEY is missing"

missing=0

if [ -z "${SESSION_REPORT_EMAIL_FROM:-}" ]; then
  echo "Missing required env var: SESSION_REPORT_EMAIL_FROM" >&2
  missing=1
fi

if [ -z "${SESSION_REPORT_EMAIL_TO:-}" ]; then
  echo "Missing required env var: SESSION_REPORT_EMAIL_TO" >&2
  missing=1
fi

if [ -z "${RESEND_API_KEY:-}" ]; then
  echo "Missing required env var: RESEND_API_KEY" >&2
  missing=1
fi

exit "${missing}"
