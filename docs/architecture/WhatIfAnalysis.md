# What-If Analysis

Status: Phase 3 architecture planning document
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no runtime what-if engine, schema change, API, service, calculation engine, AI agent, provider integration, product catalog, telemetry implementation, utility API, DERMS, dispatch, operational control, or authority-of-record replacement is approved or implied

## Purpose

What-If Analysis is a future derived/advisory intelligence layer over the Residential Energy Twin.

It helps compare how a modeled change may affect topology, lifecycle state, loads, production, storage, resilience, economics, product compatibility, utility readiness, permissions, provenance, confidence, and missing data.

What-If Analysis is:

- derived from the Residential Energy Twin and approved grounding layers
- advisory unless later promoted through Matt-approved deterministic, provider-backed, product-backed, source-backed, permissioned, and provenance-preserving workflows
- scenario-aware
- topology-aware
- lifecycle-aware
- permission-aware
- provenance-preserving
- confidence-bearing
- explicit about assumptions, missing data, dependencies, blockers, and review needs

What-If Analysis is not:

- a source of canonical truth
- a runtime decision engine
- a final design authority
- a financial, tax, incentive, savings, payback, or financing authority
- a contractor replacement
- an engineer replacement
- a utility approval, dispatch, or control system
- proof that a modeled change is installed, contracted, permitted, field-verified, utility-approved, eligible, or operationally ready
- DERMS, demand response, VPP, telemetry governance, or operational control

## Inputs

What-If Analysis must consume Phase 2 and Phase 3 architecture documents as constraints.

Required architecture inputs:

- `ResidentialEnergyTwinContractV1.md`
- `TopologyLifecycleDomains.md`
- `PermissionPlacement.md`
- `ProvenancePlacement.md`
- `ViewContracts.md`
- `SolarMarketProductIntelligenceGrounding.md`
- `Phase3TwinIntelligenceLayer.md`
- `StructuredSystemReasoningGraph.md`
- `ScenarioIntelligence.md`
- `InfrastructureSimulation.md`

Required input categories:

- canonical twin facts
- topology relationships and constraints
- lifecycle state
- scenario state and scenario deltas
- simulation assumptions and simulation output context where available
- product topology and product capability evidence when available
- permission boundaries
- actor-specific view constraints
- provenance and confidence metadata
- source documents and structured source records when available
- calculator, provider, quote, benchmark, and product evidence where approved
- missing-data, unknown, placeholder, estimated, modeled, quoted, verified, manufacturer-backed, contractor-reviewed, and engineer-reviewed labels

What-If Analysis must consume the Residential Energy Twin contract. It must not redefine the Twin, bypass lifecycle state, infer permission, erase provenance, invent missing facts, or promote modeled changes into canonical or operational truth.

## What-If Categories

Future what-if categories may include:

- PV
- battery
- generator
- EVSE
- HVAC/load growth
- critical loads
- outage targets
- backup strategy
- equipment selection
- financing/incentives
- future expansion
- utility participation
- DER / ADR readiness

Category expectations:

- PV what-ifs should preserve production assumptions, roof/orientation/shading inputs, product topology, interconnection assumptions, and source/provider basis where available
- battery what-ifs should preserve usable capacity, power limits, inverter/gateway constraints, backup scope, recharge assumptions, and product evidence
- generator what-ifs should preserve output, runtime, fuel, transfer, load, installation, and review assumptions without implying safe installation or code compliance
- EVSE what-ifs should distinguish added load, circuit/service impacts, managed charging assumptions, and controllability status
- HVAC/load-growth what-ifs should identify service, panel, circuit, load, backup, and future expansion impacts
- critical-load what-ifs should distinguish user-selected critical loads from verified circuit/load mapping
- outage-target what-ifs should preserve outage-duration assumptions and avoid resilience guarantees
- backup-strategy what-ifs should compare battery, generator, solar recharge, critical-load, partial-home, and whole-home planning postures without making final design claims
- equipment-selection what-ifs should cite product evidence and missing product data
- financing/incentive what-ifs should distinguish estimates, quotes, verified values, market benchmarks, incentive assumptions, and professional/tax review needs
- future-expansion what-ifs should preserve current, sandbox, proposed, contractual, and future-state separation
- utility-participation what-ifs should remain permissioned readiness planning, not utility approval, export permission, program eligibility, or enrollment
- DER / ADR readiness what-ifs should remain readiness planning only, not dispatch, DERMS, demand response, VPP, telemetry authority, or operational control

## Evaluation Dimensions

What-If Analysis may evaluate modeled changes across structured dimensions.

