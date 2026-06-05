# Phase 7A Shared Compatibility View

## Summary

Phase 7A adds the first backend/read-only shared compatibility and install-path view.

- Runtime endpoint: `GET /api/twin-planning-context/homes/{home_id}/views/shared-compatibility`
- Status: complete in the working tree
- Commit status: not staged and not committed
- Push status: no push was run
- Focused Phase 7 verification: `5 tests`, `OK`
- Full twin planning context verification: `147 tests`, `OK`

## Scope Completed

- Backend read-only response schemas for shared compatibility scope, basis, path item, status enum, and view envelope.
- Backend read-only route under the existing `twin-planning-context` API surface.
- Service-level request-time derived classification for:
  - PV only
  - PV + battery
  - PV + battery + partial backup
  - PV + battery + whole-home backup
  - PV + generator interlock
  - PV + generator + battery
  - critical loads subpanel path
  - service upgrade likely path
  - load management path
  - existing panel reuse path
- Focused backend tests for route presence, status classification, source/basis metadata, missing information, contractor confirmation gates, trust boundaries, deterministic behavior, and absence of final-design claims.
- Compact continuity updates.

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
- `docs/handoffs/2026-06-05-phase-7a-shared-compatibility-view.md`

## Runtime Boundary

The Shared Compatibility view is:

- `home_id` anchored
- read-only
- request-time derived
- deterministic for the same inputs
- provenance-bearing
- non-authoritative
- additive only
- derived from existing `TwinPlanningContext`, topology/readiness outputs, Phase 5 contractor confirmation gates/install complexity signals, and the Phase 6 Planning Exchange Object

## Trust Boundary

The view classifies planning/install paths only. It does not produce final electrical design, final wire sizing, final conduit sizing, final breaker sizing, final disconnect/OCPD approval, permit-ready design, AHJ approval, utility approval, field verification, contractor confirmation completion, pricing, proposals, exports, permission enforcement, graph behavior, `twin_id`, or operational behavior.

## Verification

- `python3 -m unittest tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_route_is_additive_read_only_and_non_authoritative tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_classifies_required_install_paths tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_paths_preserve_basis_missing_info_and_confirmation_gates tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_preserves_final_design_boundary tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_shared_compatibility_is_deterministic_for_same_inputs` passed with `5 tests`, `OK`.
- `python3 -m unittest tests/test_twin_planning_context.py` passed with `147 tests`, `OK`.

## Recommended Next Boundary

Next safe slice: Phase 7B can harden shared compatibility basis quality, such as reducing broad missing-information noise, adding source-category summaries, or adding a compatibility summary rollup. Keep it read-only and additive.

Do not proceed next into persistence, exports/share links, auth/security enforcement, permission enforcement, frontend sharing workflows, final electrical design outputs, exact wire/conduit/breaker sizing, permit-ready design claims, AHJ/utility approval claims, scenario engine expansion, graph behavior, `twin_id`, pricing/proposals, or operational behavior without Matt approval.

