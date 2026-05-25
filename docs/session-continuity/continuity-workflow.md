# Continuity Workflow

## Purpose

This is the canonical continuity procedure for this repository. It complements the compact discovery layer and should be loaded only when continuity maintenance or deeper repo-state validation is needed.

## Restore Flow

1. Read the discovery layer:
   - `AGENTS.md`
   - `PROJECT_STATE.md`
   - `SESSION_HANDOFF.md`
   - `discovery-index.md`
   - repo-local skills under `.codex/skills/`
2. Identify the task category.
3. Load only the task-relevant operational references from `discovery-index.md`.
4. Load deep references only when the task actually depends on them.
5. Verify that code and durable memory still agree before claiming restore is current.

## Closeout Flow

At the end of a meaningful session:

1. Update `PROJECT_STATE.md`
2. Update `SESSION_HANDOFF.md`
3. Update `docs/CURRENT_STATE.md`
4. Update `docs/NEXT_STEPS.md`
5. Update `docs/ACTIVE_TASKS.md` if task status changed
6. Append `docs/SESSION_LOG.md`
7. Update only the affected files in `docs/session-continuity/`
8. Create a dated file in `docs/handoffs/`

## Deep-Reference Triggers

- Read `docs/ARCHITECTURE.md` for architecture changes.
- Read `docs/DATABASE_SCHEMA.md` for schema or persistence changes.
- Read `docs/API_CONTRACTS.md` for API shape changes.
- Read philosophy and ADR files only for doctrine-sensitive work.
- Read historical handoffs only when the latest handoff or discovery files are insufficient.

## Anti-Patterns

- mandatory full-doc restore sweeps
- mandatory philosophy or ADR sweeps
- repeating restore procedure across multiple state docs
- treating historical handoffs as the primary restore surface
