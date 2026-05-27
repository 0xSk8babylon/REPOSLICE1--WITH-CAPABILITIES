# Project State

## Snapshot Date

2026-05-27

## Repo Shape

- Monorepo with `apps/api` and `apps/web`
- SQLite-backed FastAPI backend with SQLAlchemy persistence
- React/Vite frontend with core editable planning workflows
- Continuity and doctrine docs under `docs/`
- Canonical cognition, governance, topology, provenance, trust, roadmap, security, and orchestration docs now exist under dedicated `docs/*/` directories
- Repository-specific portable project skills now exist under `.codex/project-skills/`

## Current Product Phase

- Phase 2A persistence is complete.
- Phase 2B editable workflows are materially in place.
- Current work sits in the Phase 2D/2E trust, advisor, and provenance layer.
- A repository-cognition formalization layer now supports model-agnostic restore and governance routing without changing runtime behavior.

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
- The Design Advisor API now also includes an additive `planning_state` snapshot envelope so recommendation, architecture, and pathway-comparison outputs are explicitly tied to a specific live design state plus any linked persistent scenario records
- Scenario persistence now also includes additive immutable scenario revisions so saved planning states can accumulate revision lineage and advisor-linked snapshot framing without replacing the current live scenario workspace model
- The Scenario Comparison UI now also includes a historical revision-comparison workspace that compares saved revision drift for design goal, status, recommended pathway, current-state architecture framing, and pathway-confidence posture from stored revision snapshots
- The repository now includes canonical cognition-layer definitions, terminology, governance gap analysis, trust zones, provenance lineage model, topology lifecycle, scoped intelligence boundaries, orchestration readiness gaps, and roadmap sequencing docs.
- ADR 0007 now records the decision to treat the repository as the durable project memory substrate.
- `.codex/project-skills/` now contains concise repo-specific skills for doctrine formalization, continuity governance, topology intelligence, orchestration readiness, canonical authority discipline, provenance lineage, and roadmap continuity.
- Canonical authority, trust-zone, provenance, data-classification, API-view, and RBAC-boundary language is now normalized across the source-of-truth docs without implementing auth, access control, telemetry, DER/ADR control, or migrations.
- Backend responses now include additive authority/classification/view-boundary/permission-readiness metadata on selected provenance, recommendation, AI context, scenario comparison, account, and placeholder estimate surfaces without changing recommendation behavior or enforcing access.
- `/api/*` support with legacy route compatibility

## Current Next Product Target

Near-term implementation still points toward deepening the solar-readiness and roof-capacity realism slice behind the current profile architecture. The current repository-architecture priority is preserving the new cognition structure so future implementation can resume from lean project-skill restore rather than long chat prompts.

## Restore Model

- Discovery: `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, repo-local skills, task-relevant `.codex/project-skills/*`
- Operational: only the specific global skills and docs needed for the task
- Deep reference: detailed docs, cognition docs, continuity files, doctrine, ADRs, and historical handoffs only when relevant

## Current Continuity Risks

- Detailed continuity docs still exist and remain valuable, but they are too large to treat as mandatory startup context.
- Cognition docs now reduce restore ambiguity, but future sessions must avoid duplicating state summaries across root discovery files and detailed docs.
- Provenance coverage is still partial, so trust messaging must stay explicit.
- Data classification and scoped API views are documentation/design boundaries only; current API responses are not RBAC-filtered views.
- Broad AI context exposure remains compatibility-oriented and labeled with view-boundary metadata; it is not yet split into scoped consumer/AI/contractor/utility view models.
- Migration discipline is still early-stage even though Alembic scaffolding exists.
- Existing local databases may need reseeding to surface the new seeded current-home-energy-architecture, backup-architecture-consistency, profile-architecture-fit, inverter/system-architecture, and structured-reasoning-graph rule provenance records.
- Existing local databases may also need either app restart or reseeding to create baseline rows in the new `scenario_revisions` table for older scenario records.

## Canonical Detailed References

- Product and implementation state: `docs/CURRENT_STATE.md`
- Product next step: `docs/NEXT_STEPS.md`
- Active work: `docs/ACTIVE_TASKS.md`
- Lean restore workflow: `docs/continuity/LEAN_RESTORE_WORKFLOW.md`
- Repository cognition structure: `docs/architecture/REPOSITORY_COGNITION_STRUCTURE.md`
- Cognition layers: `docs/architecture/COGNITION_LAYERS.md`
- Canonical terminology: `docs/architecture/CANONICAL_TERMINOLOGY.md`
- Continuity workflow: `docs/session-continuity/continuity-workflow.md`
