# Structured System Reasoning Graph

Status: Phase 3 architecture planning document
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no runtime graph model, graph database, schema change, API, service, calculation engine, AI agent, provider integration, product catalog, telemetry implementation, utility API, DERMS, dispatch, operational control, or authority-of-record replacement is approved or implied

## Purpose

The Structured System Reasoning Graph is a future derived/advisory reasoning layer over the Residential Energy Twin.

The graph should help Phase 3 Twin Intelligence understand how Residential Energy Twin facts, topology, lifecycle states, products, permissions, provenance, grounding layers, constraints, and missing data relate to one another before producing scenario intelligence, simulations, what-if analysis, recommendations, or exports.

The graph is:

- derived from approved Residential Energy Twin facts and approved grounding layers
- advisory unless later promoted through Matt-approved deterministic, provider-backed, source-backed, permissioned, and provenance-preserving workflows
- topology-aware
- lifecycle-aware
- permission-aware
- provenance-preserving
- confidence-bearing
- missing-data-aware
- view-contract bounded

The graph is not:

- a new source of canonical truth
- a runtime control graph
- an authority of record
- proof of installed, verified, compliant, utility-approved, or operational state
- a replacement for contractor review
- a replacement for engineer review where required
- DERMS, dispatch, telemetry, VPP, demand response, or operational control
- an AI-generated substitute for structured facts, product evidence, provider outputs, or professional review

## Inputs

The Structured System Reasoning Graph must consume Phase 2 and Phase 3 architecture documents as constraints.

Required architecture inputs:

- `ResidentialEnergyTwinContractV1.md`
- `TopologyLifecycleDomains.md`
- `PermissionPlacement.md`
- `ProvenancePlacement.md`
- `ViewContracts.md`
- `SolarMarketProductIntelligenceGrounding.md`
- `Phase3TwinIntelligenceLayer.md`

Required input categories:

- canonical twin facts
- topology relationships
- lifecycle state labels
- current deployed, sandbox, contractual, and future scenario boundaries
- product topology and product capability evidence when available
- permission boundaries
- actor-specific view constraints
- provenance and confidence metadata
- source documents, provider outputs, calculator outputs, and product evidence where approved
- missing-data, unknown, placeholder, estimated, modeled, quoted, verified, manufacturer-backed, contractor-reviewed, and engineer-reviewed labels

The graph must consume the Residential Energy Twin contract. It must not redefine the canonical aggregate, bypass lifecycle state, infer permissions, erase provenance, or promote advisory relationships into source-of-truth facts.

## Graph Nodes

Future graph nodes may represent planning objects, state markers, evidence, constraints, and derived advisory outputs. Nodes should carry stable identity only when that identity comes from an approved source or future approved implementation.

Future node categories include:

- premise
- structure/building
- service
- meter
- main panel
- subpanel
- circuit
- load
- critical load
- PV module
- inverter
- battery
- gateway / transfer equipment
- generator
- EVSE / flexible load
- utility relationship
- product capability
- scenario
- lifecycle state
- permission boundary
- provenance record
- missing-data marker
- constraint
- advisory recommendation

Node expectations:

- every node should identify whether it represents canonical, derived, advisory, historical, or future operational-adjacent context
- every node should preserve lifecycle state where applicable
- every node should carry provenance or an explicit missing-provenance marker
- every node should preserve confidence and verification posture
- product capability nodes should remain tied to verified or source-linked product evidence when available
- permission boundary nodes should not imply enforcement until a future implementation exists
- advisory recommendation nodes should remain downstream of structured facts and source evidence

Nodes must not imply installed state, field verification, engineering approval, utility approval, financial authority, telemetry authority, or operational control unless a future approved source-backed workflow explicitly supports that claim.

## Graph Edges

Future graph edges may describe relationships among nodes. Edges should be typed, directional where relevant, source-linked where possible, and bounded by lifecycle state.

Future edge types include:

- feeds
- depends on
- constrains
- supports
- backs up
- exports to
- imports from
- controlled by
- visible to
- sourced from
- verified by
- conflicts with
- replaces
- proposed for
- approved for
- installed as
- affects
- requires review

Edge expectations:

- `feeds` should describe planning topology, not measured power flow unless telemetry and authority exist later
- `depends on` should identify upstream assumptions, source facts, products, or constraints
- `constrains` should identify service, panel, circuit, product, lifecycle, permission, or missing-data limits
- `supports` and `backs up` should remain planning relationships unless verified by source-backed evidence
- `exports to` and `imports from` should remain planning or utility-relationship context unless approved utility evidence exists
- `controlled by` is reserved for future operational-control-adjacent modeling and must not create command authority
- `visible to` should be derived from approved permission and view-contract rules, not account role alone
- `sourced from` and `verified by` should preserve source evidence and verification scope
- `approved for` and `installed as` should require future source-backed lifecycle transitions before they carry authority
- `requires review` should make contractor, engineer, utility, AHJ, financial, or legal review dependencies explicit

Edges must not silently convert proposed, sandbox, or advisory relationships into current deployed, contractual, verified, utility-approved, or operational relationships.

## Reasoning Uses

The graph should support Phase 3 derived intelligence by making relationships and dependencies inspectable.

Future reasoning uses include:

- scenario intelligence
- what-if analysis
- infrastructure simulation
- dependency reasoning
- impact propagation
- critical-load survivability
- battery recharge likelihood
- solar recharge modeling
- product compatibility reasoning
- topology-aware recommendations
- DER / ADR readiness
- advisor traceability
- deterministic reasoning exports

Reasoning expectations:

- scenario intelligence should compare graph branches without making scenarios authoritative
- what-if analysis should show affected nodes, edges, assumptions, missing data, and review needs
- infrastructure simulation should remain planning simulation, not operational dispatch
- impact propagation should identify stale calculations, stale recommendations, changed confidence, and changed view/export effects
- survivability, recharge, resilience, DER readiness, and ADR readiness outputs should remain advisory unless backed by approved deterministic sources
- product compatibility reasoning should use source-linked product capabilities and topology assignments, not AI-invented equipment capabilities
- advisor outputs should be traceable to graph nodes, edges, assumptions, provenance, confidence, and missing data
- deterministic reasoning exports should preserve the graph basis without bypassing permissions

The graph may organize intelligence. It does not approve calculations, simulation engines, provider integrations, product catalogs, runtime graph stores, or automated engineering design.

## Provenance And Confidence

Every graph-derived conclusion should preserve:

- source facts
- source documents or source records when available
- assumptions
- provider, calculator, or product evidence where applicable
- rule or reasoning basis where applicable
- confidence
- missing-data flags
- lifecycle state
- verification status
- authority layer
- trust zone
- data classification where applicable
- view or export limitation text where applicable

Graph-derived conclusions should distinguish:

- canonical fact
- recorded planning fact
- derived planning intelligence
- advisory explanation
- estimated value
- modeled value
- quoted value
- verified value
- manufacturer-backed product capability
- contractor-reviewed record
- engineer-reviewed record
- unknown or missing value

If provenance is missing, stale, partial, conflicting, or outside the requested view, the graph-derived conclusion should remain provisional, lower confidence where appropriate, or block unsupported conclusions.

## Permission And View Boundaries

The reasoning graph must not bypass permissions.

Actor-specific graph views should be filtered by:

- homeowner authority
- consent
- purpose
- audience
- duration
- revocation
- view contract
- provenance visibility
- data minimization requirements
- lifecycle state
- sensitivity of the underlying fact or relationship

Graph view expectations:

- homeowner views may show broad planning context subject to future product and privacy decisions
- contractor views should include only scoped planning facts, assumptions, missing inputs, and review-relevant topology
- engineer views should preserve evidence, assumptions, and review dependencies without implying stamped approval
- utility views should remain deferred, minimized, permissioned, source-linked, and non-operational until approved
- aggregator views should remain deferred and must not imply enrollment, dispatch, DERMS, VPP, or operational control
- supplier/manufacturer views should be minimized to product-relevant context and must not expose unnecessary homeowner data
- AI advisor views should be grounded, source-linked, and non-authoritative
- audit views should preserve permission, provenance, confidence, lifecycle, and limitation context

