# Project State

## Snapshot Date

2026-05-25

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
- Structured provenance summaries on load and estimated pathway records
- A deterministic resilience recommendation-profile layer now exists in the advisor architecture
- A first internal battery sizing rule layer now exists behind the recommendation profiles
- A first internal solar sizing and recovery rule layer now exists behind the recommendation profiles
- Recommendation profile, battery sizing, and solar sizing outputs now include additive inspectability/provenance metadata describing basis signals, estimated inputs, incomplete inputs, and planning-only confidence posture
- Solar sizing now includes a first coarse site-aware adjustment layer using recorded roof placement, fallback shading caution, coarse seasonal region posture, and install-path realism signals
- Solar guidance now also includes an explicit roof-data-completeness and roof-measurement-confidence layer that distinguishes inferred placement realism from future measured roof geometry
- Recommendation outputs now also include a preliminary panel/service architecture layer that constrains backup design direction before inverter, smart-panel modifier, or generator sizing
- Recommendation outputs now also include an explicit deterministic backup-load selection layer that distinguishes recorded load grouping from the currently selected planning scope before battery, solar, or backup-architecture guidance is interpreted
- The Design Advisor now surfaces panel/service planning-direction confidence and inspectability more explicitly, and seeded advisor states now have minimal backend regression coverage
- `/api/*` support with legacy route compatibility

## Current Next Product Target

Extend profile-based planning guidance into the next architecture-fit and equipment-mix recommendation slice while keeping formulas internal, provenance-aware, and planning-only, now that backup-load selection, panel/service posture, roof-capacity certainty, and current panel/service trust framing are each explicit layers.

## Restore Model

- Discovery: `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, repo-local skills
- Operational: only the specific global skills and docs needed for the task
- Deep reference: detailed docs, continuity files, doctrine, ADRs, and historical handoffs only when relevant

## Current Continuity Risks

- Detailed continuity docs still exist and remain valuable, but they are too large to treat as mandatory startup context.
- Provenance coverage is still partial, so trust messaging must stay explicit.
- Migration discipline is still early-stage even though Alembic scaffolding exists.
- Existing local databases may need reseeding to surface the new seeded backup-load-selection rule provenance record.

## Canonical Detailed References

- Product and implementation state: `docs/CURRENT_STATE.md`
- Product next step: `docs/NEXT_STEPS.md`
- Active work: `docs/ACTIVE_TASKS.md`
- Continuity workflow: `docs/session-continuity/continuity-workflow.md`
