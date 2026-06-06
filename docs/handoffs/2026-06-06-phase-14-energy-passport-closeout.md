# Phase 14 Energy Passport Closeout

## Summary

Phase 14 adds `GET /api/energy-passport/homes/{home_id}` as an additive read-only, request-time, deterministic, provenance-bearing, non-authoritative, `home_id`-anchored Energy Passport summary.

## Scope

- Backend schemas, router, service, and route registration.
- Focused backend tests.
- Continuity and API contract docs.
- Completion and final stabilization session-report emails.

## Endpoint

- `GET /api/energy-passport/homes/{home_id}`

## Source / Provenance Basis

The view composes existing Phase 6 through Phase 13 source surfaces where available:

- `TwinPlanningContext`
- `PlanningExchangeObject`
- `ContractorWorkflowReadinessView`
- `ProductPreferencesView`
- `PostInstallView`
- `CRMHandoffView`

Every derived section carries request-time source/provenance basis metadata, missing-input refs, assumptions, limitations, and deferred boundaries.

## Runtime Boundary

The endpoint is read-only, additive, request-time derived, deterministic for the same inputs, `home_id` anchored, homeowner-safe, contractor-summary aware, provenance-bearing, and non-authoritative.

## Non-Goals

Phase 14 does not add persistence, migrations, write endpoints, auth/security changes, permission enforcement, external integrations, CRM writes, MLS/title/escrow/deed/legal transfer logic, warranty validation, permit validation, payoff calculation, lien/title/UCC search, appraisal, underwriting, tax-credit or financial conclusions, deploy, push, `twin_id`, graph behavior, operational behavior, frontend behavior, exports, or source-of-truth mutation.

## Transfer / Ownership Boundary

System financial obligations are review metadata only. Ownership status and financing structure remain `needs_confirmation` unless future source-backed records exist. Unknown or needs-confirmation ownership/financing inputs degrade transfer readiness. Transfer readiness is not legal advice, title review, escrow instruction, payoff calculation, underwriting, appraisal, tax advice, financial advice, contract validation, warranty validation, permit validation, lien search, UCC search, or deed review.

## Changed Files

- `apps/api/app/energy_passport/__init__.py`
- `apps/api/app/energy_passport/schemas.py`
- `apps/api/app/energy_passport/router.py`
- `apps/api/app/services/energy_passport.py`
- `apps/api/app/main.py`
- `apps/api/tests/test_energy_passport.py`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/API_CONTRACTS.md`
- `docs/handoffs/2026-06-06-phase-14-energy-passport-closeout.md`

## Verification

- `python3 -m py_compile apps/api/app/energy_passport/schemas.py apps/api/app/energy_passport/router.py apps/api/app/services/energy_passport.py apps/api/app/main.py` - passed.
- `PYTHONPATH=apps/api python3 -c "from app.energy_passport.schemas import EnergyPassportView; from app.energy_passport.router import router; from app.services.energy_passport import energy_passport_service; from app.main import app; print('energy_passport_import_ok')"` - passed.
- `python3 -m py_compile apps/api/app/energy_passport/schemas.py apps/api/app/energy_passport/router.py apps/api/app/services/energy_passport.py apps/api/app/main.py apps/api/tests/test_energy_passport.py` - passed.
- `PYTHONPATH=apps/api python3 -m unittest apps/api/tests/test_energy_passport.py` - passed with 7 tests.
- `PYTHONPATH=apps/api python3 -m unittest apps/api/tests/test_phase13_post_install_crm.py apps/api/tests/test_energy_passport.py` - passed with 13 tests.
- `git diff --check` - passed.

Broader backend discovery was not run because adjacent lower-phase derived-view suites are known to be slow and previously exceeded practical session caps; the adjacent Phase 13 regression was run instead.

## Email

Completion and stabilized closeout emails were requested for this phase. Delivery status is recorded in the final assistant response.

## Git / Push

No staging, commit, deploy, or push was performed.

## Next Action

Matt should review the Phase 14 working-tree changes and decide whether to approve a local commit.
