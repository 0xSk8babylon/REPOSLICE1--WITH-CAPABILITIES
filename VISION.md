# Mission

Document role: principles. `PROJECT_MAP.md` documents current reality. `ARCHITECTURE.md` documents structure. `MARKET_POSITIONING.md` documents the external narrative. `ECOSYSTEM_MAP.md` documents ecosystem relationships.

The mission of `residential-energy-planner` is to help homeowners understand, plan, and govern the energy systems inside their homes before those systems become expensive, opaque, or operationally critical.

Homes are becoming energy infrastructure. Solar, batteries, generators, electric vehicles, heat pumps, smart panels, critical loads, and utility programs are turning residential buildings into active grid-edge assets. Most homeowners do not have a durable system of record for that infrastructure. Most contractors, installers, engineers, utilities, aggregators, and manufacturers see only fragments of the home.

This project exists to create that durable system of record: a permissioned Residential Energy Twin owned by the homeowner, grounded in structured facts, labeled assumptions, provenance, and explicit boundaries between planning, professional approval, utility approval, and operational control.

# Core Thesis

## The Planner Is The First Application

The planner is the first useful surface because homeowners and contractors need to make better decisions before deployment. Planning is where goals, constraints, existing conditions, possible architectures, tradeoffs, missing information, and approval boundaries become visible.

The planner exists to make the home understandable. It is not the final asset. It is the first way to create, inspect, and improve the asset.

## The Twin Is Canonical

The twin is the durable source of truth. Applications are temporary. Applications come and go, but the twin persists.

Every application should consume the twin rather than becoming its own source of truth. The planner is the first application, not the final application.

Future contractor, utility, AI, and ecosystem applications should all operate against the same canonical twin. They may expose different views, workflows, explanations, and permissions, but they should not fragment the home into competing records.

## The Twin Is The Asset

The Residential Energy Twin is the durable asset. Applications may come and go, but the structured record of the home, its systems, assumptions, source lineage, permissions, and planning history becomes more valuable over time.

The twin compounds. Every verified panel detail, load record, equipment model, pathway assumption, contractor note, utility relationship, source document, and consent boundary makes future planning safer, faster, and more explainable.

## The Protocol Is The Moat

The long-term defensibility is not a single screen, estimate, or recommendation. It is the protocol: the standardized representation and exchange model for Residential Energy Twin data.

The protocol matters because each stakeholder needs a different view of the same home. A homeowner needs understanding. A contractor needs scoping context. An engineer needs facts and assumptions separated. A utility needs permissioned, minimized, source-linked visibility. AI needs grounded context without authority to invent facts.

## The Homeowner Owns Permissions

The homeowner controls who sees what, for what purpose, and for how long. Residential energy data can reveal occupancy patterns, appliance choices, backup priorities, budget posture, electrical constraints, upgrade plans, and resilience needs. It must not be treated as freely reusable context.

Permission is not a checkbox buried inside a workflow. Permission is central infrastructure. The twin becomes valuable because it can be shared safely, narrowly, and reversibly.

## Truth Beats Inference

The system should prefer known facts over guesses, measured values over estimates, verified sources over unverified claims, and labeled unknowns over confident fabrication.

Inference is useful only when it is clearly labeled. A rough pathway, estimated load, placeholder price, or AI summary can help planning, but it must never masquerade as measured site truth, verified product data, engineering approval, or utility authorization.

## Planning Before Deployment

Residential energy decisions are expensive to reverse. Poor sequencing can create stranded equipment, avoidable service upgrades, incompatible products, unnecessary trenching, weak backup outcomes, or unclear ownership of risk.

The platform focuses on planning before deployment because good planning reduces regret. It helps stakeholders see dependencies before work becomes physical, contractual, or operational.

## Capability Without Permission Is Stranded Value

Technical capability alone does not create usable grid capacity.

A battery, EV, generator, thermostat, solar system, or flexible load only becomes a usable grid asset when three things are true:

- technical capability exists
- customer permission exists
- availability exists

Technical Capability means the asset can physically or functionally provide value. It may be able to store energy, reduce load, shift load, generate power, support backup, or respond to a signal.

Customer Permission means the homeowner has explicitly allowed a specific use, visibility, program, party, or action. Without permission, the capability may exist, but it is not usable by anyone else.

Availability means the asset is actually available for the intended use at the relevant time. A battery may be reserved for backup. An EV may be away from home. A thermostat may be off limits during a comfort window. A generator may be unavailable, unmaintained, or outside the authorized use case.

