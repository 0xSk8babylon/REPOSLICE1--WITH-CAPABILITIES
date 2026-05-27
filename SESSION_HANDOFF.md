# Session Handoff

## Updated

2026-05-27

## Session Summary

- Session date: 2026-05-27
- Starting head commit: `c67b693`
- Repo commits created this session:
  - none yet

## What Changed Last

- Restored from the latest clean state and recent handoffs.
- Added `docs/security/SCOPED_VIEW_MODEL_MAPPING.md` as the source-of-truth map for scoped response/view boundaries.
- Mapped consumer-safe, AI-safe, contractor-safe, and future utility-safe audience boundaries.
- Identified broad/raw exposure surfaces and narrowing candidates for AI context, home/design/advisor/scenario/load/pathway/takeoff/product/provenance/account responses.
- Cross-linked the mapping from API, security, discovery, current-state, next-step, active-task, pressure-point, roadmap, and unresolved-architecture docs.
- Preserved existing behavior: no runtime endpoint changes, recommendation changes, filtering, RBAC, tenant isolation, auth rewrite, migrations, telemetry, encryption/KMS, contractor packets, utility exports, or operational-control runtime.

## Verification Performed

- `git diff --check` passed.
- No backend/frontend tests were required because this session touched documentation only.

## Protections Verified

- No runtime behavior changed.
- Existing compatibility-sensitive API contracts were not narrowed or reclassified as filtered role views.
- Scoped view models are mapped only; they are not implemented as endpoints, filters, exports, or permissions.
- AI remains advisory/grounding-only and cannot create canonical facts.
- New docs preserve structured-data authority, planning-only boundaries, provenance lineage, strict-client concerns, and model-agnostic restore posture.

## Remaining Risks

- Field-level data classification is not persisted or enforced.
- The mapped scoped view models are not implemented.
- Existing account, role, and subscription fields remain scaffolding only.
- Broad AI context remains a compatibility/grounding endpoint and is labeled rather than narrowed; `AIDesignGroundingView` is the recommended first additive split.
- Deployment lineage is defined as a gap, not implemented.
- Orchestration readiness is documented only; no DER, utility, contractor, or operational behavior exists.
- Strict clients that reject additive fields still require contract review before consuming future scoped envelopes.

## Current Resume Point

Runtime implementation can resume from the solar-readiness target if requested. If continuing scoped view/security design first, use `docs/security/SCOPED_VIEW_MODEL_MAPPING.md` and start with additive view schemas, especially a narrower AI grounding view, before implementing RBAC, exports, utility packets, contractor packets, or operational-control behavior.

## Lean Restore Prompt

```text
Load project skills before implementation.
```

## If You Resume Now

- Start from `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, and `discovery-index.md`.
- For cognition, governance, trust, provenance, or scoped API-view work, load `.codex/project-skills/canonical-authority-discipline/SKILL.md`, `.codex/project-skills/provenance-lineage/SKILL.md`, `.codex/project-skills/continuity-governance/SKILL.md`, and the task-specific project skill.
- For runtime advisor work, continue using the existing `.codex/skills/energy-planner-*` guardrail skills.

## Latest Detailed Handoff

See `docs/handoffs/2026-05-27-scoped-view-model-mapping.md`.
