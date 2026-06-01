# ResidentialEnergyTwin Contract v1

Status: canonical contract proposal for Matt approval
Scope: documentation and governance only
Implementation status: no schema, migration, runtime, API, auth, permission-enforcement, utility, DERMS, dispatch, or canonical model implementation is approved or implied

## Purpose

The `ResidentialEnergyTwin` is the durable, homeowner-governed, source-linked representation of a home's energy-relevant state over time.

It is the canonical aggregate for residential energy truth: premise context, structures, electrical planning facts, loads, equipment, designs, pathways, scenarios, permissions, provenance, and narrow utility relationship context.

The Residential Energy Twin exists so applications can consume the same underlying home energy record without becoming competing sources of truth.

The Residential Energy Twin is:

- the durable asset
- the canonical home energy aggregate
- the homeowner-governed system of record
- the permissioned source for views and applications
- the place where structured facts, assumptions, provenance, permissions, and known unknowns persist
- the basis for planner, contractor, engineer, utility, supplier, manufacturer, aggregator, and AI views

The Residential Energy Twin is not:

- a planner screen
- a proposal
- a contractor project record
- a utility account system
- an engineering stamp
- a permit set
- an AHJ decision
- a final bill of materials
- a procurement authority
- a utility approval system
- a tariff authority
- a savings guarantee
- a dispatch controller
- an operational DERMS
- a warranty authority
- an energy trading account
- a prompt-only memory system
- a source of AI-created canonical facts

Applications are consumers. The twin is the asset.

## Aggregate Root

`ResidentialEnergyTwin` is the aggregate root.

Canonical identity fields:

- `twin_id`
- `home_id`
- `owner_account_id`

### twin_id

`twin_id` is the durable identity of the Residential Energy Twin.

It identifies the canonical home energy record independently from any one application, screen, scenario, contractor workflow, utility view, AI session, or generated recommendation.

### home_id

`home_id` anchors the twin to the residential premise.

In the current planner architecture, `Home` is the persisted planning anchor for home identity, address context, utility provider field, service size, and related home records. Under this contract, `home_id` remains the premise anchor inside the aggregate, while `twin_id` identifies the canonical twin as the durable aggregate.

### owner_account_id

`owner_account_id` identifies the homeowner account relationship for the twin.

Account ownership is not the same as permission enforcement. Account role, plan, or subscription status may support future access workflows, but they do not by themselves authorize access, sharing, export, utility submission, contractor review, AI access, or operational control.

### Why The Twin Is Canonical

The Residential Energy Twin is canonical because it persists beyond applications.

Planner pages, advisor summaries, AI context payloads, contractor packets, utility views, supplier views, generated takeoffs, and scenario comparison screens are views or projections. They consume and may enrich the twin within approved authority boundaries, but they do not become the source of truth.

Canonical status belongs to the twin because it holds durable home energy context:

- recorded facts
- declared homeowner intent
- documented evidence
- verified updates
- labeled assumptions
- missing information
- provenance
- permission decisions
- planning history
- utility relationship context when authorized

## Twin Domains

### 1. Premise

Purpose:

Premise anchors the Residential Energy Twin to the home, site, owner relationship, address context, service context, and planning history.

Canonical Records:

- premise identity
- home name
- address fields
- geographic/site context when available
- service size when recorded
- utility provider field when recorded
- owner account relationship
- premise notes when energy-relevant
- premise data origin
- premise provenance summary

Dependencies:

- Buildings depend on premise identity.
- Electrical Infrastructure depends on premise/service context.
- Loads depend on premise identity.
- Designs, Pathways, Scenarios, Permissions, Provenance, Utility Relationships, and all views depend on premise identity.

Ownership:

- Primary: Twin Agent
- Supporting: Backend Agent, Permission / Consent Agent, Security / Audit / Provenance Agent

Non-Goals:

- Not a utility account authority.
- Not a legal property title system.
- Not a full homeowner profile.
- Not a billing account.
- Not proof that address, service size, or utility provider fields are verified.

