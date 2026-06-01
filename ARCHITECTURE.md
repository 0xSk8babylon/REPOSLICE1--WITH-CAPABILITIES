# Architectural Purpose

Document role: structure. `VISION.md` defines principles. `PROJECT_MAP.md` documents current reality. `MARKET_POSITIONING.md` defines the external narrative. `ECOSYSTEM_MAP.md` defines ecosystem relationships.

This document describes the architecture bridge between the current residential energy planner implementation and the future Residential Energy Twin vision.

The Planner is the first application. It is the current user-facing surface for capturing home facts, planning assumptions, equipment choices, pathways, scenarios, takeoffs, advisor outputs, and provenance summaries.

The Residential Energy Twin is the durable asset and durable source of truth. It should persist beyond any one planner screen, advisor view, contractor workflow, utility view, or future application.

Permission is a first-class domain inside the Residential Energy Twin. The Permission Layer governs access to twin views: who may see which parts of the twin, for what purpose, and under what limits. Permission does not exist outside the twin. In the current implementation, permission is represented as scaffolding and readiness metadata, not enforced access control.

External Applications are consumers of the twin. Contractor tools, utility views, aggregator workflows, supplier tools, homeowner interfaces, and AI agents should consume permissioned views of the same underlying twin instead of becoming separate sources of truth.

# Architectural Principles

- The Residential Energy Twin is canonical and is the durable asset.
- Applications are consumers.
- Truth beats inference.
- Provenance is required.
- Permission is a first-class domain inside the Residential Energy Twin.
- Structured facts outrank generated content.
- Homeowner ownership is preserved.

Structured facts may still be unverified, stale, demo-seeded, imported, or user-entered. Their authority depends on origin, provenance, confidence, and verification state. Generated content can explain, compare, summarize, or recommend, but it must not silently become canonical truth.

# Current Architecture

The current planner architecture is a monorepo planning platform with a backend service, persisted planning records, deterministic planning services, provenance primitives, broad advisor context, and a frontend planner interface.

Current planner architecture:

- `PROJECT_MAP.md` describes the system as a FastAPI/SQLite backend with React/Vite frontend, structured house data, product facts, rule-based compatibility logic, and AI-grounding/explanation layers.
- The current planner supports home/property facts, buildings, panels, loads, equipment locations, estimated pathways, designs, design equipment, scenarios, generated takeoffs, design advisor outputs, AI grounding context, and provenance summaries.
- The planner is not currently a final engineering, NEC-compliance, permitting, utility-approval, pricing-authority, or operational-dispatch system.

Current persisted entities:

- `Account`
- `Home`
- `BuildingStructure`
- `ElectricalPanel`
- `Load`
- `EquipmentLocation`
- `EnergySystemDesign`
- `DesignEquipment`
- `EquipmentProduct`
- `Scenario`
- `ScenarioRevision`
- `EstimatedPathway`
- `TakeoffRequest`
- `TakeoffLineItem`
- `LoadTemplate`
- `DesignGoalPreset`
- `SourceDocument`
- `DataProvenance`
- `RuleProvenance`
- `CompatibilityIssue`

Current trust boundaries:

- Persisted planning records are the current system of record for the planner, but they are not automatically verified site truth.
- Product records can include placeholder or unverified references, so product facts require provenance.
- Electrical outputs are planning heuristics and advisor signals, not NEC compliance, stamped engineering, AHJ approval, or utility approval.
- Cost, savings, scenario scores, and takeoff values may be placeholders or planning estimates rather than bids, procurement-ready numbers, or financial guarantees.
- Permission and consent are currently scaffolding and metadata, not enforced runtime access boundaries.
- AI grounding and advisor outputs are derived and advisory. They do not create canonical facts.

Current advisor boundaries:

- Advisor outputs consume structured planner records, deterministic service outputs, compatibility signals, provenance summaries, rule provenance, and trust metadata.
- Advisor outputs are generated at request time and are not the canonical source of home facts.
- The broad AI context endpoint is described as grounding context, not a narrowed permission-enforced view.
- Advisor outputs must remain subordinate to structured facts, provenance, professional review, utility authority, and homeowner permission.

# Twin Architecture

The twin architecture is organized around durable home energy domains. Each domain may have current planner records, derived views, missing data, and future permissioned consumers. The twin should preserve the difference between structured facts, derived facts, inferred facts, verified facts, and unknown facts.

