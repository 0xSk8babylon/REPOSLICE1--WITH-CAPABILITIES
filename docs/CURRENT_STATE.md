# Current State

## Snapshot Date

2026-05-25

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
- Recommendation outputs now also include an additive deterministic backup-load selection summary that makes current backup scope, recorded-load coverage, outage posture, confidence posture, fallback posture, and planning gaps explicit before panel/service, battery, or solar guidance is interpreted
- Solar guidance now also applies a first coarse site-aware adjustment layer using recorded roof placement where available, fallback shading caution, coarse seasonal region posture, and install-path realism signals
- Solar guidance now also carries an explicit roof-readiness layer that distinguishes inferred placement realism, estimated roof-capacity posture, measured roof-geometry availability, and future usable-area support
- Recommendation outputs now also carry a preliminary panel/service architecture layer that classifies likely service posture and backup-architecture direction before inverter, smart-panel modifier, or generator sizing
- Panel/service guidance now also carries an additive architecture-consistency check that keeps broader backup direction bounded by recorded outage posture and design-goal intent
- Recommendation profiles now also carry an additive architecture-fit tradeoff layer that explains how current equipment mix, outage posture, panel/service direction, and architecture-consistency posture pull each profile narrower or broader
- Recommendation outputs now also carry an additive inverter/system architecture layer that explains likely AC-coupled vs hybrid posture, inverter-path suitability, battery/solar/generator coexistence assumptions, expansion direction, and planning-only system-consistency posture
- Recommendation outputs now also carry an additive current-home-energy-architecture layer that classifies current solar/inverter topology, preserves existing-vs-proposed equipment boundaries, and explains outage-solar, battery-retrofit, expansion, and generator-coexistence implications at planning level
- Recommendation outputs now also carry an additive structured system reasoning graph that traces deterministic dependencies between recorded load grouping, backup scope, panel/service posture, inverter/system architecture, and the recommended battery/solar posture
- The Design Advisor now surfaces panel/service planning-direction confidence, trust framing, and inspectability inputs more explicitly instead of showing only the high-level direction
- The Design Advisor now also surfaces profile-level architecture-fit tradeoffs and warnings beside each recommendation profile card
- The Design Advisor now also surfaces inverter/system architecture direction, coexistence assumptions, confidence, and inspectability alongside the panel/service layer
- The Design Advisor now also surfaces a current home energy architecture panel that distinguishes existing microinverter/string/hybrid conditions from proposed battery, generator, smart-panel, and service-upgrade assumptions
- Seeded advisor panel/service outputs now have narrow backend regression coverage for the current demo designs
- Expanded AI grounding context with trust state, completeness, maturity, ecosystem mixing, and pathway confidence
- Source-document, data-provenance, and rule-provenance foundation for products, assumptions, internal rules, and transient takeoff reasoning
- Scenario comparison now consumes linked design completeness, pathway signals, trust warnings, and source-lineage summaries instead of returning a placeholder-only comparison shell
- A repo-level doctrine layer now exists under `docs/philosophy/` and `docs/adr/` to preserve strategic coherence across future sessions
- A compact root discovery layer and repo-local skills now exist so restore can start without a mandatory full-doc sweep

## Still Incomplete

- Verified product ingestion and provenance
- Exhaustive field-level provenance coverage across scenarios, pathways, designs, and home-model facts
- Existing local databases may need reseeding or manual provenance entry to show the new seeded pathway lineage examples
- Existing local databases may also need reseeding to surface the new current-home-energy-architecture, backup-architecture-consistency, profile-architecture-fit, inverter/system-architecture, and structured-system-reasoning-graph rule provenance records
- Recommendation profiles and sizing slices are now more inspectable, and the new reasoning graph makes their dependency chain explicit, but they still remain planning guidance only and are not yet connected to deeper site-aware recommendation logic
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
- The panel/service UI now makes its confidence posture more visible, but that confidence still reflects deterministic planning evidence rather than electrical verification.
- The new backup-load selection layer prevents silent scope inflation and now distinguishes critical-load, partial-home, and whole-home candidates from recorded load coverage, but it still depends on recorded essential/preferred tagging rather than circuit-level load studies or outage sequencing.
- The new architecture-consistency check narrows backup-direction claims when the design goal outruns recorded load grouping, but it remains a planning-only alignment check rather than an engineering validation.
- The new profile architecture-fit layer explains tradeoffs around current equipment mix and backup-path direction, but it remains a planning-only interpretation layer rather than a final architecture approval.
- The new inverter/system architecture layer explains likely AC-coupled vs hybrid direction and coexistence posture from current records, but it remains a planning-only architecture interpretation rather than inverter sizing, interconnection design, or compliance validation.
- The new current-home-energy-architecture layer explains what the home appears to have today, but it still depends on recorded role markers and product signals rather than a verified field inventory.
- The new structured reasoning graph improves advisor traceability, but it is an additive explanation layer for the recommended profile only rather than a generalized whole-system simulation graph.
- Recommendation inspectability is now broader, but it still depends on deterministic planning signals and partial provenance rather than verified engineering inputs or full field-level lineage.
