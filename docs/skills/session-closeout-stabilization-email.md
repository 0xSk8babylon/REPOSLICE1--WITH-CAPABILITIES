# Session Closeout Stabilization Email

## Purpose

This planner-root operational skill makes session-report email delivery durable across long-running Codex sessions.

Use it when Matt asks for any final session report email, including:

- "email when done"
- "send session report"
- "send closeout report"
- "stabilization email"
- "session-closeout stabilization"
- "email the final status"
- "email after commit"

## Required Rule

If the session includes an email report request, Codex must not stop at implementation closeout. Codex must send a final stabilization report after final verification and/or commit actions are complete, unless Matt explicitly cancels the email request.

## Required Sequence

1. Complete the requested implementation, documentation, commit, or stabilization work.
2. Run the required verification for that work.
3. Run the planner-root email preflight:

```bash
bash scripts/check_session_report_email_env.sh
```

4. If the preflight passes, source `.env` in the active shell:

```bash
set -a
source .env
set +a
```

5. Send the stabilization report using existing repo tooling only. The current sender requires a report file path:

```bash
python3 scripts/send_session_report.py <final-report-file> --subject "<subject>"
```

If Matt did not specify a report artifact, use the final closeout, handoff, or session-report file produced for the session. Do not create product runtime email automation.

6. Final terminal output must include:

- whether the email was sent, or the exact non-secret failure reason
- message id if available
- final git status
- commit hashes and messages if commits were made
- no push confirmation if no push was approved
- risks and open items

## Safety Constraints

- Never print `RESEND_API_KEY`.
- Never modify `.env` unless Matt explicitly approves.
- Never stage `.env`.
- Never commit `.env`.
- Never add secrets.
- Never add product runtime email automation.
- Never change Resend sender, domain, or recipient settings unless Matt explicitly approves.
- Use existing repo session-report tooling only.
- If network approval is needed, request it clearly.
- If email fails, report the exact non-secret failure reason and do not claim email was sent.
- If email succeeds, record the message id if returned.

## Verification Checklist

Before final closeout for this skill or any future session using it:

```bash
git diff --check
bash scripts/check_session_report_email_env.sh
git status --short
git diff -- .env
git diff --cached -- .env
```

Confirm no secrets were added or printed and `.env` is untouched and unstaged.
