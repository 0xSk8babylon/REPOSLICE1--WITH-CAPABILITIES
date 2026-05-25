# 2026-05-24 Roof Geometry Readiness Layer

## What Changed

- Added a roof-readiness layer to the existing profile-backed solar guidance architecture.
- Solar guidance now explicitly distinguishes:
  - inferred placement realism
  - estimated roof-capacity posture
  - measured roof-geometry availability
  - future usable-roof-area support
- Added additive solar payload fields for:
  - roof data completeness
  - roof measurement confidence
  - measured vs estimated geometry status
  - usable roof area status
  - future geometry source placeholders
  - missing geometry warning
- Kept solar sizing deterministic and planning-only. No true roof area, traced geometry, roof planes, GIS, maps, lidar, PVWatts, or inverter sizing were added.

## Architecture Intent

- The current recommendation system remains the decision layer.
- Future GIS/maps/traced-geometry inputs should plug into `roof_geometry_readiness` and future roof-capacity estimation stages.
- Future production modeling should refine solar guidance inputs rather than replace profile selection, battery sizing, or the current solar planning pipeline.

## Verification

- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`

## Exact Next Target

Deepen the roof-readiness layer with better internal roof-capacity and placement realism inputs, then let future measured geometry and production systems upgrade confidence and adjustments without replacing the recommendation architecture.