## Premise

Purpose: Anchor the Residential Energy Twin to the home, account relationship, address context, utility relationship, service context, and planning history.

Ownership: Twin Agent primary; Backend Agent and Permission / Consent Agent supporting.

Source of Truth: Current planner source is `Home`, with account linkage through `Account` where present. Future canonical truth belongs in the twin, with provenance and homeowner permission boundaries.

Dependencies: Buildings, electrical infrastructure, loads, equipment, designs, scenarios, permissions, provenance, utility relationships, homeowner views, contractor views, utility views, and AI views depend on premise identity.

## Buildings

Purpose: Represent structures that affect energy planning, including the main home, detached structures, ADUs, workshops, garages, barns, and other energy-relevant buildings.

Ownership: Twin Agent primary; Backend Agent and Frontend Agent supporting.

Source of Truth: Current planner source is `BuildingStructure`.

Dependencies: Loads, equipment locations, pathways, scenarios, takeoffs, advisor outputs, contractor views, and utility-facing context can depend on building records.

## Electrical Infrastructure

Purpose: Represent panels, service context, distribution assumptions, backup panel context, panel roles, and electrical planning constraints.

Ownership: NEC / Electrical Logic Agent primary; Twin Agent, Backend Agent, QA / Testing Agent, and Security / Audit / Provenance Agent supporting.

Source of Truth: Current planner sources are `ElectricalPanel`, related `Home` service fields, `Load`, design records, equipment assignments, and derived electrical planning services. These are planning records and do not constitute engineering approval.

Dependencies: Loads, equipment, designs, scenarios, takeoffs, advisor outputs, contractor views, engineer review context, utility views, and AI views depend on electrical infrastructure facts and assumptions.

## Loads

Purpose: Represent energy uses, backup priorities, criticality, planning assumptions, and load behavior relevant to resilience, electrification, backup, design comparison, and feasibility signals.

Ownership: Twin Agent primary; NEC / Electrical Logic Agent and Backend Agent supporting.

Source of Truth: Current planner source is `Load`, with load templates represented by `LoadTemplate`. Derived load summaries are downstream outputs and not canonical facts.

Dependencies: Electrical feasibility, backup planning, scenarios, takeoffs, advisor outputs, contractor views, engineer review context, and AI views depend on load records.

## Equipment

Purpose: Represent product identity, type, role, quantity, location, ecosystem, specification assumptions, documentation, and source provenance for energy-related equipment.

Ownership: Equipment Agent primary; Twin Agent, Backend Agent, Frontend Agent, and Security / Audit / Provenance Agent supporting.

Source of Truth: Current planner sources are `EquipmentProduct`, `DesignEquipment`, `EquipmentLocation`, `SourceDocument`, and `DataProvenance`. Product specs require provenance and may be placeholder, inferred, imported, or verified depending on source.

Dependencies: Designs, scenarios, takeoffs, compatibility, advisor outputs, contractor views, supplier views, manufacturer context, and AI views depend on equipment records.

## Designs

Purpose: Represent proposed or current system designs, architecture intent, equipment assignments, status, design goals, and planning composition.

Ownership: Twin Agent primary; Product Orchestrator, Backend Agent, Equipment Agent, and NEC / Electrical Logic Agent supporting.

Source of Truth: Current planner sources are `EnergySystemDesign` and `DesignEquipment`, with linked products, locations, pathways, loads, and provenance.

Dependencies: Electrical feasibility, equipment, scenarios, takeoffs, advisor outputs, homeowner views, contractor views, engineer review context, utility context, and AI views depend on design records.

## Scenarios

Purpose: Represent possible planning futures, tradeoffs, statuses, goals, costs, scores, warnings, and planning history without treating every scenario as complete, verified, approved, or final.

Ownership: Product Orchestrator primary; Twin Agent, Backend Agent, Frontend Agent, and Security / Audit / Provenance Agent supporting.

Source of Truth: Current planner sources are `Scenario` for live scenario state and `ScenarioRevision` for compact historical lineage. Placeholder scores and costs are not authoritative.

Dependencies: Advisor outputs, comparison views, homeowner planning, contractor context, takeoff framing, provenance, and AI views depend on scenario records.

