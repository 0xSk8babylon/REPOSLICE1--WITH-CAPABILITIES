# Session Handoff

## Updated

2026-05-25

## Session Summary

- Session date: 2026-05-25
- Starting commit: `a2b4c88`
- Current head commit before next commit: `a2b4c88`
- Repo commits created this session:
  - none yet

## What Changed Last

- Added an additive structured system reasoning graph to the advisor recommendation output without changing the existing backup-scope, panel/service, inverter/system, battery, or solar calculations.
- The new graph formalizes inspectable dependencies between recorded load grouping, backup scope, panel/service posture, inverter/system architecture, and the recommended battery/solar posture for the currently recommended profile.
- Added provenance-linked rule keys for the graph layer, surfaced the graph in the Design Advisor UI, and expanded seeded backend regression coverage for the new dependency output.

## Verification Performed

- `python3 -m unittest discover -s tests -p 'test_*.py'` passed in `apps/api`
- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`
- `git diff --check` passed

## Protections Verified

- Deterministic behavior preserved across recommendation, backup-scope, panel/service, inverter/system architecture, battery, and solar logic
- The new graph is additive and interpretive only; it does not introduce new sizing formulas or hidden coupling
- Provenance and trust framing remained explicit and planning-only
- No NEC/compliance claims, migration work, or breaking API-contract changes were introduced

## Remaining Risks

- The reasoning graph currently traces only the recommended profile, not every profile variant
- Backup-scope posture still depends on recorded essential/preferred tagging and recorded-load coverage rather than circuit-level load studies or outage sequencing
- Inverter/system architecture and downstream graph edges remain planning posture only, not final inverter sizing, transfer design, or interconnection design
- Existing local databases may need reseeding to surface the new `recommendation.system_reasoning_graph_v1` provenance record

## Current Resume Point

The next implementation target is still the deeper solar-readiness and roof-capacity-realism slice, now that the advisor dependency chain from load grouping through battery/solar posture is explicit and inspectable.

## Copy/Paste Restore Prompt

```text
Resume work in /home/mattcoje/residential-energy-planner from the latest clean commit, then load only the current advisor contract, recommendation service, and latest reasoning-graph handoff.

Load skills:
- .codex/skills/energy-planner-runtime-invariants/SKILL.md
- .codex/skills/energy-planner-provenance-rules/SKILL.md
- .codex/skills/repo-memory-map/SKILL.md
- .codex/skills/repo-guardrails/SKILL.md
- /home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md

Current completed state:
- deterministic backup-load selection is explicit and inspectable
- panel/service architecture includes planning-only consistency checks
- inverter/system architecture explains AC-coupled vs hybrid posture and coexistence assumptions
- recommendation outputs now include an additive structured reasoning graph for the recommended profile

Unfinished work:
- deeper solar-readiness and roof-capacity realism
- broader provenance coverage beyond the current inspectability and graph surfaces

Next safe implementation boundary:
- deepen the deterministic solar-readiness slice without expanding into final inverter sizing, compliance logic, migration work, or non-additive API changes
- keep the reasoning graph additive and planning-only while future site-aware signals are attached

Verification commands:
- python3 -m unittest discover -s tests -p 'test_*.py'
- python3 -m compileall apps/api/app
- npm run build
- git diff --check
- git status --short
```

## If You Resume Now

- Start from `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`
- Load `.codex/skills/repo-memory-map/SKILL.md` and `.codex/skills/repo-guardrails/SKILL.md`
- Read detailed continuity or doctrine docs only if the task requires them

## Latest Detailed Handoff

See `docs/handoffs/2026-05-25-structured-system-reasoning-graph-foundation.md`