```text
Technical Capability
+
Customer Permission
+
Availability
=
Usable Grid Capacity
```

Willingness is part of grid capacity. The grid cannot treat a home as a reliable resource simply because hardware exists. The homeowner's consent, preferences, constraints, backup needs, comfort limits, and trust boundaries determine whether technical capability can become usable capacity.

# What Is The Residential Energy Twin

The Residential Energy Twin is a structured, permissioned, source-linked representation of a home's energy-relevant state over time.

It includes recorded facts, planning assumptions, derived planning intelligence, provenance, permissions, and known unknowns. It is designed to support multiple applications without letting any one application become the source of truth.

The twin is not:

- a utility account system
- an engineering stamp
- a permit set
- an AHJ decision
- a final bill of materials
- a dispatch controller
- a warranty authority
- an energy trading account
- a prompt-only memory system

Information that belongs inside the twin:

- home identity and site context
- buildings and structures
- electrical panels and service context
- loads and backup priorities
- equipment and product references
- current and proposed system designs
- pathways, locations, and routing assumptions
- scenarios and planning history
- permissions and visibility boundaries
- source documents and provenance
- utility relationships and service context when permissioned
- missing information and uncertainty

Information that should remain outside the twin unless explicitly authorized and governed:

- private data unrelated to energy planning
- unrestricted raw utility account access
- operational control commands
- financial account credentials
- legal conclusions
- engineering approvals unless provided by the responsible professional
- utility approvals unless provided by the utility or authorized process
- manufacturer claims without source provenance
- AI-generated facts that have not been promoted through a verified source path

## Home

The home is the anchor of the twin. It identifies the residential site, its location context, service context, utility relationship, and planning history.

The home record should be durable. It should survive individual projects, proposals, contractors, devices, and applications.

## Buildings

Buildings describe the physical structures that shape energy planning: main house, detached garage, workshop, ADU, barn, or other structures.

Buildings matter because distance, use, routing, occupancy, and future expansion often change the best energy architecture.

## Panels

Panels describe the electrical distribution context: main service panels, subpanels, critical load panels, smart panels, solar-ready panels, and related constraints.

Panels belong in the twin as planning facts and assumptions. They do not, by themselves, create code compliance, engineering approval, or service upgrade approval.

## Loads

Loads describe what the home needs to power, how important each load is, and how it behaves during planning.

Loads are central because backup, battery sizing, solar recovery, generator planning, load control, and resilience all depend on what the homeowner actually wants to keep running.

## Equipment

Equipment includes solar panels, inverters, batteries, generators, gateways, smart panels, transfer equipment, EV chargers, load centers, and other energy-related products.

Equipment belongs in the twin only with clear product identity, role, quantity, location when known, and provenance. Product data without provenance should remain visibly provisional.

## Scenarios

Scenarios represent possible futures for the home. They allow homeowners and professionals to compare tradeoffs without pretending that every option is equally complete, verified, or approved.

Scenarios are planning objects. They help structure decisions, but they are not bids, permits, final designs, or guaranteed outcomes.

## Pathways

Pathways describe how equipment, buildings, panels, and future upgrades may connect physically or logically.

Pathways matter because routing, trenching, conduit, visibility, distance, and siting can dominate cost, complexity, and feasibility.

## Permissions

Permissions describe who can see which parts of the twin, for what purpose, and under what limits.

Permission is a first-class domain inside the Residential Energy Twin because data visibility is not separate from product value. The Permission Layer governs access to twin views. Permission does not exist outside the twin.

## Provenance

Provenance describes where information came from, how it was derived, how confident the system should be, and what remains unknown.

Provenance is not decoration. It is what separates a useful twin from an unsafe pile of assertions.

## Utility Relationships

Utility relationships describe service context, provider relationships, tariff or program context, interconnection state, and grid-facing visibility when permissioned.

These relationships should be minimized, source-linked, and scoped. A utility-facing view should not expose the homeowner's entire planning context.

# Canonical Truth

The twin is canonical.

Applications are views into the twin.

A planner, advisor, contractor packet, utility view, AI grounding context, estimate, dashboard, or future application should consume the twin. It should not quietly become a separate source of truth.

## Structured Facts

Structured facts are recorded fields in the twin. Examples include a panel amperage, load name, equipment model, building type, scenario name, pathway distance assumption, or source document reference.

