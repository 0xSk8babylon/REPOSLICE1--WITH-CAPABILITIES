# Project State

## Snapshot Date

2026-06-03

## Repo Shape

- Monorepo with `apps/api` and `apps/web`
- SQLite-backed FastAPI backend with SQLAlchemy persistence
- React/Vite frontend with core editable planning workflows
- Continuity and doctrine docs under `docs/`
- Canonical cognition, governance, topology, provenance, trust, roadmap, security, and orchestration docs now exist under dedicated `docs/*/` directories
- Repository-specific portable project skills now exist under `.codex/project-skills/`

## Current Product Phase

- Phase 1: Planner Foundation is complete.
- Phase 2A: Twin Doctrine Foundation is complete.
- Phase 2B: Twin Runtime Expression is complete for the current approved runtime scope: `TwinPlanningContext`, Runtime View Foundations, Dependency Awareness Foundations, and Permission Foundations. The runtime remains an approved read-only, `home_id`-anchored planning-context layer over existing planner records. Provenance Expansion runtime foundation scope is sufficiently complete; remaining provenance maturity work is deferred.
- Phase 2C: Topology + Lifecycle Intelligence Foundations are complete for the approved foundation scope: Topology Snapshot Foundation in `0c5bf23`, Lifecycle Readiness Foundation in `0d62693`, and Topology Relationship Coverage Foundation in `d56dbd6`. The topology snapshot remains read-only and derived from existing `TwinPlanningContext` records and dependency hooks, with descriptive lifecycle readiness and relationship coverage metadata only.
- Phase 3A: Derived Dependency Impact Readiness is complete in `97b57fb`: an additive read-only, request-time, `home_id`-anchored derived intelligence envelope at `/api/twin-planning-context/homes/{home_id}/views/dependency-impact-readiness`.
- Phase 3B: Derived Dependency Reasoning complete in `d56f52e`: an additive read-only, request-time, `home_id`-anchored reasoning view at `/api/twin-planning-context/homes/{home_id}/views/dependency-reasoning`. The view explains existing dependency meaning from `TwinPlanningContext`, topology snapshot, and Phase 3A dependency impact readiness basis. Every reasoning item carries traceable basis metadata and deterministic same-input/same-output coverage.
- A repository-cognition formalization layer now supports model-agnostic restore and governance routing without changing runtime behavior.
- Twin Doctrine Foundation architecture is substantially complete as a documentation/governance foundation.
- The Residential Energy Twin Interoperability Domain now defines docs-only shared semantic interpretation for cross-industry consumption without approving exchange mechanisms, ownership transfer, APIs, schemas, protocols, standards, exports, or runtime implementation.
- The Ecosystem Participant Boundary Matrix now consolidates participant-purpose boundaries for homeowners, contractors, utilities, real estate, insurance, finance, manufacturers, and aggregators before any Exchange Domain work; it does not create a new Twin domain or approve exchange, ownership transfer, APIs, schemas, protocols, or runtime implementation.
- The Dependency Impact Propagation milestone now defines docs-only Phase 3 architectural integrity behavior for stale outputs, dependency invalidation, recalculation, re-grounding, re-review, provenance impacts, confidence impacts, safety impacts, continuity impacts, and participant-view impacts; it is not a new Twin domain and does not approve runtime implementation, APIs, schemas, exchange, ownership transfer, or operational control.
- The Residential Energy Twin Canonical Architecture Hierarchy now consolidates the existing doctrine stack into eight routing layers without creating new domains, new architecture, Exchange, Ownership & Transfer, Registry, Identity, APIs, schemas, protocols, or runtime concepts.
- Phase 3 readiness references remain mostly documentation-only beyond approved Phase 3A and Phase 3B slices. Scenario intelligence, impact propagation, stale-state persistence, recalculation, invalidation, simulation, what-if analysis, optimization, ranking, recommendations, economic reasoning, utility readiness, survivability/recharge modeling, compatibility engines, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, operational control, twin_id, graph database/engine, migrations, and canonical Twin runtime model remain deferred.

## Canonical Phase Structure

