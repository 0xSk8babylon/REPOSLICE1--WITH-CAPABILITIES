# Residential Energy Twin Permissioned View Planning Note

Status: design-only permissioned-view planning note
Date: 2026-06-01
Implementation status: no schema, migration, API, runtime, auth, RBAC, ABAC, permission-enforcement, utility authority, DERMS, dispatch, operational-control, or canonical `ResidentialEnergyTwin` model change is approved or implied

## Purpose

This note plans the first permissioned view boundary for the Residential Energy Twin without implementing it.

Permissioned views are future named contracts that expose selected twin facts, derived outputs, assumptions, unknowns, and provenance for a specific audience and purpose. They are not current endpoint filters, RBAC roles, account roles, subscription states, contractor authorizations, utility submissions, or operational permissions.

## Current Broad Surfaces That May Need Scoped Views

Current `/api/*` contracts are compatibility-sensitive product surfaces. They must not be silently narrowed or reclassified as permissioned twin views.

| Current surface | Broad exposure today | Future scoped-view concern |
| --- | --- | --- |
| `GET /api/homes` and `GET /api/homes/all` | Home identity, address fields, service size, utility provider, nested buildings, panels | Split owner planning context from contractor site context and future minimized utility identity. |
| `GET /api/buildings`, `GET /api/panels`, `GET /api/loads` | Site, structure, panel, and load records with planning assumptions | Contractor and engineer views need source status and missing field visibility; utility views should be aggregate/minimized by default. |
| `GET /api/designs` and design equipment routes | Design intent, architecture type, equipment assignments, quantities, roles | Contractor and engineer views may need design basis, but not approval language or unrelated homeowner notes. |
| `GET /api/product-library` | Product references, specs, source documents, notes | AI, contractor, and engineer views need source-linked specs; broad raw specs should not become whole-home authority. |
| `GET /api/estimated-pathways` | Route assumptions, distance, difficulty, visibility, placeholders, confidence | Contractor views may need route assumptions and verification gaps; utility views should exclude construction detail unless required and approved. |
| `GET /api/scenarios`, revisions, and comparison | Scenario records, compact history, rankings, placeholders, warnings, lineage summaries | Homeowner and AI views can compare planning options; contractor/engineer views need bounded project context, not financial guarantees. |
| `GET /api/design-advisor/summary/{design_id}` | Recommendation profiles, current-state architecture, backup/load selection, panel/service posture, inverter/system posture, sizing ranges, reasoning graph, provenance | Derived intelligence must stay labeled as planning-only and should be split from recorded facts for future audiences. |
| `GET /api/ai-context/design/{design_id}` | Broad AI grounding payload with home, design, product, source, provenance, rule, warning, and policy context | Highest-priority future narrowing candidate; AI should receive minimized structured context, not broad raw object dumps by default. |
| `GET /api/provenance`, `/api/rule-provenance`, `/api/source-documents` | Raw lineage and internal rule/source records | Future views should expose summarized provenance unless raw lineage is explicitly intended and approved. |
| `GET /api/accounts` | Account role, plan, subscription, and permission-readiness metadata | Account scaffolding does not grant permission or prove authorization. |

## First Permissioned View Boundary

The first boundary should be a design for named view contracts, not enforcement.

Recommended first design sequence:

1. Keep existing broad endpoints stable.
2. Define named permissioned view shapes before mapping permissions, roles, or grants.
3. Start with read-only view contracts for homeowner, contractor, engineer, and AI contexts.
4. Keep utility view design deferred until utility authority, export scope, audit, and provenance requirements are approved.
5. Preserve provenance, data classification, authority layer, trust zone, assumptions, unknowns, derived-output status, and limitation text in every view.

## Audience Boundaries

### Homeowner View

May see in principle:

- broad owner planning context for the homeowner's own home
- recorded home, building, panel, load, equipment, design, pathway, scenario, and revision records
- provenance summaries, missing fields, assumptions, unknowns, and placeholder labels
- advisory recommendations, scenario comparisons, takeoff previews, and planning next steps when clearly labeled
- permission status and grant history only after a future approved permission model exists

Must exclude by default:

- claims of engineering, code, permit, AHJ, utility, tariff, savings, bid, procurement, or operational approval
- hidden AI-created facts
- external-party access claims before permission enforcement exists
- operational-control state or dispatch authority

### Contractor View

May see in principle:

- scoped site context needed for planning, scoping, site walks, and rough coordination
- relevant building, panel, load, equipment, pathway, design, and missing-data records
- route assumptions, product references, quantities, roles, source documents, and provenance summaries
- planning-only advisor outputs that explain scope basis, warnings, and verification gaps

Must exclude by default:

- unrelated homeowner notes, account/subscription data, broad AI context, and private context outside the project scope
- utility submission posture, interconnection approval, tariff claims, or operational-control context
- stamped-design, code-compliance, estimate, bid, procurement, or safety guarantees
- raw internal governance records unless explicitly needed and approved

### Engineer View