### 2. Buildings

Purpose:

Buildings represent physical structures that affect residential energy planning, including the main home, detached garages, workshops, ADUs, barns, and other energy-relevant structures.

Canonical Records:

- building id
- premise/twin linkage
- building name
- building type
- approximate distance from main service when recorded
- building notes
- building data origin
- building provenance summary

Dependencies:

- Loads may attach to buildings.
- Panels may attach to buildings.
- Equipment locations may attach to buildings.
- Pathways may connect buildings.
- Designs, scenarios, takeoffs, contractor views, and advisor outputs may depend on building records.

Ownership:

- Primary: Twin Agent
- Supporting: Backend Agent, Frontend Agent

Non-Goals:

- Not a full building information model.
- Not a permit record.
- Not a structural engineering model.
- Not proof of measured distances unless source-linked and verified.
- Not a substitute for field validation.

### 3. Electrical Infrastructure

Purpose:

Electrical Infrastructure represents panels, service context, distribution assumptions, backup panel context, panel roles, and electrical planning constraints.

Canonical Records:

- electrical panel records
- panel type
- amperage
- busbar rating when recorded
- breaker spaces
- indoor/outdoor posture
- building linkage
- home/premise linkage
- service size where recorded
- electrical notes
- electrical data origin
- electrical provenance summary

Dependencies:

- Loads depend on electrical context for planning interpretation.
- Designs depend on panels and service context.
- Equipment assignments may depend on panel/service posture.
- Scenarios, takeoffs, advisor outputs, contractor views, engineer views, utility views, and AI views depend on electrical infrastructure.

Ownership:

- Primary: NEC / Electrical Logic Agent
- Supporting: Twin Agent, Backend Agent, QA / Testing Agent, Security / Audit / Provenance Agent

Non-Goals:

- Not NEC compliance.
- Not a load calculation authority.
- Not a stamped electrical design.
- Not AHJ approval.
- Not utility approval.
- Not busbar validation unless explicitly implemented and approved.
- Not transfer topology approval.
- Not final inverter, battery, generator, or service-upgrade design.

### 4. Loads

Purpose:

Loads represent energy uses, backup priorities, criticality, planning assumptions, and load behavior relevant to resilience, electrification, backup planning, design comparison, and feasibility signals.

Canonical Records:

- load id
- name
- category
- running watts
- surge watts when recorded
- estimated daily hours
- backup priority
- phase type
- building linkage
- premise/twin linkage
- load notes
- load data origin
- load provenance summary

Dependencies:

- Electrical Infrastructure uses load records as planning inputs.
- Designs and Scenarios depend on load priorities and assumptions.
- Advisor outputs, backup capability, battery/solar planning, takeoffs, contractor views, engineer views, and AI views depend on loads.

Ownership:

- Primary: Twin Agent
- Supporting: NEC / Electrical Logic Agent, Backend Agent, Security / Audit / Provenance Agent

Non-Goals:

- Not a verified circuit inventory by default.
- Not a professional load study.
- Not proof of measured runtime or demand.
- Not operational telemetry.
- Not permission to control or shed loads.
- Not final backup sizing authority.

### 5. Equipment

Purpose:

Equipment represents product identity, type, role, quantity, location, ecosystem, specification assumptions, documentation, and source provenance for residential energy equipment.

Canonical Records:

- equipment product records
- manufacturer
- model
- product type
- ecosystem
- product specs
- documentation links
- source documents
- design equipment assignments
- quantity
- role in system
- equipment location
- equipment notes
- equipment data origin
- equipment provenance summary

Dependencies:

- Designs depend on product and assignment records.
- Electrical Infrastructure, Compatibility, Scenarios, Takeoffs, Advisor outputs, Contractor views, Supplier views, Manufacturer views, and AI views depend on equipment records.

Ownership:

- Primary: Equipment Agent
- Supporting: Twin Agent, Backend Agent, Frontend Agent, Security / Audit / Provenance Agent

