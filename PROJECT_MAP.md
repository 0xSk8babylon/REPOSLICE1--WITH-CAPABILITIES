# Project Purpose

Document role: current reality. `VISION.md` defines principles. `ARCHITECTURE.md` defines structure. `MARKET_POSITIONING.md` defines the external narrative. `ECOSYSTEM_MAP.md` defines ecosystem relationships.

- VERIFIED: `residential-energy-planner` is a monorepo residential energy infrastructure planning platform with a FastAPI/SQLite backend, React/Vite frontend, structured house data, product facts, rule-based compatibility logic, and AI-grounding/explanation layers. Evidence: `README.md`, `docs/PROJECT_OVERVIEW.md`, `docs/ARCHITECTURE.md`, `apps/api/app/main.py`, `apps/web/src/app/App.jsx`.
- VERIFIED: The current product purpose is a living home energy planning platform, not a one-time solar proposal tool or final engineering/permitting/NEC-compliance tool. Evidence: `docs/PROJECT_OVERVIEW.md`, `docs/adr/0005-living-house-model-as-core-domain.md`, `README.md`, `docs/safety-and-code-disclaimer.md`.
- VERIFIED: The homeowner workflow currently lets a user view and edit home/property facts, buildings, panels, loads, equipment locations, estimated pathways, scenarios, and planning notes through frontend pages. Evidence: `apps/web/src/pages/HomeModelPage.jsx`, `apps/web/src/pages/ScenarioComparisonPage.jsx`, `apps/web/src/lib/api.js`.
- INFERRED: The contractor workflow currently exists as planning support and future scoped-output design, not as a dedicated contractor portal, packet generator, or authorization workflow. Evidence: `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`, `docs/PROJECT_OVERVIEW.md`, `docs/API_CONTRACTS.md`.
- VERIFIED: The planning workflow currently models homes, buildings, panels, loads, designs, design equipment, products, estimated pathways, scenarios, scenario revisions, generated takeoffs, compatibility issues, completeness, backup capability, expansion readiness, install complexity, and resilience recommendation profiles. Evidence: `apps/api/app/core/models.py`, `apps/api/app/services/*`, `apps/api/app/design_advisor/schemas.py`.
- VERIFIED: The AI workflow currently exposes a broad AI grounding endpoint and design advisor outputs that consume structured records, deterministic service outputs, provenance summaries, and rule provenance; AI is explicitly not the source of canonical facts. Evidence: `apps/api/app/services/ai_context.py`, `apps/api/app/ai_context/router.py`, `docs/ai-grounding-strategy.md`, `docs/governance/AI_AUTHORITY_LIMITS.md`.

# Current System Layers

## 1. Customer Input Layer

### Purpose

- VERIFIED: Captures user-entered planning facts for homes, buildings, electrical panels, loads, equipment locations, estimated pathways, designs, design equipment, scenarios, products, accounts, load templates, and design goal presets through API write contracts. Evidence: `apps/api/app/core/repository.py`, `apps/api/app/*/router.py`, `docs/API_CONTRACTS.md`.
- VERIFIED: Provides frontend forms for home overview, buildings, panels, loads, equipment locations, estimated pathways, design editing, design equipment assignment, and scenario editing. Evidence: `apps/web/src/pages/HomeModelPage.jsx`, `apps/web/src/pages/SystemDesignBuilderPage.jsx`, `apps/web/src/pages/ScenarioComparisonPage.jsx`.

### Status

- VERIFIED: The layer is implemented for core editable planning workflows.
- VERIFIED: The layer does not implement authentication, authorization, tenant isolation, subscription gating, or homeowner consent enforcement. Evidence: `README.md`, `docs/API_CONTRACTS.md`, `apps/api/app/accounts/schemas.py`.

### Current Source of Truth

- VERIFIED: SQLite records accessed through SQLAlchemy models and `DatabaseRepository` are the current source of truth for persisted customer input. Evidence: `apps/api/app/core/models.py`, `apps/api/app/core/repository.py`, `apps/api/app/core/database.py`.
- VERIFIED: Frontend input state is temporary until submitted through `apps/web/src/lib/api.js`. Evidence: `apps/web/src/pages/HomeModelPage.jsx`, `apps/web/src/pages/SystemDesignBuilderPage.jsx`, `apps/web/src/pages/ScenarioComparisonPage.jsx`.

### Files Involved

- VERIFIED: `apps/api/app/accounts/router.py`, `apps/api/app/accounts/schemas.py`
- VERIFIED: `apps/api/app/homes/router.py`, `apps/api/app/homes/schemas.py`
- VERIFIED: `apps/api/app/buildings/router.py`
- VERIFIED: `apps/api/app/panels/router.py`
- VERIFIED: `apps/api/app/loads/router.py`, `apps/api/app/loads/schemas.py`
- VERIFIED: `apps/api/app/designs/router.py`, `apps/api/app/designs/schemas.py`
- VERIFIED: `apps/api/app/equipment/router.py`, `apps/api/app/equipment/schemas.py`
- VERIFIED: `apps/api/app/planning/router.py`, `apps/api/app/planning/schemas.py`
- VERIFIED: `apps/api/app/scenarios/router.py`, `apps/api/app/scenarios/schemas.py`
- VERIFIED: `apps/web/src/lib/api.js`
- VERIFIED: `apps/web/src/pages/HomeModelPage.jsx`, `apps/web/src/pages/SystemDesignBuilderPage.jsx`, `apps/web/src/pages/ScenarioComparisonPage.jsx`

### Data Structures

- VERIFIED: `Account`, `Home`, `BuildingStructure`, `ElectricalPanel`, `Load`, `EquipmentLocation`, `EnergySystemDesign`, `DesignEquipment`, `Scenario`, `EstimatedPathway`, `LoadTemplate`, `DesignGoalPreset`, `EquipmentProduct`.
- VERIFIED: `data_origin` is used on many persisted records to distinguish `demo_seed`, `user_created`, `imported`, `verified`, `derived_estimate`, and `placeholder`. Evidence: `apps/api/app/core/types.py`, `apps/api/app/core/models.py`.

### Dependencies

- VERIFIED: Residential Twin, Electrical Feasibility, Equipment/Product, Scenario Planning, Takeoff/Estimating, Audit/Provenance, AI Advisor, and UI layers depend on customer-entered records.

### Risks

