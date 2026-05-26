# Current Roadmap

## Completed

### Phase 1

- Monorepo scaffold
- FastAPI backend domain layout
- React/Vite frontend shell
- Seed-based planning prototype
- Product and architecture docs

### Phase 2A

- SQLite persistence layer
- SQLAlchemy ORM models
- repository-backed data access
- startup DB initialization and first-run seed loading
- write endpoints for key planning domains
- persisted account scaffolding without auth
- lightweight Alembic migration scaffold
- demo-vs-real `data_origin` hardening
- basic API versioning policy with `/api/*` aliases and `/api/v1` reserved

## In Progress By Implication

Phase 2B is functionally complete enough for editable planning workflows, and the repo has now moved into a Phase 2D trust-visibility and advisor-intelligence layer on top of that foundation.

## Next Target

### Phase 2B

- connect frontend forms to the new POST/PATCH endpoints
- add lightweight editable workflows for:
  - homes
  - structures
  - panels
  - loads
  - load-template-driven load creation
  - designs
  - scenarios
  - equipment locations
  - estimated pathways
- keep auth deferred
- keep engineering logic shallow and deterministic

Status:

- completed for the entities above
- completed for design equipment composition and richer product-driven editing
- takeoff derivation is now design-driven but still transient and placeholder-priced

## After Phase 2B

### Likely Next Steps

- deepen provenance/source-lineage structure behind visible trust states
- more transparent scenario scoring
- verified product ingestion and provenance fields
- migration strategy becoming normal practice instead of scaffold-only

## Phase 2D

- trust visibility layer across major planning surfaces
- planning-only design completeness reasoning
- richer deterministic advisor issues using products, ecosystems, panels, loads, pathways, and siting
- more structured AI grounding payloads
- explicit transient-takeoff posture preserved

## Phase 2E

- source-document, data-provenance, and rule-provenance foundation
- read-oriented provenance endpoints
- provenance summaries visible in product, advisor, takeoff, and AI context surfaces
- scenario comparison now consumes completeness and provenance-oriented lineage summaries
- verification-status distinction documented separately from trust badges
- load and estimated-pathway records now expose additive provenance summaries in operational GET contracts
- deterministic recommendation profiles now exist in the advisor layer as a precursor to deeper sizing rules
- battery sizing is now the first numeric planning layer behind the recommendation profiles
- solar sizing and recovery posture are now the second numeric planning layer behind the recommendation profiles
- recommendation profile fit plus battery/solar guidance now expose inspectability metadata so the advisor can explain basis and uncertainty without exposing internal formulas
- solar sizing now also includes a coarse site-aware adjustment layer before any future inverter sizing or production modeling
- solar sizing now also includes a roof-readiness layer so future GIS/maps/traced-geometry inputs can plug into the current planning architecture instead of replacing it
- recommendation outputs now also include a preliminary panel/service architecture layer so future inverter, smart-panel modifier, and generator layers can plug into a stable backup-architecture posture
- backup-load selection now also exposes outage posture, recorded-load coverage, and planning-only confidence so later architecture-fit slices inherit a narrower and more inspectable scope model
- panel/service guidance now also includes an additive architecture-consistency check so broader backup direction does not outrun recorded outage posture or design-goal intent
- recommendation profiles now also include profile-level architecture-fit tradeoffs so current equipment mix and backup-path direction can shape fit without changing sizing formulas
- recommendation outputs now also include an additive inverter/system architecture layer so AC-coupled vs hybrid posture, coexistence assumptions, and expansion direction are explicit before final inverter sizing
- recommendation outputs now also include an additive current-home-energy-architecture layer so existing microinverter/string/hybrid/unknown solar topology is explicit before future architecture guidance is interpreted
- recommendation outputs now also include an additive structured system reasoning graph so current advisor dependencies are inspectable before deeper site-aware reasoning is added
- the Design Advisor UI now uses that advisor spine more explicitly through workspace-style grouping and progressive disclosure rather than a flat panel stack
- the Design Advisor UI now also renders compact architecture relationship maps and dependency-chain visuals on top of that advisor spine so current state and deterministic planning relationships are easier to scan without changing contracts
- the Design Advisor UI now also renders a planning-pathway comparison workspace on top of the existing profile outputs so pathway tradeoffs are easier to scan without introducing a new recommendation engine

## Explicitly Deferred

- user login/session management
- billing and Stripe integration
- production deployment hardening
- NEC automation
- permitting workflows
- conversational AI design agent with write authority
- full provenance tracking
- full audit/change history

## Continuity Layer Status

- canonical repo-level memory files are now in place
- compact root discovery files now route restore before any detailed continuity sweep
- repo-local skills now capture project-specific memory routing and guardrails
- strategic doctrine files now exist under `docs/philosophy/`
- core architecture decisions are now captured under `docs/adr/`
- future sessions should update the root discovery files plus only the detailed continuity files affected by the change
