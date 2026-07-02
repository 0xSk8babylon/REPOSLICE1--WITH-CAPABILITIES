# B6 Sizers Closeout

## Summary

B6 Sizers is implemented as pure deterministic sizing primitives for battery, generator, V2H coverage, and transformer headroom.

## Runtime Files

- `apps/api/app/engines/sizers.py`
- `apps/api/tests/test_sizers.py`

## Completed Scope

- Added battery hours-to-kWh conversion including round-trip efficiency and depth-of-discharge correction.
- Added standalone and hybrid generator sizing with derate handling.
- Added V2H coverage and power-limit classification.
- Added transformer headroom status classification.
- Added assumption and confidence fields to every result.
- Added focused tests.

## Verification

- `python3 -m py_compile app/engines/sizers.py tests/test_sizers.py` passed.
- `python3 -m unittest tests/test_sizers.py` passed with `5 tests OK`.
- `python3 -m unittest tests/test_calculator_primitives.py tests/test_hourly_simulation.py tests/test_sizers.py` passed with `20 tests OK`.
- `git diff --check` passed.

## Boundary

B6 is a pure engine only. It does not add routes, persistence, migrations, frontend behavior, auth/security, permission enforcement, external utility/manufacturer lookups, pricing, SGIP, 25D, 48E, quote logic, proposal generation, product ranking, procurement, field verification, AHJ/utility approval, deployment, push, graph behavior, `twin_id`, or operational control.

## Next Action

Run B6 verification, commit the completed loop if verification passes, then continue to B7 / Phase 21.