Structured facts are canonical planning records, but they are not automatically verified. A structured fact can still be user-entered, imported, demo-seeded, outdated, or wrong. Its origin and provenance determine how much authority it carries.

## Derived Facts

Derived facts are produced from structured facts by explicit rules, calculations, comparisons, or summaries.

Examples include planning completeness, backup posture, scenario comparison, takeoff line items, recommendation profiles, or confidence summaries.

Derived facts are useful, but they are downstream of their inputs. They must expose their basis, limitations, and missing data.

## Inferred Facts

Inferred facts are plausible conclusions drawn from incomplete evidence.

Inference can help planning when clearly labeled. It must remain distinguishable from measured, verified, imported, or homeowner-confirmed information.

## Unknown Facts

Unknown facts are facts the system does not have.

Unknowns should remain visible. An unknown is often safer than a weak guess because it tells the homeowner, contractor, engineer, or utility what still needs to be confirmed.

# Permission Philosophy

Homeowners should own the Permission Layer that governs access to views of their Residential Energy Twin. Permission is a first-class domain inside the twin, not a separate record outside it.

Permission must be explicit, revocable, scoped, and based on least privilege. The default posture should be to reveal only what a stakeholder needs for a specific purpose.

## Homeowner Ownership

The homeowner is the primary owner of the Residential Energy Twin. Other stakeholders may contribute, inspect, validate, or consume specific views, but they do not silently take ownership of the whole record.

## Explicit Consent

Consent should be intentional and understandable. A homeowner should know what data is being shared, with whom, why, and for how long.

## Revocable Consent

Consent should be revocable where practical. A homeowner should be able to stop future access without erasing historical records that legitimately need to remain for audit, safety, or completed work.

## Scoped Visibility

Different stakeholders need different views. Sharing the whole twin should be rare. Most workflows should use scoped visibility.

## Least Privilege

A stakeholder should receive the minimum useful information for the task. More data is not automatically better. Unnecessary data increases privacy risk and trust risk.

## Contractor Visibility

Contractors need site context, equipment intent, load assumptions, route assumptions, missing information, and planning constraints. They do not automatically need unrelated homeowner notes, account information, utility account data, or AI advisory history.

## Utility Visibility

Utilities need minimized, source-linked, permissioned visibility into service-relevant and grid-relevant facts. They do not automatically need the homeowner's full planning workspace, budget posture, private notes, or contractor discussion history.

## AI Visibility

AI needs structured grounding context, source lineage, uncertainty, and limitations. AI should not receive broad private context by default, and it should not create canonical facts without a verified promotion path.

## Third-Party Visibility

Third parties should receive scoped, purpose-bound access. Manufacturers, aggregators, financing partners, insurers, or software vendors should not receive more visibility than their role requires.

# The Grid Edge Thesis

The home is the grid edge.

Devices are the residential edge.

## Residential Edge

The residential edge is the energy reality inside and around the home: panels, loads, solar, batteries, generators, EVs, appliances, controls, wiring constraints, homeowner priorities, and future upgrade paths.

It is where household decisions, contractor work, product ecosystems, and grid needs meet.

## Grid Edge

The grid edge is the boundary where distributed assets, customer behavior, utility infrastructure, and grid programs interact.

Historically, utilities have had strong visibility into meters and grid-side infrastructure, but weaker visibility into the actual topology, intent, constraints, and priorities behind the meter.

Utilities often see:

- meters
- device APIs
- enrollment status

But they may not see:

- panel constraints
- service constraints
- backup priorities
- future upgrades
- homeowner intent
- consent boundaries
- contractor verification
- topology
- multi-device interaction

Utilities often see the net load. They do not always see the asset logic behind the load.

That distinction matters. Net load may show what happened, but not always why it happened, what assets caused it, what constraints shaped it, what the homeowner intended, what is available next, or what is permissioned.

## Permissioned Grid Edge

The permissioned grid edge is a future where homes can selectively expose verified, source-linked, purpose-specific energy context to utilities, contractors, aggregators, manufacturers, and applications.

This does not mean utilities control the home. It means homeowners can allow better visibility when it serves a clear purpose: planning, interconnection, resilience, safety, incentives, grid programs, or coordination.

Utilities often lack visibility beyond the meter because behind-the-meter systems are fragmented across homeowners, contractors, installers, manufacturers, device apps, paper records, permit records, and utility account data. A permissioned twin can connect those fragments without making any one stakeholder the owner of all context.

