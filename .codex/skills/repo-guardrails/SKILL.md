---
name: repo-guardrails
description: Apply repository-specific operational guardrails without forcing a full documentation restore.
---

# Repo Guardrails

## Product Boundaries

- Structured facts are authoritative.
- AI explains and orchestrates; it does not invent product facts.
- Placeholder values must remain clearly labeled.
- Planning completeness must not be presented as engineering readiness.

## Technical Guardrails

- Existing frontend GET contracts are compatibility-sensitive.
- Prefer `/api/*` for current and future API work.
- SQLite is the local development system of record.
- `data_origin` distinctions must remain explicit.
- Auth, billing, NEC automation, and permitting remain deferred.

## Continuity Guardrails

- Update root discovery files when session state materially changes.
- Update only the detailed continuity docs affected by the change.
- Create a dated handoff at the end of meaningful implementation sessions.
- Load philosophy and ADR docs only when the task touches strategic doctrine or trust boundaries.
