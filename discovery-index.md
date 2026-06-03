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

## Canonical Phase Structure

- Phase 1: Planner Foundation - complete.
- Phase 2A: Twin Doctrine Foundation - complete.
- Phase 2B: Twin Runtime Expression - complete for the current approved runtime foundation scope.
  - Completed: `TwinPlanningContext`, Runtime View Foundations, Dependency Awareness Foundations, and Permission Foundations.
  - Provenance Expansion: runtime foundation scope is sufficiently complete; remaining provenance maturity work is deferred.
- Phase 2C: Topology + Lifecycle Intelligence - complete for the approved foundation scope.
  - Completed: Topology Snapshot Foundation, Lifecycle Readiness Foundation, and Topology Relationship Coverage Foundation.
  - Current boundary: descriptive, read-only topology snapshot metadata and safe relationship hooks derived from existing `TwinPlanningContext` records, dependency hooks, provenance gaps, dependency warnings, and limitation text.
  - Relationship coverage: structure-to-premise, panel/load/location-to-building, design-to-pathway, and resolvable pathway source/destination relationships are represented only when both ends resolve to concrete context nodes; unresolved or ambiguous labels remain missing relationship indicators.
  - Deferred: canonical topology graph, persistence, migrations, canonical topology table, `twin_id`, graph database, graph engine, lifecycle workflows, topology promotion workflows, lifecycle event logs, field verification workflows, recalculation engines, invalidation engines, simulation, what-if analysis, Phase 3 intelligence, contractor-reviewed topology, contractual topology, utility-reviewed topology, operational topology, auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, and operational control.
- Phase 3A: Derived Dependency Impact Readiness - complete for the approved first runtime boundary in `97b57fb`.
  - Completed: additive `/api/twin-planning-context/homes/{home_id}/views/dependency-impact-readiness` endpoint.
  - Current boundary: read-only, request-time, `home_id`-anchored derived intelligence envelope over existing `TwinPlanningContext` and topology snapshot outputs. It reports source basis, lifecycle scope, dependency impact posture, missing inputs, provenance gaps, confidence posture, limitations, and deferred capabilities. Every derived statement carries traceable basis metadata, and backend tests verify deterministic same-input/same-output behavior.
  - Deferred: broader Phase 3 implementation, scenario intelligence, impact propagation engine, recalculation engine, invalidation engine, optimization, ranking, economic reasoning, utility readiness reasoning, survivability/recharge modeling, compatibility engines, auth, RBAC/ABAC, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, operational control, `twin_id`, graph database, graph engine, scenario engine, simulation, what-if analysis, permission enforcement, recommendation actions, and operational behavior.

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
  - `docs/handoffs/2026-06-03-phase-3a-dependency-impact-readiness.md`
  - `docs/handoffs/2026-06-02-phase-2b-twin-runtime-foundations-closeout.md`
  - `docs/handoffs/2026-06-03-phase-2c-lifecycle-readiness-foundation.md`
  - `docs/handoffs/2026-06-03-phase-2c-topology-relationship-coverage-foundation.md`
  - `docs/handoffs/2026-06-03-phase-2c-foundations-closeout.md`
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
  - Twin Planning Context runtime foundation:
    - `apps/api/app/twin_planning_context/router.py`
    - `apps/api/app/twin_planning_context/schemas.py`
    - `apps/api/app/services/twin_planning_context.py`
    - `apps/api/tests/test_twin_planning_context.py`
  - Phase 3A Derived Dependency Impact Readiness:
    - `docs/handoffs/2026-06-03-phase-3a-dependency-impact-readiness.md`
    - `apps/api/app/twin_planning_context/router.py`
    - `apps/api/app/twin_planning_context/schemas.py`
    - `apps/api/app/services/twin_planning_context.py`
    - `apps/api/tests/test_twin_planning_context.py`
- Frontend behavior changes:
  - `apps/web/src/lib/api.js`
  - task-relevant pages/components
- Trust or provenance changes:
  - `docs/handoffs/2026-06-02-phase-2b-twin-runtime-foundations-closeout.md`
  - `docs/handoffs/2026-06-03-phase-3a-dependency-impact-readiness.md`
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
