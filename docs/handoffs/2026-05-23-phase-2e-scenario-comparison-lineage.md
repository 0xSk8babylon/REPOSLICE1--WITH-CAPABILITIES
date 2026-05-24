# 2026-05-23 Phase 2E Scenario Comparison Lineage

## What Changed

- Replaced the placeholder-only `/api/scenarios/compare` service with deterministic comparison output derived from persisted scenarios and linked designs.
- Added additive scenario comparison metadata for planning completeness, pathway counts, low-confidence pathways, ecosystem mixing, missing location assignments, warnings, rankings, and source-lineage summaries.
- Updated the scenario comparison frontend to consume the richer compare payload while preserving the existing edit workflow.
- Repaired continuity drift by updating schema and state docs to include the provenance tables and the new comparison behavior.

## Important Boundary

- Scenario comparison is still planning-oriented and placeholder-aware.
- The new lineage summaries improve inspectability, but they do not imply verified pricing, engineering validity, or exhaustive field-level provenance.
- Takeoff snapshots remain transient and deferred.

## Recommended Next Step

- Extend provenance coverage more deeply into scenario, pathway, design, and home-model fields so the new comparison layer rests on stronger source lineage instead of sparse summaries.
