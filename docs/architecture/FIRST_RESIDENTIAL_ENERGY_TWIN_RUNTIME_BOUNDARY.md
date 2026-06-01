# First Residential Energy Twin Runtime Boundary Planning Note

Status: design-only planning note
Date: 2026-06-01
Implementation status: no schema, migration, API, runtime, permission-enforcement, auth, or canonical model change is approved or implied

## Purpose

This note plans the first possible runtime boundary for the Residential Energy Twin without implementing it.

Primary question:

Should current planner runtime work temporarily use `home_id` as the Residential Energy Twin identity, or should a future `twin_id` be introduced before any runtime boundary exists?

## Current Context

The current planner runtime already uses `home_id` as the shared premise anchor for most persisted planning records. The Residential Energy Twin Contract v1 defines a future canonical aggregate where:

- `twin_id` is the durable aggregate identity.
- `home_id` anchors the twin to the residential premise.
- Applications consume the twin but do not become sources of truth.
- Existing broad `/api/*` contracts remain compatibility-sensitive application contracts.

No current model, table, route, or service is a canonical `ResidentialEnergyTwin` implementation.

## Existing Planner Entities That Map To Twin Domains

| Twin domain | Current planner entities | Current posture |
| --- | --- | --- |
| Home / premise | `Home`, nullable `Home.account_id`, address fields, service size, utility provider field | Persisted planning record and premise anchor. Not a full twin identity, utility authority, legal property record, or permission grant. |
| Buildings / structures | `BuildingStructure` linked by `home_id` | Persisted planning record for structures. Distances and notes remain planning assumptions unless sourced. |
| Panels / electrical infrastructure | `ElectricalPanel` linked by `home_id` and `building_id` | Persisted planning record for panel context. Not NEC compliance, engineering approval, AHJ approval, utility approval, or transfer-topology authority. |
| Loads | `Load` linked by `home_id` and `building_id`; `LoadTemplate` as reusable account/global template | Persisted planning records for modeled loads. Templates are reusable application/reference scaffolding, not recorded home facts until used to create loads. |
| Equipment | `EquipmentProduct`, `EquipmentLocation`, `DesignEquipment` | Product records and design assignments support planning. Product authority depends on source provenance; assignments are design composition records, not procurement or compatibility approval. |
| Designs | `EnergySystemDesign`, `CompatibilityIssue` | Designs are persisted planning records. Compatibility issues are derived/advisory planning outputs even when persisted. |
| Pathways | `EstimatedPathway` | Persisted pathway planning records. Route and distance fields are assumptions unless sourced; placeholder economics and resilience scores are derived/placeholders. |
| Scenarios | `Scenario`, `ScenarioRevision` | Scenario records and revision lineage are persisted planning history. Embedded snapshots preserve historical context but do not make derived advisor content canonical facts. |
| Provenance | `SourceDocument`, `DataProvenance`, `RuleProvenance`, provenance summaries | Source and rule lineage records exist. Coverage is partial and does not by itself enforce authority, access control, or verification. |

## Recorded Planner Inputs Versus Derived Or Application-Only

Current recorded planner inputs that can act as canonical planner records within the existing planner scope, but are not a canonical Residential Energy Twin implementation:

- Home/premise records and their direct home-linked structures.
- Building, panel, load, equipment-location, design, design-equipment, pathway, scenario, and scenario-revision records.
- Equipment product records when treated as reference/product data with visible provenance limits.
- Source-document, data-provenance, and rule-provenance records as lineage records.

Current derived, advisory, placeholder, or application-only data:

- Advisor summaries, recommendation profiles, reasoning graphs, backup-load selection, battery/solar sizing ranges, panel/service posture, inverter/system posture, architecture-fit signals, completeness scores, rankings, and comparison warnings.
- Compatibility issues and scenario-comparison outputs when generated from rules.
- Transient takeoffs and placeholder cost/savings/score fields.
- AI context payloads, generated explanations, UI layouts, sorted table state, and broad response shapes.
- Account role, plan, and subscription fields, which remain scaffolding and do not imply permission or authorization.

Derived outputs may be useful planning artifacts. They do not create canonical home facts or twin records unless a future Matt-approved source-backed promotion workflow exists.

## Option A: Use `home_id` As A Temporary Twin Boundary

Meaning:

Use existing `home_id` only as a temporary runtime grouping key for a first read/composition boundary over current planner records. Do not rename it to `twin_id`, expose it as canonical twin identity, or infer permission semantics from it.

Benefits:

- Matches current persistence: most twin-relevant records already link to `homes.id`.
- Avoids premature schema and migration work.
- Preserves current frontend and `/api/*` compatibility-sensitive contracts.
- Allows a future read-only twin-context composition service or document to be designed before changing persistence.
- Keeps the first boundary honest: premise-scoped planning context, not a fully implemented Residential Energy Twin aggregate.

Risks:

