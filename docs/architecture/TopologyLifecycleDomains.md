# Topology Lifecycle Domains

Status: Phase 2 architecture planning document
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no schema, migration, runtime, API, auth, RBAC, ABAC, permission enforcement, encryption, telemetry governance, utility API, DERMS, dispatch, operational-control, or canonical runtime topology implementation is approved or implied

## Purpose

Topology lifecycle domains define how the Residential Energy Twin should represent changes to a home's energy topology over time without collapsing recorded current state, proposed planning state, saved scenario state, contractual state, field-verified state, utility-facing state, or future operational-control state.

This document extends `ResidentialEnergyTwinContractV1.md` for topology-specific architecture. It is not an implementation plan and does not approve any runtime topology graph, lifecycle table, event log, migration, scoped API view, utility export, or operational-control surface.

## Topology Definition

Topology is the structured relationship among energy-relevant objects in the Residential Energy Twin.

Topology may include:

- premise and service context
- buildings and structures
- electrical panels and service equipment
- loads and backup priority groupings
- equipment products, roles, assignments, and locations
- solar, inverter, storage, generator, transfer, and backup architecture posture
- pathways between structures, panels, equipment, and future upgrade locations
- designs, scenarios, and scenario revisions
- provenance, permission, and view metadata attached to topology facts
- narrow utility relationship context when permissioned and sourced

Topology is not:

- proof of installed or commissioned state by default
- NEC compliance, AHJ approval, stamped engineering, utility approval, or interconnection approval
- live telemetry or device status
- dispatch, DERMS, demand response, VPP, aggregator enrollment, or operational-control authority
- AI-created canonical truth

## Lifecycle Domain Model

Each topology fact should belong to a lifecycle domain before downstream views, recommendations, or future integrations rely on it.

| Lifecycle domain | Meaning | Current status | Authority boundary |
| --- | --- | --- | --- |
| Recorded current topology | The system's recorded understanding of what exists at the home today. | Partially represented through persisted planning records and advisor current-home architecture outputs. | Recorded planning fact, not automatically field-verified, compliant, utility-approved, or operational. |
| Sandbox planning topology | Editable what-if topology used to explore options. | Partially represented through design workspaces, equipment assignments, pathways, and advisor summaries. | Planning-only; cannot change current deployed state or create commitments by itself. |
| Proposed pathway topology | A named design or pathway candidate that organizes planned equipment, backup scope, routes, and architecture direction. | Partially represented through designs, estimated pathways, recommendation profiles, and structured reasoning graph outputs. | Proposed planning state; not final design, bid, permit, or install authority. |
| Saved scenario revision topology | Historical snapshot of a planning state at a point in time. | Partially represented through immutable scenario revisions with compact planning-state snapshots. | Historical lineage only; not full replay unless a future full-fidelity revision graph is implemented. |
| Contractor-reviewed topology | A future contractor-scoped package reviewed for scoping or coordination. | Deferred. | Contractor planning context only; not engineering, permitting, utility, safety, or bid authority unless separate approved artifacts support it. |
| Contractual topology | A future source-linked commitment state such as accepted scope or signed proposal context. | Deferred. | Contractual context only; not permit, utility, engineering, procurement, or operational authority by default. |
| Field-verified topology | A future topology state backed by inspection, source documents, photos, commissioning records, or professional confirmation. | Deferred. | Verified only within the scope and source of the verification; does not automatically grant code, utility, or operational authority. |
| Utility-reviewed topology | A future minimized, permissioned, source-linked topology view relevant to utility workflows. | Deferred. | Not utility approval, interconnection approval, tariff authority, program eligibility, or dispatch authority without utility-source evidence and approved contracts. |
| Operational topology | A future control-adjacent topology with device identity, telemetry, command, credential, failure, and audit boundaries. | Deferred. | Separate trust domain; no operational authority exists in Phase 2. |
| Future expansion or replacement topology | Future state used to preserve upgrade, replacement, decommissioning, and scenario lineage. | Deferred beyond compact scenario history. | Planning or historical lineage unless promoted by future approved source-backed transitions. |

