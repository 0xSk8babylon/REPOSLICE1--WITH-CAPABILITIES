---
name: topology-intelligence
description: Use when changing current-home energy architecture, equipment topology, solar/inverter topology, scenario revisions, lifecycle state, or future DER topology planning in residential-energy-planner.
---

# Topology Intelligence

## Workflow

1. Load `docs/topology/TOPOLOGY_LIFECYCLE.md`.
2. Identify lifecycle stage: recorded current state, proposed pathway, saved revision, field-verified, operational, or future expansion.
3. Keep current, proposed, and operational truth separate.
4. Preserve existing-vs-proposed equipment role markers.
5. Expose source inputs, confidence, and missing field verification.

## Boundaries

- no inferred installed state without recorded source
- no operational topology until future authority exists
- no DER dispatch or utility approval claims
- topology reasoning remains planning-only unless promoted by future field verification
