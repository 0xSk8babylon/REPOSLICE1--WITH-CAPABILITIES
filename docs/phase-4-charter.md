# Phase 4 Charter: Trust / Provenance Maturity and Readiness Normalization

## Summary

Phase 4 is defined as Trust / Provenance Maturity and Readiness Normalization. This charter defines the Phase 4 boundary before implementation and does not approve runtime work.

## Product Purpose

Phase 4 should make Phase 3 outputs easier to trust, compare, audit, and reuse by normalizing how readiness posture, provenance basis, missing data, unsafe assumptions, confidence, limitations, and deferred authority boundaries are represented across existing derived intelligence surfaces.

Phase 4 builds on Phase 3A through Phase 3O as its source foundation. Phase 3 is closed. Phase 4 has not been implemented.

## First Safe Implementation Candidate

The first safe Phase 4 implementation candidate, after a separate assessment and Matt-approved implementation boundary, is a read-only trust/provenance/readiness normalization slice over existing Phase 3 outputs.

That candidate should focus on consistency and inspectability only:

- normalize existing readiness and provenance posture language
- preserve source basis and limitation visibility
- preserve missing-data and unsafe-assumption labels
- preserve deterministic same-input/same-output behavior
- preserve existing endpoint and frontend compatibility unless Matt separately approves a contract change

The first step before any implementation remains assessment-only: inventory the current Phase 3 outputs and identify the smallest normalization surface.

## Allowed Implementation Categories

Only after separate approval, Phase 4 may include:

- docs-only assessment of Phase 3 trust, provenance, readiness, confidence, limitation, and deferred-boundary surfaces
- additive read-only normalization of existing trust/provenance/readiness metadata
- additive backend verification for deterministic, traceable, same-input/same-output behavior
- continuity updates that record exactly what was normalized and what remains deferred
- narrowly scoped compatibility-preserving contract documentation when needed

## Forbidden Outputs

Phase 4 does not approve:

- proposals, quotes, packages, bids, sales copy, or proposal generation
- pricing, savings, payback, incentive, economic, tariff, or financial reasoning
- product recommendations, product selection, product ranking, procurement, vendor scraping, marketplace behavior, supplier integrations, or compatibility engines
- scenario comparison execution, scenario simulation, what-if analysis, optimization, ranking, best-option selection, calculated change analysis, impact propagation, stale-state persistence, recalculation, or invalidation engines
- frontend expansion, new user workflows, portals, exports, scoped exports, partner APIs, utility sharing, or permission enforcement
- auth, RBAC, ABAC, privacy enforcement, encryption, telemetry governance, security hardening, utility participation, DERMS, dispatch, or operational control
- persistence, migrations, canonical Twin runtime identity, `twin_id`, graph database, graph engine, canonical topology tables, or new source-of-truth models
- NEC automation, permitting, stamped-engineering conclusions, safety approval, field verification approval, utility approval, interconnection approval, or compliance claims

## Verification Requirements

Any future Phase 4 implementation must include:

- pre-implementation assessment confirming the exact Phase 3 surfaces touched
- `git status --short` before work
- focused backend tests for any runtime normalization
- full backend discovery test run when shared services, schemas, routes, or derived intelligence behavior are touched
- deterministic same-input/same-output coverage for normalized outputs
- traceability checks proving source basis, missing data, unsafe assumptions, limitations, and deferred boundaries remain visible
- `git diff --check`
- `git diff --cached --check` before commit
- final `git status --short`

Docs-only Phase 4 work does not require backend tests, but must verify that only docs and continuity files changed.

## Continuity Requirements

Phase 4 sessions must update the compact discovery layer only when state materially changes:

- `PROJECT_STATE.md`
- `discovery-index.md`
- a dated `docs/handoffs/*phase-4*` handoff

Continuity updates must distinguish:

- Phase 3 closed and serving as the source foundation
- Phase 4 chartered but not yet implemented
- Phase 4 assessment complete versus Phase 4 implementation approved
- approved implementation slices versus deferred boundaries
- latest recorded backend verification versus docs-only verification

## Assessment-Before-Implementation Rule

No Phase 4 runtime work may begin from this charter alone. Each Phase 4 implementation slice requires:

1. assessment of affected Phase 3 outputs and trust/provenance/readiness fields
2. a narrow proposed implementation boundary
3. Matt approval for that boundary
4. focused implementation within the approved files and behavior
5. verification and continuity closeout

## Current State

- Phase 3A through Phase 3O are complete.
- Latest Phase 3 closeout commit before this charter: `aebd4e8`.
- Latest recorded backend verification remains `python3 -m unittest discover tests` with 129 tests passing.
- Phase 4 readiness assessment is complete as read-only context.
- This charter defines Phase 4 boundaries only.
- Phase 4 runtime implementation has not started.
