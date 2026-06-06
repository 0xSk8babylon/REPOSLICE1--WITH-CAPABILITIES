# Phase 15 Program Intelligence & Grid Edge Readiness Closeout

## Summary

Phase 15 is implemented in the working tree as `GET /api/program-intelligence/homes/{home_id}`.

The endpoint is additive, read-only, request-time derived, deterministic for the same inputs, `home_id` anchored, non-authoritative, and provenance-bearing. It derives program/grid-edge awareness context from existing `TwinPlanningContext` records only.

## Runtime Endpoint

- `GET /api/program-intelligence/homes/{home_id}`

## Runtime Files

- `apps/api/app/program_intelligence/__init__.py`
- `apps/api/app/program_intelligence/schemas.py`
- `apps/api/app/program_intelligence/router.py`
- `apps/api/app/services/program_intelligence.py`
- `apps/api/app/main.py`
- `apps/api/tests/test_program_intelligence.py`

## Completed Scope

- Defined Phase 15 schemas and router structure.
- Added explicit boundary and hard-stop capability flags.
- Added deterministic request-time service logic over existing `TwinPlanningContext` records.
- Added program awareness summaries for utility context, program categories, incentives/rebates, demand response, VPP, TOU, and interconnection.
- Added informational grid-edge readiness indicators for battery participation, load shifting, backup planning, smart panel, EV coordination, and DER aggregation.
- Added missing-input degradation for utility, rate plan, battery configuration, export status, interconnection status, equipment compatibility, and program jurisdiction unknowns.
- Added blockers, confirmation gates, assumptions, dependencies, homeowner-safe summaries, contractor/program review prompts, verification recommendations, do-not-assume statements, and source/provenance basis metadata.
- Added focused Phase 15 tests.
- Updated continuity and API docs.

## Verification

- `python3 -m py_compile app/program_intelligence/schemas.py app/program_intelligence/router.py app/services/program_intelligence.py app/main.py tests/test_program_intelligence.py`
- `python3 -m unittest tests/test_program_intelligence.py` passed with `6 tests OK`.
- `git diff --check` passed.

## Boundary

Phase 15 does not add persistence, migrations, writes, background jobs, external API calls, auth/security changes, permission enforcement, enrollment workflows, rebate calculations, incentive calculations, tariff optimization, utility dispatch, device control, demand response execution, grid-services execution, billing logic, pricing logic, proposal generation, CRM integration, email automation, exports, pushes, deployment, `twin_id`, graph behavior, or source-of-truth mutation.

The endpoint does not determine program qualification, confirm program availability, validate incentives, approve interconnection, approve export, authorize grid participation, operate devices, dispatch loads, or create utility/aggregator authority.

## Remaining Risks

- Current runtime source basis is limited to existing structured planning records and does not call utility, tariff, rebate, aggregator, manufacturer, or interconnection sources.
- Program and rate terms may be stale or absent until source-backed records exist.
- Equipment/program compatibility remains review metadata only.
- Permission foundations remain readiness metadata only; no consent, authorization, export, RBAC/ABAC, or permission enforcement exists.

## Resume Notes

- Start with `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`.
- For Phase 15 work, load this handoff plus:
  - `apps/api/app/program_intelligence/schemas.py`
  - `apps/api/app/program_intelligence/router.py`
  - `apps/api/app/services/program_intelligence.py`
  - `apps/api/tests/test_program_intelligence.py`
  - `docs/API_CONTRACTS.md`

## Next Action

Wait for Matt's explicit approval before committing.