Only recorded current topology, sandbox planning topology, proposed pathway topology, and saved scenario revision topology are partially represented in the current product. Even there, coverage is planning-oriented and incomplete.

## Domain Placement

Topology lifecycle state can attach to multiple Residential Energy Twin domains. Placement should follow the source of truth for the fact.

| Twin domain | Topology role | Lifecycle concern |
| --- | --- | --- |
| Premise | Anchors the home, service context, owner relationship, and utility provider field when recorded. | Must not imply legal title, verified service, or utility account authority. |
| Buildings | Places loads, panels, equipment, and pathways in physical structures. | Distances and structure roles remain assumptions unless source-linked or field-verified. |
| Electrical Infrastructure | Places panels, service equipment, panel roles, and electrical constraints. | Must distinguish recorded panel facts from derived panel/service posture and professional review. |
| Loads | Places energy uses and backup priority within buildings and planning scopes. | Must distinguish recorded load records from measured demand, circuit inventory, telemetry, and control rights. |
| Equipment | Places products, roles, quantities, existing/proposed posture, and locations. | Must distinguish product references and proposed assignments from installed device status. |
| Designs | Organizes proposed architecture and equipment composition. | Must not overwrite current topology unless a future approved promotion transition exists. |
| Pathways | Models routes between topology nodes. | Must expose estimated distance, confidence, route difficulty, visibility, and missing field verification. |
| Scenarios | Preserves option branches and revision snapshots. | Must not imply selected final design, full replay, or installed state. |
| Permissions | Governs who may see, export, or act on topology views when approved. | Must not infer permission from account role, endpoint access, or UI visibility. |
| Provenance | Tracks source, confidence, authority, assumptions, and missing inputs for topology facts and derived outputs. | Must expose partial, stale, inferred, placeholder, or missing lineage. |
| Utility Relationships | Holds narrow utility/service/interconnection context when permissioned and sourced. | Must not imply utility approval, tariff authority, DERMS, dispatch, or operational control. |

## Current Phase 2 Topology Capabilities

Current product capabilities are planning-oriented:

- persisted home, building, panel, load, equipment, design, pathway, scenario, and scenario revision records
- recorded equipment roles and existing-vs-proposed posture in selected advisor outputs
- current solar/inverter topology classification from recorded equipment roles and product signals
- backup scope, panel/service posture, inverter/system architecture posture, profile architecture fit, and reasoning graph outputs as derived planning intelligence
- compact scenario revision snapshots for historical comparison
- partial provenance summaries and rule provenance for selected topology-related outputs

Current product gaps:

- no canonical runtime `ResidentialEnergyTwin` topology graph
- no lifecycle event log
- no field-verified topology model
- no topology promotion workflow
- no full-fidelity scenario or twin revision graph
- no utility interconnection state authority
- no operational device identity, telemetry authority, dispatch, DERMS, demand response, VPP, aggregator, or control surface
- no permission enforcement, RBAC, ABAC, scoped export enforcement, or utility-facing export authority

## State Transition Expectations

Future topology transitions should be explicit, source-backed, and auditable.

Required transition metadata should include:

- source lifecycle domain
- target lifecycle domain
- actor or source system
- timestamp
- source documents or structured source records
- affected object IDs and fields
- data origin
- provenance summary
- confidence and verification posture
- assumptions and missing inputs
- permission scope when a view, export, or external party is involved
- limitation text preventing overclaiming

No topology transition should be inferred from:

- AI-generated text
- recommendation profile selection
- scenario comparison ranking
- design status label alone
- account role, plan, or subscription status
- UI visibility
- broad API access
- utility provider text field
- equipment product compatibility note

## Canonical, Derived, Advisory, And Operational Topology

Canonical topology is recorded structured topology state inside approved twin domains.

Derived topology is deterministic interpretation of recorded topology, such as panel/service posture, backup architecture consistency, inverter/system architecture posture, current-home architecture classification, pathway complexity, and scenario drift comparison.

Advisory topology is explanation or guidance about topology, including AI summaries and recommendation copy.

Operational topology is future installed, commissioned, telemetry-backed, dispatchable, command-authorized, or control-capable topology. It is outside current authority and must remain separate from planning topology.

