# Topology Lifecycle

## Purpose

Topology continuity tracks how the home energy system changes over time without collapsing current state, proposed state, and operational truth.

For the Phase 2 topology lifecycle domain architecture note, see `docs/architecture/TopologyLifecycleDomains.md`. That document is docs-only and does not approve runtime topology graphs, lifecycle event logs, schema, API, utility, telemetry, or operational-control implementation.

## Lifecycle Stages

1. Recorded current state
2. Proposed planning pathway
3. Saved scenario revision
4. Contractor-reviewed planning package
5. Field-verified topology
6. Operational topology
7. Future expansion or replacement state

Only stages 1 through 3 are currently represented in the product.

## Current Capabilities

- Current solar/inverter topology is classified from recorded equipment roles and product signals.
- Existing-vs-proposed equipment posture is visible in advisor outputs.
- Scenario revisions preserve compact planning-state snapshots.
- Structured reasoning graph links current topology, backup scope, panel/service posture, inverter architecture, and battery/solar posture.

## Gaps

- No field-verified topology model.
- No topology event log.
- No DER operational state.
- No utility interconnection state.
- No lifecycle graph that links revisions, installed equipment, decommissioning, and future upgrades.

## Boundary Rule

Topology intelligence may explain planning relationships. It must not imply actual installed, commissioned, dispatchable, or utility-approved state until future authority layers exist.
