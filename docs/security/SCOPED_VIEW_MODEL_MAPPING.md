# Scoped View-Model Mapping

## Purpose

Map consumer-safe, AI-safe, contractor-safe, and future utility-safe response boundaries before adding RBAC, exports, contractor packets, utility packets, or operational-control behavior.

This document is a contract-design map only. It does not narrow current responses, enforce access, isolate tenants, authorize exports, or change recommendation behavior.

## Current Status

- Existing `/api/*` responses are compatibility-sensitive product contracts.
- Current broad responses may include canonical planning objects, derived estimates, advisory explanations, provenance records, and historical revision summaries in one payload.
- Additive authority, data-classification, view-boundary, and permission-readiness metadata exists on selected responses, but it is descriptive only.
- Future scoped views should be additive contracts or explicit versions. Current broad GET contracts should not be silently reclassified as filtered role views.

## Shared View Rules

Every future scoped view should preserve:

- stable object identity for records it exposes
- authority layer for canonical, derived, advisory, historical, or operational state
- data classification and trust-zone posture
- provenance summary for derived or advisory outputs
- visible assumptions, missing inputs, confidence, and planning-only limitations
- separation between recorded facts, deterministic estimates, and advisory text

Every future scoped view should exclude:

- hidden AI-derived facts
- enforcement claims when RBAC, tenant isolation, and auth are still absent
- permit, interconnection, engineering, tariff, savings, or operational-control claims unless a future authority layer supports them
- raw internal governance/provenance data when a summarized lineage view is enough

## Audience Boundaries

| Audience | Allowed posture | Typical data classification | Must include | Must exclude |
| --- | --- | --- | --- | --- |
| Consumer-safe | Personal planning view over the user's own recorded home, scenarios, recommendations, and limitations. | `planning_private` plus selected `public_reference` | Recorded planning facts, derived estimates, advisory explanations, missing inputs, trust/provenance summaries. | Contractor authorization, utility submission posture, operational-control data, enforcement claims. |
| AI-safe | Grounding context for explanation or orchestration that consumes structured state but cannot create canonical facts. | `planning_private`, `public_reference`, selected `internal_governance` rule summaries | Minimized structured facts, provenance summaries, rule keys, limitation text, grounding warnings. | Raw object dumps by default, unrelated account/private records, hidden prompt-only facts, write authority. |
| Contractor-safe | Planning packet candidate for future contractor review, still non-authoritative. | `contractor_scoped` | Site/design facts needed for scoping, equipment/product references, route/load assumptions, missing verification fields, planning-only estimates. | Unrelated homeowner notes, subscription/account scaffolding, utility submission claims, stamped design/code claims. |
| Future utility-safe | Minimized source-linked abstraction for possible interconnection or utility-facing workflows. Deferred. | `utility_scoped` | Service/site identifiers that a future authority model validates, minimized equipment/interconnection facts, provenance and revision identity. | AI advisory text, homeowner planning notes, broad product specs, operational dispatch data, tariff/program eligibility claims. |

## Current Broad Exposure Map

| Current surface | Broad/raw exposure | Narrowing candidate | Notes |
| --- | --- | --- | --- |
| `GET /api/ai-context/design/{design_id}` | Broad design grounding payload with home, products, source documents, provenance records, rule provenance, advisor issues, completeness, assigned products, trust summary, warnings, and policies. | `AIDesignGroundingView` | Highest-priority split candidate. Keep current endpoint for compatibility; future AI-safe view should minimize raw objects and expose summaries plus explicit source links. |
| `GET /api/homes` and `GET /api/homes/all` | Home identity, address fields, utility provider, service size, nested buildings, and panels. | `ConsumerHomePlanningView`, `ContractorSiteContextView`, future `UtilitySiteIdentityView` | Current nested shape is frontend-sensitive. Future contractor/utility views should be separate and minimized. |
| `GET /api/designs` and design equipment routes | Design goal, architecture type, status, notes, equipment roles, product IDs, quantities, and siting IDs. | `ConsumerDesignWorkspaceView`, `ContractorDesignIntentView` | Contractor view can include design intent and quantities but should preserve planning-only status and avoid approval language. |
| `GET /api/design-advisor/summary/{design_id}` | Recommendation, profile comparison, planning-state snapshot, current-home architecture, backup scope, panel/service, inverter/system, battery/solar estimates, reasoning graph, provenance summary, and advisory text. | `ConsumerAdvisorSummaryView`, `ContractorPlanningBasisView`, `AIRecommendationGroundingView` | Behavior should remain unchanged. Future splits should separate derived estimates from advisory copy and preserve inspectability metadata. |
| `GET /api/scenarios` and `GET /api/scenarios/{id}/revisions` | Scenario scores/placeholders, notes, linked design IDs, revision overview, and compact historical planning-state snapshots. | `ConsumerScenarioWorkspaceView`, `ScenarioRevisionLineageView` | Revisions are compact lineage records, not full advisor replay. Keep that limitation visible. |
| `GET /api/scenarios/compare` | Scenario records, linked design summaries, completeness, rankings, warnings, and lineage summaries in one comparison payload. | `ConsumerScenarioComparisonView`, `AIComparisonGroundingView` | Current additive `view_boundary` labels this as consumer planning intelligence, not a scoped export. |
| `GET /api/loads` and `GET /api/loads/summary` | Load names, wattage, estimated hours, phase, backup priority, building/home linkage, notes, and provenance summaries where present. | `ConsumerLoadPlanningView`, `ContractorLoadScopingView`, future `UtilityLoadAggregateView` | Utility-safe shape should be aggregate/minimized and should not expose household appliance detail by default. |
| `GET /api/estimated-pathways` | Route source/destination, distances, difficulty, visibility, placeholders, confidence, resilience score, notes, and provenance summary. | `ConsumerPathwayPlanningView`, `ContractorRouteScopingView` | Contractor-safe view may include route assumptions and missing verification fields; utility-safe use remains deferred. |
| `GET /api/takeoffs/current` and `GET /api/takeoffs/generate/{design_id}` | Transient request and line items with placeholder costs, derivation basis, assumptions, notes, trust notes, missing information, and provenance summary. | `ConsumerTakeoffPreviewView`, future `ContractorPreTakeoffView` | Takeoffs remain transient and placeholder-priced. Do not treat them as procurement-ready or persisted estimate snapshots. |
| `GET /api/product-library` | Product references, arbitrary `specs`, documentation URL, notes, provenance summary, and source documents. | `ReferenceProductView`, `ContractorProductReferenceView`, `AIProductGroundingView` | Product `specs` is flexible and can be raw. Scoped views should expose only fields relevant to the audience. |
| `GET /api/provenance`, `/api/rule-provenance`, `/api/source-documents` | Raw provenance, internal rule lineage, and source-document records. | `LineageSummaryView`, `AIRuleGroundingView`, internal governance view | Broad lineage access is useful for inspection but should not become a public/contractor export by default. |
| `GET /api/accounts` | Role, plan, subscription, ownership scaffolding, and permission-readiness metadata. | Future `AccountProfileView` after auth design | Current role/plan/subscription fields do not enforce access, billing, or tenant isolation. |
| `GET /api/estimates/placeholder` | Placeholder estimate status and limitation metadata. | No scoped split needed yet | Keep as a clear deferred-capability marker until real estimate generation exists. |

