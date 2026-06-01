# Residential Energy Twin Provenance Policy Planning Note

Status: design-only provenance policy planning note
Date: 2026-06-01
Implementation status: no schema, migration, API, runtime, permission-enforcement, auth, utility authority, operational-control, or canonical `ResidentialEnergyTwin` model change is approved or implied

## Purpose

This note plans the provenance policy needed before Residential Energy Twin facts can carry stronger authority.

It does not implement provenance enforcement, define final policy, create required fields, change trust-state semantics, or approve a canonical twin model. Matt approval is required before any provenance policy becomes schema, API, runtime behavior, enforcement behavior, or project direction.

## Authority-Bearing Twin Facts

An authority-bearing twin fact is any recorded fact that a future system, view, or workflow may rely on to make a stronger claim than "recorded planning input."

Examples:

- premise identity, address, service size, or utility provider when used outside the homeowner planning workspace
- building, panel, load, equipment, pathway, or design fields used in contractor, engineer, utility, AI, or orchestration views
- equipment product specifications, documentation links, model numbers, and compatibility-relevant attributes
- electrical facts used to support panel/service posture, load interpretation, backup design direction, or professional review packets
- utility relationship facts, interconnection context, territory context, tariff context, or program context
- permission grants, consent artifacts, revocation state, export scope, or audience-specific view authorization
- derived outputs that become persisted, versioned, exported, or used as input to another decision-support layer

Authority-bearing does not mean verified, compliant, approved, permitted, safe, eligible, payable, dispatchable, or professionally reviewed. It means the fact needs explicit lineage before the system can responsibly let another workflow depend on it.

## Proposed Minimum Provenance Requirements

Future authority-bearing facts should identify:

- source object or source document identity
- source type, such as homeowner declaration, imported record, product document, field observation, utility document, internal rule, or calculation
- data origin, such as demo seed, user-created, imported, verified, placeholder, or derived estimate
- trust state and confidence level
- verification status and verification timestamp when available
- value snapshot or enough change context to understand what was sourced
- field name or domain segment covered by the provenance record
- missing inputs and unknowns that limit authority
- assumptions used to interpret the fact
- authority layer, such as recorded planning fact, documented fact, verified fact, derived estimate, advisory explanation, historical snapshot, or future operational state
- limitation text that prevents overclaiming

Facts without this minimum should remain visible as recorded, incomplete, inferred, placeholder, demo, or unknown rather than being promoted into stronger authority.

## Provenance Levels

### Field-Level Provenance

Field-level provenance links one important field on one entity to its source basis.

Use when:

- a field may affect engineering, contractor, utility, permission, product, or AI-facing interpretation
- a source document supports only part of a record
- a field may be stale, inferred, placeholder, or manually overridden

Examples:

- `electrical_panel.amperage`
- `home.service_size`
- `equipment_product.specs`
- `estimated_pathway.estimated_distance_ft`
- `load.running_watts`
- future permission grant scope, status, or revocation state

Current support:

- `data_provenance.entity_type`
- `data_provenance.entity_id`
- `data_provenance.field_name`
- `data_provenance.source_document_id`
- `data_provenance.source_type`
- `data_provenance.trust_state`
- `data_provenance.value_snapshot`
- `data_provenance.confidence_level`
- `data_provenance.verified_at`

Current gap:

Field-level coverage is partial and not enforced. Many important fields have `data_origin` but no explicit `data_provenance` row.

### Domain-Level Provenance

Domain-level provenance summarizes whether a twin domain has enough source coverage for a given use.

Use when:

- a view needs to show whether a domain is source-backed, partial, stale, or unknown
- a contractor, engineer, utility, AI, or homeowner workflow needs a quick trust posture
- a future twin context view needs to distinguish recorded coverage from authority

Examples:

- premise provenance
- electrical infrastructure provenance
- equipment provenance
- pathway provenance
- scenario provenance
- utility relationship provenance
- permission provenance

Current support:

- `ProvenanceSummary` derived from `DataProvenance` and `SourceDocument`
- summary fields for source types, trust states, confidence levels, verification statuses, source documents, unverified fields, notes, and limitations

Current gap:

Domain-level summaries are derived metadata. They do not prove correctness, enforce completeness, authorize access, or create a canonical twin. They also depend on field-level rows that may be missing.

### Derived-Output Provenance

Derived-output provenance explains how deterministic or advisory outputs were produced.

Use when:

- outputs summarize, rank, size, compare, recommend, warn, or generate planning guidance
- a derived output may be persisted, exported, shown to AI, or used by another calculation
- a generated output could be mistaken for a source fact

Examples:

- advisor recommendations
- battery and solar planning ranges
- panel/service posture
- inverter/system architecture posture
- backup-load selection
- compatibility issues
- scenario comparison rankings
- transient takeoffs
- AI grounding summaries

Current support:

- `rule_provenance.rule_key`
- `rule_provenance.rule_name`
- `rule_provenance.source_type`
- `rule_provenance.source_document_id`
- `rule_provenance.trust_state`
- deterministic provenance builders in `apps/api/app/services/provenance.py`
- additive authority-layer, data-classification, derivation-type, limitation, input-signal, missing-input, and confidence metadata on selected outputs

