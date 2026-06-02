# Residential Energy Twin Canonical Architecture Hierarchy

Status: Residential Energy Twin doctrine consolidation document
Date: 2026-06-02
Scope: documentation and architecture governance only
Implementation status: no new domain, runtime behavior, schema, migration, API, protocol, exchange mechanism, ownership-transfer workflow, registry implementation, identity implementation, permission enforcement, utility API, DERMS, dispatch, operational-control behavior, or canonical runtime model is approved or implied

## Purpose

This document is the single authoritative architecture hierarchy and doctrine map for the current Residential Energy Twin architecture.

It consolidates existing doctrine into layers so future work can route through the right source document without creating new domains, new architecture, or premature implementation concepts.

This document does not create:

- new Residential Energy Twin domains
- Exchange Domain
- Ownership & Transfer doctrine
- Registry doctrine
- Identity doctrine
- API contracts
- schemas or migrations
- protocols or standards
- runtime behavior
- permission enforcement
- utility participation
- DERMS, dispatch, telemetry, demand response, VPP, or operational control

## Architecture Hierarchy

| Layer | Purpose | Primary authority | Depends on | Non-goals | Approval boundaries |
| --- | --- | --- | --- | --- | --- |
| 1. Strategic Doctrine Layer | Defines why the Twin exists, how the Planner relates to it, and the long-term strategic posture. | `AGENTS.md`, `PROJECT_STATE.md`, `docs/product-vision.md`, `docs/philosophy/CORE_PHILOSOPHY.md` | Matt-approved positioning and operating principles. | Does not define runtime architecture, schemas, APIs, business model changes, registry implementation, or network implementation. | Matt must approve changes to product direction, business model, market positioning, trust language, or strategic doctrine. |
| 2. Residential Energy Twin Contract Layer | Defines the canonical aggregate boundary, authority posture, source-of-truth order, lifecycle model, identity reservations, permission/provenance/view placement expectations, and deferred implementation gates. | `docs/architecture/ResidentialEnergyTwinContractV1.md` | Strategic doctrine and existing planner structured records. | Does not create a runtime `ResidentialEnergyTwin` model, `twin_id`, schema, migration, API, repository boundary, permission enforcement, utility authority, or operational control. | Matt must approve aggregate identity, canonical domains, lifecycle states, topology ownership, schema, persistence, API, permission, provenance, or runtime implementation changes. |
| 3. Foundational Domain Layer | Organizes the core planning facts that the Twin can preserve over time. | `ResidentialEnergyTwinContractV1.md`, `docs/architecture/TopologyLifecycleDomains.md` | Contract layer, current recorded planner facts, source-of-truth boundaries. | Does not imply field verification, engineering approval, legal title, utility authority, bid authority, warranty authority, or operational readiness. | Matt must approve canonical domain boundary changes, topology ownership, lifecycle-state changes, required fields, validation rules, schemas, or migrations. |
| 4. Trust-Bearing Domain Layer | Defines where safety, continuity, permissions, provenance, utility relationship context, confidence, and authority limitations attach. | `docs/architecture/SafetyDomain.md`, `docs/architecture/ContinuityDomain.md`, `docs/architecture/PermissionPlacement.md`, `docs/architecture/ProvenancePlacement.md`, `docs/trust/TRUST_ZONES.md` | Contract layer, foundational domains, lifecycle model, source lineage. | Does not create safety approval, ownership transfer, legal authority, provenance enforcement, permission enforcement, auth, RBAC, ABAC, utility approval, field verification, or operational control. | Matt must approve safety workflow, permission/consent logic, provenance policy, trust-zone policy, data-classification policy, utility authority, audit/security policy, or enforcement changes. |
| 5. Interpretation & Projection Layer | Defines how the same Twin can be interpreted and projected through permissioned, provenance-preserving, audience-specific views. | `docs/architecture/InteroperabilityDomain.md`, `docs/architecture/ViewContracts.md` | Contract layer, trust-bearing domains, participant-purpose boundaries, lifecycle and authority labels. | Does not define exchange, APIs, schemas, protocols, exports, integrations, runtime filters, RBAC, utility submissions, or operational-control views. | Matt must approve runtime view contracts, scoped exports, audience visibility, API changes, exchange formats, protocol work, or view enforcement. |
| 6. Participant Boundary Layer | Applies existing doctrine to ecosystem participants by purpose, minimum necessary domains, permissions, provenance, continuity, interoperability, prohibited claims, and prohibited authority assumptions. | `docs/architecture/EcosystemParticipantBoundaryMatrix.md` | Interpretation/projection layer, permission placement, provenance placement, safety and continuity boundaries. | Does not create a new Twin domain, exchange mechanism, participant API, ownership-transfer workflow, registry, utility control, or operational authority. | Matt must approve participant-boundary runtime models, exports, packets, integrations, exchange work, ownership-transfer semantics, utility submissions, or participant authority claims. |
| 7. Phase 3 Intelligence Layer | Defines derived/advisory intelligence built on the Twin: reasoning, scenarios, simulation, what-if analysis, dependency impact, stale-output handling, and traceability. | `docs/architecture/Phase3TwinIntelligenceLayer.md`, `docs/architecture/StructuredSystemReasoningGraph.md`, `docs/architecture/ScenarioIntelligence.md`, `docs/architecture/InfrastructureSimulation.md`, `docs/architecture/WhatIfAnalysis.md`, `docs/architecture/DependencyImpactPropagation.md` | Contract layer, topology/lifecycle model, permissions, provenance, view boundaries, grounding layers, trust zones. | Does not approve runtime engines, graph stores, calculations, AI agents, provider integrations, product catalogs, APIs, schemas, deterministic exports, authority replacement, utility participation, DERMS, dispatch, or operational control. | Matt must approve runtime intelligence behavior, provider/product integrations, calculation rules, confidence/provenance thresholds, deterministic exports, AI write authority, utility APIs, or operational-control semantics. |
| 8. Future Gated Layers | Names work that remains explicitly deferred until prerequisite contracts and Matt approvals exist. | Contract decisions and future Matt-approved doctrine only. | Stable contract layer, permission/view contracts, provenance policy, security/audit posture, lifecycle model, implementation-readiness review. | Does not start Exchange, Ownership & Transfer, Registry, Identity, Privacy Enforcement, RBAC/ABAC, Telemetry Governance, Security Hardening, Utility Participation, or Operational Control. | Matt must explicitly approve any future gated layer before doctrine, implementation design, schemas, APIs, exports, protocols, runtime behavior, or authority semantics are created. |

