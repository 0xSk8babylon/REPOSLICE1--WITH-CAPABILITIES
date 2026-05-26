# Session Handoff

## Updated

2026-05-25

## Session Summary

- Session date: 2026-05-25
- Starting commit: `6c1345c`
- Current head commit: `6c1345c`
- Repo commits created this session:
  - none

## What Changed Last

- Added a new deterministic inverter/system architecture layer to the advisor recommendation output without expanding into inverter sizing, NEC/compliance claims, or non-additive API work.
- The new layer now explains AC-coupled vs hybrid posture, inverter pathway suitability, battery/solar/generator coexistence assumptions, expansion direction, and planning-only architecture consistency from recorded design signals.
- Profile-level architecture-fit tradeoffs are now fully wired and consume the new inverter/system posture in addition to equipment mix, outage posture, and panel/service direction.
- Surfaced inverter/system architecture confidence, inspectability, and consistency output in the Design Advisor UI and added seeded regression coverage for the new advisor states.

## Verification Performed

- `python3 -m unittest discover -s tests -p 'test_*.py'` passed in `apps/api`
- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`
- Seeded advisor verification confirmed:
  - `design_001` resolves to `balanced` with `partial-home outage posture`, `high` backup-scope confidence, and `partial-home backup`
  - `design_001` now resolves to a `battery-ready path needs inverter clarification` system direction with `conditional` system-architecture consistency
  - `design_001` balanced profile now reports `aligned` architecture-fit tradeoffs tied to the partial-home path
  - `design_002` resolves to `premium_future_ready` with `future-ready service upgrade path`
  - `design_002` now resolves to a `hybrid inverter backbone` system direction with `aligned` system-architecture consistency
  - `design_002` premium profile now reports `aligned` architecture-fit tradeoffs tied to the hybrid/generator future-ready path
  - `design_001` with `whole_home_backup` goal but unchanged load grouping remains conditionally narrowed
  - `design_001` with all recorded loads promoted into backup grouping becomes a whole-home outage-posture candidate while the workshop/service path still keeps architecture future-ready

## Protections Verified

- Deterministic behavior preserved across recommendation, backup-scope, inverter/system architecture, battery, solar, and panel/service logic
- Provenance and trust framing remained additive and planning-only
- No migration, inverter sizing, NEC/compliance, or breaking API-contract scope expansion

## Remaining Risks

- Backup-scope posture still depends on recorded essential/preferred tagging and recorded-load coverage rather than circuit-level load studies or outage sequencing
- Existing local databases may need reseeding to surface the new backup-architecture-consistency, profile-architecture-fit, and inverter/system-architecture rule provenance records
- Whole-home outage posture is still a planning candidate classification, not a verified whole-property inventory or transfer design
- Inverter/system architecture remains a planning posture derived from current architecture type and equipment mix, not final inverter sizing or interconnection design
- Regression coverage remains targeted to advisor stabilization paths rather than exhaustive design permutations

## Current Resume Point

The next implementation target is the deeper solar-readiness and roof-capacity-realism slice, now that backup-load selection, profile-level architecture-fit tradeoffs, panel/service consistency checks, and inverter/system architecture reasoning are explicit before final inverter sizing.

## Copy/Paste Restore Prompt

```text
Resume work in /home/mattcoje/residential-energy-planner from commit 6c1345c, then inspect the current uncommitted architecture-reasoning changes.

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
- recommendation outputs now also include an additive inverter/system architecture layer with AC-coupled vs hybrid posture, coexistence assumptions, and planning-only consistency output

Unfinished work:
- deeper solar-readiness and roof-capacity realism behind the current profile architecture
- deeper provenance coverage beyond current inspectability surfaces

Next safe implementation boundary:
- deepen the deterministic solar-readiness slice without expanding into final inverter sizing, compliance logic, migration, or non-additive API changes
- keep backup-scope, panel/service, profile-fit, and inverter/system trust wording narrow and inspectable while doing so

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

See `docs/handoffs/2026-05-25-inverter-system-architecture-reasoning.md`