- VERIFIED: Account ownership fields exist but do not enforce access, tenant isolation, billing, or subscription behavior. Evidence: `apps/api/app/accounts/schemas.py`, `docs/API_CONTRACTS.md`.
- VERIFIED: Current write APIs accept client-provided string IDs. Evidence: `apps/api/app/*/schemas.py`.
- INFERRED: Client-provided IDs help seed/demo continuity but create future collision and ownership concerns if multi-user behavior is added.
- VERIFIED: Some routers check existence, but repository update methods generally assume the caller already validated the record. Evidence: `apps/api/app/core/repository.py`, `apps/api/app/*/router.py`.

### Missing Components

- VERIFIED: Authentication, authorization, consent enforcement, tenant isolation, billing enforcement, and role-aware scoped API views are not implemented. Evidence: `README.md`, `docs/API_CONTRACTS.md`, `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`.

## 2. Residential Twin Layer

### Purpose

- VERIFIED: Persists the home/property planning context over time through homes, buildings, panels, loads, equipment locations, designs, design equipment, scenarios, estimated pathways, and scenario revisions. Evidence: `apps/api/app/core/models.py`, `docs/PROJECT_OVERVIEW.md`, `docs/adr/0005-living-house-model-as-core-domain.md`.
- INFERRED: This layer is the current foundation for a canonical Residential Energy Twin, but the code does not use a single explicit `Twin` model or API envelope.

### Status

- VERIFIED: Partially implemented as structured domain records.
- INFERRED: Not yet a canonical twin protocol or complete twin object.

### Current Source of Truth

- VERIFIED: `homes`, `buildings`, `electrical_panels`, `loads`, `equipment_locations`, `energy_system_designs`, `design_equipment`, `scenarios`, `scenario_revisions`, and `estimated_pathways` tables are the persisted source of truth for current twin-like state. Evidence: `apps/api/app/core/models.py`.
- VERIFIED: `GET /api/homes`, `GET /api/buildings`, `GET /api/panels`, `GET /api/loads`, `GET /api/designs`, `GET /api/equipment/locations`, `GET /api/scenarios`, and `GET /api/estimated-pathways` expose slices of this state. Evidence: `apps/api/app/main.py`, `apps/api/app/*/router.py`, `apps/web/src/lib/api.js`.

### Files Involved

- VERIFIED: `apps/api/app/core/models.py`
- VERIFIED: `apps/api/app/core/repository.py`
- VERIFIED: `apps/api/app/homes/schemas.py`
- VERIFIED: `apps/api/app/designs/schemas.py`
- VERIFIED: `apps/api/app/loads/schemas.py`
- VERIFIED: `apps/api/app/planning/schemas.py`
- VERIFIED: `apps/api/app/scenarios/schemas.py`
- VERIFIED: `apps/web/src/pages/HomeModelPage.jsx`
- VERIFIED: `apps/web/src/pages/SystemDesignBuilderPage.jsx`

### Data Structures

- VERIFIED: `Home`, `BuildingStructure`, `ElectricalPanel`, `Load`, `EquipmentLocation`, `EnergySystemDesign`, `DesignEquipment`, `Scenario`, `ScenarioRevision`, `EstimatedPathway`.
- VERIFIED: `PlanningStateSnapshot`, `PlanningStateVariant`, and `PlanningStateScenarioLink` are advisor snapshot view models, not canonical persisted twin tables. Evidence: `apps/api/app/design_advisor/schemas.py`, `apps/api/app/services/design_advisor.py`.

### Dependencies

- VERIFIED: Electrical Feasibility, Equipment/Product, Scenario Planning, Takeoff/Estimating, Audit/Provenance, AI Advisor, and UI layers depend on residential twin records.

### Risks

- VERIFIED: `docs/DATABASE_SCHEMA.md` lists core tables but omits `scenario_revisions`, while `apps/api/app/core/models.py` defines `ScenarioRevision`. Evidence: `docs/DATABASE_SCHEMA.md`, `apps/api/app/core/models.py`.
- VERIFIED: Roof geometry, usable roof area, verified field inventory, service territory, permit state, and utility interconnection state are absent or documented as deferred. Evidence: `docs/CURRENT_STATE.md`, `docs/topology/TOPOLOGY_LIFECYCLE.md`, `apps/api/app/services/resilience_recommendation.py`.
- INFERRED: Twin ownership is distributed across multiple routers and schemas rather than centralized in a canonical twin contract.

### Missing Components

- VERIFIED: No explicit canonical twin export/protocol endpoint exists in the current API list. Evidence: `apps/api/app/main.py`, `apps/web/src/lib/api.js`.
- VERIFIED: Full provenance, audit/change history, permission enforcement, measured roof geometry, and operational state are not implemented. Evidence: `README.md`, `docs/provenance/LINEAGE_MODEL.md`, `docs/trust/TRUST_ZONES.md`.

## 3. Electrical Feasibility Layer

### Purpose

- VERIFIED: Provides planning-only electrical feasibility signals around panels, service size, backup load grouping, backup architecture direction, inverter/system posture, and compatibility warnings. Evidence: `apps/api/app/services/design_completeness.py`, `apps/api/app/services/compatibility.py`, `apps/api/app/services/resilience_recommendation.py`.
- VERIFIED: Does not implement final NEC compliance, permitting, engineering approval, busbar validation, final transfer design, inverter sizing, or utility approval. Evidence: `docs/CURRENT_STATE.md`, `docs/safety-and-code-disclaimer.md`, `apps/api/app/services/provenance.py`.

### Status

- VERIFIED: Implemented as deterministic planning heuristics and advisor outputs.
- VERIFIED: Not implemented as an engineering compliance engine.

### Current Source of Truth

- VERIFIED: Source inputs are persisted `ElectricalPanel`, `Load`, `EnergySystemDesign`, `DesignEquipment`, `EquipmentProduct`, `EquipmentLocation`, and `EstimatedPathway` records. Evidence: `apps/api/app/services/design_analysis.py`.
- VERIFIED: Derived outputs are produced by `DesignCompletenessService`, `CompatibilityService`, `BackupCapabilityService`, `ExpansionReadinessService`, and `ResilienceRecommendationService`. Evidence: `apps/api/app/services/*.py`.

### Files Involved

