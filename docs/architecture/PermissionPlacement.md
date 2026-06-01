# Permission Placement

Status: Phase 2 architecture planning document
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no schema, migration, runtime permission enforcement, API, auth, RBAC, ABAC, encryption, telemetry governance, utility API, DERMS, dispatch, operational-control, or canonical runtime permission model is approved or implied

## Purpose

Permission placement defines where homeowner authorization, audience scope, purpose, duration, revocation, and permissioned view expectations attach inside the Residential Energy Twin.

This document extends `ResidentialEnergyTwinContractV1.md` and `TopologyLifecycleDomains.md`. It completes Phase 2 placement architecture for permissions, but it does not implement permission grants, consent artifacts, revocation state, scoped exports, authorization, RBAC, ABAC, tenant isolation, privacy enforcement, utility access, or operational control.

## Core Principle

The homeowner remains the authority for sharing the Residential Energy Twin.

Permission is a first-class twin concept. It is not an account role, subscription status, endpoint filter, UI visibility rule, contractor relationship, utility relationship, AI session, or broad API access.

No external actor should receive a view of twin data unless a future approved permission model can answer:

- who authorized access
- which twin, domain, field, source document, derived output, or view is covered
- which audience receives access
- which purpose applies
- how long access lasts
- what is excluded
- whether access is active, expired, revoked, or superseded
- what provenance, audit, and limitation metadata travels with the view

## Attachment Points

Future permission concepts should attach at multiple levels of the Residential Energy Twin.

| Attachment level | Purpose | Examples | Boundary |
| --- | --- | --- | --- |
| Twin-level | Authorize broad owner-governed access to the home energy record. | Homeowner owner view, trusted household access, future account transfer workflow. | Does not authorize external sharing by itself. |
| Domain-level | Authorize access to a whole twin domain. | Buildings, loads, equipment, pathways, scenarios, utility relationships. | Must preserve domain provenance and exclusions. |
| Field-level | Authorize access to sensitive or authority-bearing fields. | Address, service size, load detail, equipment serial-like identifiers, utility context. | Should be used when a full domain would overexpose homeowner data. |
| Source-document level | Authorize visibility into source evidence. | Photos, equipment documents, utility documents, contractor uploads, homeowner notes. | Source access may be narrower than fact access. |
| Derived-output level | Authorize planning intelligence visibility. | Advisor summary, sizing ranges, scenario comparisons, takeoffs, reasoning graph. | Derived outputs must remain planning-only unless future authority supports stronger claims. |
| View-contract level | Authorize an explicit projection for a purpose and audience. | Contractor scoping view, engineer review-input view, AI grounding view, utility-safe view. | A view is not canonical and is not enforcement until runtime policy exists. |
| Export level | Authorize a specific package or transfer outside the system. | Contractor packet, engineer review packet, future utility packet. | Deferred until export authorization and audit behavior are approved. |
| Operational-control level | Authorize future command/control-adjacent access. | Device commands, dispatch, availability, telemetry authority. | Separate future trust domain; not part of Phase 2 permission behavior. |

## Permission Ownership Boundaries

| Area | Primary owner | Supporting owners | Boundary |
| --- | --- | --- | --- |
| Permission concepts | Permission / Consent Agent | Product Orchestrator, Technical Orchestrator | Recommends scope, grant, consent, duration, revocation, and view placement; does not approve enforcement. |
| View contracts | Technical Orchestrator | Permission / Consent Agent, Security / Audit / Provenance Agent, specialist domain agents | Defines future contract shapes; does not narrow existing `/api/*` responses without approval. |
| Provenance and audit requirements | Security / Audit / Provenance Agent | Permission / Consent Agent | Defines lineage and audit expectations; does not implement policy or security posture. |
| Utility sharing | Utility / Grid Edge Agent | Permission / Consent Agent, Security / Audit / Provenance Agent | Defines utility data needs and minimization; does not grant utility authority or export behavior. |
| Operational control | Future approved operational-control owner | Permission, Security, Utility, Twin | Reserved. No current permission can imply dispatch, DERMS, control, or telemetry authority. |

Matt approval is required before any permission placement becomes schema, API, runtime behavior, enforcement behavior, security policy, utility export behavior, or operational-control authority.

## Permission Concepts

### PermissionGrant

A `PermissionGrant` records a future explicit homeowner authorization.

Expected concepts:

- grant identity
- twin identity
- grantor identity
- recipient or audience
- purpose
- scope
- duration
- status
- view contract
- exclusions
- consent artifact linkage
- revocation state
- provenance and audit references

### PermissionScope

A `PermissionScope` defines what the grant covers.

Scope may include:

- twin domains
- specific fields
- source documents
- derived outputs
- scenario revisions
- topology lifecycle states
- view contracts
- exports
- allowed actions
- excluded data
- purpose limits
- time limits

### ConsentArtifact

A `ConsentArtifact` records what the homeowner understood and authorized.

