# 2026-05-25 Deterministic Backup Load Selection

## Session Metadata

- Session date: 2026-05-25
- Starting commit: `61693f8`
- Ending commit: `2cf88e4`
- Repo commits created this session:
  - `e854b8f` `Add energy planner refinement governance skills`
  - `9fad58b` `Refine deterministic backup load selection`
- Related global-skill commits outside this repo:
  - `4c3b257` in `~/.codex/global-skills` for `stabilization-before-feature-expansion`
  - `f68a2ba` in `~/.codex/global-skills` for `session-closeout-stabilization`

## Implementation Summary

- Added project governance skills for runtime invariants, provenance rules, and load-selection doctrine.
- Added a deterministic backup-load selection layer behind recommendation outputs.
- Recommendation payloads now expose `backup_load_selection` with selected scope label, rule basis, priority band, planning-gap warning, and inspectability metadata.
- Battery, solar, and panel/service guidance now consume the explicit selected scope instead of silently treating all backup-tagged intent as equivalent.
- Panel/service architecture recommendations now stay narrower when broader backup scope is not actually recorded.

## Files Changed

- `.codex/skills/energy-planner-runtime-invariants/SKILL.md`
- `.codex/skills/energy-planner-provenance-rules/SKILL.md`
- `.codex/skills/energy-planner-load-selection-doctrine/SKILL.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `apps/api/app/design_advisor/schemas.py`
- `apps/api/app/seed/sample_data.py`
- `apps/api/app/services/resilience_recommendation.py`
- `apps/web/src/pages/DesignAdvisorPage.jsx`
- `docs/ACTIVE_TASKS.md`
- `docs/API_CONTRACTS.md`
- `docs/CURRENT_STATE.md`
- `docs/NEXT_STEPS.md`
- `docs/SESSION_LOG.md`
- `docs/handoffs/2026-05-25-deterministic-backup-load-selection.md`

## Verification Commands And Results

- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`
- `git status --short` clean after `9fad58b`

## Deterministic / Provenance / Trust Protections Verified

- Deterministic selection basis now explicitly controls the backup scope used by battery, solar, and panel/service guidance.
- Recommendation behavior remains structured-data-first and rule-driven.
- Planning-only limitations remain explicit in the API and UI.
- Provenance expansion stayed additive through rule documentation and inspectability metadata.
- No engineering certification, inverter sizing, or generator sizing claims were introduced.

## Unresolved Risks

- Backup-scope selection still depends on recorded essential/preferred tagging rather than circuit-level load studies or outage sequencing.
- Existing local databases may need reseeding to surface the backup-load-selection rule provenance record.

## Unfinished Work

- Add the next architecture-fit recommendation slice around equipment mix and backup-path tradeoffs.
- Extend provenance coverage beyond the current inspectability surfaces.

## Next Recommended Refinement Layer

Add the next deterministic architecture-fit recommendation slice without expanding into inverter, generator, migration, or breaking API changes.

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
