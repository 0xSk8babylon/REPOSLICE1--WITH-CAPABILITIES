# Residential Energy Twin Ecosystem Participant Boundary Matrix

Status: Residential Energy Twin doctrine consolidation document
Date: 2026-06-02
Scope: documentation and architecture governance only
Implementation status: no schema, migration, runtime behavior, API, exchange mechanism, export mechanism, protocol, standard, ownership-transfer workflow, permission enforcement, auth, RBAC, ABAC, utility API, DERMS, dispatch, operational-control behavior, or canonical runtime implementation is approved or implied

## Purpose

The Ecosystem Participant Boundary Matrix defines participant-purpose boundaries before any Exchange Domain work.

It consolidates existing Residential Energy Twin doctrine for homeowners, contractors, utilities, real estate, insurance, finance, manufacturers, and aggregators. It clarifies what each participant may contribute, what each participant may consume, the minimum necessary Twin domains for the purpose, and the trust, provenance, permission, continuity, and interoperability constraints that must remain attached.

This document is not a new Residential Energy Twin domain. It is a boundary matrix for applying existing Twin doctrine consistently across ecosystem participants.

It does not define exchange mechanisms, ownership transfer, APIs, schemas, protocols, standards, exports, integrations, runtime enforcement, view implementation, utility submissions, operational control, or implementation scope.

## Core Principle

Twin neutrality comes first.

The Residential Energy Twin remains the trusted, homeowner-governed, source-linked record. Ecosystem participants may contribute information or consume permissioned views for a defined purpose, but no participant's industry role changes Twin truth, grants authority, weakens provenance, bypasses permission, erases continuity, expands safety claims, or creates operational control.

## Boundary Rules

Every participant-purpose boundary should preserve:

- explicit purpose
- minimum necessary Twin domains
- homeowner permission basis when external access is involved
- provenance for authority-bearing facts
- continuity and historical/current state distinctions
- interoperability semantics for consumer interpretation
- trust-zone, authority-layer, and limitation labels
- prohibited claims and prohibited authority assumptions

Every participant-purpose boundary must avoid:

- hidden exchange semantics
- implied ownership transfer
- API, schema, protocol, or runtime implementation design
- broad access where a minimized view is sufficient
- unsupported compliance, safety, utility, financial, warranty, procurement, or operational claims
- participant-specific interpretation being treated as canonical Twin truth

## Participant Matrix

