# 2026-05-23 Phase 2E Provenance Foundation

## What Changed

- Added `SourceDocument`, `DataProvenance`, and `RuleProvenance` as first-pass backend provenance models.
- Added read-oriented provenance endpoints for source documents, entity provenance, and rule provenance.
- Added seeded provenance examples for demo product specs, a user-entered load assumption, an internal completeness rule, and a transient takeoff basis.
- Exposed provenance summaries in the product library, advisor outputs, transient takeoff views, and AI grounding context.

## Important Boundary

- Placeholder references are still not verified product facts.
- Verification status belongs to source-document posture, not to engineering validity.
- Trust badges remain presentation-layer signals, not a replacement for structured provenance.
- Derived takeoffs remain transient and are still not persisted snapshots.

## Recommended Next Step

- Expand provenance coverage to more entity fields and scenario/estimate reasoning before considering persisted takeoff snapshots or stronger estimating claims.
