# Provenance Lineage Model

## Purpose

Preserve lineage as information moves from recorded facts to derived estimates, advisory outputs, revisions, and future orchestration abstractions.

## Lineage Elements

Each derived or advisory output should identify:

- source objects
- rule keys
- source documents when available
- data origin
- confidence level
- missing inputs
- assumptions
- scope limitations
- generated timestamp or revision identity when persisted

## Current Coverage

- Products, loads, estimated pathways, advisor outputs, scenario comparison, and recommendation inspectability have partial provenance surfaces.
- Scenario revisions preserve compact planning-state lineage.
- Rule provenance seed records exist for major advisor rules.

## Known Gaps

- Field-level provenance is not exhaustive.
- Design, scenario, home-model, and topology fields still need broader lineage summaries.
- Transient takeoffs are not versioned.
- Full advisor payload replay is not persisted for revisions.
- Deployment lineage is not formalized.

## Derivation Rule

Provenance must survive derivation. If a derived output cannot expose lineage, confidence must be downgraded or the output must remain clearly provisional.