- VERIFIED: `apps/api/app/homes/schemas.py`
- VERIFIED: `apps/api/app/loads/schemas.py`
- VERIFIED: `apps/api/app/services/design_analysis.py`
- VERIFIED: `apps/api/app/services/design_completeness.py`
- VERIFIED: `apps/api/app/services/compatibility.py`
- VERIFIED: `apps/api/app/services/backup_capability.py`
- VERIFIED: `apps/api/app/services/expansion_readiness.py`
- VERIFIED: `apps/api/app/services/resilience_recommendation.py`
- VERIFIED: `apps/api/app/compatibility_rules/router.py`
- VERIFIED: `apps/api/app/design_advisor/router.py`
- VERIFIED: `apps/web/src/pages/DesignAdvisorPage.jsx`

### Data Structures

- VERIFIED: `ElectricalPanel`, `Load`, `CompatibilityIssue`, `CompatibilityExplanation`, `BackupLoadSelectionSummary`, `PanelServiceArchitectureEstimate`, `InverterSystemArchitectureEstimate`, `CurrentHomeEnergyArchitectureEstimate`, `StructuredSystemReasoningGraph`.
- VERIFIED: `PanelType`, `BackupPriority`, `PhaseType`, `DesignGoal`, `ArchitectureType`, and product type enums drive classification and rules. Evidence: `apps/api/app/core/types.py`.

### Dependencies

- VERIFIED: Scenario Planning, Takeoff/Estimating, AI Advisor, and UI layers depend on electrical feasibility outputs.

### Risks

- VERIFIED: Planning completeness and panel/service guidance are explicitly not engineering completeness. Evidence: `docs/adr/0003-planning-completeness-not-engineering-compliance.md`, `apps/api/app/services/design_completeness.py`.
- VERIFIED: Electrical feasibility uses recorded planning fields and product signals, not measured site verification or NEC calculations. Evidence: `apps/api/app/services/resilience_recommendation.py`, `docs/CURRENT_STATE.md`.
- INFERRED: Because service, inverter, generator, and transfer logic live inside a large recommendation service, ownership boundaries may become unclear as electrical reasoning grows.

### Missing Components

- VERIFIED: NEC compliance engine, permit readiness, AHJ review, engineering approval, final load calculation, inverter sizing, busbar rules, service upgrade validation, and utility interconnection authority are not implemented. Evidence: `README.md`, `docs/CURRENT_STATE.md`, `docs/safety-and-code-disclaimer.md`.

## 4. Equipment / Product Layer

### Purpose

- VERIFIED: Stores equipment products, product specs, ecosystems, product types, documentation URLs, source documents, and product provenance for planning and design composition. Evidence: `apps/api/app/core/models.py`, `apps/api/app/equipment/schemas.py`, `apps/api/app/product_library/router.py`.

### Status

- VERIFIED: Product catalog and design-equipment assignment are implemented.
- VERIFIED: Product data provenance is partial and seed data includes placeholder/unverified references. Evidence: `README.md`, `apps/api/app/seed/sample_data.py`.

### Current Source of Truth

- VERIFIED: `equipment_products` is the persisted product record table.
- VERIFIED: `source_documents` and `data_provenance` provide partial source lineage for product fields.
- VERIFIED: `design_equipment` records connect products to designs with quantities, roles, and optional locations.

### Files Involved

- VERIFIED: `apps/api/app/equipment/schemas.py`
- VERIFIED: `apps/api/app/equipment/router.py`
- VERIFIED: `apps/api/app/product_library/router.py`
- VERIFIED: `apps/api/app/designs/schemas.py`
- VERIFIED: `apps/api/app/designs/router.py`
- VERIFIED: `apps/api/app/services/provenance.py`
- VERIFIED: `apps/web/src/pages/ProductLibraryPage.jsx`
- VERIFIED: `apps/web/src/pages/SystemDesignBuilderPage.jsx`

### Data Structures

- VERIFIED: `EquipmentProduct`, `EquipmentLocation`, `DesignEquipment`, `SourceDocument`, `DataProvenance`, `ProductType`, `Ecosystem`, `LocationType`.

### Dependencies

- VERIFIED: Electrical Feasibility, Scenario Planning, Takeoff/Estimating, AI Advisor, and UI layers depend on product and design-equipment records.

### Risks

- VERIFIED: Product specs are stored in a flexible JSON field. Evidence: `apps/api/app/core/models.py`.
- VERIFIED: Seeded product references include placeholder and unverified manufacturer references. Evidence: `apps/api/app/seed/sample_data.py`.
- INFERRED: Flexible product specs allow rapid modeling but create validation and schema consistency risk for future manufacturer-grade product data.

### Missing Components

- VERIFIED: Automated manufacturer ingestion, exhaustive product-field provenance, verified manufacturer catalog authority, compatibility certification, and product availability tracking are not implemented. Evidence: `README.md`, `docs/provenance/LINEAGE_MODEL.md`.

## 5. Scenario Planning Layer

### Purpose

- VERIFIED: Stores planning scenarios linked to designs, compares scenario tradeoffs, ranks placeholder metrics, and captures immutable compact scenario revisions on create/update. Evidence: `apps/api/app/scenarios/router.py`, `apps/api/app/services/scenario_comparison.py`, `apps/api/app/services/scenario_revision.py`.

### Status

- VERIFIED: Implemented with persisted live scenarios, persisted scenario revisions, comparison output, rankings, warnings, lineage summaries, and frontend scenario editing/comparison UI.

### Current Source of Truth

- VERIFIED: `scenarios` table is the live scenario source of truth.
- VERIFIED: `scenario_revisions` table stores compact revision lineage.
- VERIFIED: `ScenarioComparisonService` derives comparison payloads from scenarios, linked designs, completeness, products, pathways, and provenance.

### Files Involved

- VERIFIED: `apps/api/app/core/models.py`
- VERIFIED: `apps/api/app/scenarios/schemas.py`
- VERIFIED: `apps/api/app/scenarios/router.py`
- VERIFIED: `apps/api/app/services/scenario_comparison.py`
- VERIFIED: `apps/api/app/services/scenario_revision.py`
- VERIFIED: `apps/api/tests/test_scenario_revisions.py`
- VERIFIED: `apps/web/src/pages/ScenarioComparisonPage.jsx`

### Data Structures

- VERIFIED: `Scenario`, `ScenarioRevision`, `ScenarioRevisionSummary`, `ScenarioRevisionOverview`, `PlanningStateSnapshot`, comparison payload dictionaries.

### Dependencies

