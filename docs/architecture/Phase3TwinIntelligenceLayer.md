# Phase 3 Twin Intelligence Layer

Status: Phase 3 architecture planning document
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no runtime code, schema change, API, service, calculation engine, AI agent, provider integration, product catalog, telemetry implementation, utility API, DERMS, dispatch, operational-control, or authority-of-record replacement is approved or implied

## Purpose

Phase 3 defines explainable intelligence built on top of the Residential Energy Twin.

The Twin Intelligence Layer should consume canonical twin facts, topology/lifecycle state, permissions, provenance, actor-specific view constraints, and future grounding layers to produce derived and advisory planning intelligence.

Phase 3 intelligence is:

- explainable intelligence built on the Residential Energy Twin
- derived or advisory unless explicitly promoted through approved deterministic, provider-backed, or source-backed workflows
- governed by provenance, confidence, permissions, and view contracts
- traceable to structured facts, assumptions, missing data, and grounding evidence
- useful for planning, scenario comparison, simulation, dependency reasoning, and advisor explanations

Phase 3 intelligence is not:

- a runtime control layer
- an authority of record
- a source of canonical home facts
- a replacement for contractor review
- a replacement for engineer review where required
- a replacement for utility, AHJ, permitting, financial, tax, or legal authority
- DERMS, dispatch, telemetry, operational control, or grid-service participation

## Inputs From Phase 2

Phase 3 must consume the Phase 2 architecture docs as constraints, not bypass them.

Required foundations:

- `ResidentialEnergyTwinContractV1.md`: canonical aggregate boundary, identity, source-of-truth, lifecycle, permission, provenance, utility, and operational-control boundaries
- `TopologyLifecycleDomains.md`: current, sandbox, proposed, revision, future contractual, field-verified, utility-reviewed, and operational topology separation
- `PermissionPlacement.md`: homeowner authority, permission attachment points, scope, duration, revocation, and future privacy-enforcement compatibility
- `ProvenancePlacement.md`: source, evidence, confidence, verification, lifecycle, view/export, and audit/security provenance placement
- `ViewContracts.md`: actor-specific, permission-filtered, provenance-preserving view expectations
- `SolarMarketProductIntelligenceGrounding.md`: future solar production, market/economic, and verified product intelligence grounding boundaries

Phase 3 intelligence must consume:

- canonical twin facts
- topology and lifecycle states
- permission boundaries
- provenance and confidence metadata
- actor-specific view constraints
- solar production grounding
- market/economic grounding
- verified product intelligence grounding
- missing-data, assumption, placeholder, inferred, and unknown labels

No Phase 3 output may hide missing data, erase uncertainty, or elevate advisory text above structured state and source provenance.

## Structured System Reasoning Graph

The Structured System Reasoning Graph is a derived reasoning graph that maps relationships, constraints, dependencies, and missing data across the Residential Energy Twin.

Future graph nodes may include:

- service
- panels
- circuits
- loads
- PV
- batteries
- inverters
- gateways / transfer equipment
- generators
- EVSE / flexible loads
- utility relationships
- constraints
- dependencies
- missing data
- source/provenance references
- lifecycle states

The graph should explain how recorded facts and topology relationships affect recommendations, simulations, scenario comparisons, and advisor outputs.

Graph boundaries:

- derived from the Residential Energy Twin
- not a new source of canonical truth
- not proof of field verification, compliance, utility approval, or operational readiness
- must preserve provenance, confidence, assumptions, missing data, and lifecycle state
- must respect permission and view boundaries
- must not expose fields to an actor that the relevant view contract would exclude

## Scenario Intelligence

Scenario intelligence explains planning tradeoffs across scenarios without making scenarios authoritative.

Future scenario intelligence may compare:

- current deployed vs sandbox
- proposed vs contractual
- future scenario vs current
- product option alternatives
- solar, storage, generator, EVSE, and flexible-load combinations
- rate, incentive, and economic assumptions when source-backed
- resilience, backup, recharge, and outage tradeoffs
- utility/interconnection readiness assumptions when permissioned and sourced

Scenario intelligence should identify:

- source facts used
- topology/lifecycle state of each scenario
- relevant product topology
- deterministic calculator/provider outputs where approved
- estimated, modeled, quoted, verified, or benchmarked values
- missing inputs
- assumptions and limitations
- confidence and provenance posture
- affected view/permission boundaries

