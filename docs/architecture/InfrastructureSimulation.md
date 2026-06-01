# Infrastructure Simulation

Status: Phase 3 architecture planning document
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no runtime simulation model, schema change, API, service, calculation engine, AI agent, provider integration, product catalog, telemetry implementation, utility API, DERMS, dispatch, operational control, or authority-of-record replacement is approved or implied

## Purpose

Infrastructure Simulation is a future derived/advisory planning layer over the Residential Energy Twin.

It is used to estimate how a home energy system may behave under modeled assumptions across resilience, production, storage, loads, topology constraints, economic sensitivity, DER / ADR readiness, and future-state planning.

Infrastructure Simulation is:

- derived from the Residential Energy Twin and approved grounding layers
- advisory unless later promoted through Matt-approved deterministic, provider-backed, product-backed, source-backed, permissioned, and provenance-preserving workflows
- scenario-aware
- topology-aware
- lifecycle-aware
- permission-aware
- provenance-preserving
- confidence-bearing
- explicit about assumptions, missing data, and review needs

Infrastructure Simulation is not:

- operational dispatch
- real-time control
- a final engineering study
- a financial guarantee
- a utility control system
- a contractor replacement
- an engineer replacement
- proof of safety, compliance, utility approval, resilience, savings, or operational readiness
- DERMS, demand response, VPP, telemetry governance, or operational control

## Inputs

Infrastructure Simulation must consume Phase 2 and Phase 3 architecture documents as constraints.

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

Required input categories:

- canonical twin facts
- topology relationships and constraints
- lifecycle state
- scenario state and scenario deltas
- product topology and product capability evidence when available
- permission boundaries
- actor-specific view constraints
- provenance and confidence metadata
- source documents and structured source records when available
- calculator, provider, quote, benchmark, and product evidence where approved
- missing-data, unknown, placeholder, estimated, modeled, quoted, verified, manufacturer-backed, contractor-reviewed, and engineer-reviewed labels

Infrastructure Simulation must consume the Residential Energy Twin contract. It must not redefine the Twin, bypass lifecycle state, infer permission, erase provenance, invent missing facts, or promote modeled behavior into canonical or operational truth.

## Simulation Types

Future simulation categories may include:

- critical-load survivability
- outage endurance
- battery discharge duration
- battery recharge likelihood
- solar recharge modeling
- seasonal production variation
- generator runtime support
- EVSE / flexible-load impact
- load-growth impact
- service/panel/pathway constraint impact
- economic sensitivity analysis
- DER / ADR readiness simulation
- future-state expansion simulation

Simulation category expectations:

- critical-load survivability should identify load assumptions, outage-duration assumptions, storage/generator assumptions, and missing load data
- outage endurance should avoid guarantees and preserve the modeled basis for the estimate
- battery discharge duration should depend on modeled load, usable capacity, inverter/gateway constraints, efficiency assumptions, and product evidence where available
- battery recharge likelihood should distinguish modeled solar recharge assumptions from verified production
- solar recharge modeling should use approved solar production grounding when available and preserve weather, seasonality, orientation, tilt, losses, and shading assumptions
- seasonal production variation should remain modeled unless backed by approved provider outputs or verified production records
- generator runtime support should preserve fuel, runtime, output, transfer, and load assumptions without implying safe installation or code compliance
- EVSE / flexible-load impact should distinguish managed flexibility assumptions from control authority
- load-growth impact should identify upstream service, panel, circuit, equipment, and future expansion constraints
- service/panel/pathway constraint impact should preserve topology and lifecycle state and require professional review where applicable
- economic sensitivity analysis should distinguish assumptions, estimates, quotes, verified values, and market-benchmarked values
- DER / ADR readiness simulation should remain readiness planning only, not enrollment, dispatch, or operational control
- future-state expansion simulation should preserve current, sandbox, proposed, contractual, and future-state separation

## Grounding Requirements

Simulation outputs must preserve:

- input facts
- assumptions
- calculator outputs where applicable
- provider outputs where applicable
- product evidence
- topology dependencies
- lifecycle state
- scenario state
- confidence
- source attribution
- missing-data labels
- professional review requirements
- limitation text

Grounding rules:

- AI may explain simulations
- AI must not invent authoritative simulation outputs
- AI must not fill missing production, storage, load, product capability, economic, utility, or engineering facts
- deterministic calculators remain the source for approved calculator outputs
- trusted providers remain the source for approved provider-backed outputs
- verified product evidence remains the source for equipment capabilities
- structured quotes and benchmarks remain the source for quoted or market-benchmarked values
- contractor and engineer review boundaries must remain visible where professional review is required

When grounding is incomplete, Infrastructure Simulation should label the output as provisional, lower confidence where appropriate, avoid false precision, or block unsupported simulation claims.

## Simulation Outputs

Future Infrastructure Simulation outputs may include:

- simulation summary
- assumptions summary
- survivability estimate
- recharge likelihood estimate
- outage endurance estimate
- constraint impact summary
- confidence summary
- missing-data summary
- recommended next-inputs list
- advisor explanation
- topology dependency summary
- professional review dependency summary
- permission/view visibility summary
- provenance summary

Output expectations:

- simulation summaries should identify the modeled scenario, lifecycle domain, and source basis
- assumptions summaries should separate user-entered, estimated, defaulted, modeled, source-backed, and verified inputs
- survivability estimates should preserve load, storage, generator, and outage assumptions and avoid guarantees
- recharge likelihood estimates should preserve solar production, seasonality, weather, storage, and load assumptions
- outage endurance estimates should avoid implying a guaranteed duration under real outage conditions
- constraint impact summaries should distinguish hard source-backed constraints from planning cautions
- confidence summaries should explain why confidence is high, medium, low, provisional, or blocked
- missing-data summaries should identify the inputs needed to improve or unblock the simulation
- advisor explanations should remain source-linked and advisory

Outputs must not bypass permissioned views, expose hidden homeowner data, imply professional approval, imply financial certainty, imply utility approval, or imply operational control.

## Missing Data Behavior

Missing data is a first-class simulation input.

Missing data should:

- block unsupported simulation claims
- lower confidence where appropriate
- identify required next inputs
- distinguish unknown from estimated
- distinguish user-entered from verified
- distinguish placeholder from source-backed
- distinguish modeled assumptions from measured or verified values
- prevent false precision
- identify affected scenarios, conclusions, recommendations, views, and exports

Examples of missing data that may affect simulations:

- unknown critical-load list
- unknown circuit mapping
- unknown load measurement
- unknown service capacity
- unknown panel constraints
- unknown roof geometry, tilt, azimuth, shading, or irradiance basis
- unknown product capability
- unknown usable battery capacity or power limits
- unknown generator runtime or transfer constraints
- unknown EVSE controllability or flexible-load status
- unknown utility/interconnection context
- missing source document
- missing field verification
- missing contractor or engineer review
- missing permission basis

Infrastructure Simulation should not hide missing data behind advisory language. AI explanations should surface missing-data markers rather than inventing values, smoothing uncertainty, or implying completeness.

## Permission And View Boundaries

Infrastructure Simulation must not bypass view contracts.

Actor-specific simulation views should be filtered by:

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

Simulation view expectations:

- homeowner views may show broad planning simulation context subject to future product and privacy decisions
- contractor views should include scoped planning facts, assumptions, missing inputs, topology, constraints, and review-relevant simulation outputs
- engineer views should preserve evidence, assumptions, constraints, and review dependencies without implying stamped approval
- utility views should remain deferred, minimized, permissioned, source-linked, and non-operational until approved
- aggregator views should remain deferred and must not imply enrollment, dispatch, DERMS, VPP, or operational control
- supplier/manufacturer views should be minimized to product-relevant context and should not expose unnecessary homeowner or simulation data
- AI advisor views should be grounded, source-linked, and non-authoritative
- audit views should preserve permission, provenance, confidence, lifecycle, view filtering, assumptions, and limitation context

No simulation view should infer consent, bypass revocation, flatten audience boundaries, treat account role as permission, or treat broad internal access as a permissioned export.

## Lifecycle And Scenario Boundaries

Infrastructure Simulation must preserve lifecycle boundaries from `TopologyLifecycleDomains.md` and scenario boundaries from `ScenarioIntelligence.md`.

Simulation reasoning should distinguish:

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

Simulation outputs must not imply that a sandbox, proposed, future, modeled, or advisory state is installed, contracted, field-verified, utility-approved, dispatchable, or operationally controllable.

Future promotion from modeled simulation output to stronger authority requires explicit Matt-approved source-backed workflows. Infrastructure Simulation must not infer promotion from AI text, scenario ranking, design status, UI visibility, account role, broad API access, or recommendation selection.

## Utility, DER, ADR, And Operational-Control Separation

Infrastructure Simulation may support future DER / ADR readiness planning by modeling topology, product capability, load flexibility, utility relationship context, permission, provenance, and missing data.

Readiness simulation must not imply:

- utility approval
- interconnection approval
- tariff authority
- program eligibility
- aggregator enrollment
- VPP participation
- demand response enrollment
- DERMS integration
- dispatch authority
- telemetry authority
- device command authority
- operational control

Future operational-control simulation, if ever approved, must remain a separate trust domain with separate contracts, permissions, telemetry governance, cybersecurity posture, auditability, and authority rules.

## Non-Goals

This document does not approve:

- runtime simulation engine
- runtime simulation models
- simulation schemas
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

- creating runtime simulation engines, models, tables, APIs, services, or exports
- defining simulation schemas or scoring rules
- defining confidence, provenance, economic, resilience, survivability, recharge, production, compatibility, readiness, or constraint-impact rules as runtime behavior
- creating simulation-backed scenario intelligence, what-if analysis, deterministic exports, or AI advisor behaviors
- integrating provider calculators, product catalogs, manufacturer data, quote data, benchmarks, utility APIs, telemetry, or operational systems
- creating permission-filtered simulation views, contractor packets, engineer packets, utility packets, aggregator packets, or audit APIs
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
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/topology-intelligence/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

Infrastructure Simulation defines a future derived/advisory planning layer for estimating modeled Residential Energy Twin behavior across resilience, production, storage, loads, topology constraints, economic sensitivity, DER / ADR readiness, and future-state planning. It consumes the Phase 2 contract, topology/lifecycle states, permissions, provenance, view contracts, grounding layers, Phase 3 Twin Intelligence boundaries, Structured System Reasoning Graph, and Scenario Intelligence while preserving source facts, assumptions, evidence, confidence, missing data, lifecycle state, permission boundaries, and professional review requirements. It does not approve runtime simulation engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS, dispatch, operational control, or authority-of-record replacement.
