# Discovery Index

## Purpose

This file maps the smallest restore surface that can route a session without forcing a full documentation sweep.

## Discovery Layer

Read these first:

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `SESSION_HANDOFF.md`
4. `.codex/skills/repo-memory-map/SKILL.md` if present
5. `.codex/skills/repo-guardrails/SKILL.md` if present

## Operational References By Task

- Product or roadmap alignment:
  - `docs/CURRENT_STATE.md`
  - `docs/NEXT_STEPS.md`
  - `docs/ACTIVE_TASKS.md`
- Continuity maintenance:
  - `docs/session-continuity/continuity-workflow.md`
  - latest file in `docs/handoffs/`
- Architecture changes:
  - `docs/ARCHITECTURE.md`
  - task-relevant files in `docs/session-continuity/`
- Database or persistence changes:
  - `docs/DATABASE_SCHEMA.md`
  - `apps/api/app/core/models.py`
  - `apps/api/app/core/repository.py`
- API changes:
  - `docs/API_CONTRACTS.md`
  - task-relevant routers in `apps/api/app/**`
- Frontend behavior changes:
  - `apps/web/src/lib/api.js`
  - task-relevant pages/components

## Deep References

Load only when directly relevant:

- `docs/philosophy/*`
- `docs/adr/*`
- non-latest handoffs in `docs/handoffs/`
- broad `docs/session-continuity/*` sweeps

## Keep Unloaded By Default

- full doctrine sweeps
- full ADR sweeps
- historical handoff sweeps
- unrelated backend or frontend code trees
