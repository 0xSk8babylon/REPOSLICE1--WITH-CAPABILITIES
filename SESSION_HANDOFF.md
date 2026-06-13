# Session Handoff

## Updated

2026-06-06

## Session Summary

- 2026-06-13 Auto-Loop Roadmap Runner was activated by Matt for the pasted B1 through B7/A2/A4/C1/B3 roadmap under OwnerWorkflows authority. The repo/branch/remote/status were confirmed as `/home/mattcoje/residential-energy-planner`, branch `fix/github-workflow`, remotes `origin`, `twin-layer`, and `twin-layer-base`, and a clean worktree before edits.
- Loop packets were materialized in `docs/roadmap/auto-loop-roadmap-runner-packets.md`.
- Loop B1 Fact Lifecycle was implemented as an additive backend packet. It adds home-scoped fact persistence, fact create/update/read APIs, read-time effective confidence decay, derived-from parent fact IDs, and named calculation gap reporting. Runtime endpoint contracts are `GET /api/homes/{home_id}/facts`, `POST /api/homes/{home_id}/facts`, `PATCH /api/homes/{home_id}/facts/{fact_id}`, and `GET /api/homes/{home_id}/facts/gaps/{calculation_name}`.
- B1 changed `apps/api/app/core/models.py`, `apps/api/app/core/repository.py`, `apps/api/app/core/types.py`, `apps/api/app/main.py`, `apps/api/app/facts/__init__.py`, `apps/api/app/facts/schemas.py`, `apps/api/app/facts/router.py`, `apps/api/app/services/facts.py`, `apps/api/tests/test_facts.py`, `docs/API_CONTRACTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, `docs/roadmap/auto-loop-roadmap-runner-packets.md`, and `docs/handoffs/2026-06-13-b1-fact-lifecycle-closeout.md`.
- B1 intentionally does not add Alembic migrations, auth, permission enforcement, delete endpoints, frontend behavior, external services, dependency installs, lockfile rewrites, GitHub Actions changes, billing, production deployment, push behavior, NEC calculation execution, or field-verification authority.
- Matt then provided a session-only override for NEC and calculation hard stops for this roadmap/session only.
- Loop B2 NEC 220 Load Calculation is implemented in the working tree. It adds `GET /api/homes/{home_id}/load-calculations/nec-220` as an additive, deterministic, planning-only endpoint over B1 facts for 220.82 and 220.83 method results. It reports stage-level VA, service-load amps, headroom, consumed facts, effective confidence, labeled default assumptions, gaps, source basis, and professional-review/AHJ boundary text.
- B2 changed `apps/api/app/nec_load_calculation/__init__.py`, `apps/api/app/nec_load_calculation/schemas.py`, `apps/api/app/nec_load_calculation/router.py`, `apps/api/app/services/nec_load_calculation.py`, `apps/api/app/services/facts.py`, `apps/api/app/main.py`, `apps/api/tests/test_nec_load_calculation.py`, docs/API/continuity files, and `docs/handoffs/2026-06-13-b2-nec-220-load-calculation-closeout.md`.
- B2 does not add migrations, auth/security, permission enforcement, frontend behavior, external services, dependencies, lockfiles, secrets, deletion, pricing, proposal generation, field verification, AHJ/utility approval, production deployment, push, `twin_id`, graph engine behavior, or operational control.
- Loop B4 Calculator Primitives is implemented in the working tree. It adds `apps/api/app/engines/calculator_primitives.py` plus focused tests for 120% backfeed planning, supply-side tap review metadata, coupling direction, critical-load identification, tier-1 shading derate, and solar production estimation with optional injected estimator.
- B4 changed `apps/api/app/engines/calculator_primitives.py`, `apps/api/tests/test_calculator_primitives.py`, docs/continuity files, and `docs/handoffs/2026-06-13-b4-calculator-primitives-closeout.md`.
- B4 does not add persistence, migrations, routes, frontend behavior, auth/security changes, permission enforcement, external services, dependency installs, lockfile rewrites, network calls, pricing, proposal generation, field verification, AHJ/utility approval, production deployment, push, `twin_id`, graph engine behavior, or operational control.
- Loop B5 Hourly Simulation is implemented in the working tree. It adds `apps/api/app/engines/hourly_simulation.py` plus focused tests for hourly energy conservation, battery SoC/cycles, flat/TOU/tiered caller-provided rate math, bill delta, backup coverage, and invalid profile handling.
- B5 changed `apps/api/app/engines/hourly_simulation.py`, `apps/api/tests/test_hourly_simulation.py`, docs/continuity files, and `docs/handoffs/2026-06-13-b5-hourly-simulation-closeout.md`.
- B5 does not add persistence, migrations, routes, frontend behavior, auth/security, permission enforcement, external utility/rate lookup, dependencies, lockfiles, real tariff data, customer billing, proposal generation, deployment, push, graph behavior, `twin_id`, or operational control.
- Loop Phase 20 Geometry is implemented in the working tree. It adds roof-plane and obstruction SQLAlchemy models, repository helpers, schemas, router, geometry export service, and focused tests for storage/query plus per-plane B4 tier-1 shading.
- Phase 20 changed `apps/api/app/core/models.py`, `apps/api/app/core/repository.py`, `apps/api/app/main.py`, `apps/api/app/geometry/__init__.py`, `apps/api/app/geometry/schemas.py`, `apps/api/app/geometry/router.py`, `apps/api/app/services/geometry.py`, `apps/api/tests/test_geometry.py`, docs/API/continuity files, and `docs/handoffs/2026-06-13-phase-20-geometry-closeout.md`.
- Phase 20 does not add an Alembic migration file, frontend rendering, satellite/lidar/GIS ingestion, external service, auth/security, permission enforcement, deletion endpoint, dependency, lockfile, field verification, AHJ/utility approval, deployment, push, graph engine behavior, `twin_id`, or operational control.
- Loop B6 Sizers is implemented in the working tree. It adds `apps/api/app/engines/sizers.py` plus focused tests for battery, generator, V2H, and transformer headroom sizing primitives.
- B6 changed `apps/api/app/engines/sizers.py`, `apps/api/tests/test_sizers.py`, docs/continuity files, and `docs/handoffs/2026-06-13-b6-sizers-closeout.md`.
- B6 does not add routes, persistence, migrations, frontend behavior, auth/security, permission enforcement, external lookups, pricing, SGIP, 25D, 48E, quote logic, proposal generation, product ranking, procurement, field verification, AHJ/utility approval, deployment, push, graph behavior, `twin_id`, or operational control.
- Loop B7 / Phase 21 Graph Comparator and Smart Panel Scoring is implemented in the working tree. It adds `apps/api/app/engines/graph_comparator.py` plus focused tests for candidate scoring, tradeoff surfacing, smart-panel scoring, and graph confidence summaries.
- B7 changed `apps/api/app/engines/graph_comparator.py`, `apps/api/tests/test_graph_comparator.py`, docs/continuity files, and `docs/handoffs/2026-06-13-b7-graph-comparator-smart-panel-closeout.md`.
- B7 does not add a graph database, persisted topology graph, lifecycle event log, routes, frontend behavior, auth/security, permission enforcement, external services, final design selection, product ranking as sales direction, pricing authority, utility approval, field verification, DERMS, dispatch, operational control, deployment, push, or `twin_id`.
- Loop A2 Auth + Object Authorization + Audit Logging is implemented in the working tree. It adds a provider-free local header-based `HomeAccessMiddleware`, an `AuditEvent` model, and focused tests for authentication, home-level authorization, and audit writes.
- A2 changed `apps/api/app/security/__init__.py`, `apps/api/app/security/auth.py`, `apps/api/app/core/models.py`, `apps/api/app/main.py`, `apps/api/tests/test_auth_audit.py`, docs/API/continuity files, and `docs/handoffs/2026-06-13-a2-auth-object-audit-closeout.md`.
- A2 does not add an external auth provider, secrets, sessions, cookies, OAuth, password flow, RBAC/ABAC, frontend login UI, dependency installs, lockfile rewrites, production deployment, push, billing, or operational control.
- Loop A4 Privacy / CCPA is implemented in the working tree. It adds local privacy export, consent record, and deletion endpoints guarded by A2 middleware.
- A4 changed `apps/api/app/privacy/__init__.py`, `apps/api/app/privacy/schemas.py`, `apps/api/app/privacy/router.py`, `apps/api/app/services/privacy.py`, `apps/api/app/core/models.py`, `apps/api/app/main.py`, `apps/api/app/security/auth.py`, `apps/api/tests/test_privacy.py`, docs/API/continuity files, and `docs/handoffs/2026-06-13-a4-privacy-ccpa-closeout.md`.
- A4 does not add external provider deletion, CRM/utility/contractor integration, legal advice, production privacy workflow, frontend UI, dependency installs, lockfile rewrites, secrets, push, deployment, billing, or operational control.
- Loop C1 / Phases 18-19 UI shell is implemented in the working tree. It adds local auth headers to the React API client and a `/experience` route with Explore/Twin/Plan/Build tabs, fact/load/geometry summaries, and a lightweight HomeDiagram-style SVG visual.
- C1 changed `apps/web/src/lib/api.js`, `apps/web/src/app/App.jsx`, `apps/web/src/pages/C1ExperiencePage.jsx`, `apps/web/src/styles/global.css`, docs/API/continuity files, and `docs/handoffs/2026-06-13-c1-ui-shell-closeout.md`.
- C1 does not add dependencies, lockfile rewrites, Three.js package, external services, production auth provider, deployment, push, billing, operational control, final design claims, or permissioned export UI.
- Loop B3 Hardened Evidence Intake is implemented in the working tree. It adds a local validated photo-evidence-to-fact endpoint that creates B1 photo-verified facts after rejecting malformed or unsupported evidence metadata.
- B3 changed `apps/api/app/evidence/__init__.py`, `apps/api/app/evidence/schemas.py`, `apps/api/app/evidence/router.py`, `apps/api/app/services/evidence.py`, `apps/api/app/main.py`, `apps/api/app/security/auth.py`, `apps/api/tests/test_evidence.py`, docs/API/continuity files, and `docs/handoffs/2026-06-13-b3-evidence-intake-closeout.md`.
- B3 does not store raw files, perform OCR, call AI extraction, scan malware, add external providers, add dependencies, rewrite lockfiles, add frontend capture UI, add production storage, expose secrets, deploy, push, or perform field verification.
- Session date: 2026-06-04
- Starting head commit: `7f493b1`
- Current continuation starting head: `f666ec3`
- Latest committed checkpoint before Phase 5A automation: `74448241f955d6a5b98ff09d0c2ddf6edb117dbd`
- Latest commit before Phase 5A automation: `docs: record phase 4 closeout`
- Current branch: `fix/github-workflow`
- Upstream tracking branch: `origin/fix/github-workflow`
- GitHub preservation remote: `https://github.com/0xSk8babylon/resi-twin.git`
- GitHub preservation backup: succeeded on `fix/github-workflow`
- Phase 1 Planner Foundation is complete.
- Phase 2A Twin Doctrine Foundation is complete.
- The Residential Energy Twin Canonical Architecture Hierarchy has been added as a docs-only consolidation layer for routing existing doctrine without creating new domains or starting Exchange, Ownership & Transfer, Registry, Identity, API, schema, protocol, or runtime work.
- Phase 3A Derived Dependency Impact Readiness is complete in `97b57fb`.
- Phase 3B Derived Dependency Reasoning complete in `d56f52e`.
- Phase 3C Planning Intelligence Readiness complete in `a22042d`.
- Phase 3D Advisory Context Assembly complete in `1120998`.
- Phase 3E Constraint and Risk Reasoning complete in `ee3b102`.
- Phase 3F Scenario Comparison Readiness complete in `5a762a0`.
- Phase 3G Pre-Recommendation Advisory complete in `5883985`.
- Phase 3H Recommendation Eligibility Readiness complete in `958f3e0`.
- Phase 3I Basic Advisory Recommendations complete in `2f1b4bd`.
- Phase 3 derived-view assembly stabilization complete in `f1fbc7b`.
- Phase 3J Contractor-Facing Advisory Logic complete in `58bd14f`.
- Phase 3K Homeowner-Facing Advisory Logic complete in `5814c18`.
- Phase 3L Energy Goal Reasoning complete in `492d492`.
- Phase 3M Proposal Readiness Foundation complete in `916a6f5`.
- Phase 3N Product / Spec Intelligence Readiness complete in `39822c9`.
- Phase 3O Phase 3 Closeout Stabilization complete as docs-only continuity work.
- Phase 4 Trust / Provenance Maturity and Readiness Normalization is complete and closed out in `74448241f955d6a5b98ff09d0c2ddf6edb117dbd`.
- Phase 5A through Phase 5E Contractor Participant Foundation is complete and locally committed in `f616e9ac9e4d2a2b763d692a5135245d57eb6407` (`feat: add contractor participant read-only foundations`). Final status after commit was clean, and no push was run. Phase 5 runtime work remains read-only, request-time, deterministic, `home_id` anchored, provenance-bearing, contractor-safe, and non-authoritative.
- Phase 6A through Phase 6E Planning Exchange Object is complete and locally committed in `837d3ae` (`feat: add planning exchange object foundation`). Phase 6 adds `GET /api/planning-exchange/homes/{home_id}` as an additive read-only, request-time, deterministic, provenance-bearing, non-authoritative, `home_id`-anchored package over existing planning context and Phase 5 contractor-context outputs. Focused backend tests passed with `142 tests OK`; full backend discovery passed with `153 tests OK`; no push was run.
- Phase 7 Shared Compatibility & Install Path View is complete and locally committed in `7941469` (`feat: add shared compatibility install path view`). Phase 7 adds `GET /api/twin-planning-context/homes/{home_id}/views/shared-compatibility` as an additive read-only, request-time, deterministic, provenance-bearing, non-authoritative, `home_id`-anchored derived compatibility classification view over existing `TwinPlanningContext`, topology/readiness outputs, Phase 5 contractor confirmation gates/install complexity signals, and the Phase 6 Planning Exchange Object. The response includes path statuses, reasons, basis/provenance, basis-quality metadata, missing information, blockers, contractor confirmation gates, required site/product verifications, summary rollups, and homeowner-safe/contractor-facing interpretation metadata. Focused Phase 7 tests passed with `6 tests OK`; full twin planning context tests passed with `148 tests OK`; `git diff --check` passed; no push was run.
- Phase 8 Topology Takeoff & Material Cost Engine is complete and locally committed in `1058277` (`feat: add topology takeoff material cost view`). Phase 8 adds `GET /api/twin-planning-context/homes/{home_id}/views/topology-takeoff` as an additive read-only, request-time, deterministic, provenance-bearing, non-authoritative, `home_id`-anchored planning-grade topology takeoff view over existing `TwinPlanningContext`, topology snapshot, Phase 7 shared compatibility, Phase 5 contractor confirmation gates/install complexity signals, and the Phase 6 Planning Exchange Object. The response includes takeoff scope metadata, topology basis/provenance, summary rollups, material/scope line items, quantity-basis posture, cost-basis-unavailable metadata, uncertainty, missing information, blockers, homeowner-safe and contractor-facing interpretation metadata, and carried-forward confirmation gates. Focused Phase 8 tests passed with `7 tests OK`; focused Phase 7 regression tests passed with `6 tests OK`; full twin planning context tests passed with `155 tests OK`; no push was run.
- Phase 9 Estimate Readiness / Confirmation Gates is complete and locally committed in `9f20dce` (`feat: add phase 9 estimate readiness gates`); no push was run.
- Phase 10 Proposal Option Sets is complete and locally committed in `bb15b6a` (`feat: add phase 10 proposal option sets`). Phase 10 adds `GET /api/proposal-option-sets/homes/{home_id}` as an additive read-only, request-time, deterministic, provenance-bearing, non-authoritative, `home_id`-anchored derived option-set readiness layer over Phase 3M proposal readiness, Phase 6 planning exchange, Phase 9-carried shared compatibility and topology takeoff refs, Phase 9 estimate readiness, and existing scenario/design records. Focused Phase 10 tests passed with `8 tests OK`; `git diff --check` passed; no push was run.
- Phase 11 Contractor Workflow Readiness is complete and locally committed in `544c3a0` (`feat: add phase 11 contractor workflow readiness`). Phase 11 adds `GET /api/contractor-workflow/homes/{home_id}/readiness` as an additive read-only, request-time, deterministic, provenance-bearing, non-authoritative, `home_id`-anchored contractor workflow readiness projection over Phase 5 contractor context, Phase 6 planning exchange, Phase 9 estimate readiness, and Phase 10 proposal option sets. Phase 7/8 basis is carried only where already surfaced through existing contracts. Focused Phase 11 tests passed with `8 tests OK` in about 141s; `git diff --check` passed; the session-report email preflight passed; no push was approved or run.
- Phase 12 Product Preference & Install Logic is complete and locally committed in `4900fad` (`feat: add phase 12 product preference logic`). Phase 12 adds `GET /api/product-preferences/homes/{home_id}` as an additive read-only, request-time, deterministic, provenance-bearing, non-authoritative, `home_id`-anchored product preference and install-logic guidance layer over Phase 7 shared compatibility, Phase 8 topology takeoff, Phase 9 estimate readiness, and Phase 10 proposal option sets. Unsupported categories remain source-limited with explicit missing inputs. Direct Phase 11 workflow rebuild is intentionally not used in runtime composition because it is expensive and unnecessary for Phase 12 category derivation. Focused Phase 12 tests passed with `8 tests OK` in `344.870s`; `py_compile` and `git diff --check` passed; broad backend discovery was not run because the focused suite took about 345s and prior adjacent full discovery timed out under the current cap.
- Phase 13 Post-Install Retention & CRM Handoff is implemented in the working tree and not staged or committed. Phase 13 adds `GET /api/post-install/homes/{home_id}` and `GET /api/crm-handoff/homes/{home_id}` as additive read-only, request-time, deterministic, provenance-bearing, non-authoritative, `home_id`-anchored post-install retention readiness and manual CRM handoff object metadata. Runtime composes Phase 11 contractor workflow readiness and Phase 12 product preference metadata directly, carrying Phase 9/10 refs only where those source contracts already surface them. Focused Phase 13 tests were optimized to avoid redundant lower-phase rebuilds and passed with `6 tests OK` in `0.694s`; `py_compile` passed. Final verification is pending. No persistence, migrations, writes, auth/security, permission enforcement, external CRM integration, CRM writes, email/drip campaign product behavior, task creation, sales scoring, lead scoring, ranking, best upsell logic, push behavior, frontend, pricing/proposal generation, external services/secrets, `twin_id`, graph behavior, operational behavior, staging, commit, or push has been performed.
- Phase 14 Energy Passport is implemented in the working tree and not staged or committed. Phase 14 adds `GET /api/energy-passport/homes/{home_id}` as an additive read-only, request-time, deterministic, provenance-bearing, non-authoritative, `home_id`-anchored homeowner-safe Energy Passport summary over existing Phase 6 through Phase 13 source surfaces where available. Gate 14A was resumed by changing `EnergyPassportView.data_classification` to the existing `DataClassification.planning_private` enum instead of adding a new enum or changing `core/types.py`. Verification passed: Gate 14A compile/import checks, focused Phase 14 tests `7 tests OK`, adjacent Phase 13 + Phase 14 regression `13 tests OK`, and `git diff --check`. No persistence, migrations, writes, auth/security, permission enforcement, external integrations, CRM writes, MLS/title/escrow/deed/legal transfer logic, warranty validation, permit validation, payoff calculation, lien/title/UCC search, appraisal, underwriting, tax-credit or financial conclusions, deploy, staging, commit, or push has been performed.
- Phase 15 Program Intelligence & Grid Edge Readiness is implemented in the working tree and not committed. Phase 15 adds `GET /api/program-intelligence/homes/{home_id}` as an additive read-only, request-time, deterministic, provenance-bearing, non-authoritative, `home_id`-anchored program/grid-edge awareness view over existing `TwinPlanningContext` records. It reports utility context, program categories, incentive awareness, demand response awareness, VPP awareness, TOU awareness, interconnection awareness, battery/load-shifting/backup/smart-panel/EV/DER-aggregation readiness indicators, missing inputs, blockers, confirmation gates, assumptions, dependencies, homeowner-safe summaries, contractor/program review prompts, and source/provenance basis. Verification passed: `py_compile`; focused Phase 15 tests `6 tests OK`; `git diff --check`. No persistence, migrations, writes, background jobs, external API calls, auth/security changes, permission enforcement, enrollment workflows, rebate/incentive calculations, tariff optimization, utility dispatch, device control, demand response execution, grid-services execution, billing/pricing logic, proposal generation, CRM integration, email automation, exports, pushes, commit, or deploy has been performed.
- Dependency Impact Propagation milestone approved by Matt for docs-only commit in this session.
- Phase 2B Twin Runtime Expression is complete and stabilized for the current approved runtime scope: `TwinPlanningContext`, Runtime View Foundations, Dependency Awareness Foundations, and Permission Foundations.
- Phase 2C Topology + Lifecycle Intelligence Foundations are complete for the approved foundation scope: Topology Snapshot Foundation in `0c5bf23`, Lifecycle Readiness Foundation in `0d62693`, and Topology Relationship Coverage Foundation in `d56dbd6`.
- Phase 3A Derived Dependency Impact Readiness is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored derived intelligence envelope over existing `TwinPlanningContext` and topology snapshot outputs.
- Phase 3B Derived Dependency Reasoning is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored explanation view over existing `TwinPlanningContext`, topology snapshot, and Phase 3A dependency impact readiness outputs.
- Phase 3C Planning Intelligence Readiness is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored readiness inventory over existing `TwinPlanningContext`, topology snapshot, Phase 3A dependency impact readiness, and Phase 3B dependency reasoning outputs.
- Phase 3D Advisory Context Assembly is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored advisory input context assembly view over existing `TwinPlanningContext`, topology snapshot, Phase 3A dependency impact readiness, Phase 3B dependency reasoning, and Phase 3C planning intelligence readiness outputs.
- Phase 3E Constraint and Risk Reasoning is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored constraint/risk explanation view over existing `TwinPlanningContext`, topology snapshot, Phase 3A dependency impact readiness, Phase 3B dependency reasoning, Phase 3C planning intelligence readiness, and Phase 3D advisory context assembly outputs.
- Phase 3F Scenario Comparison Readiness is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored readiness inventory over existing `TwinPlanningContext`, topology snapshot, Phase 3C planning intelligence readiness, Phase 3D advisory context assembly, and Phase 3E constraint/risk reasoning outputs.
- Phase 3G Pre-Recommendation Advisory is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored advisory boundary view over existing `TwinPlanningContext`, topology snapshot, Phase 3C planning intelligence readiness, Phase 3D advisory context assembly, Phase 3E constraint/risk reasoning, and Phase 3F scenario comparison readiness outputs.
- Phase 3H Recommendation Eligibility Readiness is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored recommendation-readiness gate over existing `TwinPlanningContext`, topology snapshot, Phase 3C planning intelligence readiness, Phase 3D advisory context assembly, Phase 3E constraint/risk reasoning, Phase 3F scenario comparison readiness, and Phase 3G pre-recommendation advisory outputs.
- Phase 3I Basic Advisory Recommendations is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored prerequisite/remediation recommendation view over existing `TwinPlanningContext`, topology snapshot, Phase 3C planning intelligence readiness, Phase 3D advisory context assembly, Phase 3E constraint/risk reasoning, Phase 3F scenario comparison readiness, Phase 3G pre-recommendation advisory, and Phase 3H recommendation eligibility readiness outputs.
- Phase 3 derived-view assembly stabilization is complete for the approved internal service-layer boundary: request-time `TwinPlanningContext`, topology snapshot, and Phase 3A through Phase 3I derived view objects are reused inside a single builder chain to avoid recursive rebuilding. This changed no endpoints, schemas, routers, persistence, response shapes, frontend behavior, auth, permission enforcement, exports, graph behavior, `twin_id`, operational behavior, or Phase 3J scope.
- Phase 3J Contractor-Facing Advisory Logic is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored contractor-facing translation view over existing `TwinPlanningContext`, topology snapshot, and Phase 3C through Phase 3I readiness/advisory/recommendation context.
- Phase 3K Homeowner-Facing Advisory Logic is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored homeowner-facing translation view over existing `TwinPlanningContext`, topology snapshot, and Phase 3C through Phase 3I readiness/advisory/recommendation context.
- Phase 3L Energy Goal Reasoning is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored goal-to-context reasoning view over existing `TwinPlanningContext`, topology snapshot, and Phase 3D through Phase 3K advisory/readiness/recommendation context.
- Phase 3M Proposal Readiness Foundation is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored proposal-readiness view over existing `TwinPlanningContext`, topology snapshot, and Phase 3E through Phase 3L readiness/advisory/reasoning context.
- Phase 3N Product / Spec Intelligence Readiness is complete for the approved boundary as an additive read-only, request-time, `home_id`-anchored product/spec readiness view over existing `TwinPlanningContext`, topology snapshot, and Phase 3E through Phase 3M readiness/advisory context.
- Phase 3O Phase 3 Closeout Stabilization is complete as docs-only continuity work. It records Phase 3A through Phase 3N completion, derived-view assembly stabilization, all Phase 3 endpoints, latest recorded verification, deferred boundaries, and Phase 4 assessment-only readiness without adding runtime features or changing roadmap/doctrine.
- Phase 4 runtime work was implemented only after approved assessment-backed slices: Phase 4A per-view summaries in `7510e6a`, Phase 4B cross-view index endpoint in `c933748`, and Phase 4C through Phase 4E metadata normalization/language hardening in `79d1b47`.
- Provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, Exchange, Ownership & Transfer, Registry, Identity, canonical Twin runtime identity, permission enforcement, scoped exports, and operational control remain unapproved.
- `.github/` remains out of scope for this session.
- Current doctrine now normalizes the Residential Energy Planner as the first application, the Residential Energy Twin as the core asset, Trusted Residential Energy Record as current positioning, Residential Infrastructure Registry as the long-term end state, and Residential Infrastructure Network as the long-term vision.
- The normalized doctrine states that the planner is not the long-term moat; Twin adoption, trusted records, permissions, provenance, continuity, interoperability, ecosystem participation, and network effects are the strategic moat.
- Current doctrine now includes a docs-only Residential Energy Twin Interoperability Domain for shared cross-industry semantic interpretation without approving exchange mechanisms, ownership transfer, APIs, schemas, protocols, standards, exports, or runtime implementation.
- Current doctrine now includes a docs-only Ecosystem Participant Boundary Matrix that consolidates participant-purpose boundaries before any Exchange Domain work without creating a new Twin domain or approving exchange, ownership transfer, APIs, schemas, protocols, or runtime implementation.
- Repo commits created this session:
  - Residential Energy Twin Contract v1 docs-only governance commit
  - Residential Energy Twin first runtime-boundary planning docs-only commit
  - Residential Energy Twin governance discoverability stabilization docs-only commit
  - Residential Energy Twin provenance policy planning docs-only commit
  - Residential Energy Twin permissioned view planning docs-only commit
  - Residential Energy Twin governance/design milestone closeout docs-only commit
  - Dependency Impact Propagation docs-only milestone commit
  - Residential Energy Twin Canonical Architecture Hierarchy docs-only milestone commit
  - `b854b9e` `feat: add twin planning context service`
  - `7a2fddc` `feat: add typed provenance gaps to twin planning context`
  - `cf19dea` `feat: add AI design grounding view for twin planning context`
  - `e4d7656` `feat: add dependency awareness labels to twin planning context`
  - `8d00f91` `feat: add permission readiness metadata to twin planning context`
  - `eab68fc` `feat: add twin runtime view foundations`
  - `fd61372` `feat: add twin dependency awareness foundations`
  - `b69f3db` `feat: add twin permission readiness foundations`
  - `e0f6153` `docs: align Phase 2B runtime foundation continuity state`
  - `4602249` `docs: align discovery index phase 2b status`
  - `0c5bf23` `feat: add twin topology snapshot foundation`
  - `4fbfea5` `docs: align phase 2c topology snapshot continuity state`
  - `0d62693` `feat: add topology lifecycle readiness foundations`
  - `2fadbac` `docs: align phase 2c lifecycle readiness continuity state`
  - `d56dbd6` `feat: add topology relationship coverage foundations`
  - `8e23cd8` `docs: align phase 2c relationship coverage continuity state`
  - `97b57fb` `feat: add dependency impact readiness view`
  - `5e35926` `docs: align phase 3a dependency impact readiness continuity`
  - `d56f52e` `feat: add dependency reasoning view`
  - `f397e17` `docs: record phase 3b dependency reasoning closeout`
  - `a22042d` `feat: add planning intelligence readiness view`
  - `2f537bf` `docs: record phase 3c planning intelligence readiness closeout`
  - `1120998` `feat: add advisory context assembly view`
  - `d622d96` `docs: record phase 3d advisory context assembly closeout`
  - `ee3b102` `feat: add constraint risk reasoning view`
  - `085f230` `docs: record phase 3e constraint risk reasoning closeout`
  - `5a762a0` `feat: add scenario comparison readiness view`
  - `035fb13` `docs: record phase 3f scenario comparison readiness closeout`
  - `5883985` `feat: add pre recommendation advisory view`
  - `fdb4bc9` `docs: record phase 3g pre recommendation advisory closeout`
  - `958f3e0` `feat: add recommendation eligibility readiness view`
  - `052eae3` `docs: record phase 3h recommendation eligibility readiness closeout`
  - `2f1b4bd` `feat: add basic advisory recommendations view`
  - `8d4bea1` `docs: record phase 3i basic advisory recommendations closeout`
  - `f1fbc7b` `fix: reuse derived planning view assembly inputs`
  - `e4d5f70` `docs: record phase 3 derived view assembly stabilization`
  - `58bd14f` `feat: add contractor facing advisory view`
  - `7d7f698` `docs: record phase 3j contractor facing advisory closeout`
  - `5814c18` `feat: add homeowner facing advisory view`
  - `fa98f0a` `docs: record phase 3k homeowner facing advisory closeout`
  - `492d492` `feat: add energy goal reasoning view`
  - `031d3df` `docs: record phase 3l energy goal reasoning closeout`
  - `916a6f5` `feat: add proposal readiness foundation view`
  - `fe524ac` `docs: record phase 3m proposal readiness foundation closeout`
  - `39822c9` `feat: add product spec readiness view`
  - `ca682b6` `docs: record phase 3n product spec readiness closeout`
  - `aebd4e8` `docs: record phase 3 closeout stabilization`
  - `c6ff1c7` `docs: define phase 4 boundary charter`
  - `7510e6a` `feat: add phase 4a trust provenance readiness summaries`
  - `c933748` `feat: add phase 4b trust provenance readiness index`
  - `79d1b47` `feat: normalize phase 4 trust readiness metadata`
