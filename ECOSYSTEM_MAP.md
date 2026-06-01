# Purpose

Document role: ecosystem relationships. `VISION.md` defines principles. `PROJECT_MAP.md` documents current reality. `ARCHITECTURE.md` defines structure. `MARKET_POSITIONING.md` defines the external narrative.

The goal is not to replace every participant in the residential energy ecosystem.

The goal is to define where the Residential Energy Twin sits within that ecosystem: between the homeowner, the home's real energy assets, its Permission Layer, and the applications and organizations that need trusted residential energy context.

The company should complement many participants, compete with some claims of ownership, and integrate with ecosystem workflows when the homeowner permits it. The core boundary is simple: the homeowner remains the center, the twin remains canonical, and applications remain consumers.

# Ecosystem Model

```text
Homeowner
↓
Residential Energy Twin
  includes Permission as a first-class domain
↓
Permission Layer governing access to twin views
↓
Applications
↓
Grid Edge Ecosystem
```

## Homeowner

The homeowner owns the edge. The home is not just a meter, account, device fleet, proposal, job, or dispatch resource. It is a lived-in place with goals, constraints, comfort needs, backup priorities, privacy expectations, future plans, and consent boundaries.

## Residential Energy Twin

The Residential Energy Twin is the durable asset: the homeowner-governed record of the home's energy reality. It defines what exists, what is planned, what is possible, what is trusted, what is uncertain, what has provenance, and what still needs professional or utility approval.

## Permission Layer

Permission is a first-class domain inside the Residential Energy Twin. The Permission Layer governs access to twin views: who can see which parts of the twin, for what purpose, and under what limits. Permission does not exist outside the twin.

## Applications

Applications are views and workflows that consume the twin. They may help homeowners plan, contractors scope, utilities understand, suppliers package, manufacturers support, or AI agents explain. They should not become competing sources of truth.

## Grid Edge Ecosystem

The grid edge ecosystem includes utilities, DERMS, aggregators, device vendors, monitoring platforms, HEMS, contractors, proposal tools, permitting platforms, suppliers, manufacturers, AI agents, and energy protocols. Each participant has a role. The twin sits beneath those roles as the Customer-Permissioned Truth Layer.

# Relationship Framework

# DERMS

Examples include EnergyHub, AutoGrid, Uplight, Schneider DERMS, Oracle DERMS, and similar systems.

Key concept: DERMS orchestrate assets. The twin defines assets.

## What They Do

DERMS coordinate distributed energy resources for grid programs, demand response, monitoring, dispatch, aggregation, and operational planning.

## What We Do

We define residential asset context before orchestration: what exists, what is possible, what is permissioned, what is trusted, and what remains unknown.

## Overlap

Both care about distributed energy resources, flexible capacity, customer participation, availability, and grid-edge value.

## Complement

The twin can give DERMS better premise context before a home or device is treated as a dispatchable resource.

## Competition

We compete where DERMS providers try to own behind-the-meter asset identity, customer permission, or premise truth as a closed record.

## Strategic Boundary

DERMS answer: "What can we dispatch right now?"

The twin answers: "What exists, what is possible, what is permissioned, and what is trusted?"

DERMS should not become the canonical record of the home. The twin should not pretend to be a dispatch authority.

## Future Integration Potential

DERMS may consume permissioned twin context to better understand asset eligibility, customer constraints, availability, and trust state. DERMS may also contribute participation history or program context back to the twin when the homeowner permits it.

# Utilities

## What They Do

Utilities operate grid infrastructure, serve customers, manage service relationships, administer programs, review interconnections, and retain utility-side authority.

## What We Do

We create a homeowner-governed view of residential energy context that can be shared with utilities when the homeowner permits it.

## Overlap

Both care about service context, interconnection, resilience, grid impacts, program participation, customer energy behavior, and behind-the-meter change.

## Complement

Utilities know important grid-side and customer-account facts. The twin can complement that with permissioned premise context.

Utilities may know:

- net load
- meter behavior
- service account context
- service territory
- interconnection records
- program enrollment
- grid constraints

Utilities often do not know:

- panel constraints
- service constraints inside the home
- backup priorities
- future upgrade plans
- homeowner intent
- consent boundaries
- contractor verification
- equipment relationships
- topology
- multi-device interaction
- what the homeowner is willing to share

## Competition

We may compete with utility-owned customer data models when those models try to define the residential edge without homeowner custody or consent.

## Strategic Boundary

Utilities retain utility authority. The homeowner retains ownership of the twin. The twin does not approve utility processes, and utilities do not automatically own the whole home record.

