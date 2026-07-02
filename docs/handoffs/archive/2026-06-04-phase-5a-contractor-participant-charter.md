# Phase 5A Contractor Participant Charter

## Summary

Phase 5A Contractor Participant Charter is complete as docs-only boundary work. Phase 5 runtime implementation has not started from Phase 5A alone.

## Scope

- Adopted the Phase 5A charter at `docs/phase-5-contractor-participant-foundation.md`.
- Updated compact discovery continuity in `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`.
- Recorded Phase 4 closeout commit `74448241f955d6a5b98ff09d0c2ddf6edb117dbd` as the current starting point for Phase 5.
- Defined the contractor participant role, contractor-safe visibility model, read-only mutability boundary, trust/provenance boundaries, confirmation gate lifecycle, install complexity categories, future contractor observation doctrine, forbidden scope, verification requirements, and approved Phase 5B runtime boundary.

## Contractor Participant Boundary

The contractor participant role is purpose-bound to planning review, site-walk preparation, route review, equipment coordination, install uncertainty review, field-verification preparation, and future append-only observation contribution.

The contractor participant role is not a source-of-truth owner, account role, permission grant, engineering approval role, AHJ or utility authority, marketplace actor, proposal actor, CRM actor, or operational-control actor.

## Contractor-Safe Visibility

Approved future contractor-safe runtime visibility may include homeowner goals, home/site planning summary, known equipment summary, proposed system context, missing information, contractor verification needs, provenance/trust notes, permission-readiness notes, and next safe review prompts.

It must exclude unrelated homeowner/private context, broad source documents unless separately approved, account/auth/billing context, utility credentials, proposal/pricing/bid logic, product ranking/procurement, final electrical sizing, approval claims, and operational-control context.

## Confirmation Gate Lifecycle

Phase 5C may expose the 19 homeowner/contractor confirmation gates as structured read-only readiness items if it remains inside the approved boundary. Gate status must be derived only and must not persist state in Phase 5C.

Gate titles describe review topics only; they do not mean the app has performed or approved the underlying engineering review.

Allowed statuses are `unknown`, `homeowner_provided`, `app_derived`, `contractor_review_required`, `contractor_confirmed_future`, `contractor_rejected_future`, `needs_site_visit`, and `ahj_or_utility_dependent`.

## Install Complexity Categories

Phase 5D may expose contractor-safe install uncertainty and review-burden signals across product uncertainty, nameplate uncertainty, panel/service uncertainty, routing/path uncertainty, backup scope uncertainty, AHJ/utility uncertainty, material/takeoff uncertainty, field verification burden, homeowner decision dependency, and contractor review burden.

Install complexity output must not calculate or claim final wire size, conduit size, breaker size, disconnect requirements, or NEC-compliant installation design.

## Contractor Observation Doctrine

Phase 5E should document future contractor observations as append-only participant input. Future observations must not automatically overwrite homeowner-provided data, app-derived data, manufacturer data, AHJ data, utility data, canonical planning truth, or the Residential Energy Twin source of truth.

Future observation lifecycle states may include `submitted_future`, `reviewed_future`, `accepted_as_evidence_future`, `rejected_future`, and `superseded_future`.

## Approved Phase 5B Implementation Boundary

Phase 5B may add a backend read-only derived contractor-safe planning context endpoint:

- `GET /api/contractor-context/homes/{home_id}`

The endpoint should derive from existing planning context and derived intelligence surfaces and expose only contractor-safe planning context, missing information, verification needs, trust/provenance notes, permission-readiness notes, and safe contractor review prompts.

Phase 5B must not add persistence, migrations, auth expansion, contractor accounts, writes, frontend work, exports, marketplace/CRM behavior, pricing, proposals, source-of-truth mutation, or final electrical sizing claims.

## Verification

Phase 5A checkpoint verification:

- `git status --short` showed only Phase 5A docs/continuity changes before this handoff was created.
- `git diff --check` passed before this handoff was created.
- Backend tests were not required for Phase 5A because this checkpoint is docs-only.

## Restore Guidance

For Phase 5A charter state, load:

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/phase-5-contractor-participant-foundation.md`
- `docs/handoffs/2026-06-04-phase-5a-contractor-participant-charter.md`

Phase 5B runtime implementation may proceed only inside the approved read-only derived endpoint boundary.
