# Dependency Impact Propagation

Status: Phase 3 architecture planning document
Date: 2026-06-02
Scope: documentation and architecture governance only
Implementation status: no runtime code, schema change, API, service, calculation engine, AI agent, provider integration, product catalog, telemetry implementation, exchange mechanism, ownership-transfer workflow, utility API, DERMS, dispatch, operational-control, or authority-of-record replacement is approved or implied

## Purpose

Dependency Impact Propagation defines how changes to Residential Energy Twin facts should affect downstream derived outputs, advisory explanations, scenarios, views, provenance posture, confidence posture, safety context, continuity records, and participant-facing interpretations.

This is not a new Residential Energy Twin domain.

It is an architectural integrity and lifecycle behavior document for Phase 3 Twin Intelligence. It explains what should become stale, require recalculation, require re-grounding, require re-review, require re-labeling, or require additional provenance when an upstream Twin fact changes.

Dependency Impact Propagation is:

- derived/advisory lifecycle behavior over existing Twin domains
- a consistency rule for keeping downstream intelligence tied to current source facts
- a trust-boundary guardrail for stale recommendations, views, and scenario comparisons
- a provenance-preserving way to identify affected outputs after source facts change
- a planning-only doctrine layer for future implementation design

Dependency Impact Propagation is not:

- a new Twin domain
- a runtime invalidation engine
- an API contract
- a schema
- a graph database design
- an exchange mechanism
- an ownership-transfer workflow
- a permission enforcement model
- a safety approval workflow
- a utility submission or export mechanism
- DERMS, dispatch, telemetry, demand response, VPP participation, or operational control

## Architecture Summary

The Residential Energy Twin is source-linked and lifecycle-aware. Phase 3 intelligence depends on recorded Twin facts, topology relationships, lifecycle state, permissions, provenance, confidence, safety context, continuity history, and actor-specific view boundaries.

When an upstream fact changes, downstream outputs must not silently retain prior conclusions as if their basis still holds. A change may require:

- marking derived outputs stale
- recalculating deterministic outputs
- re-grounding provider-backed, product-backed, quote-backed, or source-backed assumptions
- re-reviewing contractor, engineer, utility, safety, financial, insurance, manufacturer, or aggregator interpretations
- updating provenance and confidence posture
- preserving continuity of what changed and what was affected
- revising participant-facing view limitations
- exposing missing data introduced by the change

The core rule:

> A downstream output is only as current, scoped, and authoritative as the upstream facts, provenance, permissions, lifecycle state, and grounding evidence it depends on.

If the dependency basis is changed, missing, stale, superseded, revoked, partial, conflicting, or outside the view scope, the downstream output should be recalculated, re-grounded, re-reviewed, downgraded, or labeled stale before it is treated as reliable planning context.

## Inputs From Existing Architecture

Dependency Impact Propagation consumes existing doctrine as constraints:

- `ResidentialEnergyTwinContractV1.md`: aggregate boundary, source-of-truth order, lifecycle states, permission/provenance placement expectations, utility and operational-control boundaries
- `TopologyLifecycleDomains.md`: current, sandbox, proposed, saved revision, future reviewed, verified, utility-facing, and operational topology separation
- `PermissionPlacement.md`: homeowner authorization, scope, duration, revocation, and view-contract attachment
- `ProvenancePlacement.md`: source, evidence, confidence, verification, lifecycle-transition, view/export, audit, and utility provenance placement
- `ViewContracts.md`: actor-specific, permission-filtered, provenance-preserving view expectations
- `SafetyDomain.md`: safety context, verification-status boundaries, energy-source, isolation, export, and operational-mode limits
- `ContinuityDomain.md`: historical/current separation, supersession, replacement, revocation, stale-state, and lifecycle history
- `InteroperabilityDomain.md`: shared semantic interpretation without exchange, schema, protocol, ownership transfer, or authority inflation
- `EcosystemParticipantBoundaryMatrix.md`: participant-purpose boundaries without creating a new domain or exchange mechanism
- `Phase3TwinIntelligenceLayer.md`: derived/advisory intelligence boundaries
- `StructuredSystemReasoningGraph.md`: future derived reasoning graph, dependencies, provenance, confidence, and view boundaries
- `ScenarioIntelligence.md`, `InfrastructureSimulation.md`, and `WhatIfAnalysis.md`: scenario, simulation, and change-analysis outputs that may become stale when inputs change

This document does not override any of those boundaries.

## Dependency Model

A dependency is a planning relationship where one output, interpretation, view, scenario, safety context, or confidence posture relies on one or more upstream facts, assumptions, sources, rules, lifecycle states, permissions, or grounding artifacts.

