# Orchestration Readiness Gaps

## Current Posture

The repository is preparing for orchestration-safe intelligence, but it does not implement operational orchestration behavior.

## Needed Before DER Orchestration

- canonical device and topology identity model
- operational state authority model
- source and verification requirements for device capabilities
- event and revision lineage
- permission and control boundaries
- utility and interconnection abstractions
- failure and fallback model
- audit log

## Needed Before Contractor-Safe Intelligence

- scoped export boundary
- distinction between recorded facts, assumptions, and recommendations
- explicit exclusions for code, permitting, and engineering approval
- revisioned planning package identity
- source-linked provenance summaries

## Needed Before Utility-Safe Abstractions

- site identity and service territory model
- interconnection state model
- tariff and program source lineage
- utility-facing data minimization
- no AI-generated operational claims

## AI-Safe Architecture Views

Future AI and orchestration agents should consume structured envelopes that include:

- object IDs
- role and lifecycle stage
- authority level
- trust zone
- data classification
- data origin
- provenance summary
- derived-output rule keys
- explicit non-authoritative fields

These envelopes are future API-view contracts, not current RBAC or operational-control enforcement.

## Scoped API View Gaps

Before role-aware API views exist, the project still needs:

- a visibility matrix for consumer, contractor, utility, AI, operator, and internal governance audiences
- field-level data classifications for canonical objects and derived outputs
- provenance requirements per view
- explicit exclusion lists for private planning, utility-scoped, and operational-control fields
- compatibility rules for additive `/api/*` evolution
- audit expectations for exports and future operational events

## Non-Goals For Now

- no DER dispatch
- no automatic utility submission
- no contractor approval workflow
- no live operational control
- no inferred field verification
