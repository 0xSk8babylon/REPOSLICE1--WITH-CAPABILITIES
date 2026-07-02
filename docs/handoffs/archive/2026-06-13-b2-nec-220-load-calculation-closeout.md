# B2 NEC 220 Load Calculation Closeout

## Summary

B2 NEC 220 Load Calculation is implemented under Matt's session-only NEC/calculation override for this roadmap/session. It adds an additive, deterministic, planning-only endpoint for NEC Article 220 dwelling service/load calculation support over B1 facts.

## Runtime Endpoint

- `GET /api/homes/{home_id}/load-calculations/nec-220`

## Runtime Files

- `apps/api/app/nec_load_calculation/__init__.py`
- `apps/api/app/nec_load_calculation/schemas.py`
- `apps/api/app/nec_load_calculation/router.py`
- `apps/api/app/services/nec_load_calculation.py`
- `apps/api/app/services/facts.py`
- `apps/api/app/main.py`
- `apps/api/tests/test_nec_load_calculation.py`

## Completed Scope

- Added 220.82 and 220.83 planning method results.
- Consumes B1 facts only; no raw request arguments are accepted.
- Reports stage-level VA values, service-load amps, and service headroom.
- Reports consumed facts with source, confidence, effective confidence, and derived-from IDs.
- Substitutes only labeled default assumptions for defaultable missing inputs.
- Refuses calculation and reports gaps when required inputs are missing or effectively missing.
- Propagates output confidence from consumed facts and assumptions.
- Preserves explicit planning-only, professional-review, and AHJ boundary text.

## Verification

- `python3 -m py_compile app/nec_load_calculation/schemas.py app/nec_load_calculation/router.py app/services/nec_load_calculation.py app/services/facts.py app/main.py tests/test_nec_load_calculation.py` passed.
- `python3 -m unittest tests/test_nec_load_calculation.py` passed with `6 tests OK`.
- `python3 -m unittest tests/test_facts.py tests/test_nec_load_calculation.py` passed with `14 tests OK`.
- `python3 -m unittest tests/test_nec_load_calculation.py tests/test_system_visibility.py` passed with `15 tests OK`.
- `git diff --check` passed.

## Boundary

B2 does not add migrations, auth/security changes, permission enforcement, frontend behavior, external services, dependency installs, lockfile rewrites, GitHub Actions changes, secrets, deletion, billing, production deployment, push behavior, pricing, proposal generation, field verification, stamped engineering approval, permit-ready design, AHJ approval, utility approval, `twin_id`, graph engine behavior, or operational control.

The endpoint is not a substitute for the NEC text, local amendments, electrician or engineer review, AHJ interpretation, manufacturer instructions, site conditions, or utility review.

## Remaining Risks

- The implementation is a planning-grade NEC Article 220 method support surface and must be reviewed before being treated as authoritative.
- Local amendments and jurisdiction-specific interpretations are not modeled.
- Existing local SQLite databases rely on app startup table creation for the B1 `facts` table because migrations remain a hard stop.

## Next Action

Run B2 verification, commit the completed loop if verification passes, then continue to B4 Calculator Primitives if no hard stop appears.
