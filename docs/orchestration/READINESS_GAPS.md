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
- data origin
- provenance summary
- derived-output rule keys
- explicit non-authoritative fields

## Non-Goals For Now

- no DER dispatch
- no automatic utility submission
- no contractor approval workflow
- no live operational control
- no inferred field verification
