# Residential Energy Twin Continuity Domain

Status: Residential Energy Twin architecture planning document
Date: 2026-06-02
Scope: documentation and architecture governance only
Implementation status: no schema, migration, runtime behavior, API, auth, RBAC, ABAC, permission enforcement, ownership-transfer workflow, legal-title workflow, utility authority, compliance approval, safety certification, contractual-rights workflow, operational-control behavior, or canonical runtime Continuity Domain implementation is approved or implied

## Purpose

The Continuity Domain defines how the Residential Energy Twin persists across the lifecycle of the home.

Its purpose is to preserve lifecycle history and maintain a durable, source-linked record of residential infrastructure across time. The Continuity Domain ensures the Twin remains attached to the home rather than any individual project, contractor, homeowner, utility, manufacturer, equipment vendor, or software platform.

The Continuity Domain is a foundational Residential Energy Twin domain. It is not a separate product, registry runtime, legal record system, utility account system, contract system, compliance system, safety-certification system, or operational-control platform.

## Core Principle

The Twin persists with the home.

Projects, contractors, utilities, equipment, owners, manufacturers, software platforms, and planning applications may change. The Twin remains.

Continuity information should preserve what changed, when it changed, who or what supplied the change, what evidence supports it, what assumptions were involved, and whether the information describes historical state, current recorded state, sandbox planning state, proposed state, or a future approved lifecycle state.

## Continuity Objectives

The Continuity Domain helps answer:

- What existed previously?
- What exists now?
- What changed?
- When did it change?
- Who changed it or supplied the update?
- What evidence supports the change?
- What assumptions are historical versus current?
- Which records are superseded, stale, revoked, replaced, transferred, or still active?

These answers are continuity context. They are not legal ownership, title ownership, utility authority, regulatory authority, compliance approval, operational control, contractual rights, safety certification, or proof of installation.

## Continuity Categories

### Ownership Continuity

Ownership continuity preserves the historical relationship between a home, homeowner accounts, owner-authorized participants, and future ownership-transfer events when approved.

It may record:

- prior owner/account association context
- current owner/account association context
- transfer-related timestamps and source evidence
- permission and revocation implications when approved
- historical access or view lineage when approved

Boundary:

Ownership continuity does not establish legal title, property ownership, deed status, identity proof, homeowner authorization by itself, or the right to access, sell, transfer, export, or control the Twin.

### Contractor Continuity

Contractor continuity preserves historical context about contractor, installer, designer, engineer, or reviewer involvement.

It may record:

- who supplied project or field information
- contractor-reviewed, engineer-reviewed, or installer-reported context when approved
- scope of involvement
- source documents, notes, dates, and affected Twin facts
- superseded or replaced contractor assumptions

Boundary:

Contractor continuity does not establish contractor authority, contractual rights, bid authority, warranty authority, engineering approval, permit approval, safety approval, or ongoing access rights.

### Infrastructure Continuity

Infrastructure continuity preserves the history of behind-the-meter infrastructure over time.

It may record:

- equipment additions, removals, replacements, or upgrades
- panel, service, load, pathway, topology, and equipment-state changes
- current versus historical infrastructure states
- decommissioning, replacement, expansion, or supersession context
- evidence and confidence behind infrastructure changes

Boundary:

Infrastructure continuity does not prove installation, commissioning, code compliance, field verification, utility approval, operational readiness, or device-control authority.

### Utility Continuity

Utility continuity preserves source-linked history about utility provider context, service context, interconnection context, program context, and utility-reviewed or utility-limited records when approved.

It may record:

- utility provider changes
- service-context changes
- interconnection or export-context changes when sourced and permissioned
- program-context history
- utility-source evidence and effective dates when available

Boundary:

Utility continuity does not establish utility account authority, tariff authority, incentive eligibility, interconnection approval, export permission, utility submission authority, program enrollment, DERMS, dispatch, demand response, VPP participation, or operational control.

### Safety Continuity

Safety continuity preserves historical and current safety-relevant context from the Safety Domain.

It may record:

- historical and current energy sources
- isolation systems
- export capabilities
- operational modes
- safety-relevant equipment changes
- verification status changes and verification scope
- safety evidence, assumptions, unknowns, and limitation text

Boundary:

Safety continuity does not establish safety certification, code compliance, AHJ approval, inspection approval, utility approval, field verification, emergency-response authority, or operational readiness.

### Permission Continuity

Permission continuity preserves the history of permission grants, view scopes, consent artifacts, revocation state, expiration, supersession, and access lineage when approved.

It may record:

- grant creation, update, expiration, revocation, or supersession
- view purpose, audience, duration, scope, and exclusions
- historical access or export records when approved
- permission provenance and consent-artifact references

Boundary:

Permission continuity does not create permission by itself. Account role, subscription status, endpoint access, UI visibility, contractor relationship, utility relationship, or AI session access is not a permission grant.

### Provenance Continuity

Provenance continuity preserves source lineage over time.

It may record:

- source document history
- data provenance history
- rule provenance history
- source conflicts, supersession, staleness, and replacement
- confidence and verification-status changes
- historical assumptions and missing-data posture
- revision identity or snapshot identity where available

Boundary:

Provenance continuity does not prove correctness, grant access, establish authority, or resolve conflicts by itself. If sources conflict, the conflict should remain visible rather than silently erased.

## Lifecycle Principle

The Twin should survive:

- homeowner changes
- contractor changes
- utility changes
- equipment replacement
- system upgrades
- software changes
- project changes
- scenario branching
- permission revocation or expiration
- source supersession

without losing historical context.

Continuity should preserve the record of change while keeping current, historical, sandbox, proposed, contractual, verified, utility-reviewed, and future operational states distinct.

No continuity transition should be inferred from:

- AI-generated text
- account role, plan, subscription, or UI visibility
- endpoint access
- design status labels
- contractor relationship labels
- utility provider text fields
- recommendation profile selection
- scenario ranking
- product compatibility notes

## Historical Record Principle

Historical information must remain distinguishable from current information.

The Twin should preserve history without confusing historical state with present state. Historical facts, superseded assumptions, old source documents, prior contractor inputs, prior owner/account relationships, previous utility context, obsolete equipment, revoked permissions, stale product data, and prior safety context should remain labeled with lifecycle state, source, timestamp, confidence, missing inputs, and limitation metadata.

Historical records may support learning, comparison, auditability, real-estate continuity, contractor continuity, and future review. They do not automatically describe the current home.

Current recorded state should identify whether it is:

- newly recorded
- carried forward from historical state
- superseded
- stale
- replaced
- revoked
- unknown
- inferred
- placeholder/demo
- source-backed
- verified within a defined scope

## Continuity Boundaries

The Continuity Domain records continuity information only.

It does not establish:

- legal ownership
- title ownership
- utility authority
- regulatory authority
- compliance approval
- operational control
- contractual rights
- safety certification
- contractor authority
- engineer approval
- AHJ approval
- interconnection approval
- tariff authority
- export permission
- program eligibility
- financial guarantees
- procurement authority
- warranty authority
- identity proof

Continuity improves traceability and context. It does not increase authority unless a future approved source-backed lifecycle transition explicitly records that authority with provenance, permissions, scope, and limitations.

## Strategic Role

Continuity strengthens:

- trust
- provenance
- safety
- lifecycle understanding
- real-estate transfer context
- utility coordination context
- infrastructure awareness
- contractor continuity
- homeowner understanding
- future registry and network readiness

The Continuity Domain supports the Trusted Residential Energy Record and the long-term Residential Infrastructure Registry / Residential Infrastructure Network vision by preserving lifecycle history across changes in people, projects, equipment, utilities, and software.

Continuity is a foundational Twin domain rather than a separate product.

## Relationship To Existing Domains

