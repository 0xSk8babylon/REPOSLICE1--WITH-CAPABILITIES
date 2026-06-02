# ResidentialEnergyTwin Contract v1

Status: canonical Phase 2 contract document
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no schema, migration, runtime, API, auth, RBAC, ABAC, permission enforcement, encryption, telemetry governance, utility API, DERMS, dispatch, operational-control, or canonical runtime model implementation is approved or implied

## Purpose

The `ResidentialEnergyTwin` is the durable, homeowner-governed, source-linked representation of a home's energy-relevant state over time.

It is the canonical aggregate for residential energy planning truth: premise context, physical structures, electrical planning facts, loads, equipment, designs, pathways, scenarios, permissions, provenance, and narrow utility relationship context.

The twin exists so planner, contractor, engineer, utility, supplier, manufacturer, aggregator, AI, and future applications can consume the same underlying home energy record through scoped views instead of creating competing sources of truth.

The Residential Energy Twin is:

- the durable home energy asset
- the canonical aggregate root for homeowner-governed planning state
- the place where structured facts, assumptions, known unknowns, permissions, and provenance persist
- the source for audience-specific view contracts
- the continuity layer for current state, scenario state, revision lineage, and future approved lifecycle states

The Residential Energy Twin is not:

- a planner screen, proposal, contractor project record, permit set, engineering stamp, utility account system, tariff authority, procurement authority, savings guarantee, dispatch controller, DERMS, warranty authority, or prompt-only memory system
- a source of AI-created canonical facts
- proof of compliance, safety, eligibility, approval, installation, field verification, or operational readiness

Applications are consumers. The twin is the asset.

## Aggregate Root

`ResidentialEnergyTwin` is the canonical aggregate root.

Contract v1 defines the aggregate boundary and required governance posture. It does not create a runtime class, table, endpoint, migration, repository boundary, or enforcement behavior.

The aggregate owns the durable relationships among:

- premise identity and home context
- buildings and energy-relevant structures
- electrical infrastructure records
- load records and backup priorities
- equipment product references, assignments, and locations
- safety-relevant records about energy sources, isolation systems, export capabilities, operational modes, verification status, and provenance when approved
- continuity records for lifecycle history, ownership continuity, contractor continuity, infrastructure continuity, utility continuity, safety continuity, permission continuity, and provenance continuity when approved
- design intent and pathway planning records
- scenarios and revision lineage
- permission grants, scopes, consent artifacts, and revocation state when approved
- provenance records and source lineage
- narrow utility relationship context when permissioned and sourced
- scoped view contracts when approved

## Identity Model

Canonical identity concepts:

- `twin_id`: durable identity of the Residential Energy Twin aggregate.
- `home_id`: premise anchor for the residential home or site context.
- `owner_account_id`: homeowner account relationship to the twin.

### twin_id

`twin_id` identifies the durable Residential Energy Twin independently from any one application, screen, scenario, contractor workflow, utility view, AI session, or generated recommendation.

`twin_id` is reserved for a future approved canonical runtime implementation. Until Matt approves the schema, migration, API, permission, provenance, and lifecycle decisions needed to implement it, no current table or route should be treated as the implemented `ResidentialEnergyTwin`.

### home_id

`home_id` anchors records to the residential premise.

In the current planner, `home_id` is the persisted planning anchor for home identity, address context, utility provider field, service size, and many related planning records. Under this contract, `home_id` remains the premise anchor inside the future aggregate. It is not automatically the durable twin aggregate identity.

If Matt later approves a first runtime boundary, `home_id` may be used only as a temporary premise-scoped planning-context anchor as described in `FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md`.

### owner_account_id

`owner_account_id` identifies the homeowner account relationship for the twin.

Account ownership is not permission enforcement. Account role, plan, subscription status, endpoint access, or UI visibility does not authorize sharing, export, contractor review, utility submission, AI access, or operational control.

### Identity Rules

- The twin must have stable identity before external views, exports, or operational workflows depend on it.
- Premise identity, homeowner account relationship, permission grant identity, and view identity must remain separate concepts.
- Identity must not imply verification, access rights, utility authority, engineering approval, or operational-control authority.
- Historical lineage must survive ownership transfer, scenario branching, supersession, revocation, and future lifecycle changes.

## Canonical, Derived, Advisory, And Operational Boundaries

### Canonical State

Canonical state is durable structured twin data recorded inside an approved twin domain.

Canonical state may be declared, imported, demo-seeded, documented, verified, inferred, stale, incomplete, or wrong. Its practical authority depends on provenance, data origin, source type, confidence, verification status, permission scope, and lifecycle state.

