# 2026-05-25 Persistent Scenario / Revision Foundation

## Session Metadata

- Session date: 2026-05-25
- Starting commit: `7412538`
- Current head commit before next commit: `7412538`
- Repo commits created this session:
  - none yet

## Implementation Summary

- Added a lightweight immutable `scenario_revisions` persistence layer under the existing saved scenario model.
- Saved scenarios now accumulate:
  - revision identity
  - revision lineage
  - revision timestamps
  - linked design identity
  - compact planning-state framing derived from deterministic advisor output
- Preserved the live editable scenario row as the current workspace anchor.
- Extended scenario responses with additive revision metadata and added `GET /api/scenarios/{scenario_id}/revisions`.
- Extended Design Advisor planning-state links so saved scenarios can expose latest revision identity when historical state exists.
- Surfaced revision framing in the Design Advisor and Scenario Comparison UI without introducing a broad version-control or revision-browser system.

## Files Changed

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `apps/api/app/core/models.py`
- `apps/api/app/core/repository.py`
- `apps/api/app/design_advisor/schemas.py`
- `apps/api/app/scenarios/router.py`
- `apps/api/app/scenarios/schemas.py`
- `apps/api/app/seed/runtime.py`
- `apps/api/app/services/design_advisor.py`
- `apps/api/app/services/scenario_revision.py`
- `apps/api/tests/test_resilience_recommendation.py`
- `apps/api/tests/test_scenario_revisions.py`
- `apps/web/src/pages/DesignAdvisorPage.jsx`
- `apps/web/src/pages/ScenarioComparisonPage.jsx`
- `docs/API_CONTRACTS.md`
- `docs/ACTIVE_TASKS.md`
- `docs/CURRENT_STATE.md`
- `docs/NEXT_STEPS.md`
- `docs/SESSION_LOG.md`
- `docs/handoffs/2026-05-25-persistent-scenario-revision-foundation.md`
- `docs/session-continuity/current-roadmap.md`
- `docs/session-continuity/project-state.md`

## Verification Commands And Results

- `python3 -m unittest discover -s tests -p 'test_scenario_revisions.py'` passed in `apps/api`
- `python3 -m unittest discover -s tests -p 'test_resilience_recommendation.py'` passed in `apps/api`
- `python3 -m compileall app` passed in `apps/api`
- `npm run build` passed in `apps/web`
- `git diff --check` passed

## Deterministic / Provenance / Trust Protections Verified

- Advisor logic remained deterministic and unchanged
- Persistence and API evolution stayed additive
- Historical framing remains explicit about being planning-only revision context, not final engineering state
- Live scenario editing remains separate from immutable saved revision history

## Remaining Risks

- Scenario revisions currently store compact planning-state framing rather than full historical advisor payloads
- Historical revisions are not yet replayable as first-class advisor workspaces
- Existing local databases may need reseeding or startup backfill to create baseline revisions for older saved scenarios

## Next Recommended Boundary

Deepen the solar-readiness and roof-capacity-realism slice behind the current recommendation architecture while preserving the current planning-state framing, revision identity surface, pathway comparison workspace, and planning-only trust boundary.
