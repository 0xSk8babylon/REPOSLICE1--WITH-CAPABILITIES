# 2026-05-24 Profile-Backed Battery Sizing

## What Changed

- Extended the resilience recommendation-profile architecture with the first internal battery sizing rule layer.
- Added planning-only battery sizing outputs for each profile:
  - backup load energy need
  - autonomy duration range
  - usable battery capacity range
  - reserve margin posture
  - future growth margin posture
  - recommended battery capacity range
- Kept the formulas internal and exposed only high-level planning outputs in the advisor UI.

## Architecture Impact

- No migration or persistence change was required.
- The change stays inside the existing advisor and recommendation service layer.
- The profile system was extended rather than redesigned.

## Trust Boundary

- Battery sizing remains a planning estimate only.
- The UI does not expose raw reserve coefficients, autonomy math internals, or engineering sizing formulas.
- Outputs remain deterministic and provenance-aware through the existing recommendation rule provenance path.

## Next Recommended Step

Add the first internal solar sizing and recovery rule layer behind the same recommendation profiles so battery and solar guidance evolve together.

## Remaining Gaps

- Solar recovery and low-solar sizing behavior are still posture-only, not numeric.
- Recommendation provenance is rule-level, but detailed field-level provenance for recommendation inputs remains partial.
- Scenario scoring is still not integrated with the new profile-backed sizing model.