Deterministic calculators, provider-backed sources, structured quotes, benchmarks, and verified product evidence remain the source for authoritative numeric outputs. AI may explain and compare tradeoffs, but it must not invent unknown values, fill missing pricing, infer verified production, or create canonical facts.

## Infrastructure Simulation

Infrastructure simulation is planning simulation, not operational dispatch.

Possible future simulations include:

- critical-load survivability
- battery discharge duration
- battery recharge likelihood
- solar recharge modeling
- outage endurance
- load-growth impacts
- service/panel/pathway constraint impacts
- seasonal solar production variation
- economic sensitivity analysis

Simulation outputs should include:

- structured inputs
- assumptions
- calculation basis or provider reference where applicable
- product topology used
- lifecycle state used
- provenance
- confidence
- missing inputs
- limitations
- actor-specific view constraints

Missing data must be surfaced, not hidden. Simulation remains advisory unless backed by approved verified deterministic outputs within a defined scope. Simulation is not a device-control instruction, operational schedule, utility command, dispatch plan, engineering approval, savings guarantee, or resilience guarantee.

## What-If Analysis

What-if analysis should produce planning guidance by showing how a change affects dependencies, constraints, scenarios, and missing data.

Supported future what-if categories may include:

- adding EV charger
- adding heat pump / HVAC load
- adding battery
- adding generator
- adding PV
- changing critical loads
- changing outage-duration target
- changing financing / incentive assumptions
- changing equipment selection
- changing future expansion path

What-if analysis should show:

- affected topology nodes
- upstream and downstream dependencies
- calculations that need rerun
- scenarios affected
- assumptions changed
- missing inputs introduced or resolved
- confidence changes
- provenance changes
- permission/view implications
- professional review still required

What-if analysis is planning guidance. It is not final engineering approval, contractor approval, utility approval, procurement approval, financing advice, tax advice, or operational authorization.

## Dependency Reasoning And Impact Propagation

Phase 3 should reason about upstream and downstream dependencies before presenting recommendations.

Dependency categories may include:

- service and panel constraints
- circuit/load dependencies
- battery/inverter/gateway/generator dependencies
- PV production and inverter constraints
- equipment compatibility
- critical-load dependencies
- utility/interconnection dependencies
- permit, contractor, and engineering review dependencies
- lifecycle state changes
- permission, provenance, and view-contract dependencies

Impact propagation should identify affected:

- calculations
- scenarios
- views
- recommendations
- costs/economics
- resilience assumptions
- utility readiness
- product compatibility
- provenance/confidence status
- missing-data requirements
- actor-specific exports

When one fact changes, Phase 3 should identify what might need recalculation, re-review, re-grounding, or re-labeling. It should not silently preserve stale recommendations or imply that all dependent outputs remain valid.

## Deployment Sequencing

Deployment sequencing is advisory sequencing for planning and execution readiness.

Future sequencing guidance may include:

- panel/service constraints before downstream upgrades
- topology cleanup before battery or EVSE planning
- verified equipment data before production or resilience claims
- utility/interconnection readiness before export or participation assumptions
- source-backed solar production assumptions before solar recharge confidence increases
- contractor/engineer review before authority-of-record claims
- provenance and view-contract readiness before external exports

Sequencing boundaries:

- not project-management implementation
- not construction management
- not a replacement for contractor judgment
- not engineering approval
- not procurement authorization
- not a permitting or AHJ workflow
- not utility approval
- not operational control

## Future-State Architecture Modeling

Phase 3 can model the evolution of a home's energy architecture across lifecycle states.

Future modeling may include:

- Day 0 / Day 1 / Day 2 evolution
- current deployed state
- sandbox state
- contractual state
- future scenario state
- expansion paths
- resilience upgrades
- DER/ADR readiness path
- utility participation readiness path
- future operational-control separation

Future-state models should preserve:

- lifecycle state
- source/provenance basis
- confidence
- missing inputs
- assumptions
- explicit current vs proposed vs future separation
- view/permission boundaries
- professional review requirements

Future-state architecture modeling must not imply that future scenarios are installed, field-verified, utility-approved, operationally controllable, financially guaranteed, or professionally approved.

