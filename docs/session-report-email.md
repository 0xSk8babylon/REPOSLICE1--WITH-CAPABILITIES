# Session Report Email Preflight

## Purpose

Session-report email delivery is ops-only. It uses the existing scripts under `scripts/` and is not product runtime email automation.

When Matt asks for "email when done", "send report", "send session report", or similar, Codex must run the active-shell preflight from the planner root before attempting delivery.

For long-running session closeout behavior, use the operational skill checklist in `docs/skills/session-closeout-stabilization-email.md`.

## Required Preflight

Run exactly:

```bash
cd ~/residential-energy-planner
set -a
source .env
set +a

echo "FROM=$SESSION_REPORT_EMAIL_FROM"
echo "TO=$SESSION_REPORT_EMAIL_TO"
test -n "$RESEND_API_KEY" && echo "RESEND_API_KEY is loaded" || echo "RESEND_API_KEY is missing"
```

Equivalent helper:

```bash
bash scripts/check_session_report_email_env.sh
```

## Required Behavior

- If `FROM` is empty, stop and report `SESSION_REPORT_EMAIL_FROM` missing.
- If `TO` is empty, stop and report `SESSION_REPORT_EMAIL_TO` missing.
- If `RESEND_API_KEY` is missing, stop and report `RESEND_API_KEY` missing.
- Never print `RESEND_API_KEY`.
- Never modify, stage, or commit `.env`.
- Use only the existing repo session-report tooling.
- Do not change Resend sender, domain, recipient, or external service configuration.
- If email fails, report the exact non-secret failure reason.
- If email succeeds, final closeout must explicitly say email sent.

## Send Command

After preflight passes, send an existing report artifact with:

```bash
python3 scripts/send_session_report.py <report-file> --subject "<subject>"
```