## Future Integration Potential

Utilities may consume scoped, source-linked twin views for interconnection context, program design, resilience planning, grid-edge visibility, and customer support. Utilities may contribute utility-side facts when those facts are allowed and properly sourced.

# Aggregators

## What They Do

Aggregators combine many customer assets into demand response programs, virtual power plants, grid services, or market participation.

## What We Do

We define permissioned premise-level capability, constraints, trust, availability, and homeowner intent before assets are aggregated.

## Overlap

Both care about flexible capacity, participation, availability, asset eligibility, and customer value.

## Complement

The twin can help aggregators distinguish technical capability from usable capacity. Capability alone is not enough. Permission and availability determine whether an asset can participate.

## Competition

We may compete where aggregators try to own customer permission, premise truth, or the durable home energy record as part of enrollment.

## Strategic Boundary

Aggregators coordinate participation. The twin governs the customer's edge model and permissioned facts. The twin does not imply dispatch authority by default.

## Future Integration Potential

Aggregators may consume permissioned capability and availability context. They may contribute participation history, program constraints, and event outcomes back to the twin when authorized.

# Device Vendors

Examples include Tesla, Enphase, SolarEdge, SPAN, FranklinWH, Generac, and EG4.

Key concept: Vendors know devices. The twin knows the home.

## What They Do

Device vendors make and support batteries, inverters, EV chargers, generators, smart panels, gateways, controls, solar equipment, and related products.

## What We Do

We place device facts into whole-home context: homeowner goals, panels, loads, buildings, scenarios, pathways, permissions, provenance, and cross-device relationships.

## Overlap

Both care about product identity, capability, status, compatibility, support, and customer value.

## Complement

Device vendors can contribute product facts, documentation, capability signals, support context, and installed-equipment history to the twin when permissioned.

## Competition

We may compete where device vendors try to own the entire home energy relationship through a closed product ecosystem.

## Strategic Boundary

Vendors know their devices. The twin knows the home across devices, vendors, stakeholders, and time.

## Future Integration Potential

Device vendors may contribute source-backed product facts, installed-equipment context, warranty-relevant documentation, support history, and capability signals. The twin may provide vendors with permissioned context for better support and compatibility understanding.

# Monitoring Platforms

Examples include Sense, Emporia, and smart meter analytics.

Key concept: They infer behavior. The twin records capability, intent, permissions, and history.

## What They Do

Monitoring platforms observe or infer energy behavior from meters, sensors, devices, or load signatures.

## What We Do

We preserve the broader residential energy record: assets, goals, documents, plans, permissions, provenance, scenarios, constraints, and verified facts.

## Overlap

Both care about energy behavior, appliance understanding, load patterns, homeowner insight, and grid-edge visibility.

## Complement

Monitoring can contribute inferred signals. The twin can place those signals in context and prevent inference from becoming unearned certainty.

## Competition

We may compete where monitoring platforms expand from behavior insight into ownership of the full residential energy truth layer.

## Strategic Boundary

Monitoring sees behavior. The twin models capability, intent, provenance, permission, and history.

## Future Integration Potential

Monitoring platforms may contribute inferred truth when permissioned and labeled. The twin may provide planning and asset context that helps interpret observed behavior.

# HEMS

Examples include energy management systems, agentic HEMS, and optimization systems.

Key concept: HEMS optimize behavior. The twin preserves truth.

## What They Do

HEMS manage, automate, or optimize energy behavior inside the home across devices, schedules, comfort, storage, generation, charging, and load control.

## What We Do

We preserve the homeowner-governed truth layer that describes assets, constraints, goals, permissions, provenance, scenarios, and planning history.

## Overlap

Both care about home energy assets, behavior, optimization potential, constraints, comfort, and customer outcomes.

## Complement

HEMS can make better decisions when grounded in accurate twin context. The twin can benefit from HEMS observations when those observations are permissioned and labeled.

## Competition

We may compete where HEMS providers try to become the full system of record for the home rather than an operating layer.

## Strategic Boundary

HEMS optimize behavior. The twin preserves truth. HEMS should consume the twin, not replace it.

## Future Integration Potential

HEMS may consume permissioned asset, constraint, and preference context. They may contribute operational history, status patterns, and optimization outcomes back to the twin when authorized.

# Contractor Software

Examples include CRM, proposal software, and project management systems.

Key concept: Contractor software manages projects. The twin manages residential energy truth.

## What They Do

Contractor software manages leads, customers, estimates, proposals, site visits, jobs, crews, documents, and project workflows.

## What We Do

