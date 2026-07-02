# Phase 13 Post-Install Retention & CRM Handoff Closeout

## Summary

Phase 13 is implemented in the working tree and not staged or committed.

Added `GET /api/post-install/homes/{home_id}` and `GET /api/crm-handoff/homes/{home_id}` as additive read-only backend/API surfaces. The post-install view derives manual retention readiness, fixed retention opportunities, request-time lifecycle event detections, follow-up readiness notes, blockers, missing inputs, confirmation gates, and provenance basis. The CRM handoff endpoint shapes that post-install context into a deterministic manual handoff object only.

## Scope

- Phase 13A: post-install state view.
- Phase 13B: retention opportunity identification.
- Phase 13C: lifecycle event detection.
- Phase 13D: CRM handoff object.
- Phase 13E: follow-up readiness.

## Runtime Endpoints

- `GET /api/post-install/homes/{home_id}`
- `GET /api/crm-handoff/homes/{home_id}`

## Changed Files

- `apps/api/app/main.py`
- `apps/api/app/post_install/__init__.py`
- `apps/api/app/post_install/router.py`
- `apps/api/app/post_install/schemas.py`
- `apps/api/app/services/post_install.py`
- `apps/api/app/crm_handoff/__init__.py`
- `apps/api/app/crm_handoff/router.py`
- `apps/api/app/crm_handoff/schemas.py`
- `apps/api/app/services/crm_handoff.py`
- `apps/api/tests/test_phase13_post_install_crm.py`
- `docs/API_CONTRACTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/handoffs/2026-06-05-phase-13-post-install-retention-crm-handoff-closeout.md`

## Boundary

Phase 13 remains read-only, additive, request-time derived, deterministic, provenance-bearing, non-authoritative, and `home_id` anchored.

Runtime composes Phase 11 contractor workflow readiness and Phase 12 product preference metadata directly. Phase 9/10 references are carried only where those Phase 11/12 source contracts already surface them.

## Explicit Non-Goals

Phase 13 does not add persistence, migrations, write endpoints, auth/security changes, permission enforcement, external CRM integration, CRM writes, CRM record creation, email/drip campaign product behavior, task creation, sales scoring, lead scoring, ranking, best upsell logic, push behavior, frontend work, exports, pricing, proposal generation, external services, secrets, `twin_id`, graph behavior, operational behavior, or source-of-truth mutation.

## Verification

Passed so far:

- `python3 -m py_compile apps/api/app/post_install/schemas.py apps/api/app/post_install/router.py apps/api/app/services/post_install.py apps/api/app/crm_handoff/schemas.py apps/api/app/crm_handoff/router.py apps/api/app/services/crm_handoff.py apps/api/app/main.py apps/api/tests/test_phase13_post_install_crm.py`
- `python3 -m unittest tests.test_phase13_post_install_crm` from `apps/api`: `6 tests OK` in `0.694s`

Pending final stabilization:

- `git diff --check`
- final `git status --short`

## Test Path Note

The initial focused test path rebuilt expensive Phase 9-12 source stacks and appeared overlong. The final focused Phase 13 test uses deterministic Phase 11/12 source fixtures to verify Phase 13 behavior directly: route registration, `home_id` anchoring, deterministic ordering, no persistence mutation, false forbidden-scope flags, post-install state/opportunity/lifecycle/readiness metadata, CRM handoff object boundaries, and source/provenance basis.

## Risks / Open Questions

- Broader backend discovery was not run before this handoff because adjacent Phase 11/12 derived-view integration tests are known slow and prior broad discovery timed out under the current cap.
- Phase 13 is not staged or committed.

## Next Safe Boundary

Run final stabilization verification, send the stabilization email, report final changed files and git status, then stop without staging, committing, or pushing unless Matt explicitly approves a separate commit boundary.