| Participant | Purpose | Information contributed | Information consumed | Minimum necessary domains | Permission requirements | Provenance requirements | Continuity requirements | Interoperability requirements | Prohibited claims | Prohibited authority assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Homeowners | Owner-governed planning, review, correction, permission management, and lifecycle understanding. | Home declarations, goals, missing-data corrections, source documents, consent decisions, revocations, planning choices. | Broad owner view of recorded facts, derived planning intelligence, advisory explanations, provenance summaries, missing-data posture, continuity history, and permission status when approved. | Premise, Buildings, Electrical Infrastructure, Loads, Equipment, Designs, Pathways, Scenarios, Safety, Continuity, Permissions, Provenance, Interoperability, Views. | Homeowner authority for own Twin context; external sharing still requires explicit grants, purpose, duration, exclusions, and revocation handling when approved. | Source, data origin, confidence, verification posture, assumptions, missing inputs, conflicts, and limitations should remain visible. | Must preserve historical/current separation, supersession, stale data, revoked permissions, scenario history, and carried-forward facts. | Must support clear understanding of canonical, derived, advisory, historical, and future operational distinctions. | Do not claim engineering approval, code compliance, permit approval, utility approval, tariff authority, incentive eligibility, savings, bid, procurement approval, safety certification, or operational readiness. | Owner account relationship is not permission enforcement, title ownership, legal identity proof, export authority, utility authority, or device-control authority. |
| Contractors | Scoping, site-walk preparation, route review, equipment coordination, installation planning input, and rough planning context. | Site observations, project notes, photos or documents when approved, equipment observations, pathway assumptions, contractor-reviewed context within scope. | Minimized site, building, panel, load, equipment, pathway, design, safety context, missing data, and selected source/provenance summaries relevant to the project. | Premise, Buildings, Electrical Infrastructure, Loads, Equipment, Designs, Pathways, Safety, Continuity, Provenance, Interoperability, Views. | Purpose-bound contractor view authorized by homeowner; access should be scoped by project, domains, fields, source documents, duration, exclusions, and revocation expectations. | Contractor-supplied facts need actor/source, date, affected fields, confidence, verification scope, missing inputs, assumptions, and limitation text. | Contractor involvement and superseded assumptions should remain historically traceable without implying ongoing access or authority. | Contractor interpretation should remain scoping context and must preserve planning-only, historical, and verification labels. | Do not claim bid authority, warranty authority, procurement approval, engineering approval, permit approval, code compliance, safety approval, field verification, utility approval, or operational readiness. | Contractor relationship is not permission, legal authority, ongoing access, professional engineering approval, AHJ approval, utility authority, or operational control. |
| Utilities | Source-linked service, interconnection, export, program, or utility-reviewed context when approved and permissioned. | Utility documents, provider/service context, interconnection context, export limits, program context, utility-reviewed or utility-limited records when sourced. | Minimized service/site identity, selected equipment/inverter/storage/generator/PV facts, export-capability context, aggregate load context when approved, provenance and limitation summaries. | Premise, Electrical Infrastructure, Equipment, Safety, Utility Relationships, Permissions, Provenance, Continuity, Interoperability, Views. | Explicit utility-safe permission with audience, purpose, duration, allowed domains/fields, source-document limits, revocation expectations, and audit expectations when implemented. | Utility-source claims require source document identity, effective dates where available, field/domain coverage, verification scope, conflicts, and limits. | Utility provider, service, interconnection, export, and program history should remain distinguishable from current recorded state. | Utility interpretation must distinguish equipment capability from utility approval, export permission, tariff authority, program eligibility, and operational control. | Do not claim tariff authority, incentive eligibility, interconnection approval, export permission, utility submission authority, program enrollment, utility approval, DERMS, dispatch, demand response, VPP participation, or grid-service participation. | Utility relationship does not grant account authority, unrestricted access, homeowner consent, operational availability, telemetry authority, credential access, or device-control authority. |
| Real Estate | Infrastructure awareness, lifecycle context, and transfer-adjacent understanding when approved. | Property-related documents or seller/owner-supplied infrastructure context when approved; historical record updates within source-backed limits. | Minimized continuity, infrastructure, safety, equipment, and provenance summaries relevant to property understanding. | Premise, Buildings, Electrical Infrastructure, Equipment, Safety, Continuity, Provenance, Interoperability, Views. | Purpose-specific permission from authorized homeowner or future approved transfer workflow; access should exclude unrelated private homeowner data and broad source documents unless needed. | Real-estate-facing facts need source, date, current/historical label, confidence, missing inputs, assumptions, and limitation text. | Must preserve ownership continuity boundaries, prior/current context, superseded equipment, safety history, and stale or unknown records without implying current truth. | Real-estate interpretation should treat the Twin as infrastructure context, not title, legal disclosure, appraisal, or transfer authority. | Do not claim legal title, ownership transfer, deed status, disclosure compliance, appraisal value, sale condition, safety certification, code compliance, utility approval, warranty, or operational readiness. | Real-estate participation does not create ownership rights, transfer rights, access rights, title authority, legal disclosure authority, compliance authority, or control of the Twin. |
| Insurance | Infrastructure and safety-context understanding for future insurance-related review when approved. | Insurance-related documents, inspection artifacts, claims-adjacent records, or risk-context notes when approved and source-backed. | Minimized safety, equipment, infrastructure, continuity, provenance, and limitation summaries relevant to the approved insurance purpose. | Premise, Electrical Infrastructure, Equipment, Safety, Continuity, Provenance, Interoperability, Views. | Narrow purpose-bound permission; should exclude unrelated household/private context, broad planning notes, utility credentials, and source documents not needed for the purpose. | Insurance-facing records require source basis, verification scope, confidence, missing data, assumptions, historical/current state, and explicit limits. | Must preserve safety and equipment history, supersession, replacements, stale records, and verification-status changes without presenting history as current state. | Insurance interpretation should preserve safety context without converting it into insurability, underwriting, premium, or claim authority. | Do not claim underwriting approval, insurability, premium impact, claim approval, safety certification, compliance approval, risk-score authority, field verification, or operational readiness. | Insurance participant status does not grant authority to certify safety, determine coverage, access unrelated homeowner data, inspect without permission, or control equipment. |
| Finance | Project, asset, and lifecycle context for future financing-related review when approved. | Financing documents, project-cost artifacts, lender-required records, payment or contract references when approved and source-backed. | Minimized project, equipment, design, continuity, provenance, and limitation summaries relevant to the approved finance purpose. | Equipment, Designs, Pathways, Scenarios, Continuity, Provenance, Interoperability, Views, and limited Premise context when needed. | Purpose-bound permission; access should be scoped to finance purpose, excluded private data, and source-document visibility should be narrow. | Finance-facing facts require source, date, confidence, estimate boundary, missing inputs, assumptions, limitations, and whether amounts are placeholder, rough, quoted, contracted, or historical. | Must distinguish current recorded equipment/project state from proposed, contractual, historical, replaced, or revoked context. | Finance interpretation should treat Twin records as planning or source-linked context, not credit, valuation, savings, lien, or ownership authority. | Do not claim credit approval, loan approval, valuation, appraisal, savings guarantee, payback guarantee, lien authority, title authority, procurement approval, bid authority, or financial advice. | Finance participant status does not create ownership rights, transfer rights, contractual rights, payment authority, collateral authority, warranty authority, or control rights. |
| Manufacturers | Product support, documentation, compatibility review, substitution discussion, and warranty-adjacent context when authorized. | Product specs, manuals, compatibility notes, support records, product-document updates, model metadata when sourced. | Scoped product references, equipment assignments, quantities, roles, design-need context, compatibility assumptions, and product provenance summaries. | Equipment, Designs, Pathways, Provenance, Interoperability, Views, and limited Safety context when product safety interpretation is necessary. | Product-support permission should be scoped to product/domain fields and exclude unrelated home, utility, household, financial, and private context. | Manufacturer facts require source document identity, model/version, source date, spec coverage, confidence, missing fields, conflicts, and limitation text. | Product substitutions, superseded specs, obsolete equipment, and support history should remain traceable without overwriting installed/current state. | Manufacturer interpretation should distinguish product capability from installed capability, verified compatibility, warranty approval, procurement approval, or operational status. | Do not claim guaranteed compatibility, availability, warranty approval, procurement approval, performance guarantee, installed status, safety approval, utility approval, or operational readiness. | Manufacturer role does not grant access to the full Twin, warranty authority by default, procurement authority, field verification, device status authority, telemetry authority, or device-control authority. |
| Aggregators | Future grid-program or aggregation-readiness context when approved. | Program context, participation constraints, capability requirements, or source-backed enrollment-related context when future approvals exist. | Minimized, permissioned capability context, equipment/topology facts, constraints, availability context only when sourced, program context only when authorized, provenance and limitations. | Equipment, Safety, Utility Relationships, Permissions, Provenance, Continuity, Interoperability, Views, and future operational domains only after approval. | Explicit aggregator/grid-program permission; must be purpose-bound, revocable where practical, minimized, and separate from operational-control authorization. | Aggregator-facing facts need source-backed capability basis, lifecycle state, permission scope, confidence, missing inputs, assumptions, revision identity, and limitation text. | Participation history, revoked permissions, superseded capabilities, equipment replacement, and program context must remain traceable. | Aggregator interpretation must distinguish capability/readiness context from enrollment, availability, telemetry, dispatch, VPP, DERMS, or control authority. | Do not claim enrollment, dispatch authority, performance guarantee, availability guarantee, grid-service commitment, tariff/program eligibility, utility approval, telemetry authority, or operational control. | Aggregator relationship does not grant homeowner consent, utility authority, device credentials, telemetry authority, command authority, DERMS, dispatch, demand response, VPP participation, or operational control. |