We preserve the homeowner-governed home energy record that contractors can consume through scoped visibility.

## Overlap

Both care about site facts, customer goals, project context, equipment, estimates, documents, and coordination.

## Complement

Contractor tools can work from better structured context instead of recreating the home model for every job.

## Competition

We may compete where contractor platforms try to make the contractor's project record the canonical home energy record.

## Strategic Boundary

Contractor software manages contractor operations. The twin remains the homeowner-governed record.

## Future Integration Potential

Contractor systems may consume scoped twin context for site walks, scoping, estimates, and project coordination. Contractors may contribute field notes, documentation, and verified updates when the homeowner permits it.

# Proposal Platforms

Examples include Aurora, OpenSolar, and proposal systems.

Key concept: Proposals are views. The twin is the record.

## What They Do

Proposal platforms create customer-facing offers, savings narratives, system layouts, equipment packages, financing views, and sales materials.

## What We Do

We define the underlying home energy context before a proposal is created and preserve it after a proposal changes or disappears.

## Overlap

Both care about customer understanding, options, equipment, cost framing, decision support, and project feasibility.

## Complement

Proposal tools can become more honest and reusable when grounded in a permissioned twin with clear assumptions and provenance.

## Competition

We may compete where proposal platforms position the proposal as the durable record of the home.

## Strategic Boundary

A proposal is a view. The twin is the record. A proposal should not silently become canonical truth.

## Future Integration Potential

Proposal platforms may consume twin context to reduce repeated discovery and improve assumption clarity. Accepted, rejected, or revised proposal facts may enrich the twin when properly sourced and permissioned.

# Permitting Platforms

## What They Do

Permitting platforms organize permit applications, forms, plan sets, jurisdictional requirements, submissions, and approval workflows.

## What We Do

We organize planning context, documented evidence, assumptions, and permissioned facts that may support professional and jurisdictional workflows.

## Overlap

Both care about structured project information, equipment, site facts, documentation, and approval boundaries.

## Complement

The twin can provide cleaner context before permitting workflows begin and can preserve permit-related records after the workflow ends.

## Competition

We do not compete as an AHJ, permit authority, stamped plan system, or permit approval platform.

## Strategic Boundary

Permits are approvals. The twin is context. The twin does not grant permits.

## Future Integration Potential

Permitting platforms may consume scoped twin context and contribute submitted, approved, rejected, or revised permit artifacts back to the twin when authorized.

# Suppliers

## What They Do

Suppliers provide equipment, parts, packages, availability signals, purchasing channels, and relationships with contractors or installers.

## What We Do

We preserve the home context that can make supplier recommendations, equipment packaging, and inventory alignment more relevant when the homeowner permits sharing.

## Overlap

Both care about equipment fit, product availability, project scope, compatibility, and installer needs.

## Complement

Suppliers can use permissioned twin data to understand likely equipment needs, package products more intelligently, support preferred installer networks, and reduce mismatch between project intent and available inventory.

## Competition

We may compete where suppliers try to own the home energy record as a sales channel instead of contributing to a homeowner-governed model.

## Strategic Boundary

Suppliers support equipment fulfillment and packaging. The twin governs residential energy truth and homeowner permission.

## Future Integration Potential

Suppliers may contribute availability, packaging, substitution, and documentation context. They may consume scoped project needs to align inventory, bundles, and installer support.

# Manufacturers

## What They Do

Manufacturers create equipment, publish product facts, support installations, manage warranties, and define product capabilities.

## What We Do

We attach manufacturer facts to the home context with provenance, permissions, and cross-device relationships.

## Overlap

Both care about product identity, specifications, support, compatibility, installation context, and customer outcomes.

## Complement

Manufacturers can contribute source-backed product facts and support context. The twin can help manufacturers understand how products fit into real residential systems when the homeowner permits it.

## Competition

We may compete where manufacturers try to make their product account the whole-home energy record.

## Strategic Boundary

Manufacturers are authoritative for their product claims when properly sourced. The twin is authoritative for the homeowner-governed home energy context.

## Future Integration Potential

Manufacturers may contribute product documentation, compatibility notes, warranty context, lifecycle information, and support records. Provenance matters because product facts without source history can become unsafe or stale.

# AI Agents

Examples include Homeowner Agent, Contractor Agent, Utility Agent, and Planning Agent.

Key concept: AI consumes the twin. AI does not become the twin.

## What They Do

AI agents explain, summarize, organize, compare, coordinate, and help participants ask better questions.

## What We Do

We provide permissioned, source-linked, structured residential energy context that AI agents can consume without becoming the source of truth.

