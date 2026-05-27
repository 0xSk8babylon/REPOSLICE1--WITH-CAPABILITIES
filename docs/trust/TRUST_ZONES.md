# Trust Zones

## Zone 1: Recorded Planning Facts

User-created, imported, demo, or verified records in structured persistence.

Trust posture depends on `data_origin`, source lineage, and verification status. Recorded does not automatically mean verified.

## Zone 2: Derived Planning Intelligence

Deterministic outputs from recorded facts.

Examples: recommendation profiles, sizing ranges, readiness scores, scenario comparisons.

Required posture: expose basis, confidence, limitations, and missing inputs.

## Zone 3: Advisory Explanation

Human-readable guidance created from recorded and derived layers.

Required posture: explain uncertainty and avoid authority inflation.

## Zone 4: Operational Truth

Runtime, installation, utility, permitting, code, field, or dispatch truth.

Current status: outside system authority.

## Scoped Output Rules

- Consumer-safe outputs may explain planning tradeoffs and next questions.
- Contractor-safe outputs may organize recorded facts and planning assumptions, but must not imply engineering sign-off.
- Utility-safe outputs are deferred until an explicit utility abstraction and authority model exists.
- AI-safe outputs must be structured, source-linked, and non-authoritative unless promoted through an approved canonical path.