No graph view should expose hidden homeowner data, infer consent, bypass revocation, flatten audience boundaries, or treat broad internal graph access as a permissioned export.

## Missing Data

Missing-data markers are first-class graph elements.

Missing-data markers may represent:

- unknown service capacity
- unknown panel constraints
- unknown circuit mapping
- unknown load measurement
- unknown critical-load priority
- unknown product capability
- unknown utility/interconnection context
- missing source document
- missing field verification
- missing contractor review
- missing engineer review
- missing permission basis
- stale or conflicting source evidence

Missing data should:

- block unsupported conclusions
- lower confidence where appropriate
- surface required next inputs
- distinguish unknown from estimated
- distinguish user-entered from verified
- distinguish placeholder from source-backed
- distinguish recorded planning facts from field-verified facts
- identify affected calculations, recommendations, scenarios, views, and exports

The graph should not hide missing data behind advisory language. AI explanations should surface missing-data markers rather than inventing values or implying completeness.

## Lifecycle Boundaries

The graph should preserve topology lifecycle boundaries from `TopologyLifecycleDomains.md`.

Graph reasoning should distinguish:

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

Lifecycle state should affect interpretation. For example, a battery proposed in a sandbox scenario may support a what-if analysis, but it is not installed, contracted, field-verified, utility-approved, dispatchable, or operationally controllable.

Future promotion between lifecycle states requires explicit Matt-approved source-backed workflows. The graph must not infer promotion from AI text, recommendation ranking, design status, UI visibility, account role, or broad API access.

## Utility, DER, ADR, And Operational-Control Separation

The graph may support future DER / ADR readiness reasoning by organizing topology, product capability, utility relationship, permission, provenance, and missing-data context.

Readiness reasoning must not imply:

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

Future operational-control modeling, if ever approved, must remain a separate trust domain with separate contracts, permissions, telemetry governance, cybersecurity posture, auditability, and authority rules.

## Non-Goals

This document does not approve:

- runtime graph implementation
- graph database adoption
- schemas
- migrations
- APIs
- services
- calculation engines
- AI agents
- provider integrations
- spec-sheet ingestion
- product catalog implementation
- telemetry implementation or governance
- utility APIs
- automated engineering design
- final electrical approval
- NEC, AHJ, permitting, or stamped-engineering authority
- financial, tax, incentive, savings, payback, or financing authority
- contractor or engineer authority replacement
- utility dispatch
- DERMS
- demand response
- VPP or aggregator participation
- operational control
- critical-infrastructure, NERC/CIP, utility, government, or national-defense compliance claims

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating runtime reasoning graph models, tables, graph stores, APIs, services, or exports
- defining graph node or edge schemas
- defining confidence, provenance, compatibility, readiness, resilience, economic, or impact-propagation rules as runtime behavior
- creating graph-backed scenario intelligence, simulations, what-if analysis, or deterministic exports
- integrating provider calculators, product catalogs, manufacturer data, utility APIs, telemetry, or operational systems
- creating permission-filtered graph views, contractor packets, engineer packets, utility packets, aggregator packets, or audit APIs
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
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/topology-intelligence/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

The Structured System Reasoning Graph defines a future derived/advisory graph layer for Phase 3 Twin Intelligence. It organizes Residential Energy Twin facts, topology, lifecycle states, products, permissions, provenance, grounding evidence, constraints, and missing data so scenario intelligence, what-if analysis, simulations, dependency reasoning, impact propagation, topology-aware recommendations, advisor traceability, and deterministic exports can remain inspectable. It does not approve runtime graph implementation, schemas, APIs, services, calculations, AI agents, provider integrations, product catalogs, telemetry, utility APIs, DERMS, dispatch, operational control, or authority-of-record replacement.