## Doctrine Impact

This matrix strengthens existing doctrine by making participant-purpose boundaries explicit before any future Exchange Domain work.

It does not add a new Residential Energy Twin domain. It routes participant interpretation through existing doctrine:

- Residential Energy Twin Contract for canonical truth and domain ownership
- Permission Placement for homeowner authorization and revocation posture
- Provenance Placement for source lineage, confidence, assumptions, conflicts, and limitations
- View Contracts for minimized audience-specific projections
- Interoperability Domain for shared semantic understanding
- Safety Domain for safety context without safety authority
- Continuity Domain for lifecycle history without ownership, title, or transfer authority
- Trust Zones for recorded, derived, advisory, historical, and future operational boundaries

The matrix makes Exchange Domain prerequisites clearer: before any exchange doctrine, the repository should know the participant, purpose, minimum necessary domains, required permission basis, provenance requirements, continuity requirements, interoperability semantics, prohibited claims, and prohibited authority assumptions.

## Overlap Analysis

### Permissions And Views

The matrix depends on Permission Placement and View Contracts. Permission defines who may receive information and why. Views define minimized projections. The matrix does not grant permission or define runtime views.

### Interoperability And Exchange

The matrix depends on interoperability semantics so participants can understand the same Twin. It does not define how information moves, how packages are structured, what APIs exist, what schemas exist, or what protocols exist.

