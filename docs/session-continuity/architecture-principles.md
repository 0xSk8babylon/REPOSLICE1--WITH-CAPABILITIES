# Architecture Principles

## Core Principles

1. Structured facts before AI.
2. Deterministic rules before narrative explanations.
3. Persistent house context before one-off proposals.
4. Stable API contracts before internal refactors.
5. Extensibility over premature enterprise complexity.

## Boundary Rules

- Property facts belong in persisted domain entities.
- Product facts belong in structured product records.
- Compatibility judgments belong in explicit rule outputs.
- Scoring logic belongs in deterministic services.
- Explanations compose facts, rule results, and calculations.
- AI context is assembled from authoritative system state.

## Architectural Non-Goals For The Current Phase

- Do not turn the backend into a generic agentic system.
- Do not treat placeholder scoring as engineering truth.
- Do not let frontend convenience drive domain collapse.
- Do not add auth/billing/deployment complexity before editable planning workflows are stable.

## Ingestion Philosophy

- Product and system facts should enter the platform through explicit structured ingestion, not through prompt memory.
- Seed data exists for demo continuity, not for factual authority.
- Future verified product ingestion must preserve source lineage, document confidence, and distinguish placeholder values from verified values.

## Persistence Principles

- Persistence should preserve planning state across sessions and account contexts.
- Ownership should be modeled early enough to avoid later rewrites, but enforcement can be deferred.
- Seed/demo continuity must remain available for first-run environments.
- Data mutations should become more deliberate over time, not more freeform.

## Provenance Philosophy

The repo does not yet implement a full provenance system. The target posture is:

- every factual product record should eventually know its source
- every derived rule output should be reproducible from structured inputs
- every future AI explanation should be traceable to a persisted context payload

Until that exists, sessions must explicitly avoid overstating certainty.

## Versioning And Idempotency Principles

- API compatibility for existing GET routes is currently a hard constraint.
- Prefer additive API evolution and dual-route compatibility before introducing versioned breaks.
- `/api/*` is the preferred forward path; `/api/v1` is reserved for future explicit versioning.
- Seed routines must be idempotent for normal startup and destructive only when explicitly invoked through reseed flows.
- Future migrations should be additive-first when possible.
- Continuity docs should be updated when architecture or contracts materially change.

## Demo Versus Real Data Principle

- Demo continuity is allowed and useful.
- Demo records must be distinguishable from real user-created or imported records.
- `data_origin` is now the minimum separation contract, not the final governance model.
- Future sessions must not treat `demo_seed` records as production-grade truth.