- Current Phase 4 closeout checkpoint:
  - Phase 4 is defined as Trust / Provenance Maturity and Readiness Normalization. Phase 3 is closed and serves as the source foundation. Phase 4A through Phase 4E runtime normalization is complete and committed. Phase 4 closeout is committed in `74448241f955d6a5b98ff09d0c2ddf6edb117dbd`.
- Current Phase 5 checkpoint:
  - Phase 5 is defined as Contractor Participant Foundation. Phase 5A through Phase 5E is complete and locally committed in `f616e9ac9e4d2a2b763d692a5135245d57eb6407`; no push was run. Phase 5A is docs-only charter work defining the contractor participant role, contractor-safe visibility model, read-only mutability boundary, trust/provenance boundaries, confirmation gate lifecycle, install complexity categories, future contractor observation doctrine, forbidden scope, verification requirements, and approved Phase 5B through Phase 5D runtime boundaries. Phase 5B through Phase 5D add read-only derived contractor-context endpoints. Phase 5E documents future contractor observation doctrine only. No Phase 5 write endpoint, persistence, migration, auth/security change, permission enforcement, contractor account, frontend, export, marketplace/CRM/payment behavior, source-of-truth mutation, or final electrical sizing/design claim is approved or implemented.
- Current Phase 6 checkpoint:
  - Phase 6 is defined as Planning Exchange Object. Phase 6A through Phase 6E is complete and locally committed in `837d3ae`; no push was run. Phase 6A adds `docs/phase-6-planning-exchange-object.md` as the docs-only charter. Phase 6B through Phase 6E add a read-only derived planning exchange package at `GET /api/planning-exchange/homes/{home_id}` that composes existing planning context plus Phase 5B contractor planning context, Phase 5C confirmation gates, and Phase 5D install complexity signals. Runtime files changed are `apps/api/app/planning_exchange/__init__.py`, `apps/api/app/planning_exchange/schemas.py`, `apps/api/app/planning_exchange/router.py`, `apps/api/app/services/planning_exchange.py`, `apps/api/app/main.py`, and `apps/api/tests/test_twin_planning_context.py`. The endpoint is additive, `home_id` anchored, request-time derived, deterministic, provenance-bearing, non-authoritative, and not a source of truth. No persistence, migrations, write endpoints, exports/PDFs/share links, auth/security changes, permission enforcement, frontend work, pricing/proposals, final electrical sizing, final design claims, `twin_id`, graph behavior, marketplace/CRM/payment behavior, or operational behavior was introduced. Verification passed: focused backend tests `142 tests OK`; full backend discovery `153 tests OK`.
