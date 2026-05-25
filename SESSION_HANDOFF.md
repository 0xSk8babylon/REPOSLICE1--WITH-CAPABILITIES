# Session Handoff

## Updated

2026-05-25

## What Changed Last

- Added a deterministic backup-load selection layer behind the recommendation stack.
- Recommendation outputs now distinguish recorded essential/preferred load grouping from the selected planning backup scope and expose that basis additively in the API and Design Advisor UI.
- Battery, solar, and panel/service guidance now consume the explicit selected scope instead of silently inheriting broader backup intent.
- Kept the change additive: no migration, no persistence change, no inverter sizing, no generator sizing, and no exposed engineering formulas.

## Current Resume Point

The next implementation target is to add the next architecture-fit recommendation slice around equipment mix and backup-path tradeoffs, now that backup-load selection, panel/service posture, and current planning scope are all explicit before inverter sizing.

## If You Resume Now

- Start from `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`
- Load `.codex/skills/repo-memory-map/SKILL.md` and `.codex/skills/repo-guardrails/SKILL.md`
- Read detailed continuity or doctrine docs only if the task requires them

## Latest Detailed Handoff

See `docs/handoffs/2026-05-25-deterministic-backup-load-selection.md`