| Related domain or document | Continuity relationship | Boundary |
| --- | --- | --- |
| Residential Energy Twin Contract | Defines the aggregate identity, lifecycle states, source-of-truth boundaries, and domain ownership that continuity must preserve. | Continuity does not create a runtime Twin model, table, endpoint, or canonical identity implementation. |
| Provenance Domain | Supplies source lineage, evidence, confidence, verification posture, conflict, and supersession context for continuity records. | Provenance continuity does not prove correctness or grant access. |
| Permission Domain | Supplies grant, scope, consent, duration, revocation, expiration, and view-access history when approved. | Permission continuity does not create or imply permission. |
| Safety Domain | Supplies historical and current safety-relevant context for energy sources, isolation systems, export capabilities, operational modes, verification status, and safety provenance. | Safety continuity does not create safety certification, inspection approval, field verification, utility approval, or operational readiness. |
| View Contracts | Define how continuity and historical records may be projected to homeowner, contractor, engineer, utility, AI, audit, safety-scoped, and future continuity/history views. | Views are projections, not canonical facts or enforcement. Existing broad `/api/*` contracts are not continuity views. |
| Topology Lifecycle Domains | Define lifecycle separation for recorded current, sandbox, proposed, saved revision, future reviewed, verified, utility-facing, and operational topology states. | Continuity does not collapse lifecycle states or promote planning state into verified or operational truth. |

## Future Continuity Views

Future continuity or history views may expose minimum necessary lifecycle history for a specific purpose and audience.

They may include after future approval:

- current-versus-historical state markers
- changed fields and affected Twin objects
- actor or source system
- source documents and provenance summaries
- timestamp and lifecycle context
- confidence and verification posture
- assumptions, missing inputs, and limitations
- supersession, revocation, replacement, or stale-state labels
- permission scope when enforcement exists

They must exclude or label:

- legal title or ownership claims
- utility authority claims
- compliance, safety, permit, AHJ, or engineering approval claims
- operational-control claims
- unrelated homeowner/private context
- broad raw records when summaries are sufficient
- historical data presented as current state

No current runtime continuity view, endpoint, export, packet, filter, permission enforcement, RBAC/ABAC behavior, or audit workflow is approved by this document.

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating runtime Continuity Domain models, fields, tables, migrations, APIs, services, exports, UI workflows, or lifecycle event logs
- defining ownership-transfer workflows, contractor-transition workflows, utility-transition workflows, equipment-replacement workflows, or software-platform transition workflows as runtime behavior
- defining continuity completeness rules, stale-state rules, supersession rules, retention rules, legal-transfer semantics, or historical-state authority semantics as implementation policy
- creating continuity/history views, continuity exports, transfer packets, real-estate packets, contractor handoff packets, utility continuity packets, audit APIs, or scoped API contracts
- implementing permission enforcement, RBAC, ABAC, tenant isolation, encryption, telemetry governance, audit policy, or access monitoring for continuity records
- treating continuity records as proof of legal ownership, title ownership, utility authority, regulatory authority, compliance approval, operational control, contractual rights, safety certification, field verification, interconnection approval, export permission, or professional review
- implementing DERMS, dispatch, demand response, VPP, aggregator participation, telemetry-as-truth, command authorization, or operational-control behavior
- changing trust language that could imply ownership, compliance, safety approval, utility approval, interconnection approval, operational readiness, contractual rights, or professional review

## Sources / Provenance

- User-provided Residential Energy Twin Continuity Domain doctrine, 2026-06-02
- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/SafetyDomain.md`
- `docs/architecture/TopologyLifecycleDomains.md`
- `docs/architecture/PermissionPlacement.md`
- `docs/architecture/ProvenancePlacement.md`
- `docs/architecture/ViewContracts.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/project-skills/doctrine-formalization/SKILL.md`
- `.codex/project-skills/continuity-governance/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

The Continuity Domain defines docs-only Residential Energy Twin doctrine for preserving lifecycle history and maintaining a durable, source-linked record of residential infrastructure across time. It ensures the Twin remains attached to the home while projects, contractors, utilities, equipment, owners, and software platforms change. It records continuity context only and preserves strict boundaries against legal ownership, title ownership, utility authority, regulatory authority, compliance approval, operational control, contractual rights, safety certification, runtime implementation, schemas, APIs, exports, and enforcement behavior.
