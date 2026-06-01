# Provenance Placement

Status: Phase 2 architecture planning document
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no schema, migration, runtime provenance enforcement, API, auth, RBAC, ABAC, encryption, telemetry governance, utility API, DERMS, dispatch, operational-control, or canonical runtime provenance model is approved or implied

## Purpose

Provenance placement defines where source lineage, evidence, confidence, verification posture, assumptions, limitations, and authority metadata attach inside the Residential Energy Twin.

This document extends `ResidentialEnergyTwinContractV1.md` and `TopologyLifecycleDomains.md`. It completes Phase 2 placement architecture for provenance, but it does not implement mandatory provenance fields, completeness thresholds, trust-state semantics, audit policy, enforcement behavior, or schema/API changes.

## Core Principle

Provenance is required for authority-bearing facts and derived outputs.

A fact may be recorded without complete provenance, but its authority must remain limited and visible. Missing provenance is itself important planning information. The system should show unknown, partial, stale, inferred, placeholder, demo, or conflicting provenance instead of replacing it with confident prose.

Provenance does not grant access. Permission does not prove source quality. Both must survive into future view contracts.

## Attachment Points

Future provenance should attach at multiple levels.

| Attachment level | Purpose | Examples | Boundary |
| --- | --- | --- | --- |
| Twin-level | Summarize the overall source, confidence, and limitation posture of the Residential Energy Twin. | Domain coverage, stale areas, missing provenance, demo content. | Does not prove correctness or completeness. |
| Domain-level | Summarize source quality for a twin domain. | Premise, buildings, electrical infrastructure, loads, equipment, designs, pathways, scenarios, permissions, utility relationships. | Useful for quick trust posture, not a replacement for field evidence. |
| Field-level | Link important authority-bearing fields to source basis. | `home.service_size`, panel amperage, load watts, product specs, pathway distance, future permission scope. | Required before stronger claims depend on the field. |
| Source-document level | Preserve evidence references and document context. | Photos, product sheets, utility documents, homeowner uploads, contractor notes, inspection records. | Source documents may support only specific fields, not whole records. |
| Derived-output level | Explain deterministic or advisory outputs. | Advisor recommendations, sizing ranges, scenario comparison, takeoffs, AI grounding, topology posture. | Derived provenance does not make the output canonical. |
| Lifecycle-transition level | Record evidence behind authority increases. | Sandbox to proposed, proposed to contractual, contractual to field-verified, future utility-reviewed. | No transition should increase authority without source-backed lineage. |
| View/export level | Preserve provenance in audience-specific projections. | Contractor, engineer, utility, AI, audit views. | Views should downgrade or label claims when provenance is partial. |
| Audit/security level | Preserve who did what, when, under what authority. | Future grant changes, exports, verification, revocation, utility sharing, operational events. | Deferred until audit/security implementation is approved. |

## Source-Of-Truth Expectations

Structured facts outrank generated text.

Expected source posture, strongest to weakest within a defined scope:

1. Field-verified or professionally confirmed source with scope and timestamp.
2. Source-backed document or artifact such as photo, equipment label, drawing, utility document, manufacturer documentation, permit artifact, or submitted record.
3. Homeowner or stakeholder declaration.
4. Imported or application-created structured planning record.
5. Deterministic derived output from recorded inputs and explicit rules.
6. Inferred planning interpretation.
7. Advisory explanation or AI-generated summary.
8. Unknown, placeholder, demo, or missing source.

This order does not imply code compliance, utility approval, safety, eligibility, savings, or operational readiness. Stronger source quality improves traceability only within its stated scope.

## Evidence And Reference Expectations

Authority-bearing facts should identify:

- source object or source document identity
- source type
- data origin
- field, domain, lifecycle state, or output covered
- value snapshot or change context
- source date and verified date when available
- actor or source system when relevant
- confidence level
- verification posture
- assumptions and missing inputs
- limitation text
- conflicts or supersession notes

Evidence can be granular. A source document that supports one equipment spec should not certify every spec on the product record. A panel photo may support a label value but not full NEC compliance. A utility document may support service or interconnection context but not tariff authority unless a future approved rate model supports it.

## Confidence And Verification Expectations

Confidence describes how strongly the system should rely on a value for a stated use. Verification describes whether a source or responsible party has confirmed a value within a defined scope.

Expected confidence posture:

- high: source-backed, current, and appropriate for the stated planning use
- medium: plausible and structured, but incomplete, stale, or not field-verified
- low: inferred, placeholder, demo, conflicting, or missing important evidence
- not assessed: no responsible confidence evaluation exists

Verification must not be overstated. A verified field is not a verified record unless the source covers the whole record. A verified planning input is not engineering approval, utility approval, code compliance, safety approval, or operational authority.

## Canonical, Derived, And Advisory Provenance

### Canonical Provenance

Canonical provenance attaches to recorded twin facts and source documents.

It should preserve:

- source identity
- field/domain coverage
- lifecycle state
- data origin
- confidence and verification posture
- assumptions, missing inputs, limitations
- created/updated timestamps when implemented
- supersession or conflict state when implemented

### Derived Provenance

Derived provenance attaches to deterministic outputs.

It should preserve:

- source records and fields
- rule keys
- generated timestamp when persisted
- derivation type
- confidence posture
- missing inputs
- assumptions
- limitations
- authority layer and data classification
- revision identity when persisted historically

Derived provenance explains how an output was produced. It does not promote the output into a canonical fact.

### Advisory Provenance

Advisory provenance attaches to explanations, AI summaries, planning guidance, and recommendation copy.

It should preserve:

- grounding records
- source summaries
- derived-output basis
- limitation text
- AI cannot create canonical facts warning where relevant
- missing inputs and unknowns

Advisory provenance prevents generated text from being mistaken for source truth.

## Lifecycle-State Provenance Requirements

| Lifecycle state | Provenance expectation |
| --- | --- |
| Current deployed state | Must expose whether recorded facts are declared, imported, documented, field-verified, stale, inferred, placeholder, or unknown. |
| Sandbox state | Must label assumptions and draft values so they are not mistaken for current deployed or contractual state. |
| Proposed pathway state | Must preserve design basis, source records, derived rule keys, assumptions, missing inputs, and planning-only limitations. |
| Saved scenario revision state | Must include revision identity and snapshot fidelity limits. Compact revisions do not imply full replay. |
| Contractual state | Future state requires source-backed commitment evidence, scope, exclusions, actor, timestamp, and permission/audit linkage. |
| Field-verified state | Future state requires verification source, scope, verified fields, verified date, responsible party, and limitations. |
| Utility-reviewed state | Future state requires utility source evidence, export purpose, permission scope, service/interconnection context, and no unsupported approval claims. |
| Operational topology state | Separate future trust domain requiring telemetry source validation, command authorization, audit lineage, failure boundaries, and security posture. |

## Utility And Grid-Edge Trust Implications

Utility and grid-edge contexts require stricter provenance because weak lineage can create unsupported authority.

Future utility-facing provenance should identify:

- utility/provider source documents
- service territory or service context basis
- interconnection context source and status
- equipment and topology facts included in the view
- export purpose
- permission scope
- revision identity
- limitation text for tariff, eligibility, approval, export, and operational status

Utility provenance must not imply:

- tariff authority
- incentive eligibility
- interconnection approval
- utility submission authority
- DERMS, dispatch, demand response, VPP, aggregator enrollment, device availability, or operational control

## Future Grounding-Layer Provenance

Future solar production, market/economic, and verified product intelligence grounding must preserve provider, quote, product, benchmark, and derived-output provenance.

See `SolarMarketProductIntelligenceGrounding.md` for the Phase 2 architecture bridge. Provider-backed or benchmark-backed outputs should identify source/provider references, provider/version where applicable, source dates, input assumptions, normalized fields used, confidence, missing inputs, limitations, and whether the output is estimated, modeled, quoted, parsed, verified, manufacturer-backed, contractor-reviewed, engineer-reviewed, or market-benchmarked.

No grounding-layer output should become canonical, verified, financial, utility, engineering, or operational authority without a future approved source-backed promotion workflow.

## Future Audit And Security Compatibility

Provenance placement should prepare for future audit and security layers without claiming they exist now.

Future-compatible requirements:

- audit events for source creation, source update, source conflict, verification, supersession, view creation, export, permission grant, revocation, utility sharing, and future operational-control-adjacent events
- data classification attached to source facts, derived outputs, views, exports, and audit records
- provenance survival through scoped views and minimized exports
- integrity expectations for sensitive evidence and future operational-control records
- encryption/key-management readiness for sensitive source documents, permission records, utility documents, and operational-control data
- telemetry governance before telemetry can become source truth

Deferred implementation:

- mandatory field-level provenance
- provenance completeness thresholds
- runtime provenance enforcement
- audit policy and audit event persistence
- data-classification enforcement
- auth, RBAC, ABAC, tenant isolation
- encryption/KMS
- telemetry governance
- utility export provenance enforcement
- operational-control provenance

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- defining mandatory provenance fields, completeness thresholds, trust-state semantics, confidence semantics, or verification-status semantics
- changing schema, migrations, persistence contracts, canonical models, APIs, or existing `/api/*` contracts
- enforcing twin-level, domain-level, field-level, permission-level, utility-level, derived-output, or view/export provenance
- implementing audit events, data classification enforcement, security policy, auth, RBAC, ABAC, encryption, telemetry governance, or access monitoring
- promoting derived or advisory outputs into canonical facts
- defining utility provenance authority, tariff authority, interconnection authority, utility exports, DERMS, dispatch, aggregator, or operational-control provenance

## Sources / Provenance

- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/TopologyLifecycleDomains.md`
- `docs/architecture/SolarMarketProductIntelligenceGrounding.md`
- `docs/provenance/RESIDENTIAL_ENERGY_TWIN_PROVENANCE_POLICY_PLANNING.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/canonical-authority-discipline/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `.codex/project-skills/topology-intelligence/SKILL.md`

## Summary

Provenance placement attaches source lineage to the Residential Energy Twin at twin, domain, field, source-document, derived-output, lifecycle-transition, view/export, and future audit/security levels. Phase 2 defines where provenance belongs and what it must preserve. Runtime enforcement, mandatory provenance fields, audit/security policy, utility export provenance, and operational-control provenance remain deferred until Matt explicitly approves them.
