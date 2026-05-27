# Scoped Intelligence Outputs

## Purpose

Define safe output boundaries before contractor, utility, consumer, or orchestration intelligence becomes operational.

These boundaries are source-of-truth design constraints, not runtime security controls. Current APIs do not implement RBAC, tenant isolation, contractor portals, utility packets, or operational control permissions.

## Shared Envelope Requirements

Future scoped API views should include:

- object identity and lifecycle stage
- authority layer: canonical, derived, advisory, operational, or historical
- trust zone
- data classification
- provenance summary with source objects, data origin, confidence, assumptions, and missing inputs
- explicit planning-only limitations where engineering, permitting, utility, or operational authority is absent

Current additive metadata support:

- Backend enums now represent authority layers, data classifications, and intended API-view audiences.
- Backend schema helpers now represent view-boundary and permission-readiness metadata.
- AI context and scenario comparison responses now carry additive view-boundary metadata.
- Account responses may carry additive permission-readiness metadata that explicitly marks role, plan, and subscription fields as non-enforcing scaffolding.
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md` now maps current broad/raw response surfaces to candidate consumer-safe, AI-safe, contractor-safe, and future utility-safe view models without changing behavior or implementing enforcement.

Future scoped API views should exclude:

- hidden AI-derived facts
- fields whose classification is broader than the requested view
- advisory text without structured source context
- operational-control fields unless an operational authority model exists

## Consumer-Safe

May include:

- planning explanations
- tradeoffs
- assumptions
- missing inputs
- non-authoritative next steps

Typical classification: `planning_private` plus selected `public_reference` material.

Must not include:

- permit readiness
- engineering approval
- utility approval
- hidden confidence upgrades
- contractor, utility, or operational-control claims

## Contractor-Safe

May include:

- recorded planning facts
- source-linked assumptions
- design intent
- known missing field checks
- planning-only derived estimates

Typical classification: `contractor_scoped`.

Must not include:

- stamped design claims
- code compliance claims
- verified site conditions unless explicitly recorded
- access to unrelated homeowner-private planning context
- AI explanations separated from their structured source context

## Utility-Safe

Deferred. Future outputs must be source-linked, minimized, and separated from AI-generated advisory text.

Typical classification: `utility_scoped`.

Future requirements:

- explicit site and service-territory identity model
- utility-facing data minimization
- interconnection-state authority model
- no submission, approval, tariff, or program eligibility claim without a dedicated authority layer

## Orchestration-Safe

Deferred. Future outputs require operational authority, device identity, auditability, and failure handling before control behavior exists.

Typical classification: `operational_control`.

Future requirements:

- permission and control boundary
- auditable command/event lineage
- failure and fallback model
- no DER dispatch, device-control, or live operational behavior from advisory context

## RBAC Preparation Boundary

Role labels, account fields, and subscription fields are currently scaffolding only. Documentation may define future consumer, contractor, utility, operator, or internal views, but no current endpoint should be described as enforcing those roles.

Before implementation, each future role-aware API view needs:

- allowed authority layers
- allowed data classifications
- required provenance fields
- explicit excluded fields
- audit and revision expectations
- compatibility plan for existing `/api/*` contracts

The current scoped view-model mapping is the next design input for that work; it should be treated as a contract-design guide, not as a runtime access-control policy.