Derived and advisory topology may help users understand options. They do not promote facts, verify installation, create permission, authorize utility sharing, or enable operational control.

## Provenance Expectations

Topology provenance should survive through canonical records, derived outputs, views, and future revisions.

Topology provenance should identify:

- source objects and source documents
- source type and data origin
- lifecycle domain
- authority layer
- trust zone
- data classification
- verification status
- confidence level
- missing inputs
- assumptions
- limitation text
- rule keys for derived topology
- revision identity when persisted historically

If topology provenance is missing or partial, the topology state should remain labeled as recorded, inferred, placeholder, estimated, unknown, or planning-only instead of being promoted into stronger authority.

## View And Permission Expectations

Topology views should be scoped by audience, purpose, permission, lifecycle domain, provenance, and authority.

Future topology views should preserve:

- stable object identity
- lifecycle domain
- existing-vs-proposed posture
- current-vs-sandbox-vs-scenario boundaries
- source and provenance summary
- data classification
- missing field verification
- derived-output basis and rule keys
- limitation text

Future topology views must not expose or imply:

- homeowner data sharing without permission
- contractor authorization without an approved view contract
- engineering, code, permit, AHJ, or safety approval
- utility submission, utility approval, tariff authority, interconnection authority, or program eligibility
- operational-control authority, device commands, dispatch, DERMS, demand response, VPP, aggregator participation, or telemetry authority

## Future Privacy, Security, Utility, And Operational Compatibility

Topology lifecycle domains should prepare the system for future privacy and security layers without claiming they exist now.

Future-compatible needs:

- field/domain/view-level data classification for topology facts
- permission grants and revocation state before external sharing
- provenance survival through scoped topology views and exports
- audit events for future view creation, exports, topology promotions, field verification, utility sharing, and operational-control-adjacent events
- encryption/key-management readiness for sensitive topology, utility, permission, and operational-control data
- telemetry governance before telemetry becomes source truth
- utility-safe topology abstractions before utility exports
- separate operational-control contracts before commands, dispatch, telemetry authority, or device-control behavior

Deferred implementation:

- runtime topology graph
- lifecycle event log
- field verification workflow
- scoped topology APIs
- permission enforcement
- auth, RBAC, ABAC, tenant isolation
- encryption/KMS
- telemetry governance
- utility APIs or exports
- interconnection or tariff authority
- DERMS, dispatch, demand response, VPP, aggregator participation
- operational control

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating a canonical topology graph, lifecycle event table, topology revision graph, or topology promotion workflow
- changing `ResidentialEnergyTwin` domain ownership, lifecycle states, topology ownership, or canonical boundaries
- changing schema, migrations, persistence contracts, or canonical data models
- implementing field-verified topology, contractor-reviewed topology, contractual topology, utility-reviewed topology, or operational topology
- implementing topology permission grants, scoped topology views, exports, consent artifacts, revocation, or audit events
- implementing auth, RBAC, ABAC, tenant isolation, encryption, telemetry governance, access monitoring, or security posture changes
- creating utility-facing topology exports, interconnection context authority, tariff authority, DERMS, dispatch, demand response, VPP, aggregator, or operational-control semantics
- promoting derived advisor, AI, takeoff, compatibility, scenario comparison, or recommendation outputs into canonical topology facts
- changing trust language that could imply installation, verification, compliance, utility approval, safety, savings, authorization, or operational readiness

## Sources / Provenance

- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/topology/TOPOLOGY_LIFECYCLE.md`
- `docs/architecture/COGNITION_LAYERS.md`
- `docs/architecture/CANONICAL_TERMINOLOGY.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/project-skills/topology-intelligence/SKILL.md`
- `.codex/project-skills/canonical-authority-discipline/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`

## Summary

Topology lifecycle domains define how Residential Energy Twin topology facts should move from recorded current state through planning, scenario, future reviewed, future verified, future utility-facing, and future operational states without authority inflation. The current product supports only planning-oriented portions of this model. Runtime topology implementation, enforcement, utility integration, and operational control remain deferred until Matt explicitly approves them.
