# 2026-05-27 Provenance API Permission Readiness

## Session Metadata

- Session date: 2026-05-27
- Starting head commit: `304b135`
- Repo commits created this session:
  - none yet

## Implementation Summary

- Continued Trust Boundary + Canonical Authority Stabilization from the completed docs/source-of-truth pass.
- Added backend enum types for authority layer, data classification, and intended API-view audience.
- Added shared additive metadata schemas for view-boundary and permission-readiness descriptions.
- Added provenance-readiness metadata to provenance summaries, recommendation inspectability, recommendation provenance, takeoff line provenance, advisor issue provenance, and scenario comparison lineage summaries.
- Added AI context `view_boundary` and `permission_readiness` metadata to label the existing broad grounding payload as compatibility-oriented, not scoped RBAC output or a source of new canonical facts.
- Added scenario comparison `view_boundary` metadata.
- Added account `permission_readiness` metadata that explicitly marks role, plan, and subscription fields as scaffolding only.
- Added placeholder-estimate authority/classification/limitation metadata.
- Updated source-of-truth and continuity docs for the additive metadata.

## Files Changed

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `apps/api/app/accounts/schemas.py`
- `apps/api/app/core/schemas.py`
- `apps/api/app/core/types.py`
- `apps/api/app/design_advisor/schemas.py`
- `apps/api/app/estimates/router.py`
- `apps/api/app/provenance/schemas.py`
- `apps/api/app/services/ai_context.py`
- `apps/api/app/services/provenance.py`
- `apps/api/app/services/scenario_comparison.py`
- `docs/ACTIVE_TASKS.md`
- `docs/API_CONTRACTS.md`
- `docs/CURRENT_STATE.md`
- `docs/NEXT_STEPS.md`
- `docs/SESSION_LOG.md`
- `docs/provenance/LINEAGE_MODEL.md`
- `docs/security/SCOPED_INTELLIGENCE_OUTPUTS.md`
- `docs/session-continuity/active-pressure-points.md`
- `docs/session-continuity/current-roadmap.md`
- `docs/session-continuity/project-state.md`

## Verification

- `python3 -m unittest discover -s tests -p 'test_*.py'` in `apps/api` passed.
- `python3 -m compileall app` in `apps/api` passed.
- `git diff --check` passed.

## Protections Verified

- No recommendation behavior changed.
- No existing API contract was narrowed or removed.
- No persistence model or migration changed.
- No frontend code changed.
- No RBAC, ABAC, tenant isolation, auth rewrite, telemetry, encryption/KMS, contractor packet, utility export, DER/ADR, or operational-control runtime was introduced.

## Risks And Gaps

- Added metadata changes response shape additively; existing compatibility-sensitive clients should tolerate additive fields, but external strict consumers would still need contract review.
- Field-level data classification is not persisted or enforced.
- Broad AI context remains broad; metadata labels it but does not narrow it.
- Account role, subscription, and plan fields remain scaffolding only.
- A role-aware API view matrix is still not defined.

## Next Recommended Boundary

Define the role-aware API view matrix before implementing RBAC, ABAC, tenant isolation, exports, contractor packets, utility packets, or operational-control views. Decide whether broad AI context should remain one compatibility endpoint or split into explicit consumer-safe, AI-safe, contractor-safe, and future utility-safe view models.