Non-Goals:

- Not manufacturer warranty authority.
- Not product certification authority.
- Not proof of availability.
- Not procurement approval.
- Not final compatibility approval.
- Not verified product truth without source provenance.
- Not operational device status unless an approved operational source exists.

### 6. Designs

Purpose:

Designs represent current or proposed system architectures, design intent, status, equipment composition, design goals, and planning posture.

Canonical Records:

- design id
- premise/twin linkage
- design name
- design goal
- architecture type
- design status
- assigned design equipment
- design notes
- design data origin
- design provenance summary

Dependencies:

- Designs depend on Premise, Buildings, Electrical Infrastructure, Loads, Equipment, Pathways, Provenance, and Permissions.
- Scenarios, Takeoffs, Advisor outputs, Contractor views, Engineer views, Utility views, and AI views depend on design records.

Ownership:

- Primary: Twin Agent
- Supporting: Product Orchestrator, Backend Agent, Equipment Agent, NEC / Electrical Logic Agent

Non-Goals:

- Not a final electrical design.
- Not an installation plan.
- Not a permit package.
- Not an engineering stamp.
- Not a contractor bid.
- Not utility approval.
- Not operational dispatch authority.

### 7. Pathways

Purpose:

Pathways represent physical or logical routing assumptions between buildings, panels, equipment, and future upgrades. They capture distance, routing type, difficulty, visibility, confidence, and planning-stage pathway assumptions.

Canonical Records:

- pathway id
- premise/twin linkage
- optional design linkage
- pathway name
- description
- lifecycle stage
- source location
- destination location
- estimated distance
- route type
- route difficulty
- visibility level
- confidence level
- pathway notes
- pathway data origin
- pathway provenance summary

Dependencies:

- Designs may depend on pathways.
- Scenarios may compare pathway implications.
- Takeoffs may use pathway assumptions.
- Advisor outputs, install complexity, contractor views, supplier views, and AI views may depend on pathways.

Ownership:

- Primary: Twin Agent
- Supporting: Takeoff / Estimating Agent, Backend Agent, Frontend Agent, Security / Audit / Provenance Agent

Non-Goals:

- Not a surveyed route.
- Not trenching approval.
- Not conduit design.
- Not field-verified distance unless explicitly sourced.
- Not permit approval.
- Not final construction scope.

### 8. Scenarios

Purpose:

Scenarios represent possible planning futures, tradeoffs, statuses, linked designs, costs/scores when labeled, warnings, and planning history without treating every option as complete, verified, approved, or final.

Canonical Records:

- scenario id
- premise/twin linkage
- scenario name
- description
- linked design id
- scenario notes
- placeholder cost fields when explicitly labeled
- placeholder score fields when explicitly labeled
- live scenario state
- scenario revision records
- scenario data origin
- scenario provenance summary

Dependencies:

- Scenarios depend on Premise, Designs, Equipment, Loads, Pathways, Provenance, and Derived Intelligence.
- Scenario comparisons, homeowner views, contractor planning context, AI views, and historical lineage depend on scenario records.

Ownership:

- Primary: Product Orchestrator
- Supporting: Twin Agent, Backend Agent, Frontend Agent, Security / Audit / Provenance Agent

Non-Goals:

- Not a bid.
- Not a proposal authority.
- Not a financial guarantee.
- Not a permit package.
- Not a utility application.
- Not a final selected design unless separately recorded.
- Not procurement-ready pricing.

### 9. Permissions

Purpose:

Permissions represent who may see, use, export, or act on parts of the Residential Energy Twin, for which audience, purpose, scope, duration, and revocation state.

Canonical Records:

- PermissionGrant
- PermissionScope
- PermissionedView
- ConsentArtifact
- RevocationState
- permission audit references
- permission provenance summary

Dependencies:

- All external and role-specific views depend on Permissions.
- Provenance depends on permission events for lineage.
- Contractor, Engineer, Utility, Aggregator, Supplier, Manufacturer, AI, and future application access depends on permission state.
- Permissions depend on Premise/twin identity and homeowner ownership.

