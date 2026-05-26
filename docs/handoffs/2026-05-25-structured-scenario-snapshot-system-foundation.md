# 2026-05-25 Structured Scenario / Snapshot System Foundation

## Session Metadata

- Session date: 2026-05-25
- Starting commit: `befd05e`
- Current head commit before next commit: `befd05e`
- Repo commits created this session:
  - none yet

## Implementation Summary

- Added an additive `planning_state` envelope to the Design Advisor API so recommendation, architecture, reasoning, and pathway-comparison outputs are explicitly tied to a named live design state.
- The new snapshot envelope includes:
  - snapshot identity and version framing
  - generated planning-state variants for current state, proposed pathway, future-ready pathway, and constrained/minimal-upgrade pathway
  - linked saved-scenario metadata for the current design
- Added snapshot-oriented UI framing to the Design Advisor so users can see that advisor outputs belong to a specific planning state without introducing a broad version-management workflow.
- Kept scenario/snapshot handling deterministic and inspectable.
- Preserved the existing reasoning graph, architecture visuals, and pathway-comparison surfaces.
- Kept persistence changes intentionally minimal: saved scenarios act as linked metadata anchors, while advisor logic still runs against the current linked design state only.

## Files Changed

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `apps/api/app/design_advisor/schemas.py`
- `apps/api/app/services/design_advisor.py`
- `apps/api/tests/test_resilience_recommendation.py`
- `apps/web/src/pages/DesignAdvisorPage.jsx`
- `apps/web/src/styles/global.css`
- `docs/API_CONTRACTS.md`
- `docs/ACTIVE_TASKS.md`
- `docs/CURRENT_STATE.md`
- `docs/NEXT_STEPS.md`
- `docs/SESSION_LOG.md`
- `docs/handoffs/2026-05-25-structured-scenario-snapshot-system-foundation.md`
- `docs/session-continuity/current-roadmap.md`
- `docs/session-continuity/project-state.md`

## Verification Commands And Results

- `python3 -m unittest discover -s tests -p 'test_resilience_recommendation.py'` passed in `apps/api`
- `python3 -m compileall app` passed in `apps/api`
- `npm run build` passed in `apps/web`
- `git diff --check` passed

## Deterministic / Provenance / Trust Protections Verified

- Advisor logic stayed deterministic and unchanged
- API evolution was additive only
- Snapshot framing is explicit about being planning-state identity rather than a stored engineering revision
- Linked scenarios remain visible as metadata anchors without implying scenario-specific recommendation persistence

## Remaining Risks

- The new `planning_state` layer does not yet persist historical advisor-result snapshots or full revision history
- Linked scenarios now help anchor planning identity, but the advisor still evaluates the current linked design state rather than scenario-specific stored advisor states
- If later work introduces many saved snapshots, the current lightweight card-based presentation will need a richer browsing model

## Next Recommended Boundary

Deepen the solar-readiness and roof-capacity-realism slice behind the current recommendation architecture while preserving the new planning-state framing, pathway-comparison workspace, architecture visuals, and planning-only trust boundary.