### Derived State

Derived state is deterministic or computed intelligence produced from canonical or recorded inputs.

Examples include recommendation profiles, battery/solar sizing ranges, backup-load selection, panel/service posture, inverter/system posture, architecture-fit signals, scenario comparison, completeness scores, compatibility issues, takeoff previews, and provenance summaries.

Derived state is downstream of its inputs. It may be transient or persisted as a versioned artifact, but it does not create canonical facts unless Matt approves a source-backed promotion workflow.

### Advisory State

Advisory state is generated or composed guidance used for explanation, organization, prioritization, comparison, or next-step support.

AI output is advisory unless a future approved workflow promotes a structured, source-backed fact through explicit validation and provenance. AI cannot create canonical facts, permission grants, product truth, engineering approval, code compliance, utility approval, savings guarantees, or operational authorization through prose.

### Operational State

Operational state means installed, commissioned, dispatchable, utility-integrated, field-verified, credentialed, telemetry-backed, or control-capable state.

Operational state is outside current system authority. It requires future explicit contracts for verification, security, audit, permissions, failure behavior, utility relationships, and operational-control isolation.

### Unknown, Placeholder, And Demo State

Unknowns, placeholders, and demo data are allowed only when clearly labeled.

Unknowns should remain visible in twin domains, derived outputs, and views. Placeholder or demo values may support product development and continuity, but they are not factual authority.

## Source-Of-Truth Boundaries

Structured facts outrank generated text.

Authority order for Phase 2:

1. Persisted structured records and accepted architecture contracts.
2. Source documents, data provenance, rule provenance, and approved doctrine.
3. Recorded homeowner declarations, imports, and verified updates with visible provenance.
4. Deterministic derived outputs with inspectability metadata.
5. Scenario revisions and historical snapshots within their recorded fidelity limits.
6. Advisory explanations and AI-generated summaries.

Current broad `/api/*` responses, UI screens, AI context payloads, generated recommendation copy, transient takeoffs, sorted table state, and prompt memory are not the Residential Energy Twin.

Existing planner records can map to future twin domains, but they are not by themselves an implemented canonical Residential Energy Twin model.

## Domain Ownership Boundaries

| Domain | Owns | Does Not Own | Primary Governance |
| --- | --- | --- | --- |
| Premise | Home identity, address context, service context when recorded, owner relationship, premise provenance | Legal title, utility account authority, billing account, proof of verified address/service | Twin Agent |
| Buildings | Energy-relevant structures, building type, distance assumptions, notes, provenance | BIM, structural engineering, permit record, field-verified distance by default | Twin Agent |
| Electrical Infrastructure | Panels, service planning context, panel roles, electrical planning constraints, provenance | NEC compliance, load calculation authority, AHJ approval, stamped design, utility approval | NEC / Electrical Logic Agent with Twin Agent |
| Loads | Load records, backup priority, wattage assumptions, phase, building linkage, provenance | Verified circuit inventory, professional load study, telemetry, load-control permission | Twin Agent with NEC / Electrical Logic Agent |
| Equipment | Product references, model/spec metadata, source documents, assignments, locations, roles | Warranty authority, procurement approval, guaranteed compatibility, live device status | Equipment Agent |
| Safety | Safety-relevant context about energy sources, isolation systems, export capabilities, operational modes, verification status, and supporting provenance | Safety approval, code compliance, AHJ approval, utility approval, interconnection approval, field verification, operational readiness, emergency-response authority, or device-control authority | Twin Agent with NEC / Electrical Logic Agent, Permission / Consent Agent, Security / Audit / Provenance Agent, and Utility / Grid Edge Agent |
| Continuity | Lifecycle history across ownership, contractors, infrastructure, utility context, safety context, permissions, provenance, and software/platform changes | Legal ownership, title ownership, utility authority, regulatory authority, compliance approval, operational control, contractual rights, safety certification, or proof of current state by itself | Twin Agent with Permission / Consent Agent and Security / Audit / Provenance Agent |
| Designs | Design intent, architecture type, status, equipment composition, planning posture | Final electrical design, installation plan, permit package, contractor bid, dispatch authority | Twin Agent with Product Orchestrator |
| Pathways | Route assumptions, source/destination context, distance, difficulty, visibility, confidence | Surveyed route, construction approval, conduit design, trenching approval | Twin Agent with Takeoff / Estimating Agent |
| Scenarios | Planning futures, linked designs, compact revision lineage, labeled placeholders, scenario provenance | Bid, proposal authority, financial guarantee, procurement-ready estimate, full advisor replay by default | Product Orchestrator with Twin Agent |
| Permissions | Permission grants, scopes, consent artifacts, revocation state, permissioned view linkage when approved | Account role, subscription status, generic checkbox, implied consent | Permission / Consent Agent |
| Provenance | Source documents, data provenance, rule provenance, summaries, trust state, confidence, authority metadata | Proof of correctness by itself, access control by itself, professional review | Security / Audit / Provenance Agent |
| Utility Relationships | Narrow provider/service/interconnection/program context when permissioned and sourced | Utility account system, tariff authority, eligibility approval, utility submission, DERMS, dispatch | Utility / Grid Edge Agent with Permission and Provenance review |
| Views | Audience-specific projections with authority, classification, provenance, assumptions, and limits | Canonical source facts, enforcement by themselves, broad endpoint filters relabeled as permissions | Technical Orchestrator with relevant specialists |