Ownership:

- Primary: Permission / Consent Agent
- Supporting: Security / Audit / Provenance Agent, Backend Agent, Frontend Agent, Product Orchestrator

Non-Goals:

- Not equivalent to account role.
- Not equivalent to subscription status.
- Not a generic checkbox.
- Not separate from the twin.
- Not operational-control authority unless explicitly authorized under a future approved operational model.
- Not permission to infer, resell, or reuse data outside the granted scope.

### 10. Provenance

Purpose:

Provenance represents where information came from, how it was derived, how confident the system should be, what authority layer applies, what assumptions were used, and what remains unknown.

Canonical Records:

- SourceDocument
- DataProvenance
- RuleProvenance
- ProvenanceSummary
- trust state
- confidence level
- verification status
- authority layer
- data classification
- lineage references

Dependencies:

- Every canonical domain depends on Provenance for authority.
- Every derived output depends on Provenance for inspectability.
- Permissions depend on Provenance for auditability.
- Views depend on Provenance to communicate trust and limits.

Ownership:

- Primary: Security / Audit / Provenance Agent
- Supporting: Twin Agent, Equipment Agent, Backend Agent, Documentation Agent, QA / Testing Agent

Non-Goals:

- Not proof of correctness by itself.
- Not access control by itself.
- Not a replacement for professional review.
- Not a replacement for utility approval.
- Not optional for authority-bearing facts.
- Not generated prose without source linkage.

### 11. Utility Relationships

Purpose:

Utility Relationships represent narrow, permissioned utility/service context relevant to the premise and potential future grid-facing workflows.

Canonical Records:

- utility provider
- service context
- service territory when known
- meter context when permissioned and sourced
- interconnection context when permissioned and sourced
- program context when permissioned and sourced
- utility source documents
- utility provenance summary
- permission scope for utility-facing visibility

Dependencies:

- Premise anchors Utility Relationships.
- Electrical Infrastructure and Designs may depend on utility/service context.
- Utility Views depend on Utility Relationships, Permissions, and Provenance.
- Aggregator views may depend on utility/program context when permissioned.

Ownership:

- Primary: Utility / Rate Agent
- Supporting: Permission / Consent Agent, Twin Agent, Backend Agent, Security / Audit / Provenance Agent

Non-Goals:

- Not a utility account system.
- Not tariff authority.
- Not rate calculation authority.
- Not interconnection approval.
- Not program eligibility approval.
- Not utility submission authority.
- Not operational dispatch authority.
- Not unrestricted utility account access.
- Not raw utility data storage unless explicitly authorized and governed.

## Canonical Data Rules

### Canonical

Definition:

Canonical data is durable twin data recorded inside a twin domain as part of the homeowner-governed residential energy record.

Authority Level:

Canonical data is authoritative as a recorded planning record, but not automatically verified truth. Its practical authority depends on provenance, source type, confidence, verification status, data origin, and scope.

Persistence Expectations:

Canonical data should persist in the twin until updated, archived, superseded, or removed through an approved lifecycle. Canonical records should have stable identity, domain linkage, data origin, timestamps, provenance references, and permission classification.

### Derived

Definition:

Derived data is produced from canonical data through explicit rules, calculations, comparisons, summaries, deterministic services, or advisory processes.

Authority Level:

Derived data is downstream of its inputs. It may explain, compare, estimate, rank, or recommend, but it does not create canonical facts by itself.

Persistence Expectations:

Derived data may be transient or persisted as a versioned artifact depending on approved contract design. If persisted, it must include source inputs, rule keys, generated timestamp, confidence, missing inputs, assumptions, limitations, and provenance summary.

### Inferred

Definition:

Inferred data is a plausible conclusion drawn from incomplete evidence, patterns, declarations, monitoring signals, or indirect source material.

Authority Level:

Inferred data has lower authority than documented or verified data. It can support planning only when clearly labeled as inferred.

