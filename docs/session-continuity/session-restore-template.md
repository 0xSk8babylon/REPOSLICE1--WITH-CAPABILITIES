# Session Restore Template

Status: retained as a compatibility stub. The canonical restore procedure now lives in `docs/session-continuity/continuity-workflow.md`, and startup routing now begins from the root discovery layer.

## Purpose

Use this file only if you need a longer-form restore checklist after the discovery layer was insufficient.

## Compact Restore First

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `SESSION_HANDOFF.md`
4. `discovery-index.md`
5. repo-local skills in `.codex/skills/`

Then follow `docs/session-continuity/continuity-workflow.md`.

## If More Context Is Needed

Escalate to deeper references selectively:

- product state: `docs/CURRENT_STATE.md`, `docs/NEXT_STEPS.md`, `docs/ACTIVE_TASKS.md`
- architecture: `docs/ARCHITECTURE.md`
- database: `docs/DATABASE_SCHEMA.md`
- API: `docs/API_CONTRACTS.md`
- doctrine: only the specific philosophy or ADR files relevant to the change
- historical context: latest file in `docs/handoffs/`