- VERIFIED: Scenario Planning depends on Customer Input, Residential Twin, Equipment/Product, Electrical Feasibility, Audit/Provenance, and AI Advisor layers.
- VERIFIED: UI and AI Advisor layers depend on scenario state and linked revisions for display/context.

### Risks

- VERIFIED: Scenario cost and score fields are placeholders. Evidence: `apps/api/app/scenarios/schemas.py`, `apps/api/app/services/scenario_comparison.py`.
- VERIFIED: Scenario revisions preserve compact planning-state snapshots, not full advisor replay payloads. Evidence: `apps/api/app/services/scenario_revision.py`, `docs/provenance/LINEAGE_MODEL.md`.
- VERIFIED: `docs/DATABASE_SCHEMA.md` omits `scenario_revisions`, creating documentation/schema mismatch.

### Missing Components

- VERIFIED: Full replayable historical advisor payload persistence, complete field lineage for scenario scores, and non-placeholder pricing/estimate authority are not implemented. Evidence: `docs/provenance/LINEAGE_MODEL.md`, `apps/api/app/services/scenario_comparison.py`.

## 6. Takeoff / Estimating Layer

### Purpose

- VERIFIED: Generates planning takeoff line items from persisted design equipment composition and placeholder unit cost data. Evidence: `apps/api/app/services/takeoff_generation.py`, `apps/api/app/takeoffs/router.py`.

### Status

- VERIFIED: Implemented as transient generated takeoff output for selected designs.
- VERIFIED: Persisted `takeoff_requests` and `takeoff_line_items` tables exist and seed data includes a sample takeoff, but generated takeoffs are intentionally transient in the current phase. Evidence: `apps/api/app/core/models.py`, `apps/api/app/seed/runtime.py`, `apps/api/app/services/takeoff_generation.py`.

### Current Source of Truth

- VERIFIED: Generated takeoff output uses current `EnergySystemDesign`, `DesignEquipment`, `EquipmentProduct`, and `EquipmentLocation` records.
- VERIFIED: Placeholder costs come from product specs when present or `PLACEHOLDER_UNIT_COSTS` in `takeoff_generation.py`.
- VERIFIED: `/api/takeoffs/current` returns the first persisted takeoff request, while `/api/takeoffs/generate/{design_id}` returns derived current output. Evidence: `apps/api/app/core/repository.py`, `apps/api/app/takeoffs/router.py`.

### Files Involved

- VERIFIED: `apps/api/app/takeoffs/schemas.py`
- VERIFIED: `apps/api/app/takeoffs/router.py`
- VERIFIED: `apps/api/app/services/takeoff_generation.py`
- VERIFIED: `apps/api/app/services/provenance.py`
- VERIFIED: `apps/web/src/pages/TakeoffEstimatePage.jsx`

### Data Structures

- VERIFIED: `TakeoffRequest`, `TakeoffLineItem`, `TakeoffResponse`, `DesignEquipment`, `EquipmentProduct`.

### Dependencies

- VERIFIED: Takeoff/Estimating depends on Customer Input, Residential Twin, Equipment/Product, Audit/Provenance, and UI layers.

### Risks

- VERIFIED: Unit costs and total costs are placeholders and not procurement-ready. Evidence: `apps/api/app/services/takeoff_generation.py`, `apps/web/src/pages/TakeoffEstimatePage.jsx`.
- VERIFIED: Generated takeoff snapshots are not persisted or versioned. Evidence: `apps/api/app/services/takeoff_generation.py`, `README.md`, `docs/provenance/LINEAGE_MODEL.md`.
- INFERRED: Coexistence of persisted seed takeoff records and transient generated takeoffs can create source-of-truth ambiguity.

### Missing Components

- VERIFIED: Verified cost basis, contractor bid workflow, persisted generated snapshots, procurement readiness, and full takeoff lineage are not implemented. Evidence: `README.md`, `docs/provenance/LINEAGE_MODEL.md`.

## 7. Permission / Consent Layer

### Purpose

- VERIFIED: Provides account, role, plan, subscription, permission-readiness metadata, and future scoped-view documentation boundaries.
- VERIFIED: Does not currently enforce homeowner consent, RBAC, tenant isolation, export authorization, subscription access, contractor authorization, utility submission authorization, or operational-control permission. Evidence: `apps/api/app/accounts/schemas.py`, `docs/API_CONTRACTS.md`, `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`.

### Status

- VERIFIED: Implemented as scaffolding and descriptive metadata only.
- UNKNOWN: No dedicated homeowner consent capture model or consent event table was found in the inspected code.

### Current Source of Truth

- VERIFIED: `accounts` table stores role, subscription status, and plan type.
- VERIFIED: `homes.account_id` links homes to accounts but is nullable.
- VERIFIED: `PermissionReadinessMetadata` describes non-enforced permission posture in responses.

### Files Involved

