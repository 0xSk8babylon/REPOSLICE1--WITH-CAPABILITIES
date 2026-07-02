# Phase 3 Derived View Assembly Stabilization

## Date

2026-06-04

## Commit

- `f1fbc7b` `fix: reuse derived planning view assembly inputs`

## Summary

Phase 3 derived-view assembly stabilization is complete. This was an internal service-layer runtime-performance stabilization for the already-complete Phase 3A through Phase 3I derived views.

The stabilization reuses already-built request-time `TwinPlanningContext`, topology snapshot, and Phase 3A through Phase 3I derived view objects inside a single `TwinPlanningContextService` builder chain. It does not create a new endpoint, schema, router behavior, persistence behavior, response shape, frontend flow, auth behavior, permission enforcement, export, graph engine, `twin_id`, operational behavior, or Phase 3J implementation.

## Root Cause

Phase 3I Basic Advisory Recommendations recursively rebuilt Phase 3C through Phase 3H and earlier Phase 3 views during derived-view assembly. The deterministic same-input/same-output test called the Phase 3I builder twice, amplifying the recursive rebuilding into CPU-bound focused unittest runs.

## Fix Boundary

- Internal service-layer stabilization only.
- Public builder entry points still support the existing `db, home_id` call pattern.
- Existing endpoints and response payloads remain unchanged.
- Derived views remain read-only, request-time, `home_id`-anchored, deterministic for the same inputs, and traceable through basis metadata.
- Phase 3I remains limited to prerequisite/remediation recommendations.
- Phase 3J Contractor-Facing Advisory Logic remains unimplemented and assessment-only until separately approved by Matt.

## Verification Recorded

Verification completed before commit `f1fbc7b`:

- `git diff --check` passed.
- Focused problematic test passed:
  - `python3 -m unittest -v tests.test_twin_planning_context.TwinPlanningContextServiceTests.test_basic_advisory_recommendations_is_deterministic_for_same_inputs`
  - `1 test in 2.099s`
  - `elapsed=0:03.37`
- `python3 -m unittest tests.test_twin_planning_context` passed with 93 tests.
- `python3 -m unittest discover tests` passed with 104 tests.
- `git diff --cached --check` passed.
- Final git status was clean before the continuity-only documentation update.

## Changed Files In Runtime Commit

- `apps/api/app/services/twin_planning_context.py`

## Deferred Boundaries

Product/design recommendations, recommendation ranking, best-option selection, scenario comparison execution, scenario intelligence, scenario simulation, what-if analysis, outcome calculation, calculated change analysis, option ordering, optimization, change propagation, stale-state persistence, recalculation, invalidation, final design guidance, proposal generation, contractor directives, homeowner directives, economic reasoning, utility readiness logic/reasoning, permission enforcement, auth, RBAC/ABAC, persistence, migrations, `twin_id`, graph engine/database, exports, operational behavior, survivability/recharge modeling, compatibility engines, utility sharing, telemetry governance, ownership transfer, registry, marketplace, canonical Twin runtime model, and Phase 3J implementation remain deferred.

## Restore Guidance

For Phase 3 derived-view assembly stabilization state, load:

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/handoffs/2026-06-04-phase-3-derived-view-assembly-stabilization.md`
- `apps/api/app/services/twin_planning_context.py`
- `apps/api/tests/test_twin_planning_context.py`

Next safe step remains assessment-only for a separately approved Phase 3J Contractor-Facing Advisory Logic boundary.
