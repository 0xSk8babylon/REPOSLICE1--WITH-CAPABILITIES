# Residential Energy Twin Interoperability Domain

Status: Residential Energy Twin architecture planning document
Date: 2026-06-02
Scope: documentation and architecture governance only
Implementation status: no schema, migration, runtime behavior, API, exchange mechanism, export mechanism, protocol, standard, auth, RBAC, ABAC, permission enforcement, utility API, DERMS, dispatch, operational-control behavior, ownership-transfer workflow, or canonical runtime Interoperability Domain implementation is approved or implied

## Purpose

The Interoperability Domain defines how external participants can understand, consume, interpret, and interact with Residential Energy Twin information without modifying the Twin's core truth, authority boundaries, permissions, provenance rules, safety boundaries, or continuity principles.

Its purpose is semantic consistency. It helps different industries interpret the same Residential Energy Twin as a shared, source-linked residential infrastructure record while preserving the distinction between the Twin's recorded facts and each consumer's purpose-specific interpretation.

The Interoperability Domain answers:

How can different industries understand the same Twin?

It does not answer:

How is the Twin exchanged?

This document defines interoperability doctrine and architecture boundaries only. It does not define exchange mechanisms, ownership transfer, APIs, schemas, protocols, standards, exports, integrations, runtime enforcement, utility submissions, operational control, or implementation scope.

## Core Principle

One Twin. Many interpreters.

The Residential Energy Twin remains the canonical source-linked record. External participants may interpret Twin information through their own professional, operational, commercial, or support context, but those interpretations do not change the Twin's canonical truth, lifecycle state, provenance, permission scope, safety posture, or authority boundaries.

Interoperability should make Twin information understandable across industries without collapsing industry context into a single authority model.

## Interoperability Objectives

The Interoperability Domain helps answer:

- What does this Twin fact mean across audiences?
- Which Residential Energy Twin domain owns the meaning of the fact?
- Is the information canonical, derived, advisory, historical, or future operational?
- Is the information current, historical, sandbox, proposed, contractual, verified within a scope, or deferred?
- What provenance supports the information?
- What permission or view boundary governs visibility?
- What safety or continuity context must remain attached?
- Which interpretation is consumer-specific rather than Twin truth?
- What should not be inferred by a contractor, engineer, utility, supplier, manufacturer, aggregator, AI system, real-estate participant, or future application?

These answers are interpretation context. They are not exchange authorization, API behavior, schema design, protocol ownership, legal ownership transfer, utility authority, regulatory authority, compliance approval, safety certification, field verification, contractual rights, financial guarantees, procurement authority, warranty authority, telemetry authority, or operational control.

## Interoperability Categories

### Domain Semantics

Domain semantics define what each Twin domain means and which domain owns each category of meaning.

They help consumers distinguish:

- premise context from legal title or utility account authority
- electrical planning records from NEC compliance or stamped engineering
- equipment references from installed device status, warranty authority, or procurement approval
- safety context from safety approval, field verification, inspection approval, or operational readiness
- continuity history from current state, legal transfer, or proof of ownership
- utility relationship context from utility approval, tariff authority, program eligibility, or export permission

Boundary:

Domain semantics do not create new canonical domains, schemas, runtime models, or exchange structures. They preserve the existing Residential Energy Twin Contract and domain documents.

### Authority Semantics

Authority semantics define how consumers should interpret the authority layer of Twin information.

Expected authority layers include:

- canonical recorded planning fact
- derived planning intelligence
- advisory explanation
- historical record
- future operational state

Boundary:

Authority semantics do not promote recorded planning facts into verified, compliant, approved, installed, utility-authorized, safety-certified, or operational truth. A consumer's use of the information does not increase the Twin's authority.

### Lifecycle Semantics

Lifecycle semantics define how consumers should interpret current, historical, sandbox, proposed, contractual, verified-within-scope, utility-reviewed, and future operational lifecycle states.

They preserve the distinction between:

- what existed previously
- what exists now as recorded planning state
- what is proposed
- what is historical
- what has been superseded, replaced, revoked, or carried forward
- what requires future approved verification or operational contracts

Boundary:

Lifecycle semantics do not create promotion workflows, lifecycle event logs, runtime state machines, exchange processes, field verification, ownership transfer, contractual authority, or operational-control transitions.

### Provenance Semantics

Provenance semantics define how consumers should understand source lineage, evidence, confidence, verification posture, missing data, assumptions, conflicts, supersession, and limitation text.