Current gap:

Derived-output provenance is not uniformly versioned, field-complete, replayable, or enforced across all outputs. Full advisor payload replay is not persisted for revisions. Transient takeoffs are not versioned.

## Current Structure To Twin Domain Mapping

| Twin domain | Current provenance structure | Coverage posture |
| --- | --- | --- |
| Premise | `Home.data_origin`; possible `DataProvenance` by `entity_type` and `field_name`; `SourceDocument` where linked | Partial. Address, service size, and utility provider fields are not guaranteed source-backed. |
| Buildings | `BuildingStructure.data_origin`; possible field provenance | Partial. Structure type and distance may be assumptions unless explicitly sourced. |
| Electrical infrastructure | `ElectricalPanel.data_origin`; possible field provenance; derived advisor provenance for panel/service posture | Partial. Recorded panel data is not NEC, AHJ, utility, or engineering authority. |
| Loads | `Load.data_origin`; load provenance summaries on selected responses; possible field provenance | Partial. Runtime, demand, circuit mapping, and criticality may be estimated or declared. |
| Equipment | `EquipmentProduct.data_origin`; `SourceDocument`; `DataProvenance`; product provenance summaries | Stronger than some domains where source documents exist, but not complete. Product specs without source linkage remain limited authority. |
| Designs | `EnergySystemDesign.data_origin`; `DesignEquipment.data_origin`; rule provenance for derived design guidance | Partial. Design records are planning state, not final engineering design. |
| Pathways | `EstimatedPathway.data_origin`; pathway provenance summaries on selected responses | Partial. Distance, difficulty, visibility, and cost/savings placeholders are not field-verified unless sourced. |
| Scenarios | `Scenario.data_origin`; `ScenarioRevision.data_origin`; comparison lineage summaries | Partial. Revisions preserve compact history, not full replayable twin state. |
| Permissions | No implemented permission grant, consent artifact, or revocation model | Missing. Account role and subscription fields are not permission provenance. |
| Utility relationships | Utility provider/service fields on `Home`; no utility relationship authority model | Missing or partial. No tariff, interconnection, service-territory, or utility export authority exists. |
| Derived intelligence | `RuleProvenance`; deterministic provenance metadata; inspectability payloads | Partial. Good planning lineage exists on selected outputs, but no universal derived-output provenance policy is enforced. |

## Unknowns And Partial Areas

- Field-level provenance is not exhaustive.
- Domain-level provenance completeness thresholds are not defined.
- Required provenance differs by audience and use case, but scoped view contracts are not implemented.
- Permission provenance does not exist because permission grants, consent artifacts, and revocation state are not implemented.
- Utility provenance is not sufficient for utility authority, tariff authority, interconnection authority, or utility-facing export behavior.
- Professional review provenance is not implemented for engineer, electrician, AHJ, or permitting authority.
- Product-source freshness, conflict handling, and stale-document policy are not finalized.
- Historical lineage is partial; scenario revisions are compact snapshots, not full twin revisions.
- AI grounding provenance is descriptive and advisory; AI cannot create canonical facts.
- Data classification metadata is descriptive and not enforced as RBAC, tenant isolation, export authorization, or privacy policy.

## Planning Rules For Future Design

- If a fact lacks provenance, expose the gap instead of hiding it.
- If a source supports only one field, do not let it certify the whole record.
- If a derived output is persisted or exported, preserve source inputs, rule keys, assumptions, missing inputs, confidence, generated timestamp, and limitations.
- If a field is inferred, keep it distinguishable from declared, documented, imported, verified, and demo data.
- If a fact will enter contractor, engineer, utility, AI, supplier, manufacturer, aggregator, or operational workflows, define the required provenance before implementation.
- If provenance conflicts, surface the conflict rather than silently choosing a winner.
- If provenance cannot support a stronger claim, downgrade the claim to planning-only.

## Decisions Requiring Matt Approval Before Implementation

Matt approval is required before any of the following:

- Defining mandatory provenance fields or completeness thresholds for Residential Energy Twin domains.
- Changing schema, migrations, persistence contracts, or canonical data models for provenance.
- Creating twin-level, domain-level, field-level, permission-level, utility-level, or derived-output provenance enforcement.
- Defining trust-state semantics, authority-layer semantics, confidence semantics, or verification-status semantics as implementation policy.
- Promoting any derived output into canonical persisted twin data.
- Creating permission grants, consent artifacts, revocation provenance, audit policy, or export authorization.
- Creating utility provenance, tariff provenance, interconnection provenance, utility-facing exports, DERMS, dispatch, or operational-control provenance.
- Changing existing `/api/*` contracts or creating scoped provenance view contracts.
- Treating this planning note as approval for implementation.

## Sources / Provenance

- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `docs/DATABASE_SCHEMA.md`
- `apps/api/app/core/models.py`
- `apps/api/app/provenance/schemas.py`
- `apps/api/app/services/provenance.py`

## Summary

Residential Energy Twin provenance should make authority explicit at the field, domain, and derived-output levels before facts are used outside planning context. Existing structures provide a useful partial foundation, but field coverage, permission provenance, utility authority, enforcement, and canonical twin provenance remain unimplemented and require Matt approval before code changes.
