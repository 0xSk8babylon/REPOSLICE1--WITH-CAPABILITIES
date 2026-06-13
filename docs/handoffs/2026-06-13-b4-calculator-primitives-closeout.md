# B4 Calculator Primitives Closeout

## Summary

B4 Calculator Primitives is implemented as a pure-function backend math library. It adds deterministic primitives for backfeed planning, supply-side tap review metadata, coupling direction, critical-load identification, tier-1 shading derate, and solar production estimation.

## Runtime Files

- `apps/api/app/engines/calculator_primitives.py`
- `apps/api/tests/test_calculator_primitives.py`

## Completed Scope

- Added 120% backfeed planning calculation with pass/fail and supply-side alternative flag.
- Added supply-side tap planning review metadata.
- Added AC/DC/hybrid coupling direction primitive.
- Added critical-load selection and peak/continuous draw primitive.
- Added tier-1 horizon-trace shading derate primitive.
- Added solar production estimator with simplified internal model or injected PVWatts-style estimator.
- Added tests for normal cases, boundary cases, and failure/alternative paths.

## Verification

- `python3 -m py_compile app/engines/calculator_primitives.py tests/test_calculator_primitives.py` passed.
- `python3 -m unittest tests/test_calculator_primitives.py` passed with `10 tests OK`.
- `python3 -m unittest tests/test_facts.py tests/test_nec_load_calculation.py tests/test_calculator_primitives.py` passed with `24 tests OK`.
- `git diff --check` passed.

## Boundary

B4 does not add database access, persistence, migrations, routes, frontend behavior, auth/security changes, permission enforcement, external services, dependency installs, lockfile rewrites, network calls, pricing, proposal generation, field verification, AHJ/utility approval, deployment, push, graph engine behavior, `twin_id`, or operational control.

The primitives are planning calculations only and must be consumed by higher-level services with explicit trust/provenance boundaries.

## Remaining Risks

- Supply-side tap and coupling outputs are review metadata, not design approval.
- Tier-1 shading derate is intentionally coarse and does not replace measured geometry, irradiance modeling, or professional site assessment.
- The optional PVWatts path is injection-only; no client or external API call exists.

## Next Action

Run B4 verification, commit the completed loop if verification passes, then continue to B5 if no hard stop appears.
