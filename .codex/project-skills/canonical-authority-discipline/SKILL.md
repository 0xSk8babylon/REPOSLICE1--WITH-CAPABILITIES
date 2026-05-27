---
name: canonical-authority-discipline
description: Use when a change could blur canonical objects, derived estimates, advisory outputs, operational state, revision lineage, or deployment lineage in residential-energy-planner.
---

# Canonical Authority Discipline

## Workflow

1. Load `docs/architecture/COGNITION_LAYERS.md`.
2. Load `docs/architecture/CANONICAL_TERMINOLOGY.md`.
3. Classify affected outputs by authority layer.
4. Keep canonical state, derived estimates, advisory explanations, and operational facts distinct.
5. Downgrade wording when evidence does not support stronger authority.

## Checks

- source of truth is explicit
- derived output has inspectable basis
- advisory text cannot be mistaken for persisted fact
- operational truth is not implied by planning state
- revision and deployment lineage are not invented
