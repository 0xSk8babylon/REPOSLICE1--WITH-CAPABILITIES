# Solar, Market, And Product Intelligence Grounding

Status: Phase 2 architecture bridge for future Phase 3 Twin Intelligence
Date: 2026-06-01
Scope: documentation and architecture governance only
Implementation status: no runtime code, provider integration, API, schema, migration, provider SDK, spec-sheet ingestion, product catalog, AI engineering feature, auth/security implementation, telemetry implementation, utility API, DERMS, dispatch, operational-control, or authority-of-record replacement is approved or implied

## Purpose

This document defines where future Solar Production, Market / Economic Intelligence, and Verified Product Intelligence grounding layers should fit around the Residential Energy Twin before Phase 3 derived intelligence work begins.

These layers are future grounding layers. They are not current runtime providers, product catalogs, quote engines, spec-sheet ingestion workflows, AI engineering features, schemas, APIs, utility integrations, or operational-control systems.

Phase 2 documents placement and trust boundaries. Phase 3 may later use these layers for derived intelligence only after Matt explicitly approves any provider-backed calculators, integrations, product catalogs, normalized schemas, spec-sheet workflows, APIs, or runtime behavior.

## Architecture Rule

Grounding must flow from structured evidence into deterministic reasoning before AI explains it.

Future architecture should follow this pattern:

```text
Manufacturer Evidence / Provider Evidence / Quote Evidence
-> Normalized Product, Production, Or Market Model
-> Deterministic Rules Or Provider-Backed Calculation Layer
-> Residential Energy Twin Analysis
-> AI Explanation Layer
```

AI may explain, summarize, educate, compare scenarios, surface missing information, describe tradeoffs, and produce advisory narratives.

AI must not be treated as:

- the authoritative engineering source
- the source of verified product capabilities
- the source of provider-backed production outputs
- the source of deterministic financial outputs
- the final authority of record
- a replacement for contractor review
- a replacement for engineer review where required
- a replacement for homeowner permission, provenance, source evidence, or auditability

## Solar Production Grounding Layer

The Solar Production Grounding Layer is a future provider-backed or trusted-calculator-backed layer for physical solar production assumptions.

PVWatts or an equivalent trusted provider/calculator may be considered later only with explicit approval. This document does not approve PVWatts integration, any provider SDK, API, data model, cached result store, or production calculation workflow.

### Future Inputs

Future solar production grounding may include:

- location-based production assumptions
- sun-hours or irradiance assumptions
- seasonality
- system size
- losses
- tilt
- azimuth or orientation
- shading assumptions where supported and explicitly labeled
- module and inverter topology from the product topology model
- provider name and provider/version reference where applicable
- source timestamp or generated timestamp where applicable

### Future Outputs

Future solar production grounding may produce:

- monthly kWh outputs
- annual kWh outputs
- daily or representative-day kWh outputs
- confidence posture
- missing-input list
- modeled-vs-estimated-vs-verified classification
- provider/source reference
- limitation text

### Production Authority Boundary

PVWatts-style calculations ground physical production assumptions. The trusted calculator, provider, or deterministic rules layer remains the source for production outputs.

AI may explain the results, describe assumptions, compare scenarios, and surface missing inputs. AI must not create, override, verify, or certify production outputs.

Production labels should distinguish:

- estimated production: planning estimate from incomplete or generic inputs
- modeled production: provider/calculator-backed output from explicit inputs
- verified production: future source-backed production evidence, such as measured production or approved source records, within a defined scope

No production output should imply utility approval, interconnection approval, incentive eligibility, tariff authority, savings guarantee, system performance guarantee, or operational readiness.

## Market / Economic Intelligence Layer

The Market / Economic Intelligence Layer is a future provider-backed, quote-backed, or benchmark-backed layer for economic reasonableness.

EnergySage-style market intelligence concepts may inform future architecture, such as quote normalization and benchmark comparison, but this document does not copy proprietary logic, approve an EnergySage integration, imply partnership, or make EnergySage authoritative by default.

### Future Inputs

Future market/economic grounding may include:

- quote line items
- system size
- product topology and equipment mix
- cost per watt
- regional pricing assumptions
- incentive assumptions and sources
- financing terms
- lease, loan, and cash structures
- installer benchmark concepts
- equipment benchmark concepts
- source/provider references where applicable
- quote dates, benchmark dates, and provider/version references where applicable

### Future Outputs

Future market/economic grounding may support:

- quote normalization
- cost-per-watt comparison
- incentive comparison
- financing comparison
- payback estimate
- lease vs loan vs cash comparison
- market reasonableness checks
- equipment benchmark comparisons
- installer benchmark comparisons
- regional pricing reasonableness
- missing economic input detection
- confidence posture and limitation text

### Economic Authority Boundary

EnergySage-style market intelligence grounds economic reasonableness concepts. Structured calculators, quotes, benchmarks, source documents, or provider-backed data remain the source of deterministic financial outputs.

AI may explain tradeoffs, compare scenarios, and surface uncertainty. AI must not create verified pricing, guarantee savings, certify payback, determine incentive eligibility, approve financing, rank installers as factual authority, or replace homeowner, contractor, financial, tax, or legal review.

Economic labels should distinguish:

- estimated value: planning assumption or placeholder
- quoted value: source-linked quote or proposal value
- verified value: future confirmed value within a defined scope
- market-benchmarked value: value compared against approved benchmark or provider-backed data

No economic output should imply final price, bid, savings guarantee, incentive availability, payback guarantee, financing approval, tax advice, installer endorsement, procurement authority, or business-model approval.

## Verified Product Intelligence Layer

The Verified Product Intelligence Layer is a future verified product capability layer.

Its purpose is to provide trusted equipment capabilities that support Residential Energy Twin reasoning, ground calculations in manufacturer-backed or verified product data, preserve provenance, versioning, auditability, and source attribution, and prevent AI from becoming the authoritative source of equipment capabilities.

### Future Sources

Future product grounding may use:

- manufacturer spec sheets
- verified product catalogs
- approved manufacturer integrations
- future product data providers
- contractor-verified product records
- engineer-reviewed product records where applicable
- source documents and evidence references

None of these sources is authoritative by default. Authority depends on provenance, source scope, version, freshness, confidence, and review status.

### Product Data Requirements

Future verified product intelligence should preserve:

- provenance
- source attribution
- versioning
- audit history
- source date and normalized date where applicable
- confidence boundaries
- deterministic normalized fields
- evidence/reference linkage
- stale or superseded source flags
- conflict handling
- lifecycle and review status

Product labels should distinguish:

- estimated product data
- parsed product data
- manufacturer-backed product data
- verified product data
- contractor-reviewed product data
- engineer-reviewed product data

Parsed data is not verified by default. Manufacturer-backed data is source-backed within the manufacturer's documented scope, but it does not certify installation, compatibility, code compliance, utility approval, or suitability for a specific home.

## Future Normalized Product Fields

Future normalized fields may include the following when supported by approved source evidence.

### PV Modules

- wattage
- efficiency
- temperature coefficients
- degradation assumptions if supported
- module dimensions if relevant to planning
- warranty terms if relevant to market/economic reasoning

### Inverters

- continuous output
- surge limits
- MPPT limits
- AC output limits
- DC input limits
- supported configurations
- operating limits

### Batteries

- usable capacity
- continuous power
- surge power
- round-trip efficiency
- operating limits
- supported expansion limits
- supported inverter/gateway pairings if available

### Gateways / Transfer Equipment

- supported configurations
- backup constraints
- transfer capabilities
- islanding capabilities where applicable
- load-shed or critical-load support where applicable

### Generators

- rated output
- surge output if available
- fuel type
- operating constraints
- runtime assumptions if supported
- transfer compatibility where applicable

### EVSE / Flexible Loads

EVSE and flexible-load fields may be included where consistent with approved load and topology models:

- continuous load
- circuit requirements
- managed charging support
- controllability status
- flexibility classification

Controllability status is descriptive only. It must not imply permission to control, dispatch, curtail, enroll, aggregate, or operate a device.

## Product-Topology Grounding

Future calculations and recommendations must follow product topology.

The Residential Energy Twin should connect product capabilities to topology roles before derived intelligence relies on them.

Future topology-aware calculations should ensure:

- solar production calculations follow product topology
- battery calculations follow product topology
- backup calculations follow product topology
- economic calculations follow product topology
- scenario modeling follows product topology
- resilience calculations follow product topology
- DER / ADR readiness follows product topology

Examples:

- A PV module wattage should not feed production modeling unless the module is part of the modeled system topology.
- A battery usable-capacity value should not feed backup endurance if the battery is not assigned to the scenario topology being analyzed.
- An inverter limit should constrain battery, solar, and backup reasoning only when the inverter is part of the relevant topology and source-backed enough for the use.
- A quote benchmark should compare against the modeled product topology rather than a generic equipment mix when product data is available.

## Future Phase 3 Twin Intelligence Support

These grounding layers may support future Phase 3 derived intelligence, including:

- Structured System Reasoning Graph
- scenario intelligence
- infrastructure simulation
- what-if analysis
- critical-load survivability
- battery recharge likelihood
- outage endurance
- solar recharge modeling
- infrastructure dependency analysis
- topology-aware recommendations
- DER / ADR readiness
- future-state architecture modeling
- advisor traceability
- deterministic reasoning exports
- Residential Energy Twin reasoning

Phase 3 intelligence should remain derived intelligence unless a future approved source-backed workflow promotes a structured fact into canonical twin state.

## Contractor Value Proposition

Future contractor-facing value may include:

- equipment validation
- topology validation
- constraint detection
- resilience analysis
- production analysis
- economic analysis
- design tradeoff explanation
- product compatibility checks
- missing-data detection
- quote reasonableness review
- scenario comparison

These capabilities must preserve:

- contractor review
- engineer review where required
- authority-of-record boundaries
- professional responsibility boundaries
- provenance and auditability
- homeowner authority
- permissioned sharing
- AI advisory boundaries

The system may organize evidence and derived intelligence for review. It must not become the contractor's or engineer's professional authority of record.

## Permission, Provenance, And View Boundaries

Future grounding-layer outputs should follow Phase 2 placement docs:

- `PermissionPlacement.md`: external sharing requires explicit homeowner-governed permission, purpose, duration, scope, and revocation posture.
- `ProvenancePlacement.md`: provider, quote, product, and derived-output provenance must preserve source, version, confidence, assumptions, missing inputs, and limitations.
- `ViewContracts.md`: views should expose only the minimized actor-specific data needed while preserving provenance, confidence, and limitations.
- `TopologyLifecycleDomains.md`: current, sandbox, scenario, contractual, verified, utility-facing, and operational states remain separate.

Provider-backed output should not become a broad export by default. Product evidence should not become whole-home authority by default. Economic intelligence should not become a savings guarantee. Solar production modeling should not become field-verified production by default.

## Phase Placement

Phase 2:

- documents placement and boundaries
- reserves future grounding-layer concepts
- protects homeowner authority, provenance, permissioned sharing, view contracts, AI advisory limits, contractor/engineer review, and operational-control separation

Phase 3 may later:

- use approved grounding layers for derived intelligence
- add provider-backed calculators or integrations
- add normalized product catalogs
- add spec-sheet workflows
- add product-topology-aware calculations
- add market benchmark workflows
- add deterministic reasoning exports

Later implementation may introduce provider-backed calculators, APIs, schemas, product catalogs, spec-sheet workflows, or integrations only with explicit approval.

These docs do not approve:

- runtime integration
- provider SDKs
- schemas or migrations
- APIs
- spec-sheet ingestion
- product catalog implementation
- AI-based engineering automation
- verified pricing
- vendor partnership claims
- compliance claims
- authority-of-record replacement
- utility APIs
- telemetry implementation
- operational control

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- integrating PVWatts, EnergySage, manufacturer systems, product data providers, quote providers, or any equivalent provider
- adding provider SDKs, API clients, schemas, migrations, provider result storage, product catalogs, or spec-sheet ingestion workflows
- defining normalized product fields as runtime schema or canonical data model
- defining production, economic, market, product, quote, benchmark, or provider confidence rules as runtime behavior
- promoting modeled production, quote benchmarks, parsed specs, AI explanations, or derived intelligence into canonical verified facts
- implementing AI engineering automation, contractor packet authority, engineer review replacement, utility exports, DERMS, dispatch, demand response, VPP, telemetry, or operational control
- changing trust language that could imply partnership, integration, compliance, verified pricing, guaranteed savings, utility approval, engineering approval, or authority-of-record replacement

## Sources / Provenance

- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/TopologyLifecycleDomains.md`
- `docs/architecture/PermissionPlacement.md`
- `docs/architecture/ProvenancePlacement.md`
- `docs/architecture/ViewContracts.md`
- `docs/architecture/COGNITION_LAYERS.md`
- `docs/architecture/CANONICAL_TERMINOLOGY.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/skills/repo-guardrails/SKILL.md`
- `.codex/project-skills/canonical-authority-discipline/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `.codex/project-skills/topology-intelligence/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

Solar, Market, and Product Intelligence Grounding defines how future Phase 3 intelligence can use provider-backed production calculations, benchmark-backed economic reasonableness, and verified product capabilities without treating AI as an authority source. The document preserves Phase 2 homeowner authority, permission, provenance, view-contract, topology/lifecycle, contractor/engineer review, and operational-control boundaries while deferring all runtime integration and implementation approval.
