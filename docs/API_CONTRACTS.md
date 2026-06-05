# API Contracts

## Versioning Policy

- Legacy unprefixed routes remain supported for compatibility.
- `/api/*` is the preferred route base for current and future frontend work.
- `/api/v1` is reserved for the first explicit breaking version if needed later.
- Current policy is additive-first.

## Authority And View Boundary Policy

- Current API responses are product data contracts, not security enforcement boundaries.
- Existing account, role, and subscription fields are scaffolding only; they do not imply RBAC, tenant isolation, contractor authorization, utility submission, or operational-control permission.
- Future scoped API views should be additive and should carry explicit authority layer, trust-zone posture, data classification, and provenance summaries where they expose derived or advisory intelligence.
- Future consumer, contractor, utility, AI, or orchestration views must not scrape prose as source of truth. They should consume structured fields that distinguish canonical objects, derived estimates, advisory explanations, operational state, and historical lineage.
- Existing compatibility-sensitive GET contracts should not be narrowed or reclassified as role-filtered views without a deliberate versioning and migration plan.
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md` is the current source-of-truth map for broad/raw response exposure and future scoped view-model candidates. It is not an enforcement plan and does not change current endpoint behavior.

## Additive Boundary Metadata In Current Responses

- Shared backend enums now exist for `authority_layer`, `data_classification`, and intended API-view audience.
- Shared additive metadata models now exist for view-boundary and permission-readiness descriptions.
- These metadata fields are descriptive only. They do not filter responses, enforce RBAC, enforce tenant isolation, authorize exports, or change account/session behavior.
- Provenance and recommendation inspectability surfaces may now include additive `authority_layer`, `data_classification`, `derivation_type`, and `limitations` fields.
- Account responses may now include additive `permission_readiness` metadata explaining that role, plan, and subscription fields remain scaffolding only.

## Core GET Contracts In Use

- `GET /api/homes`
- `GET /api/homes/all`
- `GET /api/buildings`
- `GET /api/panels`
- `GET /api/loads`
- `GET /api/loads/summary`
- `GET /api/load-templates`
- `GET /api/designs`
- `GET /api/product-library`
- `GET /api/compatibility-rules/issues`
- `GET /api/compatibility-rules/evaluate/{design_id}`
- `GET /api/scenarios`
- `GET /api/scenarios/compare`
- `GET /api/scenarios/{scenario_id}/revisions`
- `GET /api/equipment/locations`
- `GET /api/estimated-pathways`
- `GET /api/takeoffs/current`
- `GET /api/takeoffs/generate/{design_id}`
- `GET /api/design-advisor/summary/{design_id}`
- `GET /api/ai-context/design/{design_id}`
- `GET /api/estimates/placeholder`
- `GET /api/planning-exchange/homes/{home_id}`
- `GET /api/twin-planning-context/homes/{home_id}/views/topology-takeoff`
- `GET /api/estimate-readiness/homes/{home_id}`
- `GET /api/proposal-option-sets/homes/{home_id}`

## Current Write Contracts

- `POST/PATCH /api/accounts`
- `POST/PATCH /api/homes`
- `POST/PATCH /api/buildings`
- `POST/PATCH /api/panels`
- `POST/PATCH /api/loads`
- `POST/PATCH /api/designs`
- `POST/PATCH /api/product-library`
- `POST/PATCH /api/scenarios`
  - scenario responses now include additive `created_at`, `updated_at`, `revision_overview`, and `revisions`
  - create/update flows now capture additive immutable scenario revisions behind the existing live scenario record
- `POST/PATCH /api/equipment/locations`
- `POST/PATCH /api/estimated-pathways`

## Compatibility-Sensitive Contracts

- `GET /api/homes`
  - frontend depends on nested buildings and panels
- design/advisor/context endpoints
  - frontend assumes stable design IDs and current persisted demo data
- `GET /api/ai-context/design/{design_id}` now includes additive `view_boundary` and `permission_readiness` metadata that identifies the endpoint as broad AI-grounding context, not a filtered RBAC view or source of new canonical facts
- `GET /api/design-advisor/summary/{design_id}` now includes additive `recommendation_profiles` guidance
- `GET /api/design-advisor/summary/{design_id}` recommendation and inspectability payloads now include additive authority/classification/derivation/limitation metadata so derived estimates stay distinct from canonical facts and advisory text
- `GET /api/design-advisor/summary/{design_id}` now also includes additive `planning_state` snapshot framing for the live design state, generated pathway variants, and linked saved-scenario metadata
  - `planning_state.linked_scenarios[*]` now also includes additive latest-revision identity metadata when saved scenario revisions exist
  - `recommendation_profiles.profiles[*]` now include additive planning-only battery sizing estimate ranges
  - `recommendation_profiles.profiles[*]` now include additive planning-only solar sizing and recovery estimate ranges
  - `recommendation_profiles.profiles[*]` now include additive `architecture_fit` tradeoff summaries, warnings, and status tied to recorded equipment mix and backup-path posture
  - `recommendation_profiles.current_home_energy_architecture` now includes additive current-state solar/inverter topology classification, existing-vs-proposed architecture summaries, outage-solar cautions, battery retrofit implications, generator coexistence notes, topology source inputs, and architecture relationship components
  - `recommendation_profiles.inverter_system_architecture` now includes additive AC-coupled vs hybrid posture, pathway suitability, coexistence assumptions, planning-only consistency output, confidence framing, and inspectability metadata
  - `recommendation_profiles.reasoning_graph` now includes additive recommended-profile dependency nodes and provenance-linked reasoning edges connecting loads, current topology, backup scope, panel/service posture, inverter/system architecture, battery posture, and solar posture
  - `recommendation_profiles.profiles[*]`, `battery_sizing_estimate`, and `solar_sizing_estimate` now include additive inspectability metadata for basis signals, estimated inputs, incomplete inputs, and planning-only warnings
  - `recommendation_profiles.backup_load_selection` now includes additive selected-scope reasoning, recorded-load coverage, outage posture, confidence posture, planning-gap warning, and inspectability metadata for deterministic backup/load selection
  - `solar_sizing_estimate` now also includes additive site-aware planning fields such as the base solar range, site capacity posture, shading caution, seasonal production caution, and install realism caution
  - `solar_sizing_estimate.roof_geometry_readiness` now includes additive roof-data completeness, roof-measurement confidence, measured-vs-estimated status, future geometry source placeholders, and missing-geometry warnings
  - `recommendation_profiles.panel_service_architecture` now includes additive panel/service posture, backup-architecture recommendation, architecture-consistency output, upgrade cautions, readiness notes, and planning-only inspectability metadata
- scenario and takeoff endpoints
  - current UI treats placeholder score/cost content as planning-level outputs only
- `GET /api/scenarios/compare`
  - now returns additive comparison metadata, rankings, warnings, completeness, and lineage summaries on top of scenario records
  - scenario records returned in comparison now also include additive revision framing and immutable revision history summaries
  - comparison payloads now include additive `view_boundary`, and lineage summaries now include additive authority/classification/derivation/limitation metadata
- `GET /api/loads`
  - now returns additive `provenance_summary` metadata on each load record
- `GET /api/estimated-pathways`
  - now returns additive `provenance_summary` metadata on each pathway record
- `GET /api/estimates/placeholder`
  - now returns additive authority/classification/derivation/limitation metadata clarifying that estimate generation remains deferred
- `GET /api/planning-exchange/homes/{home_id}`
  - additive read-only, request-time, deterministic Planning Exchange Object over existing planning context and Phase 5 contractor-context views
  - response is a derived package for participant planning review only, not a persisted source of truth, export, share link, permission-enforced view, proposal, estimate, final electrical sizing output, or final design claim
- `GET /api/twin-planning-context/homes/{home_id}/views/shared-compatibility`
  - additive read-only, request-time, deterministic Phase 7 shared compatibility view over existing `TwinPlanningContext`, topology/readiness outputs, Phase 5 contractor gates/signals, and the Phase 6 Planning Exchange Object
  - response classifies planning/install paths as compatible, likely compatible, blocked, unknown, or requiring contractor confirmation with per-path reason, basis/provenance, basis-quality metadata, missing information where relevant, blockers, assumptions, required site/product verification gates, and contractor confirmation gates
  - response includes top-level summary rollups plus homeowner-safe and contractor-facing interpretation metadata; these are metadata only, not permissioned views, exports, auth, sharing, or enforcement
  - response is planning classification only, not a final design output, full compatibility engine, recommendation ranking, permission-enforced export, contractor confirmation, field verification, permit-ready design, AHJ/utility approval, final wire/conduit/breaker sizing, final disconnect/OCPD approval, proposal, price, or operational behavior
- `GET /api/twin-planning-context/homes/{home_id}/views/topology-takeoff`
  - additive read-only, request-time, deterministic Phase 8 topology takeoff view over existing `TwinPlanningContext`, topology snapshot, Phase 7 shared compatibility, Phase 5 contractor gates/signals, and the Phase 6 Planning Exchange Object
  - response emits planning-grade topology-driven material/scope categories with per-line reason, traceable basis/provenance, basis-quality metadata, quantity-basis posture, cost-basis-unavailable metadata, uncertainty, missing information, blockers, required confirmations, and contractor confirmation gates
  - response includes top-level takeoff summary rollups plus homeowner-safe and contractor-facing interpretation metadata; these are metadata only, not permissioned views, exports, auth, sharing, or enforcement
  - response is planning-grade scope discovery only, not a persisted takeoff, final contractor estimate, final bill of materials, contractor-approved BOM, final engineered design, NEC/code-compliant material list, permit-ready design, AHJ/utility approval, field verification, exact wire/conduit/breaker sizing, final disconnect/OCPD approval, proposal, price, or operational behavior
- `GET /api/estimate-readiness/homes/{home_id}`
  - additive read-only, request-time, deterministic Phase 9 estimate readiness view over existing `TwinPlanningContext`, Phase 5 confirmation gates, Phase 7 shared compatibility, Phase 8 topology takeoff, and existing scenario records
  - response includes `overall_status`, `scenario_statuses`, versioned 19-gate `confirmation_gates`, blocker records, missing inputs, homeowner-safe summary, contractor-facing summary, `estimate_allowed`, `contractor_review_required`, confidence level, source basis, and deferred-boundary metadata
  - confirmation gates are readiness metadata only; gate status is not persisted confirmation, contractor completion, field verification, engineering approval, AHJ approval, utility approval, or final design authority
  - response is pre-estimate readiness classification only, not a final estimate, proposal, quote, bid, final bill of materials, contractor-approved scope, pricing source, permit-ready design, AHJ/utility approval, field verification, exact wire/conduit/breaker sizing, final disconnect/OCPD approval, or operational behavior
- `GET /api/proposal-option-sets/homes/{home_id}`
  - additive read-only, request-time, deterministic Phase 10 proposal option-set readiness view over Phase 3M proposal readiness, Phase 6 planning exchange, Phase 9-carried shared compatibility and topology takeoff refs, Phase 9 estimate readiness, and existing scenario/design records
  - response includes option candidates, scenario/design/source basis, homeowner-safe summaries, contractor-facing review notes, blockers, missing inputs, confirmation gates, dependencies, assumptions, deferred boundaries, confidence level, and explicit capability-boundary flags
  - Phase 9 scenario readiness remains home-level metadata, so Phase 10 candidates inherit that limitation rather than claiming scenario-specific estimate/proposal readiness
  - response is proposal-option readiness metadata only, not pricing, quote/bid logic, final proposal generation, final estimate, final design, permission enforcement, approval claims, final electrical sizing, persistence, migrations, write behavior, frontend behavior, exports, CRM, email automation, or operational behavior

## Scoped View-Model Mapping Notes

- Highest-priority narrowing candidate: `GET /api/ai-context/design/{design_id}`. It intentionally remains a broad compatibility/grounding payload today, but a future `AIDesignGroundingView` should minimize raw object exposure and preserve source-linked summaries.
- Contractor-safe and utility-safe outputs should be new explicit view contracts, not filtered copies of existing broad responses.
- Consumer-safe views may reuse much of the current frontend planning surface, but they still need explicit planning-only limitation and provenance framing for derived estimates.
- Future scoped views should be added before RBAC/ABAC enforcement so permissions can bind to stable response shapes instead of ad hoc endpoint filtering.