## Lifecycle State Model

Contract v1 separates planning state from verified and operational truth.

### Current Deployed State

Current deployed state is the recorded understanding of what exists at the home today.

Allowed content:

- existing panels, loads, structures, equipment, service context, solar/inverter/generator/battery posture, and relevant notes
- source documents, photos, homeowner declarations, imports, and verification markers when available
- explicit unknowns, stale fields, and missing field verification

Boundary:

Recorded current state is not automatically field-verified, code-compliant, safe, commissioned, utility-approved, or operationally controllable.

### Sandbox State

Sandbox state is editable planning work used to explore options.

Allowed content:

- draft designs, proposed equipment assignments, tentative pathways, what-if load sets, rough takeoff assumptions, advisory outputs, and temporary comparisons

Boundary:

Sandbox state does not alter current deployed state, contractual state, permission grants, utility relationship authority, or operational behavior unless a future approved promotion workflow records that transition with provenance.

### Contractual State

Contractual state represents a future approved, source-linked commitment or agreement state, such as an accepted scope, signed proposal, reviewed package, or other contract-backed project artifact.

Contract v1 reserves this state but does not implement it.

Boundary:

Contractual state is not a bid, quote, permit, engineering stamp, procurement approval, utility approval, interconnection approval, or guarantee unless a future authority layer explicitly supports that claim with source provenance and required approvals.

### Future Scenario State

Future scenario state represents possible planning futures.

Allowed content:

- scenario records, linked designs, revision snapshots, comparison outputs, planning tradeoffs, placeholder economics when labeled, and known risks

Boundary:

Future scenario state is not a selected final design, install plan, financial guarantee, or operational state. Scenario revisions preserve lineage at their recorded fidelity; they do not imply full replay unless that is implemented later.

### Future Lifecycle Extensions

Future lifecycle stages may include contractor-reviewed package, engineer-reviewed package, field-verified topology, utility-reviewed context, installed topology, operational topology, decommissioned state, and replacement/expansion state.

These are reserved. They require Matt approval before schema, API, workflow, enforcement, audit, utility, or operational-control implementation.

## State Transition Rules

- No derived or advisory output may promote itself into canonical state.
- No sandbox object may become current deployed, contractual, utility-facing, or operational state without an approved source-backed transition.
- No permission, consent, revocation, export, or operational-control transition may be inferred from account role, UI visibility, endpoint access, or AI text.
- Every transition that increases authority must preserve source lineage, actor, timestamp, scope, assumptions, missing data, and limitation metadata.
- Historical state should remain traceable after supersession, revocation, ownership changes, scenario branching, or future installation events.

## Permission Placement Expectations

Permissions are first-class twin concepts.

Future approved permission structures should live inside or attach directly to the Residential Energy Twin aggregate through:

- `PermissionGrant`
- `PermissionScope`
- `PermissionedView`
- `ConsentArtifact`
- `RevocationState`
- permission audit references
- permission provenance summaries

Permissions should answer:

- who can see or use which twin facts
- for what purpose
- for which audience
- for how long
- under which exclusions
- whether access is active, expired, revoked, or superseded
- which view contract is authorized

Permission is not equivalent to account role, subscription status, endpoint access, UI rendering, contractor relationship, utility relationship, or AI session access.

No current runtime permission enforcement is implied by this document.

## Provenance Placement Expectations

Provenance is required for authority-bearing facts and derived outputs.

Future approved provenance structures should exist at these levels:

- twin-level provenance for overall source coverage and authority limitations
- domain-level provenance for each twin domain
- field-level provenance for important authority-bearing fields
- derived-output provenance for recommendations, comparisons, takeoffs, AI grounding, sizing, scoring, and rule outputs
- safety provenance for energy-source, isolation-system, export-capability, operational-mode, verification-status, and safety-view context
- continuity provenance for lifecycle history, changed fields, actors or source systems, timestamps, supersession, replacement, revocation, stale-state markers, and historical/current-state distinctions
- permission provenance for grants, consent, revocation, and exports
- utility provenance for provider, service, interconnection, tariff, program, and source-document context
- revision provenance for historical snapshots and future replayable state

