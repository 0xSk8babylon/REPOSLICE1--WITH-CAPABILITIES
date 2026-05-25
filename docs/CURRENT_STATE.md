# Current State

## Snapshot Date

2026-05-24

## Platform State

- Backend persistence is live with SQLite + SQLAlchemy.
- First-run demo seeding is active and reseeding is supported.
- Core frontend planning pages fetch live backend data.
- Core living house model workflows are editable from the frontend.
- `/api/*` is available and preferred, while legacy routes remain supported.

## Implemented Systems

- Account scaffolding with future ownership and subscription fields
- Homes, buildings, panels, loads, designs, equipment locations, products, scenarios, takeoffs, estimated pathways, load templates, and design goal presets
- Repository-backed CRUD for core planning entities
- Alembic baseline scaffold for local schema evolution
- `data_origin` markers for demo-vs-real separation
- Frontend editing for homes, structures, panels, loads, load-template-driven loads, designs, scenarios, equipment locations, and estimated pathways
- Frontend editing for design equipment and product assignments
- Derived takeoff structure from persisted design equipment composition
- Trust/provenance visibility badges across products, loads, pathways, scenarios, takeoff views, and advisor outputs
- Planning-only design completeness scoring and design maturity/status explanations
- Expanded deterministic advisor reasoning using products, ecosystems, pathways, panel context, and backup/load signals
- Expanded AI grounding context with trust state, completeness, maturity, ecosystem mixing, and pathway confidence
- Source-document, data-provenance, and rule-provenance foundation for products, assumptions, internal rules, and transient takeoff reasoning
- Scenario comparison now consumes linked design completeness, pathway signals, trust warnings, and source-lineage summaries instead of returning a placeholder-only comparison shell
- A repo-level doctrine layer now exists under `docs/philosophy/` and `docs/adr/` to preserve strategic coherence across future sessions
- A compact root discovery layer and repo-local skills now exist so restore can start without a mandatory full-doc sweep

## Still Incomplete

- Verified product ingestion and provenance
- Exhaustive field-level provenance coverage across scenarios, pathways, designs, and home-model facts
- Audit trail and change history
- Delete/archive workflows
- Auth and billing enforcement
- Persisted/versioned takeoff snapshots remain intentionally deferred

## Notable Documentation Drift Resolved This Session

- The continuity system now has canonical top-level memory files.
- README language should reflect that the frontend is no longer read-only.
- Restore procedure is now separated from project-state memory, with doctrine and historical docs moved out of the mandatory startup path.

## Stability Notes

- Existing GET response shapes should be treated as compatibility-sensitive.
- String IDs remain intentional for seed continuity and frontend stability.
- Placeholder scores, estimates, and compatibility logic remain non-authoritative.
- Derived takeoffs remain transient by design in the current phase.
- Verification status and visible trust badges are related, but they are not the same contract.
- Scenario comparison is now more inspectable, but it still depends on planning heuristics and partial provenance rather than verified estimating inputs.