- VERIFIED: `apps/api/app/accounts/schemas.py`
- VERIFIED: `apps/api/app/accounts/router.py`
- VERIFIED: `apps/api/app/core/schemas.py`
- VERIFIED: `apps/api/app/core/types.py`
- VERIFIED: `apps/api/app/services/ai_context.py`
- VERIFIED: `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- VERIFIED: `docs/security/SCOPED_INTELLIGENCE_OUTPUTS.md`
- VERIFIED: `docs/API_CONTRACTS.md`

### Data Structures

- VERIFIED: `Account`, `PermissionReadinessMetadata`, `AccountRole`, `SubscriptionStatus`, `PlanType`, `ApiViewAudience`, `DataClassification`.

### Dependencies

- VERIFIED: UI, AI Advisor, Audit/Provenance, and future contractor/utility views depend on permission boundaries.
- INFERRED: Current runtime behavior does not depend on permission enforcement because enforcement is absent.

### Risks

- VERIFIED: Existing broad API responses are product data contracts, not security enforcement boundaries. Evidence: `docs/API_CONTRACTS.md`.
- VERIFIED: AI context includes broad raw object exposure for compatibility/grounding and labels this with permission-readiness warnings. Evidence: `apps/api/app/services/ai_context.py`.
- INFERRED: The presence of account roles without enforcement can be mistaken for active permissions if UI/API copy drifts.

### Missing Components

- VERIFIED: Auth, RBAC, ABAC, tenant isolation, consent records, export authorization, contractor-safe packet enforcement, utility-safe packet enforcement, and audit-backed permission events are not implemented. Evidence: `docs/API_CONTRACTS.md`, `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`.

## 8. Audit / Provenance Layer

### Purpose

- VERIFIED: Tracks source documents, data provenance, rule provenance, provenance summaries, trust states, authority layer metadata, data classification metadata, and derived-output inspectability. Evidence: `apps/api/app/provenance/schemas.py`, `apps/api/app/services/provenance.py`, `docs/provenance/LINEAGE_MODEL.md`.

### Status

- VERIFIED: Partially implemented.
- VERIFIED: Full audit/change history and exhaustive field-level provenance are not implemented. Evidence: `README.md`, `docs/provenance/LINEAGE_MODEL.md`.

### Current Source of Truth

- VERIFIED: `source_documents`, `data_provenance`, and `rule_provenance` tables are persisted lineage sources.
- VERIFIED: `ProvenanceService` derives provenance summaries and inspectability payloads for products, loads, pathways, takeoffs, advisor issues, recommendations, scenario comparison, and AI context.

### Files Involved

- VERIFIED: `apps/api/app/provenance/schemas.py`
- VERIFIED: `apps/api/app/provenance/router.py`
- VERIFIED: `apps/api/app/rule_provenance/router.py`
- VERIFIED: `apps/api/app/source_documents/router.py`
- VERIFIED: `apps/api/app/services/provenance.py`
- VERIFIED: `apps/api/app/seed/sample_data.py`
- VERIFIED: `docs/provenance/LINEAGE_MODEL.md`
- VERIFIED: `docs/trust/TRUST_ZONES.md`

### Data Structures

- VERIFIED: `SourceDocument`, `DataProvenance`, `RuleProvenance`, `ProvenanceSummary`, `EstimateInspectability`, `InspectabilitySignal`, `ViewBoundaryMetadata`, `PermissionReadinessMetadata`.

### Dependencies

- VERIFIED: Equipment/Product, Scenario Planning, Takeoff/Estimating, AI Advisor, UI, and future Permission/Consent views depend on provenance and trust metadata.

### Risks

- VERIFIED: Field-level provenance is partial. Evidence: `docs/provenance/LINEAGE_MODEL.md`.
- VERIFIED: Data classification is descriptive and not enforced as an API policy. Evidence: `docs/provenance/LINEAGE_MODEL.md`, `docs/API_CONTRACTS.md`.
- VERIFIED: Deployment lineage is not formalized. Evidence: `docs/provenance/LINEAGE_MODEL.md`, `docs/governance/GOVERNANCE_GAP_ANALYSIS.md`.

### Missing Components

- VERIFIED: Full audit/change history, exhaustive field-level provenance, deployment lineage, enforced data classification, and persisted generated takeoff lineage are not implemented. Evidence: `README.md`, `docs/provenance/LINEAGE_MODEL.md`.

## 9. AI Advisor Layer

### Purpose

- VERIFIED: Composes structured facts, deterministic planning heuristics, recommendation profiles, completeness, compatibility, backup, expansion, install complexity, planning-state snapshots, reasoning graphs, trust posture, and AI grounding context. Evidence: `apps/api/app/services/design_advisor.py`, `apps/api/app/services/resilience_recommendation.py`, `apps/api/app/services/ai_context.py`.
- VERIFIED: Advisor output is planning guidance only and not engineering, permit, code, utility, or operational approval. Evidence: `apps/api/app/services/design_advisor.py`, `apps/api/app/services/provenance.py`, `docs/governance/AI_AUTHORITY_LIMITS.md`.

### Status

- VERIFIED: Implemented as deterministic service composition plus broad AI grounding payloads.
- VERIFIED: No conversational AI model call or AI write authority was found in inspected code.

### Current Source of Truth

- VERIFIED: Advisor inputs come from persisted design/home/building/panel/load/product/location/pathway/scenario/provenance/rule records.
- VERIFIED: Advisor outputs are derived at request time by services and are not persisted except compact scenario revisions.

### Files Involved

- VERIFIED: `apps/api/app/design_advisor/router.py`
- VERIFIED: `apps/api/app/design_advisor/schemas.py`
- VERIFIED: `apps/api/app/services/design_advisor.py`
- VERIFIED: `apps/api/app/services/resilience_recommendation.py`
- VERIFIED: `apps/api/app/services/design_completeness.py`
- VERIFIED: `apps/api/app/services/compatibility.py`
- VERIFIED: `apps/api/app/services/ai_context.py`
- VERIFIED: `apps/web/src/pages/DesignAdvisorPage.jsx`
- VERIFIED: `apps/web/src/pages/AIContextPage.jsx`

### Data Structures

- VERIFIED: `ResilienceRecommendation`, `RecommendationProfileCard`, `BackupLoadSelectionSummary`, `CurrentHomeEnergyArchitectureEstimate`, `PanelServiceArchitectureEstimate`, `InverterSystemArchitectureEstimate`, `StructuredSystemReasoningGraph`, `PlanningStateSnapshot`.

### Dependencies

- VERIFIED: AI Advisor depends on Customer Input, Residential Twin, Electrical Feasibility, Equipment/Product, Scenario Planning, Audit/Provenance, and Permission/Consent metadata.
- VERIFIED: User Interface depends on AI Advisor payloads for Design Advisor and AI Context pages.

### Risks

- VERIFIED: `GET /api/ai-context/design/{design_id}` intentionally remains broad raw grounding context and is not a narrowed RBAC view. Evidence: `apps/api/app/services/ai_context.py`, `docs/API_CONTRACTS.md`.
- VERIFIED: Recommendation logic is concentrated in a large `resilience_recommendation.py` service. Evidence: `apps/api/app/services/resilience_recommendation.py`.
- INFERRED: As advisor behavior grows, the large service may become a coupling point across backup scope, topology, panel/service, inverter/system, battery, solar, and reasoning graph concerns.

### Missing Components

- VERIFIED: AI-safe narrowed grounding view, conversational write controls, model integration, full advisor replay persistence, and operational orchestration are not implemented. Evidence: `docs/API_CONTRACTS.md`, `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`, `docs/orchestration/READINESS_GAPS.md`.

## 10. User Interface Layer

### Purpose

- VERIFIED: Provides the current planning UI for dashboard, home/property model, system design builder, product library, scenario comparison, design advisor, AI context, and takeoff/estimate. Evidence: `apps/web/src/app/App.jsx`.

### Status

- VERIFIED: Implemented as React/Vite pages using a shared API client, query helper, mutation helper, shared shell, form inputs, cards, badges, and trust helpers.

### Current Source of Truth

- VERIFIED: UI state is client-side and temporary; persisted state comes from backend API responses. Evidence: `apps/web/src/lib/api.js`, `apps/web/src/lib/useApiQuery.js`, `apps/web/src/lib/useApiMutation.js`.

### Files Involved

- VERIFIED: `apps/web/src/app/App.jsx`
- VERIFIED: `apps/web/src/lib/api.js`
- VERIFIED: `apps/web/src/lib/useApiQuery.js`
- VERIFIED: `apps/web/src/lib/useApiMutation.js`
- VERIFIED: `apps/web/src/lib/trust.js`
- VERIFIED: `apps/web/src/pages/DashboardPage.jsx`
- VERIFIED: `apps/web/src/pages/HomeModelPage.jsx`
- VERIFIED: `apps/web/src/pages/SystemDesignBuilderPage.jsx`
- VERIFIED: `apps/web/src/pages/ProductLibraryPage.jsx`
- VERIFIED: `apps/web/src/pages/ScenarioComparisonPage.jsx`
- VERIFIED: `apps/web/src/pages/DesignAdvisorPage.jsx`
- VERIFIED: `apps/web/src/pages/AIContextPage.jsx`
- VERIFIED: `apps/web/src/pages/TakeoffEstimatePage.jsx`

### Data Structures

- VERIFIED: Frontend consumes API JSON contracts for home, load summary, designs, products, source documents, provenance, compatibility issues, scenarios, comparison, equipment locations, pathways, takeoff, design advisor, AI context, and placeholder estimates.

### Dependencies

- VERIFIED: UI depends on every backend layer exposed through `apps/web/src/lib/api.js`.

### Risks

- VERIFIED: Frontend depends on compatibility-sensitive GET contracts. Evidence: `docs/API_CONTRACTS.md`, `apps/web/src/lib/api.js`.
- INFERRED: Because the frontend fetches broad endpoint payloads directly, future scoped views will need additive contracts or versioning to avoid breaking current pages.

### Missing Components

- VERIFIED: Dedicated contractor, utility, admin/security, consent-management, and audit-log UI workflows were not found in inspected frontend routes.

# Ownership Map

| Layer | Primary Agent Owner | Supporting Agents | Protected Decisions Requiring Matt Approval |
| --- | --- | --- | --- |
| Customer Input Layer | VERIFIED: Frontend Agent | VERIFIED: Backend Agent, Permission / Consent Agent, QA / Testing Agent | VERIFIED: schema changes, permission logic, data ownership rules, API contract breaks |
| Residential Twin Layer | VERIFIED: Twin Agent | VERIFIED: Backend Agent, Documentation Agent, Security / Audit / Provenance Agent | VERIFIED: canonical twin model, schema changes, persistence contracts, architecture changes |
| Electrical Feasibility Layer | VERIFIED: NEC / Electrical Logic Agent | VERIFIED: Backend Agent, Security / Audit / Provenance Agent, QA / Testing Agent | VERIFIED: NEC logic, compliance logic, load calculation authority, stamped electrical decisions |
| Equipment / Product Layer | VERIFIED: Equipment Agent | VERIFIED: Backend Agent, Security / Audit / Provenance Agent, Frontend Agent | VERIFIED: product/spec authority, schema changes, provenance policy, compatibility claims |
| Scenario Planning Layer | VERIFIED: Product Orchestrator | VERIFIED: Twin Agent, Backend Agent, Frontend Agent, Security / Audit / Provenance Agent | VERIFIED: business model changes, scenario authority, pricing logic, architecture changes |
| Takeoff / Estimating Layer | VERIFIED: Takeoff / Estimating Agent | VERIFIED: Equipment Agent, Backend Agent, Frontend Agent, Security / Audit / Provenance Agent | VERIFIED: pricing logic, estimate authority, bid/procurement claims, persistence contracts |
| Permission / Consent Layer | VERIFIED: Permission / Consent Agent | VERIFIED: Security / Audit / Provenance Agent, Backend Agent, Frontend Agent | VERIFIED: permissions, consent, privacy, homeowner authorization, RBAC/tenant isolation |
| Audit / Provenance Layer | VERIFIED: Security / Audit / Provenance Agent | VERIFIED: Documentation Agent, Backend Agent, Equipment Agent, Twin Agent | VERIFIED: provenance policy, audit policy, trust-state semantics, data-classification enforcement |
| AI Advisor Layer | VERIFIED: Technical Orchestrator | VERIFIED: Security / Audit / Provenance Agent, NEC / Electrical Logic Agent, Equipment Agent, Backend Agent, Frontend Agent | VERIFIED: architecture, compliance claims, pricing claims, AI authority, advisor trust language |
| User Interface Layer | VERIFIED: Frontend Agent | VERIFIED: Product Orchestrator, Backend Agent, QA / Testing Agent, Security / Audit / Provenance Agent | VERIFIED: trust copy implying approval/certainty, permission UX, contract-breaking API changes |

# Data Flow

```text
Customer Input
↓
Twin
↓
Electrical
↓
Equipment
↓
Scenarios
↓
Takeoff
↓
Permissions
↓
Audit
↓
Advisor
↓
UI
```

- VERIFIED: Customer Input to Twin flow exists when frontend forms call `/api/homes`, `/api/buildings`, `/api/panels`, `/api/loads`, `/api/equipment/locations`, `/api/estimated-pathways`, `/api/designs`, and `/api/scenarios`, and repository methods persist SQLAlchemy models. Evidence: `apps/web/src/lib/api.js`, `apps/api/app/core/repository.py`.
- VERIFIED: Twin to Electrical flow exists through `DesignAnalysisService`, which loads home, buildings, panels, loads, locations, pathways, design, and assigned products before completeness, compatibility, backup, expansion, install, and recommendation services run. Evidence: `apps/api/app/services/design_analysis.py`.
- VERIFIED: Electrical to Equipment flow exists bidirectionally in practice: electrical/advisor services inspect assigned product types/ecosystems, and design equipment connects equipment products to design roles and locations. Evidence: `apps/api/app/services/compatibility.py`, `apps/api/app/services/resilience_recommendation.py`, `apps/api/app/designs/schemas.py`.
- VERIFIED: Equipment to Scenarios flow exists because scenario comparison builds linked-design summaries and lineage from assigned products, pathways, and provenance. Evidence: `apps/api/app/services/scenario_comparison.py`.
- VERIFIED: Scenarios to Takeoff flow is not direct in current code; takeoff generation uses design composition, not scenario records. Evidence: `apps/api/app/services/takeoff_generation.py`.
- INFERRED: The requested conceptual flow places scenarios before takeoff because scenarios frame selected planning paths, but current generated takeoff logic is design-driven.
- VERIFIED: Takeoff to Permissions flow is not implemented as authorization or consent enforcement; takeoff payloads include trust notes and missing information only. Evidence: `apps/api/app/services/takeoff_generation.py`, `docs/API_CONTRACTS.md`.
- VERIFIED: Permissions to Audit flow is descriptive only; permission readiness metadata labels non-enforcement but does not create audit records. Evidence: `apps/api/app/accounts/schemas.py`, `apps/api/app/services/ai_context.py`.
- VERIFIED: Audit to Advisor flow exists through provenance summaries, rule provenance, recommendation provenance, estimate inspectability, scenario lineage, and AI context source records. Evidence: `apps/api/app/services/provenance.py`, `apps/api/app/services/ai_context.py`, `apps/api/app/services/resilience_recommendation.py`.
- VERIFIED: Advisor to UI flow exists through `/api/design-advisor/summary/{design_id}` and `/api/ai-context/design/{design_id}` consumed by `DesignAdvisorPage.jsx` and `AIContextPage.jsx`. Evidence: `apps/web/src/lib/api.js`, `apps/web/src/pages/DesignAdvisorPage.jsx`, `apps/web/src/pages/AIContextPage.jsx`.
- UNKNOWN: No runtime flow was found for external contractor review, homeowner consent approval, utility submission, permitting, or operational dispatch.

# Sources of Truth

| Source | Classification | Evidence |
| --- | --- | --- |
| `accounts` | VERIFIED: authoritative for account scaffolding; temporary for permissions because enforcement is absent | `apps/api/app/core/models.py`, `apps/api/app/accounts/schemas.py` |
| `homes` | VERIFIED: authoritative persisted planning record for home identity, address, utility provider placeholder, service size, and notes | `apps/api/app/core/models.py`, `apps/api/app/homes/schemas.py` |
| `buildings` | VERIFIED: authoritative persisted planning record for structures | `apps/api/app/core/models.py`, `apps/api/app/homes/schemas.py` |
| `electrical_panels` | VERIFIED: authoritative persisted planning record for panel facts; not authoritative for NEC compliance | `apps/api/app/core/models.py`, `docs/safety-and-code-disclaimer.md` |
| `loads` | VERIFIED: authoritative persisted planning record for load assumptions; derived summaries are not authoritative facts | `apps/api/app/core/models.py`, `apps/api/app/services/load_calculation.py` |
| `equipment_products` | VERIFIED: authoritative current catalog records; inferred/temporary for manufacturer-grade specs when provenance is placeholder or unverified | `apps/api/app/core/models.py`, `apps/api/app/seed/sample_data.py` |
| `equipment_locations` | VERIFIED: authoritative persisted planning record for siting assumptions; not field-verified geometry | `apps/api/app/core/models.py`, `apps/api/app/equipment/schemas.py` |
| `energy_system_designs` | VERIFIED: authoritative persisted planning record for design intent/status/architecture type | `apps/api/app/core/models.py`, `apps/api/app/designs/schemas.py` |
| `design_equipment` | VERIFIED: authoritative persisted planning record for product assignments, quantities, roles, and locations | `apps/api/app/core/models.py`, `apps/api/app/designs/schemas.py` |
| `compatibility_issues` | VERIFIED: authoritative for seeded/persisted compatibility issue records; derived advisor issues are derived | `apps/api/app/core/models.py`, `apps/api/app/services/compatibility.py` |
| `scenarios` | VERIFIED: authoritative live scenario records; placeholder scores/costs are temporary/non-authoritative | `apps/api/app/core/models.py`, `apps/api/app/scenarios/schemas.py` |
| `scenario_revisions` | VERIFIED: derived/historical compact revision lineage, not full replay authority | `apps/api/app/core/models.py`, `apps/api/app/services/scenario_revision.py` |
| `estimated_pathways` | VERIFIED: authoritative persisted planning route assumptions; derived/inferred for cost, confidence, visibility, and savings placeholders | `apps/api/app/core/models.py`, `apps/api/app/planning/schemas.py` |
| `takeoff_requests` and `takeoff_line_items` | VERIFIED: authoritative for persisted seed/current takeoff records; generated takeoffs are temporary derived outputs | `apps/api/app/core/models.py`, `apps/api/app/services/takeoff_generation.py` |
| `load_templates` | VERIFIED: authoritative persisted templates for creating loads | `apps/api/app/core/models.py`, `apps/api/app/planning/schemas.py` |
| `design_goal_presets` | VERIFIED: authoritative persisted presets for design goal creation | `apps/api/app/core/models.py`, `apps/api/app/planning/schemas.py` |
| `source_documents` | VERIFIED: authoritative source-document records; not proof of correctness | `apps/api/app/core/models.py`, `apps/api/app/provenance/schemas.py` |
| `data_provenance` | VERIFIED: authoritative current provenance rows for covered fields; partial coverage | `apps/api/app/core/models.py`, `docs/provenance/LINEAGE_MODEL.md` |
| `rule_provenance` | VERIFIED: authoritative current rule lineage records for covered internal rules | `apps/api/app/core/models.py`, `apps/api/app/seed/sample_data.py` |
| Deterministic services | VERIFIED: derived outputs from persisted records and internal rules | `apps/api/app/services/*.py` |
| AI context payload | VERIFIED: advisory/derived grounding view; not canonical fact source | `apps/api/app/services/ai_context.py`, `docs/ai-grounding-strategy.md` |
| Frontend component state | VERIFIED: temporary UI state before persistence | `apps/web/src/pages/*.jsx` |
| Demo seed data | VERIFIED: temporary/demo continuity source; not factual authority | `README.md`, `apps/api/app/seed/sample_data.py` |

# Architectural Gaps

- VERIFIED: `docs/DATABASE_SCHEMA.md` is stale or incomplete because it omits `scenario_revisions` while the ORM defines the table.
- VERIFIED: Field-level provenance is partial and not exhaustive.
- VERIFIED: Generated takeoffs are transient and not versioned.
- VERIFIED: Full audit/change history is missing.
- VERIFIED: Auth, RBAC, ABAC, tenant isolation, subscription enforcement, and consent enforcement are missing.
- VERIFIED: Existing scoped view models are documented as future contract boundaries, not implemented filtered endpoints.
- VERIFIED: AI context remains a broad grounding payload rather than a minimized AI-safe view.
- VERIFIED: Data classification and authority metadata are descriptive and not enforced.
- VERIFIED: Product specs can be placeholder/unverified and product ingestion is not automated.
- VERIFIED: Cost, savings, and scenario score fields are placeholders or planning estimates.
- VERIFIED: NEC/permitting/engineering compliance is explicitly deferred.
- VERIFIED: Utility-safe abstractions, interconnection state, tariff/rate lineage, and operational-control state are missing.
- VERIFIED: Roof geometry and usable roof area are not measured/calculated.
- INFERRED: Residential twin ownership is distributed across multiple domain modules rather than represented by a single canonical twin contract.
- INFERRED: The large recommendation service concentrates many reasoning responsibilities and may become a coupling risk.
- UNKNOWN: No evidence was found for production deployment lineage tying code revision, schema revision, seed revision, and trust posture.

# Twin Readiness Assessment

- VERIFIED: Existing twin capabilities include persisted home identity, address, utility provider field, service size, buildings, panel records, load records, equipment locations, product assignments, designs, scenarios, scenario revisions, estimated pathways, and data origins.
- VERIFIED: Existing twin capabilities include deterministic derived views over the recorded home state: completeness, compatibility, backup capability, expansion readiness, install complexity, resilience recommendations, current-home energy architecture, panel/service posture, inverter/system posture, battery/solar planning ranges, and reasoning graph.
- VERIFIED: Existing twin capabilities include partial provenance for products, loads, pathways, takeoffs, rules, scenario comparison, recommendations, and AI context.
- INFERRED: The current planner is a strong early residential-energy-twin foundation because most planner workflows consume structured persisted state instead of prompt-only memory.
- INFERRED: The current planner is not yet a canonical twin because there is no explicit twin aggregate, twin export protocol, complete field provenance, consent model, or enforced audience-specific view boundary.
- VERIFIED: Missing twin capabilities include measured roof geometry, usable roof area, verified field inventory, complete equipment spec authority, service territory, utility interconnection state, permit state, operational state, complete audit history, and full replayable revision lineage.
- VERIFIED: Required persistence improvements include reconciling docs/schema mismatch, expanding provenance coverage, deciding whether generated takeoffs become versioned records, and preserving scenario/advisor lineage beyond compact snapshots.
- VERIFIED: Required provenance improvements include exhaustive field-level provenance for important twin fields, source-document freshness, stronger product/spec lineage, estimate cost basis, and deployment lineage.
- VERIFIED: Required permission improvements include homeowner consent records, role-aware scoped views, access enforcement, tenant isolation, export authorization, and audit events.
- UNKNOWN: Current database contents in `apps/api/data/residential_energy_planner.sqlite3` were not inspected directly; this map is based on code, seed definitions, and docs.

# Summary

## Top 10 Architectural Strengths

1. VERIFIED: Structured persisted records exist for core home, design, load, product, pathway, scenario, and provenance domains.
2. VERIFIED: The backend separates ORM models, schemas, routers, repository access, services, and seed runtime.
3. VERIFIED: Frontend workflows consume live API data and support core editable planning surfaces.
4. VERIFIED: AI is explicitly bounded as an explanation/grounding layer rather than a source of canonical facts.
5. VERIFIED: Provenance primitives exist through source documents, data provenance, rule provenance, and provenance summaries.
6. VERIFIED: Advisor outputs include authority, classification, confidence, missing-input, limitation, and inspectability metadata.
7. VERIFIED: Scenario revisions provide initial historical planning-state lineage.
8. VERIFIED: API policy is additive-first and `/api/*` is the preferred current route base.
9. VERIFIED: Trust-boundary docs clearly state that engineering, NEC, permitting, utility, and operational authority are deferred.
10. VERIFIED: Repo-local governance and restore docs reduce ambiguity for future agent work.

## Top 10 Architectural Weaknesses

1. VERIFIED: Permission and consent are scaffolding only, not enforced behavior.
2. VERIFIED: Provenance is partial and not exhaustive at field level.
3. VERIFIED: Pricing, savings, cost, and scenario score values are placeholders or planning estimates.
4. VERIFIED: Generated takeoffs are transient and not versioned.
5. VERIFIED: NEC, permitting, utility approval, and engineering compliance are not implemented.
6. VERIFIED: `docs/DATABASE_SCHEMA.md` does not reflect the current `scenario_revisions` ORM model.
7. VERIFIED: Scoped view models are documented but not implemented as separate API contracts.
8. VERIFIED: AI context remains broad/raw for compatibility and grounding inspection.
9. INFERRED: Twin state is distributed across domain slices without a single canonical twin aggregate.
10. INFERRED: Recommendation logic is broad enough to risk service-level coupling as additional reasoning layers are added.

## Top 10 Opportunities

1. VERIFIED: The existing structured domain records can support a canonical twin contract once ownership and persistence boundaries are approved.
2. VERIFIED: Existing provenance primitives can be expanded into fuller lineage without changing the high-level architecture.
3. VERIFIED: Scenario revisions provide a starting point for richer historical planning-state lineage.
4. VERIFIED: The scoped view-model mapping provides a documented basis for future consumer, AI, contractor, and utility-safe contracts.
5. VERIFIED: The advisor inspectability model provides a foundation for keeping derived intelligence traceable.
6. VERIFIED: Existing product/source-document structures can support stronger equipment-spec provenance.
7. VERIFIED: Existing pathway and location records can support more realistic routing, siting, and roof-readiness models.
8. VERIFIED: Existing `data_origin` fields give the system a baseline for separating demo, user-created, imported, verified, derived, and placeholder records.
9. INFERRED: The current UI pages already map closely to the conceptual planner workflows, which reduces discovery cost for future interface expansion.
10. INFERRED: The clear trust-zone and authority-layer language creates a strong governance base for future implementation after Matt approves protected decisions.
