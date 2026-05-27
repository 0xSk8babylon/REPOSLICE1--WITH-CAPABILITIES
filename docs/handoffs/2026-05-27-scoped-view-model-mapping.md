# 2026-05-27 Scoped View-Model Mapping

## Session Metadata

- Session date: 2026-05-27
- Starting head commit: `c67b693`
- Repo commits created this session:
  - none yet

## Implementation Summary

- Restored from the latest clean state and recent handoffs.
- Added `docs/security/SCOPED_VIEW_MODEL_MAPPING.md` as the source-of-truth contract-design map for scoped response/view boundaries.
- Mapped consumer-safe, AI-safe, contractor-safe, and future utility-safe audience boundaries.
- Identified current broad/raw exposure across AI context, home/design/advisor/scenario/load/pathway/takeoff/product/provenance/account surfaces.
- Defined narrowing candidates such as `AIDesignGroundingView`, `ConsumerAdvisorSummaryView`, `ContractorPlanningBasisView`, and future utility-safe abstractions.
- Cross-linked the mapping from API contracts, scoped intelligence outputs, discovery routing, current state, next steps, active tasks, pressure points, roadmap, and unresolved architecture.

## Files Changed

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `discovery-index.md`
- `docs/ACTIVE_TASKS.md`
- `docs/API_CONTRACTS.md`
- `docs/CURRENT_STATE.md`
- `docs/NEXT_STEPS.md`
- `docs/SESSION_LOG.md`
- `docs/continuity/UNRESOLVED_ARCHITECTURE.md`
- `docs/governance/GOVERNANCE_GAP_ANALYSIS.md`
- `docs/security/SCOPED_INTELLIGENCE_OUTPUTS.md`
- `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
- `docs/session-continuity/active-pressure-points.md`
- `docs/session-continuity/current-roadmap.md`

## Verification

- `git diff --check` passed.
- No backend/frontend tests were required because only documentation changed.

## Protections Verified

- No runtime behavior changed.
- No recommendation behavior changed.
- No API response shape was changed.
- No persistence model, migration, frontend, auth rewrite, telemetry, encryption/KMS, RBAC, ABAC, tenant isolation, scoped filtering, contractor packet, utility packet, export, DER/ADR, or operational-control behavior was introduced.
- Current broad endpoints remain compatibility surfaces, not scoped enforcement views.

## Risks And Gaps

- Scoped view models are mapped but not implemented as schemas or endpoints.
- Broad AI context remains broad and compatibility-oriented.
- Field-level data classification and provenance are still partial.
- Account role, plan, and subscription fields remain scaffolding only.
- Future strict clients still need explicit contract review because even additive metadata can be rejected by rigid clients.

## Next Recommended Boundary

If continuing scoped-view work, add explicit view schemas first and preserve existing GET contracts. The narrowest first implementation candidate is an additive AI-safe design grounding view that summarizes the current broad AI context without turning it into RBAC, export, contractor, utility, or operational-control behavior.