- Current Phase 7 checkpoint:
  - Phase 7 is defined as Shared Compatibility & Install Path View. Phase 7 is complete and locally committed in `7941469`; no push was run. Phase 7 adds backend read-only schemas, service logic, and route support for `GET /api/twin-planning-context/homes/{home_id}/views/shared-compatibility`. The view classifies PV only, PV + battery, PV + battery + partial backup, PV + battery + whole-home backup, PV + generator interlock, PV + generator + battery, critical-loads subpanel, service-upgrade likely, load-management, and existing-panel-reuse paths as compatible, likely compatible, blocked, unknown, or requiring contractor confirmation. Every path includes status, reason, basis/provenance, basis-quality metadata, source-ref categories, missing information where relevant, blockers, assumptions, required site/product verification gates, and contractor confirmation gates. The top-level response includes summary rollups and homeowner-safe/contractor-facing interpretation metadata. Runtime files changed were `apps/api/app/twin_planning_context/schemas.py`, `apps/api/app/twin_planning_context/router.py`, `apps/api/app/services/twin_planning_context.py`, and `apps/api/tests/test_twin_planning_context.py`. No persistence, migrations, write endpoints, auth/security changes, permission enforcement, frontend work, exports, pricing/proposals, recommendations ranking, scenario engine expansion, graph behavior, `twin_id`, operational behavior, final wire/conduit/breaker sizing, final disconnect/OCPD approval, permit-ready design, AHJ/utility approval, field-verification approval, or final electrical design output was introduced. Verification passed: focused Phase 7 tests `6 tests OK`; full twin planning context backend tests `148 tests OK`; `git diff --check` passed.
- Current Phase 8 checkpoint:
  - Phase 8 is defined as Topology Takeoff & Material Cost Engine. Phase 8 is complete and locally committed in `1058277`; no push was run. Phase 8 adds backend read-only schemas, service logic, and route support for `GET /api/twin-planning-context/homes/{home_id}/views/topology-takeoff`. The view derives planning-grade material/scope categories from existing topology and planning context. Runtime files changed were `apps/api/app/twin_planning_context/schemas.py`, `apps/api/app/twin_planning_context/router.py`, `apps/api/app/services/twin_planning_context.py`, and `apps/api/tests/test_twin_planning_context.py`. Verification passed: focused Phase 8 tests `7 tests OK`; focused Phase 7 regression tests `6 tests OK`; full twin planning context backend tests `155 tests OK`.
- Current Phase 9 checkpoint:
  - Phase 9 is defined as Estimate Readiness / Confirmation Gates. Phase 9 is complete and locally committed in `9f20dce`; no push was run. Phase 9 adds backend read-only schemas, service logic, route support, and focused tests for `GET /api/estimate-readiness/homes/{home_id}`. The view builds a versioned 19-gate estimate-readiness registry from existing Phase 5 confirmation gates, connects required gates to current topology/scenario complexity, classifies blockers and missing inputs, separates homeowner-safe summary from contractor-facing notes, and reports estimate allowance plus contractor-review requirement without generating estimates or proposals. Runtime files changed are `apps/api/app/estimate_readiness/__init__.py`, `apps/api/app/estimate_readiness/schemas.py`, `apps/api/app/estimate_readiness/router.py`, `apps/api/app/services/estimate_readiness.py`, `apps/api/app/main.py`, and `apps/api/tests/test_estimate_readiness.py`. No persistence, migrations, write endpoints, auth/security changes, permission enforcement, frontend work, exports, pricing/proposals, final estimate, final bill of materials, contractor-approved scope, final wire/conduit/breaker sizing, final disconnect/OCPD approval, permit-ready design, AHJ/utility approval, field-verification approval, graph behavior, `twin_id`, operational behavior, or final electrical design output was introduced. Verification passed: focused Phase 9 tests `7 tests OK`; existing twin planning context regression tests `155 tests OK`.
- Current Phase 10 checkpoint:
  - Phase 10 is defined as Proposal Option Sets. Phase 10 is complete and locally committed in `bb15b6a`; no push was run. Phase 10 adds backend read-only schemas, service logic, route support, and focused tests for `GET /api/proposal-option-sets/homes/{home_id}`. The view assembles proposal option-set readiness candidates from existing scenario/design context and the Phase 3M, Phase 6, Phase 9-carried compatibility/takeoff, and Phase 9 estimate-readiness surfaces. Runtime files changed are `apps/api/app/proposal_option_sets/__init__.py`, `apps/api/app/proposal_option_sets/schemas.py`, `apps/api/app/proposal_option_sets/router.py`, `apps/api/app/services/proposal_option_sets.py`, `apps/api/app/main.py`, and `apps/api/tests/test_proposal_option_sets.py`. No persistence, migrations, write endpoints, auth/security changes, permission enforcement, frontend work, exports, CRM, email automation, pricing, quote/bid logic, final proposal generation, final estimate, final design, approval claims, final electrical sizing, graph behavior, `twin_id`, operational behavior, or source-of-truth mutation was introduced. Verification passed: focused Phase 10 tests `8 tests OK`; `git diff --check` passed.