## Candidate Future View Models

### Consumer-Safe

- `ConsumerHomePlanningView`: current home/building/panel planning facts with trust labels and without export/approval claims.
- `ConsumerDesignWorkspaceView`: design intent, equipment composition, scenario links, and editable planning posture.
- `ConsumerAdvisorSummaryView`: derived recommendation summaries, inspectability, missing inputs, and advisory explanations.
- `ConsumerScenarioComparisonView`: planning rankings, completeness, lineage summaries, and placeholder warnings.
- `ConsumerTakeoffPreviewView`: transient line items with placeholder cost labels and missing-information warnings.

### AI-Safe

- `AIDesignGroundingView`: minimized structured state, source-linked facts, rule keys, provenance summaries, and grounding warnings.
- `AIRecommendationGroundingView`: derived advisor outputs separated from advisory copy, with inspectability and limitations.
- `AIComparisonGroundingView`: scenario comparison facts and lineage summaries without broad raw scenario or account context.
- `AIProductGroundingView`: selected product reference fields and source-document identity rather than arbitrary raw specs by default.

### Contractor-Safe

- `ContractorSiteContextView`: site/building/panel/load/pathway facts needed for planning scoping, with recorded-vs-estimated status.
- `ContractorDesignIntentView`: design goal, equipment quantities, roles, siting assumptions, and known gaps.
- `ContractorPlanningBasisView`: planning-only backup scope, panel/service posture, inverter/system posture, battery/solar ranges, and missing-input lists.
- `ContractorRouteScopingView`: pathway assumptions, distances, source/destination labels, confidence, and verification gaps.
- `ContractorProductReferenceView`: product identity, relevant specs, documentation links, and source verification posture.

### Future Utility-Safe

- `UtilitySiteIdentityView`: minimized service/site identity once a future authority model exists.
- `UtilityInterconnectionContextView`: source-linked service, inverter, storage, generator, and PV facts only after the system has a utility-facing authority layer.
- `UtilityLoadAggregateView`: minimized aggregate load context, not household-level appliance detail by default.

Utility-safe models are deferred until service-territory identity, interconnection-state authority, and export/audit expectations exist.

## Implementation Sequencing

1. Keep current broad endpoints stable and label them as compatibility or internal grounding surfaces.
2. Add explicit view-model schemas before adding role enforcement.
3. Add new endpoints or versioned aliases for scoped views rather than silently narrowing existing frontend GET contracts.
4. Preserve lineage summaries and limitation metadata in every scoped view that exposes derived or advisory intelligence.
5. Only after scoped view contracts exist, map future roles or permissions to those views.
6. Defer RBAC, ABAC, tenant isolation, export authorization, audit, utility submission, contractor packet generation, and operational-control behavior until their authority models exist.

## Strict-Client And API-Shape Concerns

- Additive metadata is acceptable for tolerant clients but can still affect strict external clients that reject unknown fields.
- Existing frontend-sensitive GET contracts should not lose fields, rename fields, or become role-filtered without a versioning plan.
- Future scoped views should use explicit names and envelopes so callers can distinguish them from broad compatibility responses.
- AI-safe views should not depend on scraping advisory prose for canonical facts.
- Contractor-safe and utility-safe views should be new contract shapes, not filtered copies of current broad payloads.

## Deferred Refactors

- Field-level data classification persistence.
- Exhaustive field-level provenance across design, scenario, home-model, and topology records.
- Full replayable advisor payload revisions.
- Scoped export package schemas.
- RBAC/ABAC enforcement, tenant isolation, auth rewrite, billing enforcement, telemetry, encryption/KMS, audit trail, and operational-control command/event lineage.