A permissioned twin changes the relationship by making the home legible on homeowner-controlled terms.

It creates a new layer of visibility: not surveillance, not raw device control, and not unrestricted access, but permissioned premise intelligence. It can show what exists, what is possible, what is trusted, what is constrained, what is available, and what the homeowner has allowed.

# Layer of Truth

The Residential Energy Twin should distinguish different kinds of truth instead of flattening them into one confidence level.

## Inferred Truth

Inferred Truth comes from patterns and signals. Examples include meter patterns, device behavior, and load signatures.

Inferred Truth can be useful, but it is not enough by itself. It should remain labeled because it may explain behavior without proving the underlying asset, intent, permission, or field condition.

## Declared Truth

Declared Truth comes from the homeowner or another stakeholder stating goals, plans, preferences, or constraints. Examples include customer goals, future EV plans, backup priorities, and budget targets.

Declared Truth is essential because many important grid-edge facts cannot be inferred from telemetry. A meter cannot reliably know what a homeowner intends to install next, what they are willing to share, or which loads matter most during an outage.

## Documented Truth

Documented Truth comes from artifacts. Examples include equipment labels, bills, photos, permits, and drawings.

Documented Truth gives the twin more grounding than inference or declaration alone. It can show what was recorded, photographed, issued, quoted, submitted, or drawn, even before field validation is complete.

## Verified Truth

Verified Truth comes from trusted confirmation. Examples include inspections, installed equipment, approved interconnections, and field validation.

Verified Truth carries the strongest authority, but it still has scope. A verified installation fact does not automatically approve every future use case, export, program enrollment, or operational action.

All four layers together create a stronger model than any one layer alone. Inference provides signals. Declaration provides intent. Documentation provides evidence. Verification provides authority. The twin becomes valuable because it can preserve the difference between them.

# Ecosystem Positioning

Core principle:

DERMS orchestrate assets.

The twin defines assets.

DERMS answer: "What can we dispatch right now?"

The twin answers: "What exists, what is possible, what is permissioned, and what is trusted?"

## DERMS

### What They Do

DERMS coordinate distributed energy resources for grid programs, dispatch, monitoring, and operational planning.

### What We Do

We define the residential asset context before orchestration: what exists, what is possible, what is permissioned, what is trusted, and what remains unknown.

### Overlap

Both care about distributed energy resources, flexibility, availability, and grid-edge value.

### Complement

The twin can give DERMS better premise context, permission boundaries, and trust signals before assets are treated as dispatchable.

### Competition

The platform may compete if DERMS providers try to own behind-the-meter asset identity, customer permission, and premise intelligence as their own closed record.

### Strategic Boundary

DERMS should not be the canonical record of the home. The twin should not pretend to be a dispatch authority.

## HEMS

### What They Do

HEMS manage or optimize energy behavior inside the home, often across devices, appliances, schedules, comfort, solar, storage, or load control.

### What We Do

We define the broader residential energy truth layer: assets, constraints, goals, permissions, provenance, scenarios, and long-term planning context.

### Overlap

Both care about home energy behavior, devices, loads, and optimization potential.

### Complement

HEMS can act on a better model when the twin clarifies what exists, what matters, what is permissioned, and what should remain off limits.

### Competition

The platform may compete if HEMS systems try to become the homeowner's full energy system of record rather than an operating layer or application.

### Strategic Boundary

HEMS can optimize behavior. The twin governs truth, context, permission, and provenance.

## Smart Meters

### What They Do

Smart meters record energy flow at the meter and provide interval-level visibility into net consumption, export, and grid-facing behavior.

### What We Do

We describe the asset logic behind the meter: panels, loads, equipment, scenarios, topology, homeowner intent, permissions, and trusted context.

### Overlap

Both help explain energy behavior and grid-edge conditions.

### Complement

Meter data can strengthen inferred truth, while the twin can explain what meter data alone cannot see.

### Competition

The platform does not compete with meters as measurement infrastructure.

### Strategic Boundary

Meters see net behavior. The twin explains premise context, subject to permission and provenance.

## Sense

### What They Do

Sense and similar energy monitoring products infer device-level behavior from electrical signatures and help homeowners understand consumption patterns.

### What We Do

We organize the broader home energy graph: declared goals, documented assets, verified records, permissions, scenarios, and stakeholder views.

