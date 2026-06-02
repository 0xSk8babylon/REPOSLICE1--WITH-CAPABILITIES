# View Contracts

Status: Phase 2 architecture planning document
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no schema, migration, runtime view enforcement, API, auth, RBAC, ABAC, encryption, telemetry governance, utility API, DERMS, dispatch, operational-control, or scoped runtime view implementation is approved or implied

## Purpose

View contracts define how different actors should receive permission-filtered, provenance-preserving projections of the Residential Energy Twin.

This document extends `ResidentialEnergyTwinContractV1.md`, `TopologyLifecycleDomains.md`, `PermissionPlacement.md`, and `ProvenancePlacement.md`. It completes Phase 2 architecture for actor-specific view boundaries, but it does not create endpoints, schemas, filters, exports, RBAC, ABAC, tenant isolation, utility packets, contractor packets, AI tools, audit APIs, or operational-control views.

## Core Principle

Same twin. Different views.

The Residential Energy Twin remains the canonical aggregate. A view is a scoped projection for an audience and purpose. A view does not become canonical, does not grant access by itself, and does not replace provenance.

Existing broad `/api/*` responses are compatibility-sensitive product contracts. They must not be silently narrowed or reclassified as permissioned twin views.

## Shared View Contract Requirements

Every future view contract should define:

- view name
- actor or audience
- purpose
- permission basis
- lifecycle state coverage
- included domains and fields
- excluded domains and fields
- source and provenance requirements
- authority layer
- trust zone
- data classification
- derived-output handling
- advisory text handling
- missing data and assumption handling
- revocation and expiration expectations when enforcement exists
- audit expectations when implementation exists
- limitation text preventing overclaiming

Every future view should preserve:

- stable object identity for included records
- current-vs-sandbox-vs-scenario-vs-contractual boundaries
- recorded-vs-derived-vs-advisory separation
- source documents or source summaries where needed
- confidence and verification posture
- missing inputs and known unknowns
- planning-only labels for estimates, recommendations, and comparisons
- permission scope and purpose when approved runtime permission exists

Every future view should exclude:

- hidden AI-created facts
- unsupported compliance, safety, permit, AHJ, engineering, utility, tariff, incentive, savings, bid, procurement, or operational claims
- raw unrelated homeowner/private data
- broad utility, account, source-document, provenance, or internal governance data when a minimized summary is enough
- operational-control authority, device commands, dispatch, DERMS, demand response, VPP, aggregator participation, telemetry authority, or credentials

## Data Minimization

View contracts should expose the minimum information needed for the actor and purpose.

Data minimization should consider:

- whether the actor needs field-level facts or only summaries
- whether source documents are needed or only source summaries
- whether load detail can be aggregated
- whether homeowner notes are relevant
- whether derived outputs are necessary or advisory copy is enough
- whether product specs should be narrowed to relevant fields
- whether utility context is necessary and permissioned
- whether internal rule/provenance records should be summarized

Minimization must not hide uncertainty. A minimized view should still preserve missing data, assumptions, confidence, limitations, and provenance posture.

## Permission-Filtered Visibility

Future view visibility should be permission-filtered before it is actor-filtered.

Account role, endpoint access, UI visibility, subscription status, utility relationship, contractor relationship, or AI session access is not a permission grant.

Permission-filtered visibility should consider:

- grantor
- audience
- purpose
- duration
- active/revoked/expired/superseded state
- allowed domains and fields
- excluded domains and fields
- source-document visibility
- derived-output visibility
- export rights
- audit requirements

Until runtime permission enforcement exists, these view contracts are design boundaries only.

## Provenance-Preserving Outputs

Every view that exposes authority-bearing facts, derived outputs, or advisory guidance should carry provenance at the narrowest useful level.

Expected provenance in views:

- source summary
- data origin
- authority layer
- trust zone
- data classification
- confidence and verification posture
- missing inputs
- assumptions
- limitation text
- rule keys for derived outputs
- revision identity for historical snapshots
- permission scope for external views when implemented

If provenance is missing or partial, the view should say so instead of filling the gap with confident text.

## Actor-Specific View Contracts

### Homeowner View

Purpose:

Support owner-governed planning, comparison, missing-data review, provenance visibility, and future permission management.

May include:

