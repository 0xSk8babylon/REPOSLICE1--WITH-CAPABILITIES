# 2026-05-24 Recommendation Inspectability Layer

## What Changed

- Added an additive inspectability layer to the resilience recommendation payload.
- Selected profile cards now carry structured basis signals, estimated inputs, incomplete inputs, confidence posture, rule keys, and planning-only warnings when provenance is partial.
- Battery sizing estimates now carry inspectability metadata for backup load energy need, autonomy posture, reserve posture, future growth posture, and estimated-input warnings.
- Solar sizing estimates now carry inspectability metadata for solar posture, low-solar posture, recovery posture, battery-recovery relationship, and estimated-input warnings.
- Added seeded rule-provenance entries for profile-backed battery sizing and solar sizing.
- Surfaced the new inspectability layer in the Design Advisor UI without exposing raw sizing formulas.

## Verification

- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`

## Constraints Preserved

- No migration or persistence change
- No redesign of recommendation profiles
- No redesign of battery or solar sizing logic
- No inverter sizing implementation
- Outputs remain deterministic, provenance-aware, and planning-only

## Exact Next Target

Add the next deterministic recommendation slice that explains how current architecture choices and equipment mix shift profile fit, while extending lineage coverage into design facts and scenario-facing guidance without exposing engineering formulas.