### Overlap

Both care about appliance behavior, load understanding, and homeowner visibility.

### Complement

Load signatures can contribute inferred truth to the twin when permissioned and labeled.

### Competition

The platform may compete if monitoring products expand into the full source of truth for home energy planning, permissions, and stakeholder collaboration.

### Strategic Boundary

Load inference is one layer of truth. It should not replace declared, documented, or verified truth.

## Device Vendors

### What They Do

Device vendors make and operate products such as batteries, inverters, EV chargers, thermostats, generators, panels, gateways, and smart panels.

### What We Do

We place device facts inside a homeowner-governed context with source provenance, permissions, scenarios, topology, and cross-device relationships.

### Overlap

Both care about product identity, capability, status, compatibility, and customer value.

### Complement

Device vendors can contribute product facts, documentation, status, and capability signals to the twin when permissioned.

### Competition

The platform may compete if device vendors try to own the entire home energy relationship through closed ecosystems.

### Strategic Boundary

Device vendors know their devices. The twin describes the home across devices, vendors, stakeholders, and time.

## Utilities

### What They Do

Utilities operate grid infrastructure, serve customers, administer tariffs and programs, and approve or manage utility-side processes.

### What We Do

We help create a homeowner-governed, permissioned view of premise energy context that can be shared with utilities when appropriate.

### Overlap

Both care about service context, interconnection, grid impacts, resilience, programs, and customer energy behavior.

### Complement

The twin can reduce blind spots beyond the meter while preserving homeowner control and scoped visibility.

### Competition

The platform does not aim to become a utility. It may compete with utility-owned customer data models if those models try to define the residential edge without homeowner custody.

### Strategic Boundary

Utilities retain utility authority. The homeowner retains permission over the twin.

## Contractor Software

### What They Do

Contractor software helps manage leads, customers, site visits, estimates, jobs, crews, documents, and project workflows.

### What We Do

We maintain the homeowner-governed energy truth layer that contractors can consume through scoped visibility.

### Overlap

Both care about project context, site facts, customer goals, estimates, equipment, and work coordination.

### Complement

Contractor tools can work from better structured context instead of recreating the home model for every job.

### Competition

The platform may compete if contractor systems try to own the canonical home energy record rather than contributing to it.

### Strategic Boundary

Contractor software manages contractor operations. The twin preserves homeowner-governed premise truth.

## Proposal Software

### What They Do

Proposal software creates sales proposals, savings narratives, equipment packages, financing views, and customer-facing offers.

### What We Do

We define the underlying home energy context before a proposal is generated.

### Overlap

Both care about customer understanding, options, equipment, cost framing, and decision support.

### Complement

Proposal tools can become more honest and reusable when grounded in a permissioned twin with clear assumptions and provenance.

### Competition

The platform may compete if proposal tools position the proposal as the durable record of the home.

### Strategic Boundary

A proposal is a view. The twin is the record.

## Permitting Software

### What They Do

Permitting software organizes permit applications, forms, plan sets, jurisdictional requirements, and submission workflows.

### What We Do

We organize planning facts, assumptions, documented evidence, and permissioned context before formal approval workflows.

### Overlap

Both care about structured project information, equipment, site facts, and approval boundaries.

### Complement

The twin can prepare cleaner source context for permitting workflows when professional and jurisdictional authority are involved.

### Competition

The platform does not compete as an AHJ, permit authority, or stamped plan system.

### Strategic Boundary

Permitting tools support submissions. The twin preserves homeowner-governed energy context and does not grant permits.

## Aggregators

### What They Do

Aggregators combine many distributed assets into programs, markets, or grid services.

### What We Do

We define permissioned premise-level capability, constraints, trust, and homeowner intent before aggregation.

### Overlap

Both care about flexible capacity, availability, customer participation, and asset value.

### Complement

The twin can help aggregators understand which capacity is real, permissioned, available, and bounded by homeowner constraints.

### Competition

The platform may compete if aggregators attempt to own customer permission and premise truth as part of enrollment.

### Strategic Boundary

Aggregators coordinate participation. The twin governs the customer's edge model and permissioned facts.

## AI Systems

### What They Do

AI systems interpret information, answer questions, summarize context, plan workflows, and coordinate tasks.

### What We Do

We provide the permissioned, source-linked home energy context AI systems should consume.

### Overlap

Both care about explanation, decision support, and coordination.

### Complement

