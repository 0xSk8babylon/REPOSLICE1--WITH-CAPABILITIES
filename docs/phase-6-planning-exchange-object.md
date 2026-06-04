# Phase 6 Charter: Planning Exchange Object

## Summary

Phase 6 defines a read-only Planning Exchange Object that packages existing planning context into one portable planning artifact for controlled participant review.

The Planning Exchange Object is a derived package, not a new source of truth. It does not create persistence, migrations, write behavior, exports, PDFs, share links, permission enforcement, participant accounts, marketplace behavior, pricing, proposals, CRM behavior, payments, contractor ranking, final electrical sizing, final install design, or authority over the Residential Energy Twin.

## Product Purpose

Phase 6 answers this product question:

What planning information can be safely exchanged between participants without making the exchange object authoritative, mutable, or final-design-bearing?

The Planning Exchange Object should help a homeowner, contractor, and future qualified reviewers look at the same bounded planning context without converting planning data into a bid, proposal, permit package, utility submission, engineering approval, field verification, or source-of-truth record.

## Exchange Object Role

The Planning Exchange Object is:

- home_id anchored
- read-only
- request-time derived
- deterministic for the same inputs
- provenance-bearing
- non-authoritative
- additive to existing API surfaces
- composed from existing planning and contractor-context outputs
- scoped to participant review preparation

The Planning Exchange Object is not:

- a persisted exchange record
- a Residential Energy Twin aggregate or `twin_id`
- a source of truth
- an export, PDF, report, share link, or partner API
- a permission grant, consent artifact, auth role, or enforcement layer
- a contractor account, CRM workflow, marketplace object, bid, quote, proposal, or payment workflow
- a product recommendation, product ranking, compatibility engine, or procurement decision
- a final electrical design, stamped engineering conclusion, AHJ approval, utility approval, safety approval, or field verification

## Source Composition

Phase 6 runtime work must compose existing outputs instead of duplicating planning interpretation:

existing planning context + Phase 5 contractor-context views -> read-only Planning Exchange Object

Allowed source views include:

- `TwinPlanningContext`
- `TwinRuntimeProjectionView.contractor`
- Phase 3 and Phase 4 trust/provenance/readiness outputs when already used by existing services
- `ContractorPlanningContextView` from Phase 5B
- `ContractorConfirmationGateProjectionView` from Phase 5C
- `ContractorInstallComplexityView` from Phase 5D

The Planning Exchange Object may organize:

- homeowner intent and goals
- home/site planning context
- known electrical equipment summary
- proposed system context
- contractor-safe planning context
- confirmation gates
- install complexity and uncertainty signals
- provenance and trust-basis metadata
- missing information
- required verifiers
- review prompts
- limitations
- deferred boundaries

## Participant Boundary

The first Phase 6 participant boundary is planning review only.

Allowed participant uses:

- homeowner review of what planning context is visible
- contractor scoping preparation
- contractor review preparation
- future qualified professional review preparation
- future estimate-readiness input review
- future proposal-option input review

Not allowed:

- treating the package as authorization to share data externally
- treating the package as permission enforcement
- treating the package as contractor assignment, bid request, or proposal request
- treating the package as final design input without separate qualified review
- treating the package as AHJ, utility, permit, safety, or field-verification evidence

## Provenance And Trust Rules

Every section of the Planning Exchange Object must preserve:

- source view names
- source field paths
- source references when available
- derived-from lineage
- authority layer
- data classification
- data origin where available
- missing inputs
- required verifiers
- review prompts
- limitations
- deferred boundaries

Source or trust categories should use this fixed vocabulary:

- `homeowner_provided`
- `app_derived`
- `contractor_safe_projection`
- `manufacturer_required_future`
- `ahj_utility_dependent_future`
- `missing_unknown`

The object must not hide uncertainty to make the package look complete. Readiness language must remain planning-only and must not become approval, readiness certification, or pass/fail scoring.

## Phase 6 Sequence

### Phase 6A - Planning Exchange Object Charter

Docs-only charter defining object purpose, participants, visibility boundaries, source/basis rules, non-authoritative posture, deferred scope, and verification requirements.

### Phase 6B - Read-only Exchange Object Schema

Backend schema/contract defining the response shape for a read-only exchange object. The schema must compose existing planning and contractor-context outputs and must not create a persisted model.

### Phase 6C - Exchange Package Endpoint

Backend read-only derived endpoint:

`GET /api/planning-exchange/homes/{home_id}`

The endpoint must be home_id anchored, read-only, request-time derived, deterministic, provenance-bearing, non-authoritative, additive only, and must not write, persist, export, or enforce permissions.

### Phase 6D - Exchange Provenance / Trust Boundary Mapping

Backend and docs mapping for where each exchange section came from:

- homeowner-provided
- app-derived
- contractor-safe projection
- manufacturer-required/future
- AHJ/utility-dependent/future
- missing/unknown

### Phase 6E - Exchange Readiness Summary

Backend and docs summary of whether the exchange object is ready for participant review, contractor review, estimate-readiness input review, or later proposal-option input review. Readiness means planning-review posture only, not approval or final design readiness.

## Forbidden Scope

Phase 6 does not approve:

- persistence
- migrations
- write endpoints
- exports, PDFs, report generation, or share links
- auth, security, RBAC, ABAC, or permission enforcement changes
- contractor accounts
- source-of-truth mutation
- frontend work
- marketplace, bidding, contractor ranking, CRM, payment, pricing, proposal, or quote behavior
- product recommendations, product selection, product ranking, compatibility engines, vendor scraping, supplier integrations, or procurement logic
- scenario simulation, what-if analysis, optimization, calculated change analysis, or final design guidance
- `twin_id`, canonical Twin runtime identity, graph database, graph engine, canonical topology table, or new source-of-truth model
- final wire sizing, final conduit sizing, final breaker sizing, final disconnect requirements, NEC/code-compliant installation design, permitting conclusions, AHJ approval, utility approval, safety approval, or field-verification approval
- git push, production deployment, external services, secrets, destructive commands, broad refactors, or unrelated repo changes

## Verification Requirements

Each Phase 6 slice must pass checkpoint gates before continuing:

- `git status --short`
- `git diff --check`
- targeted backend tests when runtime code changes
- compile checks for touched Python files when applicable
- confirmation that no forbidden scope occurred
- confirmation that runtime remains read-only and deterministic
- confirmation that provenance/trust basis is preserved
- confirmation that no final electrical design or sizing claims were introduced
- confirmation that no export, share, persistence, or write behavior was introduced

No staging, commit, or push may occur without explicit Matt approval.

## Current State

- Phase 5 Contractor Participant Foundation is complete.
- Phase 5B through Phase 5D provide read-only contractor-context runtime inputs.
- Phase 6 starts from a clean local worktree and must remain additive.
