# Phase 3J Contractor-Facing Advisory Logic

## Date

2026-06-04

## Commit

- `58bd14f` `feat: add contractor facing advisory view`

## Summary

Phase 3J Contractor-Facing Advisory Logic is complete. The milestone adds a bounded, read-only, request-time contractor-facing translation view over existing Phase 3 advisory/readiness/recommendation context.

The view translates existing context into contractor-facing field-verification and install-readiness language only. It does not direct contractor action, generate proposals, generate pricing or bids, rank options, choose designs, recommend products, recommend final designs, optimize, simulate, compare scenarios, create marketplace behavior, integrate CRM workflows, enforce permissions, export data, persist state, create graph behavior, create `twin_id`, or operate devices.

## Endpoint

- `/api/twin-planning-context/homes/{home_id}/views/contractor-facing-advisory`

## Completed

- `TwinContractorFacingAdvisoryView`
- `TwinContractorFacingAdvisoryScope`
- `TwinContractorFacingAdvisoryArea`
- `TwinContractorFacingAdvisoryBasis`
- `TwinContractorFacingAdvisoryItem`
- Additive Contractor-Facing Advisory endpoint
- Contractor-visible known/unknown summary
- Field-verification needs translation
- Install-readiness signal translation
- Missing equipment/spec information translation
- Topology verification need translation
- Provenance-basis translation
- Permission-readiness metadata translation
- Professional-review boundary translation
- Phase 3I prerequisite/remediation recommendation translation
- Deferred contractor workflow boundaries
- Deterministic same-input/same-output coverage

## Runtime Shape

- The view is anchored by `home_id`.
- The view is read-only.
- The view is generated request-time only.
- The view derives from existing `TwinPlanningContext`, topology snapshot, and Phase 3C through Phase 3I readiness/advisory/recommendation context.
- Permission readiness remains metadata only and is not authorization or enforcement.
- Provenance remains basis/source context only and is not verification.
- Phase 3I recommendations remain prerequisite/remediation-only recommendations and are not design advice.
- The view preserves the stabilized Phase 3 request-time assembly path.

## Deferred Boundaries

Contractor action directives, proposal generation, pricing, bid logic, product recommendations, final design recommendations, ranked options, best-option selection, optimization, simulation, scenario comparison, marketplace behavior, CRM workflows, permission enforcement, auth, RBAC/ABAC, persistence, migrations, `twin_id`, graph database/engine, exports, operational behavior, canonical Twin runtime model, and Phase 3K implementation remain deferred.

## Verification Recorded

Verification completed before commit `58bd14f`:

- `git diff --check` passed.
- Focused Phase 3J tests passed.
- `python3 -m unittest tests.test_twin_planning_context` passed with 98 tests.
- `python3 -m unittest discover tests` passed with 109 tests.
- `git diff --cached --check` passed.
- Staged files were exactly the four approved implementation files.

## Changed Files In Runtime Commit

- `apps/api/app/services/twin_planning_context.py`
- `apps/api/app/twin_planning_context/router.py`
- `apps/api/app/twin_planning_context/schemas.py`
- `apps/api/tests/test_twin_planning_context.py`

## Restore Guidance

For Phase 3J contractor-facing advisory state, load:

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/handoffs/2026-06-04-phase-3j-contractor-facing-advisory.md`
- `apps/api/app/services/twin_planning_context.py`
- `apps/api/app/twin_planning_context/schemas.py`
- `apps/api/app/twin_planning_context/router.py`
- `apps/api/tests/test_twin_planning_context.py`

Next safe step is assessment-only for a separately approved Phase 3K Homeowner-Facing Advisory Logic boundary.