- Current Phase 11 checkpoint:
  - Phase 11 is defined as Contractor Workflow Readiness. Phase 11A through Phase 11I is complete and locally committed in `544c3a0`; no push was approved or run. Runtime Phase 11A through Phase 11F adds backend read-only schemas, service logic, route support, and focused tests for `GET /api/contractor-workflow/homes/{home_id}/readiness`. The view opens the Contractor-Owned Workflow Layer as contractor-facing workflow readiness projection only, not true contractor-owned persisted workflow state. It composes existing Phase 5, Phase 6, Phase 9, and Phase 10 surfaces; carries Phase 7/8 basis only where already surfaced through existing contracts; and returns readiness lanes for planning review, missing-input review, confirmation-gate review, option-candidate review, and proposal-prep blocked/deferred. Runtime files changed are `apps/api/app/contractor_workflow/__init__.py`, `apps/api/app/contractor_workflow/schemas.py`, `apps/api/app/contractor_workflow/router.py`, `apps/api/app/services/contractor_workflow.py`, `apps/api/app/main.py`, and `apps/api/tests/test_contractor_workflow.py`. No POST/PATCH/DELETE, persistence, migrations, contractor-owned state, contractor accounts, auth/security/permission enforcement, approvals, pricing/bids/quotes, final proposal, final estimate, final design, CRM automation, product-runtime email automation, exports, external services/secrets, Phase 12+ work, graph behavior, `twin_id`, operational behavior, or source-of-truth mutation was introduced. Verification passed: `git diff --check`; `bash scripts/check_session_report_email_env.sh`; focused Phase 11 tests `8 tests OK` in about 141s. `pytest` is unavailable; full backend unittest discovery previously timed out at 900s with passing dots only.
- Current Phase 12 checkpoint:
  - Phase 12 is defined as Product Preference & Install Logic. Phase 12 runtime/tests are complete and locally committed in `4900fad`. Runtime adds backend read-only schemas, service logic, route support, and focused tests for `GET /api/product-preferences/homes/{home_id}`. The view derives supported product/install categories from existing Phase 7 shared compatibility, Phase 8 topology takeoff, Phase 9 estimate readiness, and Phase 10 proposal option-set outputs. Unsupported categories remain source-limited with explicit missing inputs rather than inferred preferences. Direct Phase 11 workflow rebuild is intentionally not used in runtime composition because it is expensive and unnecessary for category derivation. Runtime/test files changed are `apps/api/app/product_preferences/__init__.py`, `apps/api/app/product_preferences/schemas.py`, `apps/api/app/product_preferences/router.py`, `apps/api/app/services/product_preferences.py`, `apps/api/app/main.py`, and `apps/api/tests/test_product_preferences.py`. No final product recommendation, product ranking, best-option selection, pricing, live inventory, distributor quote, procurement, purchase link, payment, final BOM, final electrical design, manufacturer certification, warranty claim, CRM handoff, runtime email automation, frontend work, persistence, migration, write endpoint, auth/security, permission enforcement, external service/secret change, push, `twin_id`, graph behavior, operational behavior, or source-of-truth mutation was introduced. Verification passed: `py_compile`; focused Phase 12 tests `8 tests OK` in `344.870s`; `git diff --check`. Broad backend discovery was not run because the focused suite took about 345s and prior adjacent full discovery timed out under the current cap.

## Canonical Phase Structure

- Phase 1: Planner Foundation - complete.
- Phase 2A: Twin Doctrine Foundation - complete.
- Phase 2B: Twin Runtime Expression - complete for the current approved runtime scope.
- Phase 2C: Topology + Lifecycle Intelligence - complete for the approved foundation scope: Topology Snapshot Foundation, Lifecycle Readiness Foundation, and Topology Relationship Coverage Foundation.
- Phase 3A: Derived Dependency Impact Readiness - complete for the approved first runtime boundary in `97b57fb`.
- Phase 3B: Derived Dependency Reasoning - complete for the approved second runtime boundary in `d56f52e`.
- Phase 3C: Planning Intelligence Readiness - complete for the approved third runtime boundary in `a22042d`.
- Phase 3D: Advisory Context Assembly - complete for the approved fourth runtime boundary in `1120998`.
- Phase 3E: Constraint and Risk Reasoning - complete for the approved fifth runtime boundary in `ee3b102`.
- Phase 3F: Scenario Comparison Readiness - complete for the approved sixth runtime boundary in `5a762a0`.
- Phase 3G: Pre-Recommendation Advisory - complete for the approved seventh runtime boundary in `5883985`.
- Phase 3H: Recommendation Eligibility Readiness - complete for the approved eighth runtime boundary in `958f3e0`.
- Phase 3I: Basic Advisory Recommendations - complete for the approved ninth runtime boundary in `2f1b4bd`; broader Phase 3 remains deferred until Matt approves a new implementation boundary.
- Phase 3J: Contractor-Facing Advisory Logic - complete for the approved tenth runtime boundary in `58bd14f`.
- Phase 3K: Homeowner-Facing Advisory Logic - complete for the approved eleventh runtime boundary in `5814c18`.
- Phase 3L: Energy Goal Reasoning - complete for the approved twelfth runtime boundary in `492d492`.
- Phase 3M: Proposal Readiness Foundation - complete for the approved thirteenth runtime boundary in `916a6f5`.
- Phase 3N: Product / Spec Intelligence Readiness - complete for the approved fourteenth runtime boundary in `39822c9`; broader Phase 3 remains deferred until Matt approves a new implementation boundary.
- Phase 3O: Phase 3 Closeout Stabilization - complete as docs-only continuity closeout. Phase 3O is not Phase 4 planning implementation and does not add runtime behavior.
- Phase 4: Trust / Provenance Maturity and Readiness Normalization - complete through approved runtime slices 4A through 4E and docs-only closeout in `74448241f955d6a5b98ff09d0c2ddf6edb117dbd`.
- Phase 5A: Contractor Participant Charter - approved as docs-only boundary work.
- Phase 5B: Contractor-Scoped Planning View - complete in the working tree as a read-only derived contractor-safe planning context endpoint.
- Phase 5C: Confirmation Gate Projection - complete in the working tree as a read-only derived 19-gate readiness projection.
- Phase 5D: Install Complexity Signals - complete in the working tree as read-only derived uncertainty and review-burden signals.
- Phase 5E: Contractor Observation Doctrine - complete in the working tree as docs-only future append-only observation doctrine.
- Phase 6A: Planning Exchange Object Charter - complete in the working tree as docs-only boundary work.
- Phase 6B: Read-only Exchange Object Schema - complete in the working tree as an additive backend response contract.
- Phase 6C: Exchange Package Endpoint - complete in the working tree as `GET /api/planning-exchange/homes/{home_id}`.
- Phase 6D: Exchange Provenance / Trust Boundary Mapping - complete in the working tree as section-level source/trust mapping.
- Phase 6E: Exchange Readiness Summary - complete in the working tree as planning-review readiness posture only.
- Phase 7: Shared Compatibility & Install Path View - complete and locally committed in `7941469` as `GET /api/twin-planning-context/homes/{home_id}/views/shared-compatibility`.
- Phase 8: Topology Takeoff & Material Cost Engine - complete and locally committed in `1058277` as `GET /api/twin-planning-context/homes/{home_id}/views/topology-takeoff`.
- Phase 9: Estimate Readiness / Confirmation Gates - complete and locally committed in `9f20dce` as `GET /api/estimate-readiness/homes/{home_id}`.
- Phase 10: Proposal Option Sets - complete and locally committed in `bb15b6a` as `GET /api/proposal-option-sets/homes/{home_id}`.
- Phase 11: Contractor Workflow Readiness - complete and locally committed in `544c3a0` as `GET /api/contractor-workflow/homes/{home_id}/readiness`.
- Phase 12: Product Preference & Install Logic - complete and locally committed in `4900fad` as `GET /api/product-preferences/homes/{home_id}`.
- Phase 13: Post-Install Retention & CRM Handoff - implemented in the working tree as `GET /api/post-install/homes/{home_id}` and `GET /api/crm-handoff/homes/{home_id}`.
- Phase 14: Energy Passport - implemented in the working tree as `GET /api/energy-passport/homes/{home_id}`.
- Phase 15: Program Intelligence & Grid Edge Readiness - implemented in the working tree as `GET /api/program-intelligence/homes/{home_id}`.

## What Changed Last

- B1 Fact Lifecycle was implemented for the Auto-Loop Roadmap Runner.
- Added backend fact lifecycle package, schemas, router, and deterministic service logic under `apps/api/app/facts/` and `apps/api/app/services/facts.py`.
- Added `FactSource`, `FactConfidenceTier`, and `FactDecayPolicy` enums.
- Added the SQLAlchemy `Fact` model and home relationship without creating an Alembic migration file.
- Updated `apps/api/app/main.py` to include the fact lifecycle router under `/api`.
- Added `apps/api/tests/test_facts.py` with focused coverage for route registration, create/read effective confidence, update `verified_at` reset, derived parent IDs, no/slow/standard/fast decay policies, known-to-missing transition, expiry behavior, and named calculation gap reporting.
- Updated roadmap/API/continuity docs for B1.

- B2 NEC 220 Load Calculation was implemented under Matt's session-only NEC/calculation override.
- Added backend read-only NEC load-calculation schemas, router, service, and focused tests for `GET /api/homes/{home_id}/load-calculations/nec-220`.
- Updated the B1 fact gap registry with `nec_220_83` and additional NEC defaultable input keys.
- Updated continuity and API docs for B2.

- B4 Calculator Primitives was implemented under Matt's session-only calculation override.
- Added pure deterministic calculator primitives and focused tests.
- Updated continuity docs for B4.

- B5 Hourly Simulation was implemented under Matt's broad roadmap override.
- Added pure deterministic hourly simulation engine and focused tests.
- Updated continuity docs for B5.

- Phase 20 Geometry was implemented under Matt's broad roadmap override.
- Added home-scoped roof-plane and obstruction storage/query surfaces and a geometry export with per-plane shading.
- Updated API and continuity docs for Phase 20.

- B6 Sizers was implemented under Matt's broad roadmap override.
- Added pure deterministic sizer primitives and focused tests.
- Updated continuity docs for B6.

- B7 / Phase 21 Graph Comparator and Smart Panel Scoring was implemented under Matt's broad roadmap override.
- Added pure deterministic graph comparator and smart-panel scoring primitives.
- Updated continuity docs for B7.

- A2 Auth + Object Authorization + Audit Logging was implemented under Matt's broad roadmap override.
- Added local provider-free home-data auth middleware and audit logging.
- Updated API and continuity docs for A2.

- A4 Privacy / CCPA was implemented under Matt's broad roadmap override.
- Added local homeowner export, consent record, and deletion foundations.
- Updated API and continuity docs for A4.

- C1 / Phases 18-19 UI shell was implemented under Matt's broad roadmap override.
- Added authenticated API client headers and a four-surface homeowner workspace route.
- Updated API and continuity docs for C1.

- B3 Hardened Evidence Intake was implemented under Matt's broad roadmap override.
- Added local validated evidence-to-fact endpoint and focused tests.
- Updated API and continuity docs for B3.