AI becomes safer and more useful when grounded in structured twin context with provenance, permissions, and unknowns.

### Competition

The platform may compete with prompt-only or assistant-owned memory systems that try to become the source of home energy truth.

### Strategic Boundary

AI explains and coordinates. The twin remains canonical.

## Energy Protocols

### What They Do

Energy protocols define how devices, programs, markets, or systems communicate about energy capabilities, events, states, or transactions.

### What We Do

We define homeowner-governed premise context: assets, relationships, permissions, provenance, scenarios, and trusted visibility.

### Overlap

Both care about structured representation, interoperability, and energy coordination.

### Complement

The twin can provide premise truth that energy protocols may consume or reference when permissioned.

### Competition

The platform may compete if a protocol attempts to define the entire residential premise record without homeowner permission and provenance.

### Strategic Boundary

Energy protocols move or structure energy information. The twin defines the homeowner-governed truth graph behind that information.

# Customer-Permissioned Home Energy Graph

The company is not another dashboard, another smart home app, another proposal tool, or another DERMS.

Those categories may expose useful views, controls, recommendations, or workflows, but they do not fully describe the strategic asset being created.

The category is:

Customer-Permissioned Home Energy Graph

Alternative category names include:

- Premise Intelligence Layer
- Home Energy Truth Layer
- Residential Grid Edge Custody Layer
- Home Energy Passport
- Premise Energy Vault

Customer-Permissioned Home Energy Graph is the preferred description because it captures the four essential ideas:

- Customer-Permissioned: the homeowner controls visibility and use
- Home Energy: the domain is the residential energy reality behind the meter
- Graph: the value is in relationships among home, buildings, panels, loads, equipment, scenarios, pathways, permissions, provenance, utility relationships, and stakeholders
- Truth: the graph distinguishes inferred, declared, documented, verified, derived, and unknown facts

The platform is not just a place to view information. It is a governed graph of residential energy context that can support many applications while preserving homeowner control.

Customer-Permissioned Truth Layer is market positioning language for the same strategic position; it should not replace the category name or the Residential Energy Twin.

# Wedge Strategy

## Stage 1: Residential Energy Planner

Purpose: Help homeowners and contractors model the home, compare planning options, expose missing information, and make better pre-deployment decisions.

Users: Homeowners, contractors, installers, and advisors.

Value created: Clearer planning, fewer hidden assumptions, better sequencing, explicit tradeoffs, and the first durable structured record of the home's energy context.

## Stage 2: Residential Energy Twin

Purpose: Convert planning context into a durable home energy system of record that persists across projects, stakeholders, and applications.

Users: Homeowners, contractors, installers, engineers, advisors, and future applications.

Value created: A compounding asset that stores structured facts, assumptions, scenarios, provenance, and history in one homeowner-governed record.

## Stage 3: Permission Layer

Purpose: Let the homeowner control scoped visibility into the twin.

Users: Homeowners first; then contractors, utilities, AI systems, manufacturers, aggregators, and other third parties.

Value created: Trustworthy collaboration without oversharing, unclear authority, or uncontrolled data reuse. Permission is a first-class domain inside the Residential Energy Twin, and the Permission Layer governs access to twin views.

## Stage 4: Contractor Layer

Purpose: Give contractors and installers a scoped planning basis for scoping, site walks, estimating, equipment review, and project coordination.

Users: Contractors, installers, homeowners, and engineers.

Value created: Less repetitive discovery, better context before site work, clearer assumptions, and cleaner handoff between homeowner intent and professional review.

## Stage 5: Utility Layer

Purpose: Provide utilities with permissioned, minimized, source-linked visibility into relevant residential energy context.

Users: Utilities, homeowners, engineers, aggregators, and authorized program partners.

Value created: Better interconnection context, safer program design, more accurate grid-edge visibility, and fewer blind spots behind the meter.

## Stage 6: Grid Edge Intelligence Network

Purpose: Enable many permissioned Residential Energy Twins to support safer planning, coordination, resilience, and grid-edge intelligence without stripping homeowners of control.

Users: Homeowners, utilities, aggregators, contractors, manufacturers, communities, and future energy applications.

Value created: A network of structured, permissioned, provenance-backed residential energy context that can support better decisions across the grid edge.

## Stage 7: Energy Application Ecosystem

Purpose: Allow third parties to build applications on top of the Residential Energy Twin.

