# Project State

## Snapshot Date

2026-06-01

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
- Phase 2 Residential Energy Twin architecture is substantially complete as a documentation-only foundation.
- Phase 3 Twin Intelligence Layer architecture planning has started; current Phase 3 docs remain documentation/governance only and do not approve runtime implementation.

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
- `docs/architecture/ResidentialEnergyTwinContractV1.md` now defines the Residential Energy Twin aggregate contract as documentation/governance only; it does not approve schema changes, migrations, runtime behavior, auth/permission enforcement, API contract changes, utility semantics, DERMS/dispatch semantics, or a new canonical runtime model. `docs/architecture/RESIDENTIAL_ENERGY_TWIN_CONTRACT_V1.md` remains only a compatibility pointer.
- `docs/architecture/TopologyLifecycleDomains.md` now defines docs-only topology lifecycle domain boundaries for recorded current topology, sandbox planning topology, proposed pathways, scenario revisions, future reviewed/contractual/verified/utility-facing states, and future operational topology separation; it does not approve runtime topology graphs, lifecycle event logs, schema, APIs, enforcement, utility exports, DERMS/dispatch, or operational control.
- `docs/architecture/PermissionPlacement.md`, `docs/architecture/ProvenancePlacement.md`, and `docs/architecture/ViewContracts.md` now complete the remaining Phase 2 Residential Energy Twin placement/view architecture docs for permissions, provenance, and actor-specific views; they do not approve runtime enforcement, schemas, APIs, RBAC/ABAC, encryption, telemetry governance, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/SolarMarketProductIntelligenceGrounding.md` now bridges Phase 2 architecture to future Phase 3 Twin Intelligence grounding for solar production, market/economic reasonableness, and verified product intelligence; it does not approve provider integrations, spec-sheet ingestion, schemas, APIs, product catalogs, AI engineering automation, utility APIs, telemetry, DERMS/dispatch, or operational control.
- `docs/architecture/Phase3TwinIntelligenceLayer.md` now defines the docs-only Phase 3 Twin Intelligence planning layer for structured reasoning graphs, scenario intelligence, infrastructure simulation, what-if analysis, dependency reasoning, advisor traceability, deterministic reasoning exports, and non-goal boundaries; it does not approve runtime implementation, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/StructuredSystemReasoningGraph.md` now defines the docs-only Phase 3 derived/advisory reasoning graph planning layer for future graph nodes, graph edges, scenario intelligence, what-if analysis, infrastructure simulation, dependency reasoning, impact propagation, provenance/confidence preservation, permission-filtered graph views, and missing-data markers; it does not approve runtime graph implementation, graph database adoption, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/ScenarioIntelligence.md` now defines the docs-only Phase 3 derived/advisory scenario comparison planning layer for scenario types, comparison dimensions, grounding requirements, scenario outputs, tradeoff language, permission-filtered scenario views, and lifecycle boundaries; it does not approve runtime scenario engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/InfrastructureSimulation.md` now defines the docs-only Phase 3 derived/advisory simulation planning layer for critical-load survivability, outage endurance, battery discharge, recharge likelihood, solar recharge, seasonal production variation, generator support, flexible-load impacts, constraint impacts, economic sensitivity, DER/ADR readiness, future-state expansion, missing-data behavior, and permission-filtered simulation views; it does not approve runtime simulation engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/WhatIfAnalysis.md` now defines the docs-only Phase 3 derived/advisory what-if planning layer for modeled PV, battery, generator, EVSE, HVAC/load growth, critical-load, outage-target, backup-strategy, equipment-selection, financing/incentive, future-expansion, utility-participation, and DER/ADR readiness changes; it does not approve runtime what-if engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md` now records the docs-only first-boundary planning recommendation: use `home_id` only as a temporary premise-scoped planning-context anchor if Matt later approves implementation, while reserving `twin_id` for a future approved canonical aggregate.
- `docs/provenance/RESIDENTIAL_ENERGY_TWIN_PROVENANCE_POLICY_PLANNING.md` and `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md` complete the current Residential Energy Twin governance/design milestone as documentation-only planning for provenance authority and permissioned-view boundaries; no schema, API, runtime, auth/RBAC/ABAC, permission enforcement, utility authority, operational control, or canonical `ResidentialEnergyTwin` model is approved or implemented.
- Backend responses now include additive authority/classification/view-boundary/permission-readiness metadata on selected provenance, recommendation, AI context, scenario comparison, account, and placeholder estimate surfaces without changing recommendation behavior or enforcing access.
- Scoped view-model mapping now identifies consumer-safe, AI-safe, contractor-safe, and future utility-safe response boundaries, names broad/raw exposure surfaces, and defines narrowing candidates without changing recommendation behavior or implementing enforcement.
- `/api/*` support with legacy route compatibility

## Current Next Product Target

Near-term implementation still points toward deepening the solar-readiness and roof-capacity realism slice behind the current profile architecture, but no implementation work is approved by the Phase 2 or Phase 3 architecture docs. The current architecture-only next target is `docs/architecture/DependencyImpactPropagation.md`.

Runtime code, schemas, APIs, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, and operational control remain unapproved. `.github/` remains out of scope for the current Residential Energy Twin architecture session.

## Restore Model

- Discovery: `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, repo-local skills, task-relevant `.codex/project-skills/*`
- Operational: only the specific global skills and docs needed for the task
- Deep reference: detailed docs, cognition docs, continuity files, doctrine, ADRs, and historical handoffs only when relevant

## Current Continuity Risks

- Detailed continuity docs still exist and remain valuable, but they are too large to treat as mandatory startup context.
- Cognition docs now reduce restore ambiguity, but future sessions must avoid duplicating state summaries across root discovery files and detailed docs.
- Provenance coverage is still partial, so trust messaging must stay explicit.
- Data classification and scoped API views are documentation/design boundaries only; current API responses are not RBAC-filtered views.
- Broad AI context exposure remains compatibility-oriented and labeled with view-boundary metadata; scoped consumer/AI/contractor/utility view models are mapped but not implemented.
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
- Residential Energy Twin Contract v1: `docs/architecture/ResidentialEnergyTwinContractV1.md`
- Topology lifecycle domains: `docs/architecture/TopologyLifecycleDomains.md`
- Permission placement: `docs/architecture/PermissionPlacement.md`
- Provenance placement: `docs/architecture/ProvenancePlacement.md`
- View contracts: `docs/architecture/ViewContracts.md`
- Solar, market, and product intelligence grounding: `docs/architecture/SolarMarketProductIntelligenceGrounding.md`
- Phase 3 Twin Intelligence Layer: `docs/architecture/Phase3TwinIntelligenceLayer.md`
- Structured System Reasoning Graph: `docs/architecture/StructuredSystemReasoningGraph.md`
- Scenario Intelligence: `docs/architecture/ScenarioIntelligence.md`
- Infrastructure Simulation: `docs/architecture/InfrastructureSimulation.md`
- What-If Analysis: `docs/architecture/WhatIfAnalysis.md`
- First Residential Energy Twin runtime-boundary planning note: `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md`
- Residential Energy Twin provenance policy planning note: `docs/provenance/RESIDENTIAL_ENERGY_TWIN_PROVENANCE_POLICY_PLANNING.md`
- Residential Energy Twin permissioned-view planning note: `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md`
- Scoped view-model mapping: `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- Continuity workflow: `docs/session-continuity/continuity-workflow.md`
