# Discovery Index

## Purpose

This file maps the smallest restore surface that can route a session without forcing a full documentation sweep.

## Discovery Layer

Read these first:

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `SESSION_HANDOFF.md`
4. `.codex/skills/repo-memory-map/SKILL.md` if present
5. `.codex/skills/repo-guardrails/SKILL.md` if present

## Operational References By Task

- Product or roadmap alignment:
  - `docs/CURRENT_STATE.md`
  - `docs/NEXT_STEPS.md`
  - `docs/ACTIVE_TASKS.md`
- Cognition, doctrine, or portability refactor:
  - `docs/architecture/REPOSITORY_COGNITION_STRUCTURE.md`
  - `docs/architecture/COGNITION_LAYERS.md`
  - `docs/architecture/CANONICAL_TERMINOLOGY.md`
  - `docs/governance/GOVERNANCE_GAP_ANALYSIS.md`
  - `docs/governance/PROJECT_SKILL_RECOMMENDATIONS.md`
  - `.codex/project-skills/`
- Continuity maintenance:
  - `docs/continuity/LEAN_RESTORE_WORKFLOW.md`
  - `docs/continuity/UNRESOLVED_ARCHITECTURE.md`
  - `docs/session-continuity/continuity-workflow.md`
  - latest file in `docs/handoffs/`
- Architecture changes:
  - `docs/ARCHITECTURE.md`
  - `docs/architecture/RESIDENTIAL_ENERGY_TWIN_CONTRACT_V1.md`
  - `docs/architecture/COGNITION_LAYERS.md`
  - `docs/architecture/CANONICAL_TERMINOLOGY.md`
  - task-relevant files in `docs/session-continuity/`
- Database or persistence changes:
  - `docs/DATABASE_SCHEMA.md`
  - `docs/governance/MIGRATION_DISCIPLINE.md`
  - `apps/api/app/core/models.py`
  - `apps/api/app/core/repository.py`
- API changes:
  - `docs/API_CONTRACTS.md`
  - task-relevant routers in `apps/api/app/**`
- Frontend behavior changes:
  - `apps/web/src/lib/api.js`
  - task-relevant pages/components
- Trust or provenance changes:
  - `docs/trust/TRUST_ZONES.md`
  - `docs/provenance/LINEAGE_MODEL.md`
  - `docs/security/SCOPED_INTELLIGENCE_OUTPUTS.md`
  - `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
  - `docs/governance/AI_AUTHORITY_LIMITS.md`
- Topology or orchestration planning:
  - `docs/topology/TOPOLOGY_LIFECYCLE.md`
  - `docs/orchestration/READINESS_GAPS.md`
  - `docs/security/SCOPED_INTELLIGENCE_OUTPUTS.md`
  - `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`

## Deep References

Load only when directly relevant:

- `docs/philosophy/*`
- `docs/adr/*`
- `docs/governance/*`
- `docs/trust/*`
- `docs/provenance/*`
- `docs/topology/*`
- `docs/orchestration/*`
- non-latest handoffs in `docs/handoffs/`
- broad `docs/session-continuity/*` sweeps

## Keep Unloaded By Default

- full doctrine sweeps
- full ADR sweeps
- historical handoff sweeps
- unrelated backend or frontend code trees
