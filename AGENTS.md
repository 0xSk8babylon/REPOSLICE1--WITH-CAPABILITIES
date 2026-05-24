# AGENTS

## Scope

This repository is an isolated project memory boundary for `residential-energy-planner`.

- Do not import assumptions, APIs, workflows, or architecture from other repositories.
- Preserve continuity and modular architecture before making local optimizations.
- Prefer additive changes over rewrites.

## Canonical Memory Order

At session start, read these files in order:

1. `docs/PROJECT_OVERVIEW.md`
2. `docs/CURRENT_STATE.md`
3. `docs/NEXT_STEPS.md`
4. `docs/ARCHITECTURE.md`
5. `docs/DATABASE_SCHEMA.md`
6. `docs/API_CONTRACTS.md`
7. `docs/ACTIVE_TASKS.md`
8. `docs/SESSION_LOG.md`
9. `docs/session-continuity/*`
10. Latest file in `docs/handoffs/`

If any of those files are missing or stale, treat that as a continuity defect and repair it before making broader architecture changes.

## Operating Principles

- Structured facts are authoritative.
- Deterministic rules and calculations must remain inspectable.
- AI is an explanation and orchestration layer, not a source of product facts.
- Existing frontend GET contracts are compatibility-sensitive.
- `/api/*` is the preferred API base path.
- Placeholder values must remain clearly labeled as placeholders.

## Current Phase Expectations

- SQLite is the local development system of record.
- Auth, billing, NEC automation, and permitting remain deferred.
- The frontend has moved beyond read-only and now exercises core POST/PATCH flows.
- Demo seed data remains valid for first-run continuity, but it is not factual authority.

## End-Of-Session Requirements

Before stopping work:

- update `docs/CURRENT_STATE.md`
- update `docs/NEXT_STEPS.md`
- update `docs/ACTIVE_TASKS.md` if task status changed
- append `docs/SESSION_LOG.md`
- update `docs/session-continuity/*` if architecture, persistence, roadmap, or pressure points changed
- create a dated handoff in `docs/handoffs/`

## Non-Goals

- Do not quietly redesign the architecture.
- Do not replace structured persistence with prompt-only memory.
- Do not present placeholder engineering logic as verified truth.