Evaluation dimensions include:

- topology
- lifecycle
- service/panel/pathways
- loads
- production
- storage/backup
- survivability
- recharge likelihood
- economic reasonableness
- product compatibility
- utility readiness
- permission/view implications
- provenance/confidence
- missing data

Evaluation expectations:

- topology evaluation should identify affected nodes, edges, dependencies, and constraints through the Structured System Reasoning Graph where available
- lifecycle evaluation should preserve current, sandbox, proposed, contractual, future, and historical separation
- service/panel/pathway evaluation should distinguish source-backed constraints from planning cautions
- load evaluation should distinguish recorded, estimated, measured, unknown, flexible, critical, and controllable load posture
- production evaluation should preserve calculator/provider basis, assumptions, seasonality, losses, tilt, azimuth, orientation, and shading assumptions where applicable
- storage/backup evaluation should preserve product capability, usable capacity, power, inverter/gateway, generator, and critical-load assumptions
- survivability and recharge-likelihood evaluation should remain modeled and should avoid guarantees
- economic reasonableness evaluation should distinguish assumptions, estimates, quotes, verified values, and market-benchmarked values
- product compatibility evaluation should use source-linked product capabilities and topology assignments, not AI-invented equipment capabilities
- utility-readiness evaluation should remain readiness planning, not approval, participation, dispatch, or control authority
- permission/view evaluation should identify visibility changes and whether a view or export would be allowed
- provenance/confidence evaluation should identify source basis, uncertainty, and whether confidence should change
- missing-data evaluation should identify blockers, weak assumptions, and next inputs

## Output Types

Future What-If Analysis outputs may include:

- what-if summary
- before/after delta
- affected dependencies/scenarios
- blockers
- missing data
- confidence
- review requirements
- next inputs
- advisor explanation
- affected permission/view summary
- provenance summary

Output expectations:

- what-if summaries should identify the modeled change, scenario state, lifecycle domain, and source basis
- before/after deltas should identify changed facts, assumptions, topology, lifecycle state, confidence, missing inputs, and affected outputs
- affected dependencies/scenarios should identify what might need recalculation, re-review, re-grounding, or re-labeling
- blockers should distinguish missing data, product constraints, topology constraints, permission limits, and professional review needs
- missing-data summaries should identify the inputs needed to improve or unblock analysis
- confidence summaries should explain why confidence is high, medium, low, provisional, or blocked
- review requirements should distinguish contractor, engineer, utility, AHJ, financial, tax, legal, and homeowner approval dependencies
- next inputs should guide data collection without implying that the system has authority to approve the change
- advisor explanations should remain source-linked and advisory

Outputs must not bypass permissioned views, expose hidden homeowner data, imply professional approval, imply financial certainty, imply utility approval, or imply operational control.

## Grounding Requirements

What-If Analysis outputs must preserve:

- source facts
- assumptions
- provider evidence where applicable
- calculator evidence where applicable
- product evidence
- quote/benchmark evidence where applicable
- lifecycle state
- confidence
- permissions and view filtering basis
- missing-data labels
- source attribution
- professional review requirements
- limitation text

Grounding rules:

- AI may explain what-if tradeoffs
- AI must not invent authoritative what-if outputs
- AI must not fill missing production, storage, load, product capability, economic, utility, or engineering facts
- deterministic calculators remain the source for approved calculator outputs
- trusted providers remain the source for approved provider-backed outputs
- verified product evidence remains the source for equipment capabilities
- structured quotes and benchmarks remain the source for quoted or market-benchmarked values
- contractor and engineer review boundaries must remain visible where professional review is required

When grounding is incomplete, What-If Analysis should label the output as provisional, lower confidence where appropriate, avoid false precision, or block unsupported conclusions.

## Permission And View Boundaries

What-If Analysis must not bypass view contracts.

Actor-specific what-if views should be filtered by:

- homeowner authority
- consent
- audience
- purpose
- duration
- revocation
- view contract
- data minimization
- provenance visibility
- lifecycle state
- data sensitivity

View expectations:

- homeowner views may show broad planning what-if context subject to future product and privacy decisions
- contractor views should include scoped planning facts, assumptions, missing inputs, topology, constraints, and review-relevant deltas
- engineer views should preserve evidence, assumptions, constraints, and review dependencies without implying stamped approval
- utility views should remain deferred, minimized, permissioned, source-linked, and non-operational until approved
- aggregator views should remain deferred and must not imply enrollment, dispatch, DERMS, VPP, or operational control
- supplier/manufacturer views should be minimized to product-relevant context and should not expose unnecessary homeowner or scenario data
- AI advisor views should be grounded, source-linked, and non-authoritative
- audit views should preserve permission, provenance, confidence, lifecycle, view filtering, assumptions, and limitation context

