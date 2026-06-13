# API Contracts

## Versioning Policy

- Legacy unprefixed routes remain supported for compatibility.
- `/api/*` is the preferred route base for current and future frontend work.
- `/api/v1` is reserved for the first explicit breaking version if needed later.
- Current policy is additive-first.

## Authority And View Boundary Policy

- A2 adds local header-based authentication, home-level authorization, and audit logging for home-data API paths.
- Current API responses remain product data contracts; A2 enforcement is a runtime access boundary, not a scoped view-model guarantee.
- Existing account, role, and subscription fields are scaffolding only; they do not imply RBAC, tenant isolation, contractor authorization, utility submission, or operational-control permission.
- Future scoped API views should be additive and should carry explicit authority layer, trust-zone posture, data classification, and provenance summaries where they expose derived or advisory intelligence.
- Future consumer, contractor, utility, AI, or orchestration views must not scrape prose as source of truth. They should consume structured fields that distinguish canonical objects, derived estimates, advisory explanations, operational state, and historical lineage.
- Existing compatibility-sensitive GET contracts should not be narrowed or reclassified as role-filtered views without a deliberate versioning and migration plan.
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md` is the current source-of-truth map for broad/raw response exposure and future scoped view-model candidates. It is not an enforcement plan and does not change current endpoint behavior.

## Additive Boundary Metadata In Current Responses

- Shared backend enums now exist for `authority_layer`, `data_classification`, and intended API-view audience.
- Shared additive metadata models now exist for view-boundary and permission-readiness descriptions.
- These metadata fields are descriptive only. They do not filter responses, enforce RBAC, enforce tenant isolation, authorize exports, or change account/session behavior.
- A2 home-data middleware requires `x-user-id` and, where a home ID is present, `x-home-access` containing that home ID or `*`. This is provider-free local enforcement, not production auth provider integration.
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
- `GET /api/contractor-workflow/homes/{home_id}/readiness`
- `GET /api/product-preferences/homes/{home_id}`
- `GET /api/post-install/homes/{home_id}`
- `GET /api/crm-handoff/homes/{home_id}`
- `GET /api/energy-passport/homes/{home_id}`
- `GET /api/program-intelligence/homes/{home_id}`
- `GET /api/homes/{home_id}/facts`
- `GET /api/homes/{home_id}/facts/gaps/{calculation_name}`
- `GET /api/homes/{home_id}/load-calculations/nec-220`
- `GET /api/homes/{home_id}/geometry/roof-planes`
- `GET /api/homes/{home_id}/geometry/obstructions`
- `GET /api/homes/{home_id}/geometry/export`
- `GET /api/privacy/homes/{home_id}/export`

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
- `POST/PATCH /api/homes/{home_id}/facts`
- `POST /api/homes/{home_id}/geometry/roof-planes`
- `POST /api/homes/{home_id}/geometry/obstructions`
- `POST /api/privacy/homes/{home_id}/consent`
- `DELETE /api/privacy/homes/{home_id}`

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
- `GET /api/contractor-workflow/homes/{home_id}/readiness`
  - additive read-only, request-time, deterministic Phase 11 contractor workflow readiness projection over existing Phase 5 contractor-context views, Phase 6 planning exchange, Phase 9 estimate readiness, and Phase 10 proposal option sets
  - Phase 7 shared-compatibility and Phase 8 topology-takeoff basis is carried only where already surfaced through existing Phase 9 and Phase 10 source contracts
  - response organizes readiness lanes for planning review, missing-input review, confirmation-gate review, option-candidate review, and proposal-prep blocked/deferred
  - response preserves blockers, missing inputs, confirmation gates, option-candidate refs, dependencies, assumptions, deferred boundaries, homeowner-safe summary, contractor-facing readiness prompts, and source/provenance basis
  - response is contractor workflow readiness projection only, not true contractor-owned persisted workflow state, not a contractor account, not assignment/acceptance/completion/approval tracking, not permission enforcement, not pricing, not bids/quotes, not final proposal, not final estimate, not final design, not CRM automation, not product-runtime email automation, not export behavior, not external service behavior, and not operational behavior
- `GET /api/product-preferences/homes/{home_id}`
  - additive read-only, request-time, deterministic Phase 12 product preference and install-logic guidance view over existing Phase 7 shared compatibility, Phase 8 topology takeoff, Phase 9 estimate readiness, and Phase 10 proposal option-set outputs
  - direct Phase 11 workflow rebuild is intentionally not used in runtime composition because it is expensive and unnecessary for Phase 12 category derivation
  - response includes fixed product/install categories, planning direction, install-logic review notes, homeowner-safe explanations, contractor-facing review prompts, blockers, missing inputs, confirmation gates, assumptions, deferred boundaries, explicit capability-boundary flags, and source/provenance basis
  - unsupported categories remain source-limited with explicit missing inputs rather than inferred preferences
  - response is product preference/install-logic guidance metadata only, not a final product recommendation, product ranking, best-option selection, pricing, live inventory, distributor quote, procurement, purchase link, payment, final BOM, final electrical design, manufacturer certification, warranty claim, CRM handoff, runtime email automation, frontend behavior, persistence, migrations, write behavior, auth/security behavior, permission enforcement, external service behavior, export behavior, or operational behavior
- `GET /api/post-install/homes/{home_id}`
  - additive read-only, request-time, deterministic Phase 13 post-install retention readiness view over existing Phase 11 contractor workflow readiness and Phase 12 product preference metadata, carrying Phase 9/10 references only where those source contracts already surface them
  - response includes post-install scope flags, retention opportunities, request-time lifecycle event detections, blockers, missing inputs, confirmation gates, follow-up readiness notes, homeowner-safe summary, contractor-facing summary, assumptions, limitations, deferred boundaries, and source/provenance basis
  - lifecycle events are request-time detections only; they are not persisted events, installation records, task records, CRM activities, field verification, contractor approval, or source-of-truth changes
  - response is manual follow-up readiness metadata only, not CRM integration, CRM writes, email/drip campaign behavior, task creation, sales scoring, lead scoring, ranking, best upsell logic, push behavior, pricing, proposal generation, persistence, migrations, auth/security behavior, permission enforcement, external service behavior, frontend behavior, export behavior, or operational behavior
- `GET /api/crm-handoff/homes/{home_id}`
  - additive read-only, request-time, deterministic Phase 13 CRM handoff object over the Phase 13 post-install retention view
  - response includes a deterministic manual handoff object id, fixed handoff fields, lifecycle event refs, retention opportunity refs, missing inputs, blocker refs, confirmation gates, manual review summary, homeowner-safe summary, contractor review summary, assumptions, limitations, deferred boundaries, explicit capability-boundary flags, and source/provenance basis
  - response is a handoff-shaped object for manual review only; it is not an external CRM integration, CRM sync, CRM write, CRM record creation, task creation, email/drip campaign behavior, lead scoring, sales scoring, ranking, best upsell logic, push behavior, persistence, migration, write behavior, auth/security behavior, permission enforcement, external service behavior, frontend behavior, export behavior, or operational behavior
- `GET /api/energy-passport/homes/{home_id}`
  - additive read-only, request-time, deterministic Phase 14 Energy Passport summary over existing Phase 6 through Phase 13 source surfaces where available
  - response includes explicit scope and capability-boundary flags, safe system statuses for solar PV, battery storage, backup/generator, panel/load management, EV readiness, and utility/program context, system financial obligation review metadata, supported financing structures, transfer relevance flags, documents needed, transfer readiness, missing transfer inputs, confirmation needs, buyer-safe and contractor-safe summaries, planning history summary, post-install context, ownership context, future upgrade context, assumptions, limitations, deferred boundaries, and source/provenance basis
  - unknown or needs-confirmation ownership/financing inputs degrade transfer readiness; readiness metadata is deterministic and non-authoritative
  - response is an Energy Passport summary for homeowner-safe review only, not persistence, migration, write behavior, auth/security behavior, permission enforcement, external integration, CRM write, legal/title/escrow/deed transfer logic, contract validation, warranty validation, permit validation, payoff calculation, lien/title/UCC search, appraisal, underwriting, tax-credit or financial conclusion, deploy, push, export behavior, frontend behavior, or operational behavior
- `GET /api/program-intelligence/homes/{home_id}`
  - additive read-only, request-time, deterministic Phase 15 Program Intelligence & Grid Edge Readiness view over existing `TwinPlanningContext` records
  - response includes explicit scope and capability-boundary flags, utility context awareness, program categories, incentive awareness, demand response awareness, VPP awareness, TOU awareness, interconnection awareness, battery participation readiness, load-shifting readiness, backup-planning readiness, smart-panel readiness, EV coordination readiness, DER aggregation readiness, missing inputs, blockers, confirmation gates, assumptions, dependencies, homeowner-safe summaries, contractor/program review prompts, verification recommendations, do-not-assume statements, and source/provenance basis
  - unknown utility, rate-plan, battery configuration, export status, interconnection status, equipment compatibility, and program jurisdiction inputs degrade the response through missing inputs, blockers, and confirmation gates rather than inference
  - response is program/grid-edge awareness metadata only, not persistence, migration, write behavior, background jobs, external API calls, auth/security behavior, permission enforcement, eligibility determination, enrollment workflow, rebate calculation, incentive calculation, tariff optimization, utility dispatch, device control, demand response execution, grid-services execution, billing logic, pricing logic, proposal generation, CRM integration, email automation, export behavior, push behavior, frontend behavior, interconnection approval, utility approval, or operational behavior
- `GET /api/homes/{home_id}/facts`
  - additive B1 Fact Lifecycle batch-read endpoint over persisted home-scoped facts
  - response includes stored fact value, unit, source, confidence tier, verified timestamp, optional expiry/decay policy, derived-from parent fact IDs, effective confidence score/tier, applied decay policy, and confidence reason
  - effective confidence is computed at read time; no background aging job, auth enforcement, permission enforcement, frontend behavior, migration file, external source lookup, engineering approval, or field-verification authority is added
- `POST /api/homes/{home_id}/facts` and `PATCH /api/homes/{home_id}/facts/{fact_id}`
  - additive B1 Fact Lifecycle create/update endpoints for home-scoped planning facts
  - create/update resets `verified_at` server-side and stores `derived_from` parent fact IDs for derived facts
  - these endpoints are fact-entry surfaces only; they do not verify truth, approve engineering inputs, enforce permission, import external data, delete facts, or create audit/auth behavior
- `GET /api/homes/{home_id}/facts/gaps/{calculation_name}`
  - additive B1 gap-readiness endpoint for named calculation requirement sets such as `nec_220_82` and `battery_backup_sizing`
  - response reports required keys, defaultable keys, present keys, missing/effectively-missing gaps, readiness, and limitations
  - readiness reflects fact availability and effective confidence only; it is not NEC compliance, engineering approval, field verification, AHJ approval, proposal readiness, or permission enforcement
- `GET /api/homes/{home_id}/load-calculations/nec-220`
  - additive B2 NEC Article 220 planning load-calculation endpoint over B1 facts
  - response includes 220.82 and 220.83 method results, calculation readiness, service load VA/amps, service headroom, stage-level VA values, consumed facts with effective confidence, substituted assumptions, missing/effectively-missing gaps, output confidence tier, source basis, and compliance boundary text
  - defaultable inputs are labeled as assumptions; required inputs with no safe default block calculation and return gaps
  - response is a planning calculation only, not stamped engineering, permit-ready design, AHJ approval, utility approval, field verification, final service sizing, proposal, pricing, auth/security behavior, permission enforcement, migration behavior, or operational behavior
- `GET/POST /api/homes/{home_id}/geometry/roof-planes`, `GET/POST /api/homes/{home_id}/geometry/obstructions`, and `GET /api/homes/{home_id}/geometry/export`
  - additive Phase 20 Geometry surfaces for home-scoped roof planes, obstructions, HomeDiagram-ready geometry export, and per-plane tier-1 shading derived from stored horizon traces
  - response is a planning geometry model only, not field verification, measured roof certification, satellite/lidar/GIS ingestion, permit-ready roof layout, structural engineering, AHJ/utility approval, frontend rendering, permission enforcement, auth/security behavior, export authorization, or operational behavior
- `GET /api/privacy/homes/{home_id}/export`, `POST /api/privacy/homes/{home_id}/consent`, and `DELETE /api/privacy/homes/{home_id}`
  - additive A4 local privacy surfaces for portable home record export, consent record capture, and local SQLite homeowner record deletion
  - guarded by A2 home-data middleware
  - deletion applies to local app records only; it does not contact external providers, utilities, contractors, CRMs, email systems, backups, legal systems, payment systems, or production privacy workflows

## Scoped View-Model Mapping Notes

- Highest-priority narrowing candidate: `GET /api/ai-context/design/{design_id}`. It intentionally remains a broad compatibility/grounding payload today, but a future `AIDesignGroundingView` should minimize raw object exposure and preserve source-linked summaries.
- Contractor-safe and utility-safe outputs should be new explicit view contracts, not filtered copies of existing broad responses.
- Consumer-safe views may reuse much of the current frontend planning surface, but they still need explicit planning-only limitation and provenance framing for derived estimates.
- Future scoped views should be added before RBAC/ABAC enforcement so permissions can bind to stable response shapes instead of ad hoc endpoint filtering.
