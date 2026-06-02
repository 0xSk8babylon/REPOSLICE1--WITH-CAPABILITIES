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
  - `docs/product-vision.md`
  - `docs/philosophy/CORE_PHILOSOPHY.md`
  - `docs/CURRENT_STATE.md`
  - `docs/NEXT_STEPS.md`
  - `docs/ACTIVE_TASKS.md`
- Cognition, doctrine, or portability refactor:
  - `docs/product-vision.md`
  - `docs/philosophy/CORE_PHILOSOPHY.md`
  - `docs/philosophy/MENTAL_MODELS.md`
  - `docs/philosophy/SYSTEM_BOUNDARIES.md`
  - `docs/philosophy/TRUST_AND_PROVENANCE_PHILOSOPHY.md`
  - `docs/philosophy/AI_PHILOSOPHY.md`
  - `docs/philosophy/UX_PRINCIPLES.md`
  - `docs/philosophy/NON_GOALS.md`
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
  - `docs/architecture/ResidentialEnergyTwinCanonicalArchitectureHierarchy.md`
  - `docs/architecture/ResidentialEnergyTwinContractV1.md`
  - `docs/architecture/TopologyLifecycleDomains.md`
  - `docs/architecture/ContinuityDomain.md`
  - `docs/architecture/SafetyDomain.md`
  - `docs/architecture/ResidentialEnergyTwinCanonicalArchitectureHierarchy.md`
  - `docs/architecture/InteroperabilityDomain.md`
  - `docs/architecture/EcosystemParticipantBoundaryMatrix.md`
  - `docs/architecture/PermissionPlacement.md`
  - `docs/architecture/ProvenancePlacement.md`
  - `docs/architecture/ViewContracts.md`
  - `docs/architecture/SolarMarketProductIntelligenceGrounding.md`
  - `docs/architecture/Phase3TwinIntelligenceLayer.md`
  - `docs/architecture/StructuredSystemReasoningGraph.md`
  - `docs/architecture/ScenarioIntelligence.md`
  - `docs/architecture/InfrastructureSimulation.md`
  - `docs/architecture/WhatIfAnalysis.md`
  - `docs/architecture/DependencyImpactPropagation.md`
  - `docs/architecture/FIRST_RESIDENTIAL_ENERGY_TWIN_RUNTIME_BOUNDARY.md`
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
  - `docs/architecture/ContinuityDomain.md`
  - `docs/architecture/SafetyDomain.md`
  - `docs/architecture/InteroperabilityDomain.md`
  - `docs/architecture/EcosystemParticipantBoundaryMatrix.md`
  - `docs/architecture/PermissionPlacement.md`
  - `docs/architecture/ProvenancePlacement.md`
  - `docs/architecture/ViewContracts.md`
  - `docs/architecture/SolarMarketProductIntelligenceGrounding.md`
  - `docs/architecture/Phase3TwinIntelligenceLayer.md`
  - `docs/architecture/StructuredSystemReasoningGraph.md`
  - `docs/architecture/ScenarioIntelligence.md`
  - `docs/architecture/InfrastructureSimulation.md`
  - `docs/architecture/WhatIfAnalysis.md`
  - `docs/architecture/DependencyImpactPropagation.md`
  - `docs/trust/TRUST_ZONES.md`
  - `docs/provenance/LINEAGE_MODEL.md`
  - `docs/provenance/RESIDENTIAL_ENERGY_TWIN_PROVENANCE_POLICY_PLANNING.md`
  - `docs/security/SCOPED_INTELLIGENCE_OUTPUTS.md`
  - `docs/security/SCOPED_VIEW_MODEL_MAPPING.md`
  - `docs/security/RESIDENTIAL_ENERGY_TWIN_PERMISSIONED_VIEW_PLANNING.md`
  - `docs/governance/AI_AUTHORITY_LIMITS.md`
- Topology or orchestration planning:
  - `docs/architecture/TopologyLifecycleDomains.md`
  - `docs/architecture/ResidentialEnergyTwinCanonicalArchitectureHierarchy.md`
  - `docs/architecture/ContinuityDomain.md`
  - `docs/architecture/SafetyDomain.md`
  - `docs/architecture/InteroperabilityDomain.md`
  - `docs/architecture/EcosystemParticipantBoundaryMatrix.md`
  - `docs/architecture/SolarMarketProductIntelligenceGrounding.md`
  - `docs/architecture/Phase3TwinIntelligenceLayer.md`
  - `docs/architecture/StructuredSystemReasoningGraph.md`
  - `docs/architecture/ScenarioIntelligence.md`
  - `docs/architecture/InfrastructureSimulation.md`
  - `docs/architecture/WhatIfAnalysis.md`
  - `docs/architecture/DependencyImpactPropagation.md`
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
