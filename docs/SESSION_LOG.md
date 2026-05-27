# Session Log

## 2026-05-23

- Reconstructed repo state from `docs/session-continuity/*`.
- Validated that the implementation already includes SQLite persistence, seed/reseed flows, `/api/*` aliases, and Phase 2B editable frontend workflows.
- Identified a continuity gap: the canonical top-level memory files requested for orchestration did not exist yet.
- Identified documentation drift: README still described the frontend as read-only even though editing workflows are live.
- Established the top-level continuity layer and handoff structure so future sessions can restore context without relying on chat history.
- Added dedicated `DesignEquipment` CRUD routes under `/api/designs/{design_id}/equipment`.
- Extended the System Design Builder UI to assign products, quantities, system roles, and locations to persisted designs.
- Replaced selected-design takeoff generation so line items derive from current design composition instead of the seeded placeholder request.
- Added a Phase 2D trust-visibility layer so placeholder, demo, user-entered, verified, and derived states are visibly distinct in core planning views.
- Added deterministic planning completeness scoring and richer advisor reasoning tied to products, ecosystems, pathways, panels, and backup/load signals.
- Expanded AI grounding context to include trust state, design maturity, completeness, ecosystem mixing, and pathway-confidence signals.
- Kept derived takeoffs transient and explicitly documented that decision in both UI messaging and continuity docs.
- Added Phase 2E provenance/source-lineage tables, read endpoints, and seeded examples for source documents, data provenance, and internal rule provenance.
- Connected provenance summaries into product library records, advisor issue displays, transient takeoff displays, and AI grounding context.
- Documented the difference between verification status and trust badges, while keeping placeholder and derived states explicit.
- Replaced placeholder-only scenario comparison output with deterministic comparison summaries that incorporate linked design completeness, pathway signals, trust warnings, and source-lineage summaries.
- Added a repo-level doctrine layer under `docs/philosophy/` and `docs/adr/` so future sessions can restore product philosophy, non-goals, trust posture, UX principles, and durable architecture decisions before making changes.

## 2026-05-24

- Migrated repo restore flow to a layered skills-based operating model rooted in compact discovery files instead of mandatory full-doc startup sweeps.
- Added root discovery files: `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`.
- Added repo-local skills for repo memory mapping and project guardrails under `.codex/skills/`.
- Added `docs/session-continuity/continuity-workflow.md` as the canonical continuity procedure.
- Reduced duplicated restore logic by converting `docs/session-continuity/session-restore-template.md` into a compatibility stub and narrowing `persistence-agent-plan.md` to a maintenance role.
- Added additive `provenance_summary` metadata to load and estimated-pathway API responses.
- Seeded first-pass structured pathway provenance records and surfaced load/pathway lineage details in the Home Model UI.
- Preserved compatibility and planning-only trust boundaries by keeping the change additive and exposing missing lineage honestly when records are absent.
- Added a deterministic resilience recommendation-profile model to the advisor layer with four philosophies: Critical / Efficient, Balanced, Conservative, and Premium / Future-Ready.
- Kept profile outputs additive and planning-only, with explicit scope notes and rule provenance instead of exposed engineering coefficients or certainty inflation.
- Added the first internal battery sizing rule layer behind each recommendation profile.
- Recommendation profiles now derive planning-only battery energy need, autonomy range, usable capacity range, reserve posture, future growth margin, and recommended battery capacity range without exposing raw formulas.
- Added the first internal solar sizing and recovery rule layer behind each recommendation profile.
- Recommendation profiles now derive planning-only solar range guidance, recovery posture, low-solar resilience notes, and simple battery-recovery relationship guidance without exposing raw production math.
- Added an additive inspectability/provenance layer for selected recommendation profiles plus battery and solar guidance.
- Recommendation outputs now expose basis signals, estimated inputs, incomplete inputs, confidence posture, partial-provenance warnings, and explicit rule provenance without exposing internal sizing formulas.
- Added a first coarse site-aware solar adjustment layer behind the existing profile-backed solar planning range.
- Solar guidance now uses recorded roof placement where available plus fallback shading caution, coarse seasonal region posture, and install-path realism signals to adjust the planning range without introducing PVWatts or inverter sizing.
- Added an explicit roof-readiness architecture layer to solar guidance.
- Solar payloads now distinguish inferred placement realism, estimated roof-capacity posture, measured geometry status, and future geometry-source placeholders without claiming measured roof area already exists.
- Added a preliminary panel/service architecture layer to recommendation outputs.
- Recommendation payloads now classify likely panel/service posture, panel/service upgrade caution, backup-architecture suitability, smart-panel readiness, and generator-integration readiness before inverter or generator sizing exists.

