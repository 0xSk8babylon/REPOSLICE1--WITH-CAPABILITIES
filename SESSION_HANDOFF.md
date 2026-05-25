# Session Handoff

## Updated

2026-05-25

## Session Summary

- Session date: 2026-05-25
- Starting commit: `61693f8`
- Ending commit: `2cf88e4`
- Repo commits created this session:
  - `e854b8f` `Add energy planner refinement governance skills`
  - `9fad58b` `Refine deterministic backup load selection`
- Related global-skill commits created outside this repo:
  - `4c3b257` in `~/.codex/global-skills` for `stabilization-before-feature-expansion`
  - `f68a2ba` in `~/.codex/global-skills` for `session-closeout-stabilization`

## What Changed Last

- Added project governance skills for runtime invariants, provenance rules, and load-selection doctrine.
- Added a deterministic backup-load selection layer behind the recommendation stack.
- Recommendation outputs now distinguish recorded essential/preferred load grouping from the selected planning backup scope and expose that basis additively in the API and Design Advisor UI.
- Battery, solar, and panel/service guidance now consume the explicit selected scope instead of silently inheriting broader backup intent.
- Kept the change additive: no migration, no persistence change, no inverter sizing, no generator sizing, and no exposed engineering formulas.

## Verification Performed

- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`
- `git status --short` clean after the implementation commit

## Protections Verified

- Deterministic behavior preserved across recommendation, battery, solar, and panel/service logic
- Provenance and trust framing remained additive and planning-only
- No migration, inverter, or generator scope expansion

## Remaining Risks

- Backup-scope selection still depends on recorded essential/preferred tagging rather than circuit-level load studies
- Existing local databases may need reseeding to surface the new backup-load-selection rule provenance record

## Current Resume Point

The next implementation target is to add the next architecture-fit recommendation slice around equipment mix and backup-path tradeoffs, now that backup-load selection, panel/service posture, and current planning scope are all explicit before inverter sizing.

## Copy/Paste Restore Prompt

```text
Resume work in /home/mattcoje/residential-energy-planner from clean commit 2cf88e4.

Load skills:
- ~/.codex/global-skills/stabilization-before-feature-expansion/SKILL.md
- ~/.codex/global-skills/session-closeout-stabilization/SKILL.md
- .codex/skills/energy-planner-runtime-invariants/SKILL.md
- .codex/skills/energy-planner-provenance-rules/SKILL.md
- .codex/skills/energy-planner-load-selection-doctrine/SKILL.md
- .codex/skills/repo-memory-map/SKILL.md
- .codex/skills/repo-guardrails/SKILL.md

Current completed state:
- project governance skills added
- deterministic backup-load selection added
- additive backup_load_selection API/UI exposure added
- battery, solar, and panel/service guidance now consume explicit selected backup scope

Unfinished work:
- next architecture-fit recommendation slice for equipment mix and backup-path tradeoffs
- deeper provenance coverage beyond current inspectability surfaces

Next safe implementation boundary:
- add the next deterministic architecture-fit recommendation slice without expanding into inverter, generator, migration, or non-additive API changes

Verification commands:
- python3 -m compileall apps/api/app
- npm run build
- git status --short
```

## If You Resume Now

- Start from `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`
- Load `.codex/skills/repo-memory-map/SKILL.md` and `.codex/skills/repo-guardrails/SKILL.md`
- Read detailed continuity or doctrine docs only if the task requires them

## Latest Detailed Handoff

See `docs/handoffs/2026-05-25-deterministic-backup-load-selection.md`