They help consumers understand why a Twin fact carries a particular trust posture and where the source basis is partial, stale, inferred, placeholder, demo, conflicting, or unknown.

Boundary:

Provenance semantics do not prove correctness, grant access, resolve source conflicts by themselves, replace professional review, or create stronger authority than the source supports.

### Permission Semantics

Permission semantics define how consumers should understand homeowner authorization, audience, purpose, duration, revocation, exclusions, and view scope.

They help prevent consumers from treating account roles, endpoint access, UI visibility, contractor relationships, utility relationships, AI sessions, or business relationships as permission.

Boundary:

Permission semantics do not implement permission enforcement, RBAC, ABAC, tenant isolation, consent capture, revocation workflows, exports, or authorization behavior.

### Safety Semantics

Safety semantics define how consumers should interpret safety-relevant Twin information such as energy sources, isolation systems, export capabilities, operational modes, verification status, and safety provenance.

They help preserve safety context while preventing safety-related overclaims.

Boundary:

Safety semantics do not establish safety approval, code compliance, AHJ approval, inspection approval, utility approval, interconnection approval, emergency-response authority, field verification, operational readiness, dispatch authority, or device-control authority.

### Continuity Semantics

Continuity semantics define how consumers should interpret Twin history across owners, contractors, utilities, equipment changes, software changes, safety context, permissions, provenance, and lifecycle transitions.

They help preserve historical context without confusing historical state with present state.

Boundary:

Continuity semantics do not establish legal ownership, title ownership, identity proof, transfer rights, utility authority, regulatory authority, compliance approval, contractual rights, safety certification, or proof of current state by themselves.

### View Semantics

View semantics define how consumers should understand audience-specific projections of the same Twin.

They help consumers distinguish a minimized contractor view, engineer view, utility view, safety-scoped view, continuity/history view, AI grounding view, audit view, or future industry-specific view from the underlying Twin.

Boundary:

View semantics do not define APIs, schemas, exports, protocol messages, runtime filters, access enforcement, or exchange mechanisms. A view is a projection, not a separate source of truth.

### Industry Interpretation Semantics

Industry interpretation semantics define how a consumer's domain context may shape interpretation without changing Twin truth.

Examples:

- a contractor may interpret pathway and equipment facts as scoping context
- an engineer may interpret electrical and load records as review inputs
- a utility may interpret service, equipment, export, or interconnection context only within source-backed and permissioned limits
- a supplier or manufacturer may interpret product facts as support or compatibility context
- an aggregator may interpret capability context only as future program-readiness context, not enrollment or dispatch authority
- an AI system may interpret Twin facts as grounding context, not as permission to invent facts
- a real-estate participant may interpret continuity context as infrastructure awareness, not title or transfer authority

Boundary:

Industry interpretation does not create authority, permission, eligibility, compliance, approval, transfer, warranty, procurement, financial, telemetry, utility, operational, or control rights.

## Preservation Of Twin Truth

Interoperability must preserve:

- canonical Twin facts and domain ownership
- current, historical, sandbox, proposed, contractual, verified-within-scope, and future operational lifecycle distinctions
- provenance, confidence, missing data, assumptions, conflicts, and limitation text
- homeowner permission scope and view boundaries
- safety context and safety limitations
- continuity context and historical/current separation
- trust zones and authority layers
- data classification and minimization expectations when views are defined

Interoperability must not allow a consumer, integration, view, export, protocol, standard, AI system, industry workflow, or downstream application to overwrite Twin truth or silently increase authority.

If an external participant contributes new information, that contribution would require a future approved source-backed update workflow with provenance, permission, lifecycle state, conflict handling, and authority boundaries. This document does not approve that workflow.

## Relationship To Existing Domains

