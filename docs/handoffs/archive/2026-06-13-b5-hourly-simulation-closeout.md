# B5 8760 Hourly Simulation Closeout

## Summary

B5 Hourly Simulation is implemented as a pure deterministic engine for hourly solar, load, battery, grid import/export, bill, cycle-count, and outage-coverage modeling.

## Runtime Files

- `apps/api/app/engines/hourly_simulation.py`
- `apps/api/tests/test_hourly_simulation.py`

## Completed Scope

- Added hourly load/solar netting.
- Added battery charge/discharge within power and SoC limits.
- Added grid import/export tracking.
- Added flat, TOU, and tiered rate bill calculations.
- Added bill-without-system delta, self-consumption, annual import/export, peak import/export, cycles/year, and backup coverage.
- Added confidence carry-through from input confidence tiers.
- Added tests for energy conservation, flat/TOU/tiered rates, backup partial-hour coverage, and invalid inputs.

## Verification

- `python3 -m py_compile app/engines/hourly_simulation.py tests/test_hourly_simulation.py` passed.
- `python3 -m unittest tests/test_hourly_simulation.py` passed with `5 tests OK`.
- `python3 -m unittest tests/test_calculator_primitives.py tests/test_hourly_simulation.py` passed with `15 tests OK`.
- `git diff --check` passed.

## Boundary

B5 is a pure engine only. It does not add persistence, migrations, routes, frontend behavior, auth/security changes, permission enforcement, external utility/rate lookup, dependency installs, lockfile rewrites, real tariffs, customer billing, proposal generation, deployment, push, `twin_id`, graph behavior, or operational control.

Bill outputs are calculation results from caller-provided rate inputs only, not utility billing authority, savings guarantees, eligibility, tariff advice, or financial recommendation.

## Next Action

Run B5 verification, commit the completed loop if verification passes, then continue to Phase 20 Geometry.