## Pathways

Purpose: Represent physical or logical routing assumptions between buildings, equipment, panels, and future upgrades, including route type, distance assumptions, trenching, conduit, visibility, and confidence.

Ownership: Twin Agent primary; Takeoff / Estimating Agent, Backend Agent, and Frontend Agent supporting.

Source of Truth: Current planner source is `EstimatedPathway`. Pathway records are planning assumptions unless verified by documentation or field validation.

Dependencies: Designs, scenarios, takeoffs, install complexity, contractor views, homeowner planning, and advisor outputs depend on pathways.

## Permissions

Purpose: Represent who can see, use, export, or act on parts of the twin, for what audience, purpose, duration, and scope.

Ownership: Permission / Consent Agent primary; Security / Audit / Provenance Agent, Backend Agent, Frontend Agent, and Product Orchestrator supporting.

Source of Truth: Current planner sources are account role and permission-readiness metadata only. No dedicated enforced consent record was identified in `PROJECT_MAP.md`. Permission is a first-class domain inside the Residential Energy Twin. The Permission Layer governs access to twin views. Permission does not exist outside the twin.

Dependencies: Contractor views, utility views, AI views, aggregator views, supplier views, external application access, audit, provenance, and homeowner governance depend on permission state.

## Provenance

Purpose: Represent where information came from, how it was derived, what confidence it carries, what assumptions were used, what is missing, and which authority layer applies.

Ownership: Security / Audit / Provenance Agent primary; Twin Agent, Equipment Agent, Backend Agent, Documentation Agent, and QA / Testing Agent supporting.

Source of Truth: Current planner sources are `SourceDocument`, `DataProvenance`, `RuleProvenance`, provenance summaries, inspectability metadata, data origin fields, and trust metadata. Coverage is partial.

Dependencies: Equipment, loads, pathways, scenarios, takeoffs, advisor outputs, AI context, contractor views, utility views, homeowner review, and external consumers depend on provenance.

## Utility Relationships

Purpose: Represent provider relationships, service context, tariff or program context, interconnection state, grid-facing visibility, and utility approval boundaries when permissioned.

Ownership: Utility / Rate Agent primary; Permission / Consent Agent, Twin Agent, Backend Agent, and Security / Audit / Provenance Agent supporting.

Source of Truth: Current planner source is limited to home utility provider/service context and planning metadata. Utility approval, interconnection authority, tariff authority, and operational program state are not implemented as canonical authority in the current project map.

Dependencies: Permissioned utility views, scenarios, designs, advisor outputs, grid-edge context, aggregator participation, homeowner decisions, and AI views depend on utility relationship data.

# Permission Architecture

Permission is a first-class domain inside the Residential Energy Twin because the twin is valuable only if it can be shared safely and narrowly. The Permission Layer governs access to twin views. Permission does not exist outside the twin. Permission is not merely a screen, checkbox, or external policy. It is a structured part of the homeowner-governed record.

Consent: The homeowner's explicit authorization for a specific party, purpose, and use of twin information. Consent should be distinguishable from inferred interest, account role, or generic acceptance.

Visibility: The subset of twin data exposed to a consumer. Visibility should be scoped to the consumer's role and purpose.

Audience: The party receiving access, such as homeowner, contractor, engineer, utility, aggregator, supplier, manufacturer, AI agent, or other third party.

Scope: The facts, domains, documents, derived outputs, assumptions, or views included in a permission grant.

Duration: The time boundary for access. Permission may be temporary, project-specific, event-specific, or ongoing depending on homeowner authorization.

Revocation: The homeowner's ability to stop future access where practical. Historical records may still need to preserve completed work, audit evidence, or safety-relevant lineage.

Permission becomes part of the twin by linking access rights, visibility boundaries, consent state, audience, purpose, scope, duration, and revocation state to the same canonical home energy record. This keeps sharing decisions attached to the data they govern.

# Consumer Architecture

Future consumers should operate against the same twin with different views.

Homeowner: Sees the broadest owner view, including home facts, assumptions, planning history, missing data, permissions, provenance, scenarios, and advisor explanations.

Contractor: Sees scoped project context needed for scoping, estimating, site walks, equipment review, routes, assumptions, missing information, and project coordination.