Persistence Expectations:

Inferred data may persist only when labeled with source basis, confidence, assumptions, and limitations. It must remain distinguishable from declared, documented, verified, and canonical structured records.

### Unknown

Definition:

Unknown data is information the system does not have or cannot responsibly determine from available sources.

Authority Level:

Unknown has no factual authority, but it has planning value because it identifies gaps that require homeowner input, documentation, field verification, professional review, or utility confirmation.

Persistence Expectations:

Unknowns should remain visible in domain records, derived outputs, and views. Unknown status should not be hidden by generated explanations or placeholder assumptions.

## Permission Domain

Permission is a first-class domain inside the Residential Energy Twin.

Permission does not exist outside the twin. Account role, subscription status, application session, or endpoint access is not equivalent to permission.

### PermissionGrant

A `PermissionGrant` records an explicit authorization by the homeowner or authorized grantor.

Required concepts:

- grant identity
- twin identity
- grantor
- audience
- subject or receiving party
- purpose
- scope
- view contract
- duration
- status
- revocation state
- provenance/audit reference

### PermissionScope

A `PermissionScope` defines what the grant covers.

Scope may include:

- domains
- fields
- documents
- source summaries
- derived outputs
- scenario history
- exports
- allowed actions
- excluded data
- time limits
- purpose limits

### PermissionedView

A `PermissionedView` is the explicit data contract exposed under a permission grant.

Permissioned views are not broad endpoint filters. They are stable, named contracts that define what an audience can see and what authority the view carries.

### ConsentArtifact

A `ConsentArtifact` records what the homeowner understood and authorized.

It may include:

- consent text or version
- audience
- purpose
- scope summary
- effective date
- expiration date
- source of consent
- related permission grant
- revocation terms

### RevocationState

`RevocationState` records whether a permission grant is active, expired, revoked, superseded, or otherwise inactive.

Revocation stops future access where practical. Historical access records may remain for audit, safety, completed-work lineage, or legal retention where appropriate.

### Audience Types

Homeowner:

Sees the broadest owner view of the twin, including planning facts, assumptions, missing data, scenarios, provenance, permissions, and advisory explanations.

Contractor:

Sees scoped project context needed for scoping, site walks, estimating, equipment review, pathway assumptions, missing information, and project coordination.

Engineer:

Sees organized factual inputs, assumptions, missing data, equipment information, electrical context, and provenance needed for professional review. The twin does not replace engineering authority.

Utility:

Sees minimized, source-linked, permissioned service-relevant and grid-relevant facts. The twin does not replace utility authority.

Aggregator:

Sees permissioned capability, constraints, availability, and participation context relevant to authorized programs. The twin does not imply dispatch authority by default.

Supplier:

Sees scoped equipment, product, availability, compatibility, and documentation context needed for supplier workflows when authorized.

Manufacturer:

Sees product-relevant, permissioned installation/support context when authorized. Manufacturer facts require provenance and do not become whole-home authority.

AI Agent:

Sees permissioned, source-linked, bounded context needed to explain, organize, compare, and coordinate. AI does not own the twin and does not create canonical truth without an authorized source path.

## Provenance Domain

Provenance is first-class. It governs trust, lineage, confidence, authority, and inspectability.

### Twin-Level Provenance

Twin-level provenance summarizes the overall trust posture of the Residential Energy Twin.

It should identify:

- source coverage by domain
- missing provenance areas
- stale or unverified domains
- demo/placeholder/inferred content
- verified content where available
- revision state
- authority limitations

### Domain-Level Provenance

Domain-level provenance summarizes source coverage for a specific twin domain.

Examples:

- premise provenance
- building provenance
- panel provenance
- load provenance
- equipment provenance
- pathway provenance
- scenario provenance
- utility relationship provenance

### Field-Level Provenance

Field-level provenance links individual important fields to source documents, user declarations, imports, calculations, verified updates, or internal rules.

Field-level provenance is required for authority-bearing claims and should remain visibly incomplete when coverage is partial.

