---
name: provenance-lineage
description: Use when changing provenance summaries, source lineage, trust states, derived outputs, scenario revisions, or AI grounding in residential-energy-planner.
---

# Provenance Lineage

## Workflow

1. Load `docs/provenance/LINEAGE_MODEL.md`.
2. Load `docs/trust/TRUST_ZONES.md` if user-visible trust posture changes.
3. Map source objects, rule keys, data origin, confidence, missing inputs, and assumptions.
4. Preserve lineage through derived and advisory outputs.
5. Mark provisional outputs explicitly when lineage is partial.

## Checks

- provenance survives derivation
- verification is not overstated
- missing inputs are visible
- AI context remains grounded in structured state
- scenario revisions do not imply full replay unless persisted
