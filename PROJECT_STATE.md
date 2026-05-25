# Project State

## Snapshot Date

2026-05-24

## Repo Shape

- Monorepo with `apps/api` and `apps/web`
- SQLite-backed FastAPI backend with SQLAlchemy persistence
- React/Vite frontend with core editable planning workflows
- Continuity and doctrine docs under `docs/`

## Current Product Phase

- Phase 2A persistence is complete.
- Phase 2B editable workflows are materially in place.
- Current work sits in the Phase 2D/2E trust, advisor, and provenance layer.

## What Is Live

- Core POST/PATCH planning flows from the frontend
- Transient derived takeoffs from persisted design composition
- Trust and provenance visibility across major planning surfaces
- `/api/*` support with legacy route compatibility

## Current Next Product Target

Deepen provenance coverage across more entity fields and derived outputs while keeping takeoffs transient and preserving the planning-only boundary.

## Restore Model

- Discovery: `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, repo-local skills
- Operational: only the specific global skills and docs needed for the task
- Deep reference: detailed docs, continuity files, doctrine, ADRs, and historical handoffs only when relevant

## Current Continuity Risks

- Detailed continuity docs still exist and remain valuable, but they are too large to treat as mandatory startup context.
- Provenance coverage is still partial, so trust messaging must stay explicit.
- Migration discipline is still early-stage even though Alembic scaffolding exists.

## Canonical Detailed References

- Product and implementation state: `docs/CURRENT_STATE.md`
- Product next step: `docs/NEXT_STEPS.md`
- Active work: `docs/ACTIVE_TASKS.md`
- Continuity workflow: `docs/session-continuity/continuity-workflow.md`
