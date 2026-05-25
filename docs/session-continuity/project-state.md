# Project State

## Purpose

This document records the actual current state of the `residential-energy-planner` repo so future AI-assisted sessions can resume work without re-inferring architecture from partial context.

## Repo Status As Of 2026-05-24

- Monorepo structure is stable:
  - `apps/api`: FastAPI backend
  - `apps/web`: React/Vite frontend prototype with core editing workflows
  - `docs`: product, architecture, and continuity docs
- Canonical top-level continuity files now exist at:
  - `AGENTS.md`
  - `PROJECT_STATE.md`
  - `SESSION_HANDOFF.md`
  - `discovery-index.md`
  - `docs/PROJECT_OVERVIEW.md`
  - `docs/CURRENT_STATE.md`
  - `docs/NEXT_STEPS.md`
  - `docs/ARCHITECTURE.md`
  - `docs/DATABASE_SCHEMA.md`
  - `docs/API_CONTRACTS.md`
  - `docs/ACTIVE_TASKS.md`
  - `docs/SESSION_LOG.md`
  - `docs/philosophy/*`
  - `docs/adr/*`
  - `docs/handoffs/`
- Backend has completed Phase 2A persistence:
  - SQLite local database
  - SQLAlchemy ORM models
  - repository layer replacing the old in-memory seed repository
  - first-run database seeding
  - simple write endpoints added for future editable workflows
  - lightweight Alembic migration scaffold
  - `data_origin` separation metadata on persisted planning records
  - `/api/*` alias support with legacy route preservation
- Frontend has now entered Phase 2B with additive editable workflows layered on top of the existing read views.

## What Is Implemented

- Persistent account scaffolding with future-ready ownership fields
- Persistent homes, structures, panels, loads, designs, equipment locations, products, scenarios, takeoffs
- Persistent estimated pathways, load templates, and design goal presets
- Seed-backed demo mode loaded into SQLite on first startup
- Design advisor and AI context endpoints still compose deterministic placeholder outputs on top of persisted data
- Design advisor and AI context now include explicit trust visibility, planning completeness, and richer deterministic reasoning
- Design advisor, product library, transient takeoffs, and AI context now have initial provenance/source-lineage support
- Scenario comparison now uses persisted scenario records plus linked design completeness, pathway visibility/confidence, and additive lineage summaries
- Demo-vs-real separation is now explicit at the record level through `data_origin`, but not yet enforced through tenancy or permissions
- Editable frontend workflows now exist for:
  - home overview
  - structures
  - electrical panels
  - loads
  - load-template-driven load creation
  - equipment locations
  - estimated pathways
  - designs
  - scenarios
  - design equipment composition
- Selected-design takeoff generation now derives line items from current persisted design composition.
- Derived takeoffs remain intentionally transient and now surface explicit trust/placeholder messaging in the UI.
- Source documents, data provenance, and rule provenance now exist as first-pass backend structures, but coverage is still partial.
- Scenario comparison is no longer placeholder-only, but its lineage depth is still constrained by partial provenance coverage.
- Design status now acts as a lightweight planning maturity model, not an engineering approval state.
- A dedicated doctrine layer now exists under `docs/philosophy/` and `docs/adr/` to preserve strategic coherence across future implementation sessions.
- Restore now starts from a compact root discovery layer plus repo-local skills instead of requiring an immediate sweep across all detailed continuity and doctrine docs.

## What Is Not Implemented

- Authentication
- Billing or subscription enforcement
- Multi-tenant authorization
- NEC compliance engine
- Permitting workflows
- Product ingestion with verified manufacturer provenance
- exhaustive field-level provenance coverage
- DB migration tooling such as Alembic
- Change history, audit trail, or provenance ledger
- delete/archive workflows for editable records
- persisted takeoff snapshots

Note:
Alembic is now scaffolded, but migration discipline is still early-stage and not yet backed by a mature revision history strategy.

## Current Operating Model

- The product is still intentionally a planning prototype.
- Structured facts are authoritative.
- Rules and calculations should remain deterministic and inspectable.
- AI is a consumer of structured context and explanation contracts, not a source of facts.
- Design completeness is planning completeness only, not engineering completeness.
- Trust visibility is now a first-class UX layer, even though deep provenance and audit systems are still deferred.
- Verification status belongs to source documents; trust badges belong to current application presentation and should not be conflated.
- Philosophy and ADR documents remain durable deep references, but they are no longer mandatory startup reads for every session.

## Important Current Constraints

- The repo currently uses string IDs for seeded and persisted records. This is deliberate to preserve seed/demo continuity and keep frontend assumptions stable.
- SQLite is the local system of record for development.
- Current GET routes must be treated as compatibility-sensitive because the frontend already depends on them.
- `/api/*` aliases now exist, but legacy unprefixed routes remain active for compatibility.
- Current POST/PATCH routes are now exercised by the frontend for core planning entities.

## Current Database Facts

- DB path: `apps/api/data/residential_energy_planner.sqlite3`
- DB is initialized on FastAPI startup
- Seed routine only runs automatically when no home records exist
- Reseed flow exists via `python3 -m app.seed.cli reseed`

## Continuity Assumptions

- Future sessions should assume the database schema is the current system of record unless explicitly replaced.
- Future sessions should not assume undocumented product facts, code rules, or subscription semantics are implemented.
- If a later session changes API shapes, it must treat that as a compatibility event and document it immediately in this continuity system.
