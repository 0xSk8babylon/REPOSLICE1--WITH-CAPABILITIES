# AGENTS

## Scope

This repository is an isolated project memory boundary for `residential-energy-planner`.

- Do not import assumptions, APIs, workflows, or architecture from other repositories.
- Preserve continuity and modular architecture before making local optimizations.
- Prefer additive changes over rewrites.

## Startup Routing

Use the layered restore model. Do not perform a full `docs/` sweep by default.

At session start, read these files in order:

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `SESSION_HANDOFF.md`
4. `discovery-index.md`
5. repo-local skills if present:
   - `.codex/skills/repo-memory-map/SKILL.md`
   - `.codex/skills/repo-guardrails/SKILL.md`
   - task-relevant `.codex/project-skills/*/SKILL.md`

Then:

- load only the global skills needed for the task
- load only the task-relevant deep references listed in `discovery-index.md`
- read the latest file in `docs/handoffs/` only when the discovery files or current task indicate it is relevant

If any discovery-layer file is missing or stale, treat that as a continuity defect and repair it before making broader architecture changes.

## Memory Layers

- Discovery layer:
  - `AGENTS.md`
  - `PROJECT_STATE.md`
  - `SESSION_HANDOFF.md`
  - `discovery-index.md`
  - repo-local skills under `.codex/skills/`
- Operational layer:
  - selected global skill instructions
  - selected project skills under `.codex/project-skills/`
  - task-relevant continuity workflow docs
  - specific current-state or contract docs needed for the task
- Deep-reference layer:
  - architecture docs
  - schema and API contract docs
  - `docs/session-continuity/*`
  - philosophy docs, ADRs, and historical handoffs only when directly relevant

## Operating Principles

- Structured facts are authoritative.
- Deterministic rules and calculations must remain inspectable.
- AI is an explanation and orchestration layer, not a source of product facts.
- Existing frontend GET contracts are compatibility-sensitive.
- `/api/*` is the preferred API base path.
- Placeholder values must remain clearly labeled as placeholders.

## Current Phase Expectations

- SQLite is the local development system of record.
- Auth, billing, NEC automation, and permitting remain deferred.
- The frontend has moved beyond read-only and now exercises core POST/PATCH flows.
- Demo seed data remains valid for first-run continuity, but it is not factual authority.

## Project-Specific Guardrails

- Existing frontend GET contracts are compatibility-sensitive.
- Current product next-step priority remains provenance expansion, not architecture reinvention.
- Deep doctrine reads are not mandatory startup work; load philosophy or ADR files only when the task touches strategic boundaries, trust posture, or product doctrine.
- Historical handoffs are reference material, not the primary restore entry point.

## End-Of-Session Requirements

Before stopping work:

- update `PROJECT_STATE.md`
- update `SESSION_HANDOFF.md`
- update `docs/CURRENT_STATE.md`
- update `docs/NEXT_STEPS.md`
- update `docs/ACTIVE_TASKS.md` if task status changed
- append `docs/SESSION_LOG.md`
- update the specific `docs/session-continuity/*` files affected by architecture, persistence, roadmap, or pressure-point changes
- create a dated handoff in `docs/handoffs/`

## Non-Goals

- Do not quietly redesign the architecture.
- Do not replace structured persistence with prompt-only memory.
- Do not present placeholder engineering logic as verified truth.
