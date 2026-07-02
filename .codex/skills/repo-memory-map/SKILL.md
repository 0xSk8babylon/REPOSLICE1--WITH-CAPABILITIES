---
name: repo-memory-map
description: Map this repository's durable memory layers and route the session to the smallest relevant context set.
---

# Repo Memory Map

## Purpose

Use the compact discovery layer first, then route to only the project-specific references needed for the task.

## Discovery Order

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `discovery-index.md`
4. `.codex/skills/repo-guardrails/SKILL.md`

## Routing

- Continuity or restore work:
  - `docs/session-continuity/continuity-workflow.md`
  - latest file in `docs/handoffs/`
- Product-state check:
  - `docs/CURRENT_STATE.md`
  - `docs/NEXT_STEPS.md`
  - `docs/ACTIVE_TASKS.md`
- Architecture or persistence change:
  - `docs/ARCHITECTURE.md`
  - `docs/DATABASE_SCHEMA.md`
  - only the relevant `docs/session-continuity/*` files
- API change:
  - `docs/API_CONTRACTS.md`
  - relevant router and schema modules
- Doctrine-sensitive change:
  - only the philosophy or ADR files directly tied to the decision

## Rules

- Do not load all of `docs/session-continuity/` by default.
- Do not load all philosophy docs or ADRs by default.
- Treat root discovery files as the restore entry point and the `docs/` tree as detailed supporting memory.