If provenance is missing, partial, stale, conflicting, inferred, placeholder, or demo-sourced, the twin and its views should expose that limitation rather than fill the gap with confident language.

Provenance does not replace permission. Permission does not replace provenance.

## Utility Relationship Placement Expectations

Utility relationship context belongs in the twin only as narrow, permissioned, source-linked context.

It may include, when approved and sourced:

- utility provider
- service context
- service territory
- meter or service identifiers where permissioned
- interconnection context
- program context
- tariff/source documents as reference context
- utility-facing permission scope
- utility provenance summary

It must not include by default:

- unrestricted utility account access
- utility credentials
- full billing history
- tariff authority
- incentive eligibility authority
- savings guarantees
- interconnection approval claims
- utility submission authority
- DERMS, dispatch, aggregator enrollment, or operational-control semantics

Utility sharing is permissioned, minimized, source-linked, revocable where practical, and separate from operational control.

## View Contract Expectations

Same twin. Different views.

A view is an audience-specific projection of selected canonical facts, derived outputs, advisory text, unknowns, assumptions, and provenance. A view does not become canonical.

Future view contracts should be explicit, named, additive, and purpose-bound. Existing broad `/api/*` responses must not be silently narrowed or reclassified as permissioned twin views.

Every future view should preserve:

- stable object identity for exposed records
- authority layer
- lifecycle state
- trust zone
- data classification
- source and provenance summary
- data origin
- confidence and verification posture
- assumptions and missing inputs
- derived-output rule keys where relevant
- limitations and non-authoritative labels
- permission scope and view purpose when enforcement exists

Expected future view families:

- homeowner planning view
- contractor scoping view
- engineer review-input view
- safety-scoped view for minimum necessary safety context when explicitly approved
- continuity/history view for minimum necessary lifecycle history when explicitly approved
- AI grounding view
- supplier/manufacturer product-support view
- future utility-safe view
- future operational-control-adjacent view only after a separate authority model exists

## Trust-Boundary Rules

- The twin is homeowner-governed.
- Structured facts outrank generated text.
- AI remains advisory and cannot create canonical facts.
- Permissions are first-class and cannot be replaced by account roles or endpoint access.
- Provenance is required for authority-bearing facts, product/spec data, derived intelligence, and utility-facing context.
- Utility sharing must be permissioned, scoped, minimized, source-linked, and non-authoritative unless a future authority layer supports stronger claims.
- Electrical, NEC, permitting, safety, AHJ, interconnection, tariff, incentive, savings, procurement, and bid claims remain outside current system authority.
- Cybersecurity must be layered into identity, permission, view, provenance, audit, classification, and future operational-control design. It is not a later cosmetic layer.
- Operational control remains a separate future trust domain.
- Current data classification and scoped-view language is design metadata only, not RBAC, ABAC, tenant isolation, or export enforcement.
- Do not overclaim compliance, approval, verification, eligibility, safety, savings, or operational readiness.

## Future Privacy And Security Compatibility

Contract v1 must remain compatible with later privacy/security layers without pretending they exist now.

Future-compatible requirements:

- field/domain/view-level data classification
- permission grants before external sharing
- revocation state and historical access/audit lineage
- scoped views before RBAC/ABAC enforcement
- data minimization by audience and purpose
- provenance survival through views and exports
- audit events for exports, view creation, grant changes, revocation, and future operational events
- encryption and key-management readiness for sensitive twin, permission, utility, and operational-control data
- telemetry governance readiness before telemetry becomes source or operational truth
- strict separation between homeowner planning privacy and grid-edge asset integrity needs

Deferred implementation:

- authentication
- authorization
- RBAC
- ABAC
- tenant isolation
- encryption/KMS
- telemetry governance
- access monitoring
- export enforcement
- security event tracking
- utility-grade security posture
- critical-infrastructure compliance claims

This contract supports those future layers. It does not implement or certify them.

## Future Utility And Grid-Edge Compatibility

The twin should be compatible with future utility/grid-edge workflows only through permissioned, minimized, source-linked abstractions.

Future-compatible requirements:

- service/site identity with source provenance
- equipment and topology identity with lifecycle state
- interconnection context only when sourced and permissioned
- utility-safe view contracts before export behavior
- provenance and revision identity on utility-facing packets
- explicit limitation text for tariff, program, eligibility, export, and approval status
- auditability of future sharing events
- cybersecurity posture appropriate for grid-edge trust before utility-facing operational integration

