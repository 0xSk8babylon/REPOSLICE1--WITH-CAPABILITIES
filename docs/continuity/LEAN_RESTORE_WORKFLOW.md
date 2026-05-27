# Lean Restore Workflow

## Short Prompt

```text
Load project skills before implementation.
```

## Agent Steps

1. Read `AGENTS.md`.
2. Read `PROJECT_STATE.md`.
3. Read `SESSION_HANDOFF.md`.
4. Read `discovery-index.md`.
5. Load `.codex/project-skills/*` metadata relevant to the task.
6. Load `.codex/skills/*` only when implementation touches that governed area.
7. Load task-specific docs from `discovery-index.md`.
8. Verify code and docs agree before changing behavior.

## Deep Reference Triggers

- Doctrine change: `docs/philosophy/`, `docs/adr/`, `docs/architecture/`
- Persistence change: `docs/DATABASE_SCHEMA.md`, `docs/governance/MIGRATION_DISCIPLINE.md`
- Trust or provenance change: `docs/trust/`, `docs/provenance/`
- Topology change: `docs/topology/`
- Orchestration planning: `docs/orchestration/`
- Roadmap change: `docs/roadmap/`, `docs/NEXT_STEPS.md`, `docs/ACTIVE_TASKS.md`

## Closeout

Update root discovery files, affected canonical docs, session log, and a dated handoff. Avoid repeating the same state summary in every file.