May see in principle:

- organized factual inputs for professional review
- panel, load, equipment, pathway, design, and source-document context
- field-level and domain-level provenance where available
- assumptions, inferred fields, unknowns, limitations, and derived-output lineage
- planning outputs only as non-authoritative context

Must exclude by default:

- language implying the system has performed engineering review
- unproven compliance claims, AHJ approval, permit readiness, or utility approval
- hidden assumptions or advisory prose presented as fact
- operational-control, dispatch, or DERMS semantics

### Utility View

Utility views are deferred.

May see in principle after Matt-approved design:

- minimized service/site identity and source-linked utility-relevant facts
- service context, interconnection context, equipment facts, and aggregate load context only when permissioned and sourced
- provenance, revision identity, export purpose, and limitation metadata

Must exclude by default:

- broad homeowner planning notes, household appliance detail, AI advisory text, contractor notes, and unrelated product specs
- tariff authority, incentive eligibility, savings claims, utility approval, interconnection approval, submission authority, or program enrollment claims
- operational dispatch, DERMS, aggregator enrollment, device-control, or availability semantics
- raw utility account data unless explicitly authorized and governed

### AI Agent View

May see in principle:

- minimized structured context needed to explain, summarize, compare, organize, or coordinate
- stable object identity, source-linked facts, provenance summaries, rule keys, missing inputs, assumptions, and limitations
- derived outputs separated from recorded facts and advisory text
- grounding warnings that AI cannot create canonical facts

Must exclude by default:

- broad raw object dumps when summarized context is sufficient
- unrelated account/private records, permission grants outside scope, utility secrets, raw operational-control data, and hidden prompt-only facts
- write authority, canonical fact promotion, permission creation, verification claims, or professional/utility approval claims
- generated prose as a source of truth

## Provenance Inside Permissioned Views

Every future permissioned view should carry provenance at the narrowest useful level:

- field-level provenance for authority-bearing fields
- domain-level provenance summaries for quick trust posture
- derived-output provenance for recommendations, comparisons, takeoffs, AI grounding, and planning scores
- source-document identity when a fact or product spec depends on a document
- rule keys when deterministic outputs are exposed
- confidence, trust state, data origin, authority layer, data classification, and limitation metadata

If provenance is missing or partial, the view should say so rather than filling the gap with confident prose.

## Unknowns, Assumptions, Inference, And Derived Outputs

Permissioned views should preserve these labels:

- Unknown: missing or unavailable information.
- Assumption: declared, estimated, or planning-stage value that needs confirmation.
- Inferred: plausible but unverified interpretation from incomplete evidence.
- Placeholder/demo: non-authoritative continuity or demonstration data.
- Derived: deterministic or advisory output downstream of source records and rules.
- Advisory: explanatory text that cannot create canonical facts.

Views should not collapse these labels into a single "ready" status. Missing information should remain visible to every audience that may act on the view.

## Design Rules

- Do not filter existing broad endpoints and call the result permissioned.
- Do not use account role, plan, subscription, endpoint access, or UI visibility as a permission grant.
- Do not expose derived intelligence without source inputs, rule keys or lineage, confidence, missing inputs, assumptions, and limitations.
- Do not let a view imply utility, engineering, code, financial, procurement, safety, or operational authority.
- Do not let AI-facing views scrape prose as canonical facts.
- Do not create utility-safe or operational-control views before their authority models exist.
- Prefer explicit named view contracts over ad hoc per-endpoint filtering.

## Decisions Requiring Matt Approval Before Implementation

Matt approval is required before any of the following:

- Creating permission grants, permission scopes, consent artifacts, revocation state, audit events, or export authorization.
- Creating, changing, or enforcing permissioned view contracts in schema, APIs, services, or frontend workflows.
- Mapping account roles, subscriptions, users, contractors, engineers, utilities, or AI agents to view access.
- Implementing auth, RBAC, ABAC, tenant isolation, session policy, privacy policy, or permission enforcement.
- Narrowing or reclassifying existing `/api/*` contracts as permissioned twin APIs.
- Defining data classification, provenance completeness, authority-layer, trust-zone, or field-redaction policy as implementation behavior.
- Creating utility-facing, interconnection, tariff, program, DERMS, dispatch, aggregator, device-control, or operational-control semantics.
- Treating this planning note as approval for implementation.

## Sources / Provenance

- `AGENTS.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/API_CONTRACTS.md`
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- `docs/provenance/RESIDENTIAL_ENERGY_TWIN_PROVENANCE_POLICY_PLANNING.md`
- `docs/architecture/RESIDENTIAL_ENERGY_TWIN_CONTRACT_V1.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`

## Summary

The first Residential Energy Twin permissioned view boundary should be a set of design-only named view contracts that preserve provenance, unknowns, assumptions, inference labels, and derived-output limits. Existing broad planner APIs remain compatibility surfaces, not permissioned twin APIs. Any enforcement, API, schema, permission, utility, or operational-control implementation requires explicit Matt approval.