Future dependency records or reasoning should preserve these concepts when implementation is approved:

- upstream fact or source object
- affected downstream output or interpretation
- dependency type
- lifecycle state of the upstream and downstream context
- source and provenance basis
- confidence and verification posture
- assumptions and missing inputs
- rule keys or grounding references where applicable
- view and permission scope where external visibility is involved
- limitation text
- last reviewed or generated context when persisted

### Dependency Types

| Dependency type | Meaning | Examples | Boundary |
| --- | --- | --- | --- |
| Source dependency | Output depends on a recorded Twin fact or source document. | Load watts drive backup sizing; panel amperage drives service posture. | Source quality limits downstream confidence. |
| Topology dependency | Output depends on how objects relate. | Battery recommendation depends on inverter/gateway topology; pathway estimate depends on structure and route context. | Planning topology is not field verification. |
| Lifecycle dependency | Output depends on current, sandbox, proposed, scenario, contractual, verified, utility-reviewed, or future operational state. | Scenario comparison depends on saved revision state; utility-readiness context depends on proposed versus utility-reviewed status. | Lifecycle state must not be collapsed. |
| Rule dependency | Output depends on a deterministic rule or calculation basis. | Recommendation profile, sizing range, roof-readiness posture, backup-scope classification. | Rule output remains derived planning intelligence. |
| Grounding dependency | Output depends on provider-backed, product-backed, benchmark-backed, quote-backed, or source-backed evidence. | Solar production model, product capability, market reasonableness, quoted cost. | Grounding does not create provider integration, verified pricing, or authority by itself. |
| Permission dependency | Output or view depends on a permission scope, audience, purpose, duration, exclusion, or revocation state. | Contractor view, utility-safe view, AI grounding view. | Permission doctrine is not runtime enforcement until approved. |
| Provenance dependency | Output depends on source lineage, confidence, verification scope, missing data, assumptions, or conflict state. | Confidence posture, trust badges, view limitation text. | Provenance does not grant access or prove correctness. |
| Safety dependency | Output depends on safety-relevant energy-source, isolation, export, operational-mode, or verification context. | Safety-scoped view, worker-safety context, utility export-capability interpretation. | Safety context is not safety approval. |
| Continuity dependency | Output depends on historical/current state, supersession, replacement, revocation, stale-state, or scenario lineage. | Historical comparison, real-estate infrastructure summary, contractor handoff context. | Continuity is not ownership transfer or proof of current state by itself. |
| Participant interpretation dependency | Output depends on audience, purpose, minimum necessary domains, prohibited claims, and prohibited authority assumptions. | Contractor scoping, insurance context, manufacturer support, aggregator readiness. | Participant interpretation does not change Twin truth. |

## Invalidation Model

Invalidation means a downstream output, view, scenario, confidence posture, safety context, continuity record, or participant interpretation can no longer be treated as current without review.

Invalidation does not mean deletion.

Stale outputs should remain traceable when they are useful for history, scenario revision lineage, audit, comparison, or explanation. The system should distinguish active/current outputs from stale, superseded, historical, revoked, or snapshot-bound outputs.

### Invalidation States

| State | Meaning | Expected posture |
| --- | --- | --- |
| Current | Dependency basis still matches the relevant Twin facts, lifecycle state, provenance, and view scope. | May be used within its planning-only authority limits. |
| Stale | One or more upstream facts changed after the output was generated or reviewed. | Must be labeled before reuse; should not support confident planning claims. |
| Needs recalculation | Deterministic output depends on changed facts or rules. | Recalculate before treating as current planning intelligence. |
| Needs re-grounding | Output depends on source, provider, product, quote, market, utility, or document evidence that changed, expired, conflicted, or became missing. | Refresh grounding basis or lower confidence. |
| Needs re-review | Output depends on contractor, engineer, utility, AHJ, safety, insurance, finance, manufacturer, aggregator, or other participant interpretation. | Treat prior review as limited to its original scope until updated. |
| Needs re-labeling | Output remains useful, but confidence, provenance, lifecycle, safety, permission, or participant limitation text changed. | Update labels before presenting to users or participants. |
| Superseded | A newer source-backed output or record replaces the old one. | Preserve history; avoid presenting as current. |
| Revoked or out of scope | Permission, view scope, source-document access, or participant purpose no longer covers the output. | Do not use for external visibility unless future approved permission permits it. |
| Snapshot-bound | Output belongs to a saved scenario revision or historical state. | Preserve as historical context; do not imply current validity or full replay. |

### Invalidation Triggers

Changes that should trigger impact review include:

- premise or service context changes
- building or structure changes
- panel, service, circuit, load, backup-priority, or pathway changes
- equipment product, role, assignment, quantity, location, or existing/proposed posture changes
- energy-source, isolation-system, export-capability, operational-mode, or verification-status changes
- design goal, backup scope, outage target, pathway, scenario, or scenario revision changes
- utility provider, service, interconnection, export, program, tariff, or utility-source context changes
- product-spec, provider, quote, market, benchmark, or source-document changes
- permission grant, scope, audience, purpose, exclusion, duration, revocation, or view-contract changes
- provenance, confidence, verification scope, source conflict, missing-data, or stale-state changes
- lifecycle transition, supersession, replacement, revocation, or historical/current state change
- participant-purpose or prohibited-claim boundary changes

No invalidation state should imply that a runtime invalidation engine, event log, API, schema, or persistence model exists.

## Recalculation Requirements

Future deterministic outputs should be recalculated when their source facts, topology, lifecycle state, rules, product assumptions, grounding evidence, or missing-data posture changes.

Affected outputs may include:

- recommendation profiles
- battery sizing ranges
- solar sizing ranges
- backup-load selection
- panel/service architecture posture
- inverter/system architecture posture
- architecture-fit tradeoffs
- roof-readiness or roof-measurement-confidence posture
- scenario comparisons
- infrastructure simulations
- what-if analyses
- product compatibility reasoning
- takeoff previews
- cost/economic sensitivity where approved and source-backed

Recalculation should preserve:

- source facts and source objects used
- rule keys
- generated or reviewed context where available
- assumptions and missing inputs
- confidence and verification posture
- lifecycle state
- provenance summary
- limitation text
- stale or superseded output lineage where persisted

Recalculation must not promote derived outputs into canonical facts.

## Re-Grounding Requirements

Re-grounding means refreshing the evidence basis for an output before it is reused.

Future outputs may require re-grounding when:

- product documentation changes
- product availability, model identity, capability evidence, or compatibility notes change
- quote, benchmark, or market reasonableness context changes
- solar production or provider-backed model inputs change
- utility source documents, interconnection context, export context, or program context change
- safety source documents or verification scope changes
- provenance becomes stale, partial, conflicting, missing, or out of view scope

Re-grounding should preserve the difference between:

- recorded fact
- source-backed document
- provider-backed model
- product-backed capability
- benchmark-backed context
- quote-backed context
- utility-source context
- contractor-reviewed context
- engineer-reviewed context
- advisory explanation

Re-grounding must not imply provider integration, verified pricing, savings guarantee, product compatibility approval, utility approval, engineering approval, safety approval, operational readiness, or authority-of-record replacement.

## Re-Review Requirements

Re-review means a prior participant or authority-adjacent interpretation should not be reused as current without checking the changed facts and original scope.

Future re-review may be required for:

- contractor scoping or route assumptions after site, pathway, equipment, or load changes
- engineer review inputs after panel, service, circuit, load, equipment, topology, or source-evidence changes
- safety context after energy-source, isolation, export, operational-mode, or verification-status changes
- utility context after provider, service, interconnection, export, equipment, load, or permission changes
- manufacturer support after product model, role, assignment, or compatibility assumption changes
- insurance context after safety, equipment, continuity, verification, or source-document changes
- finance context after equipment, design, scenario, estimate boundary, quote, or contractual-context changes
- aggregator readiness after equipment, utility, capability, permission, lifecycle, telemetry, or operational-boundary changes
- AI grounding after any source, derived, provenance, permission, or view-boundary change relevant to the AI task

Re-review does not create professional approval, utility approval, safety certification, legal authority, financial authority, warranty authority, or operational authorization.

## Impact Categories

### Derived Output Impacts

Derived outputs should become stale or need recalculation when upstream facts, rules, grounding, lifecycle state, or missing-data posture changes.

Examples:

- a load wattage change affects backup-load selection, battery sizing, outage endurance, scenario comparison, and contractor scoping context
- a panel service-size change affects panel/service posture, pathway suitability, equipment constraints, and engineer review inputs
- a product capability change affects solar sizing, inverter/system posture, product compatibility, manufacturer support context, and utility-readiness context

### View Impacts

Views should be re-evaluated when included facts, excluded facts, permission scope, source-document visibility, derived-output visibility, audience, purpose, revocation, or limitation text changes.

View impact should preserve:

- minimum necessary exposure
- permission and purpose boundaries
- source and provenance summaries
- lifecycle state
- data classification
- trust-zone posture
- missing-data and assumption visibility
- prohibited claims

Existing broad `/api/*` responses are not permissioned Twin views and must not be silently reclassified as runtime enforcement.