- broad owner planning context for the homeowner's own twin
- premise, buildings, panels, loads, equipment, designs, pathways, scenarios, revisions, provenance summaries, and planning advisor outputs
- unknowns, assumptions, placeholders, missing inputs, and confidence labels
- future permission status and grant history after permission model approval

Must exclude or label:

- engineering, code, permit, AHJ, utility, tariff, incentive, savings, bid, procurement, safety, or operational approval claims
- external-party access claims before permission enforcement exists
- hidden AI-created facts
- operational-control state, commands, dispatch, DERMS, telemetry authority, or credentials

### Contractor View

Purpose:

Support scoping, site walks, early coordination, route review, product review, and rough planning context.

May include:

- scoped site, building, panel, load, equipment, pathway, design, and missing-data records relevant to the project
- product references and selected source documents
- route assumptions, quantities, roles, confidence, and verification gaps
- planning-only advisor outputs that explain basis and limitations

Must exclude or label:

- unrelated homeowner notes or private context
- account/subscription scaffolding
- utility submission posture or interconnection approval
- stamped design, code-compliance, estimate, bid, procurement, warranty, or safety guarantees
- operational-control context

### Engineer View

Purpose:

Provide organized factual inputs and source lineage for professional review.

May include:

- panel, load, equipment, pathway, design, topology, source-document, and provenance context
- field-level and domain-level provenance where available
- assumptions, inferred fields, unknowns, limitations, and derived-output lineage
- planning outputs as non-authoritative context

Must exclude or label:

- language implying the system performed engineering review
- unproven code, permit, AHJ, safety, or utility approval claims
- hidden assumptions or advisory prose presented as fact
- operational-control, dispatch, DERMS, or telemetry authority

### Utility View

Purpose:

Provide minimized, permissioned, source-linked utility-relevant context after Matt-approved utility authority and export design exists.

May include after future approval:

- minimized service/site identity
- source-linked service context
- interconnection context when permissioned and sourced
- selected equipment/inverter/storage/generator/PV facts
- aggregate load context when approved
- provenance, revision identity, export purpose, and limitation metadata

Must exclude or label:

- broad homeowner planning notes
- household appliance detail unless required and authorized
- AI advisory text
- contractor notes unrelated to utility purpose
- tariff authority, incentive eligibility, savings claims, utility approval, interconnection approval, submission authority, or program enrollment claims
- operational dispatch, DERMS, aggregator enrollment, device-control, availability, telemetry, or credentials

Utility views are deferred until explicit authority, permission, provenance, export, audit, and security expectations exist.

### Safety-Scoped View

Purpose:

Provide minimized, permissioned, source-linked safety context for a defined audience and purpose after Matt-approved safety-view design exists.

May include after future approval:

- safety-relevant energy sources
- isolation systems
- export-capability context
- operational-mode context
- verification status and verification scope
- provenance, confidence, missing inputs, assumptions, and limitation metadata
- lifecycle state and revision identity when relevant

Must exclude or label:

- unrelated homeowner/private context
- broad planning notes not needed for the safety purpose
- unsupported code, permit, AHJ, safety, utility, interconnection, export, inspection, or operational-readiness claims
- emergency-response authority, field-verification authority, utility approval, dispatch, DERMS, device-control, availability, telemetry authority, or credentials

Safety-scoped views are deferred until explicit permission, provenance, verification-scope, audit, and view-contract expectations exist.

### Aggregator View

Purpose:

Reserve a future minimized view for potential grid-program or aggregation context.

May include after future approval:

- permissioned capability context
- relevant equipment/topology facts
- constraints and availability context only when sourced
- program participation context only when authorized
- provenance, revision identity, purpose, and limitation metadata

Must exclude or label:

- implied enrollment, dispatch authority, performance guarantee, availability claim, grid-service commitment, tariff/program eligibility, or operational-control permission
- raw household planning detail not needed for the approved purpose
- utility secrets, credentials, telemetry authority, or command capability

Aggregator views are deferred and must not be created before permission, utility/grid-edge, security, and operational-control boundaries are approved.

### Supplier / Manufacturer View

Purpose:

Support product support, documentation, compatibility review, substitution discussion, or warranty-adjacent context when authorized.

May include:

- scoped product references
- selected equipment assignments, quantities, and roles
- relevant design need context
- source documents and product provenance summaries
- compatibility assumptions and unknowns