### Derived-Output Provenance

Derived-output provenance identifies the lineage of generated intelligence.

It should include:

- source canonical records
- rule keys
- source documents where applicable
- generated timestamp
- derivation type
- confidence level
- missing inputs
- assumptions
- limitations
- authority layer
- data classification

### Revision Provenance

Revision provenance records what changed, when it changed, what source state was used, what generated outputs were captured, and whether the revision is compact, replayable, or full-fidelity.

Scenario revisions and future twin revisions should distinguish historical lineage from current live state.

### Authority Hierarchy

Authority hierarchy, highest to lowest:

1. Verified Truth: trusted confirmation within a defined scope, such as inspection, field validation, approved interconnection, or responsible professional confirmation.
2. Documented Truth: source-backed artifacts such as equipment labels, photos, permits, drawings, manufacturer documents, bills, or submitted records.
3. Declared Truth: homeowner or stakeholder-provided facts, goals, priorities, plans, and constraints.
4. Structured Planning Record: persisted canonical twin record that may be declared, imported, demo-seeded, verified, stale, or wrong depending on provenance.
5. Derived Truth: deterministic or calculated output based on source records and rules.
6. Inferred Truth: plausible conclusion from incomplete or indirect evidence.
7. Advisory Explanation: generated or composed explanation that helps interpretation but does not create facts.
8. Unknown: explicitly missing or unavailable information.
9. Placeholder/Demo: non-authoritative continuity or demonstration data.

Structured facts outrank generated text. Verified, source-linked facts outrank unsupported inference. Unknowns are safer than unmarked guesses.

## Utility Relationship Domain

The Utility Relationship domain is intentionally narrow in v1.

It may include:

### Provider

- utility provider name
- provider identifier where source-linked
- service organization context when relevant

### Service Context

- recorded service size
- service type where known
- meter/service context where permissioned and sourced
- service notes relevant to planning

### Territory

- service territory when known and sourced
- jurisdictional or region context only when relevant to utility-facing workflows
- territory provenance and confidence

### Interconnection Context

- interconnection status when permissioned and sourced
- application or approval references when available
- system-relevant interconnection facts
- source documents
- limitations and authority boundaries

### What Does Not Belong Here

The Utility Relationship domain does not include:

- unrestricted raw utility account access
- financial account credentials
- full billing history by default
- tariff authority without sourced rate model approval
- incentive eligibility authority
- savings guarantees
- utility approval claims
- interconnection approval claims without utility source evidence
- operational dispatch commands
- DERMS control authority
- aggregator enrollment authority
- legal conclusions
- private household data unrelated to energy planning
- broad utility-facing exports without permission

## View Contract Philosophy

Same Twin. Different Views.

Every application and external consumer should operate against the same Residential Energy Twin through a scoped view. The view changes by audience, purpose, permission, provenance, and authority. The underlying twin remains the canonical record.

Views do not become canonical. Views expose selected twin domains and derived outputs under explicit boundaries.

### Consumer View

Audience:

Homeowner or owner-authorized consumer planning experience.

Purpose:

Support homeowner understanding, planning, comparison, missing-data review, permission management, and provenance visibility.

Boundary:

May expose the broadest planning workspace, but still distinguishes canonical facts, derived estimates, inferred assumptions, unknowns, and advisory explanations.

### Contractor View

Audience:

Contractor or installer.

Purpose:

Support scoping, site walks, early estimating, equipment review, route review, missing-information discovery, and project coordination.

Boundary:

Should include only project-relevant site/design/load/pathway/equipment context. It should exclude unrelated homeowner notes, broad account data, utility submission claims, operational-control data, and private context outside the permission scope.

### Engineer View

Audience:

Engineer or licensed professional reviewer.

Purpose:

Support review of organized factual inputs, assumptions, equipment information, panel/load context, missing data, and provenance.

Boundary:

Should separate recorded facts from assumptions and derived planning outputs. It must not imply the twin replaces engineering judgment or stamped approval.