No what-if view should infer consent, bypass revocation, flatten audience boundaries, treat account role as permission, or treat broad internal access as a permissioned export.

## Missing Data Behavior

Missing data is a first-class what-if input and output.

Missing data should:

- block unsupported what-if conclusions
- lower confidence where appropriate
- identify required next inputs
- distinguish unknown from estimated
- distinguish user-entered from verified
- distinguish placeholder from source-backed
- distinguish modeled assumptions from measured or verified values
- prevent false precision
- identify affected dependencies, scenarios, recommendations, views, and exports

Examples of missing data that may affect what-if analysis:

- unknown service capacity
- unknown panel constraints
- unknown circuit mapping
- unknown load measurement
- unknown critical-load priority
- unknown outage-duration target
- unknown roof geometry, tilt, azimuth, shading, or irradiance basis
- unknown product capability
- unknown usable battery capacity or power limits
- unknown generator runtime or transfer constraints
- unknown EVSE controllability or flexible-load status
- unknown utility/interconnection context
- missing quote, benchmark, incentive, or financing evidence
- missing source document
- missing field verification
- missing contractor or engineer review
- missing permission basis

What-If Analysis should not hide missing data behind advisory language. AI explanations should surface missing-data markers rather than inventing values, smoothing uncertainty, or implying completeness.

## Lifecycle And Scenario Boundaries

What-If Analysis must preserve lifecycle boundaries from `TopologyLifecycleDomains.md` and scenario boundaries from `ScenarioIntelligence.md`.

What-if reasoning should distinguish:

- current deployed state
- sandbox planning state
- proposed pathway state
- saved scenario revision state
- future contractor-reviewed state
- future contractual state
- future field-verified state
- future utility-reviewed state
- future operational topology
- future expansion or replacement state

What-if outputs must not imply that a sandbox, proposed, future, modeled, or advisory change is installed, contracted, field-verified, utility-approved, dispatchable, or operationally controllable.

Future promotion from modeled what-if output to stronger authority requires explicit Matt-approved source-backed workflows. What-If Analysis must not infer promotion from AI text, scenario ranking, design status, UI visibility, account role, broad API access, or recommendation selection.

## Non-Goals

This document does not approve:

- runtime what-if engine
- runtime what-if models
- schemas
- migrations
- APIs
- services
- calculation engines
- AI agents
- provider integrations
- product catalogs
- spec-sheet ingestion
- telemetry implementation or governance
- utility APIs
- financial, tax, incentive, savings, payback, or financing authority
- final engineering design
- permit-ready design
- NEC, AHJ, permitting, or stamped-engineering authority
- contractor or engineer authority replacement
- utility approval or participation authority
- DERMS
- dispatch
- demand response
- VPP or aggregator participation
- operational control
- critical-infrastructure, NERC/CIP, utility, government, or national-defense compliance claims

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating runtime what-if engines, models, tables, APIs, services, or exports
- defining what-if schemas, scoring rules, ranking rules, or recommendation rules
- defining confidence, provenance, economic, resilience, survivability, recharge, production, compatibility, readiness, or constraint-impact rules as runtime behavior
- creating what-if-backed scenario intelligence, simulations, deterministic exports, or AI advisor behaviors
- integrating provider calculators, product catalogs, manufacturer data, quote data, benchmarks, utility APIs, telemetry, or operational systems
- creating permission-filtered what-if views, contractor packets, engineer packets, utility packets, aggregator packets, or audit APIs
- changing trust language that could imply compliance, approval, safety, savings, eligibility, authorization, professional review, utility approval, operational readiness, or operational control

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
- `docs/architecture/Phase3TwinIntelligenceLayer.md`
- `docs/architecture/StructuredSystemReasoningGraph.md`
- `docs/architecture/ScenarioIntelligence.md`
- `docs/architecture/InfrastructureSimulation.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/topology-intelligence/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

What-If Analysis defines a future derived/advisory planning layer for evaluating modeled changes to the Residential Energy Twin. It consumes the Phase 2 contract, topology/lifecycle states, permissions, provenance, view contracts, grounding layers, Phase 3 Twin Intelligence boundaries, Structured System Reasoning Graph, Scenario Intelligence, and Infrastructure Simulation while preserving source facts, assumptions, evidence, lifecycle state, confidence, permissions, missing data, and professional review requirements. It does not approve runtime what-if engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS, dispatch, operational control, or authority-of-record replacement.
