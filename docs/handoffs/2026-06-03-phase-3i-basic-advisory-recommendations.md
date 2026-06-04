# Phase 3I Basic Advisory Recommendations

## Date

2026-06-03

## Commit

- `2f1b4bd` `feat: add basic advisory recommendations view`

## Summary

Phase 3I Basic Advisory Recommendations complete. The milestone adds a bounded, read-only, request-time prerequisite/remediation recommendation view. This is the first actual Phase 3 recommendation surface, but it is limited to basic advisory recommendations about missing data, verification, review prerequisites, permission/provenance blockers, scenario-comparison readiness blockers, and proposal-generation deferral.

The view does not recommend products, final designs, ranked options, best options, scenarios, economic paths, utility-readiness paths, proposals, directives, permission grants, exports, persistence, graph behavior, `twin_id`, or operational behavior.

## Endpoint

- `/api/twin-planning-context/homes/{home_id}/views/basic-advisory-recommendations`

## Completed

- `TwinBasicAdvisoryRecommendationsView`
- `TwinBasicAdvisoryRecommendationScope`
- `TwinBasicAdvisoryRecommendationCategory`
- `TwinBasicAdvisoryRecommendationBasis`
- `TwinBasicAdvisoryRecommendationItem`
- Additive Basic Advisory Recommendations endpoint
- Collect missing data recommendation
- Verify topology recommendation
- Verify equipment/spec information recommendation
- Request spec sheet recommendation
- Contractor review required recommendation
- Professional review required recommendation
- Cannot recommend yet because prerequisites are missing recommendation
- Permission/provenance limitations prevent broader recommendation
- Scenario comparison is not ready yet recommendation
- Proposal generation remains deferred recommendation
- Traceable basis metadata on every recommendation item
- Deterministic same-input/same-output test

## Runtime Shape

- The view is anchored by `home_id`.
- The view is read-only.
- The view is generated request-time only.
- The view derives from existing `TwinPlanningContext`, topology snapshot, Phase 3C planning intelligence readiness, Phase 3D advisory context assembly, Phase 3E constraint/risk reasoning, Phase 3F scenario comparison readiness, Phase 3G pre-recommendation advisory, and Phase 3H recommendation eligibility readiness outputs.
- The view emits prerequisite/remediation recommendations only.
- The view does not generate product recommendations, final design recommendations, ranked options, best option selection, optimization, simulation, scenario comparison, outcome calculation, proposal generation, economic reasoning, utility-readiness reasoning, contractor directives, homeowner directives, permission enforcement, exports, persistence, migrations, `twin_id`, graph behavior, or operational behavior.

## Deferred Boundaries

Product/design recommendations, recommendation ranking, best-option selection, scenario comparison execution, scenario intelligence, scenario simulation, what-if analysis, outcome calculation, calculated change analysis, option ordering, optimization, change propagation, stale-state persistence, recalculation, invalidation, final design guidance, proposal generation, contractor directives, homeowner directives, economic reasoning, utility readiness logic/reasoning, permission enforcement, auth, RBAC/ABAC, persistence, migrations, twin_id, graph database/engine, exports, operational behavior, survivability/recharge modeling, compatibility engines, utility sharing, telemetry governance, ownership transfer, registry, marketplace, and canonical Twin runtime model remain deferred.

## Verification Recorded

Verification completed before commit `2f1b4bd`:

- `python3 -m unittest tests.test_twin_planning_context` passed with 93 tests.
- `python3 -m unittest discover tests` passed with 104 tests.
- `git diff --check` passed.
- `git diff --cached --check` passed.
- Staged files were exactly the four approved backend/test files.

## Changed Files In Runtime Commit

- `apps/api/app/services/twin_planning_context.py`
- `apps/api/app/twin_planning_context/router.py`
- `apps/api/app/twin_planning_context/schemas.py`
- `apps/api/tests/test_twin_planning_context.py`

## Restore Guidance

For Phase 3I basic advisory recommendations state, load:

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/handoffs/2026-06-03-phase-3i-basic-advisory-recommendations.md`
- `apps/api/app/services/twin_planning_context.py`
- `apps/api/app/twin_planning_context/schemas.py`
- `apps/api/app/twin_planning_context/router.py`
- `apps/api/tests/test_twin_planning_context.py`

Next safe step is assessment-only for a separately approved Phase 3J Contractor-Facing Advisory Logic boundary.
