# Phase 5 Charter: Contractor Participant Foundation

## Summary

Phase 5A is approved as the docs-only Contractor Participant Charter checkpoint. This document defines the Phase 5 Contractor Participant Foundation boundary and records the approved Phase 5A through Phase 5E sequence.

Phase 5A approval did not approve Phase 5B through Phase 5E completion by itself. Phase 5B through Phase 5D runtime slices require the approved read-only derived endpoint boundaries and checkpoint verification. Phase 5E is docs-only doctrine for possible future contractor observations and does not approve observation implementation, runtime/API/schema/persistence work, auth/security or permission enforcement changes, write endpoints, contractor accounts, marketplace behavior, or final electrical design logic.

## Product Purpose

Phase 5 turns the existing planning intelligence foundation into a contractor-safe participant workflow foundation.

Under this charter, the contractor is a permission-scoped planning participant who may receive minimized, read-only planning context for scoping, site-walk preparation, route review, equipment coordination, installation planning input, uncertainty review, and future field-observation contribution. Contractor participation does not create authority over the Residential Energy Twin, homeowner permission, canonical planning truth, final electrical design, AHJ/utility decisions, bids, proposals, procurement, marketplace ranking, CRM workflows, or operational behavior.

## Contractor Participant Role

The contractor participant role is:

- purpose-bound to planning review and field-verification preparation
- homeowner permission-scoped in doctrine, while runtime permission enforcement remains deferred
- read-only for Phase 5B through Phase 5D runtime foundations
- provenance-preserving and trust-boundary preserving
- bounded to known facts, missing inputs, uncertainty, review burden, required verifier, field-verification needs, and safe next review prompts

The contractor role is not:

- a source-of-truth owner
- an account or auth role
- a permission grant by itself
- an engineering approval role
- an AHJ or utility authority
- a bid, proposal, sales, marketplace, ranking, or CRM actor
- an operational-control actor

## Contractor-Safe Visibility Model

Contractor-safe visibility should expose the minimum planning context needed for an approved contractor purpose.

Allowed contractor-safe visibility may include:

- recorded homeowner goals relevant to the project
- home/site planning summary
- known electrical equipment summary
- proposed system context and planning-only design context
- selected topology and pathway context when already available from read-only derived views
- missing information
- field-verification needs
- contractor review needs
- install complexity and uncertainty signals
- provenance, trust, confidence, missing-data, unsafe-assumption, limitation, and deferred-boundary notes
- permission-readiness notes that preserve the fact that enforcement is not active
- contractor-safe next review prompts framed as planning review prompts

Contractor-safe visibility must exclude:

- unrelated homeowner notes or household/private context
- broad source-document access unless specifically included by a future approved view contract
- raw internal governance context not needed for contractor scoping
- account, billing, auth, or subscription details
- utility credentials, utility submission claims, interconnection authority, or operational-control context
- proposal generation, quotes, bid logic, pricing, savings, payback, or financial claims
- final product selection, product ranking, procurement, marketplace, vendor, or compatibility-engine decisions
- stamped engineering conclusions, final electrical sizing, permit approval, AHJ approval, utility approval, safety approval, or field-verification approval

## Mutability Boundary

Phase 5 contractor runtime foundations must be read-only.

Contractors cannot mutate:

- homeowner-provided data
- app-derived data
- manufacturer data
- AHJ data
- utility data
- canonical planning truth
- Residential Energy Twin source-of-truth concepts
- permission grants, consent artifacts, or authorization state
- scenario records, designs, takeoffs, source documents, or provenance records

Future contractor observations may be modeled later as append-only participant input only after separate approval. They must not silently overwrite any existing source or derived fact.

## Trust And Provenance Boundaries

Every contractor-facing planning output should preserve:

- source or basis
- provenance references where available
- confidence or uncertainty posture
- missing inputs
- assumptions
- limitations
- required verifier
- authority boundary
- permission-readiness posture
- advisory-only and planning-only language

Contractor-facing output must not imply:

- engineering certification
- code compliance
- permit readiness
- AHJ or utility approval
- safety approval
- field verification completion
- contractor readiness as a pass/fail verdict
- final install design readiness
- bid, proposal, savings, compatibility, procurement, or operational readiness
- permission enforcement, active consent, scoped export authority, or contractor account access

## Confirmation Gate Lifecycle

Phase 5C exposes confirmation gates as structured read-only readiness items inside the approved boundary. Gate status is derived only and is not persisted in Phase 5C.

Allowed derived statuses:

- `unknown`
- `homeowner_provided`
- `app_derived`
- `contractor_review_required`
- `contractor_confirmed_future`
- `contractor_rejected_future`
- `needs_site_visit`
- `ahj_or_utility_dependent`

The required 19 confirmation gates are:

Gate titles describe review topics only; they do not mean the app has performed or approved the underlying engineering review.

1. Product specs verified
2. Nameplate ratings verified
3. Manufacturer install manual reviewed
4. Circuit purpose confirmed
5. Load/current assumptions confirmed
6. Distance measurements confirmed
7. Conduit/routing path confirmed
8. Indoor/outdoor/wet location confirmed
9. Conductor material confirmed
10. Raceway type confirmed
11. Number of current-carrying conductors confirmed
12. Derating factors applied
13. Voltage drop reviewed
14. Disconnect requirements reviewed
15. Overcurrent protection reviewed
16. Grounding/bonding reviewed
17. Labeling/signage requirements reviewed
18. Utility/AHJ requirements reviewed
19. Contractor final review completed

Each gate should include:

- `gate_id`
- `title`
- `category`
- `status`
- `required_verifier`
- `source_or_basis`
- `blocker_level`
- `reason`
- `next_action`
- `provenance`

Gate projection must identify readiness, missing data, uncertainty, review burden, and the next safe review step. It must not claim that final wire size, conduit size, breaker size, disconnect requirements, or code-compliant installation design has been calculated or approved.

## Install Complexity Categories

Phase 5D exposes contractor-safe install uncertainty and review-burden signals only inside the approved boundary.

Allowed signal categories:

- product uncertainty
- nameplate uncertainty
- panel/service uncertainty
- routing/path uncertainty
- backup scope uncertainty
- AHJ/utility uncertainty
- material/takeoff uncertainty
- field verification burden
- homeowner decision dependency
- contractor review burden

Allowed severity labels:

- `low`
- `medium`
- `high`
- `blocked`
- `unknown`

Each signal should include:

- `signal_id`
- `category`
- `severity`
- `reason`
- `missing_inputs`
- `required_verifier`
- `next_action`
- `source_or_basis`
- `provenance`

Install complexity reasoning must say only what is uncertain, missing, needs review, or depends on contractor/AHJ/utility confirmation.

It must not calculate or claim final:

- wire size
- conduit size
- breaker size
- disconnect requirement
- NEC-compliant installation design

## Phase 5E Future Contractor Observation Doctrine

Phase 5E is docs-only. It defines future contractor observations as append-only participant input doctrine before any observation intake, POST endpoints, persistence, migrations, contractor accounts, observation tables, or mutation workflows are approved.

Future contractor observations, if separately approved later, should be append-only participant input. They are evidence candidates for review, not canonical truth, verified fact, field-verification completion, engineering approval, AHJ/utility approval, contractor directive, proposal input, bid input, or source-of-truth mutation.

They must not automatically overwrite:

- homeowner-provided data
- app-derived data
- manufacturer data
- AHJ data
- utility data
- canonical planning truth
- Residential Energy Twin source of truth

They must preserve:

- observation source and submitter context
- affected planning topic or equipment context
- source_or_basis
- provenance
- confidence or uncertainty label
- missing inputs
- limitations
- required reviewer or verifier
- non-authoritative status until accepted through a separately approved future workflow

Future observation types may include:

- field measurement
- equipment correction
- install concern
- routing issue
- AHJ/utility note
- product substitution concern
- missing information
- homeowner decision dependency
- site access issue
- material availability concern

Future observation lifecycle states may include:

- `submitted_future`
- `reviewed_future`
- `accepted_as_evidence_future`
- `rejected_future`
- `superseded_future`

Future observation handling must remain append-only even when an observation is later accepted as evidence. Acceptance as evidence may support a future review workflow, but it must not directly replace homeowner-provided data, app-derived data, manufacturer data, AHJ data, utility data, canonical planning truth, or Residential Energy Twin source-of-truth records without a separately approved source-of-truth update path.

Phase 5E does not implement:

- POST, PUT, PATCH, or DELETE endpoints
- persistence, migrations, observation tables, or event logs
- contractor accounts
- auth/security or permission enforcement changes
- source-of-truth mutation
- exports or contractor packets
- marketplace, bidding, ranking, CRM, payment, pricing, proposal, or takeoff behavior
- final electrical sizing, final NEC/code-compliant installation design, or AHJ/utility approval logic

## Internal Checkpoints

Phase 5 proceeds as one coordinated automated sequence with checkpoint gates after each slice:

