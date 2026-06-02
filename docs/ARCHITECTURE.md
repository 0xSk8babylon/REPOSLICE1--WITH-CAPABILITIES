# Architecture

## Monorepo Shape

- `apps/api`: FastAPI backend, persistence, rules/services, seed runtime
- `apps/web`: React/Vite frontend, live planning UI
- `docs`: product vision, architecture, continuity, handoffs

## Architectural Boundaries

- Property facts: homes, buildings, panels, loads
- Design facts: energy system designs, design equipment, scenarios, estimated pathways
- Product facts: equipment products and future ingestion metadata
- Rule outputs: compatibility issues and advisor explanations
- Estimate artifacts: takeoff requests and line items
- AI context: grounded summaries assembled from persisted structured state

## Residential Energy Twin Governance

- `docs/architecture/ResidentialEnergyTwinContractV1.md` defines the Residential Energy Twin aggregate contract as documentation/governance doctrine only. `docs/architecture/RESIDENTIAL_ENERGY_TWIN_CONTRACT_V1.md` is retained as a compatibility pointer.
- `docs/architecture/TopologyLifecycleDomains.md` defines topology lifecycle domain boundaries as documentation/governance doctrine only.
- `docs/architecture/ContinuityDomain.md` defines the Residential Energy Twin Continuity Domain for preserving lifecycle history across ownership, contractor, infrastructure, utility, safety, permission, provenance, equipment, and software/platform changes as documentation/governance doctrine only.
- `docs/architecture/SafetyDomain.md` defines the Residential Energy Twin Safety Domain for persistent, provenance-bearing, permissioned safety context as documentation/governance doctrine only.
- `docs/architecture/InteroperabilityDomain.md` defines the Residential Energy Twin Interoperability Domain for shared cross-industry semantic interpretation of Twin information as documentation/governance doctrine only.
- `docs/architecture/EcosystemParticipantBoundaryMatrix.md` consolidates participant-purpose boundaries for ecosystem actors before future Exchange Domain work as documentation/governance doctrine only; it is not a new Twin domain.
- `docs/architecture/PermissionPlacement.md` defines where homeowner-governed permission concepts attach to the twin as documentation/governance doctrine only.
- `docs/architecture/ProvenancePlacement.md` defines where source lineage, evidence, confidence, verification, and authority metadata attach to the twin as documentation/governance doctrine only.
- `docs/architecture/ViewContracts.md` defines actor-specific, permission-filtered, provenance-preserving view-contract expectations as documentation/governance doctrine only.
- `docs/architecture/SolarMarketProductIntelligenceGrounding.md` defines Phase 2 placement boundaries for future solar production, market/economic, and verified product intelligence grounding as documentation/governance doctrine only.
- `docs/architecture/Phase3TwinIntelligenceLayer.md` defines the governing Phase 3 derived/advisory Twin Intelligence planning layer as documentation/governance doctrine only.
- `docs/architecture/StructuredSystemReasoningGraph.md` defines the Phase 3 derived/advisory graph planning layer for topology-aware reasoning as documentation/governance doctrine only.
- `docs/architecture/ScenarioIntelligence.md` defines the Phase 3 derived/advisory scenario comparison planning layer as documentation/governance doctrine only.
- `docs/architecture/InfrastructureSimulation.md` defines the Phase 3 derived/advisory infrastructure simulation planning layer as documentation/governance doctrine only.
- `docs/architecture/WhatIfAnalysis.md` defines the Phase 3 derived/advisory what-if analysis planning layer as documentation/governance doctrine only.
- `docs/architecture/DependencyImpactPropagation.md` defines the Phase 3 derived/advisory integrity layer for stale outputs, dependency invalidation, recalculation, re-grounding, re-review, provenance impacts, confidence impacts, safety impacts, continuity impacts, and participant-view impacts as documentation/governance doctrine only; it is not a new Twin domain.
- `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md` plans the first possible runtime boundary as docs-only design work; it recommends `home_id` only as a temporary premise-scoped planning-context anchor if Matt later approves implementation and reserves `twin_id` for a future approved canonical aggregate.
- None of these documents approve schema changes, migrations, API changes, runtime behavior changes, exchange mechanisms, ownership transfer, protocols, standards, legal ownership, title ownership, contractual rights, safety approval, field verification, permission enforcement, utility authority, operational control, or a canonical `ResidentialEnergyTwin` model.

## Persistence Architecture

- SQLAlchemy ORM models in `apps/api/app/core/models.py`
- Session and engine setup in `apps/api/app/core/database.py`
- Repository access in `apps/api/app/core/repository.py`
- SQLite local DB in `apps/api/data/residential_energy_planner.sqlite3`
- First-run seed loading in `apps/api/app/seed/runtime.py`

## Frontend Architecture

- Shared API client in `apps/web/src/lib/api.js`
- Query helpers in `apps/web/src/lib/useApiQuery.js`
- Mutation helpers in `apps/web/src/lib/useApiMutation.js`
- Workflow pages in `apps/web/src/pages/*`
- Lightweight shared form components in `apps/web/src/components/form/*`

## API Stability Policy

- Preserve current GET contracts unless frontend and docs change together.
- Prefer additive evolution.
- Prefer `/api/*` for clients.
- Reserve `/api/v1` for the first intentional breaking version boundary.

## Architectural Constraints

- Do not collapse structured facts, rules, calculations, and AI into one layer.
- Do not treat placeholder values as engineering truth.
- Do not introduce auth/billing-driven complexity before planning workflows are stable.