Users: Homeowners, contractors, utilities, manufacturers, aggregators, software developers, and future AI agents.

Value created: A shared source of truth, reduced data silos, reusable permission framework, reusable provenance framework, and reusable twin infrastructure.

The long-term goal is not a single application. The long-term goal is an ecosystem of applications built on top of the same homeowner-governed Residential Energy Twin.

# Stakeholders

## Homeowner

The homeowner gains understanding, control, continuity, and leverage. The twin helps the homeowner know what exists, what is planned, what is uncertain, what has been shared, and what still needs professional or utility approval.

## Contractor

The contractor gains structured context before scoping work: site facts, design intent, equipment assumptions, pathways, missing data, and homeowner priorities. This can reduce repetitive discovery and make estimates more honest.

## Installer

The installer gains clearer field context, equipment relationships, planned locations, route assumptions, and known gaps. The twin can help distinguish planning assumptions from verified install conditions.

## Engineer

The engineer gains better organized inputs and assumption visibility. The twin does not replace engineering approval; it helps prepare the factual context an engineer needs to review.

## Utility

The utility gains permissioned visibility into relevant behind-the-meter context when the homeowner allows it. This can support better interconnection review, program design, resilience planning, and grid-edge understanding.

## Aggregator

The aggregator gains a consented, source-linked view of eligible residential energy assets and constraints. The twin can help prevent operational or program claims that exceed what the homeowner authorized or what the system can prove.

## Manufacturer

The manufacturer gains clearer product context, installation patterns, compatibility questions, and support needs when homeowners permit the relevant visibility. Product facts still require provenance.

## AI Agent

AI agents are future consumers of the twin. They do not own the twin. They consume permissioned context and help interpret, explain, organize, and coordinate work around the home.

AI agents should operate within homeowner-defined permission boundaries. They should not create canonical truth, and they should remain advisory unless explicitly authorized for a specific workflow.

Future homeowner agents may help homeowners understand tradeoffs, missing information, and permission choices. Future contractor agents may help organize scoped project context without seeing unrelated private data. Future utility agents may consume minimized, permissioned, source-linked grid-edge context. Future planning agents may compare scenarios, surface assumptions, and coordinate next questions while keeping the twin as the source of truth.

# Trust Principles

## Truth Beats Inference

Known, structured, source-linked facts carry more authority than guesses. Inference is allowed only when labeled.

## Provenance Required

Important facts, product specs, assumptions, derived outputs, and recommendations should expose where they came from. Missing provenance should be visible.

## Assumptions Labeled

Every assumption should be identifiable as an assumption. The system should not smooth over uncertainty to sound more complete.

## Engineer Approval Remains Final

The platform may organize planning facts and expose constraints, but stamped electrical decisions remain with qualified professionals.

## Utility Approval Remains Final

The platform may prepare context for utility-facing workflows, but utility approval remains with the utility or authorized process.

## AI Is Advisory

AI may explain, summarize, compare, and help users ask better questions. AI should be grounded in the twin and should show uncertainty.

## AI Is Not Authority

AI does not create canonical home facts, product truth, code compliance, engineering approval, utility approval, financial guarantees, or operational authorization.

# Non-Goals

The platform is not:

- a utility
- an AHJ
- an engineering stamp
- a permit
- a final electrical design
- a substitute for a licensed electrician or engineer
- a utility approval system
- an energy trader
- a dispatch authority
- a DER control platform by default
- a billing system
- a financing authority
- a product certification authority
- a manufacturer warranty authority
- a legal authority
- a tax advisor
- an insurer
- a black-box AI decision maker
- a system that turns inference into truth
- a system that shares homeowner data without explicit permission

# Infrastructure Versus Software

The goal is not merely to build software.

The goal is to become infrastructure.

Some formats and systems become valuable because many applications can rely on them. PDF made documents portable. DWG made drawings durable across design workflows. IFC made building information exchange more structured across building stakeholders.

The Residential Energy Twin should play a similar strategic role for home energy context.

The planner is the first application.

The Residential Energy Twin is the durable asset.

The protocol is the moat: the standardized representation and exchange model for Residential Energy Twin data.

The applications are distribution.

Future applications may include:

- contractor tools
- utility tools
- supplier tools
- financing tools
- permitting tools
- AI agents

Applications may come and go.

The twin persists.

The protocol compounds.

# Compounding Advantage

## Why The Twin Compounds

The twin becomes more valuable because it accumulates context over time.