Must exclude or label:

- full home record by default
- unrelated homeowner notes
- utility account or private household data
- guaranteed compatibility, availability, warranty approval, procurement approval, or performance claims
- operational device status unless a future source-backed operational authority exists

### AI Advisor View

Purpose:

Provide minimized structured grounding context for explanation, summarization, comparison, organization, and planning support.

May include:

- stable object IDs
- source-linked facts
- provenance summaries
- rule keys
- derived outputs separated from advisory text
- missing inputs, assumptions, limitations, and trust posture
- data classification and authority-layer metadata

Must exclude or label:

- broad raw object dumps when summaries are sufficient
- unrelated account/private records
- hidden prompt-only facts
- permission grants outside the AI task scope
- utility secrets, credentials, raw operational-control data, telemetry authority, command authority, or write authority
- generated prose as canonical fact

AI may explain and organize. AI may not create canonical facts, permission grants, verification claims, compliance claims, utility authority, or operational authorization.

## Future Grounding-Layer Views

Future views may expose solar production grounding, market/economic grounding, and verified product intelligence only as permission-filtered, provenance-preserving derived or reference context.

See `SolarMarketProductIntelligenceGrounding.md` for the Phase 2 bridge. Homeowner, contractor, engineer, utility, aggregator, supplier/manufacturer, AI, and audit views should minimize grounding-layer fields by audience and preserve provider/source references, confidence, assumptions, missing inputs, limitations, and estimated/modeled/quoted/verified/benchmarked labels.

Grounding-layer views must not imply provider integration, partnership, verified pricing, guaranteed savings, production guarantee, product compatibility approval, engineering approval, utility approval, operational authority, or AI-based authority of record.

### Audit View

Purpose:

Reserve a future internal governance view for source lineage, permission changes, exports, revocation, view creation, and future operational-control-adjacent audit events.

May include after future approval:

- source-document summaries
- data provenance
- rule provenance
- permission grant and revocation lineage
- view/export lineage
- actor, timestamp, purpose, scope, and limitation metadata
- security/audit event summaries when implemented

Must exclude or label:

- broad homeowner data when audit summaries are sufficient
- operational credentials or secrets
- security posture claims not implemented
- critical-infrastructure, utility, government, NERC/CIP, or national-defense compliance claims unless separately implemented and verified

Audit views are not a substitute for runtime audit policy, security controls, or enforcement.

## No Direct Operational-Control View

Phase 2 has no direct operational-control view.

Operational-control context is a separate future trust domain that may require:

- operational device identity
- command authorization
- homeowner consent for control actions
- utility/aggregator authority and limits
- telemetry source validation
- failure and fallback behavior
- audit/event lineage
- cybersecurity posture
- key management and credential boundaries
- separation between planning views and control surfaces

No planning view, utility view, AI view, contractor view, or permissioned planning export may imply dispatch, DERMS, device control, telemetry authority, load shedding, availability, grid-service participation, or operational authorization.

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating runtime view schemas, endpoints, filters, exports, or scoped API contracts
- narrowing or reclassifying existing compatibility-sensitive `/api/*` contracts
- implementing permission-filtered visibility, auth, RBAC, ABAC, tenant isolation, encryption, telemetry governance, access monitoring, or audit enforcement
- mapping users, account roles, contractors, engineers, utilities, aggregators, suppliers, manufacturers, AI agents, or internal auditors to view access
- creating contractor packets, engineer packets, utility packets, supplier/manufacturer packets, AI tools, audit APIs, or export behavior
- implementing utility authority, tariff authority, interconnection authority, DERMS, dispatch, demand response, VPP, aggregator, or operational-control semantics
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
- `docs/architecture/SafetyDomain.md`
- `docs/architecture/SolarMarketProductIntelligenceGrounding.md`
- `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md`
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/canonical-authority-discipline/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`

## Summary

View contracts define actor-specific, permission-filtered, provenance-preserving projections of the Residential Energy Twin. Phase 2 defines the expected homeowner, contractor, engineer, utility, aggregator, supplier/manufacturer, AI advisor, and audit view boundaries. It explicitly excludes direct operational-control views and leaves runtime APIs, enforcement, exports, utility integration, and operational control deferred until Matt approves them.