- Phase 15 Program Intelligence & Grid Edge Readiness is implemented in the working tree and not committed.
- Added backend read-only program-intelligence schemas, router, service, and package files under `apps/api/app/program_intelligence/` plus `apps/api/app/services/program_intelligence.py`.
- Updated `apps/api/app/main.py` to include the program-intelligence router under `/api`.
- Added `apps/api/tests/test_program_intelligence.py` with focused coverage for route registration, deterministic output, unknown-input degradation, required program/readiness sections, source/provenance reporting, and false hard-stop flags for eligibility, enrollment, dispatch/control, pricing/billing, persistence, writes, external calls, and permission enforcement.
- Updated continuity and API docs in `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, `docs/API_CONTRACTS.md`, and `docs/handoffs/2026-06-05-phase-15-program-intelligence-closeout.md`.
- Verification passed: `python3 -m py_compile app/program_intelligence/schemas.py app/program_intelligence/router.py app/services/program_intelligence.py app/main.py tests/test_program_intelligence.py`; focused Phase 15 tests `6 tests OK`; `git diff --check`.
- No persistence, migration, write endpoint, background job, external API call, auth/security change, permission enforcement, enrollment workflow, rebate/incentive calculation, tariff optimization, utility dispatch, device control, demand response execution, grid-services execution, billing/pricing logic, proposal generation, CRM integration, email automation, export, push, commit, or deploy has been performed during Phase 15.

- Phase 10 Proposal Option Sets is complete and locally committed in `bb15b6a`.
- Added backend read-only proposal-option-set schemas, router, service, and package files under `apps/api/app/proposal_option_sets/` plus `apps/api/app/services/proposal_option_sets.py`.
- Updated `apps/api/app/main.py` to include the proposal-option-sets router under `/api`.
- Added `apps/api/tests/test_proposal_option_sets.py` with focused coverage for route presence, deterministic read-only response, `home_id` anchoring, no persistence mutation, source/scenario/design basis, Phase 9 blocker/missing-input/gate carry-through, forbidden boundary flags, homeowner-safe text, contractor review-prompt language, and sorted deferred boundaries.
- Updated continuity and API docs in `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, `docs/API_CONTRACTS.md`, and `docs/handoffs/2026-06-05-phase-10-proposal-option-sets-closeout.md`.
- Verification passed: focused Phase 10 tests `8 tests OK`; `git diff --check` passed.
- No frontend, persistence, migration, auth/security, permission enforcement, write endpoint, export/PDF/share link, pricing, quote/bid logic, final proposal generation, final estimate, final design, approval claims, final electrical sizing, CRM, email automation, `twin_id`, graph, operational behavior, push, or source-of-truth mutation work has been performed during Phase 10.
- Known caveat: Phase 9 scenario readiness remains home-level metadata, so Phase 10 candidates inherit that limitation rather than claiming scenario-specific estimate/proposal readiness.

- Phase 11 Contractor Workflow Readiness is complete and locally committed in `544c3a0`; no push was approved or run.
- Added backend read-only contractor-workflow schemas, router, service, and package files under `apps/api/app/contractor_workflow/` plus `apps/api/app/services/contractor_workflow.py`.
- Updated `apps/api/app/main.py` to include the contractor-workflow router under `/api`.
- Added `apps/api/tests/test_contractor_workflow.py` with focused coverage for route presence/handler response, deterministic lane ordering, no persistence mutation, forbidden boundary flags, non-authoritative wording, Phase 10 proposal option-set basis consumption, blocker/missing-input/gate carry-forward, homeowner-safe summary, contractor-facing prompts, and source/provenance basis.
- Updated continuity and API docs in `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, `docs/API_CONTRACTS.md`, and `docs/handoffs/2026-06-05-phase-11-contractor-workflow-readiness-closeout.md`.
- Verification passed: `git diff --check`; `bash scripts/check_session_report_email_env.sh`; focused Phase 11 tests `8 tests OK` in about 141s.
- `pytest` is unavailable; full backend unittest discovery previously timed out at 900s with passing dots only.
- No POST/PATCH/DELETE, persistence, migration, contractor-owned state, contractor account, auth/security, permission enforcement, approval tracking, pricing, bid/quote logic, final proposal, final estimate, final design, CRM automation, product-runtime email automation, export, external service/secret change, Phase 12+ work, `twin_id`, graph, operational behavior, push, or source-of-truth mutation work has been performed during Phase 11.
- Known risk: focused Phase 11 tests are slow because the endpoint composes expensive existing derived-view stacks; full backend discovery is too slow under the current cap.

- Phase 12 Product Preference & Install Logic is complete and locally committed in `4900fad`.
- Added backend read-only product-preference schemas, router, service, and package files under `apps/api/app/product_preferences/` plus `apps/api/app/services/product_preferences.py`.
- Updated `apps/api/app/main.py` to include the product-preferences router under `/api`.
- Added `apps/api/tests/test_product_preferences.py` with focused coverage for route presence/handler response, deterministic output, no persistence mutation, false forbidden-scope flags, no pricing/procurement/final recommendation claims, missing-input behavior, blocker/confirmation-gate behavior, homeowner-safe and contractor-facing language separation, and provenance/source basis carry-through.
- Updated continuity and API docs in `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, `docs/API_CONTRACTS.md`, and `docs/handoffs/2026-06-05-phase-12-product-preference-install-logic-closeout.md`.
- Verification passed: `python3 -m py_compile apps/api/app/product_preferences/schemas.py apps/api/app/product_preferences/router.py apps/api/app/services/product_preferences.py apps/api/tests/test_product_preferences.py`; focused Phase 12 tests `8 tests OK` in `344.870s`; `git diff --check`.
- Broad backend discovery was not run because the focused Phase 12 suite took about 345s and prior adjacent full discovery timed out under the current cap.
- No final product recommendation, product ranking, best-option selection, pricing, live inventory, distributor quote, procurement, purchase link, payment, final BOM, final electrical design, manufacturer certification, warranty claim, CRM handoff, runtime email automation, frontend, persistence, migration, write endpoint, auth/security, permission enforcement, external service/secret change, push, `twin_id`, graph, operational behavior, or source-of-truth mutation work has been performed during Phase 12.
- Known risk: focused Phase 12 tests are slow because the endpoint composes expensive existing derived-view stacks.