- Phase 5A: Contractor Participant Charter, docs-only.
- Phase 5B: Contractor-Scoped Planning View, backend read-only derived view.
- Phase 5C: Confirmation Gate Projection, backend read-only derived projection.
- Phase 5D: Install Complexity Signals, backend read-only derived reasoning.
- Phase 5E: Contractor Observation Doctrine, docs-only.

No commit should be created until Matt explicitly approves. Prefer one clean final commit after Phase 5A through Phase 5E pass verification unless diff size suggests separate checkpoint commits and Matt approves that split.

## Phase 5 Runtime Boundary

The approved Phase 5B runtime slice adds:

- `GET /api/contractor-context/homes/{home_id}`
- contractor-safe planning context schemas
- service derivation from existing read-only planning context and derived intelligence surfaces
- focused backend tests

Phase 5B includes only read-only derived content:

- homeowner goals
- home/site planning summary
- known electrical equipment summary
- proposed system context
- missing information
- contractor verification needs
- provenance/trust notes
- permission-readiness notes
- next safe contractor review prompts

Phase 5B must not add persistence, migrations, auth expansion, contractor accounts, writes, source-of-truth mutation, frontend work, exports, marketplace behavior, CRM behavior, pricing, proposals, or final electrical sizing claims.

The approved Phase 5C runtime slice adds:

- `GET /api/contractor-context/homes/{home_id}/confirmation-gates`
- contractor-safe confirmation gate projection schemas
- deterministic 19-gate projection logic
- focused backend tests

Phase 5C must keep gate status read-only and derived. Gate status must not imply final approval, compliance, completion, field verification, AHJ/utility approval, contractor confirmation, or persisted gate state.

The approved Phase 5D runtime slice adds:

- `GET /api/contractor-context/homes/{home_id}/install-complexity`
- contractor-safe install complexity/uncertainty signal schemas
- deterministic review-burden and uncertainty signal logic
- focused backend tests

Phase 5D must expose only missing inputs, uncertainty, review burden, required verifier, next action, source/basis, provenance, and limitations. It must not calculate or claim final wire size, conduit size, breaker size, disconnect requirement, or NEC/code-compliant installation design.

## Forbidden Scope

This Phase 5A charter and the Phase 5A checkpoint do not approve:

- backend implementation during Phase 5A
- frontend implementation unless separately approved
- persistence changes
- migrations
- auth, RBAC, ABAC, privacy/security enforcement, or permission enforcement
- contractor accounts
- write endpoints
- source-of-truth mutation
- scoped exports or contractor packets
- marketplace features
- bidding, proposals, pricing, quotes, savings, payback, incentives, or financial logic
- contractor ranking
- CRM integration
- payments
- product recommendations, product ranking, procurement, vendor scraping, supplier integrations, or compatibility engines
- scenario simulation, what-if analysis, optimization, or best-option selection
- final wire sizing, conduit sizing, breaker sizing, disconnect requirements, or final NEC-compliant installation design
- AHJ approval, utility approval, permit approval, safety approval, field-verification approval, stamped-engineering claims, or operational readiness claims
- utility participation, DERMS, dispatch, telemetry governance, or operational control
- canonical `twin_id`, graph database, graph engine, or canonical Residential Energy Twin runtime model
- git push or production deployment

## Verification Requirements

Docs-only checkpoints must run:

- `git status --short`
- `git diff --check`

Runtime checkpoints must run:

- `git status --short`
- `git diff --check`
- targeted backend tests
- deterministic same-input/same-output tests for derived outputs
- traceability checks for source/basis, missing inputs, assumptions, limitations, and deferred boundaries

Final closeout before any commit must report:

- all changed files
- all endpoints added
- all tests run
- `git diff --check`
- targeted backend tests
- confirmation that no forbidden scope occurred
- confirmation that no migrations occurred
- confirmation that no auth/security changes occurred
- confirmation that no write endpoints occurred
- confirmation that no final electrical sizing claims occurred

## Current State

- Phase 4 is closed out and committed in `74448241f955d6a5b98ff09d0c2ddf6edb117dbd`.
- Phase 5A is approved as a docs-only charter checkpoint.
- Phase 5B through Phase 5D are approved read-only, request-time, deterministic, `home_id`-anchored runtime foundations inside the contractor participant boundary.
- Phase 5E is approved as docs-only contractor observation doctrine.
- Phase 5A through Phase 5E do not approve persistence, migrations, auth/security changes, permission enforcement, write endpoints, contractor accounts, exports, frontend work, marketplace behavior, CRM behavior, payments, pricing/proposals, source-of-truth mutation, or final electrical sizing/design claims.
