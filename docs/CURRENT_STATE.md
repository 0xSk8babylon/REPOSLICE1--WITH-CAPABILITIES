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
- Load and estimated pathway GET contracts now include additive `provenance_summary` metadata, and the Home Model UI now surfaces source count, confidence, unverified fields, and lineage notes where available
- Planning-only design completeness scoring and design maturity/status explanations
- Expanded deterministic advisor reasoning using products, ecosystems, pathways, panel context, and backup/load signals
- Advisor architecture now includes a deterministic resilience recommendation-profile layer that expresses planning philosophies without exposing raw sizing math
- Recommendation profiles now include a first internal battery sizing estimate layer based on current backup-load modeling and profile posture
- Recommendation profiles now include a first internal solar sizing and recovery estimate layer based on recovery posture, low-solar assumptions, and battery-recovery planning
- Recommendation profile fit, battery guidance, and solar guidance now include additive inspectability metadata that exposes basis signals, estimated inputs, incomplete inputs, confidence posture, and partial-provenance warnings without exposing raw formulas
- Solar guidance now also applies a first coarse site-aware adjustment layer using recorded roof placement where available, fallback shading caution, coarse seasonal region posture, and install-path realism signals
- Solar guidance now also carries an explicit roof-readiness layer that distinguishes inferred placement realism, estimated roof-capacity posture, measured roof-geometry availability, and future usable-area support
- Recommendation outputs now also carry a preliminary panel/service architecture layer that classifies likely service posture and backup-architecture direction before inverter, smart-panel modifier, or generator sizing
- Expanded AI grounding context with trust state, completeness, maturity, ecosystem mixing, and pathway confidence
- Source-document, data-provenance, and rule-provenance foundation for products, assumptions, internal rules, and transient takeoff reasoning
- Scenario comparison now consumes linked design completeness, pathway signals, trust warnings, and source-lineage summaries instead of returning a placeholder-only comparison shell
- A repo-level doctrine layer now exists under `docs/philosophy/` and `docs/adr/` to preserve strategic coherence across future sessions
- A compact root discovery layer and repo-local skills now exist so restore can start without a mandatory full-doc sweep

## Still Incomplete

- Verified product ingestion and provenance
- Exhaustive field-level provenance coverage across scenarios, pathways, designs, and home-model facts
- Existing local databases may need reseeding or manual provenance entry to show the new seeded pathway lineage examples
- Recommendation profiles and sizing slices are now more inspectable, but they still remain planning guidance only and are not yet connected to deeper site-aware recommendation logic
- Battery sizing now has a first numeric planning layer, but richer battery/site constraints and product-specific sizing are still not implemented behind the profile system
- Solar sizing now has a first numeric planning layer plus a coarse site-aware adjustment stage, but richer seasonal modeling, roof-capacity realism, and more grounded recovery inputs are still incomplete behind the profile system
- Roof-capacity certainty is now structurally separated from measured geometry, but no true roof-area, roof-plane, polygon, or usable-area calculations exist yet
- Panel/service architecture is now structurally separated from later inverter, smart-panel modifier, and generator layers, but it remains a planning posture rather than a validated electrical design
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
- Load and pathway trust views are now more grounded in structured provenance, but most design, home, and scenario fields still lack equivalent field-level coverage.
- Recommendation profiles now formalize resilience philosophies, but battery/solar/autonomy sizing math still needs a deeper deterministic implementation layer behind them.
- Battery planning ranges are now present, but they remain intentionally planning-only and should not be treated as final engineered storage sizing.
- Solar planning ranges are now present, but they remain intentionally planning-only and should not be treated as final engineered production sizing.
- The new solar site-aware layer uses only coarse internal postures and fallback caution defaults; it is not a production model, roof-fit model, or shading analysis.
- The new roof-readiness layer is architectural scaffolding for future measured-geometry inputs; it does not imply that scaled or traced roof data already exists.
- The new panel/service layer uses current panel, service, load-grouping, and pathway signals only; it does not confirm busbar compliance, transfer topology, or final backup hardware architecture.
- Recommendation inspectability is now broader, but it still depends on deterministic planning signals and partial provenance rather than verified engineering inputs or full field-level lineage.
