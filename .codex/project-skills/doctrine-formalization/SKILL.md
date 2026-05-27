---
name: doctrine-formalization
description: Use when changing project doctrine, philosophy, ADRs, governance docs, or canonical terminology in residential-energy-planner. Keeps implicit concepts explicit and portable across agents.
---

# Doctrine Formalization

## Workflow

1. Read `AGENTS.md`, `PROJECT_STATE.md`, `discovery-index.md`.
2. Load only relevant doctrine:
   - `docs/philosophy/*`
   - `docs/adr/*`
   - `docs/architecture/COGNITION_LAYERS.md`
   - `docs/architecture/CANONICAL_TERMINOLOGY.md`
3. Identify whether the change affects canonical, derived, advisory, operational, or historical knowledge.
4. Prefer additive doctrine or ADR updates over rewriting history.
5. Preserve: structured data decides, deterministic rules interpret, AI explains, UI reveals.

## Checks

- no fake completeness
- no hidden authority upgrade
- no advisory output promoted to canonical without explicit decision
- model-agnostic wording
- continuity files updated when doctrine changes restore behavior
