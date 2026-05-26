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
- Backup-load selection now also classifies outage posture from recorded load coverage, exposes planning-only scope confidence, and distinguishes critical-load, partial-home, and whole-home candidates without inferring missing load grouping
- The Design Advisor now surfaces panel/service planning-direction confidence and inspectability more explicitly, and seeded advisor states now have minimal backend regression coverage
- Panel/service guidance now also includes an additive architecture-consistency check so broader backup direction stays bounded by recorded outage posture and design-goal intent
- Recommendation profiles now also include an additive architecture-fit tradeoff layer that explains how recorded equipment mix, outage posture, and backup-path direction pull each profile narrower or broader without changing sizing formulas
- Recommendation outputs now also include an additive inverter/system architecture layer that explains AC-coupled vs hybrid posture, coexistence assumptions, pathway suitability, expansion direction, and planning-only architecture consistency before final inverter sizing
- Recommendation outputs now also include an additive structured system reasoning graph that links recorded load grouping, backup scope, panel/service posture, inverter/system architecture, and the recommended battery/solar posture through inspectable planning-only dependencies
- Recommendation outputs now also include an additive current-home-energy-architecture layer that models existing solar/inverter topology, explicit existing-vs-proposed equipment state, outage-solar cautions, battery retrofit implications, generator coexistence uncertainty, and topology confidence before future architecture recommendations are interpreted
- The Design Advisor UI now organizes its reasoning spine into clearer workspace sections for current state, existing-vs-proposed posture, recommendation path, and reasoning/evidence with progressive disclosure for inspectability details
- The Design Advisor UI now also renders the current-home-energy-architecture and structured reasoning graph layers through more visual planning surfaces, including architecture relationship mapping, explicit existing/proposed/missing state cards, and a compact dependency-chain trace while preserving text fallback and trust framing
- The Design Advisor UI now also includes a planning-pathway comparison workspace that anchors current state once and compares multiple deterministic profile postures against the same backup, panel/service, and inverter architecture context without adding frontend-side recommendation logic
- `/api/*` support with legacy route compatibility

## Current Next Product Target

Deepen the solar-readiness and roof-capacity realism slice behind the current profile architecture while keeping formulas internal, provenance-aware, and planning-only, now that current-state solar topology, backup-scope posture, panel/service consistency, inverter/system architecture, structured reasoning dependencies, and the advisor workspace visualization surface are explicit layers.

## Restore Model

- Discovery: `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, repo-local skills
- Operational: only the specific global skills and docs needed for the task
- Deep reference: detailed docs, continuity files, doctrine, ADRs, and historical handoffs only when relevant

## Current Continuity Risks

- Detailed continuity docs still exist and remain valuable, but they are too large to treat as mandatory startup context.
- Provenance coverage is still partial, so trust messaging must stay explicit.
- Migration discipline is still early-stage even though Alembic scaffolding exists.
- Existing local databases may need reseeding to surface the new seeded current-home-energy-architecture, backup-architecture-consistency, profile-architecture-fit, inverter/system-architecture, and structured-reasoning-graph rule provenance records.

## Canonical Detailed References

- Product and implementation state: `docs/CURRENT_STATE.md`
- Product next step: `docs/NEXT_STEPS.md`
- Active work: `docs/ACTIVE_TASKS.md`
- Continuity workflow: `docs/session-continuity/continuity-workflow.md`
