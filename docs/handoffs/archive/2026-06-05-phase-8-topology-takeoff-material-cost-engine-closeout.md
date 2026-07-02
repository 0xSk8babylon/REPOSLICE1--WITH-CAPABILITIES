# Phase 8 Topology Takeoff Material Cost Engine Closeout

## Summary

Phase 8 Topology Takeoff & Material Cost Engine is complete in the working tree and not yet staged or committed.

- Runtime endpoint: `GET /api/twin-planning-context/homes/{home_id}/views/topology-takeoff`
- Commit status: not staged and not committed
- Push status: no push was run
- Focused Phase 8 verification: `7 tests`, `OK`
- Focused Phase 7 regression verification: `6 tests`, `OK`
- Full twin planning context verification: `155 tests`, `OK`

## Scope Completed

- Backend read-only response schemas for planning-grade topology takeoff scope, basis, quantity basis, cost basis, line items, summary, and view envelope.
- Backend read-only route under the existing `twin-planning-context` API surface.
- Service-level request-time derivation from existing `TwinPlanningContext`, topology snapshot, Phase 7 shared compatibility, Phase 5 contractor confirmation gates/install complexity signals, and the Phase 6 Planning Exchange Object.
- Planning-grade material/scope categories where supported by current topology context:
  - PV source circuit / array-side scope
  - inverter / microinverter / power electronics scope
  - battery / ESS scope
  - backup interface / gateway / transfer equipment scope
  - generator integration scope
  - panel / subpanel / load center scope
  - conduit / raceway pathway scope
  - conductor / circuit placeholder scope
  - disconnect / OCPD placeholder scope
  - monitoring / communications scope
  - labeling / signage placeholder scope
  - grounding / bonding placeholder scope
  - trenching / routing / structural / mounting scope
- Line-level basis/provenance, basis quality, quantity-basis posture, cost-basis-unavailable metadata, uncertainty, missing information, blockers, required confirmations, and contractor confirmation gates.
- Homeowner-safe and contractor-facing interpretation metadata on the same backend object.
- Focused backend tests and relevant Phase 7 regression tests.
- Compact continuity, API contract, and handoff updates.

## Runtime Files Changed

- `apps/api/app/twin_planning_context/schemas.py`
- `apps/api/app/twin_planning_context/router.py`
- `apps/api/app/services/twin_planning_context.py`
- `apps/api/tests/test_twin_planning_context.py`

## Continuity / Docs Files Changed

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/API_CONTRACTS.md`
- `docs/handoffs/2026-06-05-phase-7-shared-compatibility-install-path-view-closeout.md`
- `docs/handoffs/2026-06-05-phase-8-topology-takeoff-material-cost-engine-closeout.md`
- `PHASE_8_FINAL_REPORT.txt`
- `docs/handoffs/PHASE_8_FINAL_REPORT.txt`

## Runtime Boundary

The topology takeoff view is:

- `home_id` anchored
- read-only
- request-time derived
- deterministic for the same inputs
- provenance-bearing
- non-authoritative
- additive only
- derived from existing planning/twin/topology context and already-approved read-only derived views

## Response Contents

The endpoint returns:

- `home_id`
- `view_name`
- `generated_at`
- `permission_scope`
- `takeoff_scope`
- `topology_basis` / `provenance_basis`
- `takeoff_summary`
- `line_items`
- `missing_information`
- `blockers`
- `uncertainty`
- `required_confirmations`
- `contractor_confirmation_gates`
- `cost_basis`
- `homeowner_interpretation`
- `contractor_interpretation`
- assumptions, limitations, and deferred boundaries

Each line item includes category, label, reason, basis/provenance, quantity basis, cost basis, uncertainty, missing information, blockers, required confirmations, contractor confirmation gates, homeowner-safe interpretation, contractor-facing interpretation, assumptions, and limitations.

## Trust Boundary

The view identifies planning-grade material/scope categories only. It does not produce a final contractor estimate, final bill of materials, contractor-approved BOM, final engineered design, NEC/code-compliant material list, permit-ready design, AHJ approval, utility approval, field verification, exact wire sizing, exact conduit sizing, exact breaker sizing, final disconnect/OCPD approval, pricing, proposals, exports, permission enforcement, graph behavior, `twin_id`, or operational behavior.

Cost basis defaults to unavailable / requires contractor pricing. Existing placeholder cost fields are not reused as contractor pricing or final estimate totals.

Homeowner and contractor interpretation fields are metadata only. They are not auth, sharing, exports, role enforcement, permission grants, consent artifacts, portals, or scoped external views.

## Verification

- `python3 -m unittest tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_topology_takeoff_route_is_additive_read_only_and_non_authoritative tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_topology_takeoff_derives_material_scope_categories_from_topology tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_topology_takeoff_line_items_preserve_basis_quality_and_provenance tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_topology_takeoff_surfaces_missing_information_blockers_and_confirmations tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_topology_takeoff_preserves_homeowner_and_contractor_interpretation_boundaries tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_topology_takeoff_preserves_final_estimate_and_design_boundary tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_topology_takeoff_is_deterministic_for_same_inputs` passed with `7 tests`, `OK`.
- `python3 -m unittest tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_route_is_additive_read_only_and_non_authoritative tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_classifies_required_install_paths tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_paths_preserve_basis_missing_info_and_confirmation_gates tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_missing_info_and_gates_remain_review_requirements tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_preserves_final_design_boundary tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_is_deterministic_for_same_inputs` passed with `6 tests`, `OK`.
- `python3 -m unittest tests/test_twin_planning_context.py` passed with `155 tests`, `OK`.

## Recommended Next Boundary

Do not start Phase 9 without Matt approval.

Next safe owner-controlled action is review, then optional local commit if Matt says `approve commit`.

Recommended commit message:

`feat: add topology takeoff material cost view`