## 2026-05-25

- Added the global `stabilization-before-feature-expansion` skill in the separate `~/.codex/global-skills` repo.
- Added project governance skills for runtime invariants, provenance rules, and load-selection doctrine under `.codex/skills/`.
- Refined the recommendation service so backup-load selection is explicit and deterministic instead of silently falling through to broad backup scope.
- Added additive `backup_load_selection` API output and surfaced it in the Design Advisor UI.
- Battery, solar, and panel/service guidance now consume the explicit selected backup scope and expose planning-gap warnings when broader backup ambition is not actually recorded in load grouping.
- Added a seeded internal rule provenance record for deterministic backup-load selection.
- Verified the refinement with `python3 -m compileall apps/api/app` and `npm run build` in `apps/web`.
- Stabilized the Design Advisor panel/service card so it shows explicit planning-only trust framing, confidence posture, and inspectability inputs.
- Added minimal backend regression coverage for seeded panel/service advisor outputs on `design_001` and `design_002`.
- Verified the stabilization with `python3 -m unittest discover -s tests -p 'test_*.py'`, `python3 -m compileall apps/api/app`, and `npm run build` in `apps/web`.
- Stabilized backup-scope modeling by adding explicit outage-posture classification, recorded-load coverage, and planning-only backup-scope confidence to the recommendation output.
- Refined panel/service architecture assumptions so partial-home and whole-home direction now respect the explicit outage posture instead of only a broad backup-scope boolean.
- Added an additive backup-architecture consistency check that narrows architecture direction when design-goal ambition outruns recorded load grouping.
- Surfaced backup-scope confidence/provenance and architecture-consistency output in the Design Advisor UI.
- Expanded backend regression coverage to include whole-home-goal fallback and whole-home-candidate boundary cases.
- Verified the stabilization with `python3 -m unittest discover -s tests -p 'test_*.py'`, `python3 -m compileall app`, and `npm run build` in `apps/web`.
- Added a deterministic inverter/system architecture layer that explains AC-coupled vs hybrid posture, pathway suitability, coexistence assumptions, expansion direction, and planning-only system consistency.
- Fully wired the profile-architecture-fit layer so recommendation profiles now incorporate current inverter/system posture in addition to equipment mix, outage posture, and panel/service direction.
- Surfaced inverter/system architecture confidence, inspectability, and consistency output in the Design Advisor UI.
- Added seeded rule provenance for `recommendation.inverter_system_architecture_v1` and expanded backend regression coverage for the new inverter/system architecture states.
- Verified the architecture reasoning layer with `python3 -m unittest discover -s tests -p 'test_*.py'`, `python3 -m compileall app`, and `npm run build` in `apps/web`.
- Added an additive structured system reasoning graph to recommendation outputs so the recommended profile now exposes inspectable dependencies between recorded load grouping, backup scope, panel/service posture, inverter/system architecture, and battery/solar posture.
- Added seeded rule provenance for `recommendation.system_reasoning_graph_v1` and surfaced the reasoning graph in the Design Advisor UI with planning-only dependency trace framing.
- Expanded backend regression coverage to lock the seeded reasoning-graph nodes and dependency edges for `design_001` and `design_002`.
- Verified the reasoning-graph foundation with `python3 -m unittest discover -s tests -p 'test_*.py'`, `python3 -m compileall app`, `npm run build` in `apps/web`, and `git diff --check`.
- Added an additive current-home-energy-architecture layer that classifies existing solar/inverter topology, preserves existing-vs-proposed equipment state, and explains outage-solar, battery-retrofit, expansion, and generator-coexistence implications at planning level.
- Updated seeded design data so `design_001` now exercises an existing microinverter solar plus proposed battery retrofit path, while `design_002` remains proposed-only and preserves current-state unknowns.
- Threaded current-state topology into future inverter/system reasoning and the structured reasoning graph so the advisor distinguishes existing-home architecture from future recommendations.
- Verified the topology-modeling milestone with `python3 -m unittest discover -s tests -p 'test_*.py'`, `python3 -m compileall app`, `npm run build` in `apps/web`, and `git diff --check`.
- Reorganized the Design Advisor UI into clearer workspace sections for current state, existing-vs-proposed system posture, recommendation path, and reasoning/evidence.
- Moved deeper inspectability, provenance, and missing-input detail behind progressive disclosure so the default page reads like a planning workspace instead of a flat stack of peer panels.
- Reduced local page duplication by introducing small helper render components inside the Design Advisor page without changing advisor logic or API contracts.
- Verified the UI architecture foundation with `npm run build` in `apps/web` and `git diff --check`.
- Added compact card-and-lane visualizations for current-home architecture and structured reasoning dependencies so the Design Advisor reads more like an explainable energy-planning workspace than a text-only panel stack.
- Kept the visualization layer frontend-only and deterministic by deriving it from existing advisor contracts without recomputing backend reasoning in the client.
- Verified the reasoning-graph visualization foundation with `npm run build` in `apps/web` and `git diff --check`.
- Extended the Design Advisor into a planning-pathway comparison workspace anchored by current state so users can compare recommended, future-ready, staged, and constrained deterministic postures without a generic dashboard table.
- Kept the new comparison layer frontend-only and interpretive by composing existing profile, backup-scope, panel/service, inverter, and current-architecture outputs rather than adding client-side optimization logic.
- Verified the planning-pathways foundation with `npm run build` in `apps/web` and `git diff --check`.
- Added an additive `planning_state` snapshot envelope to the Design Advisor API so architecture, reasoning, recommendation, and pathway-comparison outputs are explicitly tied to a named live design state and any linked saved scenarios.
- Added snapshot identity, version framing, generated planning-state variants, and linked-scenario metadata to the Design Advisor UI so the workspace now feels iterative without introducing a generalized version-history system.
- Verified the structured scenario/snapshot foundation with `python3 -m unittest discover -s tests -p 'test_resilience_recommendation.py'`, `python3 -m compileall app`, `npm run build` in `apps/web`, and `git diff --check`.
- Added additive immutable `scenario_revisions` persistence so saved scenarios now accumulate revision lineage, revision timestamps, latest revision identity, and compact advisor-linked planning-state framing.
- Surfaced revision-aware scenario metadata in the Design Advisor and Scenario Comparison UIs so live workspace state, saved scenario state, and historical revision identity remain visibly distinct without a broad version-control workflow.
- Verified the persistent scenario/revision foundation with `python3 -m unittest discover -s tests -p 'test_scenario_revisions.py'`, `python3 -m unittest discover -s tests -p 'test_resilience_recommendation.py'`, `python3 -m compileall app`, `npm run build` in `apps/web`, and `git diff --check`.
- Added a historical revision-comparison workspace to the Scenario Comparison page so saved revision drift can be inspected without flattening the page into a generic rankings dashboard.
- Surfaced drift across linked design, design goal/status, recommended pathway, current-state architecture framing, and proposed-pathway confidence using stored immutable revision snapshots.
- Verified the historical revision comparison workspace with `npm run build` in `apps/web` and `git diff --check`.

## 2026-05-27

- Formalized repository cognition layers so future agents can distinguish canonical knowledge, derived intelligence, advisory knowledge, operational knowledge, and historical knowledge.
- Added canonical terminology for canonical objects, derived estimates, transient recommendations, operational state, revision graphs, continuity lineage, deployment lineage, and orchestration-safe abstractions.
- Added governance, trust, provenance, topology, security, roadmap, continuity, and orchestration readiness docs under dedicated `docs/*/` directories.
- Added ADR 0007 for the repository-as-memory-substrate decision.
- Added project-specific portable skills under `.codex/project-skills/` for doctrine formalization, continuity governance, topology intelligence, orchestration readiness, canonical authority discipline, provenance lineage, and roadmap continuity.
- Updated discovery routing and continuity docs so future restore can start from a lean prompt such as `Load project skills before implementation.`
