# Session Handoff

## Updated

2026-05-25

## Session Summary

- Session date: 2026-05-25
- Starting commit: `314e4ef`
- Current head commit before next commit: `314e4ef`
- Repo commits created this session:
  - none yet

## What Changed Last

- Added an additive current-home-energy-architecture layer to the advisor recommendation output.
- The new layer classifies current solar/inverter topology, preserves existing-vs-proposed equipment boundaries, explains outage-solar cautions, battery retrofit implications, expansion posture, and generator coexistence uncertainty, and keeps unknown current-state evidence unresolved instead of guessed.
- Threaded that current-state topology into the future-looking inverter/system layer and the structured reasoning graph so existing-home conditions now shape future-path explanation explicitly.

## Verification Performed

- `python3 -m unittest discover -s tests -p 'test_*.py'` passed in `apps/api`
- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`
- `git diff --check` passed

## Protections Verified

- Deterministic behavior preserved across backup-scope, current-topology, panel/service, inverter/system, battery, solar, and reasoning-graph logic
- Existing-vs-proposed equipment state remains explicit instead of inferred from future recommendations
- Microinverter handling remains planning-only and does not imply outage capability, NEC/compliance, interconnection approval, or final compatibility validation
- API evolution stayed additive and existing GET contracts remained compatible

## Remaining Risks

- Current-state topology still depends on role markers plus current product signals rather than a verified field inventory
- Optimizer-based topology remains inferred from product context because no dedicated optimizer equipment type exists yet
- Existing local databases may need reseeding to surface the new `recommendation.current_home_energy_architecture_v1` provenance record and the updated seeded microinverter demo path
- Outage solar behavior, generator coexistence, and retrofit posture remain planning-level cautions, not product-level operating guarantees

## Current Resume Point

The next implementation target is still the deeper solar-readiness and roof-capacity-realism slice, now with explicit current-state solar topology and a clearer distinction between today’s home architecture and the future recommendation path.

## Copy/Paste Restore Prompt

```text
Resume work in /home/mattcoje/residential-energy-planner from the latest clean commit, then load only the current advisor contract, recommendation service, and latest topology-modeling handoff.

Load skills:
- .codex/skills/energy-planner-runtime-invariants/SKILL.md
- .codex/skills/energy-planner-provenance-rules/SKILL.md
- .codex/skills/repo-memory-map/SKILL.md
- .codex/skills/repo-guardrails/SKILL.md
- /home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md

Current completed state:
- deterministic backup-load selection is explicit and inspectable
- current home energy architecture now distinguishes existing solar/inverter topology from proposed future equipment
- panel/service architecture includes planning-only consistency checks
- inverter/system architecture now consumes current topology before explaining future AC-coupled vs hybrid direction
- recommendation outputs still include an additive structured reasoning graph

Unfinished work:
- deeper solar-readiness and roof-capacity realism
- broader provenance coverage beyond the current inspectability, topology, and graph surfaces

Next safe implementation boundary:
- deepen the deterministic solar-readiness slice without expanding into final inverter sizing, compliance logic, migration work, or non-additive API changes
- keep current topology, future architecture, and outage-solar trust wording narrow and inspectable while future site-aware signals are attached

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

See `docs/handoffs/2026-05-25-existing-solar-inverter-topology-modeling.md`