## Doctrine Topology Map

The current doctrine topology is:

```text
Strategic Doctrine
  -> ResidentialEnergyTwin Contract v1
    -> Foundational Domains
      -> Trust-Bearing Domains
        -> Interpretation & Projection
          -> Participant Boundaries
            -> Phase 3 Derived/Advisory Intelligence
              -> Future Gated Layers only after explicit Matt approval
```

### Layer Relationships

- Strategic doctrine explains why the Twin exists.
- The contract layer defines what the Twin is and what it is not.
- Foundational domains define what planning facts can be organized inside the Twin boundary.
- Trust-bearing domains define how authority, safety, continuity, permission, provenance, confidence, and utility-context limits remain visible.
- Interpretation and projection define how the same Twin can be understood and viewed without changing Twin truth.
- Participant boundaries apply the same doctrine to specific audiences and purposes without creating exchange.
- Phase 3 intelligence consumes the prior layers to produce derived/advisory reasoning without becoming a source of truth.
- Future gated layers remain deferred until Matt approves them separately.

## Cross-Reference Index

### Strategic Doctrine Layer

- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `docs/product-vision.md`
- `docs/philosophy/CORE_PHILOSOPHY.md`

### Residential Energy Twin Contract Layer

- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/RESIDENTIAL_ENERGY_TWIN_CONTRACT_V1.md` as compatibility pointer only
- `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md` as docs-only first-boundary planning note

### Foundational Domain Layer

- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/TopologyLifecycleDomains.md`
- Current planner structured records described in `docs/ARCHITECTURE.md`