Deferred implementation:

- utility APIs
- utility submissions
- utility account linking
- tariff authority
- incentive eligibility
- interconnection authority
- DERMS
- demand response
- VPP or aggregator participation
- dispatch or device availability
- grid services

Future utility compatibility must not become uncontrolled utility access to homeowner data.

## Future Twin Intelligence Grounding

Future Phase 3 Twin Intelligence may use provider-backed production calculations, benchmark-backed market/economic checks, and verified product intelligence only as derived grounding layers.

See `SolarMarketProductIntelligenceGrounding.md` for the Phase 2 architecture bridge. That document does not approve provider integrations, schemas, APIs, spec-sheet ingestion, product catalogs, AI engineering automation, utility APIs, telemetry, or operational control.

The Residential Energy Twin remains homeowner-governed. AI may explain future grounded outputs, but deterministic providers, normalized product evidence, structured quotes, benchmarks, and rules remain the source for production, economic, and product-capability outputs.

## Future Operational-Control Separation

Operational control is a separate future trust domain.

The Residential Energy Twin may eventually provide source-linked context to an operational-control system, but the twin contract does not authorize commands, dispatch, load shedding, device enrollment, telemetry ingestion as truth, failover behavior, DERMS behavior, or aggregator control.

Before any operational-control work exists, the project needs separate approved contracts for:

- operational identity and device capability authority
- command authorization
- homeowner consent for control actions
- utility/aggregator authority and limits
- telemetry source validation
- failure and fallback behavior
- audit/event lineage
- cybersecurity posture
- key management and credential boundaries
- separation between planning views and control surfaces

Operational-control data should be classified separately from planning data. Operational-control authority must never be inferred from the existence of a twin, a utility relationship, a scenario, an AI recommendation, or a permissioned planning view.

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating or modifying a canonical `ResidentialEnergyTwin` runtime data model
- deciding whether `twin_id` is a new persistent identifier or whether `home_id` temporarily acts as a runtime planning-context anchor
- changing schemas, migrations, persistence contracts, or canonical data models
- defining required fields, validation rules, lifecycle states, or topology ownership for twin domains
- implementing permission grants, consent artifacts, revocation semantics, homeowner authorization, scoped exports, or view lifecycle rules
- implementing auth, RBAC, ABAC, tenant isolation, encryption, telemetry governance, access monitoring, audit enforcement, or security posture changes
- creating contractor, engineer, utility, supplier, manufacturer, aggregator, AI, or operational-control view contracts in runtime
- changing existing compatibility-sensitive `/api/*` contracts
- defining provenance policy, provenance completeness thresholds, trust-state semantics, authority-layer semantics, or data-classification policy as runtime behavior
- promoting derived outputs, AI output, recommendations, takeoffs, scenario comparisons, or compatibility issues into canonical facts
- defining utility relationship authority, utility-facing export behavior, service-territory authority, tariff authority, interconnection authority, DERMS, dispatch, program participation, or operational-control semantics
- implementing NEC, electrical-code, load-calculation, permitting, AHJ, stamped-engineering, pricing, savings, payback, incentive, estimate, procurement, or bid authority
- changing trust language that could imply certainty, compliance, approval, savings, safety, authorization, professional review, utility approval, or operational readiness

## Sources / Provenance

- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/architecture/COGNITION_LAYERS.md`
- `docs/architecture/CANONICAL_TERMINOLOGY.md`
- `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md`
- `docs/architecture/ContinuityDomain.md`
- `docs/architecture/SafetyDomain.md`
- `docs/architecture/SolarMarketProductIntelligenceGrounding.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/provenance/RESIDENTIAL_ENERGY_TWIN_PROVENANCE_POLICY_PLANNING.md`
- `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md`
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- `docs/topology/TOPOLOGY_LIFECYCLE.md`
- `docs/orchestration/READINESS_GAPS.md`
- `.codex/skills/repo-memory-map/SKILL.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/canonical-authority-discipline/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `.codex/project-skills/topology-intelligence/SKILL.md`
- `.codex/project-skills/orchestration-readiness/SKILL.md`

## Summary

`ResidentialEnergyTwin` Contract v1 defines the Phase 2 canonical aggregate boundary as documentation and governance only. It establishes the twin as a homeowner-governed, source-linked, permission-aware, provenance-bearing planning asset while reserving runtime identity, persistence, enforcement, utility, privacy/security, and operational-control implementation for later Matt-approved work.
