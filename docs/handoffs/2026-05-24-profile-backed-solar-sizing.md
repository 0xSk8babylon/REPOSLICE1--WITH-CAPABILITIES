# 2026-05-24 Profile-Backed Solar Sizing

## What Changed

- Extended the resilience recommendation-profile architecture with the first internal solar sizing and recovery rule layer.
- Added planning-only solar sizing outputs for each profile:
  - solar production posture
  - low-solar condition posture
  - recovery strength
  - seasonal conservatism
  - recommended solar capacity range
  - battery-recovery relationship guidance
- Kept the formulas internal and exposed only high-level planning outputs in the advisor UI.

## Architecture Impact

- No migration or persistence change was required.
- The change stays inside the existing recommendation service and advisor payload.
- The profile system and battery sizing slice were extended rather than redesigned.

## Trust Boundary

- Solar sizing remains a planning estimate only.
- The UI does not expose raw production coefficients, recharge-credit math, or engineering formulas.
- Outputs remain deterministic and provenance-aware through the existing recommendation rule provenance path.

## Next Recommended Step

Expand provenance coverage around recommendation inputs and resulting battery/solar guidance so users can inspect what current planning assumptions are driving profile fit.

## Remaining Gaps

- Recommendation inputs still rely on partial field-level provenance.
- Seasonal and site-condition modeling are still high-level posture, not deeper site-aware planning logic.
- Scenario scoring is still not integrated with the profile-backed sizing model.