| Related domain or document | Interoperability relationship | Boundary |
| --- | --- | --- |
| Residential Energy Twin Contract | Defines the aggregate identity, source-of-truth order, domain ownership, and authority boundaries that interoperability must preserve. | Interoperability does not create a runtime Twin model, schema, endpoint, export, protocol, or exchange format. |
| Provenance Domain | Supplies source lineage, evidence, confidence, verification posture, conflicts, and limitations that consumers need to interpret Twin facts. | Provenance semantics do not prove correctness or grant access. |
| Permission Domain | Supplies homeowner authorization, audience, purpose, duration, revocation, exclusions, and view-scope expectations. | Permission semantics do not implement enforcement or authorize exchange. |
| View Contracts | Define how consumer-specific projections should preserve provenance, permissions, limits, authority, lifecycle state, and data minimization. | View semantics are not APIs, schemas, runtime filters, or exchange mechanisms. |
| Trust Zones | Define recorded, derived, advisory, historical, and future operational authority posture. | Trust semantics do not increase authority or create compliance, safety, utility, financial, or operational claims. |
| Safety Domain | Supplies safety-relevant context and limits that every consumer must preserve when interpreting safety information. | Safety semantics do not create safety approval, field verification, inspection approval, utility approval, or operational readiness. |
| Continuity Domain | Supplies lifecycle history and current-versus-historical distinctions that consumers must preserve. | Continuity semantics do not establish ownership, title, transfer, utility authority, contractual rights, or proof of current state. |
| Topology Lifecycle Domains | Supplies topology and lifecycle-state interpretation for recorded, sandbox, proposed, scenario, future reviewed, future verified, utility-facing, and operational topology. | Interoperability does not create topology promotion workflows, event logs, or runtime topology exchange. |

## Interoperability Boundaries

The Interoperability Domain defines shared understanding only.

It does not define or approve:

- exchange mechanisms
- ownership transfer
- APIs
- schemas
- protocols
- standards
- exports
- integrations
- runtime models
- data synchronization
- import workflows
- source-backed promotion workflows
- field verification workflows
- utility submissions
- utility authority
- regulatory authority
- compliance approval
- safety certification
- legal ownership
- title ownership
- contractual rights
- financial guarantees
- procurement authority
- warranty authority
- telemetry authority
- DERMS
- dispatch
- demand response
- VPP participation
- aggregator enrollment
- operational control

Interoperability improves shared interpretation. It does not move, mutate, transfer, approve, certify, operate, or control the Twin.

## Strategic Role

Interoperability strengthens:

- common understanding across industries
- semantic consistency
- consumer independence
- cross-industry consumption
- preservation of Twin truth
- provenance survival
- permission and view discipline
- safety-boundary preservation
- continuity across lifecycle changes
- future registry and network readiness

The Interoperability Domain supports the Trusted Residential Energy Record and the long-term Residential Infrastructure Registry / Residential Infrastructure Network vision by making Twin records understandable to multiple industries without requiring the repository to optimize for protocol ownership.

Interoperability is a Residential Energy Twin domain. It is not a separate product, protocol program, standards body, exchange platform, integration layer, utility system, legal-transfer system, compliance system, safety-certification system, or operational-control platform.

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating runtime interoperability models, fields, tables, migrations, services, APIs, exports, integrations, or UI workflows
- defining exchange mechanisms, import mechanisms, synchronization mechanisms, ownership-transfer workflows, source-backed promotion workflows, or external contribution workflows
- defining schemas, protocols, standards, versioned exchange formats, conformance rules, certification programs, registries, networks, or external data packages
- creating industry-specific runtime views, packets, exports, or integration contracts
- changing canonical Twin domain ownership, lifecycle states, source-of-truth order, permission boundaries, provenance requirements, safety boundaries, continuity boundaries, trust zones, or view contracts
- implementing permission enforcement, RBAC, ABAC, tenant isolation, auth, encryption, telemetry governance, audit policy, utility APIs, utility submissions, DERMS, dispatch, demand response, VPP, aggregator participation, or operational-control behavior
- treating external interpretation as proof of compliance, safety, utility approval, interconnection approval, eligibility, legal ownership, title transfer, contractual rights, financial guarantee, warranty authority, procurement approval, field verification, operational readiness, or device-control authority

## Sources / Provenance

- User-provided Residential Energy Twin Interoperability Domain milestone, 2026-06-02
- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/product-vision.md`
- `docs/philosophy/CORE_PHILOSOPHY.md`
- `docs/philosophy/TRUST_AND_PROVENANCE_PHILOSOPHY.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/TopologyLifecycleDomains.md`
- `docs/architecture/ContinuityDomain.md`
- `docs/architecture/SafetyDomain.md`
- `docs/architecture/PermissionPlacement.md`
- `docs/architecture/ProvenancePlacement.md`
- `docs/architecture/ViewContracts.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/project-skills/doctrine-formalization/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `.codex/project-skills/continuity-governance/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

The Interoperability Domain defines docs-only Residential Energy Twin doctrine for shared cross-industry understanding of Twin information. It preserves semantic consistency, consumer independence, domain interpretation, provenance, permissions, safety boundaries, continuity principles, trust zones, and core Twin truth while explicitly deferring exchange mechanisms, ownership transfer, APIs, schemas, protocols, standards, runtime implementation, utility authority, compliance authority, safety certification, and operational control.
