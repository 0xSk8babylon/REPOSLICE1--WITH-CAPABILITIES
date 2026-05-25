# 2026-05-24 Layered Skills Restore Migration

## What Changed

- Added a compact discovery layer at the repo root with `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`.
- Added repo-local skills for memory routing and project guardrails under `.codex/skills/`.
- Refactored `AGENTS.md` so it routes sessions through layered restore instead of mandating a full `docs/` sweep.
- Added `docs/session-continuity/continuity-workflow.md` as the canonical procedure for restore and closeout.
- Reduced duplicated restore instructions in `docs/session-continuity/session-restore-template.md` and `docs/session-continuity/persistence-agent-plan.md`.
- Added lightweight helper scripts in `scripts/restore-context.sh` and `scripts/closeout-checklist.sh`.

## Architecture Impact

- Runtime architecture did not change.
- Repository operating architecture did change: restore procedure is now separated from project-state memory, and detailed doctrine/history is loaded on demand.

## Token-Efficiency Impact

- Startup no longer requires loading all top-level docs, all continuity docs, or doctrine files by default.
- Discovery now routes sessions to the smallest relevant context set before any deep-reference reads.

## Next Recommended Product Step

Deepen provenance coverage across more entity fields and derived outputs while preserving transient takeoffs and the planning-only boundary.

## Remaining Gaps

- Detailed continuity docs are still broad and could be slimmed further over time.
- No automated enforcement yet ensures the root discovery files and detailed continuity docs stay synchronized.
- Provenance depth and migration discipline remain the main product-side pressure points.
