# Residential Energy Twin Safety Domain

Status: Residential Energy Twin architecture planning document
Date: 2026-06-02
Scope: documentation and architecture governance only
Implementation status: no schema, migration, runtime behavior, API, auth, RBAC, ABAC, permission enforcement, safety approval, field-verification workflow, inspection workflow, utility API, DERMS, dispatch, operational-control, or canonical runtime Safety Domain implementation is approved or implied

## Purpose

The Safety Domain preserves trusted information necessary to understand, assess, and safely interact with residential energy infrastructure throughout the lifecycle of a property.

The Safety Domain exists independently of any individual contractor, utility, homeowner, installer, manufacturer, or software platform. Inside this repository, it is a component of the Residential Energy Twin and does not exist as a separate product.

This document defines Safety Domain doctrine and architecture boundaries only. It does not approve runtime safety records, safety scoring, NEC automation, field verification, utility submission, operational control, or safety approval workflows.

## Core Principle

Safety information should persist with the home.

Safety information should not be recreated from memory after ownership changes, contractor changes, equipment replacements, utility program changes, scenario revisions, or lifecycle transitions.

Safety information should preserve provenance, verification posture, confidence, missing data, assumptions, permission scope, and lifecycle state so future users can distinguish recorded safety context from verified safety evidence.

## Safety Domain Objectives

The Safety Domain helps answer:

- What infrastructure exists behind the meter?
- What systems can energize the property?
- What systems can operate while disconnected from the grid?
- What systems can export power?
- What systems can create safety considerations for workers or occupants?
- What information is verified versus assumed?
- What information is unknown, stale, homeowner-reported, contractor-reported, permit-backed, inspection-backed, or utility-backed?

These answers are safety context. They are not safety approval, code compliance, AHJ approval, utility approval, interconnection approval, field verification, operational readiness, or permission to control equipment.

## Safety Record Categories

### Energy Sources

Examples:

- utility service
- solar generation
- battery systems
- backup generators
- vehicle-to-home systems
- vehicle-to-grid systems
- microgrid systems

Boundary:

Recorded energy-source information does not prove installation, commissioning, code compliance, utility approval, interconnection approval, export authorization, operational availability, or device-control authority.

### Isolation Systems

Examples:

- automatic transfer switches
- manual transfer switches
- interlock systems
- islanding controls
- disconnecting means

Boundary:

Recorded isolation-system information does not prove correct installation, safe operation, inspected status, transfer compliance, anti-islanding compliance, or worker-safety readiness unless a future approved verification workflow records source-backed evidence within a defined scope.

### Export Capabilities

Examples:

- export capable
- non-export capable
- utility-approved export
- utility-limited export

Boundary:

Export-capability records must distinguish equipment capability from utility approval, interconnection status, tariff authority, program eligibility, export permission, and operational dispatch. Utility-approved or utility-limited export claims require utility-source provenance before they can carry stronger authority.

### Operational Modes

Examples:

- grid connected
- backup capable
- island capable
- whole-home backup
- partial backup

Boundary:

Operational-mode records should describe recorded or verified capability context. They must not imply live telemetry, current operating state, command authority, dispatch authority, DERMS behavior, demand response, VPP participation, or operational-control readiness.

### Verification Status

Examples:

- contractor verified
- permit verified
- inspection verified
- utility verified
- homeowner reported
- unknown

Boundary:

Verification status must preserve scope. A verified field is not a verified system unless the source covers the system. A contractor-verified record is not automatically engineer-approved, AHJ-approved, utility-approved, code-compliant, safe, commissioned, or operationally controllable.

### Provenance

The Safety Domain records:

- who supplied information
- when information was supplied
- what evidence supports the information
- source type and data origin
- lifecycle state
- affected equipment, topology, field, or capability
- confidence level
- verification status and verification scope
- missing inputs
- assumptions
- limitation text

Safety provenance does not replace permission, professional review, utility review, AHJ review, inspection, field verification, or operational-control authorization.

## Safety Visibility Principle

Safety information should be permissioned.

Visibility should be limited to the minimum information required for the intended purpose. The Twin should not expose unrelated homeowner information when only safety information is required.

Future safety views should be scoped by:

- audience
- purpose
- lifecycle state
- included safety categories
- excluded homeowner/private context
- source-document visibility
- verification scope
- provenance summary
- permission scope when enforcement exists
- revocation and expiration expectations when enforcement exists

Safety views should preserve uncertainty. A minimized safety view must not hide unknowns, assumptions, missing verification, stale information, or conflicting evidence.

No current runtime permission enforcement, safety-scoped endpoint, safety export, contractor packet, utility packet, first-responder packet, or operational-control view is approved by this document.

## Lifecycle Placement

Safety Domain facts should follow the Residential Energy Twin lifecycle model.