## Overlap

Both care about interpretation, planning support, decision support, coordination, and user understanding.

## Complement

AI agents become more useful when grounded in the twin's structured facts, provenance, permissions, assumptions, and unknowns.

## Competition

We may compete with prompt-only memory systems or assistant-owned records that try to become the canonical home energy truth layer.

## Strategic Boundary

AI is advisory unless explicitly authorized for a specific workflow. AI should not create canonical truth without a verified source path.

## Future Integration Potential

Homeowner agents may help explain tradeoffs and permission choices. Contractor agents may organize scoped project context. Utility agents may consume minimized grid-edge views. Planning agents may compare scenarios and surface assumptions while keeping the twin canonical.

# Energy Protocols

Examples include OpenADR, IEEE 2030.5, OCPP, and future protocols.

Key concept: Protocols move information. The twin defines information.

## What They Do

Energy protocols structure communication across devices, programs, events, states, markets, chargers, distributed resources, and grid participants.

## What We Do

We define homeowner-governed premise context: assets, relationships, permissions, provenance, scenarios, constraints, and trusted visibility.

## Overlap

Both care about structured energy information, interoperability, coordination, and participation.

## Complement

Protocols can move or reference energy information. The twin can define the trusted, permissioned home context behind that information.

## Competition

We may compete where a protocol or protocol-based platform attempts to define the entire residential premise record without homeowner permission and provenance.

## Strategic Boundary

The protocol is the standardized representation and exchange model for Residential Energy Twin data. External energy protocols move information. The twin defines information. The twin remains the homeowner-governed residential energy record.

## Future Integration Potential

Energy protocols may carry permissioned signals that relate to twin context. The twin may provide source-backed premise meaning behind protocol-level messages, events, capabilities, and constraints.

# Competition Matrix

| Category | Compete | Complement | Integrate | No Conflict |
| --- | --- | --- | --- | --- |
| DERMS | If they claim the canonical home record | Yes | Yes | No |
| Utilities | If they claim homeowner-owned premise truth | Yes | Yes | No |
| Aggregators | If they own permission and premise truth as enrollment artifacts | Yes | Yes | No |
| Device Vendors | If closed product ecosystems claim whole-home ownership | Yes | Yes | No |
| Monitoring Platforms | If inference becomes the full source of truth | Yes | Yes | No |
| HEMS | If optimization systems become the canonical record | Yes | Yes | No |
| Contractor Software | If project records become the home energy record | Yes | Yes | No |
| Proposal Platforms | If proposals become the durable record | Yes | Yes | No |
| Permitting Platforms | No, unless they claim broader premise truth | Yes | Yes | Mostly |
| Suppliers | If sales channels claim ownership of the home model | Yes | Yes | No |
| Manufacturers | If product accounts become the whole-home record | Yes | Yes | No |
| AI Agents | If assistant memory becomes canonical truth | Yes | Yes | No |
| Energy Protocols | If they define the whole premise record without permission | Yes | Yes | No |

# Strategic Position

## Why We Are Not A DERMS

A DERMS coordinates assets for programs and grid operations. We define the residential asset context before orchestration. We do not position the twin as a dispatch authority.

## Why We Are Not A Utility

A utility operates grid infrastructure and retains utility authority. We provide homeowner-governed premise context that may be shared with utilities when permissioned. We do not replace utility authority.

## Why We Are Not A HEMS

A HEMS optimizes behavior inside the home. We preserve the truth layer that explains what exists, what is constrained, what is permissioned, and what history matters. Optimization can consume the twin, but it should not replace it.

## Why We Are Not A CRM

A CRM manages customer relationships and sales workflows. We manage residential energy truth under homeowner governance. Contractor relationship data is not the same as the home energy record.

## Why We Are Not A Proposal Platform

A proposal platform creates offers and sales views. The twin persists before and after any proposal. Proposals are views. The twin is the record.

## Why We Are Not A Monitoring Company

Monitoring companies observe or infer behavior. We preserve asset truth, intent, permission, provenance, and history. Inference can enrich the twin, but it does not replace it.

## What We Are

We are the Customer-Permissioned Truth Layer for residential energy infrastructure.

The customer owns the edge.

We custody the model.

The twin is canonical.

Applications are consumers.

# Ecosystem Summary

The planner is the acquisition wedge.

The Residential Energy Twin is the durable asset.

The protocol is the moat: the standardized representation and exchange model for Residential Energy Twin data.

The applications are distribution.

The ecosystem enriches the twin.

The homeowner remains the center of the system.