### Scenario Impacts

Scenarios and scenario revisions should distinguish live current state from snapshot-bound historical state.

When source facts change:

- live scenario comparisons may need recalculation
- saved scenario revisions should remain historical snapshots
- snapshot-bound outputs should not imply full replay unless that future capability exists
- changed assumptions should be visible when comparing old and new states
- stale scenario recommendations should be labeled before reuse

### Provenance Impacts

Provenance posture should update when source lineage, source quality, confidence, verification scope, source conflicts, missing inputs, assumptions, or limitation text changes.

If provenance weakens or becomes incomplete, downstream confidence should be lowered or the output should be labeled provisional. If provenance improves, the output may still require recalculation, re-grounding, or re-review before stronger language is used.

Provenance impacts do not grant permission, prove correctness, resolve conflicts by themselves, or create compliance, safety, utility, financial, warranty, procurement, or operational authority.

### Confidence Impacts

Confidence should reflect the current dependency basis.

Confidence should decrease when:

- source facts are missing, stale, inferred, placeholder, demo, conflicting, revoked, or outside scope
- topology is incomplete or not field-verified
- product capability evidence is missing or stale
- utility, safety, or participant context lacks source evidence
- a deterministic output has not been recalculated after changed inputs
- a participant review predates material source changes

Confidence should not increase merely because advisory text is clearer or an AI explanation is more polished.

### Safety Impacts

Safety context should be re-evaluated when changes affect:

- energy sources
- isolation systems
- export capabilities
- operational modes
- verification status
- source evidence
- equipment roles or assignments
- topology relationships
- utility or interconnection context
- permissioned safety visibility

Safety impact propagation must preserve the boundary between safety context and safety approval. A change may require re-labeling safety limitations, re-grounding safety evidence, or re-reviewing safety-scoped views. It does not create field verification, AHJ approval, inspection approval, utility approval, emergency-response authority, operational readiness, or device-control authority.

### Continuity Impacts

Continuity records should preserve what changed, when it changed, what source supports it, what outputs were affected, and whether prior outputs are current, stale, superseded, revoked, or historical.

Continuity impact should distinguish:

- current recorded state
- historical state
- sandbox state
- proposed state
- saved scenario revision state
- future contractual state
- future field-verified state
- future utility-reviewed state
- future operational state

Continuity impact propagation does not define ownership transfer, legal title, contractual rights, utility authority, proof of installation, proof of current state, or operational control.

### Participant-View Impacts

Participant-facing interpretations should be re-evaluated when changes affect the participant's purpose, minimum necessary domains, permission basis, provenance requirements, continuity requirements, interoperability semantics, prohibited claims, or prohibited authority assumptions.

Examples:

- contractor interpretation may change after pathway, equipment, load, or safety context changes
- utility interpretation may change after service, interconnection, export, equipment, load, permission, or provenance changes
- real-estate interpretation may change after continuity, safety, equipment, or historical/current labels change
- insurance interpretation may change after safety, verification, equipment, or source evidence changes
- finance interpretation may change after scenario, quote, equipment, estimate boundary, or contractual-context changes
- manufacturer interpretation may change after product model, assignment, compatibility, or source-document changes
- aggregator interpretation may change after capability, utility, permission, lifecycle, telemetry, or operational-boundary changes
- AI interpretation should change whenever grounding facts, derived outputs, provenance, confidence, or view constraints change

Participant interpretation must not overwrite Twin truth or create exchange, ownership transfer, approval, eligibility, warranty, financial, utility, telemetry, dispatch, or operational authority.

## Stale Output Handling

Stale outputs should remain visible when they carry useful historical, audit, scenario, or continuity value. They should not be presented as current planning intelligence without clear labels.

Stale output handling should preserve:

- original source basis
- generated or reviewed context where available
- changed dependency basis
- current stale reason
- affected downstream outputs or views where known
- confidence downgrade when applicable
- limitation text
- revision or continuity linkage when applicable

Stale output handling must not silently delete historical context or silently retain obsolete recommendations.

## Missing Data Behavior

Dependency impact propagation should surface missing data introduced by a change.

Examples:

- adding a battery may introduce missing inverter compatibility, gateway, critical-load, and interconnection inputs
- changing a load may introduce missing circuit, wattage, duty-cycle, backup-priority, or phase inputs
- changing a utility context may introduce missing effective date, source document, export limit, program context, or permission scope
- changing a safety record may introduce missing verification scope, source evidence, lifecycle state, or view limitation

Missing data should downgrade confidence, block unsupported claims, or require re-grounding or re-review where appropriate.

