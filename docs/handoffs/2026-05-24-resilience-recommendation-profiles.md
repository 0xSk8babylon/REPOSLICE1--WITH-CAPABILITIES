# 2026-05-24 Resilience Recommendation Profiles

## What Changed

- Added a deterministic resilience recommendation-profile architecture to the advisor layer.
- Introduced four recommendation philosophies:
  - Critical / Efficient
  - Balanced
  - Conservative
  - Premium / Future-Ready
- Added new internal enums and advisor schemas for battery posture, solar posture, autonomy reserve posture, future growth margin posture, and low-solar assumption posture.
- Added additive `recommendation_profiles` output to `GET /api/design-advisor/summary/{design_id}`.
- Added rule provenance support for the recommendation-profile matrix.
- Added a new advisor UI section that presents the profiles as planning guidance without exposing raw sizing math.

## Architecture Impact

- Runtime architecture changed additively inside the advisor layer only.
- No schema migration or persistence change was required.
- The new service sits above `design_analysis_service` and below the current advisor presentation layer.

## Why This Slice

- It formalizes recommendation philosophy before deeper sizing implementation.
- It keeps deterministic logic internal and preserves trust boundaries.
- It creates a stable contract for future numeric sizing work without forcing premature data-model expansion.

## Remaining Gaps

- The model currently expresses posture, not full deterministic sizing outputs.
- Scenario scoring and recommendation profiles remain separate for now.
- Recommendation input provenance is only partially explicit and should deepen as sizing implementation grows.

## Next Recommended Step

Implement the first internal sizing rule layer behind the recommendation profiles, beginning with battery/autonomy posture logic and provenance-aware basis reporting while keeping formulas internal.