- Future code or docs could blur `home_id` and `twin_id`, making the premise anchor appear to be the durable aggregate identity.
- Permission, provenance, and utility boundaries could be incorrectly treated as already solved because records share a home anchor.
- Multi-owner, transferred-home, multi-premise, historical split/merge, or portfolio cases may outgrow a one-to-one `home_id` assumption.
- Developers could accidentally reclassify existing planner APIs as canonical twin APIs.
- Existing incomplete provenance could look stronger than it is if the boundary is named too confidently.

Required guardrails if Matt later approves implementation:

- Name the boundary as a temporary `home_id`-anchored planning boundary, not canonical `ResidentialEnergyTwin`.
- Keep it read-only/compositional until schema, permission, and provenance decisions are approved.
- Preserve authority labels separating recorded facts, derived estimates, advisory text, unknowns, and placeholders.
- Do not narrow or reclassify existing `/api/*` contracts.

## Option B: Introduce `twin_id` Before The First Runtime Boundary

Meaning:

Add or require a durable `twin_id` before composing current planner data as a twin boundary.

Benefits:

- Aligns directly with Residential Energy Twin Contract v1.
- Avoids later migration from premise identity to aggregate identity.
- Makes the twin's durable asset boundary explicit from the start.
- Better supports future cases where one premise anchor is not enough.

Risks:

- Requires schema, migration, persistence-contract, API-shape, and data-backfill decisions before the implementation problem is fully scoped.
- Could imply the canonical aggregate exists before permissions, provenance coverage, view contracts, and lifecycle semantics are ready.
- Could force premature decisions about ownership, account transfer, revocation, historical identity, utility relationship authority, and canonical domain membership.
- Could disrupt compatibility-sensitive planner workflows for an identity distinction that the first runtime slice may not need yet.
- Could create a partially implemented twin model that developers treat as more authoritative than it is.

## Recommendation

For the first implementation boundary, if Matt later approves code work, use `home_id` as a temporary planning-context anchor only.

Do not introduce `twin_id` yet. Reserve `twin_id` for a later approved canonical aggregate implementation after the team has explicit decisions for:

- canonical twin lifecycle and identity semantics
- permission grants, consent artifacts, and revocation state
- provenance requirements for authority-bearing fields
- scoped view contracts
- migration/backfill behavior
- compatibility expectations for existing `/api/*` consumers

The safest first boundary is a design for a read-only, source-labeled, `home_id`-anchored composition layer that gathers existing home, building, panel, load, equipment, design, pathway, scenario, and provenance records into a twin-context view without changing storage or contracts.

This boundary should be described as "Residential Energy Twin planning context" or "home energy planning context" until `twin_id` exists and Matt approves canonical aggregate implementation.

## First Implementation Boundary To Design Next

Design only, not approved implementation:

1. Compose existing planner records by `home_id`.
2. Classify each included field or object as recorded planning fact, source-backed fact, derived output, advisory text, placeholder, or unknown.
3. Attach provenance summaries where available and explicit "provenance missing" status where not available.
4. Exclude permission grants, utility authority, operational control, and canonical write workflows until those domains are approved.
5. Keep current broad `/api/*` contracts unchanged; if an API is later approved, make it additive and clearly labeled as a planning-context view.
6. Preserve AI limits: AI may consume the context for explanation and orchestration, but it cannot create canonical facts or permission grants.

## Decisions Requiring Matt Approval Before Code Changes

Matt approval is required before any of the following:

- Treating `home_id` as a temporary runtime twin identity in code.
- Introducing `twin_id` in schema, APIs, services, docs as implemented direction, or generated data.
- Creating a `ResidentialEnergyTwin` model, table, API, service, view, or canonical repository boundary.
- Changing schema, migrations, persistence contracts, or canonical data models.
- Changing existing `/api/*` contracts or reclassifying them as canonical twin APIs.
- Implementing permission grants, consent artifacts, revocation semantics, homeowner authorization, RBAC, ABAC, tenant isolation, or export authorization.
- Defining provenance policy, field-level provenance requirements, trust-state semantics, or audit policy.
- Promoting derived advisor, comparison, takeoff, AI, compatibility, or recommendation outputs into canonical facts.
- Defining utility relationship authority, utility-facing export behavior, interconnection authority, tariff authority, DERMS, dispatch, or operational-control semantics.

## Sources / Provenance

- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `docs/architecture/RESIDENTIAL_ENERGY_TWIN_CONTRACT_V1.md`
- `docs/ARCHITECTURE.md`
- `docs/DATABASE_SCHEMA.md`
- `docs/API_CONTRACTS.md`
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/governance/AI_AUTHORITY_LIMITS.md`
- `apps/api/app/core/models.py`
- `apps/api/app/services/design_analysis.py`
- `apps/api/app/services/design_completeness.py`
- `apps/api/app/services/design_advisor.py`
- `apps/api/app/services/provenance.py`

## Summary

`home_id` is the pragmatic temporary anchor for the first Residential Energy Twin runtime boundary design, but only as a premise-scoped planning-context grouping key. `twin_id` should remain a future durable aggregate identity until Matt approves the schema, migration, permission, provenance, API, and lifecycle decisions needed to make it real.
