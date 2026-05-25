# Session Handoff

## Updated

2026-05-24

## What Changed Last

- Added a preliminary panel/service architecture layer behind the existing recommendation stack.
- Recommendation outputs now classify likely panel/service posture, panel-upgrade likelihood, service-upgrade caution, backup-architecture suitability, smart-panel readiness, and generator-integration readiness without performing inverter or generator sizing.
- Kept the change additive: no migration, no persistence change, no inverter sizing, no smart-panel modifier logic, no generator sizing, and no exposed engineering formulas in the UI.

## Current Resume Point

The next implementation target is to refine backup-load selection and backup-scope realism before inverter sizing, so the new panel/service architecture layer constrains a better-grounded power path instead of sizing around weak load assumptions.

## If You Resume Now

- Start from `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`
- Load `.codex/skills/repo-memory-map/SKILL.md` and `.codex/skills/repo-guardrails/SKILL.md`
- Read detailed continuity or doctrine docs only if the task requires them

## Latest Detailed Handoff

See `docs/handoffs/2026-05-24-panel-service-preliminary-architecture.md`
