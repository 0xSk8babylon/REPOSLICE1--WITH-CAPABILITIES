# Phase 11 Contractor Workflow Readiness Closeout

## Summary

Phase 11A through Phase 11F is implemented in the working tree as an additive read-only backend/API slice.

Added `GET /api/contractor-workflow/homes/{home_id}/readiness` to organize existing contractor-facing planning context into contractor workflow readiness lanes. This opens the Contractor-Owned Workflow Layer as contractor-facing workflow readiness projection only. It is not true contractor-owned persisted workflow state.

## Scope

- Backend read-only contractor workflow readiness schemas.
- Backend read-only contractor workflow readiness route.
- Request-time deterministic contractor workflow readiness service.
- Composition from existing Phase 5 contractor context, Phase 6 planning exchange, Phase 9 estimate readiness, and Phase 10 proposal option sets.
- Phase 7/8 basis carry-through only where already surfaced through existing contracts.
- Homeowner-safe summary and contractor-facing readiness prompts.
- Boundary flags for deferred and forbidden capabilities.
- Focused backend tests.
- Phase 11G through Phase 11I continuity and API docs closeout.

## Readiness Lanes

- planning review
- missing-input review
- confirmation-gate review
- option-candidate review
- proposal-prep blocked/deferred

## Changed Files

- `apps/api/app/contractor_workflow/__init__.py`
- `apps/api/app/contractor_workflow/schemas.py`
- `apps/api/app/contractor_workflow/router.py`
- `apps/api/app/services/contractor_workflow.py`
- `apps/api/app/main.py`
- `apps/api/tests/test_contractor_workflow.py`
- `docs/API_CONTRACTS.md`
- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/handoffs/2026-06-05-phase-11-contractor-workflow-readiness-closeout.md`

## Endpoint Added

- `GET /api/contractor-workflow/homes/{home_id}/readiness`

## Verification

- `git diff --check` - passed.
- `bash scripts/check_session_report_email_env.sh` - passed.
- `cd apps/api && python3 -m unittest tests/test_contractor_workflow.py` - passed, 8 tests in about 141s.
- `pytest` - unavailable in the current environment.
- Full backend unittest discovery previously timed out at 900s with passing dots only.

## Boundary Preserved

Phase 11 remains read-only, additive, request-time derived, `home_id` anchored, deterministic, provenance-bearing, and non-authoritative.

Phase 11 does not add POST/PATCH/DELETE, persistence, migrations, contractor-owned state, contractor accounts, auth/security changes, permission enforcement, approvals, pricing, bids, quotes, final proposal, final estimate, final design, CRM automation, product-runtime email automation, exports, external services, secrets, Phase 12+ work, graph behavior, `twin_id`, operational behavior, or source-of-truth mutation.

## Assumptions

- Existing Phase 5, Phase 6, Phase 9, and Phase 10 outputs are the only source surfaces for the readiness projection.
- Phase 7/8 basis may be carried only when already surfaced through those existing contracts.
- Structured planning records and existing derived views remain authoritative over generated wording.

## Risks / Open Questions

- Focused Phase 11 tests are slow because the endpoint composes expensive existing derived-view stacks.
- Full backend discovery is too slow under the current 900s cap.
- Phase 11 is not committed yet, and the working tree also contains separate session-report email preflight changes.

## Decisions Needed From Matt

- Whether to stage Phase 11 and session-report email preflight as two separate commits with hunk staging for `discovery-index.md`.
- Whether to run a longer full backend test window before commit.

## Next Safe Boundary

Do not proceed into contractor-owned persisted workflow state, contractor accounts, write endpoints, permission enforcement, exports, CRM/email automation, pricing/bids/quotes, final proposal, final estimate, final design, external services/secrets, operational behavior, graph behavior, `twin_id`, or Phase 12+ scope without Matt approval.
