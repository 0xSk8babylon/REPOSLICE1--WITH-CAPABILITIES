# 2026-05-24 Panel Service Preliminary Architecture

## What Changed

- Added a first-pass deterministic panel/service architecture layer to the recommendation output.
- The new layer classifies:
  - existing main service panel posture
  - panel upgrade likelihood
  - service upgrade caution
  - critical-loads subpanel suitability
  - partial-home backup suitability
  - whole-home backup suitability
  - smart-panel readiness note
  - generator integration readiness note
  - recommended backup architecture
- The layer uses only current planning signals:
  - main panel data
  - service size
  - backup load grouping
  - design goal
  - recommendation profile
  - product/architecture signals
  - pathway/install realism

## Constraints Preserved

- No migration or persistence change
- No redesign of recommendation profiles
- No redesign of battery, solar, or roof-readiness layers
- No inverter sizing
- No smart-panel modifier logic
- No generator sizing

## Verification

- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`

## Exact Next Target

Refine backup-load selection and backup-scope realism before inverter sizing, so the new panel/service layer constrains a better-grounded backup architecture path instead of sizing around weak or incomplete load intent.