### Continuity And Ownership Transfer

The matrix uses continuity context for real estate, finance, insurance, contractors, utilities, manufacturers, and aggregators. It does not establish ownership transfer, legal title, deed status, identity proof, transfer rights, or ongoing access.

### Safety And Insurance / Utility / Aggregator Context

The matrix allows safety context to be minimized and permissioned for participant purposes. It does not create safety certification, inspection approval, field verification, utility approval, operational readiness, or emergency-response authority.

### Provenance And Trust

The matrix requires provenance to travel with authority-bearing facts and participant-facing interpretations. Provenance and trust posture do not prove correctness, grant access, resolve conflicts by themselves, or create stronger authority than the source supports.

## Architectural Impact Assessment

This is a doctrine-only consolidation milestone.

No runtime code, schemas, migrations, APIs, database models, permission enforcement, auth, RBAC, ABAC, protocols, exchange mechanisms, ownership-transfer workflows, utility APIs, DERMS, dispatch, operational control, exports, integrations, or canonical runtime Twin models are approved or implied.

The architecture impact is limited to clarifying participant-purpose boundaries before future Exchange Domain planning.

## Risks

- Real estate boundaries can drift into title, transfer, disclosure, appraisal, or legal authority if future documents are not explicit.
- Insurance boundaries can drift into underwriting, insurability, risk scoring, claim authority, or safety certification.
- Finance boundaries can drift into credit, valuation, savings, lien, ownership, or contractual authority.
- Utility and aggregator boundaries can drift into utility approval, export permission, telemetry, DERMS, dispatch, VPP, demand response, or operational control.
- Manufacturer boundaries can drift into warranty, procurement, compatibility guarantees, installed status, or operational device status.
- Exchange Domain work remains premature if participant-purpose boundaries are not treated as prerequisites.

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating runtime participant-boundary models, tables, fields, services, APIs, exports, integrations, packets, or UI workflows
- defining exchange mechanisms, schemas, protocols, standards, conformance rules, registries, networks, or external data packages
- defining ownership transfer, legal title, disclosure, appraisal, insurance, underwriting, finance, credit, lien, warranty, procurement, or contractual authority
- implementing permission enforcement, RBAC, ABAC, auth, tenant isolation, encryption, telemetry governance, audit policy, utility APIs, utility submissions, DERMS, dispatch, demand response, VPP, aggregator participation, or operational control
- treating any participant interpretation as proof of compliance, safety, utility approval, interconnection approval, eligibility, legal ownership, title transfer, financial guarantee, warranty authority, procurement approval, field verification, operational readiness, or device-control authority

## Sources / Provenance

- User-provided Residential Energy Twin Ecosystem Participant Boundary Matrix milestone, 2026-06-02
- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/product-vision.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/InteroperabilityDomain.md`
- `docs/architecture/ViewContracts.md`
- `docs/architecture/PermissionPlacement.md`
- `docs/architecture/ProvenancePlacement.md`
- `docs/architecture/ContinuityDomain.md`
- `docs/architecture/SafetyDomain.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/project-skills/doctrine-formalization/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `.codex/project-skills/continuity-governance/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

The Ecosystem Participant Boundary Matrix defines docs-only participant-purpose boundaries for homeowners, contractors, utilities, real estate, insurance, finance, manufacturers, and aggregators. It consolidates existing Residential Energy Twin doctrine around minimum necessary access, permissions, provenance, continuity, interoperability, prohibited claims, and prohibited authority assumptions before any Exchange Domain work. It does not create a new Twin domain and does not define exchange, ownership transfer, APIs, schemas, protocols, runtime behavior, utility control, or operational control.