## Advisor Traceability

Every advisory output should be traceable.

Minimum traceability requirements:

- what Twin facts were used
- what topology/lifecycle states were used
- what assumptions were used
- what was estimated
- what was missing
- what provider/calculator/product evidence was used
- what confidence applies
- what provenance supports the output
- what permissions or view filters affected the output
- what professional review may still be required
- what limitations apply

Traceability must be visible enough for homeowner, contractor, engineer, AI, audit, and future utility-safe views to preserve appropriate authority boundaries.

AI explanations should cite structured basis and limitations. AI should not be allowed to make unsupported claims when traceability is incomplete.

## Deterministic Reasoning Exports

Future deterministic reasoning exports may package structured planning intelligence for review, comparison, or audit.

Future export contents may include:

- structured reasoning summaries
- scenario comparison outputs
- assumptions
- inputs
- outputs
- provenance
- confidence
- missing-data labels
- warnings and limitations
- actor-specific view filtering
- revision identity
- lifecycle state
- rule/provider/product evidence references where applicable

Export expectations:

- deterministic and auditable where possible
- permission-filtered
- provenance-preserving
- view-contract bounded
- explicit about missing data and assumptions
- explicit about professional review requirements

Exports must not bypass permissions, expose hidden homeowner data, imply operational control, imply utility approval, or turn advisory intelligence into authority of record.

## Phase 3 Boundaries And Non-Goals

Phase 3 planning does not approve:

- runtime implementation
- schema changes
- API services
- service-layer implementation
- provider integrations
- spec-sheet ingestion
- product catalog implementation
- AI engineering automation
- financial, tax, or financing authority
- contractor or engineer authority replacement
- telemetry governance implementation
- utility participation APIs
- utility submission authority
- tariff or incentive authority
- DERMS
- dispatch
- demand response
- VPP or aggregator participation
- operational control
- critical-infrastructure, NERC/CIP, utility, government, or national-defense compliance claims

Phase 3 intelligence remains derived/advisory unless a later Matt-approved implementation creates deterministic, provider-backed, source-backed, permissioned, and provenance-preserving promotion workflows.

## Suggested Future Subdocs

Future architecture subdocuments may include:

- `StructuredSystemReasoningGraph.md`
- `ScenarioIntelligence.md`
- `InfrastructureSimulation.md`
- `AdvisorTraceability.md`
- `DeterministicReasoningExports.md`

Do not create these subdocs until Matt approves the next architecture slice.

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating runtime reasoning graph models, tables, APIs, services, or exports
- implementing simulations, calculations, provider integrations, product catalogs, spec-sheet workflows, or deterministic reasoning engines
- implementing AI agents, AI engineering automation, advisory automation with write authority, or canonical fact promotion
- defining confidence, provenance, scoring, economic, resilience, survivability, or readiness rules as runtime behavior
- creating permission-filtered exports, contractor packets, engineer packets, utility packets, or audit APIs
- creating utility participation APIs, DERMS, dispatch, demand response, VPP, telemetry governance, or operational-control semantics
- replacing contractor, engineer, AHJ, utility, financial, tax, or legal authority
- changing trust language that could imply compliance, approval, safety, savings, eligibility, authorization, professional review, utility approval, or operational readiness

## Sources / Provenance

- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/TopologyLifecycleDomains.md`
- `docs/architecture/PermissionPlacement.md`
- `docs/architecture/ProvenancePlacement.md`
- `docs/architecture/ViewContracts.md`
- `docs/architecture/SolarMarketProductIntelligenceGrounding.md`
- `docs/architecture/COGNITION_LAYERS.md`
- `docs/architecture/CANONICAL_TERMINOLOGY.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/canonical-authority-discipline/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `.codex/project-skills/topology-intelligence/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

Phase 3 Twin Intelligence defines explainable, traceable, derived planning intelligence over the Residential Energy Twin. It consumes Phase 2 canonical facts, topology/lifecycle states, permissions, provenance, views, and grounding layers to support reasoning graphs, scenario intelligence, simulation, what-if analysis, dependency reasoning, sequencing, future-state modeling, traceable advisor outputs, and deterministic reasoning exports. It does not approve runtime implementation, authority replacement, provider integrations, utility participation, DERMS, dispatch, telemetry, or operational control.
