# Session Handoff

## Updated

2026-05-25

## Session Summary

- Session date: 2026-05-25
- Starting commit: `542a368`
- Current head commit: `542a368`
- Repo commits created this session:
  - none

## What Changed Last

- Continued backup-scope modeling stabilization by adding an additive profile-level architecture-fit tradeoff layer instead of changing sizing formulas or expanding into inverter/generator work.
- Recommendation profiles now explain how recorded equipment mix, explicit outage posture, panel/service direction, and architecture-consistency posture pull each profile narrower or broader.
- Surfaced the new architecture-fit tradeoff summary in the Design Advisor UI and extended profile inspectability/provenance to cite the new deterministic rule layer.
- Added a seeded internal rule provenance record plus backend regression coverage for the new profile-fit output on the current seeded advisor states.

## Verification Performed

- `python3 -m unittest discover -s tests -p 'test_*.py'` passed in `apps/api`
- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`
- Seeded advisor verification confirmed:
  - `design_001` resolves to `balanced` with `partial-home outage posture`, `high` backup-scope confidence, and `partial-home backup`
  - `design_001` balanced profile now reports `aligned` architecture-fit tradeoffs tied to the partial-home path
  - `design_002` resolves to `premium_future_ready` with `future-ready service upgrade path`
  - `design_002` premium profile now reports `aligned` architecture-fit tradeoffs tied to the hybrid/generator future-ready path
  - `design_001` with `whole_home_backup` goal but unchanged load grouping remains conditionally narrowed
  - `design_001` with all recorded loads promoted into backup grouping becomes a whole-home outage-posture candidate while the workshop/service path still keeps architecture future-ready

## Protections Verified

- Deterministic behavior preserved across recommendation, backup-scope, battery, solar, and panel/service logic
- Provenance and trust framing remained additive and planning-only
- No migration, inverter, generator, NEC/compliance, or breaking API-contract scope expansion

## Remaining Risks

- Backup-scope posture still depends on recorded essential/preferred tagging and recorded-load coverage rather than circuit-level load studies or outage sequencing
- Existing local databases may need reseeding to surface the new backup-architecture-consistency and profile-architecture-fit rule provenance records
- Whole-home outage posture is still a planning candidate classification, not a verified whole-property inventory or transfer design
- Regression coverage remains targeted to advisor stabilization paths rather than exhaustive design permutations

## Current Resume Point

The next implementation target is the deeper solar-readiness and roof-capacity-realism slice, now that backup-load selection, outage-posture reasoning, architecture-consistency checks, and profile-level equipment-mix tradeoffs are explicit before inverter sizing.

## Copy/Paste Restore Prompt

```text
Resume work in /home/mattcoje/residential-energy-planner from commit 542a368, then inspect the current uncommitted stabilization changes.

Load skills:
- .codex/skills/energy-planner-runtime-invariants/SKILL.md
- .codex/skills/energy-planner-provenance-rules/SKILL.md
- .codex/skills/repo-memory-map/SKILL.md
- .codex/skills/repo-guardrails/SKILL.md
- /home/mattcoje/.codex/skills/lean-context-loading/SKILL.md
- /home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md

Current completed state:
- deterministic backup-load selection is already in place
- backup-scope selection now exposes outage posture, recorded-load coverage, confidence, and inspectable planning-only provenance
- panel/service UI now exposes explicit planning-only confidence, provenance, and architecture-consistency output
- seeded advisor outputs now have targeted regression coverage for partial-home and whole-home-goal boundary cases
- recommendation profiles now include an additive architecture-fit tradeoff layer tied to equipment mix, outage posture, and backup-path direction

Unfinished work:
- deeper solar-readiness and roof-capacity realism behind the current profile architecture
- deeper provenance coverage beyond current inspectability surfaces

Next safe implementation boundary:
- deepen the deterministic solar-readiness slice without expanding into inverter, generator, migration, or non-additive API changes
- keep backup-scope, panel/service, and profile-fit trust wording narrow and inspectable while doing so

Verification commands:
- python3 -m unittest discover -s tests -p 'test_*.py'
- python3 -m compileall apps/api/app
- npm run build
- git status --short
```

## If You Resume Now

- Start from `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`
- Load `.codex/skills/repo-memory-map/SKILL.md` and `.codex/skills/repo-guardrails/SKILL.md`
- Read detailed continuity or doctrine docs only if the task requires them

## Latest Detailed Handoff

See `docs/handoffs/2026-05-25-profile-architecture-fit-stabilization.md`
