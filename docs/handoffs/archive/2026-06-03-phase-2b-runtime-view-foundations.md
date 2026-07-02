# Phase 2B Runtime View Foundations

## Date

2026-06-03

## Summary

Added additive role-aware and scope-aware runtime projection foundations over the existing `home_id`-anchored Twin Planning Context.

The implementation keeps one canonical runtime source: `TwinPlanningContextService.build(home_id)`. Projections are read-only views over that context and do not create a separate Twin model, portal, product codebase, export package, permission grant, ownership workflow, registry, marketplace, partner API, utility sharing surface, or Phase 3 intelligence layer.

## Implemented

- Added minimal runtime concepts:
  - `TwinRuntimeParticipantRole`
  - `TwinRuntimeVisibilityScope`
  - `TwinRuntimeParticipant`
  - `TwinRuntimeViewContext`
  - `TwinRuntimeContributionIdentity`
  - `TwinRuntimeProjectionRecord`
  - `TwinRuntimeProjectionView`
- Added `TwinPlanningContextService.build_runtime_projection_view(db, home_id, role)`.
- Added `/api/twin-planning-context/homes/{home_id}/views/runtime-projection/{role}`.
- Added homeowner, contractor, and internal/system projection behavior.
- Preserved provenance summaries, source document IDs, typed provenance gaps, dependency hooks, dependency awareness, permission-readiness metadata, limitations, and contributor/source identity where available.
- Added tests proving the same `home_001` canonical context yields different homeowner, contractor, and internal/system projections.

## Runtime Boundaries

- No `twin_id`.
- No canonical `ResidentialEnergyTwin` model or table.
- No migrations.
- No schema redesign.
- No permission enforcement.
- No grants, consent artifacts, revocation workflow, RBAC/ABAC, auth, tenant isolation, or scoped exports.
- No full homeowner portal.
- No full contractor portal.
- No utility sharing.
- No ownership transfer.
- No registry.
- No marketplace.
- No external partner APIs.
- No operational control.
- No Phase 3 intelligence implementation.

## Verification

- `python3 -m unittest tests.test_twin_planning_context` passed with 21 tests.
- `python3 -m unittest discover tests` passed with 32 tests.
- `git diff --check` passed.

## Risks And Follow-Up Boundaries

- Runtime projection scopes are descriptive/minimizing contract foundations only; they are not authorization or enforcement.
- Contractor projection is minimized but still not a contractor packet, bid, stamped design, procurement artifact, or export.
- Internal/system projection includes governance context but does not imply auth, audit policy, tenant isolation, or operational authority.
- Pilot and partner roles exist as domain concepts, but no pilot or partner API behavior is implemented.
- Utility-facing, export, permission-enforced, registry, marketplace, ownership-transfer, and operational-control behavior remain deferred.

## Resume Guidance

For this slice, load:

- `apps/api/app/twin_planning_context/schemas.py`
- `apps/api/app/services/twin_planning_context.py`
- `apps/api/app/twin_planning_context/router.py`
- `apps/api/tests/test_twin_planning_context.py`

Next safe step remains either a separately approved permission-enforcement planning milestone or a Matt-approved Phase 3 advisory/derived implementation plan grounded in the completed Twin Planning Context runtime and projection foundations.