## Architectural Impact Assessment

This is a doctrine-only Phase 3 architecture milestone.

It adds an integrity model for stale outputs, dependency invalidation, recalculation, re-grounding, re-review, provenance impacts, confidence impacts, safety impacts, continuity impacts, and participant-view impacts.

It does not approve or imply:

- runtime invalidation logic
- event logs
- databases or graph databases
- schemas or migrations
- APIs or API versioning
- services or background jobs
- UI workflows
- permission enforcement
- auth, RBAC, ABAC, tenant isolation, encryption, telemetry governance, audit policy, or access monitoring
- source-backed promotion workflows
- exchange mechanisms
- ownership transfer
- exports or scoped packets
- utility submissions
- provider integrations
- product catalogs
- safety approval or field verification workflows
- NEC, AHJ, permitting, engineering, financial, tax, warranty, procurement, or legal authority
- DERMS, dispatch, demand response, VPP participation, aggregator enrollment, telemetry authority, operational control, or authority-of-record replacement

Any future implementation requires explicit Matt approval before changing runtime behavior, schemas, APIs, persistence contracts, permission enforcement, provenance policy, utility authority, safety workflows, or operational-control boundaries.

## Risks

- Stale recommendations could be reused without visible labels if future implementation does not preserve dependency basis.
- Recalculation could be mistaken for verification if confidence and provenance posture are not carried forward.
- Scenario revisions could be mistaken for current state if snapshot boundaries are hidden.
- Participant-facing views could overclaim if invalidation does not update prohibited claims and limitation text.
- Safety context could drift into safety approval if verification scope and source evidence are not explicit.
- Continuity records could drift into ownership transfer or proof of current state if historical/current labels are weak.
- Utility and aggregator contexts could drift into export permission, program eligibility, dispatch, telemetry, or operational control if view and permission boundaries are not enforced in future implementation.
- AI explanations could preserve stale conclusions if grounding context is not refreshed after source facts change.

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating runtime dependency, invalidation, impact, stale-output, event-log, or graph models
- changing schema, migrations, persistence contracts, canonical data models, APIs, services, calculations, or UI workflows
- implementing recalculation engines, re-grounding workflows, re-review workflows, background jobs, or notification behavior
- defining mandatory dependency metadata, stale-output semantics, confidence thresholds, provenance thresholds, or invalidation policies as runtime behavior
- creating exchange mechanisms, exports, packets, protocols, standards, ownership-transfer workflows, or external contribution workflows
- implementing permission enforcement, scoped views, auth, RBAC, ABAC, tenant isolation, encryption, telemetry governance, audit enforcement, access monitoring, utility APIs, DERMS, dispatch, demand response, VPP participation, aggregator enrollment, or operational control
- treating dependency impact propagation as safety approval, professional review, utility approval, interconnection approval, financial authority, warranty authority, procurement authority, legal authority, field verification, operational readiness, or authority-of-record replacement

## Sources / Provenance

- User-provided Dependency Impact Propagation milestone, 2026-06-02
- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/ARCHITECTURE.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/TopologyLifecycleDomains.md`
- `docs/architecture/PermissionPlacement.md`
- `docs/architecture/ProvenancePlacement.md`
- `docs/architecture/ViewContracts.md`
- `docs/architecture/SafetyDomain.md`
- `docs/architecture/ContinuityDomain.md`
- `docs/architecture/InteroperabilityDomain.md`
- `docs/architecture/EcosystemParticipantBoundaryMatrix.md`
- `docs/architecture/Phase3TwinIntelligenceLayer.md`
- `docs/architecture/StructuredSystemReasoningGraph.md`
- `docs/architecture/ScenarioIntelligence.md`
- `docs/architecture/InfrastructureSimulation.md`
- `docs/architecture/WhatIfAnalysis.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `docs/architecture/COGNITION_LAYERS.md`
- `docs/architecture/CANONICAL_TERMINOLOGY.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/doctrine-formalization/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `.codex/project-skills/continuity-governance/SKILL.md`
- `.codex/project-skills/canonical-authority-discipline/SKILL.md`
- `/home/mattcoje/.codex/skills/provenance-enforcement/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

Dependency Impact Propagation defines docs-only Phase 3 architecture for how changes to Residential Energy Twin facts should affect downstream derived outputs, views, scenarios, provenance posture, confidence posture, safety context, continuity records, and participant-facing interpretations. It establishes stale-output, invalidation, recalculation, re-grounding, re-review, and re-labeling expectations without creating a new Twin domain and without approving runtime implementation, APIs, schemas, exchange, ownership transfer, utility behavior, safety approval, or operational control.