| Lifecycle context | Safety posture |
| --- | --- |
| Recorded current state | Captures current known safety-relevant infrastructure and safety conditions as recorded planning facts, with provenance and missing-data labels. |
| Sandbox planning state | Captures draft safety implications of proposed designs without changing current safety context. |
| Proposed pathway state | Captures safety considerations for a named planning pathway, still planning-only. |
| Saved scenario revision state | Preserves historical safety context at recorded fidelity, not full replay unless future revision support exists. |
| Contractor-reviewed state | Future state for contractor-scoped safety context; not engineering, AHJ, utility, or safety approval by default. |
| Permit / inspection / utility verified state | Future source-backed verification contexts that require approved workflows, source evidence, scope, and authority boundaries. |
| Operational state | Future separate trust domain requiring telemetry governance, command authorization, failure handling, audit, cybersecurity, and operational-control separation. |

No safety lifecycle transition should be inferred from AI text, recommendation profile selection, design status, scenario ranking, account role, endpoint access, utility provider text, or UI visibility.

## Relationship To Other Twin Domains

The Safety Domain is a cross-cutting Residential Energy Twin domain. It depends on, but does not replace, other domains.

| Related domain | Safety relationship | Boundary |
| --- | --- | --- |
| Premise | Service context, site identity, and behind-the-meter scope. | Does not prove legal title, utility account authority, service territory, or verified service status. |
| Electrical Infrastructure | Panels, service equipment, disconnects, transfer equipment, and electrical constraints. | Does not approve NEC compliance, AHJ readiness, stamped design, or safe installation. |
| Equipment | Energy sources, isolation systems, export-capable equipment, and operational-mode capabilities. | Product capability is not installed capability, verified safety, utility approval, or operational authority. |
| Loads | Backup scope, critical loads, and occupant/worker safety considerations. | Recorded loads are not circuit inventory, load study, telemetry, or load-control permission. |
| Topology | Relationships among sources, panels, isolation equipment, backup systems, export paths, and lifecycle state. | Topology is not field verification, utility approval, or operational dispatch. |
| Permissions | Controls who may see or use safety information. | Permission does not prove source quality or safety authority. |
| Provenance | Records evidence, source, verification scope, confidence, and limitations. | Provenance does not grant access, approval, or operational permission. |
| Utility Relationships | Captures source-linked utility approval, limitation, or interconnection context when approved and sourced. | Utility context does not imply tariff authority, program eligibility, DERMS, dispatch, or grid-service participation. |
| Views | Projects minimum necessary safety context for an audience and purpose. | Views are not canonical and are not enforcement without future approved runtime policy. |

## Strategic Role

The Safety Domain strengthens:

- worker safety
- outage restoration context
- infrastructure awareness
- homeowner understanding
- contractor continuity
- utility trust
- lifecycle continuity across ownership, contractor, equipment, and program changes

The Safety Domain supports the Trusted Residential Energy Record and the long-term Residential Infrastructure Registry / Residential Infrastructure Network vision by preserving safety-relevant facts with provenance and permission boundaries.

It does not create a standalone safety product, safety certification system, inspection product, utility registry, operational-control platform, or emergency-response system.

## Decisions Requiring Matt Approval

Matt approval is required before any of the following become implementation, schema, API contract, enforcement behavior, or settled product direction:

- creating runtime Safety Domain models, fields, tables, migrations, APIs, services, exports, or UI workflows
- adding safety verification workflows, inspection workflows, permit workflows, AHJ workflows, or utility verification workflows
- defining mandatory safety provenance fields, verification-status semantics, confidence thresholds, safety-readiness scoring, or safety-record completeness rules as runtime behavior
- creating safety-scoped views, contractor safety packets, utility safety packets, first-responder views, or safety exports
- implementing permission enforcement, RBAC, ABAC, tenant isolation, encryption, telemetry governance, audit policy, or access monitoring for safety records
- treating energy-source, isolation-system, export-capability, operational-mode, or verification-status records as proof of safety, compliance, utility approval, field verification, operational readiness, dispatchability, or device-control authority
- implementing DERMS, dispatch, demand response, VPP, aggregator participation, telemetry-as-truth, command authorization, or operational-control behavior
- changing trust language that could imply safety approval, compliance, utility approval, interconnection approval, field verification, operational readiness, or professional review

## Sources / Provenance

- User-provided Residential Energy Twin Safety Domain doctrine, 2026-06-02
- `AGENTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/architecture/ResidentialEnergyTwinContractV1.md`
- `docs/architecture/TopologyLifecycleDomains.md`
- `docs/architecture/PermissionPlacement.md`
- `docs/architecture/ProvenancePlacement.md`
- `docs/architecture/ViewContracts.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/trust/TRUST_ZONES.md`
- `.codex/project-skills/doctrine-formalization/SKILL.md`
- `.codex/project-skills/provenance-lineage/SKILL.md`
- `/home/mattcoje/.codex/skills/trust-boundary-enforcement/SKILL.md`

## Summary

The Safety Domain defines docs-only Residential Energy Twin doctrine for preserving trusted, provenance-bearing, permissioned safety context about behind-the-meter infrastructure over time. It records safety-relevant information such as energy sources, isolation systems, export capabilities, operational modes, verification status, and provenance while preserving strict boundaries against safety approval, code compliance, field verification, utility approval, operational readiness, runtime implementation, and operational control.