Consent should preserve:

- consent text or version
- audience
- purpose
- scope summary
- effective date
- expiration date when applicable
- source of consent
- related permission grant
- revocation terms
- limitation text

### RevocationState

`RevocationState` records whether access is active, expired, revoked, superseded, or otherwise inactive.

Revocation should stop future access where practical. Historical access records may remain for audit, completed-work lineage, dispute resolution, safety, legal retention, or provenance continuity where approved.

## Lifecycle Permission Differences

Permissions should respect lifecycle state.

| Lifecycle state | Permission posture |
| --- | --- |
| Current deployed state | Most sensitive owner-governed state. External views should be minimized, source-linked, purpose-bound, and revocable where practical. |
| Sandbox state | Editable planning workspace. External sharing should be explicit because sandbox assumptions can be mistaken for current or committed facts. |
| Proposed pathway state | Can be shared for planning, scoping, review, or AI grounding only with planning-only labels and provenance. |
| Saved scenario revision state | Historical planning lineage. Sharing should include revision identity and should not imply current validity or full replay. |
| Contractual state | Future approved commitment context. Requires stronger source, consent, audit, and exclusion handling before implementation. |
| Field-verified state | Future verified context. Permission should distinguish the verified field, source, scope, date, and limitations. |
| Utility-reviewed state | Future minimized utility-facing context. Requires explicit homeowner permission, provenance, export purpose, and utility authority boundaries. |
| Operational topology state | Separate future trust domain. Requires separate command/control authorization and security model; not covered by planning permissions. |

## Audience, Purpose, Duration, And Revocation

Every future permission grant should be audience-specific.

Expected audience families:

- homeowner or owner-authorized household participant
- contractor or installer
- engineer or licensed professional reviewer
- utility or utility-facing workflow
- aggregator or grid-program participant
- supplier or manufacturer
- AI advisor or AI-assisted workflow
- internal governance or audit reviewer

Every future permission grant should be purpose-specific.

Example purposes:

- homeowner planning
- contractor scoping
- engineering review input
- product support
- utility-safe interconnection context
- AI grounding
- audit or provenance review

Every future permission grant should define duration.

Duration may be one-time, session-bound, project-bound, time-bound, until revoked, or tied to a future contractual state. "Until revoked" still requires visible revocation handling and audit expectations.

## Utility And Grid-Edge Permission Boundaries

Utility and grid-edge sharing is permissioned, minimized, source-linked, and separate from operational control.

Utility-facing permissions may cover only approved future views such as:

- site/service identity
- source-linked service context
- interconnection context when permissioned and sourced
- minimized equipment or inverter/storage facts
- aggregate load context when approved
- revision identity and export purpose
- provenance and limitation metadata

Utility-facing permissions must not imply:

- unrestricted utility account access
- utility credential access
- full billing history access
- tariff authority
- incentive eligibility
- interconnection approval
- utility submission authority
- DERMS, dispatch, demand response, VPP, aggregator enrollment, device-control, or operational availability

## Future Privacy Enforcement Compatibility

Permission placement should prepare for future privacy enforcement without claiming it exists now.

Future-compatible requirements:

- explicit permission grants before external sharing
- view contracts before role enforcement
- data minimization by audience and purpose
- field/domain/view-level data classification
- revocation state and historical access lineage
- audit events for grant creation, view creation, exports, revocation, and future operational-control-adjacent access
- provenance survival through permissioned views
- encryption/key-management readiness for sensitive permissions, exports, utility context, and future operational-control data

Deferred implementation:

- runtime permission enforcement
- auth, RBAC, ABAC, tenant isolation, or export authorization
- encryption/KMS
- telemetry governance
- privacy policy enforcement
- utility APIs or exports
- operational-control authorization

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating permission grants, scopes, consent artifacts, revocation state, permission audit events, or export authorization
- mapping account roles, subscriptions, users, contractors, engineers, utilities, aggregators, suppliers, manufacturers, or AI agents to view access
- creating, changing, narrowing, or enforcing permissioned view contracts in runtime
- implementing auth, RBAC, ABAC, tenant isolation, privacy enforcement, encryption, telemetry governance, or access monitoring
- creating utility-facing exports, interconnection authority, DERMS, dispatch, demand response, VPP, aggregator, or operational-control permissions
- treating current `/api/*` contracts, account scaffolding, UI visibility, or AI access as permission enforcement

## Sources / Provenance

- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/TopologyLifecycleDomains.md`
- `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md`
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/canonical-authority-discipline/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`

## Summary

Permission placement attaches homeowner-governed authorization to the Residential Energy Twin at twin, domain, field, source-document, derived-output, view, export, and future operational-control-adjacent boundaries. Phase 2 defines placement and guardrails only. Runtime permission enforcement, scoped exports, privacy enforcement, utility sharing behavior, and operational control remain deferred until Matt explicitly approves them.
