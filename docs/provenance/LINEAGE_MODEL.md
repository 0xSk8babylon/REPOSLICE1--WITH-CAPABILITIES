# Provenance Lineage Model

## Purpose

Preserve lineage as information moves from recorded facts to derived estimates, advisory outputs, revisions, and future orchestration abstractions.

## Lineage Elements

Each derived or advisory output should identify:

- source objects
- rule keys
- source documents when available
- data origin
- authority layer
- trust zone
- data classification
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
- Data classification is not yet persisted or enforced as an API policy.
- Existing API responses are not scoped RBAC views.

## Derivation Rule

Provenance must survive derivation. If a derived output cannot expose lineage, confidence must be downgraded or the output must remain clearly provisional.

## Classification Rule

Provenance describes where information came from and how it was derived. Data classification describes intended handling and visibility. Neither replaces the other.

Future scoped API views should preserve both:

- provenance lineage for source quality, assumptions, and missing inputs
- data classification for audience-specific exposure
- authority layer for canonical, derived, advisory, operational, or historical status
- trust zone for recorded, derived, advisory, or operational posture