- Phase 1: Planner Foundation - complete.
- Phase 2A: Twin Doctrine Foundation - complete.
- Phase 2B: Twin Runtime Expression - complete for the current approved runtime scope.
- Phase 2C: Topology + Lifecycle Intelligence - complete for the approved foundation scope: Topology Snapshot Foundation, Lifecycle Readiness Foundation, and Topology Relationship Coverage Foundation.
- Phase 3A: Derived Dependency Impact Readiness - complete for the approved first runtime boundary in `97b57fb`.
- Phase 3B: Derived Dependency Reasoning - complete for the approved second runtime boundary in `d56f52e`; broader Phase 3 remains deferred until Matt approves a new implementation boundary.

## Current Strategic Doctrine

- Current application: Residential Energy Planner.
- Core asset: Residential Energy Twin.
- Current positioning: Trusted Residential Energy Record.
- Long-term end state: Residential Infrastructure Registry.
- Long-term vision: Residential Infrastructure Network.
- The Residential Energy Planner is the first application built on top of the Residential Energy Twin and serves as the distribution mechanism for Twin creation, maintenance, and adoption.
- The planner exists to create, maintain, and enrich the Twin. Features that strengthen persistence, provenance, permissions, safety, interoperability, and lifecycle continuity take precedence over features that exist only within one project workflow.
- The Residential Energy Twin is the trusted record of residential infrastructure, energy capabilities, permissions, provenance, interoperability, and safety conditions behind the meter.
- Safety is a first-class Twin concern. Any future trusted safety-record posture for residential DER, backup systems, or grid-edge infrastructure remains gated by approved verification, provenance, permission, audit, and authority layers.
- The planner is not the long-term moat. Twin adoption, trusted records, permissioned provenance, continuity, interoperability, ecosystem participation, and network effects form the long-term moat.
- Protocols and standards are artifacts of successful ecosystem adoption. The repository should optimize for Twin adoption, trust, continuity, and ecosystem participation rather than protocol ownership.

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
- Phase 2B Twin Runtime Expression is now live through `TwinPlanningContextService`, an additive `/api/twin-planning-context/homes/{home_id}` endpoint, typed provenance gaps, dependency awareness labels, permission-readiness metadata, an additive `/api/twin-planning-context/homes/{home_id}/views/ai-design-grounding` scoped AI/design grounding projection, and an additive `/api/twin-planning-context/homes/{home_id}/views/runtime-projection/{role}` role-aware projection foundation.
- `TwinPlanningContextService` composes existing `home_id`-linked planner records only; it does not create `twin_id`, a canonical `ResidentialEnergyTwin` model/table, migrations, permission enforcement, Exchange, Ownership & Transfer, Registry, Identity, utility-control, or operational-control behavior.
- `AIDesignGroundingView` is a minimized read-only projection for grounded AI/design recommendations; it preserves provenance summaries, typed provenance gaps, rule keys, dependency hooks, missing fields, limitations, dependency awareness labels, and permission-readiness metadata while excluding account and street-address fields.
- `TwinRuntimeProjectionView` is a read-only projection foundation over the same canonical `home_id` context. It introduces minimal participant role, view context, visibility scope, contributor identity, and permission-readiness metadata for homeowner, contractor, and internal/system contexts while preserving provenance and contributor/source identity where available.
- Dependency Awareness Foundations are live as additive planning-context metadata through relationship-level dependency hooks, load-to-panel relationships via shared `building_id` labeled as planning context only, equipment-to-system/design/product/location references, scenario dependency references, descriptive change-impact hints, and descriptive planning dependency warnings. They do not implement a topology graph, recalculation engine, invalidation engine, background queue, or persisted stale-state system.
- Permission Foundations are live as explicit placeholder/readiness metadata through audience, purpose, duration, revocation-state, consent-artifact placeholder, homeowner-authority-preservation, view-permission-alignment, and permission-readiness fields carried through context, section, record, AI grounding, homeowner projection, contractor projection, and internal/system projection paths. They are not active grants, active consent, authorization checks, persisted permission state, security, auth, RBAC/ABAC, portals, exports, or enforcement.
- Phase 2C Topology Snapshot Foundation is live through `TwinTopologyNode`, `TwinTopologyEdge`, `TwinTopologySnapshot`, and the additive `/api/twin-planning-context/homes/{home_id}/views/topology-snapshot` endpoint. The snapshot includes `home_id`, scenario branch references, revision lineage references, lifecycle-domain summaries, and limitations, and is derived only from existing `TwinPlanningContext` records and dependency hooks.
- Phase 2C Lifecycle Readiness Foundation is live as additive metadata on the topology snapshot endpoint through `lifecycle_readiness_summary`, `lifecycle_readiness_hints`, `deferred_lifecycle_domains`, `missing_readiness_indicators`, and `source_marker_found` traceability. Readiness remains descriptive, read-only, topology-derived, and provenance-aware.
- Phase 2C Topology Relationship Coverage Foundation is live as additive metadata and safe derived edges on the topology snapshot endpoint through structure-to-premise relationships, panel/load/location-to-building relationships, design-to-pathway relationships, pathway source/destination relationships when resolvable to concrete context nodes, `relationship_coverage_summary`, `missing_relationship_indicators`, and conservative unresolved relationship handling.
- The topology snapshot, lifecycle readiness, and relationship coverage metadata are descriptive/advisory planning context only. They do not create persistence, migrations, a canonical topology table, `twin_id`, graph database, graph engine, lifecycle workflows, topology promotion engine, lifecycle event log, recalculation engine, invalidation engine, simulation, what-if analysis, Phase 3 intelligence, field-verified topology, contractor-reviewed topology, contractual topology, utility-reviewed topology, operational topology, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, or operational control.
- Phase 3A Derived Dependency Impact Readiness is live through `TwinDependencyImpactReadinessView` and the additive `/api/twin-planning-context/homes/{home_id}/views/dependency-impact-readiness` endpoint. It is a read-only request-time derived intelligence envelope over existing `TwinPlanningContext` and topology snapshot outputs. It explains source basis, lifecycle scope, dependency impact posture, missing inputs, provenance gaps, confidence posture, limitations, and deferred capabilities. Every derived statement includes traceable `basis` metadata, and backend tests verify deterministic same-input/same-output behavior. It does not recommend, optimize, simulate, rank, choose, authorize, persist state, create `twin_id`, create a graph engine, enforce permissions, export data, or operate devices.
- Phase 3B Derived Dependency Reasoning is live through `TwinDependencyReasoningView` and the additive `/api/twin-planning-context/homes/{home_id}/views/dependency-reasoning` endpoint. It is a read-only request-time derived explanation view over existing `TwinPlanningContext`, topology snapshot, and Phase 3A dependency impact readiness outputs. It explains source, topology, lifecycle, rule, provenance, permission-readiness, continuity/snapshot, and missing-information dependency context. Every reasoning item includes traceable `basis` metadata, and backend tests verify deterministic same-input/same-output behavior. It does not create persistence, migrations, `twin_id`, graph database/engine, scenario intelligence, impact propagation, stale-state persistence, recalculation, invalidation, simulation, what-if analysis, recommendations, ranking, optimization, exports, permission enforcement, or operational behavior.
- The repository now includes canonical cognition-layer definitions, terminology, governance gap analysis, trust zones, provenance lineage model, topology lifecycle, scoped intelligence boundaries, orchestration readiness gaps, and roadmap sequencing docs.
- ADR 0007 now records the decision to treat the repository as the durable project memory substrate.
- `.codex/project-skills/` now contains concise repo-specific skills for doctrine formalization, continuity governance, topology intelligence, orchestration readiness, canonical authority discipline, provenance lineage, and roadmap continuity.
- Canonical authority, trust-zone, provenance, data-classification, API-view, and RBAC-boundary language is now normalized across the source-of-truth docs without implementing auth, access control, telemetry, DER/ADR control, or migrations.
- `docs/architecture/ResidentialEnergyTwinContractV1.md` now defines the Residential Energy Twin aggregate contract as documentation/governance only; it does not approve schema changes, migrations, runtime behavior, auth/permission enforcement, API contract changes, utility semantics, DERMS/dispatch semantics, or a new canonical runtime model. `docs/architecture/RESIDENTIAL_ENERGY_TWIN_CONTRACT_V1.md` remains only a compatibility pointer.
- `docs/architecture/ResidentialEnergyTwinCanonicalArchitectureHierarchy.md` now defines the docs-only canonical architecture hierarchy and doctrine map for Strategic Doctrine, Residential Energy Twin Contract, Foundational Domains, Trust-Bearing Domains, Interpretation & Projection, Participant Boundaries, Phase 3 Intelligence, and Future Gated Layers; it does not create new domains, new architecture, Exchange, Ownership & Transfer, Registry, Identity, APIs, schemas, protocols, or runtime concepts.
- `docs/architecture/TopologyLifecycleDomains.md` now defines docs-only topology lifecycle domain boundaries for recorded current topology, sandbox planning topology, proposed pathways, scenario revisions, future reviewed/contractual/verified/utility-facing states, and future operational topology separation; it does not approve runtime topology graphs, lifecycle event logs, schema, APIs, enforcement, utility exports, DERMS/dispatch, or operational control.
- `docs/architecture/ContinuityDomain.md` now defines the docs-only Residential Energy Twin Continuity Domain for preserving lifecycle history across ownership, contractors, infrastructure, utility context, safety context, permissions, provenance, equipment replacement, system upgrades, and software/platform changes; it does not approve runtime continuity records, schemas, APIs, legal ownership, title ownership, contractual rights, compliance approval, utility authority, safety certification, exports, DERMS/dispatch, or operational control.
- `docs/architecture/SafetyDomain.md` now defines the docs-only Residential Energy Twin Safety Domain for persistent, provenance-bearing, permissioned safety context around energy sources, isolation systems, export capabilities, operational modes, verification status, and safety provenance; it does not approve runtime safety records, schemas, APIs, safety approval, field verification, inspection workflows, utility approval, exports, DERMS/dispatch, or operational control.
- `docs/architecture/InteroperabilityDomain.md` now defines the docs-only Residential Energy Twin Interoperability Domain for common understanding, semantic consistency, consumer independence, cross-industry consumption, domain interpretation, and preservation of Twin truth; it does not approve exchange mechanisms, ownership transfer, APIs, schemas, protocols, standards, exports, integrations, runtime implementation, utility authority, compliance approval, safety certification, DERMS/dispatch, or operational control.
- `docs/architecture/EcosystemParticipantBoundaryMatrix.md` now defines a docs-only participant-purpose boundary matrix for homeowners, contractors, utilities, real estate, insurance, finance, manufacturers, and aggregators; it consolidates minimum necessary domains, permissions, provenance, continuity, interoperability, prohibited claims, and prohibited authority assumptions without creating a new Twin domain or approving exchange mechanisms, ownership transfer, APIs, schemas, protocols, runtime implementation, utility control, or operational control.
- `docs/architecture/PermissionPlacement.md`, `docs/architecture/ProvenancePlacement.md`, and `docs/architecture/ViewContracts.md` now complete the remaining Phase 2A Twin Doctrine Foundation placement/view architecture docs for permissions, provenance, and actor-specific views; they do not approve runtime enforcement, schemas, APIs, RBAC/ABAC, encryption, telemetry governance, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/SolarMarketProductIntelligenceGrounding.md` now bridges Phase 2A doctrine and Phase 2B runtime foundations to future Phase 3 Twin Intelligence Expansion grounding for solar production, market/economic reasonableness, and verified product intelligence; it does not approve provider integrations, spec-sheet ingestion, schemas, APIs, product catalogs, AI engineering automation, utility APIs, telemetry, DERMS/dispatch, or operational control.
- `docs/architecture/Phase3TwinIntelligenceLayer.md` now defines the docs-only Phase 3 Twin Intelligence Expansion planning layer for structured reasoning graphs, scenario intelligence, infrastructure simulation, what-if analysis, dependency reasoning, advisor traceability, deterministic reasoning exports, and non-goal boundaries; it does not approve runtime implementation, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/StructuredSystemReasoningGraph.md` now defines the docs-only Phase 3 derived/advisory reasoning graph planning layer for future graph nodes, graph edges, scenario intelligence, what-if analysis, infrastructure simulation, dependency reasoning, impact propagation, provenance/confidence preservation, permission-filtered graph views, and missing-data markers; it does not approve runtime graph implementation, graph database adoption, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/ScenarioIntelligence.md` now defines the docs-only Phase 3 derived/advisory scenario comparison planning layer for scenario types, comparison dimensions, grounding requirements, scenario outputs, tradeoff language, permission-filtered scenario views, and lifecycle boundaries; it does not approve runtime scenario engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/InfrastructureSimulation.md` now defines the docs-only Phase 3 derived/advisory simulation planning layer for critical-load survivability, outage endurance, battery discharge, recharge likelihood, solar recharge, seasonal production variation, generator support, flexible-load impacts, constraint impacts, economic sensitivity, DER/ADR readiness, future-state expansion, missing-data behavior, and permission-filtered simulation views; it does not approve runtime simulation engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/WhatIfAnalysis.md` now defines the docs-only Phase 3 derived/advisory what-if planning layer for modeled PV, battery, generator, EVSE, HVAC/load growth, critical-load, outage-target, backup-strategy, equipment-selection, financing/incentive, future-expansion, utility-participation, and DER/ADR readiness changes; it does not approve runtime what-if engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, or operational control.
- `docs/architecture/DependencyImpactPropagation.md` now defines the docs-only Phase 3 derived/advisory integrity layer for stale outputs, dependency invalidation, recalculation, re-grounding, re-review, provenance impacts, confidence impacts, safety impacts, continuity impacts, and participant-view impacts; it does not create a new Twin domain or approve runtime invalidation logic, event logs, schemas, APIs, services, exchange mechanisms, ownership transfer, exports, utility submissions, permission enforcement, safety approval, field verification, DERMS/dispatch, or operational control.
- `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md` now records the docs-only first-boundary planning recommendation: use `home_id` only as a temporary premise-scoped planning-context anchor if Matt later approves implementation, while reserving `twin_id` for a future approved canonical aggregate.
- `docs/provenance/RESIDENTIAL_ENERGY_TWIN_PROVENANCE_POLICY_PLANNING.md` and `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md` complete the current Residential Energy Twin governance/design milestone as documentation-only planning for provenance authority and permissioned-view boundaries; no schema, API, runtime, auth/RBAC/ABAC, permission enforcement, utility authority, operational control, or canonical `ResidentialEnergyTwin` model is approved or implemented.
- Backend responses now include additive authority/classification/view-boundary/permission-readiness metadata on selected provenance, recommendation, AI context, scenario comparison, account, and placeholder estimate surfaces without changing recommendation behavior or enforcing access.
- Scoped view-model mapping now identifies consumer-safe, AI-safe, contractor-safe, and future utility-safe response boundaries, names broad/raw exposure surfaces, and defines narrowing candidates without changing recommendation behavior or implementing enforcement.
- `/api/*` support with legacy route compatibility

## Current Next Product Target

Phase 2B Twin Runtime Expression is complete. Phase 2C Topology + Lifecycle Intelligence Foundations are complete for the approved foundation scope: Topology Snapshot Foundation, Lifecycle Readiness Foundation, and Topology Relationship Coverage Foundation are complete and synchronized. Phase 3A Derived Dependency Impact Readiness is complete in `97b57fb`. Phase 3B Derived Dependency Reasoning is complete in `d56f52e`.

The next safe step is Phase 3B continuity closeout or a new Matt-approved implementation boundary. Scenario intelligence, impact propagation, stale-state persistence, recalculation, invalidation, simulation, what-if analysis, optimization, ranking, recommendations, economic reasoning, utility readiness, survivability/recharge modeling, compatibility engines, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, operational control, twin_id, graph database/engine, migrations, and canonical Twin runtime model remain deferred.

## Restore Model

- Discovery: `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, repo-local skills, task-relevant `.codex/project-skills/*`
- Operational: only the specific global skills and docs needed for the task
- Deep reference: detailed docs, cognition docs, continuity files, doctrine, ADRs, and historical handoffs only when relevant

## Current Continuity Risks

- Detailed continuity docs still exist and remain valuable, but they are too large to treat as mandatory startup context.
- Cognition docs now reduce restore ambiguity, but future sessions must avoid duplicating state summaries across root discovery files and detailed docs.
- Provenance Expansion remains partial and gap-reporting based, so trust messaging must stay explicit.
- Dependency Awareness Foundations are descriptive planning-context metadata only; there is no Phase 2C topology graph, invalidation engine, recalculation queue, background job, or persisted stale-state system.
- Permission Foundations are placeholder/readiness metadata only; there is no permission enforcement, grant ID, active consent, authorization check, persisted permission state, RBAC/ABAC, auth, tenant isolation, portal, export, utility sharing, ownership transfer, registry, marketplace, telemetry governance, or operational control.
- Phase 2C Topology Snapshot, Lifecycle Readiness, and Relationship Coverage Foundations are read-only and derived from existing planning-context records; remaining topology/lifecycle work is deferred, including canonical topology graph, persistence, topology promotion workflows, lifecycle event logs, field verification workflows, contractor-reviewed topology, contractual topology, utility-reviewed topology, operational topology, graph database, graph engine, recalculation engines, invalidation engines, simulation, what-if analysis, Phase 3 intelligence, or advisory pseudo-node edge materialization.
- Phase 3A Derived Dependency Impact Readiness and Phase 3B Derived Dependency Reasoning are explainable derived intelligence only. They must stay read-only, request-time, deterministic for the same Twin inputs, and traceable through basis metadata. Scenario intelligence, impact propagation, stale-state persistence, recalculation, invalidation, simulation, what-if analysis, optimization, ranking, recommendations, economic reasoning, utility readiness, survivability/recharge modeling, compatibility engines, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, operational control, twin_id, graph database/engine, migrations, and canonical Twin runtime model remain deferred.
- `TwinRuntimeProjectionView` now provides additive homeowner, contractor, and internal/system projection foundations, but these are not enforced permissioned views and do not create portals, exports, grants, consent artifacts, RBAC/ABAC, tenant isolation, utility views, or partner APIs.
- No canonical Residential Energy Twin runtime identity exists; `home_id` remains the only runtime anchor for the Twin Planning Context.
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
- Residential Energy Twin Canonical Architecture Hierarchy: `docs/architecture/ResidentialEnergyTwinCanonicalArchitectureHierarchy.md`
- Residential Energy Twin Contract v1: `docs/architecture/ResidentialEnergyTwinContractV1.md`
- Topology lifecycle domains: `docs/architecture/TopologyLifecycleDomains.md`
- Continuity Domain: `docs/architecture/ContinuityDomain.md`
- Safety Domain: `docs/architecture/SafetyDomain.md`
- Interoperability Domain: `docs/architecture/InteroperabilityDomain.md`
- Ecosystem participant boundary matrix: `docs/architecture/EcosystemParticipantBoundaryMatrix.md`
- Permission placement: `docs/architecture/PermissionPlacement.md`
- Provenance placement: `docs/architecture/ProvenancePlacement.md`
- View contracts: `docs/architecture/ViewContracts.md`
- Solar, market, and product intelligence grounding: `docs/architecture/SolarMarketProductIntelligenceGrounding.md`
- Phase 3 Twin Intelligence Expansion layer: `docs/architecture/Phase3TwinIntelligenceLayer.md`
- Structured System Reasoning Graph: `docs/architecture/StructuredSystemReasoningGraph.md`
- Scenario Intelligence: `docs/architecture/ScenarioIntelligence.md`
- Infrastructure Simulation: `docs/architecture/InfrastructureSimulation.md`
- What-If Analysis: `docs/architecture/WhatIfAnalysis.md`
- Dependency Impact Propagation: `docs/architecture/DependencyImpactPropagation.md`
- Phase 2B Twin Runtime Foundation closeout handoff: `docs/handoffs/2026-06-02-phase-2b-twin-runtime-foundations-closeout.md`
- Phase 2B runtime view foundations handoff: `docs/handoffs/2026-06-03-phase-2b-runtime-view-foundations.md`
- Phase 2B dependency and permission foundations handoff: `docs/handoffs/2026-06-03-phase-2b-dependency-permission-foundations.md`
- Phase 2C topology snapshot foundation handoff: `docs/handoffs/2026-06-03-phase-2c-topology-snapshot-foundation.md`
- Phase 2C lifecycle readiness foundation handoff: `docs/handoffs/2026-06-03-phase-2c-lifecycle-readiness-foundation.md`
- Phase 2C topology relationship coverage foundation handoff: `docs/handoffs/2026-06-03-phase-2c-topology-relationship-coverage-foundation.md`
- Phase 2C foundations closeout handoff: `docs/handoffs/2026-06-03-phase-2c-foundations-closeout.md`
- Phase 3A dependency impact readiness handoff: `docs/handoffs/2026-06-03-phase-3a-dependency-impact-readiness.md`
- Phase 3B dependency reasoning handoff: `docs/handoffs/2026-06-03-phase-3b-dependency-reasoning.md`
- First Residential Energy Twin runtime-boundary planning note: `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md`
- Residential Energy Twin provenance policy planning note: `docs/provenance/RESIDENTIAL_ENERGY_TWIN_PROVENANCE_POLICY_PLANNING.md`
- Residential Energy Twin permissioned-view planning note: `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md`
- Scoped view-model mapping: `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- Continuity workflow: `docs/session-continuity/continuity-workflow.md`
