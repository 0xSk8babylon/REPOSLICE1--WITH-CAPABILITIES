# Phase 3G Pre-Recommendation Advisory

## Date

2026-06-03

## Commit

- `5883985` `feat: add pre recommendation advisory view`

## Summary

Phase 3G Pre-Recommendation Advisory complete. The milestone adds a bounded, read-only, request-time advisory boundary view that explains what can and cannot be advised safely before recommendations are allowed. It does not generate recommendations, rank recommendations, choose a best option, optimize, simulate, compare scenarios, calculate scenario changes, produce final design guidance, generate proposals, perform economic reasoning, perform utility-readiness logic, create contractor or homeowner directives, enforce permissions, export data, persist state, create `twin_id`, create graph behavior, or operate devices.

## Endpoint

- `/api/twin-planning-context/homes/{home_id}/views/pre-recommendation-advisory`

## Completed

- `TwinPreRecommendationAdvisoryView`
- `TwinPreRecommendationAdvisoryScope`
- `TwinPreRecommendationAdvisoryArea`
- `TwinPreRecommendationAdvisoryBasis`
- `TwinPreRecommendationAdvisoryItem`
- Additive pre-recommendation advisory endpoint
- Advice-eligible area reporting for pre-recommendation explanation only
- Advice-blocked area reporting
- Missing data before advice reporting
- Unsafe assumption reporting
- Professional verification boundary reporting
- Provenance basis reporting
- Permission-readiness basis reporting
- Advisory limitation reporting
- Deferred recommendation boundary reporting
- Traceable basis metadata on every advisory item
- Deterministic derived-output test

## Runtime Shape

- The view is anchored by `home_id`.
- The view is read-only.
- The view is generated request-time only.
- The view derives from existing `TwinPlanningContext`, topology snapshot, Phase 3C planning intelligence readiness, Phase 3D advisory context assembly, Phase 3E constraint/risk reasoning, and Phase 3F scenario comparison readiness outputs.
- The view explains what can and cannot be advised safely before recommendations are allowed.
- The view does not generate recommendations, rank recommendations, choose a best option, optimize, simulate, compare scenarios, calculate scenario changes, produce final design guidance, generate proposals, perform economic reasoning, perform utility-readiness logic, create contractor or homeowner directives, enforce permissions, export data, persist state, create `twin_id`, create graph behavior, or operate devices.

## Deferred Boundaries

Recommendation generation, recommendation ranking, best-option selection, scenario comparison execution, scenario intelligence, scenario simulation, what-if analysis, calculated change analysis, option ordering, optimization, change propagation, stale-state persistence, recalculation, invalidation, final design guidance, proposal generation, contractor directives, homeowner directives, economic reasoning, utility readiness logic, permission enforcement, auth, RBAC/ABAC, persistence, migrations, twin_id, graph database/engine, exports, operational behavior, survivability/recharge modeling, compatibility engines, utility sharing, telemetry governance, ownership transfer, registry, marketplace, and canonical Twin runtime model remain deferred.

## Verification Recorded

Verification completed before commit `5883985`:

- `python3 -m unittest tests.test_twin_planning_context` passed with 78 tests.
- `python3 -m unittest discover tests` passed with 89 tests.
- `git diff --check` passed.
- `git diff --cached --check` passed.
- Staged files were exactly the four approved backend/test files.
- Final git status after commit was clean.

## Changed Files In Runtime Commit

- `apps/api/app/services/twin_planning_context.py`
- `apps/api/app/twin_planning_context/router.py`
- `apps/api/app/twin_planning_context/schemas.py`
- `apps/api/tests/test_twin_planning_context.py`

## Restore Guidance

For Phase 3G pre-recommendation advisory state, load:

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/handoffs/2026-06-03-phase-3g-pre-recommendation-advisory.md`
- `apps/api/app/services/twin_planning_context.py`
- `apps/api/app/twin_planning_context/schemas.py`
- `apps/api/app/twin_planning_context/router.py`
- `apps/api/tests/test_twin_planning_context.py`

Do not expand Phase 3 from this handoff. Broader Phase 3 work requires a separate Matt-approved implementation boundary.
