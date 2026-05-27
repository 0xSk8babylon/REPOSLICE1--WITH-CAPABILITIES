# Trust Zones

## Zone 1: Recorded Planning Facts

User-created, imported, demo, or verified records in structured persistence.

Trust posture depends on `data_origin`, source lineage, and verification status. Recorded does not automatically mean verified.

Authority layer: canonical planning state when persisted or explicitly documented, but not operational truth.

Typical data classification: `planning_private`, `public_reference`, or `internal_governance` depending on object type and source.

## Zone 2: Derived Planning Intelligence

Deterministic outputs from recorded facts.

Examples: recommendation profiles, sizing ranges, readiness scores, scenario comparisons.

Required posture: expose basis, confidence, limitations, and missing inputs.

Authority layer: derived estimate. It may be reproducible and inspectable, but it is still downstream of recorded planning state and partial provenance.

Typical data classification: inherits from source objects and may become `contractor_scoped` only through a future scoped API view.

## Zone 3: Advisory Explanation

Human-readable guidance created from recorded and derived layers.

Required posture: explain uncertainty and avoid authority inflation.

Authority layer: advisory knowledge. It is never the source of canonical facts, verification, compliance, or operational authorization.

Typical data classification: inherits from the underlying context and should not be exported without source-linked provenance.

## Zone 4: Operational Truth

Runtime, installation, utility, permitting, code, field, or dispatch truth.

Current status: outside system authority.

Authority layer: future operational state only after explicit contracts, verification, enforcement, and auditability exist.

Typical data classification: `operational_control` or `utility_scoped`; currently deferred.

## Data Classification Rule

Data classification controls intended visibility and handling. It does not prove correctness, verification, compliance, or engineering validity.

Trust posture controls confidence and source quality. It does not grant access rights or operational authority.

Future API views must carry both concepts separately:

- authority layer: canonical, derived, advisory, operational, or historical
- trust zone: recorded fact, derived planning intelligence, advisory explanation, or operational truth
- data classification: public reference, planning private, contractor scoped, utility scoped, operational control, or internal governance
- provenance summary: source objects, data origin, missing inputs, assumptions, and confidence posture

## Scoped Output Rules

- Consumer-safe outputs may explain planning tradeoffs and next questions.
- Contractor-safe outputs may organize recorded facts and planning assumptions, but must not imply engineering sign-off.
- Utility-safe outputs are deferred until an explicit utility abstraction and authority model exists.
- AI-safe outputs must be structured, source-linked, and non-authoritative unless promoted through an approved canonical path.
- Scoped API views are not RBAC until enforcement exists. They are contract boundaries that prepare safe audience-specific representations.
