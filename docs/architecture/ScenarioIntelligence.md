# Scenario Intelligence

Status: Phase 3 architecture planning document
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no runtime scenario model, schema change, API, service, calculation engine, AI agent, provider integration, product catalog, telemetry implementation, utility API, DERMS, dispatch, operational control, or authority-of-record replacement is approved or implied

## Purpose

Scenario Intelligence is a future derived/advisory planning layer over the Residential Energy Twin.

It compares possible states of the home energy system so homeowners, contractors, engineers, advisors, auditors, and future permissioned actors can understand differences, assumptions, constraints, missing data, and tradeoffs before decisions are made through approved authority channels.

Scenario Intelligence is:

- derived from the Residential Energy Twin and approved grounding layers
- advisory unless later promoted through Matt-approved deterministic, provider-backed, product-backed, source-backed, permissioned, and provenance-preserving workflows
- topology-aware
- lifecycle-aware
- permission-aware
- provenance-preserving
- confidence-bearing
- view-contract bounded
- explicit about missing data and professional review needs

Scenario Intelligence is not:

- a source of canonical truth
- a final design authority
- a financial authority
- a tax, incentive, savings, or financing authority
- a contractor replacement
- an engineer replacement
- a utility approval or dispatch system
- DERMS, demand response, VPP, telemetry, or operational control
- proof that a scenario is installed, contracted, permitted, field-verified, utility-approved, or operationally ready

## Inputs

Scenario Intelligence must consume Phase 2 and Phase 3 architecture documents as constraints.

Required architecture inputs:

- `ResidentialEnergyTwinContractV1.md`
- `TopologyLifecycleDomains.md`
- `PermissionPlacement.md`
- `ProvenancePlacement.md`
- `ViewContracts.md`
- `SolarMarketProductIntelligenceGrounding.md`
- `Phase3TwinIntelligenceLayer.md`
- `StructuredSystemReasoningGraph.md`

Required input categories:

- canonical twin facts
- current deployed, sandbox, proposed, contractual, future, and historical scenario state
- topology and lifecycle states
- product topology and product capability evidence when available
- permission boundaries
- actor-specific view constraints
- provenance and confidence metadata
- source documents and structured source records when available
- calculator, provider, quote, benchmark, and product evidence where approved
- missing-data, unknown, placeholder, estimated, modeled, quoted, verified, manufacturer-backed, contractor-reviewed, and engineer-reviewed labels

Scenario Intelligence must consume the Residential Energy Twin contract. It must not redefine the Twin, bypass lifecycle state, infer permission, erase provenance, invent missing facts, or promote advisory comparison text into canonical state.

## Scenario Types

Future scenario categories may include:

- current deployed scenario
- sandbox scenario
- proposed scenario
- contractual scenario
- future scenario
- resilience scenario
- solar production scenario
- storage/backup scenario
- generator scenario
- EVSE / flexible-load scenario
- economic/market scenario
- DER / ADR readiness scenario
- utility participation readiness scenario

Scenario category expectations:

- current deployed scenarios describe the recorded current planning state and are not automatically field-verified or operational
- sandbox scenarios support what-if exploration and cannot create commitments by themselves
- proposed scenarios organize planning choices and remain non-authoritative until later reviewed or contracted through approved workflows
- contractual scenarios require future source-backed contract evidence before they carry contractual context
- future scenarios model expansion paths and must not imply installation, approval, or readiness
- resilience, solar production, storage/backup, generator, EVSE, and flexible-load scenarios must preserve assumptions, source basis, product topology, and missing inputs
- economic/market scenarios must distinguish estimates, quotes, verified values, and market-benchmarked values
- DER / ADR and utility participation readiness scenarios must remain readiness planning only, not enrollment, approval, dispatch, or operational control

## Scenario Comparison

Scenario Intelligence may compare scenarios across structured dimensions.

Comparison dimensions include:

- topology differences
- lifecycle-state differences
- equipment differences
- product capability differences
- load differences
- critical-load coverage differences
- production assumptions
- storage/backup assumptions
- generator assumptions
- EVSE / flexible-load assumptions
- cost/economic assumptions
- quote, benchmark, incentive, payback, lease, loan, or cash assumptions when source-backed
- permission differences
- actor-specific view differences
- utility-readiness differences
- DER / ADR readiness differences
- missing-data differences
- provenance/confidence differences
- professional review requirements

Comparison expectations:

- compare current, sandbox, proposed, contractual, future, and historical states without collapsing them
- identify which facts, assumptions, and evidence changed
- identify which outputs may be stale after a scenario changes
- identify dependencies and constraints through the Structured System Reasoning Graph where available
- identify missing inputs that block or weaken conclusions
- distinguish deterministic outputs from advisory explanation
- distinguish source-backed values from estimated or modeled values
- preserve permission and view boundaries for every compared scenario

Scenario comparison should explain tradeoffs. It should not rank scenarios as final decisions unless a future Matt-approved decision model and authority boundary supports that behavior.

## Grounding Requirements

Scenario outputs must preserve:

- input facts
- assumptions
- calculator outputs where applicable
- provider outputs where applicable
- product evidence
- quote evidence where applicable
- benchmark evidence where applicable
- confidence
- source attribution
- missing-data labels
- lifecycle state
- topology basis
- permission/view filtering basis
- professional review requirements
- limitation text

Grounding rules:

- AI may explain scenario tradeoffs
- AI must not invent authoritative values
- AI must not fill missing pricing, product capability, production, resilience, utility, or engineering facts
- deterministic calculators remain the source for approved calculator outputs
- trusted providers remain the source for approved provider-backed outputs
- verified product evidence remains the source for equipment capabilities
- structured quotes and benchmarks remain the source for quoted or market-benchmarked values
- contractor and engineer review boundaries must remain visible where professional review is required

When grounding is incomplete, Scenario Intelligence should label the output as provisional, reduce confidence where appropriate, or block unsupported conclusions.

## Scenario Outputs

Future Scenario Intelligence outputs may include:

- scenario summary
- scenario delta
- constraint summary
- missing-data summary
- confidence summary
- resilience summary
- economic reasonableness summary
- product compatibility summary
- utility-readiness summary
- DER / ADR readiness summary
- recommended next-inputs list
- advisor explanation
- professional review dependency summary
- permission/view visibility summary
- provenance summary

Output expectations:

- summaries should cite the scenario state and lifecycle domain
- deltas should identify changed facts, assumptions, evidence, topology, lifecycle state, confidence, and missing inputs
- constraint summaries should distinguish hard source-backed constraints from planning cautions
- resilience summaries should avoid guarantees and preserve input assumptions
- economic summaries should distinguish estimated, quoted, verified, and benchmarked values
- product compatibility summaries should cite product evidence and missing product data
- utility-readiness summaries should remain readiness planning, not utility approval or participation authority
- next-input lists should identify missing information needed to improve confidence or unblock conclusions
- advisor explanations should remain source-linked and advisory

Outputs must not bypass permissioned views, expose hidden homeowner data, imply professional approval, imply financial certainty, or imply operational control.

## Impact And Tradeoff Language

Scenario Intelligence may explain planning tradeoffs when the source basis and limits remain visible.

Future tradeoff examples include:

- backup duration vs cost
- battery capacity vs critical-load coverage
- solar production vs recharge likelihood
- generator backup vs battery backup
- panel/service constraints vs future expansion
- lease vs loan vs cash assumptions
- product compatibility vs preferred design
- current installation vs future-readiness
- resilience target vs missing load data
- solar/storage sizing posture vs roof, orientation, shading, and product assumptions
- utility participation readiness vs permission, provenance, interconnection, and security prerequisites

Tradeoff language must:

- identify the source facts and assumptions used
- identify missing data and uncertainty
- preserve confidence and provenance
- avoid guarantees about savings, resilience, eligibility, compliance, safety, approval, or operational readiness
- distinguish planning guidance from final design, quote, contract, permit, utility, financial, or engineering authority

Scenario Intelligence may recommend next inputs or review steps. It must not present advisory tradeoffs as final approval or professional judgment.

## Permission And View Boundaries

Scenario Intelligence must not bypass view contracts.

Actor-specific scenario views should be filtered by:

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

Scenario view expectations:

- homeowner views may compare broad planning options subject to future product and privacy decisions
- contractor views should include scoped planning facts, assumptions, missing inputs, topology, constraints, and review-relevant deltas
- engineer views should preserve evidence, assumptions, constraints, and review dependencies without implying stamped approval
- utility views should remain deferred, minimized, permissioned, source-linked, and non-operational until approved
- aggregator views should remain deferred and must not imply enrollment, dispatch, DERMS, VPP, or operational control
- supplier/manufacturer views should be minimized to product-relevant context and should not expose unnecessary homeowner or scenario data
- AI advisor views should be grounded, source-linked, and non-authoritative
- audit views should preserve permission, provenance, confidence, lifecycle, view filtering, and limitation context

No scenario view should infer consent, bypass revocation, flatten audience boundaries, treat account role as permission, or treat broad internal access as a permissioned export.

## Lifecycle Boundaries

Scenario Intelligence must preserve lifecycle boundaries from `TopologyLifecycleDomains.md`.

Scenario reasoning should distinguish:

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

Scenario comparison must not imply that a sandbox, proposed, future, or advisory scenario is installed, contracted, field-verified, utility-approved, dispatchable, or operationally controllable.

Future promotion between scenario states requires explicit Matt-approved source-backed workflows. Scenario Intelligence must not infer promotion from AI text, scenario ranking, design status, UI visibility, account role, broad API access, or recommendation selection.

## Non-Goals

This document does not approve:

- runtime scenario engine
- runtime scenario models
- scenario database schemas
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
- utility dispatch
- DERMS
- demand response
- VPP or aggregator participation
- operational control
- critical-infrastructure, NERC/CIP, utility, government, or national-defense compliance claims

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating runtime scenario engines, models, tables, APIs, services, or exports
- defining scenario comparison schemas or scoring rules
- defining confidence, provenance, economic, resilience, survivability, compatibility, readiness, or impact-propagation rules as runtime behavior
- creating scenario-backed simulations, what-if analysis, deterministic exports, or AI advisor behaviors
- integrating provider calculators, product catalogs, manufacturer data, quote data, benchmarks, utility APIs, telemetry, or operational systems
- creating permission-filtered scenario views, contractor packets, engineer packets, utility packets, aggregator packets, or audit APIs
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
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/topology-intelligence/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

Scenario Intelligence defines a future derived/advisory planning layer for comparing possible Residential Energy Twin states. It consumes the Phase 2 contract, topology/lifecycle states, permissions, provenance, view contracts, grounding layers, Phase 3 Twin Intelligence boundaries, and Structured System Reasoning Graph to compare scenarios while preserving source facts, assumptions, evidence, confidence, missing data, lifecycle state, permission boundaries, and professional review requirements. It does not approve runtime scenario engines, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS, dispatch, operational control, or authority-of-record replacement.