Foundational planning areas include:

- premise
- buildings
- electrical infrastructure
- loads
- equipment
- designs
- pathways
- scenarios
- utility relationships as narrow, permissioned, source-linked context
- views as projections, not canonical facts

### Trust-Bearing Domain Layer

- `docs/architecture/SafetyDomain.md`
- `docs/architecture/ContinuityDomain.md`
- `docs/architecture/PermissionPlacement.md`
- `docs/architecture/ProvenancePlacement.md`
- `docs/trust/TRUST_ZONES.md`
- `docs/provenance/LINEAGE_MODEL.md`

### Interpretation & Projection Layer

- `docs/architecture/InteroperabilityDomain.md`
- `docs/architecture/ViewContracts.md`
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md`

### Participant Boundary Layer

- `docs/architecture/EcosystemParticipantBoundaryMatrix.md`

Participant families currently mapped:

- homeowners
- contractors
- utilities
- real estate
- insurance
- finance
- manufacturers
- aggregators

### Phase 3 Intelligence Layer

- `docs/architecture/Phase3TwinIntelligenceLayer.md`
- `docs/architecture/StructuredSystemReasoningGraph.md`
- `docs/architecture/ScenarioIntelligence.md`
- `docs/architecture/InfrastructureSimulation.md`
- `docs/architecture/WhatIfAnalysis.md`
- `docs/architecture/DependencyImpactPropagation.md`
- `docs/architecture/SolarMarketProductIntelligenceGrounding.md`

### Future Gated Layers

The following are named only as deferred gated layers. This document does not start them:

- Exchange
- Ownership & Transfer
- Registry
- Identity
- Privacy Enforcement
- RBAC / ABAC Authorization
- Encryption / Security Hardening
- Telemetry Governance
- Utility Participation
- Operational Control
- DERMS / dispatch / demand response / VPP

## Consolidation Rules

- New doctrine should first be routed into an existing layer unless Matt approves a new layer or domain.
- Participant-specific needs should route through the Participant Boundary Layer before any exchange work.
- View or export questions should route through Permission Placement, Provenance Placement, and View Contracts before runtime design.
- Derived intelligence questions should route through Phase 3 Intelligence and Dependency Impact Propagation before implementation design.
- Identity questions should remain in the Contract Layer until Matt approves runtime identity work.
- Registry concepts should remain strategic long-term positioning until Matt approves Registry doctrine.
- Ownership and transfer concepts should remain bounded by Continuity and participant-purpose limits until Matt approves Ownership & Transfer doctrine.
- Exchange concepts should remain bounded by Interoperability and participant-purpose prerequisites until Matt approves Exchange doctrine.

## Risks

- Doctrine sprawl: future sessions may create new documents where an existing layer already owns the concept.
- Exchange drift: interoperability and participant-boundary language may be mistaken for exchange authorization.
- Ownership-transfer drift: continuity and real-estate context may be mistaken for title, deed, legal transfer, or access authority.
- Registry drift: long-term Residential Infrastructure Registry language may be mistaken for current product or runtime scope.
- Identity drift: `twin_id`, `home_id`, and `owner_account_id` reservations may be mistaken for approved runtime identity implementation.
- Runtime drift: Phase 3 intelligence and Dependency Impact Propagation may be mistaken for approved engines, graph stores, APIs, schemas, or invalidation systems.
- Authority drift: safety, utility, finance, insurance, manufacturer, and aggregator interpretations may be mistaken for approval, eligibility, warranty, underwriting, savings, dispatch, or operational authority.

## Consolidation Impact Assessment

This milestone consolidates existing Residential Energy Twin architecture into one hierarchy and doctrine map.

It does not approve or imply:

- new Residential Energy Twin domains
- new architecture beyond hierarchy consolidation
- Exchange Domain
- Ownership & Transfer doctrine
- Registry doctrine
- Identity doctrine
- runtime identity implementation
- schemas or migrations
- APIs or API versioning
- protocols or standards
- exchange formats
- exports or packets
- permission enforcement
- auth, RBAC, ABAC, tenant isolation, encryption, telemetry governance, or audit enforcement
- utility APIs, utility submissions, interconnection authority, tariff authority, incentive authority, DERMS, dispatch, demand response, VPP, or operational control
- safety approval, field verification, inspection workflows, AHJ workflows, engineering approval, legal authority, financial authority, warranty authority, procurement authority, or authority-of-record replacement

The impact is limited to improving doctrine routing, reducing architecture ambiguity, and making future milestone decisions easier to evaluate against existing layers.

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, doctrine expansion, schema, API contract, enforcement behavior, or settled product direction:

- creating new Twin domains or architecture layers
- starting Exchange, Ownership & Transfer, Registry, or Identity doctrine
- creating runtime identity, canonical aggregate, schema, migration, persistence, or API behavior
- creating exchange mechanisms, exports, packets, protocols, standards, integrations, or external contribution workflows
- creating ownership-transfer workflows, legal-title workflows, registry records, registry APIs, or identity proof workflows
- implementing permission enforcement, RBAC, ABAC, tenant isolation, privacy enforcement, encryption, telemetry governance, audit enforcement, utility APIs, utility submissions, DERMS, dispatch, demand response, VPP, or operational control
- changing trust language that could imply compliance, approval, safety, savings, eligibility, authorization, professional review, utility approval, legal authority, financial authority, warranty authority, field verification, or operational readiness

## Recommended Commit Message

```text
docs: add twin architecture hierarchy
```

## Sources / Provenance

- User-provided Residential Energy Twin Canonical Architecture Hierarchy milestone, 2026-06-02
- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/ARCHITECTURE.md`
- `docs/product-vision.md`
- `docs/philosophy/CORE_PHILOSOPHY.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/TopologyLifecycleDomains.md`
- `docs/architecture/SafetyDomain.md`
- `docs/architecture/ContinuityDomain.md`
- `docs/architecture/InteroperabilityDomain.md`
- `docs/architecture/EcosystemParticipantBoundaryMatrix.md`
- `docs/architecture/DependencyImpactPropagation.md`
- `docs/architecture/ViewContracts.md`
- `docs/architecture/PermissionPlacement.md`
- `docs/architecture/ProvenancePlacement.md`
- `docs/trust/TRUST_ZONES.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/architecture/Phase3TwinIntelligenceLayer.md`
- `docs/architecture/COGNITION_LAYERS.md`
- `docs/architecture/CANONICAL_TERMINOLOGY.md`
- `.codex/project-skills/doctrine-formalization/SKILL.md`
- `.codex/project-skills/canonical-authority-discipline/SKILL.md`
- `.codex/project-skills/continuity-governance/SKILL.md`
- `/home/mattcoje/.codex/skills/architecture-inspection/SKILL.md`

## Summary

The Residential Energy Twin Canonical Architecture Hierarchy consolidates the current doctrine stack into eight layers: Strategic Doctrine, Residential Energy Twin Contract, Foundational Domains, Trust-Bearing Domains, Interpretation & Projection, Participant Boundaries, Phase 3 Intelligence, and Future Gated Layers. It is a routing and consolidation document only. It does not create new domains, new architecture, Exchange, Ownership & Transfer, Registry, Identity, APIs, schemas, protocols, runtime behavior, permission enforcement, utility behavior, safety approval, field verification, DERMS, dispatch, or operational control.
