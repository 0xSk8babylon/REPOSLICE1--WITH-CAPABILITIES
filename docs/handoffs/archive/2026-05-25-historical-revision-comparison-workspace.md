# 2026-05-25 Historical Revision Comparison Workspace

## Session Metadata

- Session date: 2026-05-25
- Starting commit: `a35923d`
- Current head commit before next commit: `a35923d`
- Repo commits created this session:
  - none yet

## Implementation Summary

- Added a dedicated historical revision-comparison workspace to the Scenario Comparison page.
- The new workspace compares saved revision drift per scenario using existing immutable revision snapshots.
- Surfaced drift for:
  - linked design identity
  - design goal
  - design status
  - recommended pathway
  - current-state architecture summary
  - proposed-pathway confidence
  - future-ready and constrained pathway posture
- Kept the comparison deterministic and frontend-only.
- Preserved planning-only trust framing and explicit scope notes that historical comparison is interpretive and does not replay advisor logic against older revisions.

## Files Changed

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `apps/web/src/pages/ScenarioComparisonPage.jsx`
- `apps/web/src/styles/global.css`
- `docs/ACTIVE_TASKS.md`
- `docs/CURRENT_STATE.md`
- `docs/NEXT_STEPS.md`
- `docs/SESSION_LOG.md`
- `docs/handoffs/2026-05-25-historical-revision-comparison-workspace.md`
- `docs/session-continuity/current-roadmap.md`
- `docs/session-continuity/project-state.md`

## Verification Commands And Results

- `npm run build` passed in `apps/web`
- `git diff --check` passed

## Deterministic / Provenance / Trust Protections Verified

- No advisor logic changed
- No backend or persistence changes were required
- Historical comparison is derived from stored immutable revision snapshots only
- Planning-only trust framing remains explicit and historical certainty is not overstated

## Remaining Risks

- Historical comparison currently uses latest-vs-previous revision pairing per scenario rather than arbitrary revision selection
- Stored revision snapshots are compact planning-state framing, not full replayable advisor payloads
- Drift is readable, but not yet connected to diffable reasoning-graph or architecture-map overlays

## Next Recommended Boundary

Deepen the solar-readiness and roof-capacity-realism slice behind the current recommendation architecture while preserving the current planning-state framing, persistent scenario revision layer, historical revision comparison workspace, and planning-only trust boundary.
