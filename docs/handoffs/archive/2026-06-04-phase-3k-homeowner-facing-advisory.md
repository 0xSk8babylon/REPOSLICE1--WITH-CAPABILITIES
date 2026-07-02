# Phase 3K Homeowner-Facing Advisory Logic

## Date

2026-06-04

## Commit

- `5814c18` `feat: add homeowner facing advisory view`

## Summary

Phase 3K Homeowner-Facing Advisory Logic is complete. The milestone adds a bounded, read-only, request-time homeowner-facing translation view over existing Phase 3 advisory/readiness/recommendation context.

The view translates existing context into homeowner-safe explanation language only. It does not direct homeowner action, generate final design guidance, recommend products or specific equipment, rank options, choose designs, compare scenarios, simulate outcomes, calculate savings or payback, generate proposals, create sales claims, create contractor directives, enforce permissions, export data, persist state, create graph behavior, create `twin_id`, or operate devices.

## Endpoint

- `/api/twin-planning-context/homes/{home_id}/views/homeowner-facing-advisory`

## Completed

- `TwinHomeownerFacingAdvisoryView`
- `TwinHomeownerFacingAdvisoryScope`
- `TwinHomeownerFacingAdvisoryArea`
- `TwinHomeownerFacingAdvisoryBasis`
- `TwinHomeownerFacingAdvisoryItem`
- Additive Homeowner-Facing Advisory endpoint
- Homeowner-visible known/unknown summary
- Safe context explanation
- Missing-information translation
- Questions-to-ask-contractor translation as conversation prompts only
- Professional-review boundary translation
- Plain-language provenance-basis translation
- Permission-readiness metadata translation
- Phase 3I prerequisite/remediation recommendation translation
- Deferred homeowner workflow boundaries
- Deterministic same-input/same-output coverage

## Runtime Shape

- The view is anchored by `home_id`.
- The view is read-only.
- The view is generated request-time only.
- The view derives from existing `TwinPlanningContext`, topology snapshot, and Phase 3C through Phase 3I readiness/advisory/recommendation context.
- Permission readiness remains visibility/readiness metadata only and is not authorization or enforcement.
- Provenance remains basis/source context only and is not verification.
- Phase 3I recommendations remain prerequisite/remediation-only recommendations and are not design advice.
- Questions to ask a contractor are conversation prompts only and are not homeowner instructions or contractor directives.
- The view preserves the stabilized Phase 3 request-time assembly path.

## Deferred Boundaries

Homeowner action directives, final design guidance, product recommendations, specific equipment recommendations, ranked options, best-option selection, scenario comparison, simulation, savings/payback, proposal generation, sales claims, contractor directives, permission enforcement, auth, RBAC/ABAC, persistence, migrations, `twin_id`, graph database/engine, exports, operational behavior, canonical Twin runtime model, and any next Phase 3 implementation remain deferred.

## Verification Recorded

Verification completed before commit `5814c18`:

- `python3 -m py_compile apps/api/app/twin_planning_context/schemas.py apps/api/app/twin_planning_context/router.py apps/api/app/services/twin_planning_context.py apps/api/tests/test_twin_planning_context.py` passed.
- Focused Phase 3K smoke tests passed with 5 tests.
- `git diff --check` passed.
- `python3 -m unittest tests.test_twin_planning_context` passed with 103 tests.
- `python3 -m unittest discover tests` passed with 114 tests.
- `git diff --cached --check` passed.
- Staged files were exactly the four approved implementation files.

## Changed Files In Runtime Commit

- `apps/api/app/services/twin_planning_context.py`
- `apps/api/app/twin_planning_context/router.py`
- `apps/api/app/twin_planning_context/schemas.py`
- `apps/api/tests/test_twin_planning_context.py`

## Restore Guidance

For Phase 3K homeowner-facing advisory state, load:

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/handoffs/2026-06-04-phase-3k-homeowner-facing-advisory.md`
- `apps/api/app/services/twin_planning_context.py`
- `apps/api/app/twin_planning_context/schemas.py`
- `apps/api/app/twin_planning_context/router.py`
- `apps/api/tests/test_twin_planning_context.py`

Next safe step is assessment-only for a separately approved next Phase 3 boundary.