- Phase 13 Post-Install Retention & CRM Handoff was implemented in the working tree and is not staged or committed.
- Added backend read-only post-install schemas, router, service, and package files under `apps/api/app/post_install/` plus `apps/api/app/services/post_install.py`.
- Added backend read-only CRM handoff schemas, router, service, and package files under `apps/api/app/crm_handoff/` plus `apps/api/app/services/crm_handoff.py`.
- Updated `apps/api/app/main.py` to include the post-install and CRM handoff routers under `/api`.
- Added `apps/api/tests/test_phase13_post_install_crm.py` with focused coverage for route presence/handler response, deterministic ordering, no persistence mutation, false forbidden-scope flags, post-install state/opportunity/lifecycle/readiness metadata, CRM handoff object boundaries, and source/provenance basis.
- Updated continuity and API docs in `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, `docs/API_CONTRACTS.md`, and `docs/handoffs/2026-06-05-phase-13-post-install-retention-crm-handoff-closeout.md`.
- Verification passed so far: `python3 -m py_compile apps/api/app/post_install/schemas.py apps/api/app/post_install/router.py apps/api/app/services/post_install.py apps/api/app/crm_handoff/schemas.py apps/api/app/crm_handoff/router.py apps/api/app/services/crm_handoff.py apps/api/app/main.py apps/api/tests/test_phase13_post_install_crm.py`; focused Phase 13 tests `6 tests OK` in `0.694s`.
- The first integration-style Phase 13 test path rebuilt expensive Phase 9-12 source stacks and was optimized to deterministic Phase 11/12 source fixtures for focused Phase 13 behavior. Broader discovery is still pending final stabilization decision.
- No external CRM integration, CRM writes, email/drip campaign product behavior, task creation, sales scoring, lead scoring, ranking, best upsell logic, push behavior, frontend, persistence, migration, write endpoint, auth/security, permission enforcement, external service/secret change, `twin_id`, graph, operational behavior, staging, commit, push, or source-of-truth mutation work has been performed during Phase 13.

- Phase 6A through Phase 6E Planning Exchange Object was implemented and locally committed in `837d3ae`.
- Added `docs/phase-6-planning-exchange-object.md`.
- Added backend read-only planning-exchange package, schemas, router, and service.
- Updated `apps/api/app/main.py` to include the planning-exchange router under `/api`.
- Updated `apps/api/tests/test_twin_planning_context.py` with focused coverage for the exchange route, Phase 5 composition, non-authoritative trust boundaries, deterministic same-input/same-output behavior, section-level source/trust mapping, and planning-review readiness summary.
- Phase 6C adds backend read-only derived `GET /api/planning-exchange/homes/{home_id}`.
- Phase 6D maps section sources/trust categories: homeowner-provided, app-derived, contractor-safe projection, manufacturer-required future, AHJ/utility-dependent future, and missing/unknown.
- Phase 6E adds readiness summary for participant review, contractor review, estimate-readiness input review, and proposal-option input review. Readiness is planning-review posture only and is not authorization, approval, verification, estimate readiness certification, proposal readiness certification, or final design readiness.
- Verification passed: `python3 -m unittest tests/test_twin_planning_context.py` with `142 tests OK`, and `python3 -m unittest discover tests` with `153 tests OK`.
- No frontend, persistence, migration, auth/security, permission enforcement, write endpoint, contractor account, marketplace, CRM, payment, pricing/proposal, final electrical sizing, final design claim, export/PDF/share link, `twin_id`, graph, operational behavior, push, or source-of-truth mutation work has been performed during Phase 6A through Phase 6E.
- Phase 6F closeout changes docs/continuity only and does not change runtime.

- Phase 5A through Phase 5E Contractor Participant Foundation was locally committed in `f616e9ac9e4d2a2b763d692a5135245d57eb6407` with commit message `feat: add contractor participant read-only foundations`.
- Final status after commit was clean, and no push was run.
- Added `docs/phase-5-contractor-participant-foundation.md`.
- Added `docs/handoffs/2026-06-04-phase-5a-contractor-participant-charter.md`.
- Added `docs/handoffs/2026-06-04-phase-5e-contractor-observation-doctrine.md`.
- Added `docs/handoffs/2026-06-04-phase-5-contractor-participant-foundation-closeout.md`.
- Added backend read-only contractor-context package, schemas, router, and service.
- Updated compact continuity in `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`.
- Phase 5A defines contractor participant role, contractor-safe visibility, read-only mutability boundary, trust/provenance boundaries, confirmation gate lifecycle, install complexity categories, future contractor observation doctrine, forbidden scope, and verification requirements.
- Phase 5B adds backend read-only derived `GET /api/contractor-context/homes/{home_id}`.
- Phase 5C adds backend read-only derived `GET /api/contractor-context/homes/{home_id}/confirmation-gates`.
- Phase 5D adds backend read-only derived `GET /api/contractor-context/homes/{home_id}/install-complexity`.
- Phase 5E documents future contractor observations as append-only participant input only; it does not implement observation intake.
- No frontend, persistence, migration, auth/security, permission enforcement, write endpoint, contractor account, marketplace, CRM, payment, pricing/proposal, final electrical sizing, export, `twin_id`, graph, operational behavior, push, or source-of-truth mutation work has been performed during Phase 5A through Phase 5E.

- Phase 4 Trust / Provenance Maturity and Readiness Normalization runtime normalization completed through approved slices 4A through 4E and is now in docs-only closeout.
- Phase 3O Phase 3 Closeout Stabilization remains the Phase 3 closeout foundation.
- Phase 3A through Phase 3N are recorded complete, and Phase 3 derived-view assembly stabilization is recorded complete.
- All Phase 3 runtime endpoints are recorded:
  - `/api/twin-planning-context/homes/{home_id}/views/dependency-impact-readiness`
  - `/api/twin-planning-context/homes/{home_id}/views/dependency-reasoning`
  - `/api/twin-planning-context/homes/{home_id}/views/planning-intelligence-readiness`
  - `/api/twin-planning-context/homes/{home_id}/views/advisory-context-assembly`
  - `/api/twin-planning-context/homes/{home_id}/views/constraint-risk-reasoning`
  - `/api/twin-planning-context/homes/{home_id}/views/scenario-comparison-readiness`
  - `/api/twin-planning-context/homes/{home_id}/views/pre-recommendation-advisory`
  - `/api/twin-planning-context/homes/{home_id}/views/recommendation-eligibility-readiness`
  - `/api/twin-planning-context/homes/{home_id}/views/basic-advisory-recommendations`
  - `/api/twin-planning-context/homes/{home_id}/views/contractor-facing-advisory`
  - `/api/twin-planning-context/homes/{home_id}/views/homeowner-facing-advisory`
  - `/api/twin-planning-context/homes/{home_id}/views/energy-goal-reasoning`
  - `/api/twin-planning-context/homes/{home_id}/views/proposal-readiness-foundation`
  - `/api/twin-planning-context/homes/{home_id}/views/product-spec-readiness`
- Phase 4A added optional `trust_provenance_readiness_summary` metadata to all 14 Phase 3 derived views.
- Phase 4B added `/api/twin-planning-context/homes/{home_id}/views/trust-provenance-readiness-index` as a read-only, request-time cross-view index over the 14 Phase 3 summaries.
- Phase 4C normalized gap categories for confidence, missing data, unsafe assumptions, limitations, and deferred boundaries.
- Phase 4D normalized source/provenance/readiness field-path metadata.
- Phase 4E hardened readiness language with advisory-only metadata boundaries and prohibited-claim absence checks.
- Latest recorded backend verification is Phase 4C through Phase 4E verification: `python3 -m unittest tests/test_twin_planning_context.py` passed with 125 tests, and `python3 -m unittest discover tests` passed with 136 tests. Git status was clean after the Phase 4C through Phase 4E runtime commit.
- Phase 4F through Phase 4H closeout changes docs/continuity only and does not rerun backend tests unless Matt separately requests it.
- No frontend, persistence, migrations, auth/security, exports, pricing, proposals, product selection, compatibility engine, scenario simulation, graph engine, `twin_id`, marketplace behavior, operational behavior, or push work was introduced by Phase 4.
- No scoring, ranking, pass/fail verdicts, approval claims, verification claims, AHJ/manual approval claims, contractor readiness claims, pricing/proposal/compatibility/export/simulation/operational claims, or permission enforcement claims were introduced.
- Product/design recommendations, recommendation ranking, best-option selection, scenario comparison execution, scenario intelligence, scenario simulation, what-if analysis, outcome calculation, calculated change analysis, option ordering, optimization, change propagation, stale-state persistence, recalculation, invalidation, final design guidance, proposal generation, contractor directives, homeowner directives, economic reasoning, utility readiness logic/reasoning, permission enforcement, auth, RBAC/ABAC, persistence, migrations, twin_id, graph engine/database, exports, operational behavior, survivability/recharge modeling, compatibility engines, utility sharing, telemetry governance, ownership transfer, registry, marketplace, and canonical Twin runtime model remain deferred.

## Earlier Change

- Phase 2C closeout assessment completed after `8e23cd8`.
- Phase 2C is now recorded as complete for the approved foundation scope.
- Completed Phase 2C foundations are Topology Snapshot Foundation, Lifecycle Readiness Foundation, and Topology Relationship Coverage Foundation.
- Remaining topology/lifecycle work is deferred: canonical topology graph, persistence, topology promotion workflows, lifecycle event logs, field verification workflows, contractor-reviewed topology, contractual topology, utility-reviewed topology, operational topology, simulation, what-if analysis, recalculation engines, and invalidation engines.
- At that point Phase 3 had not started; Phase 3A later opened only through the approved dependency impact readiness boundary in `97b57fb`.

## Earlier Change

- Added Phase 2C Topology Relationship Coverage Foundation in `d56dbd6` as additive, read-only relationship coverage metadata and safe relationship hooks on the existing topology snapshot endpoint.
- Added structure-to-premise relationships, panel/load/location-to-building relationships, design-to-pathway relationships, and pathway source/destination relationships when resolvable to concrete context nodes.
- Added `relationship_coverage_summary` and `missing_relationship_indicators`.
- Preserved conservative unresolved relationship handling: unresolved or ambiguous pathway labels remain missing coverage instead of becoming topology edges.
- Kept relationship coverage descriptive, read-only, topology-derived, and provenance-aware.
- Preserved the required boundary that there is no persistence, migrations, canonical topology table, `twin_id`, graph database, graph engine, lifecycle workflow, topology promotion engine, lifecycle event log, recalculation engine, invalidation engine, simulation, what-if analysis, Phase 3 intelligence, field-verified topology, contractor-reviewed topology, contractual topology, utility-reviewed topology, operational topology, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, or operational control.

## Earlier Change

- Added Phase 2C Lifecycle Readiness Foundation in `0d62693` as additive metadata on the existing topology snapshot endpoint.
- Added `lifecycle_readiness_summary`, `lifecycle_readiness_hints`, `deferred_lifecycle_domains`, and `missing_readiness_indicators`.
- Added `source_marker_found` traceability so missing-readiness indicators can show whether they were derived from existing topology snapshot limitation text.
- Kept readiness descriptive, read-only, topology-derived, and provenance-aware.
- Derived readiness from topology nodes, topology edges, lifecycle domains, provenance gap types, dependency awareness labels, planning dependency warnings, source document references, and limitation text.
- Preserved the required boundary that there is no persistence, migrations, canonical topology table, `twin_id`, graph database, lifecycle workflow, topology promotion engine, lifecycle event log, simulation, Phase 3 intelligence, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, or operational control.

## Earlier Change

- Added Phase 2C Topology Snapshot Foundation in `0c5bf23` as a dedicated additive endpoint derived only from existing `TwinPlanningContext` records and dependency hooks.
- Added `TwinTopologyNode`, `TwinTopologyEdge`, and `TwinTopologySnapshot`.
- Added `/api/twin-planning-context/homes/{home_id}/views/topology-snapshot`.
- Included `home_id`, scenario branch references, revision lineage references, lifecycle-domain summaries, and explicit limitations.
- Kept lifecycle labels descriptive only: `recorded_current_topology`, `sandbox_proposed_planning_topology`, `saved_scenario_revision_topology`, and `derived_advisory_topology`.
- Preserved the required boundary that there is no persistence, migrations, canonical topology table, `twin_id`, graph database, topology promotion workflow, lifecycle event log, recalculation engine, invalidation engine, simulation, Phase 3 intelligence, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, or operational control.
- Advisory pseudo-node edges remain deferred.

## Earlier Change

- Added Phase 2B Permission Foundations in `b69f3db` as explicit placeholder/readiness metadata for audience, purpose, duration, revocation-state, consent-artifact placeholder, homeowner authority preservation, view-permission alignment, and permission readiness.
- Carried permission readiness metadata through context, section, record, AI grounding, homeowner projection, contractor projection, and internal/system projection paths.
- Preserved the required boundary that `permission_not_enforced` remains true and that there are no grant IDs, active consent, authorization checks, persisted permission state, auth, RBAC/ABAC, exports, portals, utility sharing, ownership transfer, registry, marketplace, telemetry governance, operational control, or Phase 2D implementation.

## Earlier Change

- Added Phase 2B Dependency Awareness Foundations in `fd61372` as relationship-level dependency hooks over the existing `TwinPlanningContextService`.
- Added load-to-panel relationships through shared `building_id`, explicitly labeled as planning context only.
- Added equipment-to-system/design/product/location references, scenario-to-design and revision references, descriptive change-impact hints, and descriptive planning dependency warnings.
- Preserved dependency awareness across runtime, AI grounding, contractor, homeowner, and internal/system projection paths without adding a Phase 2C topology graph, recalculation engine, invalidation engine, persisted stale-state system, approval authority, migrations, or a canonical Twin table.

## Earlier Change

- Added Phase 2B runtime view foundations over the existing `TwinPlanningContextService` in `eab68fc`.
- Added minimal runtime concepts for participant role, visibility scope, view context, contributor identity, and scoped projection records.
- Added `TwinRuntimeProjectionView` as a read-only projection over the same canonical `home_id` Twin Planning Context.
- Added `/api/twin-planning-context/homes/{home_id}/views/runtime-projection/{role}` for additive role-aware projections.
- Implemented homeowner, contractor, and internal/system projection scopes without adding portals, exports, auth, permission enforcement, schema changes, migrations, utility sharing, ownership transfer, registry, marketplace, partner APIs, or Phase 3 intelligence.
- Preserved provenance summaries, source document IDs, typed provenance gaps, dependency awareness, permission-readiness metadata, and contributor/source identity where available in projection records.

## Earlier Change

- Added `docs/architecture/ResidentialEnergyTwinCanonicalArchitectureHierarchy.md` as a docs-only consolidation milestone.
- Mapped the current Residential Energy Twin doctrine stack into Strategic Doctrine, Residential Energy Twin Contract, Foundational Domains, Trust-Bearing Domains, Interpretation & Projection, Participant Boundaries, Phase 3 Intelligence, and Future Gated Layers.
- Reaffirmed that the hierarchy creates no new domains, new architecture, Exchange, Ownership & Transfer, Registry, Identity, APIs, schemas, protocols, runtime behavior, permission enforcement, utility behavior, safety approval, field verification, DERMS/dispatch, or operational control.

## Earlier Change

- Added `docs/architecture/DependencyImpactPropagation.md` as a docs-only Phase 3 architecture integrity document.
- Defined how changes to Twin facts should affect stale outputs, dependency invalidation, recalculation, re-grounding, re-review, provenance posture, confidence posture, safety context, continuity records, and participant-facing interpretations.
- Reaffirmed that Dependency Impact Propagation is not a new Twin domain and does not define runtime implementation, APIs, schemas, exchange, ownership transfer, utility submissions, safety approval, field verification, DERMS/dispatch, or operational control.

## Earlier Change

- Added `docs/architecture/EcosystemParticipantBoundaryMatrix.md` as a docs-only Residential Energy Twin doctrine consolidation document.
- Defined participant-purpose boundaries for homeowners, contractors, utilities, real estate, insurance, finance, manufacturers, and aggregators.
- Documented each participant's purpose, contributed information, consumed information, minimum necessary domains, permission requirements, provenance requirements, continuity requirements, interoperability requirements, prohibited claims, and prohibited authority assumptions.
- Reaffirmed that the matrix is not a new Twin domain and does not define exchange, ownership transfer, APIs, schemas, protocols, standards, runtime implementation, utility control, or operational control.

## Previous Change

- Added `docs/architecture/InteroperabilityDomain.md` as a docs-only Residential Energy Twin architecture/governance document.
- Defined the Interoperability Domain as shared semantic interpretation for common understanding, domain interpretation, authority semantics, lifecycle semantics, provenance semantics, permission semantics, safety semantics, continuity semantics, view semantics, and industry interpretation.
- Clarified that interoperability answers how different industries can understand the same Twin without answering how the Twin is exchanged.
- Reaffirmed that the Interoperability Domain does not approve exchange mechanisms, ownership transfer, APIs, schemas, protocols, standards, exports, integrations, runtime implementation, utility authority, compliance approval, safety certification, DERMS/dispatch, operational control, or a separate product.

## Earlier Change

- Added `docs/architecture/ContinuityDomain.md` as a docs-only Residential Energy Twin architecture/governance document.
- Defined the Continuity Domain as a foundational Twin domain for preserving lifecycle history and keeping the Twin attached to the home across ownership, contractor, utility, infrastructure, safety, permission, provenance, equipment, project, and software/platform changes.
- Documented continuity objectives, categories, lifecycle principle, historical record principle, continuity boundaries, strategic role, relationships to existing domains, and deferred continuity/history view expectations.
- Reaffirmed that the Continuity Domain records continuity information only and does not approve runtime continuity records, schemas, APIs, legal ownership, title ownership, utility authority, regulatory authority, compliance approval, operational control, contractual rights, safety certification, exports, DERMS/dispatch, or implementation scope.

## Earlier Change

- Added `docs/architecture/SafetyDomain.md` as a docs-only Residential Energy Twin architecture/governance document.
- Defined the Safety Domain as a component of the Residential Energy Twin for persistent, provenance-bearing, permissioned safety context about behind-the-meter infrastructure across property lifecycle changes.
- Documented safety record categories for energy sources, isolation systems, export capabilities, operational modes, verification status, and provenance.
- Reaffirmed that the Safety Domain does not approve runtime safety records, schemas, APIs, safety approval, field verification, inspection workflows, utility approval, exports, DERMS/dispatch, operational control, or a separate safety product.

## Earlier Change

- Updated doctrine-only strategic language for Twin-first positioning across the product vision, philosophy, agent operating principles, and compact restore state.
- Codified the Planner First Application, Twin First, Trusted Record, Safety, and Ecosystem principles without changing runtime code, schemas, APIs, permissions architecture, utility architecture, operational-control posture, or approved Phase 2A/2B/3 boundaries.
- Clarified that protocols and standards are artifacts of successful ecosystem adoption and that the repository should optimize for Twin adoption, trust, continuity, and ecosystem participation rather than protocol ownership.
- Reaffirmed that Residential Infrastructure Registry, Residential Infrastructure Network, and future trusted safety-record concepts are long-term doctrine only and not implemented runtime capabilities.

## Earlier Change

- Added `docs/architecture/WhatIfAnalysis.md` as a docs-only Phase 3 architecture planning document.
- Defined What-If Analysis as a future derived/advisory layer for evaluating modeled changes to the Residential Energy Twin across topology, lifecycle, loads, production, storage/backup, survivability, recharge likelihood, economics, product compatibility, utility readiness, permissions, provenance, confidence, and missing data.
- Documented future what-if categories, evaluation dimensions, output types, grounding requirements, permission-filtered views, missing-data behavior, lifecycle/scenario boundaries, non-goals, and Matt approval gates.
- Reaffirmed that this document does not approve runtime what-if engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, operational control, financial authority, final engineering design, or authority-of-record replacement.

## Earlier Change

- Added `docs/architecture/InfrastructureSimulation.md` as a docs-only Phase 3 architecture planning document.
- Defined Infrastructure Simulation as a future derived/advisory layer for estimating modeled Residential Energy Twin behavior across resilience, production, storage, loads, topology constraints, economic sensitivity, DER/ADR readiness, and future-state planning.
- Documented future simulation categories, grounding requirements, simulation outputs, missing-data behavior, permission-filtered simulation views, lifecycle/scenario boundaries, utility/DER/ADR readiness limits, operational-control separation, and non-goals.
- Reaffirmed that this document does not approve runtime simulation engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, operational control, financial authority, final engineering design, or authority-of-record replacement.

## Earlier Change

- Added `docs/architecture/ScenarioIntelligence.md` as a docs-only Phase 3 architecture planning document.
- Defined Scenario Intelligence as a future derived/advisory layer for comparing Residential Energy Twin scenarios using Phase 2A doctrine contracts, Phase 2B runtime foundations, topology/lifecycle states, permissions, provenance, view contracts, grounding layers, Phase 3 boundaries, and the Structured System Reasoning Graph.
- Documented future scenario categories, comparison dimensions, grounding requirements, scenario outputs, planning tradeoff language, permission-filtered scenario views, lifecycle boundaries, and non-goals.
- Reaffirmed that this document does not approve runtime scenario engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, operational control, financial authority, final engineering design, or authority-of-record replacement.

## Earlier Change

- Added `docs/architecture/StructuredSystemReasoningGraph.md` as a docs-only Phase 3 architecture planning document.
- Defined the Structured System Reasoning Graph as a future derived/advisory graph over Residential Energy Twin facts, topology, lifecycle states, products, permissions, provenance, grounding layers, constraints, and missing data.
- Documented future graph node categories, graph edge types, reasoning uses, provenance/confidence requirements, permission-filtered graph views, missing-data markers, lifecycle boundaries, utility/DER/ADR readiness limits, operational-control separation, and non-goals.
- Reaffirmed that this document does not approve runtime graph implementation, graph database adoption, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, operational control, or authority-of-record replacement.

## Earlier Change

- Added `docs/architecture/Phase3TwinIntelligenceLayer.md` as a docs-only governing Phase 3 Twin Intelligence planning document.
- Defined how Phase 3 derived/advisory intelligence consumes Phase 2A doctrine, Phase 2B runtime foundations, topology/lifecycle model, permissions, provenance, view contracts, and solar/market/product grounding layers.
- Covered Structured System Reasoning Graph, scenario intelligence, infrastructure simulation, what-if analysis, dependency and impact propagation, advisory deployment sequencing, future-state modeling, advisor traceability, deterministic reasoning exports, and non-goals.
- Reaffirmed that this document does not approve runtime implementation, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS/dispatch, operational control, or authority-of-record replacement.

## Earlier Change

- Added `docs/architecture/SolarMarketProductIntelligenceGrounding.md` as a docs-only bridge from Phase 2A doctrine and Phase 2B runtime foundations to future Phase 3 solar production, market/economic, and verified product intelligence grounding.
- Documented future PVWatts-style trusted calculator grounding, EnergySage-style market reasonableness concepts without proprietary logic or integration claims, verified product intelligence requirements, product-topology grounding, contractor value, and Phase 3 derived-intelligence support.
- Cross-linked the bridge from the canonical twin contract, topology lifecycle domains, provenance placement, view contracts, architecture overview, project state, handoff, and discovery index.
- Reaffirmed that this bridge does not approve provider integrations, spec-sheet ingestion, schemas, APIs, product catalogs, AI engineering automation, utility APIs, telemetry, DERMS/dispatch, operational control, partnership claims, verified pricing, or authority-of-record replacement.

## Earlier Change

- Added `docs/architecture/PermissionPlacement.md`, `docs/architecture/ProvenancePlacement.md`, and `docs/architecture/ViewContracts.md` as docs-only Phase 2A Twin Doctrine Foundation architecture documents.
- Permission placement now defines homeowner authority, attachment levels, audience/purpose/duration/revocation concepts, lifecycle permission differences, utility/grid-edge sharing boundaries, and future privacy-enforcement compatibility.
- Provenance placement now defines twin/domain/field/source/derived/lifecycle/view provenance attachment, source-of-truth expectations, confidence/verification posture, utility/grid-edge trust implications, and future audit/security compatibility.
- View contracts now define homeowner, contractor, engineer, utility, aggregator, supplier/manufacturer, AI advisor, and audit view boundaries with data minimization, permission-filtered visibility, provenance-preserving outputs, and no direct operational-control view.
- Reaffirmed that these docs complete Phase 2A doctrine architecture only and do not approve schema, APIs, runtime enforcement, RBAC/ABAC, encryption, telemetry governance, utility APIs, DERMS/dispatch, or operational control.

## Earlier Change

- Added `docs/architecture/TopologyLifecycleDomains.md` as a docs-only Phase 2A Twin Doctrine Foundation architecture document for topology lifecycle domains, current/proposed/scenario boundaries, future reviewed/contractual/verified/utility-facing states, and operational-control separation.
- Cross-linked the topology lifecycle domains document from lightweight discovery state and the topology lifecycle reference.
- Reaffirmed that topology implementation remains gated by explicit Matt approval before runtime topology graphs, lifecycle event logs, schema, APIs, scoped exports, permission enforcement, utility exports, DERMS/dispatch, telemetry, or operational-control behavior.

## Earlier Change

- Normalized the canonical Phase 2A Residential Energy Twin Contract v1 to `docs/architecture/ResidentialEnergyTwinContractV1.md`.
- Converted `docs/architecture/RESIDENTIAL_ENERGY_TWIN_CONTRACT_V1.md` into a compatibility pointer so the repo does not carry two competing twin contracts.
- Expanded the contract's docs-only governance coverage for aggregate identity, canonical/derived boundaries, lifecycle states, permission/provenance/utility placement, scoped view expectations, future privacy/security compatibility, future utility/grid-edge compatibility, and operational-control separation.
- Reaffirmed that implementation remains gated by explicit Matt approval before schema, migrations, APIs, runtime behavior, auth/RBAC/ABAC, permission enforcement, utility authority, operational control, or a canonical runtime `ResidentialEnergyTwin` model.

## Prior Session Change

- Added `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md` as a docs-only planning note for the first permissioned-view boundary, audience-specific visibility, default exclusions, provenance expectations, and Matt approval gates.
- Cross-linked the note from `discovery-index.md` for future trust/provenance/security routing.
- No schema changes, migrations, APIs, runtime behavior, auth, RBAC, ABAC, permission enforcement, utility authority, DERMS, dispatch, operational control, or canonical `ResidentialEnergyTwin` model were made.

## Earlier Session Change

- Added `docs/provenance/RESIDENTIAL_ENERGY_TWIN_PROVENANCE_POLICY_PLANNING.md` as a docs-only planning note for authority-bearing twin facts, field/domain/derived-output provenance, current provenance structure mapping, partial areas, and Matt approval gates.
- Cross-linked the note from the lightweight project state, discovery index, and existing provenance lineage doc.
- No schema changes, migrations, APIs, runtime behavior, permission enforcement, utility authority, operational control, or canonical `ResidentialEnergyTwin` model were made.

## Earlier Session Change

- Stabilized Residential Energy Twin governance discoverability across the architecture overview, discovery index, project state, and first-boundary planning note.
- Added only lightweight cross-links and clarified that recorded planner inputs are not a canonical Residential Energy Twin implementation.
- No schema changes, migrations, API changes, runtime behavior changes, permission enforcement, auth, utility authority, operational control, or new `ResidentialEnergyTwin` model were made.

## Initial Session Change

- Added `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md` as a docs-only planning note for the first possible Residential Energy Twin runtime boundary.
- The note recommends using `home_id` only as a temporary premise-scoped planning-context anchor if Matt later approves implementation, while reserving `twin_id` for a future approved canonical aggregate implementation.
- No schema changes, migrations, API changes, runtime behavior changes, permission enforcement, auth, or new `ResidentialEnergyTwin` model were made.
- Next safe step is doc cross-linking or a separate Matt-approved implementation design for a read-only, source-labeled twin-context boundary.

## Original Contract Change

- Added `docs/architecture/RESIDENTIAL_ENERGY_TWIN_CONTRACT_V1.md` as the original documentation/governance-only Residential Energy Twin aggregate contract. The canonical Phase 2A contract now lives at `docs/architecture/ResidentialEnergyTwinContractV1.md`, and the uppercase filename is a compatibility pointer.
- Cross-linked the contract from the lightweight discovery/project-state layer.
- Preserved existing behavior: no schema changes, migrations, runtime behavior changes, auth/permission enforcement, new canonical `ResidentialEnergyTwin` model, API contract changes, utility semantics, DERMS semantics, dispatch semantics, contractor packets, utility exports, or operational-control runtime.
- No implementation approval is implied by the contract; next implementation requires explicit Matt approval.

## Verification Performed

- Current Phase 2B runtime view foundation implementation: `python3 -m unittest tests.test_twin_planning_context` passed with 21 tests.
- Current Phase 2B runtime view foundation implementation: `python3 -m unittest discover tests` passed with 32 tests.
- Current Phase 2B runtime view foundation implementation: `git diff --check` passed.
- Current Phase 2B dependency awareness foundations implementation: `python3 -m unittest tests.test_twin_planning_context` passed with 23 tests.
- Current Phase 2B dependency awareness foundations implementation: `python3 -m unittest discover tests` passed with 34 tests.
- Current Phase 2B dependency awareness foundations implementation: `git diff --check` passed.
- Current Phase 2B permission foundations implementation: `python3 -m unittest tests.test_twin_planning_context` passed with 26 tests.
- Current Phase 2B permission foundations implementation: `python3 -m unittest discover tests` passed with 37 tests.
- Current Phase 2B permission foundations implementation: `git diff --check` passed.
- Current Phase 2C topology snapshot foundation implementation: `python3 -m unittest tests.test_twin_planning_context` passed with 30 tests.
- Current Phase 2C topology snapshot foundation implementation: `python3 -m unittest discover tests` passed with 41 tests.
- Current Phase 2C topology snapshot foundation implementation: `git diff --check` passed.
- Current Phase 2C topology snapshot foundation implementation: `git diff --cached --check` passed before commit.
- Current Phase 2C lifecycle readiness foundation implementation: `python3 -m unittest tests.test_twin_planning_context` passed with 31 tests.
- Current Phase 2C lifecycle readiness foundation implementation: `python3 -m unittest discover tests` passed with 42 tests.
- Current Phase 2C lifecycle readiness foundation implementation: `git diff --check` passed.
- Current Phase 2C lifecycle readiness foundation implementation: `git diff --cached --check` passed before commit.
- Current Phase 2C topology relationship coverage foundation implementation: `python3 -m unittest tests.test_twin_planning_context` passed with 32 tests.
- Current Phase 2C topology relationship coverage foundation implementation: `python3 -m unittest discover tests` passed with 43 tests.
- Current Phase 2C topology relationship coverage foundation implementation: `git diff --check` passed.
- Current Phase 2C topology relationship coverage foundation implementation: `git diff --cached --check` passed before commit.
- Current Phase 2B Twin Runtime Foundation closeout review: `git status --short` clean before docs-only edits; focused `python3 -m unittest tests.test_twin_planning_context` passed with 16 tests.
- Current contract normalization pass: `git diff --check` passed.
- Current Residential Energy Twin Canonical Architecture Hierarchy milestone: `git diff --check` passed.
- Current Dependency Impact Propagation milestone: `git diff --check` passed.
- Current milestone closeout: `git diff --check` passed.
- Current permissioned-view planning pass: `git diff --check` passed.
- Current provenance planning pass: `git diff --check` passed.
- Current stabilization pass: `git diff --check` passed.
- Current docs-only planning note: `git diff --check` passed.
- Previous session: `git diff --check` passed.
- No backend/frontend tests are required for the current change because this session is documentation only.

## Protections Verified

- Phase 2B Twin Runtime Foundations are read-only and additive.
- Runtime projections derive from the existing `home_id`-anchored Twin Planning Context instead of creating a second canonical model.
- Dependency Awareness Foundations are planning-context metadata only and do not create a topology graph, recalculation engine, invalidation engine, or persisted stale-state system.
- Permission Foundations are placeholder/readiness metadata only and do not create grants, active consent, authorization checks, persisted permission state, auth, RBAC/ABAC, portals, exports, utility sharing, ownership transfer, registry, marketplace, telemetry governance, operational control, or Phase 2D implementation.
- Topology Snapshot Foundation is read-only and derived from existing planning-context records and dependency hooks only. It does not create persistence, migrations, a canonical topology table, `twin_id`, graph database, topology promotion workflow, lifecycle event log, recalculation engine, invalidation engine, simulation, Phase 3 intelligence, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, or operational control.
- Lifecycle Readiness Foundation is descriptive, read-only, topology-derived, and provenance-aware metadata only. It does not create persistence, migrations, a canonical topology table, `twin_id`, graph database, lifecycle workflows, topology promotion engine, lifecycle event log, simulation, Phase 3 intelligence, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, or operational control.
- Topology Relationship Coverage Foundation is descriptive, read-only, topology-derived, and provenance-aware metadata only. It does not create persistence, migrations, a canonical topology table, `twin_id`, graph database, graph engine, lifecycle workflows, topology promotion engine, lifecycle event log, recalculation engine, invalidation engine, simulation, what-if analysis, Phase 3 intelligence, field-verified topology, contractor-reviewed topology, contractual topology, utility-reviewed topology, operational topology, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, or operational control.
- Phase 3A Derived Dependency Impact Readiness is explainable derived intelligence only. It is read-only, request-time, `home_id`-anchored, derived from existing `TwinPlanningContext` and topology snapshot outputs, deterministic for the same Twin inputs, and traceable through statement `basis` metadata.
- Phase 3B Derived Dependency Reasoning is explainable derived intelligence only. It is read-only, request-time, `home_id`-anchored, derived from existing `TwinPlanningContext`, topology snapshot, and Phase 3A dependency impact readiness outputs, deterministic for the same Twin inputs, and traceable through reasoning item `basis` metadata.
- Phase 3C Planning Intelligence Readiness is explainable derived intelligence only. It is read-only, request-time, `home_id`-anchored, derived from existing `TwinPlanningContext`, topology snapshot, Phase 3A dependency impact readiness, and Phase 3B dependency reasoning outputs, deterministic for the same Twin inputs, and traceable through readiness item `basis` metadata.
- Phase 3D Advisory Context Assembly is explainable derived intelligence only. It is read-only, request-time, `home_id`-anchored, derived from existing `TwinPlanningContext`, topology snapshot, Phase 3A dependency impact readiness, Phase 3B dependency reasoning, and Phase 3C planning intelligence readiness outputs, deterministic for the same Twin inputs, and traceable through assembly item `basis` metadata. It assembles advisory input context only and does not generate advice.
- Unresolved pathway labels remain missing coverage indicators rather than topology edges.
- Advisory pseudo-node edges remain deferred.
- Contractor projection is minimized and excludes full address fields, account scaffolding, scenario revisions, internal unknown markers, and advisory notes.
- Internal/system projection is explicitly internal governance metadata and does not imply auth, tenant isolation, audit policy, or permission enforcement.
- Existing compatibility-sensitive API contracts were not narrowed or reclassified as filtered role views.
- Residential Energy Twin Contract v1 is governance/doctrine documentation only.
- `AIDesignGroundingView` is implemented as a minimized AI/design projection; consumer, contractor, utility, export, and permission-enforced scoped views remain unimplemented.
- AI remains advisory/grounding-only and cannot create canonical facts.
- Twin Planning Context runtime does not create `twin_id`, a canonical `ResidentialEnergyTwin` model/table, migrations, permission enforcement, Exchange, Ownership & Transfer, Registry, Identity, utility-control behavior, or operational-control behavior.
- New docs preserve structured-data authority, planning-only boundaries, provenance lineage, permission-first twin boundaries, strict-client concerns, and model-agnostic restore posture.

## Remaining Risks

- Field-level data classification is not persisted or enforced.
- Provenance Expansion remains partial and gap-reporting based.
- Dependency Awareness Foundations are descriptive only; there is no Phase 2C topology graph, invalidation engine, recalculation queue, background job, or persisted stale state.
- Permission Foundations and runtime projection scopes are metadata only; there are no grants, active consent, authorization checks, persisted permission state, revocation workflow, RBAC/ABAC, auth, tenant isolation, scoped exports, portals, utility sharing, ownership transfer, registry, marketplace, telemetry governance, operational control, or Phase 2D implementation.
- Phase 2C Topology Snapshot, Lifecycle Readiness, and Relationship Coverage Foundations are descriptive/read-only only; remaining topology/lifecycle work is deferred, including canonical topology graph, persistence, topology promotion workflows, lifecycle event logs, field verification workflows, contractor-reviewed topology, contractual topology, utility-reviewed topology, operational topology, graph database, graph engine, recalculation engines, invalidation engines, simulation, what-if analysis, Phase 3 intelligence, or advisory pseudo-node edge materialization.
- Phase 3A, Phase 3B, Phase 3C, and Phase 3D do not implement broader Phase 3 capability. Scenario intelligence, impact propagation, stale-state persistence, recalculation, invalidation, simulation, what-if analysis, optimization, ranking, recommendations, economic reasoning, utility readiness, survivability/recharge modeling, compatibility engines, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, operational control, twin_id, graph database/engine, migrations, and canonical Twin runtime model remain deferred.
- Canonical Residential Energy Twin runtime identity remains deferred; `home_id` remains the only Twin Planning Context runtime anchor.
- Runtime projection foundations now exist for homeowner, contractor, and internal/system contexts, but utility, export, partner, pilot, marketplace, registry, ownership transfer, and permission-enforced scoped view models remain unimplemented.
- Existing account, role, and subscription fields remain scaffolding only.
- Broad AI context remains compatibility-oriented and labeled; `AIDesignGroundingView` is the first additive minimized AI/design projection.
- Deployment lineage is defined as a gap, not implemented.
- Orchestration readiness is documented only; no DER, utility, contractor, or operational behavior exists.
- Strict clients that reject additive fields still require contract review before consuming future scoped envelopes.
- The contract defines a future canonical aggregate boundary but does not create persistence, API, or enforcement behavior.
- The Residential Energy Twin governance/design milestone is closed as documentation only; next implementation design still requires explicit Matt approval.

## Current Resume Point

Phase 2B Twin Runtime Expression is complete and stabilized for the current approved scope: `TwinPlanningContext`, Runtime View Foundations, Dependency Awareness Foundations, and Permission Foundations. Phase 2C Topology + Lifecycle Intelligence Foundations are complete for the approved foundation scope: Topology Snapshot Foundation in `0c5bf23`, Lifecycle Readiness Foundation in `0d62693`, and Topology Relationship Coverage Foundation in `d56dbd6`. Phase 3A Derived Dependency Impact Readiness is complete in `97b57fb` at `/api/twin-planning-context/homes/{home_id}/views/dependency-impact-readiness`. Phase 3B Derived Dependency Reasoning is complete in `d56f52e` at `/api/twin-planning-context/homes/{home_id}/views/dependency-reasoning`. Phase 3C Planning Intelligence Readiness is complete in `a22042d` at `/api/twin-planning-context/homes/{home_id}/views/planning-intelligence-readiness`. Phase 3D Advisory Context Assembly is complete in `1120998` at `/api/twin-planning-context/homes/{home_id}/views/advisory-context-assembly`. Scenario intelligence, impact propagation, stale-state persistence, recalculation, invalidation, simulation, what-if analysis, optimization, ranking, recommendations, economic reasoning, utility readiness, survivability/recharge modeling, compatibility engines, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, operational control, twin_id, graph database/engine, migrations, and canonical Twin runtime model remain deferred.

## Lean Restore Prompt

```text
Load project skills before implementation.
```

## If You Resume Now

- Start from `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`.
- For Residential Energy Twin aggregate governance, load `docs/architecture/ResidentialEnergyTwinContractV1.md`.
- For Residential Energy Twin architecture hierarchy routing, load `docs/architecture/ResidentialEnergyTwinCanonicalArchitectureHierarchy.md`.
- For topology lifecycle domain governance, load `docs/architecture/TopologyLifecycleDomains.md`.
- For permission, provenance, or view-contract placement, load `docs/architecture/PermissionPlacement.md`, `docs/architecture/ProvenancePlacement.md`, and `docs/architecture/ViewContracts.md`.
- For future Phase 3 Twin Intelligence Expansion solar production, market/economic, or verified product intelligence grounding, load `docs/architecture/SolarMarketProductIntelligenceGrounding.md`.
- For future Phase 3 readiness assessment only, load `docs/architecture/Phase3TwinIntelligenceLayer.md`.
- For future Phase 3 Structured System Reasoning Graph readiness only, load `docs/architecture/StructuredSystemReasoningGraph.md`.
- For future Phase 3 Scenario Intelligence readiness only, load `docs/architecture/ScenarioIntelligence.md`.
- For future Phase 3 Infrastructure Simulation readiness only, load `docs/architecture/InfrastructureSimulation.md`.
- For future Phase 3 What-If Analysis readiness only, load `docs/architecture/WhatIfAnalysis.md`.
- For future Phase 3 Dependency Impact Propagation readiness only, load `docs/architecture/DependencyImpactPropagation.md`.
- For Phase 3D Advisory Context Assembly state, load `docs/handoffs/2026-06-03-phase-3d-advisory-context-assembly.md`, `apps/api/app/services/twin_planning_context.py`, `apps/api/app/twin_planning_context/schemas.py`, `apps/api/app/twin_planning_context/router.py`, and `apps/api/tests/test_twin_planning_context.py`.
- For Phase 3C Planning Intelligence Readiness state, load `docs/handoffs/2026-06-03-phase-3c-planning-intelligence-readiness.md`, `apps/api/app/services/twin_planning_context.py`, `apps/api/app/twin_planning_context/schemas.py`, `apps/api/app/twin_planning_context/router.py`, and `apps/api/tests/test_twin_planning_context.py`.
- For Phase 3B Derived Dependency Reasoning state, load `docs/handoffs/2026-06-03-phase-3b-dependency-reasoning.md`, `apps/api/app/services/twin_planning_context.py`, `apps/api/app/twin_planning_context/schemas.py`, `apps/api/app/twin_planning_context/router.py`, and `apps/api/tests/test_twin_planning_context.py`.
- For Phase 3A Derived Dependency Impact Readiness state, load `docs/handoffs/2026-06-03-phase-3a-dependency-impact-readiness.md`, `apps/api/app/services/twin_planning_context.py`, `apps/api/app/twin_planning_context/schemas.py`, `apps/api/app/twin_planning_context/router.py`, and `apps/api/tests/test_twin_planning_context.py`.
- For Phase 2B Twin Runtime Foundation state, load `docs/handoffs/2026-06-02-phase-2b-twin-runtime-foundations-closeout.md`, `apps/api/app/services/twin_planning_context.py`, `apps/api/app/twin_planning_context/schemas.py`, `apps/api/app/twin_planning_context/router.py`, and `apps/api/tests/test_twin_planning_context.py`.
- For Phase 2B Runtime View, Dependency Awareness, and Permission Foundations state, load `docs/handoffs/2026-06-03-phase-2b-runtime-view-foundations.md` and `docs/handoffs/2026-06-03-phase-2b-dependency-permission-foundations.md`.
- For Phase 2C closeout state, load `docs/handoffs/2026-06-03-phase-2c-foundations-closeout.md`, `docs/handoffs/2026-06-03-phase-2c-topology-snapshot-foundation.md`, `docs/handoffs/2026-06-03-phase-2c-lifecycle-readiness-foundation.md`, `docs/handoffs/2026-06-03-phase-2c-topology-relationship-coverage-foundation.md`, `apps/api/app/services/twin_planning_context.py`, `apps/api/app/twin_planning_context/schemas.py`, `apps/api/app/twin_planning_context/router.py`, and `apps/api/tests/test_twin_planning_context.py`.
- For the first Residential Energy Twin runtime-boundary design question, load `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md`.
- For Residential Energy Twin provenance policy planning, load `docs/provenance/RESIDENTIAL_ENERGY_TWIN_PROVENANCE_POLICY_PLANNING.md`.
- For Residential Energy Twin permissioned-view planning, load `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md`.
- For cognition, governance, trust, provenance, or scoped API-view work, load `.codex/project-skills/canonical-authority-discipline/SKILL.md`, `.codex/project-skills/provenance-lineage/SKILL.md`, `.codex/project-skills/continuity-governance/SKILL.md`, and the task-specific project skill.
- For runtime advisor work, continue using the existing `.codex/skills/energy-planner-*` guardrail skills.

## Latest Detailed Handoff

See `docs/handoffs/2026-06-03-phase-3d-advisory-context-assembly.md` for the latest Phase 3D Advisory Context Assembly handoff, `docs/handoffs/2026-06-03-phase-3c-planning-intelligence-readiness.md` for the Phase 3C Planning Intelligence Readiness handoff, `docs/handoffs/2026-06-03-phase-3b-dependency-reasoning.md` for the Phase 3B Derived Dependency Reasoning handoff, and `docs/handoffs/2026-06-03-phase-3a-dependency-impact-readiness.md` for the Phase 3A Derived Dependency Impact Readiness handoff. The latest detailed historical handoff is `docs/handoffs/2026-06-03-phase-3d-advisory-context-assembly.md`.