Engineer: Sees organized factual inputs, assumptions, missing data, equipment information, electrical context, and provenance needed for professional review. The twin does not replace engineering authority.

Utility: Sees minimized, source-linked, permissioned service-relevant and grid-relevant facts. The twin does not replace utility authority.

Aggregator: Sees permissioned capability, constraints, availability, and participation context relevant to authorized programs. The twin does not imply dispatch authority by default.

Supplier: Sees scoped equipment, product, availability, compatibility, and documentation context needed for supplier workflows when authorized.

AI Agent: Sees permissioned, source-linked, bounded context needed to explain, organize, compare, and coordinate. AI does not own the twin and does not create canonical truth without an authorized source path.

The architectural rule is: same twin, different views. Each consumer receives the minimum useful view for its role, purpose, and permission scope.

# Capability Architecture

Capability describes what an asset, load, device, design, or home could technically do.

Permission describes what the homeowner has authorized others to see, use, coordinate, or act on.

Availability describes whether the capability is actually available for a specific use at a specific time or under a specific condition.

```text
Technical Capability
+
Customer Permission
+
Availability
=
Usable Grid Capacity
```

Technical capability alone is not usable grid capacity. A battery, EV, generator, thermostat, solar system, or flexible load becomes usable only when capability exists, customer permission exists, and availability exists. Willingness, backup priorities, comfort boundaries, outage needs, equipment state, program participation, and homeowner limits are part of the capacity model.

# External Ecosystem

DERMS: DERMS orchestrate assets. The twin defines assets. DERMS answer: "What can we dispatch right now?" The twin answers: "What exists, what is possible, what is permissioned, and what is trusted?" The boundary is that the twin is not a dispatch authority, and DERMS should not become the canonical home record.

HEMS: HEMS manage or optimize home energy behavior. The twin preserves premise truth, context, permissions, provenance, and planning history. The boundary is that HEMS can operate or optimize behavior, but the twin remains the homeowner-governed record.

Device Vendors: Device vendors know their products and device-specific capabilities. The twin places device facts in cross-vendor, homeowner-governed context. The boundary is that vendor records should not silently become the whole-home source of truth.

Utilities: Utilities operate grid infrastructure and retain utility authority. The twin can provide permissioned visibility into behind-the-meter context. The boundary is that the twin does not approve utility processes, and utilities do not own the whole homeowner record by default.

Smart Meters: Smart meters measure net energy behavior at the meter. The twin explains premise context behind that behavior. The boundary is that meter data can support inferred truth, but it does not by itself describe topology, intent, permissions, equipment relationships, or future plans.

Sense: Sense and similar monitoring systems infer device behavior from load signatures. The twin can preserve that as inferred truth when permissioned and labeled. The boundary is that load inference does not replace declared, documented, or verified truth.

Protocols: The protocol is the standardized representation and exchange model for Residential Energy Twin data. External energy protocols may structure communication across devices, programs, events, states, or markets. The twin defines homeowner-governed premise context and trust boundaries. The boundary is that external protocols may exchange energy information, but the twin remains the canonical residential energy record when homeowner permission allows participation.

# Canonical Twin Test

The test is:

"If this application disappeared tomorrow, would the twin still exist?"

If the answer is yes, the information likely belongs in the twin when it describes durable home energy truth, provenance, permissions, planning history, asset relationships, or homeowner-governed context.

If the answer is no, the information likely belongs in an application view, workflow state, temporary interaction, generated explanation, or consumer-specific presentation.

The planner must pass this test by treating the twin as the asset and the planner as the first application. Future contractor, utility, supplier, aggregator, homeowner, and AI applications should also pass this test.

# Long-Term Architecture

The long-term architecture is a multi-application ecosystem around one homeowner-governed Residential Energy Twin.

Many applications may exist:

- planner applications
- homeowner applications
- contractor applications
- engineer review views
- utility views
- aggregator views
- supplier views
- manufacturer views
- AI agents
- future ecosystem applications

One twin exists for the home.

Permissions govern access.

Provenance governs trust.

Applications enrich the twin by contributing structured facts, documented sources, verified updates, labeled assumptions, permission decisions, planning history, and derived outputs with traceable lineage.

Applications may come and go. The twin persists. The architecture is healthy when every application consumes the twin, enriches the twin within its authority, and avoids becoming a competing source of truth.