Every homeowner interaction improves the twin.

Every contractor interaction improves the twin.

Every utility interaction improves the twin.

Every equipment upgrade improves the twin.

Every scenario improves the twin.

Every permit, inspection, document, photo, and source record improves the twin.

Every permission decision improves the twin.

Every accepted recommendation improves the twin.

Every rejected recommendation improves the twin.

Every future plan improves the twin.

The compounding value comes from continuity. A home does not reset after one project, one proposal, one installation, one utility interaction, or one planning session. The twin becomes more useful because it remembers what changed, what was considered, what was approved, what was rejected, what was shared, what was constrained, and what the homeowner intends next.

## Historical Context Is The Moat

Algorithms can be copied.

Recommendations can be copied.

Interfaces can be copied.

AI can be copied.

Historical residential energy context is much harder to copy.

That context includes:

- home history
- upgrades
- additions
- remodels
- service changes
- equipment changes
- contractor interactions
- utility interactions
- planning history
- permissions history
- homeowner goals
- future plans
- asset evolution

The moat is not a recommendation engine.

The moat is accumulated context.

## Why The Protocol Compounds

The protocol becomes more valuable as more participants use it.

Participants may include:

- homeowners
- contractors
- engineers
- utilities
- aggregators
- suppliers
- manufacturers
- software vendors
- AI agents

Every participant enriches the twin while consuming value from it.

The protocol becomes stronger because everyone contributes to the same underlying asset. The homeowner gains continuity. Contractors gain better context. Engineers gain clearer assumptions. Utilities gain permissioned visibility. Manufacturers and suppliers gain better product context. AI agents gain grounded context without becoming the source of truth.

## Why Applications Are Distribution

Applications are important.

Applications create value.

Applications acquire users.

Applications generate data.

But applications are not the primary asset.

The planner is the first application.

Future applications may include:

- contractor tools
- utility tools
- supplier tools
- financing tools
- permitting tools
- AI agents

Applications create and enrich the twin.

The twin persists even if applications change.

## The Long-Term Flywheel

```text
More homeowners
↓
More twin creation
↓
More context
↓
More useful planning
↓
More contractor participation
↓
More utility participation
↓
More ecosystem integrations
↓
More value for homeowners
↓
More twin creation
```

This creates compounding value over time because each cycle adds context to the same durable asset. More homes create more twins. More twins create more planning context. Better context makes planning more useful. More useful planning brings more contractors, utilities, and ecosystem participants. More participation adds more context, which increases the value of the twin for homeowners and makes future twin creation more attractive.

## Strategic Summary

The planner is the acquisition wedge.

The Residential Energy Twin is the durable asset.

The protocol is the moat: the standardized representation and exchange model for Residential Energy Twin data.

The applications are distribution.

The accumulated residential energy context is the compounding advantage.

# Long-Term Strategic Position

The customer owns the edge.

We custody the model.

Not surveillance. Custody.

Not device control first. Premise intelligence first.

We define the asset before anyone controls the asset.

The future grid edge is not just hardware.

It is:

- custodial consent
- verified capability
- economic participation
- provenance
- homeowner permission

# Long-Term Vision

The long-term vision is a world where every home has a Residential Energy Twin: a durable, permissioned, source-linked system of record for the energy reality of the home.

Homeowners control the twin. They decide which contractor sees the project context, which utility sees service-relevant facts, which AI system receives grounding context, which manufacturer sees product-related information, and which third party gets access for a specific purpose.

Contractors build from twin data instead of starting from scattered photos, notes, spreadsheets, screenshots, and memory. Engineers review better organized inputs. Utilities consume permissioned visibility into the grid edge without taking ownership of the whole home context. Applications are built on top of the twin instead of becoming isolated data silos.

## Applications Are Temporary

Applications evolve. Companies evolve. Interfaces evolve. AI systems evolve.

The twin should outlive all of them. The Residential Energy Twin should become durable infrastructure rather than a feature of a single application.

The planner is the first application because planning is where trust begins. The Residential Energy Twin is the durable asset because structured truth compounds. The protocol is the moat because it is the standardized representation and exchange model for Residential Energy Twin data, and every stakeholder needs a safe, scoped, provenance-backed view of the same home.

The end state is not just better solar planning or better backup estimates. The end state is a homeowner-governed energy record that becomes more useful every year, supports many applications, and makes the residential grid edge legible without sacrificing homeowner control.