### Utility View

Audience:

Utility or authorized utility-facing workflow.

Purpose:

Support minimized, permissioned, source-linked visibility into service-relevant or grid-relevant facts.

Boundary:

Should exclude broad homeowner planning notes, AI advisory text, household-level appliance detail unless required and authorized, unrelated product specs, and operational dispatch claims.

### Supplier View

Audience:

Supplier or procurement-support participant.

Purpose:

Support scoped equipment packaging, product availability, substitution context, documentation needs, and compatibility review when authorized.

Boundary:

Should expose product/design need context, not the full home record or unrelated homeowner/private data.

### Manufacturer View

Audience:

Manufacturer or product support participant.

Purpose:

Support product documentation, compatibility support, warranty-relevant context, and installation support when authorized.

Boundary:

Should expose product-relevant context only. Manufacturer systems do not become the whole-home source of truth.

### AI View

Audience:

AI agent or AI-assisted workflow.

Purpose:

Support explanation, comparison, organization, summarization, and coordination using structured, source-linked, bounded context.

Boundary:

Should minimize raw object exposure, preserve provenance, show uncertainty, include limitations, and provide no canonical write authority unless a future approved workflow explicitly permits structured source-backed promotion.

AI may explain. AI may not create canonical facts.

## Canonical vs Derived Matrix

| Domain | Canonical Data | Derived Data | Inferred Data | Unknowns |
| --- | --- | --- | --- | --- |
| Premise | Home identity, address, owner linkage, service fields, utility provider field | Premise completeness, site-context summaries | Region or service assumptions from partial address/provider data | Missing address detail, unverified service size, unknown provider |
| Buildings | Building records, type, distance assumptions, notes | Building planning summaries, route implications | Structure use or distance interpretation from notes | Unknown structure details, unverified distances |
| Electrical Infrastructure | Panel records, amperage, spaces, service context, panel notes | Completeness, panel/service posture, backup-architecture posture | Likely service constraints or upgrade posture | Unknown busbar, unknown transfer topology, missing circuit validation |
| Loads | Load records, watts, estimated hours, backup priority, phase | Load summaries, backup grouping, battery planning inputs | Likely outage behavior or usage assumptions | Unknown true runtime, unknown measured load, missing circuit mapping |
| Equipment | Product records, specs, assignments, locations, roles, documentation links | Compatibility signals, equipment mix summaries, takeoff lines | Product capability interpretation from specs/notes | Unknown product verification, unavailable specs, missing installed status |
| Designs | Design goal, architecture type, status, equipment composition | Design completeness, advisor recommendation, architecture-fit outputs | Likely architecture direction | Unknown final design, missing engineering review |
| Pathways | Route assumptions, distance, difficulty, visibility, confidence | Install complexity, pathway comparison, takeoff assumptions | Likely trench/conduit implications | Unknown measured route, unknown constructability |
| Scenarios | Scenario records, linked designs, notes, compact revisions | Scenario comparison, ranking, warnings, drift summaries | Likely scenario tradeoffs | Unknown actual cost, unknown selected path, missing replay data |
| Permissions | Permission grants, scopes, views, consent artifacts, revocation state | Permission readiness summaries, access summaries | Likely audience need | Unknown consent status where no grant exists |
| Provenance | Source documents, data provenance, rule provenance, summaries | Trust summaries, authority rollups, provenance coverage scores | Source quality assumptions | Missing source, stale source, unverified field |
| Utility Relationships | Provider, service context, territory, interconnection context when sourced | Utility-facing readiness summaries | Likely territory/program relevance | Unknown tariff, unknown interconnection state, unknown utility approval |
| Derived Views | None as canonical source facts | Advisor outputs, AI grounding, generated takeoffs, comparison views | Advisory interpretations | Missing inputs, uncomputed outputs, unpersisted snapshots |

## Twin Boundary Test

For any future feature, ask:

If this application disappeared tomorrow, would this information still belong to the Residential Energy Twin?

If yes:

The information belongs in a Twin Domain when it describes durable home energy truth, homeowner-governed context, permissions, provenance, planning history, asset relationships, source-linked evidence, verified updates, declared intent, or known unknowns.

If no:

The information belongs in an Application Domain when it is temporary UI state, presentation copy, workflow-specific state, generated explanation, session memory, consumer-specific formatting, local interaction state, or an application-only artifact.

Examples:

- A verified panel photo belongs in the twin.
- A contractor-safe summary view belongs to an application/view contract.
- The source record behind a contractor note belongs in the twin if permissioned.
- A sorted UI table state does not belong in the twin.
- A scenario revision belongs in the twin.
- An unpersisted advisor card layout does not belong in the twin.
- A permission grant belongs in the twin.
- A broad API response shape does not become the twin.

## Architectural Constraints

Applications cannot become sources of truth.

Planner, contractor, engineer, utility, supplier, manufacturer, aggregator, homeowner, and AI applications consume the Residential Energy Twin. They may enrich it only through approved structured workflows with provenance and permission boundaries.

Permissions cannot exist outside the twin.

Permission is not merely an account role, endpoint filter, subscription state, UI checkbox, or external policy. Permission is a first-class twin domain governing access to twin views.

Provenance is required for authority.

A fact without provenance may still be recorded, but its authority remains limited. Product/spec data, assumptions, derived outputs, recommendations, estimates, and utility-facing facts require visible lineage.

Derived intelligence cannot become canonical.

Completeness scores, compatibility issues, advisor recommendations, scenario rankings, generated takeoffs, battery/solar planning ranges, AI context, and reasoning graphs are downstream projections. They do not create canonical facts unless promoted through an approved source-backed workflow.

AI cannot create canonical facts.

AI may explain, summarize, compare, organize, and coordinate. AI may not create product truth, home facts, engineering approval, code compliance, utility approval, financial guarantees, operational authorization, or permission grants by inference or prose.

Structured facts outrank generated content.

Generated text must remain subordinate to structured records, source documents, provenance, permission grants, professional authority, and utility authority.

Unknowns must remain visible.

Missing information must not be hidden by inferred defaults, placeholder values, confident prose, or broad recommendations.

Placeholder and demo data must remain labeled.

Demo seed data and placeholder values may support continuity and product development, but they are not factual authority.

Existing application contracts must not be silently reclassified.

Existing broad planner APIs are compatibility-sensitive application contracts. Future scoped views should be additive, explicit, and permission-bound.

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, project direction, schema, API contract, or enforcement behavior:

- Creating or modifying the canonical `ResidentialEnergyTwin` data model.
- Deciding whether `twin_id` is a new persistent identifier or whether `home_id` temporarily acts as twin identity.
- Changing schema, migrations, persistence contracts, or canonical data models.
- Defining required fields for any twin domain.
- Promoting any derived output into canonical persisted data.
- Implementing permission grants, consent artifacts, revocation semantics, or homeowner authorization flows.
- Implementing authentication, authorization, RBAC, ABAC, tenant isolation, export authorization, or subscription enforcement.
- Creating contractor, engineer, utility, supplier, manufacturer, aggregator, or AI permissioned views.
- Changing existing compatibility-sensitive `/api/*` contracts.
- Defining provenance policy, audit policy, field-level provenance requirements, or trust-state semantics.
- Defining utility relationship authority, service territory authority, tariff authority, interconnection status authority, or utility-facing export behavior.
- Implementing NEC, electrical-code, load-calculation, permitting, AHJ, or stamped-engineering logic.
- Implementing pricing, savings, payback, incentive, estimate, procurement, or bid authority.
- Implementing operational control, dispatch, DERMS, aggregator enrollment, device-control, or availability semantics.
- Changing trust language that could imply certainty, compliance, approval, savings, safety, authorization, or professional review.
- Refactoring architecture boundaries, service boundaries, repository structure, or integration strategy around the twin.
- Treating this contract as approved implementation direction without Matt's explicit approval.
