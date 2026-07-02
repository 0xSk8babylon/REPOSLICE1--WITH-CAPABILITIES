# 2026-05-24 Site-Aware Solar Adjustment

## What Changed

- Added a first deterministic site-aware adjustment stage behind the existing profile-backed solar sizing estimate.
- Preserved the existing base solar range calculation, then applied coarse planning-only adjustments for:
  - recorded roof placement posture
  - fallback shading/obstruction caution
  - coarse seasonal production region posture
  - install/pathway realism caution
- Added additive solar payload fields for:
  - base solar range before site adjustment
  - site capacity posture
  - shading/obstruction caution
  - seasonal production caution
  - install realism caution
- Extended solar inspectability metadata so the advisor can explain what adjusted the range without exposing formulas.
- Added a rule-provenance seed entry for the coarse site-aware solar adjustment layer.

## Existing Data Used

- `equipment_location.location_type`
- assigned equipment location records
- `estimated_pathway.route_difficulty`
- `estimated_pathway.visibility_level`
- linked pathway count
- missing location assignments
- `home.state`

## Honest Fallbacks

- No explicit shading model exists yet, so shading remains a default caution posture.
- No roof-area or module-fit model exists yet, so site capacity remains a coarse placement posture, not a roof-fit limit.
- No PVWatts or site-production integration exists yet, so seasonal region uses only a coarse state-based posture.

## Verification

- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`

## Exact Next Target

Deepen the solar site-aware layer with better roof-capacity and placement realism before adding inverter sizing, while keeping outputs deterministic, planning-only, and provenance-aware.
