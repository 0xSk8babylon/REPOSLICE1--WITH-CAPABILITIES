# Session Handoff

## Updated

2026-05-25

## Session Summary

- Session date: 2026-05-25
- Starting commit: `7412538`
- Current head commit before next commit: `7412538`
- Repo commits created this session:
  - none yet

## What Changed Last

- Added additive immutable `scenario_revisions` persistence so saved planning scenarios now accumulate revision lineage and advisor-linked snapshot framing without replacing the live editable scenario row.
- Extended scenario and advisor responses with revision-aware metadata, including revision counts, latest revision identity, and design-advisor planning-state links to the latest saved revision when present.
- Surfaced revision framing in the Design Advisor and Scenario Comparison UI so users can distinguish live workspace state, saved scenario state, and historical revision identity without introducing a full version-control workflow.

## Verification Performed

- `python3 -m unittest discover -s tests -p 'test_scenario_revisions.py'` passed in `apps/api`
- `python3 -m unittest discover -s tests -p 'test_resilience_recommendation.py'` passed in `apps/api`
- `python3 -m compileall app` passed in `apps/api`
- `npm run build` passed in `apps/web`
- `git diff --check` passed

## Protections Verified

- Advisor logic stayed unchanged
- API and persistence changes were additive only
- Planning-only trust framing remains visible near recommendation, topology, architecture, and reasoning outputs
- The UI still surfaces inspectability and provenance, and the new revision layer keeps historical framing visible without turning the page into a version-management system

## Remaining Risks

- The Design Advisor still relies on existing generic layout primitives rather than a dedicated architecture-visualization component system
- Scenario revisions currently store compact planning-state framing rather than full historical advisor payloads or diffable reasoning-graph snapshots
- The advisor still evaluates the current linked design state rather than replaying recommendation logic against a selected historical revision
- Existing local DBs may need reseeding or startup backfill to populate baseline revisions for older scenario rows

## Current Resume Point

The next implementation target remains the deeper solar-readiness and roof-capacity-realism slice, now that the advisor reasoning spine also has a clearer workspace-oriented, diagram-like, pathway-comparison, planning-state-snapshot, and persistent-revision surface.

## Copy/Paste Restore Prompt

```text
Resume work in /home/mattcoje/residential-energy-planner from the latest clean commit, then load only the current advisor UI, current topology handoff, and current recommendation contract slices.

Load skills:
- explainable-planning-ui-architecture
- .codex/skills/energy-planner-runtime-invariants/SKILL.md
- .codex/skills/energy-planner-provenance-rules/SKILL.md
- .codex/skills/repo-memory-map/SKILL.md
- .codex/skills/repo-guardrails/SKILL.md
- /home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md

Current completed state:
- current-state solar/inverter topology is explicit
- panel/service, inverter/system, and reasoning graph are explicit
- Design Advisor UI now groups those outputs into a workspace flow with progressive disclosure, compact architecture/reasoning visualizations, a pathway-comparison surface, planning-state snapshot framing, and revision-aware scenario links

Unfinished work:
- deeper solar-readiness and roof-capacity realism
- broader provenance coverage beyond current inspectability surfaces

Next safe implementation boundary:
- deepen the deterministic solar-readiness slice without expanding into final inverter sizing, compliance logic, migration work, or non-additive API changes
- preserve the current workspace structure and planning-only trust framing while attaching future site-aware signals

Verification commands:
- npm run build
- git diff --check
- git status --short
```

## If You Resume Now

- Start from `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`
- Load `.codex/skills/repo-memory-map/SKILL.md` and `.codex/skills/repo-guardrails/SKILL.md`
- Read detailed continuity or doctrine docs only if the task requires them

## Latest Detailed Handoff

See `docs/handoffs/2026-05-25-persistent-scenario-revision-foundation.md`
