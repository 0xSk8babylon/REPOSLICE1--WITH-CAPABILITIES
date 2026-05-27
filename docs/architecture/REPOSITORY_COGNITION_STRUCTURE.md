# Repository Cognition Structure

## Proposed Structure

```text
docs/
  philosophy/      durable doctrine and non-goals
  architecture/    cognition layers, terminology, architecture definitions
  adr/             accepted architecture decisions
  continuity/      lean restore workflow and unresolved architecture
  handoffs/        dated historical session records
  roadmap/         sequencing and phase boundaries
  topology/        topology lifecycle and future topology intelligence
  trust/           trust zones and scope boundaries
  provenance/      lineage model and provenance gaps
  governance/      AI, migration, authority, and process discipline
  security/        scoped intelligence outputs and safety boundaries
  orchestration/   future DER/utility/contractor readiness gaps

.codex/
  skills/          implementation guardrails currently used by Codex
  project-skills/  portable repo-specific workflows for future agents
```

## Canonical Vs Supporting Files

- Root discovery files route restore and current state.
- `docs/architecture/` defines cognition and terminology.
- `docs/philosophy/` and `docs/adr/` define durable intent and accepted decisions.
- `docs/governance/`, `docs/trust/`, and `docs/provenance/` define authority and lineage boundaries.
- `docs/continuity/`, `docs/roadmap/`, and handoffs preserve work sequencing.
- `.codex/project-skills/` compress recurring governance workflows into portable agent instructions.

## Migration Posture

This structure is additive. Existing root docs and `docs/session-continuity/` remain valid until references can be narrowed deliberately.
