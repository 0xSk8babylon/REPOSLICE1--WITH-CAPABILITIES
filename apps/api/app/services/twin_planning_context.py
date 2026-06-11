import functools
from collections import Counter
from typing import Any, Dict, Iterable, List, Optional

from app.core.repository import repository
from app.core.types import AuthorityLayer, DataClassification, DataOrigin
from app.design_advisor.schemas import ResilienceRecommendation
from app.provenance.schemas import ProvenanceSummary
from app.services.design_advisor import design_advisor_service
from app.services.provenance import provenance_service
from app.twin_planning_context.schemas import (
    AIDesignGroundingRecord,
    AIDesignGroundingView,
    TwinAdvisoryContextAssemblyArea,
    TwinAdvisoryContextAssemblyItem,
    TwinAdvisoryContextAssemblyScope,
    TwinAdvisoryContextAssemblyView,
    TwinBasicAdvisoryRecommendationBasis,
    TwinBasicAdvisoryRecommendationCategory,
    TwinBasicAdvisoryRecommendationItem,
    TwinBasicAdvisoryRecommendationScope,
    TwinBasicAdvisoryRecommendationsView,
    TwinContractorFacingAdvisoryArea,
    TwinContractorFacingAdvisoryBasis,
    TwinContractorFacingAdvisoryItem,
    TwinContractorFacingAdvisoryScope,
    TwinContractorFacingAdvisoryView,
    TwinConstraintRiskReasoningArea,
    TwinConstraintRiskReasoningItem,
    TwinConstraintRiskReasoningScope,
    TwinConstraintRiskReasoningView,
    TwinDependencyImpactPostureItem,
    TwinDependencyImpactReadinessSummary,
    TwinDependencyImpactReadinessView,
    TwinDependencyImpactStatementBasis,
    TwinDependencyMissingInputItem,
    TwinDependencyReasoningItem,
    TwinDependencyReasoningScope,
    TwinDependencyReasoningType,
    TwinDependencyReasoningView,
    TwinEnergyGoalReasoningArea,
    TwinEnergyGoalReasoningBasis,
    TwinEnergyGoalReasoningItem,
    TwinEnergyGoalReasoningScope,
    TwinEnergyGoalReasoningView,
    TwinHomeownerFacingAdvisoryArea,
    TwinHomeownerFacingAdvisoryBasis,
    TwinHomeownerFacingAdvisoryItem,
    TwinHomeownerFacingAdvisoryScope,
    TwinHomeownerFacingAdvisoryView,
    TwinPlanningIntelligenceReadinessArea,
    TwinPlanningIntelligenceReadinessItem,
    TwinPlanningIntelligenceReadinessScope,
    TwinPlanningIntelligenceReadinessView,
    TwinPreRecommendationAdvisoryArea,
    TwinPreRecommendationAdvisoryBasis,
    TwinPreRecommendationAdvisoryItem,
    TwinPreRecommendationAdvisoryScope,
    TwinPreRecommendationAdvisoryView,
    TwinProposalReadinessFoundationArea,
    TwinProposalReadinessFoundationBasis,
    TwinProposalReadinessFoundationItem,
    TwinProposalReadinessFoundationScope,
    TwinProposalReadinessFoundationView,
    TwinProductSpecReadinessArea,
    TwinProductSpecReadinessBasis,
    TwinProductSpecReadinessItem,
    TwinProductSpecReadinessScope,
    TwinProductSpecReadinessView,
    TwinPlanningChangeImpactHint,
    TwinPlanningContext,
    TwinPlanningContextRecord,
    TwinPlanningContextSection,
    TwinPlanningDependencyAwareness,
    TwinPlanningDependencyAwarenessLabel,
    TwinPlanningDependencyHook,
    TwinPlanningDependencyWarning,
    TwinPlanningPermissionReadiness,
    TwinPlanningProvenanceGap,
    TwinPlanningProvenanceGapType,
    TwinPlanningRecordClassification,
    TwinRecommendationEligibilityArea,
    TwinRecommendationEligibilityBasis,
    TwinRecommendationEligibilityItem,
    TwinRecommendationEligibilityReadinessView,
    TwinRecommendationEligibilityScope,
    TwinPermissionConsentArtifactPlaceholder,
    TwinPermissionHomeownerAuthorityMetadata,
    TwinPermissionReadinessAudience,
    TwinPermissionReadinessAudienceConcept,
    TwinPermissionReadinessDuration,
    TwinPermissionReadinessDurationConcept,
    TwinPermissionReadinessPurpose,
    TwinPermissionReadinessPurposeConcept,
    TwinPermissionReadinessRevocationConcept,
    TwinPermissionReadinessRevocationState,
    TwinRuntimeContributionIdentity,
    TwinRuntimeParticipant,
    TwinRuntimeParticipantRole,
    TwinRuntimeProjectionRecord,
    TwinRuntimeProjectionView,
    TwinRuntimeViewContext,
    TwinRuntimeVisibilityScope,
    TwinScenarioComparisonReadinessArea,
    TwinScenarioComparisonReadinessBasis,
    TwinScenarioComparisonReadinessItem,
    TwinScenarioComparisonReadinessScope,
    TwinScenarioComparisonReadinessView,
    TwinSharedCompatibilityAudienceInterpretation,
    TwinSharedCompatibilityBasis,
    TwinSharedCompatibilityPath,
    TwinSharedCompatibilityScope,
    TwinSharedCompatibilityStatus,
    TwinSharedCompatibilitySummary,
    TwinSharedCompatibilityView,
    TwinTopologyTakeoffAudienceInterpretation,
    TwinTopologyTakeoffBasis,
    TwinTopologyTakeoffCostBasis,
    TwinTopologyTakeoffCostBasisStatus,
    TwinTopologyTakeoffLineCategory,
    TwinTopologyTakeoffLineItem,
    TwinTopologyTakeoffQuantityBasis,
    TwinTopologyTakeoffScope,
    TwinTopologyTakeoffSummary,
    TwinTopologyTakeoffView,
    TwinTrustProvenanceReadinessIndexEntry,
    TwinTrustProvenanceReadinessIndexScope,
    TwinTrustProvenanceReadinessIndexView,
    TwinTrustProvenanceReadinessSummary,
    TwinTopologyDeferredLifecycleDomain,
    TwinTopologyEdge,
    TwinTopologyMissingRelationshipIndicator,
    TwinTopologyLifecycleReadinessHint,
    TwinTopologyLifecycleReadinessSummary,
    TwinTopologyLifecycleDomain,
    TwinTopologyMissingReadinessIndicator,
    TwinTopologyNode,
    TwinTopologyRelationshipCoverageSummary,
    TwinTopologySnapshot,
    TwinViewPermissionAlignmentMetadata,
)


PLACEHOLDER_FIELDS = {
    "upfront_cost_placeholder",
    "estimated_monthly_savings_placeholder",
    "future_expansion_score",
    "install_complexity_score",
    "backup_capability_score",
    "resilience_score",
    "unit_cost_placeholder",
    "total_cost_placeholder",
}

IMPORTANT_PROVENANCE_FIELDS = {
    "home": {
        "name",
        "address_line_1",
        "city",
        "state",
        "postal_code",
        "utility_provider",
        "service_size",
    },
    "building": {"name", "type", "approximate_distance_from_main_service"},
    "electrical_panel": {
        "panel_type",
        "amperage",
        "busbar_rating",
        "breaker_spaces_total",
        "breaker_spaces_available",
        "indoor_outdoor",
    },
    "load": {
        "name",
        "category",
        "running_watts",
        "surge_watts",
        "estimated_daily_hours",
        "backup_priority",
        "phase_type",
    },
    "equipment_location": {"name", "location_type", "approximate_coordinates"},
    "equipment_product": {"manufacturer", "model", "product_type", "ecosystem", "specs", "documentation_url"},
    "energy_system_design": {"name", "design_goal", "architecture_type", "status"},
    "design_equipment": {"product_id", "quantity", "location_id", "role_in_system"},
    "estimated_pathway": {
        "name",
        "source_location",
        "destination_location",
        "estimated_distance_ft",
        "route_type",
        "route_difficulty",
        "visibility_level",
        "confidence_level",
        "upfront_cost_placeholder",
        "estimated_monthly_savings_placeholder",
        "resilience_score",
    },
    "scenario": {
        "name",
        "description",
        "linked_design_id",
        "upfront_cost_placeholder",
        "future_expansion_score",
        "install_complexity_score",
        "backup_capability_score",
    },
    "scenario_revision": {
        "revision_status",
        "linked_design_id",
        "design_goal_snapshot",
        "design_status_snapshot",
        "recommended_profile_snapshot",
        "planning_summary",
        "planning_state_snapshot",
    },
}

PROVENANCE_GAP_LIMITATIONS = [
    "Provenance gaps describe source visibility only; they do not prove a value is incorrect.",
    "Provenance visibility does not imply field verification, safety approval, utility approval, or engineering approval.",
]

DEPENDENCY_AWARENESS_LIMITATIONS = [
    "Dependency awareness labels are descriptive runtime metadata only.",
    "Labels do not run recalculation, schedule work, persist stale state, verify facts, or create approval authority.",
]

CHANGE_IMPACT_HINT_LIMITATIONS = [
    "Change-impact hints are descriptive planning metadata only.",
    "Hints do not run recalculation, invalidate records, persist stale state, verify facts, or create approval authority.",
]

PLANNING_DEPENDENCY_WARNING_LIMITATIONS = [
    "Planning dependency warnings describe relationship uncertainty only.",
    "Warnings do not prove a dependency is wrong, complete, field-verified, approved, or operational.",
]

TOPOLOGY_SNAPSHOT_LIMITATIONS = [
    "Topology snapshot is descriptive runtime metadata derived from the current Twin Planning Context only.",
    "No topology graph is persisted, promoted, field-verified, recalculated, invalidated, simulated, exported, or approved.",
    "Lifecycle labels are planning context only and do not create installation, engineering, utility, safety, or operational authority.",
]

TOPOLOGY_READINESS_LIMITATIONS = [
    "Lifecycle readiness metadata is descriptive and read-only.",
    "Readiness hints do not create lifecycle workflows, topology promotion, event logs, simulation, or Phase 3 intelligence.",
]

TOPOLOGY_RELATIONSHIP_COVERAGE_LIMITATIONS = [
    "Topology relationship coverage is descriptive and read-only.",
    "Relationship coverage does not create a graph engine, lifecycle workflow, promotion engine, event log, recalculation, invalidation, simulation, what-if analysis, or Phase 3 intelligence.",
    "Relationship coverage uses existing planning-context records only and does not infer installed, verified, utility-reviewed, contractual, or operational topology.",
]

DEPENDENCY_IMPACT_READINESS_LIMITATIONS = [
    "Phase 3A dependency impact readiness explains existing structure, dependencies, limitations, confidence, and missing information only.",
    "Every derived statement is reproducible from the listed TwinPlanningContext and topology snapshot basis.",
    "This view does not recommend, optimize, simulate, rank, choose, authorize, recalculate, invalidate, export, enforce permissions, or operate devices.",
    "The Twin may interpret recorded and derived planning facts, but it may not invent facts.",
]

DEPENDENCY_IMPACT_DEFERRED_CAPABILITIES = [
    "scenario_intelligence",
    "impact_propagation_engine",
    "recalculation_engine",
    "invalidation_engine",
    "optimization",
    "upgrade_ranking",
    "economic_reasoning",
    "utility_readiness_reasoning",
    "survivability_modeling",
    "recharge_modeling",
    "compatibility_engines",
    "simulation",
    "what_if_analysis",
    "auth",
    "rbac_abac",
    "permission_enforcement",
    "exports",
    "utility_sharing",
    "telemetry_governance",
    "ownership_transfer",
    "registry",
    "marketplace",
    "operational_control",
]

DEPENDENCY_REASONING_LIMITATIONS = [
    "Phase 3B dependency reasoning explains existing dependency meaning only.",
    "Every reasoning statement is reproducible from the listed TwinPlanningContext, topology snapshot, and dependency impact readiness basis.",
    "This view does not propagate impacts, mark stale state, recalculate, invalidate, compare scenarios, recommend, optimize, simulate, rank, choose, authorize, export, enforce permissions, or operate devices.",
    "The Twin may classify existing dependency meaning, but it may not invent facts or create new topology relationships.",
]

DEPENDENCY_REASONING_DEFERRED_CAPABILITIES = [
    "scenario_intelligence",
    "impact_propagation_engine",
    "stale_state_persistence",
    "recalculation_engine",
    "invalidation_engine",
    "optimization",
    "upgrade_ranking",
    "economic_reasoning",
    "utility_readiness_reasoning",
    "survivability_modeling",
    "recharge_modeling",
    "compatibility_engines",
    "simulation",
    "what_if_analysis",
    "auth",
    "rbac_abac",
    "permission_enforcement",
    "exports",
    "utility_sharing",
    "telemetry_governance",
    "ownership_transfer",
    "registry",
    "marketplace",
    "operational_control",
    "twin_id",
    "graph_database",
    "graph_engine",
    "migrations",
    "canonical_twin_runtime_model",
    "recommendation_actions",
]

PLANNING_INTELLIGENCE_READINESS_LIMITATIONS = [
    "Phase 3C planning intelligence readiness is a readiness inventory only.",
    "Areas marked ready are ready for read-only explanation only.",
    "Areas marked blocked/deferred are not implemented and must not be treated as available intelligence.",
    "Provenance presence is not verification, and permission readiness is not permission enforcement.",
    "This view does not recommend, rank, optimize, simulate, compare scenarios, generate proposals, export data, enforce permissions, operate devices, or create canonical Twin runtime state.",
]

PLANNING_INTELLIGENCE_READINESS_DEFERRED_BOUNDARIES = [
    "scenario_intelligence",
    "impact_propagation",
    "stale_state_persistence",
    "recalculation",
    "invalidation",
    "simulation",
    "what_if_analysis",
    "optimization",
    "ranking",
    "recommendations",
    "economic_reasoning",
    "utility_readiness",
    "survivability_recharge_modeling",
    "compatibility_engines",
    "proposal_generation",
    "exports",
    "auth",
    "rbac_abac",
    "permission_enforcement",
    "marketplace",
    "operational_behavior",
    "twin_id",
    "graph_engine",
    "migrations",
    "canonical_twin_runtime_model",
]

ADVISORY_CONTEXT_ASSEMBLY_LIMITATIONS = [
    "Phase 3D advisory context assembly is advisory input context only.",
    "This view assembles existing trusted context but does not generate advice, recommendations, guidance, proposals, rankings, optimization, simulations, what-if analysis, exports, permission enforcement, or operational behavior.",
    "Homeowner goals, topology facts, equipment/site facts, provenance basis, and permission-readiness metadata are included only when already represented in existing Twin Planning Context or derived Phase 3 views.",
    "Provenance presence is not verification, and permission readiness is not permission enforcement.",
]

ADVISORY_CONTEXT_DEFERRED_BOUNDARIES = [
    "advice_generation",
    "recommendations",
    "ranking",
    "optimization",
    "scenario_simulation",
    "what_if_analysis",
    "proposal_generation",
    "contractor_sales_logic",
    "homeowner_guidance_outputs",
    "permission_enforcement",
    "auth",
    "rbac_abac",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "exports",
    "operational_behavior",
]

CONSTRAINT_RISK_REASONING_LIMITATIONS = [
    "Phase 3E constraint and risk reasoning explains existing constraint and risk context only.",
    "Non-decisional severity labels are descriptive labels, not rankings, priorities, recommendations, directives, or final design guidance.",
    "This view does not recommend actions, rank risks, optimize, simulate scenarios, generate what-if analysis, generate proposals, perform economic reasoning, perform utility readiness logic, enforce permissions, export data, or operate devices.",
    "Constraint and risk statements are derived from existing Twin Planning Context and approved Phase 3 views only; the Twin may not invent facts.",
]

CONSTRAINT_RISK_DEFERRED_CAPABILITIES = [
    "recommendations",
    "priority_ranking",
    "optimization",
    "scenario_simulation",
    "what_if_analysis",
    "proposal_generation",
    "final_design_guidance",
    "contractor_directives",
    "homeowner_directives",
    "economic_reasoning",
    "utility_readiness_logic",
    "permission_enforcement",
    "auth",
    "rbac_abac",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "exports",
    "operational_behavior",
]

SCENARIO_COMPARISON_READINESS_LIMITATIONS = [
    "Phase 3F scenario comparison readiness inventories readiness for future comparison only.",
    "This view does not compare scenario records, calculate changes, simulate results, run what-if analysis, order options, optimize designs, recommend actions, propagate changes, persist stale state, generate proposals, or operate devices.",
    "Scenario records and revision lineage are available evidence only and must not be treated as future comparison output.",
    "Provenance presence is not verification, and permission readiness is not permission enforcement.",
]

SCENARIO_COMPARISON_DEFERRED_BOUNDARIES = [
    "scenario_comparison",
    "scenario_intelligence",
    "scenario_simulation",
    "what_if_analysis",
    "calculated_change_analysis",
    "option_ordering",
    "optimization",
    "recommendations",
    "change_propagation",
    "stale_state_persistence",
    "recalculation",
    "invalidation",
    "proposal_generation",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "exports",
    "operational_behavior",
]

PRE_RECOMMENDATION_ADVISORY_LIMITATIONS = [
    "Phase 3G pre-recommendation advisory explains what can and cannot be advised safely before recommendations are allowed.",
    "This view does not generate recommendations, rank recommendations, choose a best option, optimize, simulate, compare scenarios, calculate scenario changes, produce final design guidance, generate proposals, perform economic reasoning, perform utility readiness logic, create contractor directives, create homeowner directives, enforce permissions, export data, persist state, or operate devices.",
    "Advice-eligible areas are eligible for pre-recommendation advisory explanation only, not recommendations or directives.",
    "Provenance presence is not verification, permission readiness is not permission enforcement, and professional review remains deferred.",
]

PRE_RECOMMENDATION_DEFERRED_BOUNDARIES = [
    "recommendation_generation",
    "recommendation_ranking",
    "best_option_selection",
    "optimization",
    "simulation",
    "scenario_comparison",
    "calculated_change_analysis",
    "final_design_guidance",
    "proposal_generation",
    "economic_reasoning",
    "utility_readiness_logic",
    "contractor_directives",
    "homeowner_directives",
    "permission_enforcement",
    "auth",
    "rbac_abac",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "exports",
    "operational_behavior",
]

RECOMMENDATION_ELIGIBILITY_READINESS_LIMITATIONS = [
    "Phase 3H recommendation eligibility readiness is a readiness gate only.",
    "Eligibility means readiness posture only.",
    "Eligibility is not permission, approval, engineering review, authority, or recommendation generation.",
    "Existing advisor recommendation records may be treated only as existing derived-record context/provenance, not as current recommended outputs or choices.",
    "This view does not generate recommendations, expose selected/recommended profiles, rank, choose a best option, optimize, simulate, compare scenarios, calculate outcomes, generate proposals, perform economic reasoning, perform utility-readiness reasoning, create directives, enforce permissions, export data, persist state, or operate devices.",
]

RECOMMENDATION_ELIGIBILITY_DEFERRED_BOUNDARIES = [
    "recommendation_generation",
    "advisor_profile_choice",
    "recommendation_ranking",
    "best_option_selection",
    "optimization",
    "simulation",
    "scenario_comparison",
    "outcome_calculation",
    "proposal_generation",
    "economic_reasoning",
    "utility_readiness_reasoning",
    "contractor_directives",
    "homeowner_directives",
    "permission_enforcement",
    "auth",
    "rbac_abac",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "exports",
    "operational_behavior",
]

BASIC_ADVISORY_RECOMMENDATIONS_LIMITATIONS = [
    "Phase 3I basic advisory recommendations are prerequisite/remediation recommendations only.",
    "Allowed recommendations are limited to collecting missing data, verifying topology, verifying equipment/spec information, requesting spec sheets, and seeking contractor or professional review where existing Phase 3 views identify blockers.",
    "These recommendations do not choose products, designs, ranked options, best options, scenarios, economic paths, utility-readiness paths, proposals, directives, permission grants, exports, or operational behavior.",
    "Every recommendation is derived request-time from existing Twin Planning Context and approved Phase 3 view basis only.",
]

BASIC_ADVISORY_RECOMMENDATIONS_DEFERRED_BOUNDARIES = [
    "product_recommendations",
    "final_design_recommendations",
    "ranked_options",
    "best_option_selection",
    "optimization",
    "scenario_comparison_execution",
    "scenario_intelligence",
    "simulation",
    "what_if_analysis",
    "outcome_calculation",
    "economic_reasoning",
    "utility_readiness_reasoning",
    "proposal_generation",
    "contractor_directives",
    "homeowner_directives",
    "permission_enforcement",
    "auth",
    "rbac_abac",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "exports",
    "operational_behavior",
]

CONTRACTOR_FACING_ADVISORY_LIMITATIONS = [
    "Phase 3J contractor-facing advisory is audience translation only.",
    "It translates existing advisory, readiness, risk, and prerequisite/remediation recommendation context into contractor-facing field-verification and install-readiness language.",
    "It does not direct contractor action, generate proposals, generate pricing or bids, rank options, choose designs, recommend products, recommend final designs, optimize, simulate, compare scenarios, enforce permissions, export data, persist state, create graph behavior, create twin_id, or operate devices.",
    "Permission readiness is metadata only and is not authorization or enforcement; provenance basis is source context only and is not verification.",
]

CONTRACTOR_FACING_ADVISORY_DEFERRED_BOUNDARIES = [
    "contractor_action_directives",
    "proposal_generation",
    "pricing",
    "bid_logic",
    "product_recommendations",
    "final_design_recommendations",
    "ranked_options",
    "best_option_selection",
    "optimization",
    "simulation",
    "scenario_comparison",
    "marketplace_behavior",
    "crm_workflows",
    "permission_enforcement",
    "auth",
    "rbac_abac",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "exports",
    "operational_behavior",
]

HOMEOWNER_FACING_ADVISORY_LIMITATIONS = [
    "Phase 3K homeowner-facing advisory is audience translation only.",
    "It translates existing advisory, readiness, risk, and prerequisite/remediation recommendation context into homeowner-safe explanation language.",
    "It does not direct homeowner action, generate final design guidance, recommend products or specific equipment, rank options, choose designs, compare scenarios, simulate outcomes, calculate savings or payback, generate proposals, create sales claims, enforce permissions, export data, persist state, create graph behavior, create twin_id, or operate devices.",
    "Permission readiness is visibility/readiness metadata only and is not authorization or enforcement; provenance basis is source context only and is not verification.",
]

HOMEOWNER_FACING_ADVISORY_DEFERRED_BOUNDARIES = [
    "homeowner_action_directives",
    "final_design_guidance",
    "product_recommendations",
    "specific_equipment_recommendations",
    "ranked_options",
    "best_option_selection",
    "scenario_comparison",
    "simulation",
    "savings_payback",
    "proposal_generation",
    "sales_claims",
    "contractor_directives",
    "permission_enforcement",
    "auth",
    "rbac_abac",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "exports",
    "operational_behavior",
]

ENERGY_GOAL_REASONING_LIMITATIONS = [
    "Phase 3L energy goal reasoning is goal-to-context reasoning only.",
    "Goal-readiness means context readiness for goal reasoning.",
    "Goal-readiness does not mean design readiness, proposal readiness, approval, verification, or recommendation authority.",
    "Goal alignment is categorical and traceable, not numeric, ranked, optimized, or ordered by desirability.",
    "This view does not recommend products, recommend final designs, rank goals, rank solutions, optimize, simulate, compare scenarios, calculate savings or payback, generate proposals, create directives, perform utility-readiness logic, enforce permissions, export data, persist state, create graph behavior, create twin_id, or operate devices.",
    "Permission readiness is metadata only and is not authorization or enforcement; provenance basis is source context only and is not verification.",
]

ENERGY_GOAL_REASONING_DEFERRED_BOUNDARIES = [
    "product_recommendations",
    "final_design_recommendations",
    "goal_ranking",
    "solution_ranking",
    "optimization",
    "simulation",
    "scenario_comparison",
    "savings_payback",
    "proposal_generation",
    "contractor_directives",
    "homeowner_directives",
    "utility_readiness_logic",
    "permission_enforcement",
    "auth",
    "rbac_abac",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "exports",
    "operational_behavior",
]

PROPOSAL_READINESS_FOUNDATION_LIMITATIONS = [
    "Phase 3M proposal readiness foundation is readiness reporting only.",
    "It determines whether current context is ready to support future proposal generation without generating a proposal.",
    "It does not generate proposals, pricing, quotes, good/better/best packages, sales copy, savings/payback, financing logic, ranked options, best design selection, product recommendations, final design recommendations, CRM workflows, exports, permission enforcement, persistence, graph behavior, twin_id, or operational behavior.",
    "Permission readiness is metadata only and is not authorization or enforcement; provenance basis is source context only and is not verification.",
]

PROPOSAL_READINESS_FOUNDATION_DEFERRED_BOUNDARIES = [
    "proposal_generation",
    "pricing",
    "quote_generation",
    "good_better_best_packages",
    "sales_copy",
    "savings_payback",
    "financing_logic",
    "ranked_options",
    "best_design_selection",
    "product_recommendations",
    "final_design_recommendations",
    "contractor_crm_workflow",
    "exports",
    "permission_enforcement",
    "auth",
    "rbac_abac",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "operational_behavior",
]

PRODUCT_SPEC_READINESS_LIMITATIONS = [
    "Phase 3N product/spec readiness is readiness reporting only.",
    "It prepares for future product/spec-sheet reasoning by reporting whether product/spec context is available, missing, traceable, or blocked.",
    "It does not perform autonomous engineering from spec sheets, create a compatibility engine, recommend products, select equipment, rank products, generate proposals, generate pricing, scrape vendors, integrate supplier data, create vendor marketplace behavior, create procurement logic, enforce permissions, export data, persist state, create graph behavior, create twin_id, or operate devices.",
    "Spec-sheet provenance is source context only and is not verification; missing specs remain prerequisites, not compatibility conclusions.",
]

PRODUCT_SPEC_READINESS_COMPATIBILITY_DEFERRED_BOUNDARIES = [
    "autonomous_spec_engineering",
    "compatibility_engine",
    "product_recommendations",
    "equipment_selection",
    "product_ranking",
    "proposal_generation",
    "pricing",
]

PRODUCT_SPEC_READINESS_VENDOR_DEFERRED_BOUNDARIES = [
    "vendor_scraping",
    "supplier_data_integration",
    "vendor_marketplace_behavior",
    "procurement_logic",
    "exports",
    "permission_enforcement",
    "auth",
    "rbac_abac",
    "persistence",
    "migrations",
    "twin_id",
    "graph_engine",
    "operational_behavior",
]

TRUST_PROVENANCE_READINESS_INDEX_LIMITATIONS = [
    "Phase 4B trust/provenance/readiness index is a cross-view metadata index only.",
    "Index entries mirror existing Phase 4A trust_provenance_readiness_summary metadata and minimal source metadata only.",
    "This index does not create scores, rankings, pass/fail verdicts, approval claims, verification claims, pricing, proposal generation, product selection, compatibility claims, export packages, scenario simulation, permission enforcement, persistence, graph behavior, twin_id, marketplace behavior, or operational behavior.",
]

TRUST_PROVENANCE_READINESS_INDEX_DEFERRED_BOUNDARIES = [
    "scoring",
    "ranking",
    "pass_fail_verdicts",
    "approval_claims",
    "verification_claims",
    "proposal_generation",
    "pricing",
    "product_selection",
    "compatibility_claims",
    "export_packages",
    "scenario_simulation",
    "operational_behavior",
    "permission_enforcement",
    "persistence",
    "migrations",
    "frontend",
    "auth_security_changes",
    "graph_engine",
    "twin_id",
    "marketplace_behavior",
]

SHARED_COMPATIBILITY_LIMITATIONS = [
    "Phase 7A shared compatibility view is a read-only planning/install-path classification only.",
    "Statuses describe what appears compatible, blocked, uncertain, or confirmation-required from current planning data.",
    "The view does not produce final electrical design, final wire sizing, final conduit sizing, final breaker sizing, final disconnect/OCPD approval, permit-ready design, AHJ approval, utility approval, field verification, proposals, pricing, exports, permission enforcement, or operational behavior.",
    "Contractor confirmation gates are review prompts only and do not mean confirmation has been completed.",
]

SHARED_COMPATIBILITY_DEFERRED_BOUNDARIES = [
    "auth_security_changes",
    "compatibility_engine",
    "contractor_confirmation_completion",
    "exports",
    "field_verification",
    "final_breaker_sizing",
    "final_conduit_sizing",
    "final_design_outputs",
    "final_disconnect_ocpd_approval",
    "final_wire_sizing",
    "graph_engine",
    "migrations",
    "operational_behavior",
    "permission_enforcement",
    "permit_ready_design",
    "persistence",
    "pricing",
    "proposal_generation",
    "recommendation_ranking",
    "scenario_engine_expansion",
    "twin_id",
    "utility_ahj_approval",
    "write_endpoints",
]

SHARED_COMPATIBILITY_PATH_SPECS = [
    ("pv_only", "PV only", ["solar"], ["product_specs_verified", "nameplate_ratings_verified"]),
    (
        "pv_battery",
        "PV + battery",
        ["solar", "battery"],
        ["product_specs_verified", "nameplate_ratings_verified", "manufacturer_install_manual_reviewed"],
    ),
    (
        "pv_battery_partial_backup",
        "PV + battery + partial backup",
        ["solar", "battery", "essential_loads"],
        ["circuit_purpose_confirmed", "load_current_assumptions_confirmed", "overcurrent_protection_reviewed"],
    ),
    (
        "pv_battery_whole_home_backup",
        "PV + battery + whole-home backup",
        ["solar", "battery", "whole_home_backup"],
        ["load_current_assumptions_confirmed", "utility_ahj_requirements_reviewed", "contractor_final_review_completed"],
    ),
    (
        "pv_generator_interlock",
        "PV + generator interlock",
        ["solar", "generator", "transfer_strategy"],
        ["utility_ahj_requirements_reviewed", "disconnect_requirements_reviewed", "grounding_bonding_reviewed"],
    ),
    (
        "pv_generator_battery",
        "PV + generator + battery",
        ["solar", "battery", "generator"],
        ["manufacturer_install_manual_reviewed", "utility_ahj_requirements_reviewed", "contractor_final_review_completed"],
    ),
    (
        "critical_loads_subpanel",
        "Critical loads subpanel path",
        ["essential_loads", "panel_context"],
        ["circuit_purpose_confirmed", "load_current_assumptions_confirmed", "contractor_final_review_completed"],
    ),
    (
        "service_upgrade_likely",
        "Service upgrade likely path",
        ["service_upgrade"],
        ["utility_ahj_requirements_reviewed", "overcurrent_protection_reviewed"],
    ),
    (
        "load_management",
        "Load management path",
        ["preferred_loads", "load_management"],
        ["circuit_purpose_confirmed", "load_current_assumptions_confirmed"],
    ),
    (
        "existing_panel_reuse",
        "Existing panel reuse path",
        ["panel_context", "spare_spaces"],
        ["overcurrent_protection_reviewed", "contractor_final_review_completed"],
    ),
]

TOPOLOGY_TAKEOFF_LIMITATIONS = [
    "Phase 8 topology takeoff is a read-only planning-grade material/scope view only.",
    "Line items identify topology-driven scope categories likely implicated by current planning context.",
    "Quantities are basis signals only and are not final material quantities, final wire sizes, final conduit sizes, final breaker sizes, final disconnect/OCPD requirements, or permit-ready design.",
    "Cost basis is unavailable unless source-backed pricing is explicitly present; this view does not calculate final estimates, bids, proposals, savings, payback, or cost guarantees.",
    "Every line requires contractor, manufacturer, and/or AHJ review before use in a contractor estimate, bill of materials, or electrical design.",
]

TOPOLOGY_TAKEOFF_DEFERRED_BOUNDARIES = [
    "auth_security_changes",
    "contractor_approved_bom",
    "contractor_estimate",
    "exact_breaker_sizing",
    "exact_conduit_sizing",
    "exact_wire_sizing",
    "exports",
    "field_verification",
    "final_bill_of_materials",
    "final_design_outputs",
    "final_disconnect_ocpd_approval",
    "final_estimate",
    "graph_engine",
    "migrations",
    "nec_compliance_claims",
    "operational_behavior",
    "permission_enforcement",
    "permit_ready_design",
    "persistence",
    "pricing",
    "proposal_generation",
    "takeoff_persistence",
    "twin_id",
    "utility_ahj_approval",
    "write_endpoints",
]

TOPOLOGY_TAKEOFF_CATEGORY_SPECS = [
    (
        TwinTopologyTakeoffLineCategory.pv_source_circuit_array_side,
        "PV source circuit / array-side scope",
        ["solar_equipment", "pv_location", "pv_pathway"],
        ["product_specs_verified", "nameplate_ratings_verified", "conduit_routing_path_confirmed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.inverter_power_electronics,
        "Inverter / microinverter / power electronics scope",
        ["inverter_equipment", "power_electronics_location"],
        ["product_specs_verified", "nameplate_ratings_verified", "manufacturer_install_manual_reviewed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.battery_ess,
        "Battery / ESS scope",
        ["battery_equipment", "battery_location"],
        ["product_specs_verified", "nameplate_ratings_verified", "manufacturer_install_manual_reviewed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.backup_interface_gateway_transfer,
        "Backup interface / gateway / transfer equipment scope",
        ["battery_equipment", "generator_equipment", "backup_loads", "shared_compatibility:pv_battery_partial_backup"],
        ["manufacturer_install_manual_reviewed", "disconnect_requirements_reviewed", "overcurrent_protection_reviewed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.generator_integration,
        "Generator integration scope",
        ["generator_equipment", "generator_location", "generator_pathway"],
        ["product_specs_verified", "nameplate_ratings_verified", "utility_ahj_requirements_reviewed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.panel_subpanel_load_center,
        "Panel / subpanel / load center scope",
        ["panel_context", "backup_loads"],
        ["circuit_purpose_confirmed", "load_current_assumptions_confirmed", "overcurrent_protection_reviewed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.conduit_raceway_pathway,
        "Conduit / raceway pathway scope",
        ["pathway_distance", "pv_pathway", "generator_pathway"],
        ["distance_measurements_confirmed", "conduit_routing_path_confirmed", "raceway_type_confirmed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.conductor_circuit_placeholder,
        "Conductor / circuit placeholder scope",
        ["pathway_distance", "panel_context", "backup_loads"],
        ["conductor_material_confirmed", "current_carrying_conductors_confirmed", "derating_factors_applied"],
    ),
    (
        TwinTopologyTakeoffLineCategory.disconnect_ocpd_placeholder,
        "Disconnect / OCPD placeholder scope",
        ["solar_equipment", "battery_equipment", "generator_equipment", "panel_context"],
        ["disconnect_requirements_reviewed", "overcurrent_protection_reviewed", "utility_ahj_requirements_reviewed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.monitoring_communications,
        "Monitoring / communications scope",
        ["inverter_equipment", "battery_equipment", "generator_equipment"],
        ["product_specs_verified", "manufacturer_install_manual_reviewed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.labeling_signage_placeholder,
        "Labeling / signage placeholder scope",
        ["solar_equipment", "battery_equipment", "generator_equipment", "panel_context"],
        ["labeling_signage_requirements_reviewed", "utility_ahj_requirements_reviewed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.grounding_bonding_placeholder,
        "Grounding / bonding placeholder scope",
        ["solar_equipment", "battery_equipment", "generator_equipment", "panel_context"],
        ["grounding_bonding_reviewed", "utility_ahj_requirements_reviewed"],
    ),
    (
        TwinTopologyTakeoffLineCategory.routing_trenching_structural_mounting,
        "Trenching / routing / structural / mounting scope",
        ["roof_location", "trench_pathway", "pathway_distance"],
        ["distance_measurements_confirmed", "indoor_outdoor_wet_location_confirmed", "conduit_routing_path_confirmed"],
    ),
]

PHASE_3_DERIVED_VIEW_INDEX_SPECS = [
    (
        "dependency_impact_readiness",
        "phase_3a",
        "/api/twin-planning-context/homes/{home_id}/views/dependency-impact-readiness",
    ),
    (
        "dependency_reasoning",
        "phase_3b",
        "/api/twin-planning-context/homes/{home_id}/views/dependency-reasoning",
    ),
    (
        "planning_intelligence_readiness",
        "phase_3c",
        "/api/twin-planning-context/homes/{home_id}/views/planning-intelligence-readiness",
    ),
    (
        "advisory_context_assembly",
        "phase_3d",
        "/api/twin-planning-context/homes/{home_id}/views/advisory-context-assembly",
    ),
    (
        "constraint_risk_reasoning",
        "phase_3e",
        "/api/twin-planning-context/homes/{home_id}/views/constraint-risk-reasoning",
    ),
    (
        "scenario_comparison_readiness",
        "phase_3f",
        "/api/twin-planning-context/homes/{home_id}/views/scenario-comparison-readiness",
    ),
    (
        "pre_recommendation_advisory",
        "phase_3g",
        "/api/twin-planning-context/homes/{home_id}/views/pre-recommendation-advisory",
    ),
    (
        "recommendation_eligibility_readiness",
        "phase_3h",
        "/api/twin-planning-context/homes/{home_id}/views/recommendation-eligibility-readiness",
    ),
    (
        "basic_advisory_recommendations",
        "phase_3i",
        "/api/twin-planning-context/homes/{home_id}/views/basic-advisory-recommendations",
    ),
    (
        "contractor_facing_advisory",
        "phase_3j",
        "/api/twin-planning-context/homes/{home_id}/views/contractor-facing-advisory",
    ),
    (
        "homeowner_facing_advisory",
        "phase_3k",
        "/api/twin-planning-context/homes/{home_id}/views/homeowner-facing-advisory",
    ),
    (
        "energy_goal_reasoning",
        "phase_3l",
        "/api/twin-planning-context/homes/{home_id}/views/energy-goal-reasoning",
    ),
    (
        "proposal_readiness_foundation",
        "phase_3m",
        "/api/twin-planning-context/homes/{home_id}/views/proposal-readiness-foundation",
    ),
    (
        "product_spec_readiness",
        "phase_3n",
        "/api/twin-planning-context/homes/{home_id}/views/product-spec-readiness",
    ),
]

TOPOLOGY_RELATIONSHIP_COVERAGE_RULE_KEY = "twin_topology.relationship_coverage_v1"

TOPOLOGY_RELATIONSHIP_FAMILY_BY_RELATIONSHIP = {
    "structure_belongs_to_premise_planning_context": "structure_premise_placement",
    "panel_assigned_to_building_planning_context": "panel_building_placement",
    "load_assigned_to_building_planning_context": "load_building_placement",
    "location_assigned_to_building_planning_context": "location_building_placement",
    "design_includes_pathway_planning_context": "design_pathway_reference",
    "pathway_source_location_planning_context": "pathway_endpoint_reference",
    "pathway_destination_location_planning_context": "pathway_endpoint_reference",
}

DEFERRED_TOPOLOGY_LIFECYCLE_DOMAINS = [
    (
        "contractor_reviewed_topology",
        "Contractor-reviewed topology remains deferred because no approved contractor review workflow or authority boundary exists.",
        ["contractor view contract", "source-linked review artifact", "future approved lifecycle transition"],
    ),
    (
        "contractual_topology",
        "Contractual topology remains deferred because no approved proposal, contract, or commitment state is modeled.",
        ["contract authority boundary", "source-linked contract artifact", "future approved lifecycle transition"],
    ),
    (
        "field_verified_topology",
        "Field-verified topology remains deferred because no inspection, photo, commissioning, or professional verification workflow exists.",
        ["field verification source", "verification authority boundary", "future approved lifecycle transition"],
    ),
    (
        "utility_reviewed_topology",
        "Utility-reviewed topology remains deferred because no utility-safe view, export, interconnection authority, or utility approval workflow exists.",
        ["permissioned utility-safe view", "utility source evidence", "future approved lifecycle transition"],
    ),
    (
        "operational_topology",
        "Operational topology remains deferred because no telemetry, device identity, command authority, dispatch, DERMS, or control boundary exists.",
        ["telemetry governance", "device identity", "operational-control isolation"],
    ),
    (
        "future_expansion_or_replacement_topology",
        "Expansion and replacement topology remains deferred beyond saved planning scenarios because no decommissioning, replacement, or upgrade lifecycle model exists.",
        ["lifecycle history model", "source-linked replacement artifact", "future approved lifecycle transition"],
    ),
]

TOPOLOGY_MISSING_READINESS_INDICATORS = [
    (
        "field_verification_readiness",
        "field-verified",
        "Topology snapshot limitations explicitly state that topology is not field-verified.",
    ),
    (
        "promotion_workflow_readiness",
        "promoted",
        "Topology snapshot limitations explicitly state that topology is not promoted.",
    ),
    (
        "lifecycle_event_log_readiness",
        "lifecycle event log",
        "Snapshot implementation boundary and limitations state that no lifecycle event log exists.",
    ),
    (
        "simulation_readiness",
        "simulated",
        "Topology snapshot limitations explicitly state that topology is not simulated.",
    ),
    (
        "operational_topology_readiness",
        "operational",
        "Topology snapshot limitations state that lifecycle labels do not create operational authority.",
    ),
]

DEFERRED_PERMISSION_CAPABILITIES = [
    "permission_grants",
    "consent_artifacts",
    "revocation_workflow",
    "rbac_abac",
    "auth",
    "tenant_isolation",
    "scoped_exports",
    "exchange",
    "ownership_transfer",
    "registry",
    "identity",
    "utility_control",
    "operational_control",
]

PERMISSION_READINESS_LIMITATIONS = [
    "Permission readiness metadata is descriptive only and does not enforce access.",
    "Endpoint access, account scaffolding, UI visibility, or AI use is not a permission grant.",
    "External sharing requires a future approved permission model before it can be treated as authorized.",
]

PERMISSION_FOUNDATION_LIMITATIONS = [
    "Permission foundation fields are readiness metadata only.",
    "No active permission grant, active consent, authorization check, export authorization, or enforcement behavior exists.",
]

REGROUNDING_GAP_TYPES = {
    TwinPlanningProvenanceGapType.missing_source.value,
    TwinPlanningProvenanceGapType.partial_source.value,
    TwinPlanningProvenanceGapType.placeholder_without_source.value,
    TwinPlanningProvenanceGapType.unknown_origin.value,
}

LOAD_PANEL_DEPENDENCY_RULE_KEY = "twin_dependency.load_panel_shared_building_v1"
EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY = "twin_dependency.equipment_system_reference_v1"
SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY = "twin_dependency.scenario_reference_v1"

REVIEW_LIMITATION_MARKERS = (
    "not NEC compliance",
    "not field-verified",
    "not final electrical design",
    "not surveyed",
    "not full advisor replay",
    "not verified",
    "planning only",
    "planning context",
)

AI_GROUNDING_FIELD_ALLOWLIST = {
    "home": {"id", "name", "state", "country", "utility_provider", "service_size", "data_origin"},
    "building": {
        "id",
        "home_id",
        "name",
        "type",
        "approximate_distance_from_main_service",
        "data_origin",
    },
    "electrical_panel": {
        "id",
        "home_id",
        "building_id",
        "panel_type",
        "amperage",
        "busbar_rating",
        "breaker_spaces_total",
        "breaker_spaces_available",
        "indoor_outdoor",
        "data_origin",
    },
    "load": {
        "id",
        "home_id",
        "building_id",
        "name",
        "category",
        "running_watts",
        "surge_watts",
        "estimated_daily_hours",
        "backup_priority",
        "phase_type",
        "data_origin",
    },
    "equipment_location": {
        "id",
        "home_id",
        "building_id",
        "name",
        "location_type",
        "approximate_coordinates",
        "data_origin",
    },
    "equipment_product": {
        "id",
        "manufacturer",
        "model",
        "product_type",
        "ecosystem",
        "specs",
        "documentation_url",
        "data_origin",
    },
    "energy_system_design": {
        "id",
        "home_id",
        "name",
        "design_goal",
        "architecture_type",
        "status",
        "data_origin",
    },
    "design_equipment": {
        "id",
        "design_id",
        "product_id",
        "quantity",
        "location_id",
        "role_in_system",
        "data_origin",
    },
    "estimated_pathway": {
        "id",
        "home_id",
        "design_id",
        "name",
        "lifecycle_stage",
        "source_location",
        "destination_location",
        "estimated_distance_ft",
        "route_type",
        "route_difficulty",
        "visibility_level",
        "confidence_level",
        "upfront_cost_placeholder",
        "estimated_monthly_savings_placeholder",
        "resilience_score",
        "data_origin",
    },
    "scenario": {
        "id",
        "home_id",
        "name",
        "linked_design_id",
        "upfront_cost_placeholder",
        "future_expansion_score",
        "install_complexity_score",
        "backup_capability_score",
        "data_origin",
    },
    "scenario_revision": {
        "id",
        "scenario_id",
        "parent_revision_id",
        "revision_number",
        "revision_label",
        "revision_status",
        "linked_design_id",
        "design_goal_snapshot",
        "design_status_snapshot",
        "recommended_profile_snapshot",
        "planning_state_snapshot",
        "data_origin",
    },
    "advisor_recommendation_summary": {
        "design_id",
        "recommended_profile",
        "confidence_level",
        "context_signals",
        "basis",
        "scope_note",
        "reasoning_graph_scope",
    },
    "advisor_note": {"design_id", "advisor_note"},
}

AI_GROUNDING_BASE_SECTION_KEYS = {
    "premise",
    "structures",
    "electrical_infrastructure",
    "loads",
}

RUNTIME_VIEW_SECTION_ALLOWLIST = {
    TwinRuntimeParticipantRole.homeowner: {
        "premise",
        "structures",
        "electrical_infrastructure",
        "loads",
        "equipment_locations",
        "equipment_products",
        "designs",
        "design_equipment",
        "pathways",
        "scenarios",
        "scenario_revisions",
        "derived_intelligence",
    },
    TwinRuntimeParticipantRole.contractor: {
        "premise",
        "structures",
        "electrical_infrastructure",
        "loads",
        "equipment_locations",
        "equipment_products",
        "designs",
        "design_equipment",
        "pathways",
        "derived_intelligence",
    },
    TwinRuntimeParticipantRole.internal_system: {
        "premise",
        "structures",
        "electrical_infrastructure",
        "loads",
        "equipment_locations",
        "equipment_products",
        "designs",
        "design_equipment",
        "pathways",
        "scenarios",
        "scenario_revisions",
        "derived_intelligence",
        "unknowns",
    },
}

RUNTIME_VIEW_SCOPE = {
    TwinRuntimeParticipantRole.homeowner: TwinRuntimeVisibilityScope.owner_private,
    TwinRuntimeParticipantRole.contractor: TwinRuntimeVisibilityScope.contractor_scoped,
    TwinRuntimeParticipantRole.internal_system: TwinRuntimeVisibilityScope.internal_governance,
}

TOPOLOGY_SNAPSHOT_SECTION_ALLOWLIST = {
    "premise",
    "structures",
    "electrical_infrastructure",
    "loads",
    "equipment_locations",
    "equipment_products",
    "designs",
    "design_equipment",
    "pathways",
    "scenarios",
    "scenario_revisions",
    "derived_intelligence",
}

RUNTIME_VIEW_PURPOSE = {
    TwinRuntimeParticipantRole.homeowner: "owner_planning_context",
    TwinRuntimeParticipantRole.contractor: "contractor_scoping_context",
    TwinRuntimeParticipantRole.internal_system: "runtime_governance_review",
}

PERMISSION_AUDIENCE_READINESS_MAP = {
    "homeowner_planning": TwinPermissionReadinessAudience.homeowner,
    "homeowner": TwinPermissionReadinessAudience.homeowner,
    "contractor": TwinPermissionReadinessAudience.contractor,
    "ai": TwinPermissionReadinessAudience.ai,
    "internal_governance": TwinPermissionReadinessAudience.internal_system,
    "internal_system": TwinPermissionReadinessAudience.internal_system,
}

PERMISSION_PURPOSE_READINESS_MAP = {
    "owner_planning_context": TwinPermissionReadinessPurpose.owner_planning_context,
    "contractor_scoping_context": TwinPermissionReadinessPurpose.contractor_scoping_context,
    "grounded_design_recommendation": TwinPermissionReadinessPurpose.ai_grounding,
    "runtime_governance_review": TwinPermissionReadinessPurpose.runtime_governance_review,
    "missing_context_review": TwinPermissionReadinessPurpose.missing_context_review,
}

RUNTIME_FIELD_ALLOWLIST = {
    TwinRuntimeParticipantRole.contractor: {
        "home": {"id", "name", "city", "state", "country", "utility_provider", "service_size", "data_origin"},
        "building": {
            "id",
            "home_id",
            "name",
            "type",
            "approximate_distance_from_main_service",
            "data_origin",
        },
        "electrical_panel": {
            "id",
            "home_id",
            "building_id",
            "panel_type",
            "amperage",
            "busbar_rating",
            "breaker_spaces_total",
            "breaker_spaces_available",
            "indoor_outdoor",
            "data_origin",
        },
        "load": {
            "id",
            "home_id",
            "building_id",
            "name",
            "category",
            "running_watts",
            "surge_watts",
            "estimated_daily_hours",
            "backup_priority",
            "phase_type",
            "data_origin",
        },
        "equipment_location": {
            "id",
            "home_id",
            "building_id",
            "name",
            "location_type",
            "approximate_coordinates",
            "data_origin",
        },
        "equipment_product": {
            "id",
            "manufacturer",
            "model",
            "product_type",
            "ecosystem",
            "specs",
            "documentation_url",
            "data_origin",
        },
        "energy_system_design": {
            "id",
            "home_id",
            "name",
            "design_goal",
            "architecture_type",
            "status",
            "data_origin",
        },
        "design_equipment": {
            "id",
            "design_id",
            "product_id",
            "quantity",
            "location_id",
            "role_in_system",
            "data_origin",
        },
        "estimated_pathway": {
            "id",
            "home_id",
            "design_id",
            "name",
            "lifecycle_stage",
            "source_location",
            "destination_location",
            "estimated_distance_ft",
            "route_type",
            "route_difficulty",
            "visibility_level",
            "confidence_level",
            "data_origin",
        },
        "advisor_recommendation_summary": {
            "design_id",
            "recommended_profile",
            "confidence_level",
            "context_signals",
            "basis",
            "scope_note",
            "reasoning_graph_scope",
        },
    },
}


def _freeze_metadata_value(value: Any):
    """Convert a view payload into a hashable (cacheable) nested tuple form.

    ``("d", ...)`` wraps dict items, ``("l", ...)`` wraps list/tuple/set items,
    and ``("v", ...)`` wraps scalar leaves, so the cached walker below can
    distinguish node kinds without re-checking runtime types.
    """
    if isinstance(value, dict):
        return ("d", tuple((key, _freeze_metadata_value(child)) for key, child in value.items()))
    if isinstance(value, (list, tuple, set)):
        return ("l", tuple(_freeze_metadata_value(child) for child in value))
    return ("v", value)


def _frozen_metadata_value_present(frozen) -> bool:
    kind, payload = frozen
    if kind == "v":
        if payload is None:
            return False
        if isinstance(payload, str):
            return bool(payload)
        return True
    return bool(payload)


@functools.lru_cache(maxsize=262144)
def _frozen_metadata_paths(frozen, tokens: tuple) -> tuple:
    """Metadata paths for a frozen subtree, relative to the subtree root.

    Caching on the frozen subtree means identical sub-structures (repeated
    scope blocks, limitation lists, record boilerplate) are walked once per
    token set instead of once per occurrence, which collapses the previously
    pathological recursive walk over large view payloads.
    """
    kind, children = frozen
    paths = set()
    if kind == "d":
        for key, child in children:
            if key == "trust_provenance_readiness_summary":
                continue
            if any(token in key for token in tokens) and _frozen_metadata_value_present(child):
                paths.add(key)
            for rel in _frozen_metadata_paths(child, tokens):
                paths.add(key + rel if rel.startswith("[]") else f"{key}.{rel}")
    elif kind == "l":
        for child in children:
            for rel in _frozen_metadata_paths(child, tokens):
                paths.add("[]" + rel if rel.startswith("[]") else f"[].{rel}")
    return tuple(sorted(paths))


class TwinPlanningContextService:
    def _record_snapshot(self, record, fields: Iterable[str]) -> Dict[str, object]:
        return {field: getattr(record, field, None) for field in fields}

    def _origin_value(self, data_origin: Optional[str]) -> Optional[str]:
        return data_origin.value if hasattr(data_origin, "value") else data_origin

    def _entity_summary(self, db, entity_type: str, entity_id: Optional[str]) -> Optional[ProvenanceSummary]:
        if not entity_id:
            return None
        return provenance_service.summarize_entity(db, entity_type, entity_id)

    def _data_provenance_records(self, db, entity_type: str, entity_id: Optional[str]) -> List[object]:
        if not entity_id:
            return []
        return repository.list_data_provenance(db, entity_type=entity_type, entity_id=entity_id)

    def _has_provenance(self, summary: Optional[ProvenanceSummary]) -> bool:
        if summary is None:
            return False
        return bool(summary.source_types or summary.source_document_ids or summary.trust_states)

    def _placeholder_fields(self, record_snapshot: Dict[str, object]) -> List[str]:
        return sorted(
            field
            for field, value in record_snapshot.items()
            if field in PLACEHOLDER_FIELDS and value is not None
        )

    def _gap(
        self,
        *,
        gap_type: TwinPlanningProvenanceGapType,
        entity_type: str,
        entity_id: Optional[str],
        reason: str,
        field_name: Optional[str] = None,
        severity: str = "warning",
    ) -> TwinPlanningProvenanceGap:
        return TwinPlanningProvenanceGap(
            gap_type=gap_type,
            entity_type=entity_type,
            entity_id=entity_id,
            field_name=field_name,
            severity=severity,
            reason=reason,
            limitations=PROVENANCE_GAP_LIMITATIONS,
        )

    def _dependency_hook(
        self,
        *,
        source_entity_type: str,
        source_entity_id: Optional[str],
        target_entity_type: str,
        target_entity_id: Optional[str],
        relationship: str,
        rule_key: str,
        note: str,
        confidence_level: str = "planning_context",
    ) -> TwinPlanningDependencyHook:
        return TwinPlanningDependencyHook(
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            target_entity_type=target_entity_type,
            target_entity_id=target_entity_id,
            relationship=relationship,
            rule_keys=[rule_key],
            confidence_level=confidence_level,
            note=note,
        )

    def _change_impact_hint(
        self,
        *,
        source_entity_type: str,
        source_entity_id: Optional[str],
        impacted_entity_type: str,
        impacted_entity_id: Optional[str],
        relationship: str,
        rule_key: str,
        reason: str,
    ) -> TwinPlanningChangeImpactHint:
        return TwinPlanningChangeImpactHint(
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            impacted_entity_type=impacted_entity_type,
            impacted_entity_id=impacted_entity_id,
            relationship=relationship,
            rule_keys=[rule_key],
            reason=reason,
            limitations=CHANGE_IMPACT_HINT_LIMITATIONS,
        )

    def _planning_dependency_warning(
        self,
        *,
        warning_type: str,
        entity_type: str,
        entity_id: Optional[str],
        reason: str,
        related_entity_type: Optional[str] = None,
        related_entity_id: Optional[str] = None,
        rule_key: Optional[str] = None,
        severity: str = "info",
    ) -> TwinPlanningDependencyWarning:
        return TwinPlanningDependencyWarning(
            warning_type=warning_type,
            entity_type=entity_type,
            entity_id=entity_id,
            related_entity_type=related_entity_type,
            related_entity_id=related_entity_id,
            severity=severity,
            reason=reason,
            rule_keys=[rule_key] if rule_key else [],
            limitations=PLANNING_DEPENDENCY_WARNING_LIMITATIONS,
        )

    def _sourced_fields(self, provenance_records: List[object]) -> set:
        return {
            record.field_name
            for record in provenance_records
            if getattr(record, "field_name", None)
        }

    def _important_fields(self, entity_type: str, record_snapshot: Dict[str, object]) -> List[str]:
        configured_fields = IMPORTANT_PROVENANCE_FIELDS.get(entity_type, set())
        return sorted(
            field
            for field in configured_fields
            if field in record_snapshot and record_snapshot.get(field) is not None
        )

    def _derived_output_gaps(
        self,
        *,
        entity_type: str,
        entity_id: Optional[str],
        rule_keys: Optional[List[str]],
        dependency_hooks: Optional[List[TwinPlanningDependencyHook]],
        source_document_ids: Optional[List[str]],
    ) -> List[TwinPlanningProvenanceGap]:
        if rule_keys or source_document_ids:
            return []
        return [
            self._gap(
                gap_type=TwinPlanningProvenanceGapType.derived_without_lineage,
                entity_type=entity_type,
                entity_id=entity_id,
                reason=(
                    "Derived or advisory output has no persisted rule key or source document lineage in this context."
                ),
            )
        ]

    def _provenance_gaps_for_record(
        self,
        *,
        entity_type: str,
        entity_id: Optional[str],
        record_snapshot: Dict[str, object],
        data_origin: Optional[str],
        classification: TwinPlanningRecordClassification,
        provenance_records: List[object],
        source_document_ids: List[str],
        rule_keys: Optional[List[str]] = None,
        dependency_hooks: Optional[List[TwinPlanningDependencyHook]] = None,
    ) -> List[TwinPlanningProvenanceGap]:
        gaps: List[TwinPlanningProvenanceGap] = []
        sourced_fields = self._sourced_fields(provenance_records)
        important_fields = self._important_fields(entity_type, record_snapshot)
        unsourced_important_fields = [field for field in important_fields if field not in sourced_fields]
        placeholder_fields = self._placeholder_fields(record_snapshot)
        origin_value = self._origin_value(data_origin)

        if not sourced_fields and important_fields:
            gaps.append(
                self._gap(
                    gap_type=TwinPlanningProvenanceGapType.missing_source,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    reason=(
                        "No field-level source record is linked for important planning fields: "
                        f"{', '.join(important_fields)}."
                    ),
                )
            )
        elif sourced_fields and unsourced_important_fields:
            gaps.append(
                self._gap(
                    gap_type=TwinPlanningProvenanceGapType.partial_source,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    reason=(
                        "Some field-level provenance exists, but important planning fields remain unsourced: "
                        f"{', '.join(unsourced_important_fields)}."
                    ),
                )
            )

        for field in placeholder_fields:
            if field not in sourced_fields:
                gaps.append(
                    self._gap(
                        gap_type=TwinPlanningProvenanceGapType.placeholder_without_source,
                        entity_type=entity_type,
                        entity_id=entity_id,
                        field_name=field,
                        reason=f"Placeholder-bearing field '{field}' has no field-level source record.",
                    )
                )

        if not sourced_fields and not source_document_ids:
            gaps.append(
                self._gap(
                    gap_type=TwinPlanningProvenanceGapType.unknown_origin,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    severity="info",
                    reason=(
                        f"Persisted data_origin is '{origin_value or 'unknown'}', but no source record identifies "
                        "the document, entry, import, or rule basis for this entity."
                    ),
                )
            )

        if classification in {
            TwinPlanningRecordClassification.derived_output,
            TwinPlanningRecordClassification.advisory_output,
        }:
            gaps.extend(
                self._derived_output_gaps(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    rule_keys=rule_keys,
                    dependency_hooks=dependency_hooks,
                    source_document_ids=source_document_ids,
                )
            )

        return gaps

    def _dependency_awareness(
        self,
        *,
        label: TwinPlanningDependencyAwarenessLabel,
        record: TwinPlanningContextRecord,
        reason: str,
        source_gap_types: Optional[List[str]] = None,
    ) -> TwinPlanningDependencyAwareness:
        return TwinPlanningDependencyAwareness(
            label=label,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            reason=reason,
            rule_keys=record.rule_keys,
            source_gap_types=source_gap_types or [],
            limitations=DEPENDENCY_AWARENESS_LIMITATIONS,
        )

    def _dependency_awareness_for_record(
        self, section_key: str, record: TwinPlanningContextRecord
    ) -> List[TwinPlanningDependencyAwareness]:
        items: List[TwinPlanningDependencyAwareness] = []
        source_gap_types = sorted({gap.gap_type.value for gap in record.provenance_gaps})
        regrounding_gap_types = sorted(set(source_gap_types).intersection(REGROUNDING_GAP_TYPES))
        limitation_text = " ".join(record.limitations).lower()

        if section_key == "scenario_revisions":
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.snapshot_bound,
                    record=record,
                    reason="Scenario revisions are saved historical planning snapshots, not live current-state outputs.",
                )
            )
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.needs_recalculation,
                    record=record,
                    reason=(
                        "Snapshot-bound revision data would need recalculation before reuse as current planning intelligence."
                    ),
                )
            )

        if regrounding_gap_types:
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.needs_regrounding,
                    record=record,
                    reason=(
                        "Source or provenance posture is missing, partial, placeholder-backed, or unknown."
                    ),
                    source_gap_types=regrounding_gap_types,
                )
            )

        if record.classification in {
            TwinPlanningRecordClassification.derived_output,
            TwinPlanningRecordClassification.advisory_output,
        }:
            derived_gap_types = [
                gap_type for gap_type in source_gap_types if gap_type == TwinPlanningProvenanceGapType.derived_without_lineage.value
            ]
            if derived_gap_types:
                items.append(
                    self._dependency_awareness(
                        label=TwinPlanningDependencyAwarenessLabel.stale_unknown,
                        record=record,
                        reason=(
                            "Runtime cannot determine freshness because full derived-output lineage is not available."
                        ),
                        source_gap_types=derived_gap_types,
                    )
                )
            if record.dependency_hooks or record.rule_keys:
                items.append(
                    self._dependency_awareness(
                        label=TwinPlanningDependencyAwarenessLabel.current,
                        record=record,
                        reason=(
                            "Derived or advisory output was regenerated during this request from current planner records."
                        ),
                    )
                )

        if record.classification == TwinPlanningRecordClassification.unknown:
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.stale_unknown,
                    record=record,
                    reason="Unknown marker has no independent dependency basis or freshness signal.",
                    source_gap_types=source_gap_types,
                )
            )

        if record.entity_type == "advisor_note":
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.needs_review,
                    record=record,
                    reason="Advisory text should be reviewed against structured facts before reuse.",
                )
            )

        if any(marker in limitation_text for marker in REVIEW_LIMITATION_MARKERS):
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.needs_review,
                    record=record,
                    reason=(
                        "Planning-only limitations indicate this record needs review before stronger claims are made."
                    ),
                )
            )

        if not items:
            items.append(
                self._dependency_awareness(
                    label=TwinPlanningDependencyAwarenessLabel.current,
                    record=record,
                    reason=(
                        "Record is included in the current read-only planning context; this does not imply verification."
                    ),
                )
            )

        deduped = {}
        for item in items:
            key = (item.label.value, item.reason, tuple(item.source_gap_types))
            deduped.setdefault(key, item)
        return list(deduped.values())

    def _dependency_awareness_summary(self, records: List[object]) -> Dict[str, int]:
        counts = Counter(
            item.label.value
            for record in records
            for item in getattr(record, "dependency_awareness", [])
        )
        return {
            label.value: counts.get(label.value, 0)
            for label in TwinPlanningDependencyAwarenessLabel
        }

    def _attach_dependency_awareness(self, sections: List[TwinPlanningContextSection]):
        for section in sections:
            for record in section.records:
                record.dependency_awareness = self._dependency_awareness_for_record(section.section_key, record)
            section.dependency_awareness_summary = self._dependency_awareness_summary(section.records)

    def _permission_readiness(
        self,
        *,
        permission_required: bool,
        audience: str,
        purpose: str,
        minimum_necessary: bool,
        visibility_limitations: Optional[List[str]] = None,
        view_name: str = "twin_planning_context",
        visibility_scope: Optional[TwinRuntimeVisibilityScope] = None,
    ) -> TwinPlanningPermissionReadiness:
        audience_readiness = PERMISSION_AUDIENCE_READINESS_MAP.get(
            audience,
            TwinPermissionReadinessAudience.homeowner,
        )
        fallback_purpose = TwinPermissionReadinessPurpose.owner_planning_context
        if audience_readiness == TwinPermissionReadinessAudience.contractor:
            fallback_purpose = TwinPermissionReadinessPurpose.contractor_scoping_context
        elif audience_readiness == TwinPermissionReadinessAudience.ai:
            fallback_purpose = TwinPermissionReadinessPurpose.ai_grounding
        elif audience_readiness == TwinPermissionReadinessAudience.internal_system:
            fallback_purpose = TwinPermissionReadinessPurpose.runtime_governance_review
        purpose_readiness = PERMISSION_PURPOSE_READINESS_MAP.get(purpose, fallback_purpose)
        foundation_limitations = PERMISSION_FOUNDATION_LIMITATIONS + [
            "No permission grant id, consent artifact id, revocation event, auth principal, role mapping, or export package is created.",
        ]
        return TwinPlanningPermissionReadiness(
            permission_required=permission_required,
            permission_not_enforced=True,
            audience=audience,
            purpose=purpose,
            minimum_necessary=minimum_necessary,
            audience_readiness=TwinPermissionReadinessAudienceConcept(
                audience=audience_readiness,
                reason=(
                    "Audience is labeled for future permission-scoping readiness only; it is not an authenticated "
                    "principal, account role, grant recipient, or authorization subject."
                ),
                limitations=foundation_limitations,
            ),
            purpose_readiness=TwinPermissionReadinessPurposeConcept(
                purpose=purpose_readiness,
                reason=(
                    "Purpose is labeled for future permission-scoping readiness only; it does not authorize access, "
                    "sharing, export, or operational behavior."
                ),
                limitations=foundation_limitations,
            ),
            duration_readiness=TwinPermissionReadinessDurationConcept(
                duration=TwinPermissionReadinessDuration.not_active_placeholder,
                reason=(
                    "No active permission duration exists because no permission grant or consent artifact has been created."
                ),
                limitations=foundation_limitations,
            ),
            revocation_state_readiness=TwinPermissionReadinessRevocationConcept(
                revocation_state=TwinPermissionReadinessRevocationState.not_applicable_no_active_permission,
                reason=(
                    "No revocation state exists because there is no active grant, consent artifact, or enforced access."
                ),
                limitations=foundation_limitations,
            ),
            consent_artifact_placeholder=TwinPermissionConsentArtifactPlaceholder(
                reason=(
                    "Consent artifact is a placeholder concept only; no active consent text, consent version, or consent "
                    "record is captured by this runtime foundation."
                ),
                limitations=foundation_limitations,
            ),
            homeowner_authority=TwinPermissionHomeownerAuthorityMetadata(
                authority_note=(
                    "Homeowner authority over future external sharing is preserved; this metadata does not delegate, "
                    "transfer, or enforce that authority."
                ),
                limitations=foundation_limitations,
            ),
            view_permission_alignment=TwinViewPermissionAlignmentMetadata(
                view_name=view_name,
                audience=audience_readiness,
                purpose=purpose_readiness,
                visibility_scope=visibility_scope,
                limitations=foundation_limitations,
            ),
            visibility_limitations=PERMISSION_READINESS_LIMITATIONS + (visibility_limitations or []),
            deferred_capabilities=DEFERRED_PERMISSION_CAPABILITIES,
        )

    def _context_permission_readiness(self) -> TwinPlanningPermissionReadiness:
        return self._permission_readiness(
            permission_required=False,
            audience="homeowner_planning",
            purpose="owner_planning_context",
            minimum_necessary=False,
            view_name="twin_planning_context",
            visibility_scope=TwinRuntimeVisibilityScope.owner_private,
            visibility_limitations=[
                "Broad owner planning context is not minimized for external participants.",
                "External sharing would require future explicit permission, scope, purpose, duration, and revocation handling.",
            ],
        )

    def _section_permission_readiness(self, section_key: str) -> TwinPlanningPermissionReadiness:
        if section_key == "unknowns":
            return self._permission_readiness(
                permission_required=True,
                audience="internal_governance",
                purpose="missing_context_review",
                minimum_necessary=True,
                view_name=f"section:{section_key}",
                visibility_scope=TwinRuntimeVisibilityScope.internal_governance,
                visibility_limitations=[
                    "Unknown markers are internal governance context and should not be exposed as facts.",
                ],
            )
        return self._permission_readiness(
            permission_required=True,
            audience="homeowner_planning",
            purpose=f"{section_key}_planning_context",
            minimum_necessary=False,
            view_name=f"section:{section_key}",
            visibility_scope=TwinRuntimeVisibilityScope.owner_private,
            visibility_limitations=[
                "Section data may contain homeowner planning context and requires future permission before external sharing.",
            ],
        )

    def _record_permission_readiness(
        self, section_key: str, record: TwinPlanningContextRecord
    ) -> TwinPlanningPermissionReadiness:
        audience = "internal_governance" if section_key == "unknowns" else "homeowner_planning"
        purpose = "missing_context_review" if section_key == "unknowns" else f"{record.entity_type}_planning_context"
        limitations = [
            "Record visibility metadata does not authorize access or sharing.",
            "Future permission scope may need field-level or derived-output-level limits.",
        ]
        if record.classification in {
            TwinPlanningRecordClassification.derived_output,
            TwinPlanningRecordClassification.advisory_output,
        }:
            limitations.append("Derived and advisory outputs require explicit future view-purpose limits before sharing.")
        if record.source_document_ids:
            limitations.append("Source-document visibility may be narrower than fact visibility in a future permission model.")
        return self._permission_readiness(
            permission_required=True,
            audience=audience,
            purpose=purpose,
            minimum_necessary=False,
            view_name=f"record:{record.entity_type}",
            visibility_scope=(
                TwinRuntimeVisibilityScope.internal_governance
                if section_key == "unknowns"
                else TwinRuntimeVisibilityScope.owner_private
            ),
            visibility_limitations=limitations,
        )

    def _attach_permission_readiness(self, sections: List[TwinPlanningContextSection]):
        for section in sections:
            section.permission_readiness = self._section_permission_readiness(section.section_key)
            for record in section.records:
                record.permission_readiness = self._record_permission_readiness(section.section_key, record)

    def _ai_view_permission_readiness(self) -> TwinPlanningPermissionReadiness:
        return self._permission_readiness(
            permission_required=True,
            audience="ai",
            purpose="grounded_design_recommendation",
            minimum_necessary=True,
            view_name="ai_design_grounding",
            visibility_scope=TwinRuntimeVisibilityScope.ai_grounding,
            visibility_limitations=[
                "AI grounding view is minimized for explanation and recommendation grounding only.",
                "AI access is not consent, export authorization, write authority, or permission enforcement.",
                "AI may not create canonical facts, permission grants, verification claims, or approval claims.",
            ],
        )

    def _ai_record_permission_readiness(self, record: TwinPlanningContextRecord) -> TwinPlanningPermissionReadiness:
        return self._permission_readiness(
            permission_required=True,
            audience="ai",
            purpose=f"{record.entity_type}_grounding",
            minimum_necessary=True,
            view_name=f"ai_design_grounding:{record.entity_type}",
            visibility_scope=TwinRuntimeVisibilityScope.ai_grounding,
            visibility_limitations=[
                "Record is included only because it is part of the minimized AI grounding projection.",
                "Visibility metadata does not authorize external sharing or persistence outside the approved runtime.",
            ],
        )

    def _classify_record(
        self,
        *,
        record_snapshot: Dict[str, object],
        data_origin: Optional[str],
        provenance_summary: Optional[ProvenanceSummary],
        default_classification: TwinPlanningRecordClassification = TwinPlanningRecordClassification.recorded_fact,
    ) -> TwinPlanningRecordClassification:
        placeholder_fields = self._placeholder_fields(record_snapshot)
        if data_origin == DataOrigin.placeholder.value or placeholder_fields:
            return TwinPlanningRecordClassification.placeholder
        if data_origin == DataOrigin.derived_estimate.value:
            return TwinPlanningRecordClassification.derived_output
        if self._has_provenance(provenance_summary):
            return TwinPlanningRecordClassification.source_backed_fact
        return default_classification

    def _classification_reasons(
        self,
        *,
        classification: TwinPlanningRecordClassification,
        data_origin: Optional[str],
        provenance_summary: Optional[ProvenanceSummary],
        placeholder_fields: List[str],
        extra_reasons: Optional[List[str]] = None,
    ) -> List[str]:
        reasons = list(extra_reasons or [])
        if data_origin:
            reasons.append(f"Persisted data_origin is '{data_origin}'.")
        if classification == TwinPlanningRecordClassification.source_backed_fact:
            reasons.append("A provenance summary links this record to source or lineage metadata.")
        if placeholder_fields:
            reasons.append(f"Placeholder-bearing fields are present: {', '.join(placeholder_fields)}.")
        if not self._has_provenance(provenance_summary):
            reasons.append("No field-level provenance summary is currently linked for this entity.")
        if data_origin == DataOrigin.demo_seed.value:
            reasons.append("Demo seed records are useful for continuity but are not factual authority.")
        return reasons

    def _record(
        self,
        *,
        db,
        entity_type: str,
        entity_id: Optional[str],
        label: str,
        record_snapshot: Dict[str, object],
        data_origin: Optional[str],
        authority_layer: AuthorityLayer = AuthorityLayer.canonical,
        default_classification: TwinPlanningRecordClassification = TwinPlanningRecordClassification.recorded_fact,
        provenance_entity_type: Optional[str] = None,
        rule_keys: Optional[List[str]] = None,
        dependency_hooks: Optional[List[TwinPlanningDependencyHook]] = None,
        change_impact_hints: Optional[List[TwinPlanningChangeImpactHint]] = None,
        planning_dependency_warnings: Optional[List[TwinPlanningDependencyWarning]] = None,
        extra_reasons: Optional[List[str]] = None,
        limitations: Optional[List[str]] = None,
    ) -> TwinPlanningContextRecord:
        provenance_type = provenance_entity_type or entity_type
        summary = self._entity_summary(db, provenance_type, entity_id)
        provenance_records = self._data_provenance_records(db, provenance_type, entity_id)
        placeholder_fields = self._placeholder_fields(record_snapshot)
        classification = self._classify_record(
            record_snapshot=record_snapshot,
            data_origin=data_origin,
            provenance_summary=summary,
            default_classification=default_classification,
        )
        source_document_ids = summary.source_document_ids if summary else []
        record_rule_keys = rule_keys or []
        record_dependency_hooks = dependency_hooks or []
        record_change_impact_hints = change_impact_hints or []
        record_planning_dependency_warnings = planning_dependency_warnings or []
        return TwinPlanningContextRecord(
            entity_type=entity_type,
            entity_id=entity_id,
            label=label,
            classification=classification,
            authority_layer=authority_layer,
            data_origin=data_origin,
            record=record_snapshot,
            provenance_summary=summary,
            source_document_ids=source_document_ids,
            rule_keys=record_rule_keys,
            dependency_hooks=record_dependency_hooks,
            classification_reasons=self._classification_reasons(
                classification=classification,
                data_origin=data_origin,
                provenance_summary=summary,
                placeholder_fields=placeholder_fields,
                extra_reasons=extra_reasons,
            ),
            missing_fields=placeholder_fields + (summary.unverified_fields if summary else []),
            provenance_gaps=self._provenance_gaps_for_record(
                entity_type=entity_type,
                entity_id=entity_id,
                record_snapshot=record_snapshot,
                data_origin=data_origin,
                classification=classification,
                provenance_records=provenance_records,
                source_document_ids=source_document_ids,
                rule_keys=record_rule_keys,
                dependency_hooks=record_dependency_hooks,
            ),
            change_impact_hints=record_change_impact_hints,
            planning_dependency_warnings=record_planning_dependency_warnings,
            limitations=limitations or [],
        )

    def _unknown_record(self, entity_type: str, entity_id: str, label: str, reason: str) -> TwinPlanningContextRecord:
        return TwinPlanningContextRecord(
            entity_type=entity_type,
            entity_id=entity_id,
            label=label,
            classification=TwinPlanningRecordClassification.unknown,
            authority_layer=AuthorityLayer.advisory,
            data_classification=DataClassification.internal_governance,
            record={},
            classification_reasons=[reason],
            provenance_gaps=[
                self._gap(
                    gap_type=TwinPlanningProvenanceGapType.unknown_origin,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    severity="info",
                    reason="This unknown marker has no independent source; it reflects a missing planning-context gap.",
                )
            ],
            limitations=[
                "Unknown markers identify missing planning context; they are not inferred facts.",
            ],
        )

    def _advisor_record(
        self,
        *,
        design_id: str,
        recommendation: ResilienceRecommendation,
        dependency_hooks: List[TwinPlanningDependencyHook],
    ) -> TwinPlanningContextRecord:
        recommended_profile = recommendation.recommended_profile.value if recommendation.recommended_profile else None
        rule_keys = []
        if recommendation.provenance_summary:
            rule_keys = recommendation.provenance_summary.get("rule_keys", [])
        return TwinPlanningContextRecord(
            entity_type="advisor_recommendation_summary",
            entity_id=f"advisor-summary-{design_id}",
            label=f"Advisor recommendation summary for {design_id}",
            classification=TwinPlanningRecordClassification.derived_output,
            authority_layer=AuthorityLayer.derived,
            data_origin=DataOrigin.derived_estimate,
            record={
                "design_id": design_id,
                "recommended_profile": recommended_profile,
                "confidence_level": recommendation.confidence_level.value,
                "context_signals": recommendation.context_signals,
                "basis": recommendation.basis,
                "scope_note": recommendation.scope_note,
                "reasoning_graph_scope": recommendation.reasoning_graph.scope_label
                if recommendation.reasoning_graph
                else None,
            },
            rule_keys=rule_keys,
            dependency_hooks=dependency_hooks,
            classification_reasons=[
                "Advisor recommendation summary is derived from deterministic rules over recorded planning records.",
            ],
            missing_fields=[],
            provenance_gaps=self._derived_output_gaps(
                entity_type="advisor_recommendation_summary",
                entity_id=f"advisor-summary-{design_id}",
                rule_keys=rule_keys,
                dependency_hooks=dependency_hooks,
                source_document_ids=[],
            ),
            limitations=[
                "Advisor outputs are planning intelligence only and do not create canonical Twin facts.",
                "Advisor outputs are regenerated from current records; they are not a persisted full replay snapshot.",
            ],
        )

    def _advisor_note_record(self, design_id: str, advisor_note: str) -> TwinPlanningContextRecord:
        return TwinPlanningContextRecord(
            entity_type="advisor_note",
            entity_id=f"advisor-note-{design_id}",
            label=f"Advisor note for {design_id}",
            classification=TwinPlanningRecordClassification.advisory_output,
            authority_layer=AuthorityLayer.advisory,
            data_origin=DataOrigin.derived_estimate,
            record={"design_id": design_id, "advisor_note": advisor_note},
            classification_reasons=[
                "Advisor note is explanatory text over structured records and deterministic outputs.",
            ],
            provenance_gaps=self._derived_output_gaps(
                entity_type="advisor_note",
                entity_id=f"advisor-note-{design_id}",
                rule_keys=[],
                dependency_hooks=[],
                source_document_ids=[],
            ),
            limitations=[
                "Advisory text cannot create canonical facts, permission grants, engineering approval, or utility authority.",
            ],
        )

    def _dependency_hooks_from_recommendation(
        self, design_id: str, recommendation: ResilienceRecommendation
    ) -> List[TwinPlanningDependencyHook]:
        graph = recommendation.reasoning_graph
        if graph is None:
            return []
        return [
            TwinPlanningDependencyHook(
                source_entity_type=dependency.source_node_id,
                source_entity_id=None,
                target_entity_type=dependency.target_node_id,
                target_entity_id=None,
                relationship=dependency.relationship,
                rule_keys=dependency.rule_keys,
                confidence_level=dependency.confidence_level.value,
                note=f"Design {design_id}: {dependency.summary}",
            )
            for dependency in graph.dependencies
        ]

    def _load_panel_dependency_metadata(
        self, load, panels_by_building: Dict[str, List[object]]
    ):
        related_panels = panels_by_building.get(load.building_id, [])
        hooks = [
            self._dependency_hook(
                source_entity_type="load",
                source_entity_id=load.id,
                target_entity_type="electrical_panel",
                target_entity_id=panel.id,
                relationship="shared_building_id_planning_context",
                rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                confidence_level="planning_context_only",
                note=(
                    f"Load {load.id} and panel {panel.id} share building_id {load.building_id}; "
                    "this is planning context only and does not identify circuit membership."
                ),
            )
            for panel in related_panels
        ]
        hints = [
            self._change_impact_hint(
                source_entity_type="electrical_panel",
                source_entity_id=panel.id,
                impacted_entity_type="load",
                impacted_entity_id=load.id,
                relationship="shared_building_id_planning_context",
                rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                reason=(
                    "Panel or service-capacity changes for the same building may affect how this load is interpreted "
                    "in planning outputs."
                ),
            )
            for panel in related_panels
        ]
        warnings = []
        if related_panels:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="load_panel_relationship_is_building_level_only",
                    entity_type="load",
                    entity_id=load.id,
                    related_entity_type="electrical_panel",
                    related_entity_id=related_panels[0].id,
                    rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                    reason=(
                        "The load-to-panel relationship is inferred only from shared building_id planning context; "
                        "it is not a verified circuit, breaker, or panelboard assignment."
                    ),
                )
            )
        else:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="load_has_no_same_building_panel",
                    entity_type="load",
                    entity_id=load.id,
                    rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                    severity="warning",
                    reason=(
                        "No electrical panel record shares this load's building_id, so panel/service impact context "
                        "for this load is incomplete."
                    ),
                )
            )
        return hooks, hints, warnings

    def _panel_load_dependency_metadata(
        self, panel, loads_by_building: Dict[str, List[object]]
    ):
        related_loads = loads_by_building.get(panel.building_id, [])
        hints = [
            self._change_impact_hint(
                source_entity_type="load",
                source_entity_id=load.id,
                impacted_entity_type="electrical_panel",
                impacted_entity_id=panel.id,
                relationship="shared_building_id_planning_context",
                rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                reason=(
                    "Recorded load changes for the same building may affect panel/service planning interpretation."
                ),
            )
            for load in related_loads
        ]
        warnings = []
        if related_loads:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="panel_load_relationship_is_building_level_only",
                    entity_type="electrical_panel",
                    entity_id=panel.id,
                    related_entity_type="load",
                    related_entity_id=related_loads[0].id,
                    rule_key=LOAD_PANEL_DEPENDENCY_RULE_KEY,
                    reason=(
                        "Panel-to-load impact is based on shared building_id only; it does not identify a verified "
                        "served-load, circuit, breaker, or subpanel relationship."
                    ),
                )
            )
        return [], hints, warnings

    def _design_equipment_dependency_metadata(
        self,
        equipment,
        designs_by_id: Dict[str, object],
        products_by_id: Dict[str, object],
        locations_by_id: Dict[str, object],
    ):
        hooks = []
        hints = []
        warnings = []

        if equipment.design_id in designs_by_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="design_equipment",
                    source_entity_id=equipment.id,
                    target_entity_type="energy_system_design",
                    target_entity_id=equipment.design_id,
                    relationship="assigned_to_design_planning_context",
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    note=(
                        f"Design equipment {equipment.id} is part of design {equipment.design_id} in the "
                        "current planning composition."
                    ),
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="energy_system_design",
                    source_entity_id=equipment.design_id,
                    impacted_entity_type="design_equipment",
                    impacted_entity_id=equipment.id,
                    relationship="assigned_to_design_planning_context",
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    reason="Design goal or status changes may affect how this equipment assignment is interpreted.",
                )
            )
        else:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="design_equipment_missing_design_reference",
                    entity_type="design_equipment",
                    entity_id=equipment.id,
                    related_entity_type="energy_system_design",
                    related_entity_id=equipment.design_id,
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    severity="warning",
                    reason="This equipment assignment references a design that is not present in the home planning context.",
                )
            )

        if equipment.product_id in products_by_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="design_equipment",
                    source_entity_id=equipment.id,
                    target_entity_type="equipment_product",
                    target_entity_id=equipment.product_id,
                    relationship="uses_product_reference",
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    note=(
                        f"Design equipment {equipment.id} references product {equipment.product_id}; product data "
                        "is planning reference data, not a procurement or compatibility guarantee."
                    ),
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="equipment_product",
                    source_entity_id=equipment.product_id,
                    impacted_entity_type="design_equipment",
                    impacted_entity_id=equipment.id,
                    relationship="uses_product_reference",
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    reason="Product data changes may affect equipment composition, compatibility, and planning notes.",
                )
            )
        else:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="design_equipment_missing_product_reference",
                    entity_type="design_equipment",
                    entity_id=equipment.id,
                    related_entity_type="equipment_product",
                    related_entity_id=equipment.product_id,
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    severity="warning",
                    reason="This equipment assignment references product data that is not present in the runtime context.",
                )
            )

        if equipment.location_id:
            if equipment.location_id in locations_by_id:
                hooks.append(
                    self._dependency_hook(
                        source_entity_type="design_equipment",
                        source_entity_id=equipment.id,
                        target_entity_type="equipment_location",
                        target_entity_id=equipment.location_id,
                        relationship="assigned_location_planning_context",
                        rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                        note=(
                            f"Design equipment {equipment.id} references location {equipment.location_id}; "
                            "location is planning/siting context only."
                        ),
                    )
                )
                hints.append(
                    self._change_impact_hint(
                        source_entity_type="equipment_location",
                        source_entity_id=equipment.location_id,
                        impacted_entity_type="design_equipment",
                        impacted_entity_id=equipment.id,
                        relationship="assigned_location_planning_context",
                        rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                        reason="Location changes may affect siting, pathway, and design-equipment planning interpretation.",
                    )
                )
                warnings.append(
                    self._planning_dependency_warning(
                        warning_type="equipment_location_is_planning_only",
                        entity_type="design_equipment",
                        entity_id=equipment.id,
                        related_entity_type="equipment_location",
                        related_entity_id=equipment.location_id,
                        rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                        reason="Equipment location references are planning/siting context and are not field-verified placement.",
                    )
                )
            else:
                warnings.append(
                    self._planning_dependency_warning(
                        warning_type="design_equipment_missing_location_reference",
                        entity_type="design_equipment",
                        entity_id=equipment.id,
                        related_entity_type="equipment_location",
                        related_entity_id=equipment.location_id,
                        rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                        severity="warning",
                        reason="This equipment assignment references a location that is not present in the home planning context.",
                    )
                )
        else:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="design_equipment_location_unassigned",
                    entity_type="design_equipment",
                    entity_id=equipment.id,
                    rule_key=EQUIPMENT_SYSTEM_DEPENDENCY_RULE_KEY,
                    reason="No equipment location is assigned, so siting and pathway dependency context is incomplete.",
                )
            )

        return hooks, hints, warnings

    def _scenario_dependency_metadata(self, scenario, designs_by_id: Dict[str, object]):
        hooks = []
        hints = []
        warnings = [
            self._planning_dependency_warning(
                warning_type="scenario_reference_is_not_live_invalidation",
                entity_type="scenario",
                entity_id=scenario.id,
                related_entity_type="energy_system_design",
                related_entity_id=scenario.linked_design_id,
                rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                reason=(
                    "Scenario-to-design references are planning dependencies only; design changes do not create "
                    "automatic invalidation, recalculation, or approval state."
                ),
            )
        ]
        if scenario.linked_design_id in designs_by_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="scenario",
                    source_entity_id=scenario.id,
                    target_entity_type="energy_system_design",
                    target_entity_id=scenario.linked_design_id,
                    relationship="linked_design_planning_context",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    note=f"Scenario {scenario.id} references design {scenario.linked_design_id}.",
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="energy_system_design",
                    source_entity_id=scenario.linked_design_id,
                    impacted_entity_type="scenario",
                    impacted_entity_id=scenario.id,
                    relationship="linked_design_planning_context",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    reason="Linked design changes may affect scenario comparison and planning interpretation.",
                )
            )
        else:
            warnings.append(
                self._planning_dependency_warning(
                    warning_type="scenario_missing_design_reference",
                    entity_type="scenario",
                    entity_id=scenario.id,
                    related_entity_type="energy_system_design",
                    related_entity_id=scenario.linked_design_id,
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    severity="warning",
                    reason="This scenario references a design that is not present in the home planning context.",
                )
            )
        return hooks, hints, warnings

    def _scenario_revision_dependency_metadata(
        self,
        revision,
        scenarios_by_id: Dict[str, object],
        designs_by_id: Dict[str, object],
    ):
        hooks = []
        hints = []
        warnings = [
            self._planning_dependency_warning(
                warning_type="revision_snapshot_is_not_live_replay",
                entity_type="scenario_revision",
                entity_id=revision.id,
                related_entity_type="scenario",
                related_entity_id=revision.scenario_id,
                rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                reason=(
                    "Scenario revisions are compact snapshots; current design or scenario changes do not automatically "
                    "replay, recalculate, invalidate, or approve this revision."
                ),
            )
        ]

        if revision.scenario_id in scenarios_by_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="scenario_revision",
                    source_entity_id=revision.id,
                    target_entity_type="scenario",
                    target_entity_id=revision.scenario_id,
                    relationship="snapshot_of_scenario",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    note=f"Scenario revision {revision.id} snapshots scenario {revision.scenario_id}.",
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="scenario",
                    source_entity_id=revision.scenario_id,
                    impacted_entity_type="scenario_revision",
                    impacted_entity_id=revision.id,
                    relationship="snapshot_of_scenario",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    reason="Scenario changes may affect how this saved revision should be interpreted.",
                )
            )

        if revision.linked_design_id in designs_by_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="scenario_revision",
                    source_entity_id=revision.id,
                    target_entity_type="energy_system_design",
                    target_entity_id=revision.linked_design_id,
                    relationship="snapshot_linked_design",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    note=f"Scenario revision {revision.id} preserves linked design {revision.linked_design_id}.",
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="energy_system_design",
                    source_entity_id=revision.linked_design_id,
                    impacted_entity_type="scenario_revision",
                    impacted_entity_id=revision.id,
                    relationship="snapshot_linked_design",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    reason="Linked design changes may affect whether this saved revision still matches current planning intent.",
                )
            )

        if revision.parent_revision_id:
            hooks.append(
                self._dependency_hook(
                    source_entity_type="scenario_revision",
                    source_entity_id=revision.id,
                    target_entity_type="scenario_revision",
                    target_entity_id=revision.parent_revision_id,
                    relationship="parent_revision_lineage",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    note=f"Scenario revision {revision.id} references parent revision {revision.parent_revision_id}.",
                )
            )
            hints.append(
                self._change_impact_hint(
                    source_entity_type="scenario_revision",
                    source_entity_id=revision.parent_revision_id,
                    impacted_entity_type="scenario_revision",
                    impacted_entity_id=revision.id,
                    relationship="parent_revision_lineage",
                    rule_key=SCENARIO_REFERENCE_DEPENDENCY_RULE_KEY,
                    reason="Parent revision lineage affects interpretation of saved revision drift.",
                )
            )

        return hooks, hints, warnings

    def _ai_grounding_fields(self, record: TwinPlanningContextRecord) -> Dict[str, object]:
        allowed_fields = AI_GROUNDING_FIELD_ALLOWLIST.get(record.entity_type, set())
        return {
            field: value
            for field, value in record.record.items()
            if field in allowed_fields
        }

    def _ai_grounding_related_ids(
        self, context: TwinPlanningContext, design_id: Optional[str]
    ) -> Dict[str, set]:
        related_ids = {
            "design_ids": set(),
            "product_ids": set(),
            "location_ids": set(),
            "scenario_ids": set(),
        }
        if not design_id:
            return related_ids

        related_ids["design_ids"].add(design_id)
        for section in context.sections:
            for record in section.records:
                if section.section_key == "design_equipment" and record.record.get("design_id") == design_id:
                    if record.record.get("product_id"):
                        related_ids["product_ids"].add(record.record["product_id"])
                    if record.record.get("location_id"):
                        related_ids["location_ids"].add(record.record["location_id"])
                if section.section_key == "scenarios" and record.record.get("linked_design_id") == design_id:
                    if record.entity_id:
                        related_ids["scenario_ids"].add(record.entity_id)
        return related_ids

    def _include_ai_grounding_record(
        self,
        *,
        section_key: str,
        record: TwinPlanningContextRecord,
        design_id: Optional[str],
        related_ids: Dict[str, set],
    ) -> bool:
        if section_key == "unknowns":
            return False
        if not design_id:
            return True
        if section_key in AI_GROUNDING_BASE_SECTION_KEYS:
            return True
        if section_key == "designs":
            return record.entity_id == design_id
        if section_key == "design_equipment":
            return record.record.get("design_id") == design_id
        if section_key == "equipment_products":
            return record.entity_id in related_ids["product_ids"]
        if section_key == "equipment_locations":
            return record.entity_id in related_ids["location_ids"]
        if section_key == "pathways":
            return record.record.get("design_id") == design_id
        if section_key == "scenarios":
            return record.record.get("linked_design_id") == design_id
        if section_key == "scenario_revisions":
            return (
                record.record.get("linked_design_id") == design_id
                or record.record.get("scenario_id") in related_ids["scenario_ids"]
            )
        if section_key == "derived_intelligence":
            return record.record.get("design_id") == design_id
        return False

    def _ai_grounding_record(
        self, section_key: str, record: TwinPlanningContextRecord
    ) -> AIDesignGroundingRecord:
        return AIDesignGroundingRecord(
            section_key=section_key,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            label=record.label,
            classification=record.classification,
            authority_layer=record.authority_layer,
            data_classification=record.data_classification,
            data_origin=record.data_origin,
            fields=self._ai_grounding_fields(record),
            provenance_summary=record.provenance_summary,
            source_document_ids=record.source_document_ids,
            rule_keys=record.rule_keys,
            dependency_hooks=record.dependency_hooks,
            missing_fields=record.missing_fields,
            provenance_gaps=record.provenance_gaps,
            dependency_awareness=record.dependency_awareness,
            change_impact_hints=record.change_impact_hints,
            planning_dependency_warnings=record.planning_dependency_warnings,
            permission_readiness=self._ai_record_permission_readiness(record),
            limitations=record.limitations,
        )

    def _topology_node_id(self, entity_type: str, entity_id: Optional[str]) -> str:
        return f"{entity_type}:{entity_id or 'unknown'}"

    def _topology_lifecycle_domain(
        self, section_key: str, record: TwinPlanningContextRecord
    ) -> TwinTopologyLifecycleDomain:
        if section_key == "scenario_revisions":
            return TwinTopologyLifecycleDomain.saved_scenario_revision_topology
        if section_key in {"designs", "design_equipment", "pathways", "scenarios"}:
            return TwinTopologyLifecycleDomain.sandbox_proposed_planning_topology
        if (
            section_key == "derived_intelligence"
            or record.classification
            in {
                TwinPlanningRecordClassification.derived_output,
                TwinPlanningRecordClassification.advisory_output,
            }
        ):
            return TwinTopologyLifecycleDomain.derived_advisory_topology
        return TwinTopologyLifecycleDomain.recorded_current_topology

    def _topology_node(
        self, section_key: str, record: TwinPlanningContextRecord
    ) -> TwinTopologyNode:
        permission_not_enforced = True
        if record.permission_readiness is not None:
            permission_not_enforced = record.permission_readiness.permission_not_enforced
        return TwinTopologyNode(
            node_id=self._topology_node_id(record.entity_type, record.entity_id),
            section_key=section_key,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            label=record.label,
            lifecycle_domain=self._topology_lifecycle_domain(section_key, record),
            classification=record.classification,
            authority_layer=record.authority_layer,
            data_classification=record.data_classification,
            data_origin=record.data_origin,
            source_document_ids=record.source_document_ids,
            rule_keys=record.rule_keys,
            provenance_gap_types=sorted({gap.gap_type.value for gap in record.provenance_gaps}),
            dependency_awareness_labels=sorted({item.label.value for item in record.dependency_awareness}),
            permission_not_enforced=permission_not_enforced,
            limitations=record.limitations + TOPOLOGY_SNAPSHOT_LIMITATIONS,
        )

    def _topology_edge_lifecycle_domain(
        self, source_node: TwinTopologyNode, target_node: TwinTopologyNode
    ) -> TwinTopologyLifecycleDomain:
        domains = {source_node.lifecycle_domain, target_node.lifecycle_domain}
        if TwinTopologyLifecycleDomain.saved_scenario_revision_topology in domains:
            return TwinTopologyLifecycleDomain.saved_scenario_revision_topology
        if TwinTopologyLifecycleDomain.sandbox_proposed_planning_topology in domains:
            return TwinTopologyLifecycleDomain.sandbox_proposed_planning_topology
        if TwinTopologyLifecycleDomain.derived_advisory_topology in domains:
            return TwinTopologyLifecycleDomain.derived_advisory_topology
        return TwinTopologyLifecycleDomain.recorded_current_topology

    def _topology_edge_from_nodes(
        self,
        *,
        source_node: TwinTopologyNode,
        target_node: TwinTopologyNode,
        relationship: str,
        note: str,
        rule_keys: Optional[List[str]] = None,
        confidence_level: Optional[str] = "medium",
        limitations: Optional[List[str]] = None,
    ) -> TwinTopologyEdge:
        return TwinTopologyEdge(
            edge_id=(
                f"topology-edge:{source_node.node_id}->{target_node.node_id}:"
                f"{relationship}"
            ),
            source_node_id=source_node.node_id,
            target_node_id=target_node.node_id,
            source_entity_type=source_node.entity_type,
            source_entity_id=source_node.entity_id,
            target_entity_type=target_node.entity_type,
            target_entity_id=target_node.entity_id,
            relationship=relationship,
            lifecycle_domain=self._topology_edge_lifecycle_domain(source_node, target_node),
            rule_keys=rule_keys or [TOPOLOGY_RELATIONSHIP_COVERAGE_RULE_KEY],
            confidence_level=confidence_level,
            note=note,
            limitations=limitations or (
                TOPOLOGY_RELATIONSHIP_COVERAGE_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS
            ),
        )

    def _topology_edge_key(self, edge: TwinTopologyEdge) -> tuple:
        return (
            edge.source_node_id,
            edge.target_node_id,
            edge.relationship,
            tuple(edge.rule_keys),
        )

    def _sorted_topology_edges(self, edges: Dict[tuple, TwinTopologyEdge]) -> List[TwinTopologyEdge]:
        return sorted(
            edges.values(),
            key=lambda edge: (
                edge.source_node_id,
                edge.target_node_id,
                edge.relationship,
            ),
        )

    def _topology_edges(
        self,
        records: List[TwinPlanningContextRecord],
        node_map: Dict[tuple, TwinTopologyNode],
    ) -> List[TwinTopologyEdge]:
        edges = {}
        for record in records:
            for hook in record.dependency_hooks:
                source_key = (hook.source_entity_type, hook.source_entity_id)
                target_key = (hook.target_entity_type, hook.target_entity_id)
                source_node = node_map.get(source_key)
                target_node = node_map.get(target_key)
                if source_node is None or target_node is None:
                    continue
                edge_key = (
                    source_node.node_id,
                    target_node.node_id,
                    hook.relationship,
                    tuple(hook.rule_keys),
                )
                edges.setdefault(
                    edge_key,
                    self._topology_edge_from_nodes(
                        source_node=source_node,
                        target_node=target_node,
                        relationship=hook.relationship,
                        rule_keys=hook.rule_keys,
                        confidence_level=hook.confidence_level,
                        note=hook.note,
                        limitations=TOPOLOGY_SNAPSHOT_LIMITATIONS,
                    ),
                )
        return self._sorted_topology_edges(edges)

    def _topology_deduped_edges(self, edge_sets: List[List[TwinTopologyEdge]]) -> List[TwinTopologyEdge]:
        edges = {}
        for edge_set in edge_sets:
            for edge in edge_set:
                edges.setdefault(self._topology_edge_key(edge), edge)
        return self._sorted_topology_edges(edges)

    def _topology_record_map(
        self, section_records: List[tuple]
    ) -> Dict[tuple, TwinPlanningContextRecord]:
        return {
            (record.entity_type, record.entity_id): record
            for _, record in section_records
        }

    def _topology_resolution_key(self, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        normalized = str(value).strip().lower()
        return normalized or None

    def _topology_resolution_index(
        self,
        nodes: List[TwinTopologyNode],
        records_by_key: Dict[tuple, TwinPlanningContextRecord],
    ) -> Dict[str, Optional[TwinTopologyNode]]:
        candidates: Dict[str, Dict[str, TwinTopologyNode]] = {}

        def add_candidate(value: Optional[str], node: TwinTopologyNode):
            key = self._topology_resolution_key(value)
            if key is None:
                return
            candidates.setdefault(key, {})[node.node_id] = node

        for node in nodes:
            record = records_by_key.get((node.entity_type, node.entity_id))
            add_candidate(node.node_id, node)
            add_candidate(node.entity_id, node)
            add_candidate(node.label, node)
            if record is not None:
                add_candidate(record.record.get("name"), node)

        return {
            key: next(iter(value.values())) if len(value) == 1 else None
            for key, value in candidates.items()
        }

    def _resolve_topology_node(
        self,
        value: Optional[str],
        resolution_index: Dict[str, Optional[TwinTopologyNode]],
    ) -> Optional[TwinTopologyNode]:
        key = self._topology_resolution_key(value)
        if key is None:
            return None
        return resolution_index.get(key)

    def _missing_relationship_indicator(
        self,
        *,
        indicator: str,
        record: TwinPlanningContextRecord,
        field_name: Optional[str],
        attempted_value: Optional[str],
        relationship_family: str,
        reason: str,
        derived_from: Optional[List[str]] = None,
    ) -> TwinTopologyMissingRelationshipIndicator:
        return TwinTopologyMissingRelationshipIndicator(
            indicator=indicator,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            field_name=field_name,
            attempted_value=attempted_value,
            relationship_family=relationship_family,
            reason=reason,
            derived_from=derived_from or ["topology_record_fields", "topology_node_resolution_index"],
            limitations=TOPOLOGY_RELATIONSHIP_COVERAGE_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
        )

    def _topology_relationship_coverage_edges(
        self,
        section_records: List[tuple],
        node_map: Dict[tuple, TwinTopologyNode],
    ) -> tuple:
        records_by_key = self._topology_record_map(section_records)
        resolution_index = self._topology_resolution_index(list(node_map.values()), records_by_key)
        relationship_edges: List[TwinTopologyEdge] = []
        missing_indicators: List[TwinTopologyMissingRelationshipIndicator] = []

        def append_edge(source_node, target_node, relationship, note):
            relationship_edges.append(
                self._topology_edge_from_nodes(
                    source_node=source_node,
                    target_node=target_node,
                    relationship=relationship,
                    note=note,
                )
            )

        for _, record in section_records:
            source_node = node_map.get((record.entity_type, record.entity_id))
            if source_node is None:
                continue

            if record.entity_type == "building":
                target_node = node_map.get(("home", record.record.get("home_id")))
                if target_node:
                    append_edge(
                        source_node,
                        target_node,
                        "structure_belongs_to_premise_planning_context",
                        "Structure-to-premise placement is derived from existing building.home_id planning data.",
                    )
                else:
                    missing_indicators.append(
                        self._missing_relationship_indicator(
                            indicator="structure_premise_relationship_unresolved",
                            record=record,
                            field_name="home_id",
                            attempted_value=record.record.get("home_id"),
                            relationship_family="structure_premise_placement",
                            reason="Building home_id did not resolve to a concrete home topology node.",
                        )
                    )

            if record.entity_type in {"electrical_panel", "load", "equipment_location"}:
                target_node = node_map.get(("building", record.record.get("building_id")))
                relationship_by_type = {
                    "electrical_panel": (
                        "panel_assigned_to_building_planning_context",
                        "panel_building_placement",
                        "Panel-to-building placement is derived from existing electrical_panel.building_id planning data.",
                    ),
                    "load": (
                        "load_assigned_to_building_planning_context",
                        "load_building_placement",
                        "Load-to-building placement is derived from existing load.building_id planning data.",
                    ),
                    "equipment_location": (
                        "location_assigned_to_building_planning_context",
                        "location_building_placement",
                        "Equipment-location-to-building placement is derived from existing equipment_location.building_id planning data.",
                    ),
                }
                relationship, family, note = relationship_by_type[record.entity_type]
                if target_node:
                    append_edge(source_node, target_node, relationship, note)
                else:
                    missing_indicators.append(
                        self._missing_relationship_indicator(
                            indicator=f"{family}_unresolved",
                            record=record,
                            field_name="building_id",
                            attempted_value=record.record.get("building_id"),
                            relationship_family=family,
                            reason=f"{record.entity_type}.building_id did not resolve to a concrete building topology node.",
                        )
                    )

            if record.entity_type == "estimated_pathway":
                pathway_node = source_node
                design_node = node_map.get(("energy_system_design", record.record.get("design_id")))
                if design_node:
                    append_edge(
                        design_node,
                        pathway_node,
                        "design_includes_pathway_planning_context",
                        "Design-to-pathway relationship is derived from existing estimated_pathway.design_id planning data.",
                    )
                else:
                    missing_indicators.append(
                        self._missing_relationship_indicator(
                            indicator="design_pathway_relationship_unresolved",
                            record=record,
                            field_name="design_id",
                            attempted_value=record.record.get("design_id"),
                            relationship_family="design_pathway_reference",
                            reason="Pathway design_id did not resolve to a concrete design topology node.",
                        )
                    )

                for field_name, relationship in [
                    ("source_location", "pathway_source_location_planning_context"),
                    ("destination_location", "pathway_destination_location_planning_context"),
                ]:
                    attempted_value = record.record.get(field_name)
                    target_node = self._resolve_topology_node(attempted_value, resolution_index)
                    if target_node:
                        append_edge(
                            pathway_node,
                            target_node,
                            relationship,
                            (
                                f"Pathway {field_name} relationship is derived from an existing "
                                "estimated_pathway field that resolves to a concrete topology node."
                            ),
                        )
                    else:
                        missing_indicators.append(
                            self._missing_relationship_indicator(
                                indicator=f"pathway_{field_name}_relationship_unresolved",
                                record=record,
                                field_name=field_name,
                                attempted_value=attempted_value,
                                relationship_family="pathway_endpoint_reference",
                                reason=(
                                    "Pathway endpoint value is absent, ambiguous, or a string label that does "
                                    "not resolve to a concrete topology node."
                                ),
                            )
                        )

        return self._topology_deduped_edges([relationship_edges]), missing_indicators

    def _topology_relationship_coverage_summary(
        self,
        dependency_edges: List[TwinTopologyEdge],
        relationship_edges: List[TwinTopologyEdge],
        missing_relationship_indicators: List[TwinTopologyMissingRelationshipIndicator],
    ) -> TwinTopologyRelationshipCoverageSummary:
        coverage_by_family = Counter()
        for edge in relationship_edges:
            family = TOPOLOGY_RELATIONSHIP_FAMILY_BY_RELATIONSHIP.get(
                edge.relationship,
                "other_relationship_coverage",
            )
            coverage_by_family[family] += 1
        unresolved_pathway_endpoint_count = sum(
            1
            for indicator in missing_relationship_indicators
            if indicator.relationship_family == "pathway_endpoint_reference"
        )
        return TwinTopologyRelationshipCoverageSummary(
            relationship_edge_count=len(relationship_edges),
            dependency_hook_edge_count=len(dependency_edges),
            coverage_by_relationship_family=dict(sorted(coverage_by_family.items())),
            missing_relationship_indicator_count=len(missing_relationship_indicators),
            unresolved_pathway_endpoint_count=unresolved_pathway_endpoint_count,
            limitations=TOPOLOGY_RELATIONSHIP_COVERAGE_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
        )

    def _topology_scenario_branch_references(
        self,
        records: List[TwinPlanningContextRecord],
        node_map: Dict[tuple, TwinTopologyNode],
    ) -> List[Dict[str, object]]:
        references = []
        for record in records:
            if record.entity_type != "scenario":
                continue
            linked_design_id = record.record.get("linked_design_id")
            scenario_node = node_map.get(("scenario", record.entity_id))
            design_node = node_map.get(("energy_system_design", linked_design_id))
            references.append(
                {
                    "scenario_id": record.entity_id,
                    "linked_design_id": linked_design_id,
                    "scenario_node_id": scenario_node.node_id if scenario_node else None,
                    "linked_design_node_id": design_node.node_id if design_node else None,
                    "lifecycle_domain": TwinTopologyLifecycleDomain.sandbox_proposed_planning_topology.value,
                    "limitations": TOPOLOGY_SNAPSHOT_LIMITATIONS,
                }
            )
        return sorted(references, key=lambda item: item.get("scenario_id") or "")

    def _topology_revision_lineage_references(
        self,
        records: List[TwinPlanningContextRecord],
        node_map: Dict[tuple, TwinTopologyNode],
    ) -> List[Dict[str, object]]:
        references = []
        for record in records:
            if record.entity_type != "scenario_revision":
                continue
            scenario_id = record.record.get("scenario_id")
            linked_design_id = record.record.get("linked_design_id")
            parent_revision_id = record.record.get("parent_revision_id")
            revision_node = node_map.get(("scenario_revision", record.entity_id))
            scenario_node = node_map.get(("scenario", scenario_id))
            design_node = node_map.get(("energy_system_design", linked_design_id))
            parent_node = (
                node_map.get(("scenario_revision", parent_revision_id))
                if parent_revision_id
                else None
            )
            references.append(
                {
                    "revision_id": record.entity_id,
                    "scenario_id": scenario_id,
                    "linked_design_id": linked_design_id,
                    "parent_revision_id": parent_revision_id,
                    "revision_node_id": revision_node.node_id if revision_node else None,
                    "scenario_node_id": scenario_node.node_id if scenario_node else None,
                    "linked_design_node_id": design_node.node_id if design_node else None,
                    "parent_revision_node_id": parent_node.node_id if parent_node else None,
                    "lifecycle_domain": TwinTopologyLifecycleDomain.saved_scenario_revision_topology.value,
                    "limitations": TOPOLOGY_SNAPSHOT_LIMITATIONS,
                }
            )
        return sorted(references, key=lambda item: item.get("revision_id") or "")

    def _topology_readiness_status(
        self,
        nodes: List[TwinTopologyNode],
        provenance_gap_types: List[str],
        dependency_awareness_labels: List[str],
        planning_dependency_warning_types: List[str],
        source_document_count: int,
    ) -> str:
        if not nodes:
            return "not_represented_in_snapshot"
        dependency_limited_labels = {
            TwinPlanningDependencyAwarenessLabel.needs_recalculation.value,
            TwinPlanningDependencyAwarenessLabel.needs_regrounding.value,
            TwinPlanningDependencyAwarenessLabel.needs_review.value,
            TwinPlanningDependencyAwarenessLabel.stale_unknown.value,
        }
        has_dependency_limit = bool(planning_dependency_warning_types) or bool(
            dependency_limited_labels.intersection(dependency_awareness_labels)
        )
        if provenance_gap_types and has_dependency_limit:
            return "provenance_and_dependency_limited"
        if provenance_gap_types:
            return "provenance_limited"
        if has_dependency_limit:
            return "dependency_limited"
        if source_document_count == 0:
            return "source_limited"
        return "descriptive_planning_metadata_present"

    def _topology_lifecycle_readiness_hints(
        self,
        section_records: List[tuple],
        nodes: List[TwinTopologyNode],
        edges: List[TwinTopologyEdge],
    ) -> List[TwinTopologyLifecycleReadinessHint]:
        records_by_domain: Dict[TwinTopologyLifecycleDomain, List[TwinPlanningContextRecord]] = {
            domain: [] for domain in TwinTopologyLifecycleDomain
        }
        for section_key, record in section_records:
            records_by_domain[self._topology_lifecycle_domain(section_key, record)].append(record)

        nodes_by_domain: Dict[TwinTopologyLifecycleDomain, List[TwinTopologyNode]] = {
            domain: [] for domain in TwinTopologyLifecycleDomain
        }
        for node in nodes:
            nodes_by_domain[node.lifecycle_domain].append(node)

        edges_by_domain = Counter(edge.lifecycle_domain for edge in edges)
        readiness_hints = []
        for domain in TwinTopologyLifecycleDomain:
            domain_nodes = nodes_by_domain[domain]
            domain_records = records_by_domain[domain]
            provenance_gap_types = sorted(
                {
                    gap_type
                    for node in domain_nodes
                    for gap_type in node.provenance_gap_types
                }
            )
            dependency_awareness_labels = sorted(
                {
                    label
                    for node in domain_nodes
                    for label in node.dependency_awareness_labels
                }
            )
            warning_types = sorted(
                {
                    warning.warning_type
                    for record in domain_records
                    for warning in record.planning_dependency_warnings
                }
            )
            source_document_ids = {
                source_document_id
                for node in domain_nodes
                for source_document_id in node.source_document_ids
            }
            derived_from = ["topology_nodes", "topology_edges", "topology_snapshot_limitations"]
            if provenance_gap_types:
                derived_from.append("provenance_gap_types")
            if dependency_awareness_labels:
                derived_from.append("dependency_awareness_labels")
            if warning_types:
                derived_from.append("planning_dependency_warnings")
            if source_document_ids:
                derived_from.append("source_document_ids")

            hints = [
                (
                    f"{len(domain_nodes)} topology nodes and {edges_by_domain.get(domain, 0)} topology edges "
                    f"are represented for {domain.value}."
                ),
                "No lifecycle workflow, promotion workflow, event log, simulation, or operational authority is present.",
            ]
            if provenance_gap_types:
                hints.append(
                    "Readiness is limited by provenance gap types: "
                    + ", ".join(provenance_gap_types)
                    + "."
                )
            if warning_types:
                hints.append(
                    "Readiness is limited by planning dependency warnings: "
                    + ", ".join(warning_types)
                    + "."
                )
            if source_document_ids:
                hints.append(
                    f"{len(source_document_ids)} source document references are attached to nodes in this lifecycle domain."
                )
            elif domain_nodes:
                hints.append("No source document IDs are attached to nodes in this lifecycle domain.")

            readiness_hints.append(
                TwinTopologyLifecycleReadinessHint(
                    lifecycle_domain=domain,
                    readiness_status=self._topology_readiness_status(
                        domain_nodes,
                        provenance_gap_types,
                        dependency_awareness_labels,
                        warning_types,
                        len(source_document_ids),
                    ),
                    node_count=len(domain_nodes),
                    edge_count=edges_by_domain.get(domain, 0),
                    source_document_count=len(source_document_ids),
                    provenance_gap_types=provenance_gap_types,
                    dependency_awareness_labels=dependency_awareness_labels,
                    planning_dependency_warning_types=warning_types,
                    derived_from=derived_from,
                    hints=hints,
                    limitations=TOPOLOGY_READINESS_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
                )
            )
        return readiness_hints

    def _topology_deferred_lifecycle_domains(self) -> List[TwinTopologyDeferredLifecycleDomain]:
        return [
            TwinTopologyDeferredLifecycleDomain(
                lifecycle_domain=lifecycle_domain,
                deferred_reason=deferred_reason,
                required_future_foundations=required_future_foundations,
                limitations=TOPOLOGY_READINESS_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
            )
            for lifecycle_domain, deferred_reason, required_future_foundations in DEFERRED_TOPOLOGY_LIFECYCLE_DOMAINS
        ]

    def _topology_missing_readiness_indicators(
        self, snapshot_limitations: List[str]
    ) -> List[TwinTopologyMissingReadinessIndicator]:
        limitation_text = " ".join(snapshot_limitations).lower()
        indicators = []
        for indicator, marker, reason in TOPOLOGY_MISSING_READINESS_INDICATORS:
            source_marker_found = marker.lower() in limitation_text
            indicators.append(
                TwinTopologyMissingReadinessIndicator(
                    indicator=indicator,
                    present=False,
                    source_marker_found=source_marker_found,
                    reason=reason,
                    derived_from=["topology_snapshot_limitations"],
                    limitations=TOPOLOGY_READINESS_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
                )
            )
        return indicators

    def _topology_lifecycle_readiness_summary(
        self,
        nodes: List[TwinTopologyNode],
        edges: List[TwinTopologyEdge],
        records: List[TwinPlanningContextRecord],
        deferred_lifecycle_domains: List[TwinTopologyDeferredLifecycleDomain],
        missing_readiness_indicators: List[TwinTopologyMissingReadinessIndicator],
    ) -> TwinTopologyLifecycleReadinessSummary:
        domains_present = sorted(
            {
                node.lifecycle_domain.value
                for node in nodes
            }
        )
        provenance_gap_count = sum(len(node.provenance_gap_types) for node in nodes)
        dependency_labels = sorted(
            {
                label
                for node in nodes
                for label in node.dependency_awareness_labels
            }
        )
        planning_dependency_warning_count = sum(
            len(record.planning_dependency_warnings)
            for record in records
        )
        return TwinTopologyLifecycleReadinessSummary(
            node_count=len(nodes),
            edge_count=len(edges),
            domains_present=domains_present,
            domains_deferred=[domain.lifecycle_domain for domain in deferred_lifecycle_domains],
            provenance_gap_count=provenance_gap_count,
            planning_dependency_warning_count=planning_dependency_warning_count,
            dependency_awareness_labels=dependency_labels,
            missing_readiness_indicator_count=len(missing_readiness_indicators),
            limitations=TOPOLOGY_READINESS_LIMITATIONS + TOPOLOGY_SNAPSHOT_LIMITATIONS,
        )

    def build_topology_snapshot_view(self, db, home_id: str) -> Optional[TwinTopologySnapshot]:
        context = self.build(db, home_id)
        if context is None:
            return None

        section_records = [
            (section.section_key, record)
            for section in context.sections
            if section.section_key in TOPOLOGY_SNAPSHOT_SECTION_ALLOWLIST
            for record in section.records
            if record.entity_id is not None
        ]
        nodes = [
            self._topology_node(section_key, record)
            for section_key, record in section_records
        ]
        node_map = {
            (node.entity_type, node.entity_id): node
            for node in nodes
        }
        records = [record for _, record in section_records]
        dependency_edges = self._topology_edges(records, node_map)
        relationship_edges, missing_relationship_indicators = self._topology_relationship_coverage_edges(
            section_records,
            node_map,
        )
        edges = self._topology_deduped_edges([dependency_edges, relationship_edges])
        relationship_coverage_summary = self._topology_relationship_coverage_summary(
            dependency_edges,
            relationship_edges,
            missing_relationship_indicators,
        )
        lifecycle_counts = Counter(node.lifecycle_domain.value for node in nodes)
        lifecycle_domain_summary = {
            domain.value: lifecycle_counts.get(domain.value, 0)
            for domain in TwinTopologyLifecycleDomain
        }
        snapshot_limitations = [
            "No twin_id is created or inferred.",
            "No topology graph, graph database, canonical topology table, migration, or persisted topology state is created.",
            "No topology promotion workflow, lifecycle event log, recalculation engine, invalidation engine, simulation, or Phase 3 intelligence is implemented.",
            "No auth, RBAC/ABAC, permission enforcement, exports, utility sharing, telemetry governance, ownership transfer, registry, marketplace, or operational control is implemented.",
        ]
        readiness_hints = self._topology_lifecycle_readiness_hints(section_records, nodes, edges)
        deferred_lifecycle_domains = self._topology_deferred_lifecycle_domains()
        missing_readiness_indicators = self._topology_missing_readiness_indicators(
            snapshot_limitations
            + TOPOLOGY_SNAPSHOT_LIMITATIONS
        )
        readiness_summary = self._topology_lifecycle_readiness_summary(
            nodes,
            edges,
            records,
            deferred_lifecycle_domains,
            missing_readiness_indicators,
        )

        return TwinTopologySnapshot(
            home_id=home_id,
            implementation_boundary=(
                "Read-only topology snapshot derived from the existing home_id-anchored Twin Planning Context; "
                "not a persisted graph, canonical topology table, lifecycle event log, export, or operational model."
            ),
            nodes=nodes,
            edges=edges,
            scenario_branch_references=self._topology_scenario_branch_references(records, node_map),
            revision_lineage_references=self._topology_revision_lineage_references(records, node_map),
            lifecycle_domain_summary=lifecycle_domain_summary,
            lifecycle_readiness_summary=readiness_summary,
            lifecycle_readiness_hints=readiness_hints,
            deferred_lifecycle_domains=deferred_lifecycle_domains,
            missing_readiness_indicators=missing_readiness_indicators,
            relationship_coverage_summary=relationship_coverage_summary,
            missing_relationship_indicators=missing_relationship_indicators,
            limitations=snapshot_limitations,
            compatibility_note=(
                "Existing TwinPlanningContext, AI grounding, runtime projection, and current /api/* contracts remain unchanged; "
                "this is an additive topology snapshot view."
            ),
        )

    def _sorted_unique(self, values: Iterable[Optional[str]]) -> List[str]:
        return sorted({value for value in values if value})

    def _metadata_value_present(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value)
        if isinstance(value, (list, tuple, set)):
            return bool(value)
        if isinstance(value, dict):
            return bool(value)
        return True

    def _metadata_paths(
        self,
        value: Any,
        field_tokens: Iterable[str],
        *,
        path: str = "",
    ) -> List[str]:
        tokens = tuple(field_tokens)
        rels = _frozen_metadata_paths(_freeze_metadata_value(value), tokens)
        if not path:
            return list(rels)
        return sorted(
            path + rel if rel.startswith("[]") else f"{path}.{rel}" for rel in rels
        )

    def _phase4c_gap_categories(
        self,
        *,
        confidence_paths: List[str],
        missing_paths: List[str],
        unsafe_paths: List[str],
        limitation_paths: List[str],
        deferred_paths: List[str],
    ) -> List[str]:
        categories = []
        if confidence_paths:
            categories.append("confidence")
        if missing_paths:
            categories.append("missing_data")
        if unsafe_paths:
            categories.append("unsafe_assumption")
        if limitation_paths:
            categories.append("limitation")
        if deferred_paths:
            categories.append("deferred_boundary")
        return self._sorted_unique(categories)

    def _phase4d_normalized_source_paths(
        self,
        *,
        source_basis_paths: List[str],
        source_view_paths: List[str],
    ) -> List[str]:
        return self._sorted_unique(source_basis_paths + source_view_paths)

    def _metadata_has_truthy_scope_flag(
        self,
        value: Any,
        field_name: str,
    ) -> bool:
        if isinstance(value, dict):
            return any(
                (key == field_name and child_value is True)
                or self._metadata_has_truthy_scope_flag(child_value, field_name)
                for key, child_value in value.items()
                if key != "trust_provenance_readiness_summary"
            )
        if isinstance(value, list):
            return any(
                self._metadata_has_truthy_scope_flag(child_value, field_name)
                for child_value in value
            )
        return False

    def _phase4a_gap_notes(
        self,
        *,
        view_payload: Dict[str, Any],
        confidence_paths: List[str],
        missing_paths: List[str],
        unsafe_paths: List[str],
        limitation_paths: List[str],
        deferred_paths: List[str],
    ) -> List[str]:
        notes = []
        if confidence_paths and "confidence_posture" not in view_payload:
            notes.append("Confidence metadata is available through item-level or view-specific fields.")
        if missing_paths and not any(key.startswith("missing") for key in view_payload):
            notes.append("Missing-data metadata is available through item-level or view-specific fields.")
        if unsafe_paths and "unsafe_assumptions" not in view_payload:
            notes.append("Unsafe-assumption metadata is available through item-level fields.")
        if "advisory_limitations" in view_payload and "limitations" not in view_payload:
            notes.append("Limitation metadata uses advisory_limitations on this view.")
        if deferred_paths and not any(key.startswith("deferred") for key in view_payload):
            notes.append("Deferred-boundary metadata uses a view-specific capability field.")
        if any("." in path or "[]" in path for path in confidence_paths + missing_paths + unsafe_paths):
            notes.append("Some normalized metadata is present below top-level view fields.")
        return self._sorted_unique(notes)

    def _trust_provenance_readiness_summary(self, view: Any) -> TwinTrustProvenanceReadinessSummary:
        view_payload = view.dict(exclude_none=True)
        # Freeze once, then run every token sweep against the cached walker.
        frozen_payload = _freeze_metadata_value(view_payload)
        source_basis_paths = list(_frozen_metadata_paths(frozen_payload, ("source_basis", "basis")))
        source_view_paths = list(_frozen_metadata_paths(frozen_payload, ("source_view",)))
        provenance_paths = list(_frozen_metadata_paths(frozen_payload, ("provenance", "source_trust")))
        readiness_paths = list(
            _frozen_metadata_paths(frozen_payload, ("readiness", "eligibility", "scope", "summary"))
        )
        confidence_paths = list(_frozen_metadata_paths(frozen_payload, ("confidence",)))
        missing_paths = list(_frozen_metadata_paths(frozen_payload, ("missing", "unknown")))
        unsafe_paths = list(_frozen_metadata_paths(frozen_payload, ("unsafe",)))
        limitation_paths = list(_frozen_metadata_paths(frozen_payload, ("limitation",)))
        deferred_paths = list(_frozen_metadata_paths(frozen_payload, ("deferred", "blocked_deferred")))
        return TwinTrustProvenanceReadinessSummary(
            read_only_behavior_present=self._metadata_has_truthy_scope_flag(view_payload, "read_only"),
            request_time_behavior_present=self._metadata_has_truthy_scope_flag(view_payload, "request_time_only"),
            deterministic_behavior_present=self._metadata_has_truthy_scope_flag(
                view_payload,
                "deterministic_for_same_inputs",
            ),
            home_id_scope_present=(
                view_payload.get("anchor_type") == "home_id"
                and bool(view_payload.get("home_id"))
                and self._metadata_has_truthy_scope_flag(view_payload, "home_id_anchored")
            ),
            source_basis_present=bool(source_basis_paths),
            provenance_basis_present=bool(provenance_paths),
            readiness_metadata_present=bool(readiness_paths),
            confidence_metadata_present=bool(confidence_paths),
            missing_data_metadata_present=bool(missing_paths),
            unsafe_assumption_metadata_present=bool(unsafe_paths),
            limitation_metadata_present=bool(limitation_paths),
            deferred_boundary_metadata_present=bool(deferred_paths),
            permission_enforcement=view_payload.get("permission_enforcement", "not_enforced"),
            permission_enforcement_remains_not_enforced=(
                view_payload.get("permission_enforcement") == "not_enforced"
            ),
            source_basis_field_names=source_basis_paths,
            provenance_basis_field_names=provenance_paths,
            readiness_metadata_field_names=readiness_paths,
            confidence_metadata_field_names=confidence_paths,
            missing_data_metadata_field_names=missing_paths,
            unsafe_assumption_metadata_field_names=unsafe_paths,
            limitation_metadata_field_names=limitation_paths,
            deferred_boundary_metadata_field_names=deferred_paths,
            normalized_gap_categories=self._phase4c_gap_categories(
                confidence_paths=confidence_paths,
                missing_paths=missing_paths,
                unsafe_paths=unsafe_paths,
                limitation_paths=limitation_paths,
                deferred_paths=deferred_paths,
            ),
            normalized_source_field_paths=self._phase4d_normalized_source_paths(
                source_basis_paths=source_basis_paths,
                source_view_paths=source_view_paths,
            ),
            normalized_provenance_field_paths=provenance_paths,
            normalized_readiness_field_paths=readiness_paths,
            hardened_readiness_boundary="advisory_metadata_only",
            unsupported_capability_claims_absent=True,
            gap_notes=self._phase4a_gap_notes(
                view_payload=view_payload,
                confidence_paths=confidence_paths,
                missing_paths=missing_paths,
                unsafe_paths=unsafe_paths,
                limitation_paths=limitation_paths,
                deferred_paths=deferred_paths,
            ),
            limitations=[
                "Phase 4A summary normalizes metadata visibility only.",
                "Presence flags mean response metadata exists; they are not capability, review, enforcement, or execution claims.",
                "This summary is derived request-time from existing response fields and does not replace view-specific basis, limitation, or boundary fields.",
            ],
        )

    def _attach_trust_provenance_readiness_summary(self, view: Any) -> Any:
        view.trust_provenance_readiness_summary = self._trust_provenance_readiness_summary(view)
        return view

    def _dependency_warning_ref(self, warning: TwinPlanningDependencyWarning) -> str:
        return ":".join(
            [
                warning.entity_type,
                warning.entity_id or "unknown",
                warning.warning_type,
            ]
        )

    def _provenance_gap_ref(self, gap: TwinPlanningProvenanceGap) -> str:
        return ":".join(
            [
                gap.gap_type.value,
                gap.entity_type,
                gap.entity_id or "unknown",
                gap.field_name or "record",
            ]
        )

    def _missing_readiness_ref(self, indicator: TwinTopologyMissingReadinessIndicator) -> str:
        return indicator.indicator

    def _missing_relationship_ref(self, indicator: TwinTopologyMissingRelationshipIndicator) -> str:
        return ":".join(
            [
                indicator.indicator,
                indicator.entity_type,
                indicator.entity_id or "unknown",
                indicator.field_name or "relationship",
            ]
        )

    def _all_context_records_with_sections(
        self, context: TwinPlanningContext
    ) -> List[tuple]:
        return [
            (section.section_key, record)
            for section in context.sections
            for record in section.records
        ]

    def _dependency_impact_lifecycle_signals(
        self, snapshot: TwinTopologySnapshot
    ) -> List[str]:
        signals = []
        for domain in sorted(snapshot.lifecycle_readiness_summary.domains_present):
            signals.append(f"summary:domain_present:{domain}")
        for domain in sorted(snapshot.lifecycle_readiness_summary.domains_deferred):
            signals.append(f"summary:domain_deferred:{domain}")
        for hint in sorted(
            snapshot.lifecycle_readiness_hints,
            key=lambda item: item.lifecycle_domain.value,
        ):
            signals.append(
                f"hint:{hint.lifecycle_domain.value}:{hint.readiness_status}"
            )
        for indicator in sorted(
            snapshot.missing_readiness_indicators,
            key=lambda item: item.indicator,
        ):
            signals.append(
                f"missing_readiness:{indicator.indicator}:present:{str(indicator.present).lower()}"
            )
        return signals

    def _dependency_impact_basis(
        self,
        *,
        source_section_keys: Optional[List[str]] = None,
        topology_node_ids: Optional[List[str]] = None,
        topology_edge_ids: Optional[List[str]] = None,
        lifecycle_readiness_signals_used: Optional[List[str]] = None,
        dependency_warning_refs: Optional[List[str]] = None,
        provenance_gap_refs: Optional[List[str]] = None,
        missing_readiness_indicator_refs: Optional[List[str]] = None,
        missing_relationship_indicator_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
        source_view_names: Optional[List[str]] = None,
        limitations: Optional[List[str]] = None,
    ) -> TwinDependencyImpactStatementBasis:
        return TwinDependencyImpactStatementBasis(
            source_view_names=self._sorted_unique(
                source_view_names or ["twin_planning_context", "topology_snapshot"]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            topology_node_ids=self._sorted_unique(topology_node_ids or []),
            topology_edge_ids=self._sorted_unique(topology_edge_ids or []),
            lifecycle_readiness_signals_used=self._sorted_unique(
                lifecycle_readiness_signals_used or []
            ),
            dependency_warning_refs=self._sorted_unique(dependency_warning_refs or []),
            provenance_gap_refs=self._sorted_unique(provenance_gap_refs or []),
            missing_readiness_indicator_refs=self._sorted_unique(
                missing_readiness_indicator_refs or []
            ),
            missing_relationship_indicator_refs=self._sorted_unique(
                missing_relationship_indicator_refs or []
            ),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=limitations or DEPENDENCY_IMPACT_READINESS_LIMITATIONS,
        )

    def _dependency_impact_record_refs(
        self, section_records: List[tuple]
    ) -> tuple:
        warning_refs = []
        provenance_gap_refs = []
        sections_by_entity = {}
        for section_key, record in section_records:
            sections_by_entity.setdefault((record.entity_type, record.entity_id), set()).add(section_key)
            for warning in record.planning_dependency_warnings:
                warning_refs.append(self._dependency_warning_ref(warning))
            for gap in record.provenance_gaps:
                provenance_gap_refs.append(self._provenance_gap_ref(gap))
        return warning_refs, provenance_gap_refs, sections_by_entity

    def _dependency_impact_confidence_posture(
        self,
        *,
        warning_refs: List[str],
        provenance_gap_refs: List[str],
        missing_readiness_refs: List[str],
        missing_relationship_refs: List[str],
    ) -> str:
        has_dependency_limits = bool(warning_refs or missing_relationship_refs)
        has_missing_readiness = bool(missing_readiness_refs)
        has_provenance_limits = bool(provenance_gap_refs)
        if has_provenance_limits and (has_dependency_limits or has_missing_readiness):
            return "provenance_dependency_and_missing_information_limited"
        if has_provenance_limits:
            return "provenance_limited"
        if has_dependency_limits:
            return "dependency_limited"
        if has_missing_readiness:
            return "missing_readiness_limited"
        return "descriptive_planning_context_present"

    def _dependency_impact_nodes_for_domain(
        self, snapshot: TwinTopologySnapshot, lifecycle_domain: TwinTopologyLifecycleDomain
    ) -> List[str]:
        return [
            node.node_id
            for node in snapshot.nodes
            if node.lifecycle_domain == lifecycle_domain
        ]

    def _dependency_impact_edges_for_domain(
        self, snapshot: TwinTopologySnapshot, lifecycle_domain: TwinTopologyLifecycleDomain
    ) -> List[str]:
        return [
            edge.edge_id
            for edge in snapshot.edges
            if edge.lifecycle_domain == lifecycle_domain
        ]

    def _dependency_impact_edges_for_nodes(
        self, snapshot: TwinTopologySnapshot, node_ids: List[str]
    ) -> List[str]:
        node_id_set = set(node_ids)
        return [
            edge.edge_id
            for edge in snapshot.edges
            if edge.source_node_id in node_id_set or edge.target_node_id in node_id_set
        ]

    def _dependency_impact_lifecycle_scope(
        self,
        *,
        snapshot: TwinTopologySnapshot,
        sections_by_entity: Dict[tuple, set],
    ) -> List[TwinDependencyImpactPostureItem]:
        items = []
        for hint in sorted(
            snapshot.lifecycle_readiness_hints,
            key=lambda item: item.lifecycle_domain.value,
        ):
            node_ids = self._dependency_impact_nodes_for_domain(snapshot, hint.lifecycle_domain)
            edge_ids = self._dependency_impact_edges_for_domain(snapshot, hint.lifecycle_domain)
            source_sections = []
            node_keys = {
                (node.entity_type, node.entity_id)
                for node in snapshot.nodes
                if node.node_id in set(node_ids)
            }
            for key in node_keys:
                source_sections.extend(sections_by_entity.get(key, []))
            signal = f"hint:{hint.lifecycle_domain.value}:{hint.readiness_status}"
            statement = (
                f"{hint.lifecycle_domain.value} is represented by {hint.node_count} topology nodes "
                f"and {hint.edge_count} topology edges with readiness status {hint.readiness_status}."
            )
            items.append(
                TwinDependencyImpactPostureItem(
                    impact_area=f"lifecycle_scope:{hint.lifecycle_domain.value}",
                    posture=hint.readiness_status,
                    statement=statement,
                    confidence_posture=hint.readiness_status,
                    basis=self._dependency_impact_basis(
                        source_section_keys=source_sections,
                        topology_node_ids=node_ids,
                        topology_edge_ids=edge_ids,
                        lifecycle_readiness_signals_used=[signal],
                        dependency_warning_refs=[
                            f"{warning_type}:{hint.lifecycle_domain.value}"
                            for warning_type in hint.planning_dependency_warning_types
                        ],
                        provenance_gap_refs=[
                            f"{gap_type}:{hint.lifecycle_domain.value}"
                            for gap_type in hint.provenance_gap_types
                        ],
                        derived_from=hint.derived_from,
                    ),
                    limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS + hint.limitations,
                )
            )
        return items

    def _dependency_impact_posture_items(
        self,
        *,
        context: TwinPlanningContext,
        snapshot: TwinTopologySnapshot,
        warning_refs: List[str],
        provenance_gap_refs: List[str],
        missing_readiness_refs: List[str],
        missing_relationship_refs: List[str],
        lifecycle_signals: List[str],
    ) -> List[TwinDependencyImpactPostureItem]:
        section_keys = [section.section_key for section in context.sections]
        node_ids = [node.node_id for node in snapshot.nodes]
        edge_ids = [edge.edge_id for edge in snapshot.edges]
        confidence_posture = self._dependency_impact_confidence_posture(
            warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_refs=missing_readiness_refs,
            missing_relationship_refs=missing_relationship_refs,
        )

        relationship_statement = (
            "Topology relationship coverage is derived from existing topology nodes and edges; "
            f"{snapshot.relationship_coverage_summary.missing_relationship_indicator_count} unresolved relationship indicators are present."
        )
        dependency_statement = (
            "Dependency posture is derived from existing planning dependency warnings; "
            f"{len(set(warning_refs))} warning references are present."
        )
        awareness_labels = sorted(context.dependency_awareness_summary.keys())
        awareness_statement = (
            "Dependency awareness labels are copied from the existing Twin Planning Context summary: "
            + (", ".join(awareness_labels) if awareness_labels else "none")
            + "."
        )
        return [
            TwinDependencyImpactPostureItem(
                impact_area="relationship_coverage",
                posture=(
                    "relationship_limited"
                    if missing_relationship_refs
                    else "descriptive_relationship_coverage_present"
                ),
                statement=relationship_statement,
                confidence_posture=confidence_posture,
                basis=self._dependency_impact_basis(
                    source_section_keys=section_keys,
                    topology_node_ids=node_ids,
                    topology_edge_ids=edge_ids,
                    lifecycle_readiness_signals_used=lifecycle_signals,
                    dependency_warning_refs=warning_refs,
                    provenance_gap_refs=provenance_gap_refs,
                    missing_readiness_indicator_refs=missing_readiness_refs,
                    missing_relationship_indicator_refs=missing_relationship_refs,
                    derived_from=[
                        "TwinTopologySnapshot.nodes",
                        "TwinTopologySnapshot.edges",
                        "TwinTopologySnapshot.relationship_coverage_summary",
                        "TwinTopologySnapshot.missing_relationship_indicators",
                    ],
                ),
                limitations=(
                    DEPENDENCY_IMPACT_READINESS_LIMITATIONS
                    + snapshot.relationship_coverage_summary.limitations
                ),
            ),
            TwinDependencyImpactPostureItem(
                impact_area="planning_dependency_warnings",
                posture=(
                    "dependency_limited"
                    if warning_refs
                    else "no_dependency_warnings_present"
                ),
                statement=dependency_statement,
                confidence_posture=confidence_posture,
                basis=self._dependency_impact_basis(
                    source_section_keys=section_keys,
                    topology_node_ids=node_ids,
                    topology_edge_ids=edge_ids,
                    lifecycle_readiness_signals_used=lifecycle_signals,
                    dependency_warning_refs=warning_refs,
                    provenance_gap_refs=provenance_gap_refs,
                    missing_readiness_indicator_refs=missing_readiness_refs,
                    missing_relationship_indicator_refs=missing_relationship_refs,
                    derived_from=[
                        "TwinPlanningContextRecord.planning_dependency_warnings",
                        "TwinTopologySnapshot.lifecycle_readiness_summary",
                    ],
                ),
                limitations=(
                    DEPENDENCY_IMPACT_READINESS_LIMITATIONS
                    + PLANNING_DEPENDENCY_WARNING_LIMITATIONS
                ),
            ),
            TwinDependencyImpactPostureItem(
                impact_area="dependency_awareness_summary",
                posture=(
                    "dependency_awareness_labels_present"
                    if awareness_labels
                    else "no_dependency_awareness_labels_present"
                ),
                statement=awareness_statement,
                confidence_posture=confidence_posture,
                basis=self._dependency_impact_basis(
                    source_section_keys=section_keys,
                    topology_node_ids=node_ids,
                    topology_edge_ids=edge_ids,
                    lifecycle_readiness_signals_used=lifecycle_signals,
                    dependency_warning_refs=warning_refs,
                    provenance_gap_refs=provenance_gap_refs,
                    missing_readiness_indicator_refs=missing_readiness_refs,
                    missing_relationship_indicator_refs=missing_relationship_refs,
                    derived_from=[
                        "TwinPlanningContext.dependency_awareness_summary",
                        "TwinTopologySnapshot.lifecycle_readiness_summary",
                    ],
                ),
                limitations=(
                    DEPENDENCY_IMPACT_READINESS_LIMITATIONS
                    + DEPENDENCY_AWARENESS_LIMITATIONS
                ),
            ),
        ]

    def _dependency_missing_inputs(
        self,
        *,
        snapshot: TwinTopologySnapshot,
        provenance_gap_refs: List[str],
    ) -> List[TwinDependencyMissingInputItem]:
        items: List[TwinDependencyMissingInputItem] = []
        for indicator in sorted(
            snapshot.missing_readiness_indicators,
            key=lambda item: item.indicator,
        ):
            if indicator.present:
                continue
            items.append(
                TwinDependencyMissingInputItem(
                    missing_input=indicator.indicator,
                    reason=indicator.reason,
                    basis=self._dependency_impact_basis(
                        missing_readiness_indicator_refs=[self._missing_readiness_ref(indicator)],
                        derived_from=indicator.derived_from,
                    ),
                    limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS + indicator.limitations,
                )
            )

        for indicator in sorted(
            snapshot.missing_relationship_indicators,
            key=lambda item: self._missing_relationship_ref(item),
        ):
            items.append(
                TwinDependencyMissingInputItem(
                    missing_input=self._missing_relationship_ref(indicator),
                    reason=indicator.reason,
                    basis=self._dependency_impact_basis(
                        missing_relationship_indicator_refs=[
                            self._missing_relationship_ref(indicator)
                        ],
                        derived_from=indicator.derived_from,
                    ),
                    limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS + indicator.limitations,
                )
            )

        for gap_ref in sorted(set(provenance_gap_refs)):
            items.append(
                TwinDependencyMissingInputItem(
                    missing_input=f"provenance:{gap_ref}",
                    reason=(
                        "A source or provenance basis is missing or partial for this recorded planning context."
                    ),
                    basis=self._dependency_impact_basis(
                        provenance_gap_refs=[gap_ref],
                        derived_from=["TwinPlanningContextRecord.provenance_gaps"],
                    ),
                    limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
                )
            )
        return items

    def _dependency_provenance_gap_posture(
        self,
        *,
        context: TwinPlanningContext,
        snapshot: TwinTopologySnapshot,
    ) -> List[TwinDependencyImpactPostureItem]:
        section_records = self._all_context_records_with_sections(context)
        node_by_entity = {
            (node.entity_type, node.entity_id): node
            for node in snapshot.nodes
        }
        refs_by_gap_type: Dict[str, List[str]] = {}
        node_ids_by_gap_type: Dict[str, List[str]] = {}
        sections_by_gap_type: Dict[str, List[str]] = {}
        for section_key, record in section_records:
            node = node_by_entity.get((record.entity_type, record.entity_id))
            for gap in record.provenance_gaps:
                gap_type = gap.gap_type.value
                refs_by_gap_type.setdefault(gap_type, []).append(self._provenance_gap_ref(gap))
                sections_by_gap_type.setdefault(gap_type, []).append(section_key)
                if node is not None:
                    node_ids_by_gap_type.setdefault(gap_type, []).append(node.node_id)

        items = []
        for gap_type in sorted(refs_by_gap_type):
            node_ids = node_ids_by_gap_type.get(gap_type, [])
            refs = refs_by_gap_type[gap_type]
            edge_ids = self._dependency_impact_edges_for_nodes(snapshot, node_ids)
            items.append(
                TwinDependencyImpactPostureItem(
                    impact_area=f"provenance_gap:{gap_type}",
                    posture="provenance_limited",
                    statement=(
                        f"{len(set(refs))} {gap_type} provenance gap references are present in the existing Twin Planning Context."
                    ),
                    confidence_posture="provenance_limited",
                    basis=self._dependency_impact_basis(
                        source_section_keys=sections_by_gap_type.get(gap_type, []),
                        topology_node_ids=node_ids,
                        topology_edge_ids=edge_ids,
                        provenance_gap_refs=refs,
                        derived_from=["TwinPlanningContextRecord.provenance_gaps"],
                    ),
                    limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
                )
            )
        return items

    def build_dependency_impact_readiness_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
    ) -> Optional[TwinDependencyImpactReadinessView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        warning_refs, provenance_gap_refs, sections_by_entity = self._dependency_impact_record_refs(
            section_records
        )
        missing_readiness_refs = [
            self._missing_readiness_ref(indicator)
            for indicator in snapshot.missing_readiness_indicators
            if not indicator.present
        ]
        missing_relationship_refs = [
            self._missing_relationship_ref(indicator)
            for indicator in snapshot.missing_relationship_indicators
        ]
        lifecycle_signals = self._dependency_impact_lifecycle_signals(snapshot)
        source_section_keys = [section.section_key for section in context.sections]
        topology_node_ids = [node.node_id for node in snapshot.nodes]
        topology_edge_ids = [edge.edge_id for edge in snapshot.edges]
        confidence_posture = self._dependency_impact_confidence_posture(
            warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_refs=missing_readiness_refs,
            missing_relationship_refs=missing_relationship_refs,
        )

        source_basis = self._dependency_impact_basis(
            source_section_keys=source_section_keys,
            topology_node_ids=topology_node_ids,
            topology_edge_ids=topology_edge_ids,
            lifecycle_readiness_signals_used=lifecycle_signals,
            dependency_warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_refs,
            missing_relationship_indicator_refs=missing_relationship_refs,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinTopologySnapshot.lifecycle_readiness_summary",
                "TwinTopologySnapshot.relationship_coverage_summary",
            ],
        )

        confidence_item = TwinDependencyImpactPostureItem(
            impact_area="overall_confidence_posture",
            posture=confidence_posture,
            statement=(
                "Overall dependency impact readiness confidence is derived from planning dependency warnings, "
                "provenance gaps, missing lifecycle readiness indicators, and missing relationship indicators."
            ),
            confidence_posture=confidence_posture,
            basis=source_basis,
            limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS,
        )

        return self._attach_trust_provenance_readiness_summary(TwinDependencyImpactReadinessView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3A derived intelligence envelope built request-time from TwinPlanningContext "
                "and topology snapshot; not a graph engine, scenario engine, simulation, what-if analysis, "
                "export, permission enforcement layer, or operational model."
            ),
            source_basis=source_basis,
            readiness_summary=TwinDependencyImpactReadinessSummary(
                limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS,
            ),
            lifecycle_scope=self._dependency_impact_lifecycle_scope(
                snapshot=snapshot,
                sections_by_entity=sections_by_entity,
            ),
            dependency_impact_posture=self._dependency_impact_posture_items(
                context=context,
                snapshot=snapshot,
                warning_refs=warning_refs,
                provenance_gap_refs=provenance_gap_refs,
                missing_readiness_refs=missing_readiness_refs,
                missing_relationship_refs=missing_relationship_refs,
                lifecycle_signals=lifecycle_signals,
            ),
            missing_inputs=self._dependency_missing_inputs(
                snapshot=snapshot,
                provenance_gap_refs=provenance_gap_refs,
            ),
            provenance_gap_posture=self._dependency_provenance_gap_posture(
                context=context,
                snapshot=snapshot,
            ),
            confidence_posture=[confidence_item],
            deferred_capabilities=sorted(DEPENDENCY_IMPACT_DEFERRED_CAPABILITIES),
            limitations=DEPENDENCY_IMPACT_READINESS_LIMITATIONS,
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, AI grounding, runtime projection, and current /api/* "
                "contracts remain unchanged; this is an additive Phase 3A derived intelligence view."
            ),
        ))

    def _dependency_reasoning_basis(
        self,
        *,
        source_section_keys: Optional[List[str]] = None,
        topology_node_ids: Optional[List[str]] = None,
        topology_edge_ids: Optional[List[str]] = None,
        lifecycle_readiness_signals_used: Optional[List[str]] = None,
        dependency_warning_refs: Optional[List[str]] = None,
        provenance_gap_refs: Optional[List[str]] = None,
        missing_readiness_indicator_refs: Optional[List[str]] = None,
        missing_relationship_indicator_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinDependencyImpactStatementBasis:
        return self._dependency_impact_basis(
            source_view_names=[
                "twin_planning_context",
                "topology_snapshot",
                "dependency_impact_readiness",
            ],
            source_section_keys=source_section_keys,
            topology_node_ids=topology_node_ids,
            topology_edge_ids=topology_edge_ids,
            lifecycle_readiness_signals_used=lifecycle_readiness_signals_used,
            dependency_warning_refs=dependency_warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_indicator_refs,
            missing_relationship_indicator_refs=missing_relationship_indicator_refs,
            derived_from=derived_from,
            limitations=DEPENDENCY_REASONING_LIMITATIONS,
        )

    def _dependency_reasoning_item_sort_key(self, item: TwinDependencyReasoningItem) -> tuple:
        return (item.reasoning_type.value, item.subject_ref, item.statement)

    def _dependency_reasoning_items_from_edges(
        self, snapshot: TwinTopologySnapshot
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for edge in sorted(snapshot.edges, key=lambda item: item.edge_id):
            basis = self._dependency_reasoning_basis(
                topology_node_ids=[edge.source_node_id, edge.target_node_id],
                topology_edge_ids=[edge.edge_id],
                lifecycle_readiness_signals_used=[
                    f"edge_lifecycle:{edge.lifecycle_domain.value}"
                ],
                derived_from=[
                    "TwinTopologySnapshot.edges",
                    "TwinTopologyEdge.source_node_id",
                    "TwinTopologyEdge.target_node_id",
                    "TwinTopologyEdge.relationship",
                ],
            )
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.topology_dependency,
                    subject_ref=edge.edge_id,
                    statement=(
                        f"Topology edge {edge.edge_id} explains that {edge.source_node_id} is the recorded "
                        f"source side and {edge.target_node_id} is the recorded target side for relationship {edge.relationship}."
                    ),
                    confidence_posture=edge.confidence_level or "descriptive_topology_relationship",
                    basis=basis,
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + edge.limitations,
                )
            )
        return items

    def _dependency_reasoning_upstream_downstream_items(
        self, snapshot: TwinTopologySnapshot
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for edge in sorted(snapshot.edges, key=lambda item: item.edge_id):
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.topology_dependency,
                    subject_ref=f"direction:{edge.edge_id}",
                    statement=(
                        f"Directional dependency interpretation for {edge.edge_id} follows topology edge metadata only: "
                        f"{edge.source_node_id} is upstream/source-side context and {edge.target_node_id} is downstream/target-side context."
                    ),
                    confidence_posture=edge.confidence_level or "source_target_metadata_only",
                    basis=self._dependency_reasoning_basis(
                        topology_node_ids=[edge.source_node_id, edge.target_node_id],
                        topology_edge_ids=[edge.edge_id],
                        lifecycle_readiness_signals_used=[
                            f"edge_lifecycle:{edge.lifecycle_domain.value}"
                        ],
                        derived_from=[
                            "TwinTopologySnapshot.edges",
                            "TwinTopologyEdge.source_node_id",
                            "TwinTopologyEdge.target_node_id",
                        ],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS
                    + [
                        "Upstream/downstream means topology edge source/target direction only; it is not measured power flow, field verification, utility approval, or operational direction.",
                    ],
                )
            )
        return items

    def _dependency_reasoning_source_items(
        self,
        *,
        section_records: List[tuple],
        node_by_entity: Dict[tuple, TwinTopologyNode],
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for section_key, record in sorted(
            section_records,
            key=lambda item: (item[0], item[1].entity_type, item[1].entity_id or ""),
        ):
            if not (record.source_document_ids or record.data_origin or record.provenance_summary):
                continue
            subject_ref = f"{record.entity_type}:{record.entity_id or 'unknown'}"
            node = node_by_entity.get((record.entity_type, record.entity_id))
            source_basis_parts = []
            if record.source_document_ids:
                source_basis_parts.append(f"{len(record.source_document_ids)} source document refs")
            if record.data_origin:
                source_basis_parts.append(f"data origin {record.data_origin.value}")
            if record.provenance_summary:
                source_basis_parts.append("provenance summary")
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.source_dependency,
                    subject_ref=subject_ref,
                    statement=(
                        f"{subject_ref} has source dependency context from existing "
                        f"{', '.join(source_basis_parts)}."
                    ),
                    confidence_posture="source_context_present",
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=[section_key],
                        topology_node_ids=[node.node_id] if node else [],
                        provenance_gap_refs=[
                            self._provenance_gap_ref(gap)
                            for gap in record.provenance_gaps
                        ],
                        derived_from=[
                            "TwinPlanningContextRecord.source_document_ids",
                            "TwinPlanningContextRecord.data_origin",
                            "TwinPlanningContextRecord.provenance_summary",
                        ],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS
                    + [
                        "Source dependency context identifies recorded source posture only; it does not verify correctness or create field authority.",
                    ],
                )
            )
        return items

    def _dependency_reasoning_lifecycle_items(
        self, impact_view: TwinDependencyImpactReadinessView
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for impact_item in sorted(impact_view.lifecycle_scope, key=lambda item: item.impact_area):
            basis = self._dependency_reasoning_basis(
                source_section_keys=impact_item.basis.source_section_keys,
                topology_node_ids=impact_item.basis.topology_node_ids,
                topology_edge_ids=impact_item.basis.topology_edge_ids,
                lifecycle_readiness_signals_used=impact_item.basis.lifecycle_readiness_signals_used,
                dependency_warning_refs=impact_item.basis.dependency_warning_refs,
                provenance_gap_refs=impact_item.basis.provenance_gap_refs,
                missing_readiness_indicator_refs=impact_item.basis.missing_readiness_indicator_refs,
                missing_relationship_indicator_refs=impact_item.basis.missing_relationship_indicator_refs,
                derived_from=impact_item.basis.derived_from
                + ["TwinDependencyImpactReadinessView.lifecycle_scope"],
            )
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.lifecycle_dependency,
                    subject_ref=impact_item.impact_area,
                    statement=(
                        f"Lifecycle dependency context for {impact_item.impact_area} is explained from Phase 3A posture {impact_item.posture}: {impact_item.statement}"
                    ),
                    confidence_posture=impact_item.confidence_posture,
                    basis=basis,
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + impact_item.limitations,
                )
            )
        return items

    def _dependency_reasoning_rule_items(
        self,
        *,
        section_records: List[tuple],
        snapshot: TwinTopologySnapshot,
    ) -> List[TwinDependencyReasoningItem]:
        sections_by_rule: Dict[str, List[str]] = {}
        edge_ids_by_rule: Dict[str, List[str]] = {}
        warning_refs_by_rule: Dict[str, List[str]] = {}
        for section_key, record in section_records:
            rule_keys = list(record.rule_keys)
            for hook in record.dependency_hooks:
                rule_keys.extend(hook.rule_keys)
            for warning in record.planning_dependency_warnings:
                for rule_key in warning.rule_keys:
                    warning_refs_by_rule.setdefault(rule_key, []).append(
                        self._dependency_warning_ref(warning)
                    )
                    rule_keys.append(rule_key)
            for rule_key in rule_keys:
                sections_by_rule.setdefault(rule_key, []).append(section_key)
        for edge in snapshot.edges:
            for rule_key in edge.rule_keys:
                edge_ids_by_rule.setdefault(rule_key, []).append(edge.edge_id)

        items = []
        for rule_key in sorted(set(sections_by_rule) | set(edge_ids_by_rule)):
            section_count = len(set(sections_by_rule.get(rule_key, [])))
            edge_count = len(set(edge_ids_by_rule.get(rule_key, [])))
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.rule_dependency,
                    subject_ref=rule_key,
                    statement=(
                        f"Rule dependency {rule_key} appears in {section_count} Twin Planning Context sections "
                        f"and {edge_count} topology edges."
                    ),
                    confidence_posture="deterministic_rule_reference_present",
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=sections_by_rule.get(rule_key, []),
                        topology_edge_ids=edge_ids_by_rule.get(rule_key, []),
                        dependency_warning_refs=warning_refs_by_rule.get(rule_key, []),
                        derived_from=[
                            "TwinPlanningContextRecord.rule_keys",
                            "TwinPlanningDependencyHook.rule_keys",
                            "TwinPlanningDependencyWarning.rule_keys",
                            "TwinTopologyEdge.rule_keys",
                        ],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS
                    + [
                        "Rule dependency context identifies existing rule references only; it does not run a recalculation or choose an action.",
                    ],
                )
            )
        return items

    def _dependency_reasoning_provenance_items(
        self, impact_view: TwinDependencyImpactReadinessView
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for impact_item in sorted(impact_view.provenance_gap_posture, key=lambda item: item.impact_area):
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.provenance_dependency,
                    subject_ref=impact_item.impact_area,
                    statement=(
                        f"Provenance dependency context for {impact_item.impact_area} is explained from Phase 3A posture {impact_item.posture}: {impact_item.statement}"
                    ),
                    confidence_posture=impact_item.confidence_posture,
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=impact_item.basis.source_section_keys,
                        topology_node_ids=impact_item.basis.topology_node_ids,
                        topology_edge_ids=impact_item.basis.topology_edge_ids,
                        provenance_gap_refs=impact_item.basis.provenance_gap_refs,
                        derived_from=impact_item.basis.derived_from
                        + ["TwinDependencyImpactReadinessView.provenance_gap_posture"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + impact_item.limitations,
                )
            )
        return items

    def _dependency_reasoning_permission_items(
        self,
        *,
        context: TwinPlanningContext,
        section_records: List[tuple],
        node_by_entity: Dict[tuple, TwinTopologyNode],
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        if context.permission_readiness is not None:
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.permission_readiness_dependency,
                    subject_ref="context_permission_readiness",
                    statement=(
                        f"Context permission readiness describes audience {context.permission_readiness.audience} "
                        f"and purpose {context.permission_readiness.purpose}; permission enforcement remains not enforced."
                    ),
                    confidence_posture="permission_readiness_metadata_only",
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=[section.section_key for section in context.sections],
                        derived_from=["TwinPlanningContext.permission_readiness"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
                )
            )

        for section_key, record in sorted(
            section_records,
            key=lambda item: (item[0], item[1].entity_type, item[1].entity_id or ""),
        ):
            if record.permission_readiness is None:
                continue
            subject_ref = f"{record.entity_type}:{record.entity_id or 'unknown'}"
            node = node_by_entity.get((record.entity_type, record.entity_id))
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.permission_readiness_dependency,
                    subject_ref=subject_ref,
                    statement=(
                        f"{subject_ref} carries permission readiness metadata for audience {record.permission_readiness.audience} "
                        f"and purpose {record.permission_readiness.purpose}; it is not an authorization decision."
                    ),
                    confidence_posture="permission_readiness_metadata_only",
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=[section_key],
                        topology_node_ids=[node.node_id] if node else [],
                        derived_from=["TwinPlanningContextRecord.permission_readiness"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
                )
            )
        return items

    def _dependency_reasoning_continuity_items(
        self, snapshot: TwinTopologySnapshot
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        if snapshot.scenario_branch_references:
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.continuity_snapshot_dependency,
                    subject_ref="scenario_branch_references",
                    statement=(
                        f"Topology snapshot includes {len(snapshot.scenario_branch_references)} scenario branch references as snapshot-bound continuity context."
                    ),
                    confidence_posture="snapshot_bound_context_only",
                    basis=self._dependency_reasoning_basis(
                        derived_from=["TwinTopologySnapshot.scenario_branch_references"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS
                    + [
                        "Scenario branch references are continuity context only; this view does not compare scenarios or implement scenario intelligence.",
                    ],
                )
            )
        if snapshot.revision_lineage_references:
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.continuity_snapshot_dependency,
                    subject_ref="revision_lineage_references",
                    statement=(
                        f"Topology snapshot includes {len(snapshot.revision_lineage_references)} revision lineage references as snapshot-bound continuity context."
                    ),
                    confidence_posture="snapshot_bound_context_only",
                    basis=self._dependency_reasoning_basis(
                        derived_from=["TwinTopologySnapshot.revision_lineage_references"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS
                    + [
                        "Revision lineage references are continuity context only; this view does not replay, compare, or rank revisions.",
                    ],
                )
            )
        return items

    def _dependency_reasoning_missing_items(
        self, impact_view: TwinDependencyImpactReadinessView
    ) -> List[TwinDependencyReasoningItem]:
        items = []
        for missing_item in sorted(impact_view.missing_inputs, key=lambda item: item.missing_input):
            items.append(
                TwinDependencyReasoningItem(
                    reasoning_type=TwinDependencyReasoningType.missing_information_dependency,
                    subject_ref=missing_item.missing_input,
                    statement=(
                        f"Missing information dependency {missing_item.missing_input} is identified because {missing_item.reason}"
                    ),
                    confidence_posture="missing_information_limited",
                    basis=self._dependency_reasoning_basis(
                        source_section_keys=missing_item.basis.source_section_keys,
                        topology_node_ids=missing_item.basis.topology_node_ids,
                        topology_edge_ids=missing_item.basis.topology_edge_ids,
                        provenance_gap_refs=missing_item.basis.provenance_gap_refs,
                        missing_readiness_indicator_refs=missing_item.basis.missing_readiness_indicator_refs,
                        missing_relationship_indicator_refs=missing_item.basis.missing_relationship_indicator_refs,
                        derived_from=missing_item.basis.derived_from
                        + ["TwinDependencyImpactReadinessView.missing_inputs"],
                    ),
                    limitations=DEPENDENCY_REASONING_LIMITATIONS + missing_item.limitations,
                )
            )
        return items

    def build_dependency_reasoning_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
    ) -> Optional[TwinDependencyReasoningView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        node_by_entity = {
            (node.entity_type, node.entity_id): node
            for node in snapshot.nodes
        }
        warning_refs, provenance_gap_refs, _sections_by_entity = self._dependency_impact_record_refs(
            section_records
        )
        missing_readiness_refs = [
            self._missing_readiness_ref(indicator)
            for indicator in snapshot.missing_readiness_indicators
            if not indicator.present
        ]
        missing_relationship_refs = [
            self._missing_relationship_ref(indicator)
            for indicator in snapshot.missing_relationship_indicators
        ]
        lifecycle_signals = self._dependency_impact_lifecycle_signals(snapshot)
        source_basis = self._dependency_reasoning_basis(
            source_section_keys=[section.section_key for section in context.sections],
            topology_node_ids=[node.node_id for node in snapshot.nodes],
            topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
            lifecycle_readiness_signals_used=lifecycle_signals,
            dependency_warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_refs,
            missing_relationship_indicator_refs=missing_relationship_refs,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinDependencyImpactReadinessView",
                "TwinDependencyImpactReadinessView.source_basis",
            ],
        )

        topology_items = self._dependency_reasoning_items_from_edges(snapshot)
        upstream_downstream_items = self._dependency_reasoning_upstream_downstream_items(snapshot)
        source_items = self._dependency_reasoning_source_items(
            section_records=section_records,
            node_by_entity=node_by_entity,
        )
        lifecycle_items = self._dependency_reasoning_lifecycle_items(impact_view)
        rule_items = self._dependency_reasoning_rule_items(
            section_records=section_records,
            snapshot=snapshot,
        )
        provenance_items = self._dependency_reasoning_provenance_items(impact_view)
        permission_items = self._dependency_reasoning_permission_items(
            context=context,
            section_records=section_records,
            node_by_entity=node_by_entity,
        )
        continuity_items = self._dependency_reasoning_continuity_items(snapshot)
        missing_items = self._dependency_reasoning_missing_items(impact_view)

        confidence_posture = self._dependency_impact_confidence_posture(
            warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_refs=missing_readiness_refs,
            missing_relationship_refs=missing_relationship_refs,
        )
        confidence_item = TwinDependencyReasoningItem(
            reasoning_type=TwinDependencyReasoningType.provenance_dependency,
            subject_ref="overall_dependency_reasoning_confidence",
            statement=(
                "Overall dependency reasoning confidence is derived from Phase 3A confidence posture, "
                "planning dependency warnings, provenance gaps, missing lifecycle readiness indicators, and missing relationship indicators."
            ),
            confidence_posture=confidence_posture,
            basis=source_basis,
            limitations=DEPENDENCY_REASONING_LIMITATIONS,
        )

        primary_items = sorted(
            source_items
            + topology_items
            + upstream_downstream_items
            + lifecycle_items
            + rule_items
            + provenance_items
            + permission_items
            + continuity_items
            + missing_items,
            key=self._dependency_reasoning_item_sort_key,
        )
        type_counts = Counter(item.reasoning_type.value for item in primary_items)
        dependency_type_summary = {
            dependency_type.value: type_counts.get(dependency_type.value, 0)
            for dependency_type in TwinDependencyReasoningType
        }

        return self._attach_trust_provenance_readiness_summary(TwinDependencyReasoningView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3B dependency reasoning view built request-time from TwinPlanningContext, "
                "topology snapshot, and Phase 3A dependency impact readiness; not impact propagation, "
                "scenario intelligence, simulation, what-if analysis, export, permission enforcement, or operational behavior."
            ),
            source_basis=source_basis,
            reasoning_scope=TwinDependencyReasoningScope(
                limitations=DEPENDENCY_REASONING_LIMITATIONS,
            ),
            dependency_type_summary=dependency_type_summary,
            dependency_reasoning_items=primary_items,
            upstream_downstream_interpretations=sorted(
                upstream_downstream_items,
                key=self._dependency_reasoning_item_sort_key,
            ),
            lifecycle_dependency_context=sorted(
                lifecycle_items,
                key=self._dependency_reasoning_item_sort_key,
            ),
            provenance_dependency_context=sorted(
                provenance_items,
                key=self._dependency_reasoning_item_sort_key,
            ),
            missing_information_context=sorted(
                missing_items,
                key=self._dependency_reasoning_item_sort_key,
            ),
            confidence_posture=[confidence_item],
            deferred_capabilities=sorted(DEPENDENCY_REASONING_DEFERRED_CAPABILITIES),
            limitations=DEPENDENCY_REASONING_LIMITATIONS,
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, dependency impact readiness, AI grounding, runtime projection, "
                "and current /api/* contracts remain unchanged; this is an additive Phase 3B derived explanation view."
            ),
        ))

    def _planning_intelligence_readiness_basis(
        self,
        *,
        source_section_keys: Optional[List[str]] = None,
        topology_node_ids: Optional[List[str]] = None,
        topology_edge_ids: Optional[List[str]] = None,
        lifecycle_readiness_signals_used: Optional[List[str]] = None,
        dependency_warning_refs: Optional[List[str]] = None,
        provenance_gap_refs: Optional[List[str]] = None,
        missing_readiness_indicator_refs: Optional[List[str]] = None,
        missing_relationship_indicator_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinDependencyImpactStatementBasis:
        return self._dependency_impact_basis(
            source_view_names=[
                "twin_planning_context",
                "topology_snapshot",
                "dependency_impact_readiness",
                "dependency_reasoning",
            ],
            source_section_keys=source_section_keys,
            topology_node_ids=topology_node_ids,
            topology_edge_ids=topology_edge_ids,
            lifecycle_readiness_signals_used=lifecycle_readiness_signals_used,
            dependency_warning_refs=dependency_warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_indicator_refs,
            missing_relationship_indicator_refs=missing_relationship_indicator_refs,
            derived_from=derived_from,
            limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
        )

    def _planning_intelligence_readiness_item(
        self,
        *,
        intelligence_area: TwinPlanningIntelligenceReadinessArea,
        posture: str,
        statement: str,
        available_evidence: Optional[List[str]] = None,
        missing_prerequisites: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinDependencyImpactStatementBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinPlanningIntelligenceReadinessItem:
        return TwinPlanningIntelligenceReadinessItem(
            intelligence_area=intelligence_area,
            posture=posture,
            statement=statement,
            available_evidence=self._sorted_unique(available_evidence or []),
            missing_prerequisites=self._sorted_unique(missing_prerequisites or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            provenance_presence_is_verification=False,
            permission_readiness_is_enforcement=False,
            basis=basis,
            limitations=limitations or PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
        )

    def _planning_intelligence_item_sort_key(
        self, item: TwinPlanningIntelligenceReadinessItem
    ) -> str:
        return item.intelligence_area.value

    def _planning_intelligence_ready_items(
        self,
        *,
        context: TwinPlanningContext,
        snapshot: TwinTopologySnapshot,
        impact_view: TwinDependencyImpactReadinessView,
        reasoning_view: TwinDependencyReasoningView,
        source_basis: TwinDependencyImpactStatementBasis,
    ) -> List[TwinPlanningIntelligenceReadinessItem]:
        permission_record_count = sum(
            1
            for section in context.sections
            for record in section.records
            if record.permission_readiness is not None
        )
        ready_posture = "ready for read-only explanation"
        return sorted(
            [
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.topology_explanation,
                    posture=ready_posture,
                    statement=(
                        "Topology explanation is ready for read-only explanation from existing topology snapshot nodes and edges."
                    ),
                    available_evidence=[
                        f"topology_nodes:{len(snapshot.nodes)}",
                        f"topology_edges:{len(snapshot.edges)}",
                        "TwinTopologySnapshot.nodes",
                        "TwinTopologySnapshot.edges",
                    ],
                    missing_prerequisites=[
                        "field_verified_topology",
                        "canonical_topology_graph",
                    ],
                    unsafe_assumptions=[
                        "Treating planning topology as field-verified topology would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_with_planning_limits",
                    basis=self._planning_intelligence_readiness_basis(
                        topology_node_ids=[node.node_id for node in snapshot.nodes],
                        topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
                        derived_from=[
                            "TwinTopologySnapshot.nodes",
                            "TwinTopologySnapshot.edges",
                        ],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + TOPOLOGY_SNAPSHOT_LIMITATIONS,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.lifecycle_explanation,
                    posture=ready_posture,
                    statement=(
                        "Lifecycle explanation is ready for read-only explanation from topology lifecycle readiness metadata."
                    ),
                    available_evidence=[
                        f"lifecycle_hints:{len(snapshot.lifecycle_readiness_hints)}",
                        f"domains_present:{len(snapshot.lifecycle_readiness_summary.domains_present)}",
                        "TwinTopologySnapshot.lifecycle_readiness_summary",
                        "TwinTopologySnapshot.lifecycle_readiness_hints",
                    ],
                    missing_prerequisites=[
                        "lifecycle_workflow",
                        "lifecycle_event_log",
                        "topology_promotion_workflow",
                    ],
                    unsafe_assumptions=[
                        "Treating lifecycle readiness metadata as lifecycle workflow state would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_with_lifecycle_limits",
                    basis=self._planning_intelligence_readiness_basis(
                        lifecycle_readiness_signals_used=self._dependency_impact_lifecycle_signals(snapshot),
                        derived_from=[
                            "TwinTopologySnapshot.lifecycle_readiness_summary",
                            "TwinTopologySnapshot.lifecycle_readiness_hints",
                        ],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + TOPOLOGY_READINESS_LIMITATIONS,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.relationship_coverage_explanation,
                    posture=ready_posture,
                    statement=(
                        "Relationship coverage explanation is ready for read-only explanation from topology relationship coverage metadata."
                    ),
                    available_evidence=[
                        f"relationship_edges:{snapshot.relationship_coverage_summary.relationship_edge_count}",
                        f"dependency_hook_edges:{snapshot.relationship_coverage_summary.dependency_hook_edge_count}",
                        f"missing_relationship_indicators:{len(snapshot.missing_relationship_indicators)}",
                        "TwinTopologySnapshot.relationship_coverage_summary",
                    ],
                    missing_prerequisites=[
                        "resolved_relationship_inputs_for_missing_indicators",
                        "field_verified_relationships",
                    ],
                    unsafe_assumptions=[
                        "Treating relationship coverage as complete or field-verified would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_with_relationship_limits",
                    basis=self._planning_intelligence_readiness_basis(
                        topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
                        missing_relationship_indicator_refs=[
                            self._missing_relationship_ref(indicator)
                            for indicator in snapshot.missing_relationship_indicators
                        ],
                        derived_from=[
                            "TwinTopologySnapshot.relationship_coverage_summary",
                            "TwinTopologySnapshot.missing_relationship_indicators",
                        ],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + TOPOLOGY_RELATIONSHIP_COVERAGE_LIMITATIONS,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.dependency_impact_readiness,
                    posture=ready_posture,
                    statement=(
                        "Dependency impact readiness is ready for read-only explanation from the Phase 3A dependency impact readiness view."
                    ),
                    available_evidence=[
                        f"impact_posture_items:{len(impact_view.dependency_impact_posture)}",
                        f"missing_inputs:{len(impact_view.missing_inputs)}",
                        f"provenance_gap_posture_items:{len(impact_view.provenance_gap_posture)}",
                        "TwinDependencyImpactReadinessView",
                    ],
                    missing_prerequisites=[
                        "impact_propagation_engine",
                        "recalculation_engine",
                        "invalidation_engine",
                    ],
                    unsafe_assumptions=[
                        "Treating dependency impact readiness as impact propagation would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_with_impact_limits",
                    basis=self._planning_intelligence_readiness_basis(
                        source_section_keys=impact_view.source_basis.source_section_keys,
                        topology_node_ids=impact_view.source_basis.topology_node_ids,
                        topology_edge_ids=impact_view.source_basis.topology_edge_ids,
                        lifecycle_readiness_signals_used=impact_view.source_basis.lifecycle_readiness_signals_used,
                        dependency_warning_refs=impact_view.source_basis.dependency_warning_refs,
                        provenance_gap_refs=impact_view.source_basis.provenance_gap_refs,
                        missing_readiness_indicator_refs=impact_view.source_basis.missing_readiness_indicator_refs,
                        missing_relationship_indicator_refs=impact_view.source_basis.missing_relationship_indicator_refs,
                        derived_from=impact_view.source_basis.derived_from
                        + ["TwinDependencyImpactReadinessView.source_basis"],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + impact_view.limitations,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.dependency_reasoning,
                    posture=ready_posture,
                    statement=(
                        "Dependency reasoning is ready for read-only explanation from the Phase 3B dependency reasoning view."
                    ),
                    available_evidence=[
                        f"reasoning_items:{len(reasoning_view.dependency_reasoning_items)}",
                        f"reasoning_types:{len(reasoning_view.dependency_type_summary)}",
                        "TwinDependencyReasoningView",
                    ],
                    missing_prerequisites=[
                        "scenario_intelligence",
                        "impact_propagation",
                        "recommendation_boundary",
                    ],
                    unsafe_assumptions=[
                        "Treating dependency reasoning as recommendations or scenario intelligence would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_with_reasoning_limits",
                    basis=self._planning_intelligence_readiness_basis(
                        source_section_keys=reasoning_view.source_basis.source_section_keys,
                        topology_node_ids=reasoning_view.source_basis.topology_node_ids,
                        topology_edge_ids=reasoning_view.source_basis.topology_edge_ids,
                        lifecycle_readiness_signals_used=reasoning_view.source_basis.lifecycle_readiness_signals_used,
                        dependency_warning_refs=reasoning_view.source_basis.dependency_warning_refs,
                        provenance_gap_refs=reasoning_view.source_basis.provenance_gap_refs,
                        missing_readiness_indicator_refs=reasoning_view.source_basis.missing_readiness_indicator_refs,
                        missing_relationship_indicator_refs=reasoning_view.source_basis.missing_relationship_indicator_refs,
                        derived_from=reasoning_view.source_basis.derived_from
                        + ["TwinDependencyReasoningView.source_basis"],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + reasoning_view.limitations,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.provenance_gap_reporting,
                    posture=ready_posture,
                    statement=(
                        "Provenance gap reporting is ready for read-only explanation from existing provenance gap metadata."
                    ),
                    available_evidence=[
                        f"provenance_gap_refs:{len(impact_view.source_basis.provenance_gap_refs)}",
                        "TwinPlanningContextRecord.provenance_gaps",
                        "TwinDependencyImpactReadinessView.provenance_gap_posture",
                    ],
                    missing_prerequisites=[
                        "field_level_provenance_completion",
                        "verification_workflow",
                    ],
                    unsafe_assumptions=[
                        "Treating provenance presence as verification would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_not_verification",
                    basis=self._planning_intelligence_readiness_basis(
                        provenance_gap_refs=impact_view.source_basis.provenance_gap_refs,
                        derived_from=[
                            "TwinPlanningContextRecord.provenance_gaps",
                            "TwinDependencyImpactReadinessView.provenance_gap_posture",
                        ],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + PROVENANCE_GAP_LIMITATIONS,
                ),
                self._planning_intelligence_readiness_item(
                    intelligence_area=TwinPlanningIntelligenceReadinessArea.permission_readiness_metadata,
                    posture=ready_posture,
                    statement=(
                        "Permission readiness metadata is ready for read-only explanation, but permission enforcement remains not implemented."
                    ),
                    available_evidence=[
                        f"records_with_permission_readiness:{permission_record_count}",
                        "TwinPlanningContext.permission_readiness",
                        "TwinPlanningContextRecord.permission_readiness",
                    ],
                    missing_prerequisites=[
                        "active_permission_grants",
                        "active_consent_artifacts",
                        "permission_enforcement",
                    ],
                    unsafe_assumptions=[
                        "Treating permission readiness metadata as permission enforcement would be unsafe.",
                    ],
                    confidence_posture="ready_for_read_only_explanation_metadata_only",
                    basis=self._planning_intelligence_readiness_basis(
                        source_section_keys=[section.section_key for section in context.sections],
                        derived_from=[
                            "TwinPlanningContext.permission_readiness",
                            "TwinPlanningContextRecord.permission_readiness",
                        ],
                    ),
                    limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS
                    + PERMISSION_READINESS_LIMITATIONS,
                ),
            ],
            key=self._planning_intelligence_item_sort_key,
        )

    def _planning_intelligence_blocked_item(
        self,
        *,
        intelligence_area: TwinPlanningIntelligenceReadinessArea,
        statement: str,
        missing_prerequisites: List[str],
        unsafe_assumptions: List[str],
        source_basis: TwinDependencyImpactStatementBasis,
    ) -> TwinPlanningIntelligenceReadinessItem:
        return self._planning_intelligence_readiness_item(
            intelligence_area=intelligence_area,
            posture="blocked/deferred",
            statement=statement,
            available_evidence=[
                "Phase 3C approved boundary",
                "current deferred capability list",
            ],
            missing_prerequisites=missing_prerequisites,
            unsafe_assumptions=unsafe_assumptions,
            confidence_posture="blocked_deferred_not_implemented",
            basis=self._planning_intelligence_readiness_basis(
                source_section_keys=source_basis.source_section_keys,
                topology_node_ids=source_basis.topology_node_ids,
                topology_edge_ids=source_basis.topology_edge_ids,
                lifecycle_readiness_signals_used=source_basis.lifecycle_readiness_signals_used,
                dependency_warning_refs=source_basis.dependency_warning_refs,
                provenance_gap_refs=source_basis.provenance_gap_refs,
                missing_readiness_indicator_refs=source_basis.missing_readiness_indicator_refs,
                missing_relationship_indicator_refs=source_basis.missing_relationship_indicator_refs,
                derived_from=source_basis.derived_from
                + ["Phase3C.planning_intelligence_readiness_deferred_boundaries"],
            ),
            limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
        )

    def _planning_intelligence_blocked_items(
        self, source_basis: TwinDependencyImpactStatementBasis
    ) -> List[TwinPlanningIntelligenceReadinessItem]:
        blocked_specs = [
            (
                TwinPlanningIntelligenceReadinessArea.scenario_intelligence,
                "Scenario intelligence is blocked/deferred; scenario references are continuity context only.",
                ["approved_scenario_intelligence_boundary", "scenario_comparison_engine"],
                ["Treating saved scenario references as scenario intelligence would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.impact_propagation,
                "Impact propagation is blocked/deferred; no propagation engine exists.",
                ["impact_propagation_engine", "affected_output_registry"],
                ["Treating dependency explanation as propagated impact state would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.stale_state_persistence,
                "Stale-state persistence is blocked/deferred; no stale-state records are created.",
                ["stale_state_model", "persistence_contract"],
                ["Treating request-time limitations as persisted stale state would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.recalculation,
                "Recalculation is blocked/deferred; no recalculation engine runs.",
                ["recalculation_engine", "approved_calculation_trigger_contract"],
                ["Treating readiness inventory as recalculation would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.invalidation,
                "Invalidation is blocked/deferred; no invalidation engine runs.",
                ["invalidation_engine", "approved_invalidation_state_contract"],
                ["Treating missing prerequisites as invalidated outputs would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.simulation,
                "Simulation is blocked/deferred; no scenario simulation or infrastructure simulation runs.",
                ["approved_simulation_engine", "source_backed_simulation_inputs"],
                ["Treating readiness evidence as simulated outcome data would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.what_if_analysis,
                "What-if analysis is blocked/deferred; no modeled change analysis runs.",
                ["approved_what_if_engine", "change_model_contract"],
                ["Treating blocked/deferred readiness as what-if analysis would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.optimization,
                "Optimization is blocked/deferred; no optimization logic runs.",
                ["approved_optimization_boundary"],
                ["Treating readiness posture as optimized choice would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.ranking,
                "Ranking is blocked/deferred; no ranking logic runs.",
                ["approved_ranking_boundary"],
                ["Treating deterministic ordering as ranking would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.economic_reasoning,
                "Economic reasoning is blocked/deferred; no pricing, savings, payback, incentive, or financial reasoning runs.",
                ["source_backed_economic_inputs", "approved_economic_reasoning_boundary"],
                ["Treating readiness posture as financial guidance would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.utility_readiness_logic,
                "Utility readiness logic is blocked/deferred; no utility approval, interconnection, program eligibility, or grid-edge readiness logic runs.",
                ["approved_utility_readiness_boundary", "source_backed_utility_inputs"],
                ["Treating planning context as utility readiness would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.survivability_recharge_modeling,
                "Survivability/recharge modeling is blocked/deferred; no endurance or recharge model runs.",
                ["approved_survivability_model", "approved_recharge_model"],
                ["Treating planning evidence as survivability or recharge results would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.compatibility_engine,
                "Compatibility engine behavior is blocked/deferred; no product or system compatibility engine runs.",
                ["approved_compatibility_engine", "verified_product_compatibility_sources"],
                ["Treating dependency relationships as compatibility approval would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.recommendation_or_proposal_generation,
                "Recommendations and proposal generation are blocked/deferred; this view does not choose or propose actions.",
                ["approved_recommendation_boundary", "approved_proposal_generation_boundary"],
                ["Treating readiness inventory as a recommendation or proposal would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.exports,
                "Exports are blocked/deferred; no scoped export package is generated.",
                ["approved_export_contract", "permissioned_view_enforcement"],
                ["Treating this API view as an export would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.auth_rbac_abac,
                "Auth/RBAC/ABAC is blocked/deferred; no authorization or access-control enforcement exists.",
                ["approved_auth_architecture", "approved_rbac_abac_model"],
                ["Treating metadata scopes as access control would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.permission_enforcement,
                "Permission enforcement is blocked/deferred; permission readiness remains metadata only.",
                ["active_permission_grants", "active_consent_artifacts", "permission_enforcement_layer"],
                ["Treating permission readiness as permission enforcement would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.marketplace,
                "Marketplace behavior is blocked/deferred; no registry or marketplace surface exists.",
                ["approved_marketplace_boundary", "ownership_transfer_boundary"],
                ["Treating planning intelligence readiness as marketplace readiness would be unsafe."],
            ),
            (
                TwinPlanningIntelligenceReadinessArea.operational_behavior,
                "Operational behavior is blocked/deferred; no device, dispatch, DERMS, telemetry, or control behavior exists.",
                ["operational_control_boundary", "telemetry_governance", "device_identity"],
                ["Treating planning intelligence readiness as operational readiness would be unsafe."],
            ),
        ]
        return sorted(
            [
                self._planning_intelligence_blocked_item(
                    intelligence_area=area,
                    statement=statement,
                    missing_prerequisites=missing_prerequisites,
                    unsafe_assumptions=unsafe_assumptions,
                    source_basis=source_basis,
                )
                for area, statement, missing_prerequisites, unsafe_assumptions in blocked_specs
            ],
            key=self._planning_intelligence_item_sort_key,
        )

    def build_planning_intelligence_readiness_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
    ) -> Optional[TwinPlanningIntelligenceReadinessView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        warning_refs, provenance_gap_refs, _sections_by_entity = self._dependency_impact_record_refs(
            section_records
        )
        missing_readiness_refs = [
            self._missing_readiness_ref(indicator)
            for indicator in snapshot.missing_readiness_indicators
            if not indicator.present
        ]
        missing_relationship_refs = [
            self._missing_relationship_ref(indicator)
            for indicator in snapshot.missing_relationship_indicators
        ]
        lifecycle_signals = self._dependency_impact_lifecycle_signals(snapshot)
        source_basis = self._planning_intelligence_readiness_basis(
            source_section_keys=[section.section_key for section in context.sections],
            topology_node_ids=[node.node_id for node in snapshot.nodes],
            topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
            lifecycle_readiness_signals_used=lifecycle_signals,
            dependency_warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_refs,
            missing_relationship_indicator_refs=missing_relationship_refs,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinDependencyImpactReadinessView",
                "TwinDependencyReasoningView",
            ],
        )

        ready_items = self._planning_intelligence_ready_items(
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            source_basis=source_basis,
        )
        blocked_items = self._planning_intelligence_blocked_items(source_basis)
        all_items = ready_items + blocked_items
        missing_prerequisites = self._sorted_unique(
            prerequisite
            for item in all_items
            for prerequisite in item.missing_prerequisites
        )
        available_evidence = self._sorted_unique(
            evidence
            for item in ready_items
            for evidence in item.available_evidence
        )
        unsafe_assumptions = self._sorted_unique(
            assumption
            for item in all_items
            for assumption in item.unsafe_assumptions
        )
        confidence_item = self._planning_intelligence_readiness_item(
            intelligence_area=TwinPlanningIntelligenceReadinessArea.provenance_gap_reporting,
            posture="ready for read-only explanation",
            statement=(
                "Overall planning intelligence readiness confidence is limited to read-only explanation because blocked/deferred areas are not implemented."
            ),
            available_evidence=[
                f"ready_areas:{len(ready_items)}",
                f"blocked_deferred_areas:{len(blocked_items)}",
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinDependencyImpactReadinessView",
                "TwinDependencyReasoningView",
            ],
            missing_prerequisites=missing_prerequisites,
            unsafe_assumptions=[
                "Treating ready for read-only explanation as executable intelligence would be unsafe.",
            ],
            confidence_posture="read_only_explanation_ready_blocked_deferred_execution",
            basis=source_basis,
            limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
        )

        return self._attach_trust_provenance_readiness_summary(TwinPlanningIntelligenceReadinessView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3C planning intelligence readiness inventory built request-time from "
                "TwinPlanningContext, topology snapshot, dependency impact readiness, and dependency reasoning; "
                "not a reasoning engine, recommendation layer, scenario simulation, export, permission enforcement, "
                "graph engine, canonical Twin runtime model, or operational behavior."
            ),
            source_basis=source_basis,
            readiness_scope=TwinPlanningIntelligenceReadinessScope(
                limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
            ),
            ready_areas=ready_items,
            blocked_deferred_areas=blocked_items,
            provenance_permission_basis=[
                item
                for item in ready_items
                if item.intelligence_area
                in {
                    TwinPlanningIntelligenceReadinessArea.provenance_gap_reporting,
                    TwinPlanningIntelligenceReadinessArea.permission_readiness_metadata,
                }
            ],
            missing_prerequisites=missing_prerequisites,
            available_evidence=available_evidence,
            unsafe_assumptions=unsafe_assumptions,
            deferred_reasoning_boundaries=sorted(
                PLANNING_INTELLIGENCE_READINESS_DEFERRED_BOUNDARIES
            ),
            confidence_posture=[confidence_item],
            limitations=PLANNING_INTELLIGENCE_READINESS_LIMITATIONS,
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, dependency impact readiness, dependency reasoning, "
                "AI grounding, runtime projection, and current /api/* contracts remain unchanged; this is an additive Phase 3C readiness inventory."
            ),
        ))

    def _advisory_context_basis(
        self,
        *,
        source_section_keys: Optional[List[str]] = None,
        topology_node_ids: Optional[List[str]] = None,
        topology_edge_ids: Optional[List[str]] = None,
        lifecycle_readiness_signals_used: Optional[List[str]] = None,
        dependency_warning_refs: Optional[List[str]] = None,
        provenance_gap_refs: Optional[List[str]] = None,
        missing_readiness_indicator_refs: Optional[List[str]] = None,
        missing_relationship_indicator_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinDependencyImpactStatementBasis:
        return self._dependency_impact_basis(
            source_view_names=[
                "twin_planning_context",
                "topology_snapshot",
                "dependency_impact_readiness",
                "dependency_reasoning",
                "planning_intelligence_readiness",
            ],
            source_section_keys=source_section_keys,
            topology_node_ids=topology_node_ids,
            topology_edge_ids=topology_edge_ids,
            lifecycle_readiness_signals_used=lifecycle_readiness_signals_used,
            dependency_warning_refs=dependency_warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_indicator_refs,
            missing_relationship_indicator_refs=missing_relationship_indicator_refs,
            derived_from=derived_from,
            limitations=ADVISORY_CONTEXT_ASSEMBLY_LIMITATIONS,
        )

    def _advisory_context_item(
        self,
        *,
        context_area: TwinAdvisoryContextAssemblyArea,
        posture: str,
        statement: str,
        assembled_inputs: Optional[List[str]] = None,
        missing_inputs: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinDependencyImpactStatementBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinAdvisoryContextAssemblyItem:
        return TwinAdvisoryContextAssemblyItem(
            context_area=context_area,
            posture=posture,
            statement=statement,
            assembled_inputs=self._sorted_unique(assembled_inputs or []),
            missing_inputs=self._sorted_unique(missing_inputs or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or ADVISORY_CONTEXT_ASSEMBLY_LIMITATIONS,
        )

    def _advisory_context_item_sort_key(self, item: TwinAdvisoryContextAssemblyItem) -> str:
        return item.context_area.value

    def _advisory_record_ref(self, record: TwinPlanningContextRecord) -> str:
        return f"{record.entity_type}:{record.entity_id or 'unknown'}"

    def _advisory_homeowner_goal_items(
        self,
        section_records: List[tuple],
        node_by_entity: Dict[tuple, TwinTopologyNode],
    ) -> List[TwinAdvisoryContextAssemblyItem]:
        goal_inputs = []
        source_sections = []
        node_ids = []
        provenance_refs = []
        for section_key, record in sorted(
            section_records,
            key=lambda item: (item[0], item[1].entity_type, item[1].entity_id or ""),
        ):
            if record.entity_type != "energy_system_design":
                continue
            design_goal = record.record.get("design_goal")
            if not design_goal:
                continue
            goal_inputs.append(f"{self._advisory_record_ref(record)}:design_goal:{design_goal}")
            source_sections.append(section_key)
            node = node_by_entity.get((record.entity_type, record.entity_id))
            if node is not None:
                node_ids.append(node.node_id)
            provenance_refs.extend(self._provenance_gap_ref(gap) for gap in record.provenance_gaps)

        if goal_inputs:
            return [
                self._advisory_context_item(
                    context_area=TwinAdvisoryContextAssemblyArea.homeowner_goals,
                    posture="assembled_as_advisory_input_context_only",
                    statement=(
                        "Homeowner goal context is assembled only from existing recorded design goal fields."
                    ),
                    assembled_inputs=goal_inputs,
                    missing_inputs=["field_verified_homeowner_goal_confirmation"],
                    unsafe_assumptions=[
                        "Treating recorded planning goals as final homeowner guidance would be unsafe.",
                    ],
                    confidence_posture="recorded_goal_context_present_planning_only",
                    basis=self._advisory_context_basis(
                        source_section_keys=source_sections,
                        topology_node_ids=node_ids,
                        provenance_gap_refs=provenance_refs,
                        derived_from=["TwinPlanningContextRecord.record.design_goal"],
                    ),
                )
            ]
        return [
            self._advisory_context_item(
                context_area=TwinAdvisoryContextAssemblyArea.homeowner_goals,
                posture="missing_input_context_only",
                statement=(
                    "No homeowner goal context is assembled because no existing recorded design goal field was found."
                ),
                missing_inputs=["recorded_design_goal"],
                unsafe_assumptions=[
                    "Inventing homeowner goals would be unsafe.",
                ],
                confidence_posture="missing_goal_context",
                basis=self._advisory_context_basis(
                    derived_from=["TwinPlanningContext.sections"],
                ),
            )
        ]

    def _advisory_equipment_site_item(
        self,
        *,
        section_records: List[tuple],
        node_by_entity: Dict[tuple, TwinTopologyNode],
    ) -> TwinAdvisoryContextAssemblyItem:
        allowed_sections = {
            "premise",
            "structures",
            "electrical_infrastructure",
            "loads",
            "equipment_locations",
            "equipment_products",
            "design_equipment",
            "pathways",
        }
        assembled_inputs = []
        source_sections = []
        node_ids = []
        provenance_refs = []
        for section_key, record in sorted(
            section_records,
            key=lambda item: (item[0], item[1].entity_type, item[1].entity_id or ""),
        ):
            if section_key not in allowed_sections:
                continue
            assembled_inputs.append(f"{section_key}:{self._advisory_record_ref(record)}")
            source_sections.append(section_key)
            node = node_by_entity.get((record.entity_type, record.entity_id))
            if node is not None:
                node_ids.append(node.node_id)
            provenance_refs.extend(self._provenance_gap_ref(gap) for gap in record.provenance_gaps)

        return self._advisory_context_item(
            context_area=TwinAdvisoryContextAssemblyArea.equipment_site_facts,
            posture="assembled_as_advisory_input_context_only",
            statement=(
                "Equipment and site fact context is assembled from existing premise, structure, electrical, load, equipment, location, and pathway records."
            ),
            assembled_inputs=assembled_inputs,
            missing_inputs=[
                "field_verified_site_survey",
                "complete_equipment_spec_verification",
            ],
            unsafe_assumptions=[
                "Treating planning equipment/site facts as field-verified or compatibility-approved would be unsafe.",
            ],
            confidence_posture="equipment_site_context_present_planning_only",
            basis=self._advisory_context_basis(
                source_section_keys=source_sections,
                topology_node_ids=node_ids,
                provenance_gap_refs=provenance_refs,
                derived_from=["TwinPlanningContext.sections"],
            ),
        )

    def build_advisory_context_assembly_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
    ) -> Optional[TwinAdvisoryContextAssemblyView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
        )
        if readiness_view is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        node_by_entity = {
            (node.entity_type, node.entity_id): node
            for node in snapshot.nodes
        }
        warning_refs, provenance_gap_refs, _sections_by_entity = self._dependency_impact_record_refs(
            section_records
        )
        missing_readiness_refs = [
            self._missing_readiness_ref(indicator)
            for indicator in snapshot.missing_readiness_indicators
            if not indicator.present
        ]
        missing_relationship_refs = [
            self._missing_relationship_ref(indicator)
            for indicator in snapshot.missing_relationship_indicators
        ]
        lifecycle_signals = self._dependency_impact_lifecycle_signals(snapshot)
        source_basis = self._advisory_context_basis(
            source_section_keys=[section.section_key for section in context.sections],
            topology_node_ids=[node.node_id for node in snapshot.nodes],
            topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
            lifecycle_readiness_signals_used=lifecycle_signals,
            dependency_warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_refs,
            missing_relationship_indicator_refs=missing_relationship_refs,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinDependencyImpactReadinessView",
                "TwinDependencyReasoningView",
                "TwinPlanningIntelligenceReadinessView",
            ],
        )

        homeowner_goal_items = self._advisory_homeowner_goal_items(
            section_records,
            node_by_entity,
        )
        topology_item = self._advisory_context_item(
            context_area=TwinAdvisoryContextAssemblyArea.topology_facts,
            posture="assembled_as_advisory_input_context_only",
            statement=(
                "Topology fact context is assembled from existing topology snapshot nodes, edges, lifecycle hints, and relationship coverage metadata."
            ),
            assembled_inputs=[
                f"topology_nodes:{len(snapshot.nodes)}",
                f"topology_edges:{len(snapshot.edges)}",
                f"lifecycle_hints:{len(snapshot.lifecycle_readiness_hints)}",
                f"missing_relationship_indicators:{len(snapshot.missing_relationship_indicators)}",
            ],
            missing_inputs=[
                "field_verified_topology",
                "canonical_topology_graph",
            ],
            unsafe_assumptions=[
                "Treating planning topology as field-verified topology would be unsafe.",
            ],
            confidence_posture="topology_context_present_planning_only",
            basis=self._advisory_context_basis(
                topology_node_ids=[node.node_id for node in snapshot.nodes],
                topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
                lifecycle_readiness_signals_used=lifecycle_signals,
                missing_relationship_indicator_refs=missing_relationship_refs,
                derived_from=[
                    "TwinTopologySnapshot.nodes",
                    "TwinTopologySnapshot.edges",
                    "TwinTopologySnapshot.lifecycle_readiness_hints",
                    "TwinTopologySnapshot.relationship_coverage_summary",
                ],
            ),
            limitations=ADVISORY_CONTEXT_ASSEMBLY_LIMITATIONS
            + TOPOLOGY_SNAPSHOT_LIMITATIONS,
        )
        equipment_site_item = self._advisory_equipment_site_item(
            section_records=section_records,
            node_by_entity=node_by_entity,
        )
        provenance_item = self._advisory_context_item(
            context_area=TwinAdvisoryContextAssemblyArea.provenance_basis,
            posture="assembled_as_advisory_input_context_only",
            statement=(
                "Provenance basis context is assembled from existing provenance gap and source-document metadata; provenance presence is not verification."
            ),
            assembled_inputs=[
                f"provenance_gap_refs:{len(set(provenance_gap_refs))}",
                f"source_sections:{len(context.sections)}",
                f"phase_3c_ready_areas:{len(readiness_view.ready_areas)}",
            ],
            missing_inputs=[
                "field_level_provenance_completion",
                "verification_workflow",
            ],
            unsafe_assumptions=[
                "Treating provenance presence as verification would be unsafe.",
            ],
            confidence_posture="provenance_context_present_not_verification",
            basis=self._advisory_context_basis(
                source_section_keys=[section.section_key for section in context.sections],
                provenance_gap_refs=provenance_gap_refs,
                derived_from=[
                    "TwinPlanningContextRecord.provenance_gaps",
                    "TwinPlanningContextRecord.source_document_ids",
                    "TwinPlanningIntelligenceReadinessView.provenance_permission_basis",
                ],
            ),
            limitations=ADVISORY_CONTEXT_ASSEMBLY_LIMITATIONS
            + PROVENANCE_GAP_LIMITATIONS,
        )
        permission_record_count = sum(
            1
            for _section_key, record in section_records
            if record.permission_readiness is not None
        )
        permission_item = self._advisory_context_item(
            context_area=TwinAdvisoryContextAssemblyArea.permission_readiness_metadata,
            posture="assembled_as_advisory_input_context_only",
            statement=(
                "Permission-readiness metadata is assembled as advisory input context only; permission enforcement remains not implemented."
            ),
            assembled_inputs=[
                f"records_with_permission_readiness:{permission_record_count}",
                "TwinPlanningContext.permission_readiness",
            ],
            missing_inputs=[
                "active_permission_grants",
                "active_consent_artifacts",
                "permission_enforcement_layer",
            ],
            unsafe_assumptions=[
                "Treating permission readiness metadata as permission enforcement would be unsafe.",
            ],
            confidence_posture="permission_context_present_metadata_only",
            basis=self._advisory_context_basis(
                source_section_keys=[section.section_key for section in context.sections],
                derived_from=[
                    "TwinPlanningContext.permission_readiness",
                    "TwinPlanningContextRecord.permission_readiness",
                    "TwinPlanningIntelligenceReadinessView.provenance_permission_basis",
                ],
            ),
            limitations=ADVISORY_CONTEXT_ASSEMBLY_LIMITATIONS
            + PERMISSION_READINESS_LIMITATIONS,
        )
        missing_inputs = self._sorted_unique(
            list(readiness_view.missing_prerequisites)
            + [item.missing_input for item in impact_view.missing_inputs]
        )
        missing_item = self._advisory_context_item(
            context_area=TwinAdvisoryContextAssemblyArea.missing_data,
            posture="assembled_as_advisory_input_context_only",
            statement=(
                "Missing data context is assembled from Phase 3A missing inputs and Phase 3C missing prerequisites."
            ),
            assembled_inputs=[
                f"phase_3a_missing_inputs:{len(impact_view.missing_inputs)}",
                f"phase_3c_missing_prerequisites:{len(readiness_view.missing_prerequisites)}",
            ],
            missing_inputs=missing_inputs,
            unsafe_assumptions=[
                "Filling missing data with invented advisory assumptions would be unsafe.",
            ],
            confidence_posture="missing_data_context_present",
            basis=self._advisory_context_basis(
                source_section_keys=source_basis.source_section_keys,
                topology_node_ids=source_basis.topology_node_ids,
                topology_edge_ids=source_basis.topology_edge_ids,
                provenance_gap_refs=source_basis.provenance_gap_refs,
                missing_readiness_indicator_refs=source_basis.missing_readiness_indicator_refs,
                missing_relationship_indicator_refs=source_basis.missing_relationship_indicator_refs,
                derived_from=[
                    "TwinDependencyImpactReadinessView.missing_inputs",
                    "TwinPlanningIntelligenceReadinessView.missing_prerequisites",
                ],
            ),
        )
        unsafe_inputs = self._sorted_unique(
            readiness_view.unsafe_assumptions
            + [
                "Treating assembled advisory input context as advice would be unsafe.",
                "Treating assembled advisory input context as homeowner guidance would be unsafe.",
            ]
        )
        unsafe_item = self._advisory_context_item(
            context_area=TwinAdvisoryContextAssemblyArea.unsafe_assumptions,
            posture="assembled_as_advisory_input_context_only",
            statement=(
                "Unsafe assumption context is assembled so future advisory outputs do not overstate available authority."
            ),
            assembled_inputs=unsafe_inputs,
            unsafe_assumptions=unsafe_inputs,
            confidence_posture="unsafe_assumption_context_present",
            basis=self._advisory_context_basis(
                source_section_keys=source_basis.source_section_keys,
                derived_from=[
                    "TwinPlanningIntelligenceReadinessView.unsafe_assumptions",
                    "Phase3D.advisory_context_assembly_limitations",
                ],
            ),
        )
        readiness_item = self._advisory_context_item(
            context_area=TwinAdvisoryContextAssemblyArea.advisory_input_readiness,
            posture="assembled_as_advisory_input_context_only",
            statement=(
                "Advisory input readiness is assembled for future read-only advisory grounding only; this view does not generate advice."
            ),
            assembled_inputs=[
                f"homeowner_goal_items:{len(homeowner_goal_items)}",
                "topology_facts",
                "equipment_site_facts",
                "provenance_basis",
                "permission_readiness_metadata",
                f"deferred_boundaries:{len(ADVISORY_CONTEXT_DEFERRED_BOUNDARIES)}",
            ],
            missing_inputs=missing_inputs,
            unsafe_assumptions=[
                "Treating advisory input readiness as advice generation readiness would be unsafe.",
            ],
            confidence_posture="advisory_input_context_assembled_no_advice_generated",
            basis=source_basis,
        )

        return self._attach_trust_provenance_readiness_summary(TwinAdvisoryContextAssemblyView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3D advisory context assembly view built request-time from TwinPlanningContext, "
                "topology snapshot, dependency impact readiness, dependency reasoning, and planning intelligence readiness; "
                "not advice generation, recommendations, ranking, optimization, scenario simulation, what-if analysis, "
                "proposal generation, permission enforcement, export, graph engine, persistence, or operational behavior."
            ),
            source_basis=source_basis,
            assembly_scope=TwinAdvisoryContextAssemblyScope(
                limitations=ADVISORY_CONTEXT_ASSEMBLY_LIMITATIONS,
            ),
            homeowner_goals=homeowner_goal_items,
            topology_facts=[topology_item],
            equipment_site_facts=[equipment_site_item],
            provenance_basis=[provenance_item],
            permission_readiness_metadata=[permission_item],
            missing_data=[missing_item],
            unsafe_assumptions=[unsafe_item],
            advisory_input_readiness=[readiness_item],
            deferred_advisory_output_boundaries=sorted(ADVISORY_CONTEXT_DEFERRED_BOUNDARIES),
            limitations=ADVISORY_CONTEXT_ASSEMBLY_LIMITATIONS,
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A, Phase 3B, Phase 3C, AI grounding, "
                "runtime projection, and current /api/* contracts remain unchanged; this is an additive Phase 3D advisory input assembly view."
            ),
        ))

    def _constraint_risk_basis(
        self,
        *,
        source_section_keys: Optional[List[str]] = None,
        topology_node_ids: Optional[List[str]] = None,
        topology_edge_ids: Optional[List[str]] = None,
        lifecycle_readiness_signals_used: Optional[List[str]] = None,
        dependency_warning_refs: Optional[List[str]] = None,
        provenance_gap_refs: Optional[List[str]] = None,
        missing_readiness_indicator_refs: Optional[List[str]] = None,
        missing_relationship_indicator_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinDependencyImpactStatementBasis:
        return self._dependency_impact_basis(
            source_view_names=[
                "twin_planning_context",
                "topology_snapshot",
                "dependency_impact_readiness",
                "dependency_reasoning",
                "planning_intelligence_readiness",
                "advisory_context_assembly",
            ],
            source_section_keys=source_section_keys,
            topology_node_ids=topology_node_ids,
            topology_edge_ids=topology_edge_ids,
            lifecycle_readiness_signals_used=lifecycle_readiness_signals_used,
            dependency_warning_refs=dependency_warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_indicator_refs,
            missing_relationship_indicator_refs=missing_relationship_indicator_refs,
            derived_from=derived_from,
            limitations=CONSTRAINT_RISK_REASONING_LIMITATIONS,
        )

    def _constraint_risk_item(
        self,
        *,
        risk_area: TwinConstraintRiskReasoningArea,
        non_decisional_severity_label: str,
        statement: str,
        observed_constraint_refs: Optional[List[str]] = None,
        missing_inputs: Optional[List[str]] = None,
        low_trust_inputs: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        professional_review_boundaries: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinDependencyImpactStatementBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinConstraintRiskReasoningItem:
        return TwinConstraintRiskReasoningItem(
            risk_area=risk_area,
            non_decisional_severity_label=non_decisional_severity_label,
            statement=statement,
            observed_constraint_refs=self._sorted_unique(observed_constraint_refs or []),
            missing_inputs=self._sorted_unique(missing_inputs or []),
            low_trust_inputs=self._sorted_unique(low_trust_inputs or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            professional_review_boundaries=self._sorted_unique(professional_review_boundaries or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or CONSTRAINT_RISK_REASONING_LIMITATIONS,
        )

    def _constraint_risk_item_sort_key(self, item: TwinConstraintRiskReasoningItem) -> str:
        return item.risk_area.value

    def build_constraint_risk_reasoning_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
        advisory_view: Optional[TwinAdvisoryContextAssemblyView] = None,
    ) -> Optional[TwinConstraintRiskReasoningView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
        )
        if readiness_view is None:
            return None
        advisory_view = advisory_view or self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        node_by_entity = {
            (node.entity_type, node.entity_id): node
            for node in snapshot.nodes
        }
        warning_refs, provenance_gap_refs, _sections_by_entity = self._dependency_impact_record_refs(
            section_records
        )
        missing_readiness_refs = [
            self._missing_readiness_ref(indicator)
            for indicator in snapshot.missing_readiness_indicators
            if not indicator.present
        ]
        missing_relationship_refs = [
            self._missing_relationship_ref(indicator)
            for indicator in snapshot.missing_relationship_indicators
        ]
        lifecycle_signals = self._dependency_impact_lifecycle_signals(snapshot)
        source_basis = self._constraint_risk_basis(
            source_section_keys=[section.section_key for section in context.sections],
            topology_node_ids=[node.node_id for node in snapshot.nodes],
            topology_edge_ids=[edge.edge_id for edge in snapshot.edges],
            lifecycle_readiness_signals_used=lifecycle_signals,
            dependency_warning_refs=warning_refs,
            provenance_gap_refs=provenance_gap_refs,
            missing_readiness_indicator_refs=missing_readiness_refs,
            missing_relationship_indicator_refs=missing_relationship_refs,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinDependencyImpactReadinessView",
                "TwinDependencyReasoningView",
                "TwinPlanningIntelligenceReadinessView",
                "TwinAdvisoryContextAssemblyView",
            ],
        )

        equipment_records = [
            (section_key, record)
            for section_key, record in section_records
            if record.entity_type in {"equipment_product", "design_equipment"}
        ]
        missing_equipment_refs = [
            f"{self._advisory_record_ref(record)}:specs"
            for _section_key, record in equipment_records
            if record.entity_type == "equipment_product"
            and (not record.record.get("specs") or record.provenance_gaps or record.missing_fields)
        ]
        equipment_node_ids = [
            node_by_entity[(record.entity_type, record.entity_id)].node_id
            for _section_key, record in equipment_records
            if (record.entity_type, record.entity_id) in node_by_entity
        ]
        equipment_provenance_refs = [
            self._provenance_gap_ref(gap)
            for _section_key, record in equipment_records
            for gap in record.provenance_gaps
        ]
        missing_equipment_item = self._constraint_risk_item(
            risk_area=TwinConstraintRiskReasoningArea.missing_equipment_specs,
            non_decisional_severity_label="missing_or_low_trust_input",
            statement=(
                "Missing equipment spec context is derived from existing equipment records, missing fields, and provenance gaps; it is not compatibility reasoning."
            ),
            observed_constraint_refs=missing_equipment_refs or ["equipment_spec_context_present_without_complete_verification"],
            missing_inputs=missing_equipment_refs + ["verified_equipment_spec_sources"],
            low_trust_inputs=equipment_provenance_refs,
            unsafe_assumptions=[
                "Treating recorded equipment context as verified product compatibility would be unsafe.",
            ],
            professional_review_boundaries=[
                "Product compatibility and final equipment selection require future approved review boundaries.",
            ],
            confidence_posture="equipment_spec_context_limited",
            basis=self._constraint_risk_basis(
                source_section_keys=[section_key for section_key, _record in equipment_records],
                topology_node_ids=equipment_node_ids,
                provenance_gap_refs=equipment_provenance_refs,
                derived_from=[
                    "TwinPlanningContextRecord.record.specs",
                    "TwinPlanningContextRecord.missing_fields",
                    "TwinPlanningContextRecord.provenance_gaps",
                ],
            ),
        )

        incomplete_topology_item = self._constraint_risk_item(
            risk_area=TwinConstraintRiskReasoningArea.incomplete_topology,
            non_decisional_severity_label="topology_boundary_limited",
            statement=(
                "Incomplete topology context is derived from missing readiness and missing relationship indicators."
            ),
            observed_constraint_refs=missing_readiness_refs + missing_relationship_refs,
            missing_inputs=missing_readiness_refs + missing_relationship_refs + ["field_verified_topology"],
            low_trust_inputs=provenance_gap_refs,
            unsafe_assumptions=[
                "Treating planning topology as complete or field-verified would be unsafe.",
            ],
            professional_review_boundaries=[
                "Field verification remains required before topology can support professional design decisions.",
            ],
            confidence_posture="topology_incomplete_planning_context",
            basis=self._constraint_risk_basis(
                topology_node_ids=source_basis.topology_node_ids,
                topology_edge_ids=source_basis.topology_edge_ids,
                missing_readiness_indicator_refs=missing_readiness_refs,
                missing_relationship_indicator_refs=missing_relationship_refs,
                derived_from=[
                    "TwinTopologySnapshot.missing_readiness_indicators",
                    "TwinTopologySnapshot.missing_relationship_indicators",
                ],
            ),
        )

        load_records = [
            (section_key, record)
            for section_key, record in section_records
            if record.entity_type == "load"
        ]
        unsupported_load_refs = [
            self._advisory_record_ref(record)
            for _section_key, record in load_records
            if record.provenance_gaps or record.missing_fields or not record.record.get("running_watts")
        ]
        load_provenance_refs = [
            self._provenance_gap_ref(gap)
            for _section_key, record in load_records
            for gap in record.provenance_gaps
        ]
        unsupported_load_item = self._constraint_risk_item(
            risk_area=TwinConstraintRiskReasoningArea.unsupported_load_data,
            non_decisional_severity_label="source_support_limited",
            statement=(
                "Unsupported load data context is derived from load records with provenance gaps, missing fields, or missing wattage inputs."
            ),
            observed_constraint_refs=unsupported_load_refs or ["load_context_present_without_full_source_verification"],
            missing_inputs=["fully_source_backed_load_inputs"],
            low_trust_inputs=load_provenance_refs,
            unsafe_assumptions=[
                "Treating partially sourced load data as verified load data would be unsafe.",
            ],
            professional_review_boundaries=[
                "Load data remains planning context and does not replace professional review.",
            ],
            confidence_posture="load_data_source_limited",
            basis=self._constraint_risk_basis(
                source_section_keys=[section_key for section_key, _record in load_records],
                provenance_gap_refs=load_provenance_refs,
                derived_from=[
                    "TwinPlanningContextRecord.record.running_watts",
                    "TwinPlanningContextRecord.missing_fields",
                    "TwinPlanningContextRecord.provenance_gaps",
                ],
            ),
        )

        permission_item = self._constraint_risk_item(
            risk_area=TwinConstraintRiskReasoningArea.permission_limited_visibility,
            non_decisional_severity_label="permission_metadata_only",
            statement=(
                "Permission-limited visibility context is derived from permission-readiness metadata; no permission enforcement exists."
            ),
            observed_constraint_refs=[
                f"permission_readiness_sections:{len(context.sections)}",
                f"advisory_permission_items:{len(advisory_view.permission_readiness_metadata)}",
            ],
            missing_inputs=[
                "active_permission_grants",
                "active_consent_artifacts",
                "permission_enforcement_layer",
            ],
            unsafe_assumptions=[
                "Treating permission readiness metadata as authorization would be unsafe.",
            ],
            professional_review_boundaries=[
                "External visibility requires a future approved permission model.",
            ],
            confidence_posture="permission_readiness_metadata_only",
            basis=self._constraint_risk_basis(
                source_section_keys=source_basis.source_section_keys,
                derived_from=[
                    "TwinPlanningContext.permission_readiness",
                    "TwinPlanningContextRecord.permission_readiness",
                    "TwinAdvisoryContextAssemblyView.permission_readiness_metadata",
                ],
            ),
            limitations=CONSTRAINT_RISK_REASONING_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
        )

        lifecycle_item = self._constraint_risk_item(
            risk_area=TwinConstraintRiskReasoningArea.lifecycle_conflicts,
            non_decisional_severity_label="lifecycle_boundary_requires_separation",
            statement=(
                "Lifecycle conflict risk context is limited to lifecycle boundary separation across current, proposed, saved revision, and deferred lifecycle domains."
            ),
            observed_constraint_refs=lifecycle_signals,
            missing_inputs=[
                "contractor_reviewed_topology",
                "field_verified_topology",
                "utility_reviewed_topology",
                "operational_topology",
            ],
            low_trust_inputs=provenance_gap_refs,
            unsafe_assumptions=[
                "Collapsing planning, proposed, saved revision, verified, utility-reviewed, or operational lifecycle states would be unsafe.",
            ],
            professional_review_boundaries=[
                "Future lifecycle transitions require approved review and authority boundaries.",
            ],
            confidence_posture="lifecycle_boundary_limited",
            basis=self._constraint_risk_basis(
                lifecycle_readiness_signals_used=lifecycle_signals,
                missing_readiness_indicator_refs=missing_readiness_refs,
                derived_from=[
                    "TwinTopologySnapshot.lifecycle_readiness_summary",
                    "TwinTopologySnapshot.lifecycle_readiness_hints",
                    "TwinTopologySnapshot.deferred_lifecycle_domains",
                ],
            ),
        )

        provenance_item = self._constraint_risk_item(
            risk_area=TwinConstraintRiskReasoningArea.provenance_gaps,
            non_decisional_severity_label="provenance_limited",
            statement=(
                "Provenance gap risk context is derived from existing typed provenance gaps and Phase 3A provenance gap posture."
            ),
            observed_constraint_refs=provenance_gap_refs,
            missing_inputs=["complete_field_level_provenance", "verification_workflow"],
            low_trust_inputs=provenance_gap_refs,
            unsafe_assumptions=[
                "Treating provenance presence as verification would be unsafe.",
            ],
            professional_review_boundaries=[
                "Provenance gaps do not prove facts wrong or verified; they require future source review where needed.",
            ],
            confidence_posture="provenance_gap_limited",
            basis=self._constraint_risk_basis(
                source_section_keys=source_basis.source_section_keys,
                provenance_gap_refs=provenance_gap_refs,
                derived_from=[
                    "TwinPlanningContextRecord.provenance_gaps",
                    "TwinDependencyImpactReadinessView.provenance_gap_posture",
                ],
            ),
            limitations=CONSTRAINT_RISK_REASONING_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
        )

        low_trust_item = self._constraint_risk_item(
            risk_area=TwinConstraintRiskReasoningArea.low_trust_assumptions,
            non_decisional_severity_label="assumption_boundary_present",
            statement=(
                "Low-trust assumption context is derived from Phase 3C and Phase 3D unsafe assumption lists."
            ),
            observed_constraint_refs=readiness_view.unsafe_assumptions + [
                item
                for assembly_item in advisory_view.unsafe_assumptions
                for item in assembly_item.unsafe_assumptions
            ],
            missing_inputs=["verified_replacements_for_low_trust_assumptions"],
            low_trust_inputs=provenance_gap_refs,
            unsafe_assumptions=readiness_view.unsafe_assumptions,
            professional_review_boundaries=[
                "Low-trust assumptions remain planning context until future approved verification exists.",
            ],
            confidence_posture="low_trust_assumption_context_present",
            basis=self._constraint_risk_basis(
                source_section_keys=source_basis.source_section_keys,
                provenance_gap_refs=provenance_gap_refs,
                derived_from=[
                    "TwinPlanningIntelligenceReadinessView.unsafe_assumptions",
                    "TwinAdvisoryContextAssemblyView.unsafe_assumptions",
                ],
            ),
        )

        pathway_records = [
            (section_key, record)
            for section_key, record in section_records
            if record.entity_type in {"estimated_pathway", "scenario"}
        ]
        install_refs = []
        for _section_key, record in pathway_records:
            for field_name in [
                "route_difficulty",
                "confidence_level",
                "install_complexity_score",
            ]:
                value = record.record.get(field_name)
                if value is not None:
                    install_refs.append(f"{self._advisory_record_ref(record)}:{field_name}:{value}")
        install_item = self._constraint_risk_item(
            risk_area=TwinConstraintRiskReasoningArea.contractor_install_complexity_risks,
            non_decisional_severity_label="install_complexity_context_present",
            statement=(
                "Contractor/install complexity risk context is derived from existing pathway and scenario planning fields only."
            ),
            observed_constraint_refs=install_refs or ["no_install_complexity_fields_recorded"],
            missing_inputs=["contractor_reviewed_scope", "field_surveyed_route"],
            low_trust_inputs=[
                self._provenance_gap_ref(gap)
                for _section_key, record in pathway_records
                for gap in record.provenance_gaps
            ],
            unsafe_assumptions=[
                "Treating planning install complexity context as contractor direction or proposal logic would be unsafe.",
            ],
            professional_review_boundaries=[
                "Contractor/install complexity context requires future contractor review before directing work.",
            ],
            confidence_posture="install_complexity_context_planning_only",
            basis=self._constraint_risk_basis(
                source_section_keys=[section_key for section_key, _record in pathway_records],
                derived_from=[
                    "TwinPlanningContextRecord.record.route_difficulty",
                    "TwinPlanningContextRecord.record.confidence_level",
                    "TwinPlanningContextRecord.record.install_complexity_score",
                ],
            ),
        )

        field_verification_item = self._constraint_risk_item(
            risk_area=TwinConstraintRiskReasoningArea.field_verification_needs,
            non_decisional_severity_label="field_verification_needed",
            statement=(
                "Field-verification need context is derived from topology missing-readiness indicators and planning limitations."
            ),
            observed_constraint_refs=missing_readiness_refs,
            missing_inputs=missing_readiness_refs + ["field_verification_workflow"],
            low_trust_inputs=provenance_gap_refs,
            unsafe_assumptions=[
                "Treating planning context as field verification would be unsafe.",
            ],
            professional_review_boundaries=[
                "Field verification remains outside current runtime capability.",
            ],
            confidence_posture="field_verification_not_present",
            basis=self._constraint_risk_basis(
                missing_readiness_indicator_refs=missing_readiness_refs,
                derived_from=[
                    "TwinTopologySnapshot.missing_readiness_indicators",
                    "TwinTopologySnapshot.limitations",
                ],
            ),
        )

        professional_review_item = self._constraint_risk_item(
            risk_area=TwinConstraintRiskReasoningArea.professional_review_boundaries,
            non_decisional_severity_label="professional_review_boundary_present",
            statement=(
                "Professional-review boundary context is derived from existing planning limitations and deferred review domains."
            ),
            observed_constraint_refs=[
                "contractor_review_deferred",
                "engineer_review_deferred",
                "field_verification_deferred",
                "utility_review_deferred",
            ],
            missing_inputs=[
                "contractor_reviewed_topology",
                "engineer_review_artifact",
                "field_verification_artifact",
                "utility_review_artifact",
            ],
            unsafe_assumptions=[
                "Treating constraint/risk reasoning as final design guidance or professional direction would be unsafe.",
            ],
            professional_review_boundaries=[
                "Contractor review remains deferred.",
                "Engineer review remains deferred.",
                "Field verification remains deferred.",
                "Utility review remains deferred.",
            ],
            confidence_posture="professional_review_required_not_present",
            basis=self._constraint_risk_basis(
                source_section_keys=source_basis.source_section_keys,
                derived_from=[
                    "TwinTopologySnapshot.deferred_lifecycle_domains",
                    "TwinPlanningContextRecord.limitations",
                    "TwinAdvisoryContextAssemblyView.deferred_advisory_output_boundaries",
                ],
            ),
        )

        items = sorted(
            [
                missing_equipment_item,
                incomplete_topology_item,
                low_trust_item,
                unsupported_load_item,
                permission_item,
                lifecycle_item,
                provenance_item,
                install_item,
                field_verification_item,
                professional_review_item,
            ],
            key=self._constraint_risk_item_sort_key,
        )

        return self._attach_trust_provenance_readiness_summary(TwinConstraintRiskReasoningView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3E constraint and risk reasoning view built request-time from existing TwinPlanningContext "
                "and approved Phase 3 views; not recommendations, priority ranking, optimization, scenario simulation, "
                "what-if analysis, proposals, final design guidance, contractor directives, homeowner directives, economic reasoning, "
                "utility readiness logic, permission enforcement, export, graph engine, persistence, or operational behavior."
            ),
            source_basis=source_basis,
            reasoning_scope=TwinConstraintRiskReasoningScope(
                limitations=CONSTRAINT_RISK_REASONING_LIMITATIONS,
            ),
            constraint_risk_items=items,
            missing_equipment_specs=[
                item for item in items if item.risk_area == TwinConstraintRiskReasoningArea.missing_equipment_specs
            ],
            incomplete_topology=[
                item for item in items if item.risk_area == TwinConstraintRiskReasoningArea.incomplete_topology
            ],
            low_trust_assumptions=[
                item for item in items if item.risk_area == TwinConstraintRiskReasoningArea.low_trust_assumptions
            ],
            unsupported_load_data=[
                item for item in items if item.risk_area == TwinConstraintRiskReasoningArea.unsupported_load_data
            ],
            permission_limited_visibility=[
                item for item in items if item.risk_area == TwinConstraintRiskReasoningArea.permission_limited_visibility
            ],
            lifecycle_conflicts=[
                item for item in items if item.risk_area == TwinConstraintRiskReasoningArea.lifecycle_conflicts
            ],
            provenance_gaps=[
                item for item in items if item.risk_area == TwinConstraintRiskReasoningArea.provenance_gaps
            ],
            contractor_install_complexity_risks=[
                item for item in items if item.risk_area == TwinConstraintRiskReasoningArea.contractor_install_complexity_risks
            ],
            field_verification_needs=[
                item for item in items if item.risk_area == TwinConstraintRiskReasoningArea.field_verification_needs
            ],
            professional_review_boundaries=[
                item for item in items if item.risk_area == TwinConstraintRiskReasoningArea.professional_review_boundaries
            ],
            deferred_capabilities=sorted(CONSTRAINT_RISK_DEFERRED_CAPABILITIES),
            limitations=CONSTRAINT_RISK_REASONING_LIMITATIONS,
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A, Phase 3B, Phase 3C, Phase 3D, AI grounding, "
                "runtime projection, and current /api/* contracts remain unchanged; this is an additive Phase 3E constraint/risk explanation view."
            ),
        ))

    def _scenario_comparison_readiness_basis(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_section_keys: Optional[List[str]] = None,
        scenario_record_refs: Optional[List[str]] = None,
        revision_record_refs: Optional[List[str]] = None,
        linked_design_refs: Optional[List[str]] = None,
        topology_node_refs: Optional[List[str]] = None,
        topology_edge_refs: Optional[List[str]] = None,
        topology_branch_refs: Optional[List[str]] = None,
        provenance_gap_refs: Optional[List[str]] = None,
        permission_basis_refs: Optional[List[str]] = None,
        missing_prerequisite_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinScenarioComparisonReadinessBasis:
        return TwinScenarioComparisonReadinessBasis(
            source_views=self._sorted_unique(
                source_views
                or [
                    "twin_planning_context",
                    "topology_snapshot",
                    "planning_intelligence_readiness",
                    "advisory_context_assembly",
                    "constraint_risk_reasoning",
                ]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            scenario_record_refs=self._sorted_unique(scenario_record_refs or []),
            revision_record_refs=self._sorted_unique(revision_record_refs or []),
            linked_design_refs=self._sorted_unique(linked_design_refs or []),
            topology_node_refs=self._sorted_unique(topology_node_refs or []),
            topology_edge_refs=self._sorted_unique(topology_edge_refs or []),
            topology_branch_refs=self._sorted_unique(topology_branch_refs or []),
            provenance_gap_refs=self._sorted_unique(provenance_gap_refs or []),
            permission_basis_refs=self._sorted_unique(permission_basis_refs or []),
            missing_prerequisite_refs=self._sorted_unique(missing_prerequisite_refs or []),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=SCENARIO_COMPARISON_READINESS_LIMITATIONS,
        )

    def _scenario_comparison_readiness_item(
        self,
        *,
        readiness_area: TwinScenarioComparisonReadinessArea,
        posture: str,
        statement: str,
        available: Optional[List[str]] = None,
        missing: Optional[List[str]] = None,
        blocked_deferred: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinScenarioComparisonReadinessBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinScenarioComparisonReadinessItem:
        return TwinScenarioComparisonReadinessItem(
            readiness_area=readiness_area,
            posture=posture,
            statement=statement,
            available=self._sorted_unique(available or []),
            missing=self._sorted_unique(missing or []),
            blocked_deferred=self._sorted_unique(blocked_deferred or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or SCENARIO_COMPARISON_READINESS_LIMITATIONS,
        )

    def _scenario_comparison_readiness_item_sort_key(
        self, item: TwinScenarioComparisonReadinessItem
    ) -> str:
        return item.readiness_area.value

    def _scenario_branch_ref(self, branch_ref: Dict[str, object]) -> str:
        scenario_id = branch_ref.get("scenario_id") or "unknown"
        design_id = branch_ref.get("linked_design_id") or "unknown"
        return f"scenario_branch:{scenario_id}:linked_design:{design_id}"

    def _scenario_revision_ref(self, revision_ref: Dict[str, object]) -> str:
        revision_id = revision_ref.get("revision_id") or "unknown"
        scenario_id = revision_ref.get("scenario_id") or "unknown"
        return f"scenario_revision_lineage:{revision_id}:scenario:{scenario_id}"

    def _scenario_comparison_provenance_ref(self, gap: TwinPlanningProvenanceGap) -> str:
        field_name = gap.field_name or "record"
        blocked_tokens = {
            "better",
            "worse",
            "delta",
            "score",
            "rank",
            "selected",
            "recommended",
            "impact",
            "outcome",
            "projection",
        }
        if any(token in field_name for token in blocked_tokens):
            field_name = "field_label_not_exposed"
        return f"{gap.gap_type.value}:{gap.entity_type}:{gap.entity_id or 'unknown'}:{field_name}"

    def build_scenario_comparison_readiness_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
        advisory_view: Optional[TwinAdvisoryContextAssemblyView] = None,
        risk_view: Optional[TwinConstraintRiskReasoningView] = None,
    ) -> Optional[TwinScenarioComparisonReadinessView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
        )
        if readiness_view is None:
            return None
        advisory_view = advisory_view or self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None
        risk_view = risk_view or self.build_constraint_risk_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
        )
        if risk_view is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        scenario_records = [
            (section_key, record)
            for section_key, record in section_records
            if section_key == "scenarios" and record.entity_type == "scenario"
        ]
        revision_records = [
            (section_key, record)
            for section_key, record in section_records
            if section_key == "scenario_revisions" and record.entity_type == "scenario_revision"
        ]
        design_records = [
            (section_key, record)
            for section_key, record in section_records
            if record.entity_type == "energy_system_design"
        ]
        design_ids = {record.entity_id for _section_key, record in design_records}
        scenario_refs = [self._advisory_record_ref(record) for _section_key, record in scenario_records]
        revision_refs = [self._advisory_record_ref(record) for _section_key, record in revision_records]
        def linked_design_id(record: TwinPlanningContextRecord) -> Optional[str]:
            return record.record.get("linked_design_id") or record.record.get("design_id")

        linked_design_refs = self._sorted_unique(
            f"{self._advisory_record_ref(record)}:linked_design:{linked_design_id(record) or 'missing'}"
            for _section_key, record in scenario_records + revision_records
        )
        available_link_refs = [
            ref
            for ref in linked_design_refs
            if not ref.endswith(":missing")
        ]
        missing_link_refs = [
            ref
            for ref in linked_design_refs
            if ref.endswith(":missing")
        ] + [
            f"{self._advisory_record_ref(record)}:linked_design_not_in_context:{linked_design_id(record)}"
            for _section_key, record in scenario_records + revision_records
            if linked_design_id(record) and linked_design_id(record) not in design_ids
        ]
        branch_refs = [
            self._scenario_branch_ref(branch_ref)
            for branch_ref in snapshot.scenario_branch_references
        ]
        lineage_refs = [
            self._scenario_revision_ref(revision_ref)
            for revision_ref in snapshot.revision_lineage_references
        ]
        scenario_node_ids = [
            node.node_id
            for node in snapshot.nodes
            if node.entity_type in {"scenario", "scenario_revision", "energy_system_design"}
        ]
        scenario_edge_ids = [
            edge.edge_id
            for edge in snapshot.edges
            if edge.source_node_id in scenario_node_ids or edge.target_node_id in scenario_node_ids
        ]
        provenance_refs = self._sorted_unique(
            self._scenario_comparison_provenance_ref(gap)
            for _section_key, record in scenario_records + revision_records
            for gap in record.provenance_gaps
        )
        permission_refs = self._sorted_unique(
            [
                f"context_permission:{context.permission_readiness.view_permission_alignment.permission_enforcement}"
                if context.permission_readiness
                else "context_permission:missing",
                f"advisory_permission_items:{len(advisory_view.permission_readiness_metadata)}",
            ]
        )
        missing_prerequisites = []
        if len(scenario_records) < 2:
            missing_prerequisites.append("at_least_two_scenario_records")
        if not revision_records:
            missing_prerequisites.append("scenario_revision_lineage")
        if missing_link_refs:
            missing_prerequisites.extend(missing_link_refs)
        if not branch_refs:
            missing_prerequisites.append("topology_scenario_branch_references")
        source_basis = self._scenario_comparison_readiness_basis(
            source_section_keys=[section.section_key for section in context.sections],
            scenario_record_refs=scenario_refs,
            revision_record_refs=revision_refs,
            linked_design_refs=linked_design_refs,
            topology_node_refs=scenario_node_ids,
            topology_edge_refs=scenario_edge_ids,
            topology_branch_refs=branch_refs + lineage_refs,
            provenance_gap_refs=provenance_refs,
            permission_basis_refs=permission_refs,
            missing_prerequisite_refs=missing_prerequisites,
            derived_from=[
                "TwinPlanningContext.sections.scenarios",
                "TwinPlanningContext.sections.scenario_revisions",
                "TwinTopologySnapshot.scenario_branch_references",
                "TwinTopologySnapshot.revision_lineage_references",
                "TwinPlanningIntelligenceReadinessView",
                "TwinAdvisoryContextAssemblyView",
                "TwinConstraintRiskReasoningView",
            ],
        )

        scenario_item = self._scenario_comparison_readiness_item(
            readiness_area=TwinScenarioComparisonReadinessArea.scenario_records_available,
            posture="available" if scenario_refs else "missing",
            statement=(
                "Scenario records are inventoried as available evidence for future comparison readiness only."
            ),
            available=scenario_refs,
            missing=[] if scenario_refs else ["scenario_records"],
            blocked_deferred=SCENARIO_COMPARISON_DEFERRED_BOUNDARIES,
            unsafe_assumptions=[
                "Treating available scenario records as a completed future comparison would be unsafe.",
            ],
            confidence_posture="scenario_records_available_no_comparison_performed",
            basis=self._scenario_comparison_readiness_basis(
                source_section_keys=[section_key for section_key, _record in scenario_records],
                scenario_record_refs=scenario_refs,
                derived_from=["TwinPlanningContext.sections.scenarios"],
            ),
        )
        revision_item = self._scenario_comparison_readiness_item(
            readiness_area=TwinScenarioComparisonReadinessArea.revision_lineage_available,
            posture="available" if revision_refs else "missing",
            statement=(
                "Scenario revision lineage is inventoried as saved planning history for future comparison readiness only."
            ),
            available=revision_refs + lineage_refs,
            missing=[] if revision_refs else ["scenario_revision_lineage"],
            blocked_deferred=["scenario_replay", "recalculation", "invalidation"],
            unsafe_assumptions=[
                "Treating revision lineage as replayed or recalculated scenario state would be unsafe.",
            ],
            confidence_posture="revision_lineage_available_no_replay_performed",
            basis=self._scenario_comparison_readiness_basis(
                source_section_keys=[section_key for section_key, _record in revision_records],
                revision_record_refs=revision_refs,
                topology_branch_refs=lineage_refs,
                derived_from=[
                    "TwinPlanningContext.sections.scenario_revisions",
                    "TwinTopologySnapshot.revision_lineage_references",
                ],
            ),
        )
        linked_design_item = self._scenario_comparison_readiness_item(
            readiness_area=TwinScenarioComparisonReadinessArea.linked_design_reference_readiness,
            posture="available" if available_link_refs and not missing_link_refs else "missing",
            statement=(
                "Linked design references are inventoried only to show whether future comparison prerequisites are present."
            ),
            available=available_link_refs,
            missing=missing_link_refs,
            blocked_deferred=["scenario_comparison", "change_calculation"],
            unsafe_assumptions=[
                "Treating linked design references as a comparison result would be unsafe.",
            ],
            confidence_posture="linked_design_references_checked_no_comparison_performed",
            basis=self._scenario_comparison_readiness_basis(
                source_section_keys=["scenarios", "scenario_revisions", "designs"],
                scenario_record_refs=scenario_refs,
                revision_record_refs=revision_refs,
                linked_design_refs=linked_design_refs,
                derived_from=[
                    "TwinPlanningContextRecord.record.linked_design_id",
                    "TwinPlanningContext.sections.designs",
                ],
            ),
        )
        topology_item = self._scenario_comparison_readiness_item(
            readiness_area=TwinScenarioComparisonReadinessArea.topology_branch_reference_readiness,
            posture="available" if branch_refs or lineage_refs else "missing",
            statement=(
                "Topology branch and lineage references are inventoried as readiness evidence for future comparison only."
            ),
            available=branch_refs + lineage_refs,
            missing=[] if branch_refs or lineage_refs else ["topology_branch_reference_metadata"],
            blocked_deferred=["graph_engine", "scenario_intelligence"],
            unsafe_assumptions=[
                "Treating topology branch references as graph execution or scenario intelligence would be unsafe.",
            ],
            confidence_posture="topology_references_available_no_graph_behavior",
            basis=self._scenario_comparison_readiness_basis(
                topology_node_refs=scenario_node_ids,
                topology_edge_refs=scenario_edge_ids,
                topology_branch_refs=branch_refs + lineage_refs,
                derived_from=[
                    "TwinTopologySnapshot.scenario_branch_references",
                    "TwinTopologySnapshot.revision_lineage_references",
                ],
            ),
        )
        provenance_item = self._scenario_comparison_readiness_item(
            readiness_area=TwinScenarioComparisonReadinessArea.provenance_basis,
            posture="available" if provenance_refs else "missing",
            statement=(
                "Provenance basis is inventoried as source visibility for future comparison readiness, not verification."
            ),
            available=provenance_refs,
            missing=["complete_scenario_source_basis"] if provenance_refs else ["scenario_provenance_basis"],
            blocked_deferred=["verification_workflow"],
            unsafe_assumptions=[
                "Treating provenance presence as verification would be unsafe.",
            ],
            confidence_posture="provenance_visible_not_verified",
            basis=self._scenario_comparison_readiness_basis(
                source_section_keys=["scenarios", "scenario_revisions"],
                scenario_record_refs=scenario_refs,
                revision_record_refs=revision_refs,
                provenance_gap_refs=provenance_refs,
                derived_from=[
                    "TwinPlanningContextRecord.provenance_gaps",
                    "TwinPlanningContextRecord.source_document_ids",
                ],
            ),
            limitations=SCENARIO_COMPARISON_READINESS_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
        )
        permission_item = self._scenario_comparison_readiness_item(
            readiness_area=TwinScenarioComparisonReadinessArea.permission_readiness_metadata,
            posture="available",
            statement=(
                "Permission-readiness metadata is available as metadata only and does not authorize future comparison sharing."
            ),
            available=permission_refs,
            missing=[
                "active_permission_grants",
                "active_consent_artifacts",
                "permission_enforcement_layer",
            ],
            blocked_deferred=["permission_enforcement", "exports"],
            unsafe_assumptions=[
                "Treating permission-readiness metadata as authorization would be unsafe.",
            ],
            confidence_posture="permission_metadata_only_not_enforcement",
            basis=self._scenario_comparison_readiness_basis(
                source_section_keys=source_basis.source_section_keys,
                permission_basis_refs=permission_refs,
                derived_from=[
                    "TwinPlanningContext.permission_readiness",
                    "TwinAdvisoryContextAssemblyView.permission_readiness_metadata",
                ],
            ),
            limitations=SCENARIO_COMPARISON_READINESS_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
        )
        missing_item = self._scenario_comparison_readiness_item(
            readiness_area=TwinScenarioComparisonReadinessArea.missing_prerequisites,
            posture="missing" if missing_prerequisites else "available",
            statement=(
                "Missing prerequisites are inventoried before any future comparison capability is treated as available."
            ),
            available=[] if missing_prerequisites else ["minimum_record_links_available"],
            missing=missing_prerequisites,
            blocked_deferred=SCENARIO_COMPARISON_DEFERRED_BOUNDARIES,
            unsafe_assumptions=[
                "Treating missing prerequisites as completed future comparison capability would be unsafe.",
            ],
            confidence_posture="missing_prerequisites_reported_no_comparison_performed",
            basis=source_basis,
        )
        unsafe_item = self._scenario_comparison_readiness_item(
            readiness_area=TwinScenarioComparisonReadinessArea.unsafe_assumptions,
            posture="blocked/deferred",
            statement=(
                "Unsafe assumptions are surfaced to keep future comparison readiness separate from scenario intelligence."
            ),
            available=["phase_3c_unsafe_assumption_inventory_available"],
            missing=["approved_scenario_comparison_boundary"],
            blocked_deferred=SCENARIO_COMPARISON_DEFERRED_BOUNDARIES,
            unsafe_assumptions=[
                "Treating readiness for future comparison as scenario comparison would be unsafe.",
                "Treating available records as calculated future comparison findings would be unsafe.",
                "Treating readiness metadata as recommendations would be unsafe.",
            ],
            confidence_posture="unsafe_assumptions_visible",
            basis=self._scenario_comparison_readiness_basis(
                source_section_keys=source_basis.source_section_keys,
                derived_from=[
                    "TwinPlanningIntelligenceReadinessView.unsafe_assumptions",
                    "TwinConstraintRiskReasoningView.constraint_risk_items",
                ],
            ),
        )
        confidence_item = self._scenario_comparison_readiness_item(
            readiness_area=TwinScenarioComparisonReadinessArea.confidence_posture,
            posture="readiness for future comparison",
            statement=(
                "Confidence is limited to readiness inventory because no future comparison capability is implemented."
            ),
            available=[
                f"scenario_records:{len(scenario_refs)}",
                f"scenario_revision_records:{len(revision_refs)}",
                f"topology_branch_refs:{len(branch_refs)}",
                f"lineage_refs:{len(lineage_refs)}",
            ],
            missing=missing_prerequisites,
            blocked_deferred=SCENARIO_COMPARISON_DEFERRED_BOUNDARIES,
            unsafe_assumptions=[
                "Treating readiness confidence as future comparison confidence would be unsafe.",
            ],
            confidence_posture="readiness_inventory_only",
            basis=source_basis,
        )
        deferred_item = self._scenario_comparison_readiness_item(
            readiness_area=TwinScenarioComparisonReadinessArea.deferred_scenario_boundaries,
            posture="blocked/deferred",
            statement=(
                "Future scenario comparison boundaries remain blocked/deferred and are not implemented by this view."
            ),
            blocked_deferred=SCENARIO_COMPARISON_DEFERRED_BOUNDARIES,
            unsafe_assumptions=[
                "Treating blocked/deferred boundaries as available runtime behavior would be unsafe.",
            ],
            confidence_posture="blocked_deferred_boundaries_preserved",
            basis=source_basis,
        )
        items = sorted(
            [
                scenario_item,
                revision_item,
                linked_design_item,
                topology_item,
                provenance_item,
                permission_item,
                missing_item,
                unsafe_item,
                confidence_item,
                deferred_item,
            ],
            key=self._scenario_comparison_readiness_item_sort_key,
        )
        unsafe_assumptions = self._sorted_unique(
            assumption
            for item in items
            for assumption in item.unsafe_assumptions
        )
        return self._attach_trust_provenance_readiness_summary(TwinScenarioComparisonReadinessView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3F scenario comparison readiness view built request-time from existing TwinPlanningContext, "
                "topology snapshot, and approved Phase 3 readiness/context views; readiness for future comparison only, "
                "not scenario comparison, scenario intelligence, simulation, what-if analysis, option ordering, optimization, "
                "recommendations, change propagation, stale-state persistence, recalculation, invalidation, proposals, persistence, "
                "exports, graph engine, or operational behavior."
            ),
            source_basis=source_basis,
            readiness_scope=TwinScenarioComparisonReadinessScope(
                limitations=SCENARIO_COMPARISON_READINESS_LIMITATIONS,
            ),
            readiness_items=items,
            scenario_records_available=[
                item
                for item in items
                if item.readiness_area == TwinScenarioComparisonReadinessArea.scenario_records_available
            ],
            scenario_revision_lineage_available=[
                item
                for item in items
                if item.readiness_area == TwinScenarioComparisonReadinessArea.revision_lineage_available
            ],
            linked_design_reference_readiness=[
                item
                for item in items
                if item.readiness_area == TwinScenarioComparisonReadinessArea.linked_design_reference_readiness
            ],
            topology_branch_reference_readiness=[
                item
                for item in items
                if item.readiness_area == TwinScenarioComparisonReadinessArea.topology_branch_reference_readiness
            ],
            provenance_basis=[
                item for item in items if item.readiness_area == TwinScenarioComparisonReadinessArea.provenance_basis
            ],
            permission_readiness_metadata=[
                item
                for item in items
                if item.readiness_area == TwinScenarioComparisonReadinessArea.permission_readiness_metadata
            ],
            missing_prerequisites=self._sorted_unique(missing_prerequisites),
            unsafe_assumptions=unsafe_assumptions,
            confidence_posture=[
                item for item in items if item.readiness_area == TwinScenarioComparisonReadinessArea.confidence_posture
            ],
            deferred_scenario_boundaries=sorted(SCENARIO_COMPARISON_DEFERRED_BOUNDARIES),
            limitations=SCENARIO_COMPARISON_READINESS_LIMITATIONS,
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A through Phase 3E views, AI grounding, "
                "runtime view foundations, and current /api/* contracts remain unchanged; this is an additive Phase 3F readiness view."
            ),
        ))

    def _pre_recommendation_advisory_basis(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_section_keys: Optional[List[str]] = None,
        advisory_area_refs: Optional[List[str]] = None,
        readiness_refs: Optional[List[str]] = None,
        constraint_refs: Optional[List[str]] = None,
        scenario_readiness_refs: Optional[List[str]] = None,
        provenance_refs: Optional[List[str]] = None,
        permission_refs: Optional[List[str]] = None,
        missing_data_refs: Optional[List[str]] = None,
        professional_boundary_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinPreRecommendationAdvisoryBasis:
        return TwinPreRecommendationAdvisoryBasis(
            source_views=self._sorted_unique(
                source_views
                or [
                    "twin_planning_context",
                    "topology_snapshot",
                    "planning_intelligence_readiness",
                    "advisory_context_assembly",
                    "constraint_risk_reasoning",
                    "scenario_comparison_readiness",
                ]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            advisory_area_refs=self._sorted_unique(advisory_area_refs or []),
            readiness_refs=self._sorted_unique(readiness_refs or []),
            constraint_refs=self._sorted_unique(constraint_refs or []),
            scenario_readiness_refs=self._sorted_unique(scenario_readiness_refs or []),
            provenance_refs=self._sorted_unique(provenance_refs or []),
            permission_refs=self._sorted_unique(permission_refs or []),
            missing_data_refs=self._sorted_unique(missing_data_refs or []),
            professional_boundary_refs=self._sorted_unique(professional_boundary_refs or []),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=PRE_RECOMMENDATION_ADVISORY_LIMITATIONS,
        )

    def _pre_recommendation_advisory_item(
        self,
        *,
        advisory_area: TwinPreRecommendationAdvisoryArea,
        posture: str,
        statement: str,
        available_basis: Optional[List[str]] = None,
        missing_data: Optional[List[str]] = None,
        blocked_deferred: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        professional_boundaries: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinPreRecommendationAdvisoryBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinPreRecommendationAdvisoryItem:
        return TwinPreRecommendationAdvisoryItem(
            advisory_area=advisory_area,
            posture=posture,
            statement=statement,
            available_basis=self._sorted_unique(available_basis or []),
            missing_data=self._sorted_unique(missing_data or []),
            blocked_deferred=self._sorted_unique(blocked_deferred or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            professional_boundaries=self._sorted_unique(professional_boundaries or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or PRE_RECOMMENDATION_ADVISORY_LIMITATIONS,
        )

    def _pre_recommendation_advisory_item_sort_key(
        self, item: TwinPreRecommendationAdvisoryItem
    ) -> str:
        return item.advisory_area.value

    def build_pre_recommendation_advisory_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
        advisory_view: Optional[TwinAdvisoryContextAssemblyView] = None,
        risk_view: Optional[TwinConstraintRiskReasoningView] = None,
        scenario_view: Optional[TwinScenarioComparisonReadinessView] = None,
    ) -> Optional[TwinPreRecommendationAdvisoryView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
        )
        if readiness_view is None:
            return None
        advisory_view = advisory_view or self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None
        risk_view = risk_view or self.build_constraint_risk_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
        )
        if risk_view is None:
            return None
        scenario_view = scenario_view or self.build_scenario_comparison_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
        )
        if scenario_view is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        provenance_refs = self._sorted_unique(
            self._provenance_gap_ref(gap)
            for _section_key, record in section_records
            for gap in record.provenance_gaps
        )
        permission_refs = self._sorted_unique(
            [
                f"context_permission:{context.permission_readiness.view_permission_alignment.permission_enforcement}"
                if context.permission_readiness and context.permission_readiness.view_permission_alignment
                else "context_permission:missing",
                f"advisory_permission_items:{len(advisory_view.permission_readiness_metadata)}",
                f"scenario_permission_items:{len(scenario_view.permission_readiness_metadata)}",
            ]
        )
        eligible_refs = [
            "homeowner_goal_explanation",
            "topology_context_explanation",
            "equipment_site_context_explanation",
            "provenance_gap_explanation",
            "permission_readiness_metadata_explanation",
            "constraint_risk_context_explanation",
            "future_comparison_readiness_explanation",
        ]
        missing_data_refs = self._sorted_unique(
            item
            for assembly_item in advisory_view.missing_data
            for item in assembly_item.missing_inputs
        )
        missing_data_refs.extend(
            item
            for risk_item in risk_view.constraint_risk_items
            for item in risk_item.missing_inputs
        )
        missing_data_refs.extend(scenario_view.missing_prerequisites)
        missing_data_refs = self._sorted_unique(missing_data_refs)
        unsafe_assumptions = self._sorted_unique(
            list(scenario_view.unsafe_assumptions)
            + [
                item
                for assembly_item in advisory_view.unsafe_assumptions
                for item in assembly_item.unsafe_assumptions
            ]
            + [
                item
                for risk_item in risk_view.constraint_risk_items
                for item in risk_item.unsafe_assumptions
            ]
        )
        professional_boundaries = self._sorted_unique(
            boundary
            for risk_item in risk_view.constraint_risk_items
            for boundary in risk_item.professional_review_boundaries
        )
        source_basis = self._pre_recommendation_advisory_basis(
            source_section_keys=[section.section_key for section in context.sections],
            advisory_area_refs=eligible_refs,
            readiness_refs=[item.intelligence_area.value for item in readiness_view.ready_areas],
            constraint_refs=[item.risk_area.value for item in risk_view.constraint_risk_items],
            scenario_readiness_refs=[item.readiness_area.value for item in scenario_view.readiness_items],
            provenance_refs=provenance_refs,
            permission_refs=permission_refs,
            missing_data_refs=missing_data_refs,
            professional_boundary_refs=professional_boundaries,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinPlanningIntelligenceReadinessView",
                "TwinAdvisoryContextAssemblyView",
                "TwinConstraintRiskReasoningView",
                "TwinScenarioComparisonReadinessView",
            ],
        )
        eligible_item = self._pre_recommendation_advisory_item(
            advisory_area=TwinPreRecommendationAdvisoryArea.advice_eligible_areas,
            posture="eligible_for_pre_recommendation_advisory_explanation",
            statement=(
                "These areas are eligible for pre-recommendation advisory explanation only; no recommendations are generated."
            ),
            available_basis=eligible_refs,
            missing_data=missing_data_refs,
            blocked_deferred=PRE_RECOMMENDATION_DEFERRED_BOUNDARIES,
            unsafe_assumptions=[
                "Treating eligible advisory explanation areas as recommendations would be unsafe.",
            ],
            professional_boundaries=professional_boundaries,
            confidence_posture="eligible_for_explanation_not_recommendation",
            basis=source_basis,
        )
        blocked_item = self._pre_recommendation_advisory_item(
            advisory_area=TwinPreRecommendationAdvisoryArea.advice_blocked_areas,
            posture="blocked/deferred",
            statement=(
                "Recommendation, directive, comparison, proposal, economic, utility-readiness, and operational advisory behavior remains blocked/deferred."
            ),
            blocked_deferred=PRE_RECOMMENDATION_DEFERRED_BOUNDARIES,
            unsafe_assumptions=[
                "Treating blocked/deferred advisory behavior as available would be unsafe.",
            ],
            confidence_posture="blocked_deferred_boundaries_preserved",
            basis=source_basis,
        )
        missing_item = self._pre_recommendation_advisory_item(
            advisory_area=TwinPreRecommendationAdvisoryArea.missing_data_before_advice,
            posture="missing" if missing_data_refs else "available",
            statement=(
                "Missing data before advice is surfaced so pre-recommendation explanation does not become unsupported guidance."
            ),
            missing_data=missing_data_refs,
            blocked_deferred=["recommendation_generation", "final_design_guidance"],
            unsafe_assumptions=[
                "Treating missing data as resolved advisory basis would be unsafe.",
            ],
            professional_boundaries=professional_boundaries,
            confidence_posture="missing_data_visible_before_recommendations",
            basis=self._pre_recommendation_advisory_basis(
                source_section_keys=source_basis.source_section_keys,
                missing_data_refs=missing_data_refs,
                professional_boundary_refs=professional_boundaries,
                derived_from=[
                    "TwinAdvisoryContextAssemblyView.missing_data",
                    "TwinConstraintRiskReasoningView.constraint_risk_items",
                    "TwinScenarioComparisonReadinessView.missing_prerequisites",
                ],
            ),
        )
        unsafe_item = self._pre_recommendation_advisory_item(
            advisory_area=TwinPreRecommendationAdvisoryArea.unsafe_assumptions,
            posture="unsafe_assumption",
            statement=(
                "Unsafe assumptions are surfaced before recommendations are allowed."
            ),
            available_basis=unsafe_assumptions,
            blocked_deferred=PRE_RECOMMENDATION_DEFERRED_BOUNDARIES,
            unsafe_assumptions=unsafe_assumptions,
            confidence_posture="unsafe_assumptions_visible",
            basis=self._pre_recommendation_advisory_basis(
                source_section_keys=source_basis.source_section_keys,
                derived_from=[
                    "TwinAdvisoryContextAssemblyView.unsafe_assumptions",
                    "TwinConstraintRiskReasoningView.constraint_risk_items",
                    "TwinScenarioComparisonReadinessView.unsafe_assumptions",
                ],
            ),
        )
        professional_item = self._pre_recommendation_advisory_item(
            advisory_area=TwinPreRecommendationAdvisoryArea.professional_verification_boundaries,
            posture="blocked/deferred",
            statement=(
                "Professional verification boundaries remain visible before any recommendation capability is allowed."
            ),
            missing_data=[
                "contractor_reviewed_scope",
                "engineer_review_artifact",
                "field_verification_artifact",
                "utility_review_artifact",
            ],
            blocked_deferred=["final_design_guidance", "contractor_directives", "homeowner_directives"],
            unsafe_assumptions=[
                "Treating pre-recommendation advisory explanation as professional verification would be unsafe.",
            ],
            professional_boundaries=professional_boundaries,
            confidence_posture="professional_verification_not_present",
            basis=self._pre_recommendation_advisory_basis(
                source_section_keys=source_basis.source_section_keys,
                professional_boundary_refs=professional_boundaries,
                derived_from=[
                    "TwinConstraintRiskReasoningView.professional_review_boundaries",
                    "TwinTopologySnapshot.deferred_lifecycle_domains",
                ],
            ),
        )
        provenance_item = self._pre_recommendation_advisory_item(
            advisory_area=TwinPreRecommendationAdvisoryArea.provenance_basis,
            posture="available" if provenance_refs else "missing",
            statement=(
                "Provenance basis is available as source visibility only and is not verification."
            ),
            available_basis=provenance_refs,
            missing_data=["complete_field_level_provenance", "verification_workflow"],
            unsafe_assumptions=[
                "Treating provenance presence as verification would be unsafe.",
            ],
            confidence_posture="provenance_visible_not_verified",
            basis=self._pre_recommendation_advisory_basis(
                source_section_keys=source_basis.source_section_keys,
                provenance_refs=provenance_refs,
                derived_from=[
                    "TwinPlanningContextRecord.provenance_gaps",
                    "TwinScenarioComparisonReadinessView.provenance_basis",
                ],
            ),
            limitations=PRE_RECOMMENDATION_ADVISORY_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
        )
        permission_item = self._pre_recommendation_advisory_item(
            advisory_area=TwinPreRecommendationAdvisoryArea.permission_readiness_basis,
            posture="available",
            statement=(
                "Permission-readiness basis is metadata only and does not authorize advisory sharing."
            ),
            available_basis=permission_refs,
            missing_data=[
                "active_permission_grants",
                "active_consent_artifacts",
                "permission_enforcement_layer",
            ],
            blocked_deferred=["permission_enforcement", "exports"],
            unsafe_assumptions=[
                "Treating permission-readiness basis as permission enforcement would be unsafe.",
            ],
            confidence_posture="permission_metadata_only_not_enforcement",
            basis=self._pre_recommendation_advisory_basis(
                source_section_keys=source_basis.source_section_keys,
                permission_refs=permission_refs,
                derived_from=[
                    "TwinPlanningContext.permission_readiness",
                    "TwinAdvisoryContextAssemblyView.permission_readiness_metadata",
                    "TwinScenarioComparisonReadinessView.permission_readiness_metadata",
                ],
            ),
            limitations=PRE_RECOMMENDATION_ADVISORY_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
        )
        limitations_item = self._pre_recommendation_advisory_item(
            advisory_area=TwinPreRecommendationAdvisoryArea.advisory_limitations,
            posture="blocked/deferred",
            statement=(
                "Advisory limitations preserve the pre-recommendation boundary."
            ),
            available_basis=PRE_RECOMMENDATION_ADVISORY_LIMITATIONS,
            blocked_deferred=PRE_RECOMMENDATION_DEFERRED_BOUNDARIES,
            unsafe_assumptions=[
                "Treating advisory limitations as advice output would be unsafe.",
            ],
            confidence_posture="limitations_visible",
            basis=source_basis,
        )
        deferred_item = self._pre_recommendation_advisory_item(
            advisory_area=TwinPreRecommendationAdvisoryArea.deferred_recommendation_boundaries,
            posture="blocked/deferred",
            statement=(
                "Recommendation boundaries remain blocked/deferred and are not implemented by this view."
            ),
            blocked_deferred=PRE_RECOMMENDATION_DEFERRED_BOUNDARIES,
            unsafe_assumptions=[
                "Treating deferred recommendation boundaries as available runtime behavior would be unsafe.",
            ],
            confidence_posture="deferred_recommendation_boundaries_preserved",
            basis=source_basis,
        )
        items = sorted(
            [
                eligible_item,
                blocked_item,
                missing_item,
                unsafe_item,
                professional_item,
                provenance_item,
                permission_item,
                limitations_item,
                deferred_item,
            ],
            key=self._pre_recommendation_advisory_item_sort_key,
        )
        return self._attach_trust_provenance_readiness_summary(TwinPreRecommendationAdvisoryView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3G pre-recommendation advisory view built request-time from existing TwinPlanningContext, "
                "topology snapshot, and approved Phase 3 readiness/context views; explains what can and cannot be advised "
                "before recommendations are allowed, but does not generate recommendations, rank recommendations, choose a best option, "
                "optimize, simulate, compare scenarios, calculate scenario changes, produce final design guidance, generate proposals, "
                "perform economic reasoning, perform utility readiness logic, create directives, enforce permissions, export data, persist state, "
                "create graph behavior, or operate devices."
            ),
            source_basis=source_basis,
            advisory_scope=TwinPreRecommendationAdvisoryScope(
                limitations=PRE_RECOMMENDATION_ADVISORY_LIMITATIONS,
            ),
            advisory_items=items,
            advice_eligible_areas=[
                item for item in items if item.advisory_area == TwinPreRecommendationAdvisoryArea.advice_eligible_areas
            ],
            advice_blocked_areas=[
                item for item in items if item.advisory_area == TwinPreRecommendationAdvisoryArea.advice_blocked_areas
            ],
            missing_data_before_advice=[
                item
                for item in items
                if item.advisory_area == TwinPreRecommendationAdvisoryArea.missing_data_before_advice
            ],
            unsafe_assumptions=[
                item for item in items if item.advisory_area == TwinPreRecommendationAdvisoryArea.unsafe_assumptions
            ],
            professional_verification_boundaries=[
                item
                for item in items
                if item.advisory_area == TwinPreRecommendationAdvisoryArea.professional_verification_boundaries
            ],
            provenance_basis=[
                item for item in items if item.advisory_area == TwinPreRecommendationAdvisoryArea.provenance_basis
            ],
            permission_readiness_basis=[
                item
                for item in items
                if item.advisory_area == TwinPreRecommendationAdvisoryArea.permission_readiness_basis
            ],
            advisory_limitations=PRE_RECOMMENDATION_ADVISORY_LIMITATIONS,
            deferred_recommendation_boundaries=sorted(PRE_RECOMMENDATION_DEFERRED_BOUNDARIES),
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A through Phase 3F views, AI grounding, "
                "runtime view foundations, and current /api/* contracts remain unchanged; this is an additive Phase 3G advisory boundary view."
            ),
        ))

    def _recommendation_eligibility_basis(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_section_keys: Optional[List[str]] = None,
        eligibility_category_refs: Optional[List[str]] = None,
        eligible_basis_refs: Optional[List[str]] = None,
        blocked_basis_refs: Optional[List[str]] = None,
        missing_prerequisite_refs: Optional[List[str]] = None,
        provenance_refs: Optional[List[str]] = None,
        topology_refs: Optional[List[str]] = None,
        equipment_refs: Optional[List[str]] = None,
        permission_refs: Optional[List[str]] = None,
        professional_boundary_refs: Optional[List[str]] = None,
        advisor_derived_context_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinRecommendationEligibilityBasis:
        return TwinRecommendationEligibilityBasis(
            source_views=self._sorted_unique(
                source_views
                or [
                    "twin_planning_context",
                    "topology_snapshot",
                    "planning_intelligence_readiness",
                    "advisory_context_assembly",
                    "constraint_risk_reasoning",
                    "scenario_comparison_readiness",
                    "pre_recommendation_advisory",
                ]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            eligibility_category_refs=self._sorted_unique(eligibility_category_refs or []),
            eligible_basis_refs=self._sorted_unique(eligible_basis_refs or []),
            blocked_basis_refs=self._sorted_unique(blocked_basis_refs or []),
            missing_prerequisite_refs=self._sorted_unique(missing_prerequisite_refs or []),
            provenance_refs=self._sorted_unique(provenance_refs or []),
            topology_refs=self._sorted_unique(topology_refs or []),
            equipment_refs=self._sorted_unique(equipment_refs or []),
            permission_refs=self._sorted_unique(permission_refs or []),
            professional_boundary_refs=self._sorted_unique(professional_boundary_refs or []),
            advisor_derived_context_refs=self._sorted_unique(advisor_derived_context_refs or []),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=RECOMMENDATION_ELIGIBILITY_READINESS_LIMITATIONS,
        )

    def _recommendation_eligibility_item(
        self,
        *,
        eligibility_area: TwinRecommendationEligibilityArea,
        eligibility_posture: str,
        statement: str,
        eligible_for_future_recommendation: bool = False,
        eligible_basis: Optional[List[str]] = None,
        blocked_deferred: Optional[List[str]] = None,
        missing_prerequisites: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinRecommendationEligibilityBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinRecommendationEligibilityItem:
        return TwinRecommendationEligibilityItem(
            eligibility_area=eligibility_area,
            eligibility_posture=eligibility_posture,
            statement=statement,
            eligible_for_future_recommendation=eligible_for_future_recommendation,
            eligible_basis=self._sorted_unique(eligible_basis or []),
            blocked_deferred=self._sorted_unique(blocked_deferred or []),
            missing_prerequisites=self._sorted_unique(missing_prerequisites or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or RECOMMENDATION_ELIGIBILITY_READINESS_LIMITATIONS,
        )

    def _recommendation_eligibility_item_sort_key(
        self, item: TwinRecommendationEligibilityItem
    ) -> str:
        return item.eligibility_area.value

    def build_recommendation_eligibility_readiness_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
        advisory_view: Optional[TwinAdvisoryContextAssemblyView] = None,
        risk_view: Optional[TwinConstraintRiskReasoningView] = None,
        scenario_view: Optional[TwinScenarioComparisonReadinessView] = None,
        pre_recommendation_view: Optional[TwinPreRecommendationAdvisoryView] = None,
    ) -> Optional[TwinRecommendationEligibilityReadinessView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
        )
        if readiness_view is None:
            return None
        advisory_view = advisory_view or self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None
        risk_view = risk_view or self.build_constraint_risk_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
        )
        if risk_view is None:
            return None
        scenario_view = scenario_view or self.build_scenario_comparison_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
        )
        if scenario_view is None:
            return None
        pre_recommendation_view = pre_recommendation_view or self.build_pre_recommendation_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
        )
        if pre_recommendation_view is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        source_section_keys = [section.section_key for section in context.sections]
        topology_refs = self._sorted_unique(
            [f"topology_node:{node.entity_type}:{node.node_id}" for node in snapshot.nodes]
            + [
                f"topology_edge:{edge.source_node_id}->{edge.target_node_id}:{edge.relationship}"
                for edge in snapshot.edges
            ]
        )
        equipment_records = [
            record
            for _section_key, record in section_records
            if record.entity_type in {"equipment_product", "design_equipment"}
        ]
        equipment_refs = self._sorted_unique(
            f"{record.entity_type}:{record.entity_id or 'unknown'}" for record in equipment_records
        )
        missing_equipment_refs = self._sorted_unique(
            f"{record.entity_type}:{record.entity_id or 'unknown'}:{field}"
            for record in equipment_records
            for field in record.missing_fields
        )
        load_refs = self._sorted_unique(
            f"{record.entity_type}:{record.entity_id or 'unknown'}"
            for _section_key, record in section_records
            if record.entity_type == "load"
        )
        provenance_refs = self._sorted_unique(
            self._provenance_gap_ref(gap)
            for _section_key, record in section_records
            for gap in record.provenance_gaps
        )
        permission_refs = self._sorted_unique(
            [
                f"context_permission:{context.permission_readiness.view_permission_alignment.permission_enforcement}"
                if context.permission_readiness and context.permission_readiness.view_permission_alignment
                else "context_permission:missing",
                f"pre_recommendation_permission_items:{len(pre_recommendation_view.permission_readiness_basis)}",
                f"scenario_permission_items:{len(scenario_view.permission_readiness_metadata)}",
            ]
        )
        professional_boundaries = self._sorted_unique(
            boundary
            for risk_item in risk_view.constraint_risk_items
            for boundary in risk_item.professional_review_boundaries
        )
        missing_prerequisites = self._sorted_unique(
            missing_equipment_refs
            + pre_recommendation_view.missing_data_before_advice[0].missing_data
            + scenario_view.missing_prerequisites
            + [
                "active_permission_grants",
                "active_consent_artifacts",
                "permission_enforcement_layer",
                "engineer_review_artifact",
                "field_verification_artifact",
                "complete_field_level_provenance",
                "verified_equipment_spec_sources",
            ]
        )
        unsafe_assumptions = self._sorted_unique(
            list(pre_recommendation_view.unsafe_assumptions[0].unsafe_assumptions)
            + list(scenario_view.unsafe_assumptions)
            + [
                "Treating eligibility readiness as permission, approval, engineering review, authority, or recommendation generation would be unsafe.",
                "Treating existing advisor-derived records as current recommendation outputs or choices would be unsafe.",
            ]
        )
        advisor_record_counts = Counter(
            record.entity_type
            for _section_key, record in section_records
            if record.entity_type in {"advisor_recommendation_summary", "advisor_note"}
        )
        advisor_context_refs = self._sorted_unique(
            [
                f"existing_derived_advisor_context_records:{advisor_record_counts['advisor_recommendation_summary']}",
                f"existing_advisory_note_records:{advisor_record_counts['advisor_note']}",
            ]
        )
        category_refs = [area.value for area in TwinRecommendationEligibilityArea]
        eligible_basis_refs = [
            "topology_nodes_and_edges_available",
            "pre_recommendation_boundary_explainable",
            "derived_advisor_context_count_available",
        ]
        blocked_basis_refs = self._sorted_unique(
            RECOMMENDATION_ELIGIBILITY_DEFERRED_BOUNDARIES
            + [
                "permission_metadata_only",
                "professional_review_deferred",
                "provenance_presence_not_verification",
                "equipment_specs_incomplete",
            ]
        )
        source_basis = self._recommendation_eligibility_basis(
            source_section_keys=source_section_keys,
            eligibility_category_refs=category_refs,
            eligible_basis_refs=eligible_basis_refs,
            blocked_basis_refs=blocked_basis_refs,
            missing_prerequisite_refs=missing_prerequisites,
            provenance_refs=provenance_refs,
            topology_refs=topology_refs,
            equipment_refs=equipment_refs,
            permission_refs=permission_refs,
            professional_boundary_refs=professional_boundaries,
            advisor_derived_context_refs=advisor_context_refs,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinPlanningIntelligenceReadinessView",
                "TwinAdvisoryContextAssemblyView",
                "TwinConstraintRiskReasoningView",
                "TwinScenarioComparisonReadinessView",
                "TwinPreRecommendationAdvisoryView",
            ],
        )

        topology_item = self._recommendation_eligibility_item(
            eligibility_area=TwinRecommendationEligibilityArea.topology_sufficiency,
            eligibility_posture="eligible_for_future_recommendation_readiness",
            statement=(
                "Topology sufficiency is eligible for future recommendation-readiness explanation because topology nodes and edges are available. "
                "Eligibility means readiness posture only."
            ),
            eligible_for_future_recommendation=True,
            eligible_basis=["topology_nodes_and_edges_available"],
            blocked_deferred=["field_verification", "topology_promotion"],
            missing_prerequisites=["field_verified_topology"],
            unsafe_assumptions=[
                "Treating topology sufficiency as field verification or design approval would be unsafe.",
            ],
            confidence_posture="topology_basis_available_not_verified",
            basis=self._recommendation_eligibility_basis(
                source_section_keys=source_section_keys,
                eligibility_category_refs=[TwinRecommendationEligibilityArea.topology_sufficiency.value],
                eligible_basis_refs=["topology_nodes_and_edges_available"],
                blocked_basis_refs=["field_verification", "topology_promotion"],
                missing_prerequisite_refs=["field_verified_topology"],
                topology_refs=topology_refs,
                derived_from=["TwinTopologySnapshot.nodes", "TwinTopologySnapshot.edges"],
            ),
        )
        equipment_item = self._recommendation_eligibility_item(
            eligibility_area=TwinRecommendationEligibilityArea.equipment_spec_sufficiency,
            eligibility_posture="blocked/deferred",
            statement=(
                "Equipment/spec sufficiency remains blocked/deferred where specs, product provenance, or field verification are incomplete. "
                "Eligibility means readiness posture only."
            ),
            eligible_basis=equipment_refs,
            blocked_deferred=["compatibility_engine", "product_spec_verification", "recommendation_generation"],
            missing_prerequisites=missing_equipment_refs
            or ["complete_equipment_specs", "verified_equipment_spec_sources"],
            unsafe_assumptions=[
                "Treating available equipment records as verified compatibility basis would be unsafe.",
            ],
            confidence_posture="equipment_specs_incomplete",
            basis=self._recommendation_eligibility_basis(
                source_section_keys=source_section_keys,
                eligibility_category_refs=[TwinRecommendationEligibilityArea.equipment_spec_sufficiency.value],
                eligible_basis_refs=equipment_refs,
                blocked_basis_refs=["compatibility_engine", "product_spec_verification"],
                missing_prerequisite_refs=missing_equipment_refs
                or ["complete_equipment_specs", "verified_equipment_spec_sources"],
                equipment_refs=equipment_refs,
                derived_from=["TwinPlanningContext.equipment_products", "TwinPlanningContext.design_equipment"],
            ),
        )
        load_item = self._recommendation_eligibility_item(
            eligibility_area=TwinRecommendationEligibilityArea.load_data_sufficiency,
            eligibility_posture="blocked/deferred",
            statement=(
                "Load data sufficiency remains blocked/deferred for recommendation generation because available load facts are not professional verification or outcome basis. "
                "Eligibility means readiness posture only."
            ),
            eligible_basis=load_refs,
            blocked_deferred=["outcome_calculation", "professional_load_review", "recommendation_generation"],
            missing_prerequisites=["professional_load_review", "field_verified_load_data"],
            unsafe_assumptions=[
                "Treating source-backed load entries as professional load review would be unsafe.",
            ],
            confidence_posture="load_context_available_not_verified",
            basis=self._recommendation_eligibility_basis(
                source_section_keys=source_section_keys,
                eligibility_category_refs=[TwinRecommendationEligibilityArea.load_data_sufficiency.value],
                eligible_basis_refs=load_refs,
                blocked_basis_refs=["outcome_calculation", "professional_load_review"],
                missing_prerequisite_refs=["professional_load_review", "field_verified_load_data"],
                derived_from=["TwinPlanningContext.loads", "TwinConstraintRiskReasoningView.unsupported_load_data"],
            ),
        )
        provenance_item = self._recommendation_eligibility_item(
            eligibility_area=TwinRecommendationEligibilityArea.provenance_sufficiency,
            eligibility_posture="blocked/deferred",
            statement=(
                "Provenance sufficiency is source visibility only; provenance presence is not verification. "
                "Eligibility means readiness posture only."
            ),
            eligible_basis=provenance_refs,
            blocked_deferred=["verification_workflow", "recommendation_generation"],
            missing_prerequisites=["complete_field_level_provenance", "verification_workflow"],
            unsafe_assumptions=[
                "Treating provenance presence as verification would be unsafe.",
            ],
            confidence_posture="provenance_visible_not_verified",
            basis=self._recommendation_eligibility_basis(
                source_section_keys=source_section_keys,
                eligibility_category_refs=[TwinRecommendationEligibilityArea.provenance_sufficiency.value],
                eligible_basis_refs=provenance_refs,
                blocked_basis_refs=["verification_workflow"],
                missing_prerequisite_refs=["complete_field_level_provenance", "verification_workflow"],
                provenance_refs=provenance_refs,
                derived_from=["TwinPlanningContextRecord.provenance_gaps", "TwinPreRecommendationAdvisoryView.provenance_basis"],
            ),
            limitations=RECOMMENDATION_ELIGIBILITY_READINESS_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
        )
        permission_item = self._recommendation_eligibility_item(
            eligibility_area=TwinRecommendationEligibilityArea.permission_readiness_basis,
            eligibility_posture="blocked/deferred",
            statement=(
                "Permission-readiness basis is metadata only and is not permission, authorization, or enforcement. "
                "Eligibility means readiness posture only."
            ),
            eligible_basis=permission_refs,
            blocked_deferred=["permission_enforcement", "auth", "rbac_abac", "exports"],
            missing_prerequisites=[
                "active_permission_grants",
                "active_consent_artifacts",
                "permission_enforcement_layer",
            ],
            unsafe_assumptions=[
                "Treating permission-readiness metadata as authorization would be unsafe.",
            ],
            confidence_posture="permission_metadata_only_not_authorization",
            basis=self._recommendation_eligibility_basis(
                source_section_keys=source_section_keys,
                eligibility_category_refs=[TwinRecommendationEligibilityArea.permission_readiness_basis.value],
                eligible_basis_refs=permission_refs,
                blocked_basis_refs=["permission_enforcement", "auth", "rbac_abac", "exports"],
                missing_prerequisite_refs=[
                    "active_permission_grants",
                    "active_consent_artifacts",
                    "permission_enforcement_layer",
                ],
                permission_refs=permission_refs,
                derived_from=[
                    "TwinPlanningContext.permission_readiness",
                    "TwinPreRecommendationAdvisoryView.permission_readiness_basis",
                    "TwinScenarioComparisonReadinessView.permission_readiness_metadata",
                ],
            ),
            limitations=RECOMMENDATION_ELIGIBILITY_READINESS_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
        )
        professional_item = self._recommendation_eligibility_item(
            eligibility_area=TwinRecommendationEligibilityArea.professional_review_boundaries,
            eligibility_posture="blocked/deferred",
            statement=(
                "Professional review remains deferred; eligibility is not engineering review, approval, authority, or recommendation generation."
            ),
            blocked_deferred=[
                "engineer_review",
                "contractor_review",
                "field_verification",
                "final_design_guidance",
            ],
            missing_prerequisites=[
                "engineer_review_artifact",
                "field_verification_artifact",
                "contractor_reviewed_scope",
            ],
            unsafe_assumptions=[
                "Treating this readiness gate as professional review would be unsafe.",
            ],
            confidence_posture="professional_review_not_present",
            basis=self._recommendation_eligibility_basis(
                source_section_keys=source_section_keys,
                eligibility_category_refs=[TwinRecommendationEligibilityArea.professional_review_boundaries.value],
                blocked_basis_refs=[
                    "engineer_review",
                    "contractor_review",
                    "field_verification",
                    "final_design_guidance",
                ],
                missing_prerequisite_refs=[
                    "engineer_review_artifact",
                    "field_verification_artifact",
                    "contractor_reviewed_scope",
                ],
                professional_boundary_refs=professional_boundaries,
                derived_from=[
                    "TwinConstraintRiskReasoningView.professional_review_boundaries",
                    "TwinPreRecommendationAdvisoryView.professional_verification_boundaries",
                ],
            ),
        )
        scenario_item = self._recommendation_eligibility_item(
            eligibility_area=TwinRecommendationEligibilityArea.scenario_readiness,
            eligibility_posture="blocked/deferred",
            statement=(
                "Scenario readiness may support future readiness explanation, but scenario comparison, outcomes, and what-if analysis remain blocked/deferred. "
                "Eligibility means readiness posture only."
            ),
            eligible_basis=[item.readiness_area.value for item in scenario_view.readiness_items],
            blocked_deferred=["scenario_comparison", "simulation", "what_if_analysis", "outcome_calculation"],
            missing_prerequisites=scenario_view.missing_prerequisites,
            unsafe_assumptions=[
                "Treating scenario readiness as scenario comparison or outcome calculation would be unsafe.",
            ],
            confidence_posture="scenario_readiness_visible_not_executable",
            basis=self._recommendation_eligibility_basis(
                source_section_keys=source_section_keys,
                eligibility_category_refs=[TwinRecommendationEligibilityArea.scenario_readiness.value],
                eligible_basis_refs=[item.readiness_area.value for item in scenario_view.readiness_items],
                blocked_basis_refs=["scenario_comparison", "simulation", "what_if_analysis", "outcome_calculation"],
                missing_prerequisite_refs=scenario_view.missing_prerequisites,
                derived_from=["TwinScenarioComparisonReadinessView.readiness_items"],
            ),
        )
        pre_recommendation_item = self._recommendation_eligibility_item(
            eligibility_area=TwinRecommendationEligibilityArea.pre_recommendation_boundary,
            eligibility_posture="eligible_for_future_recommendation_readiness",
            statement=(
                "The pre-recommendation boundary is eligible for future recommendation-readiness explanation only. "
                "Eligibility means readiness posture only."
            ),
            eligible_for_future_recommendation=True,
            eligible_basis=[item.advisory_area.value for item in pre_recommendation_view.advisory_items],
            blocked_deferred=PRE_RECOMMENDATION_DEFERRED_BOUNDARIES,
            missing_prerequisites=missing_prerequisites,
            unsafe_assumptions=[
                "Treating pre-recommendation advisory explanation as recommendation output would be unsafe.",
            ],
            confidence_posture="pre_recommendation_boundary_visible",
            basis=self._recommendation_eligibility_basis(
                source_section_keys=source_section_keys,
                eligibility_category_refs=[TwinRecommendationEligibilityArea.pre_recommendation_boundary.value],
                eligible_basis_refs=[item.advisory_area.value for item in pre_recommendation_view.advisory_items],
                blocked_basis_refs=PRE_RECOMMENDATION_DEFERRED_BOUNDARIES,
                missing_prerequisite_refs=missing_prerequisites,
                derived_from=["TwinPreRecommendationAdvisoryView.advisory_items"],
            ),
        )
        advisor_context_item = self._recommendation_eligibility_item(
            eligibility_area=TwinRecommendationEligibilityArea.derived_advisor_context,
            eligibility_posture="eligible_for_future_recommendation_readiness",
            statement=(
                "Existing advisor recommendation records are counted only as existing derived-record context/provenance, not as current recommended outputs or choices. "
                "Eligibility means readiness posture only."
            ),
            eligible_for_future_recommendation=True,
            eligible_basis=advisor_context_refs,
            blocked_deferred=["recommendation_generation", "advisor_profile_choice", "current_recommendation_output"],
            unsafe_assumptions=[
                "Treating existing advisor-derived context as a current recommendation or choice would be unsafe.",
            ],
            confidence_posture="derived_record_context_only",
            basis=self._recommendation_eligibility_basis(
                source_section_keys=source_section_keys,
                eligibility_category_refs=[TwinRecommendationEligibilityArea.derived_advisor_context.value],
                eligible_basis_refs=advisor_context_refs,
                blocked_basis_refs=["recommendation_generation", "advisor_profile_choice", "current_recommendation_output"],
                advisor_derived_context_refs=advisor_context_refs,
                derived_from=["TwinPlanningContext.derived_intelligence.record_counts"],
            ),
        )
        deferred_item = self._recommendation_eligibility_item(
            eligibility_area=TwinRecommendationEligibilityArea.deferred_recommendation_generation,
            eligibility_posture="blocked/deferred",
            statement=(
                "Recommendation generation remains blocked/deferred and is not implemented by this eligibility readiness view."
            ),
            blocked_deferred=RECOMMENDATION_ELIGIBILITY_DEFERRED_BOUNDARIES,
            unsafe_assumptions=[
                "Treating deferred recommendation generation as available runtime behavior would be unsafe.",
            ],
            confidence_posture="deferred_recommendation_generation_preserved",
            basis=source_basis,
        )
        items = sorted(
            [
                topology_item,
                equipment_item,
                load_item,
                provenance_item,
                permission_item,
                professional_item,
                scenario_item,
                pre_recommendation_item,
                advisor_context_item,
                deferred_item,
            ],
            key=self._recommendation_eligibility_item_sort_key,
        )
        return self._attach_trust_provenance_readiness_summary(TwinRecommendationEligibilityReadinessView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3H recommendation eligibility readiness view built request-time from existing TwinPlanningContext, "
                "topology snapshot, and approved Phase 3 readiness/advisory views; answers whether fixed categories are eligible "
                "for future recommendation-readiness posture, but does not generate recommendations, expose selected/recommended profiles, "
                "rank, choose a best option, optimize, simulate, compare scenarios, calculate outcomes, generate proposals, perform economic "
                "reasoning, perform utility-readiness reasoning, create directives, enforce permissions, export data, persist state, create graph behavior, or operate devices."
            ),
            source_basis=source_basis,
            eligibility_scope=TwinRecommendationEligibilityScope(
                limitations=RECOMMENDATION_ELIGIBILITY_READINESS_LIMITATIONS,
            ),
            eligibility_items=items,
            eligible_for_future_recommendation=[
                item for item in items if item.eligible_for_future_recommendation
            ],
            blocked_deferred_categories=[
                item for item in items if item.eligibility_posture == "blocked/deferred"
            ],
            missing_prerequisites=missing_prerequisites,
            provenance_sufficiency=[
                item for item in items if item.eligibility_area == TwinRecommendationEligibilityArea.provenance_sufficiency
            ],
            topology_sufficiency=[
                item for item in items if item.eligibility_area == TwinRecommendationEligibilityArea.topology_sufficiency
            ],
            equipment_spec_sufficiency=[
                item
                for item in items
                if item.eligibility_area == TwinRecommendationEligibilityArea.equipment_spec_sufficiency
            ],
            permission_readiness_basis=[
                item
                for item in items
                if item.eligibility_area == TwinRecommendationEligibilityArea.permission_readiness_basis
            ],
            professional_review_boundaries=[
                item
                for item in items
                if item.eligibility_area == TwinRecommendationEligibilityArea.professional_review_boundaries
            ],
            unsafe_assumptions=unsafe_assumptions,
            limitations=RECOMMENDATION_ELIGIBILITY_READINESS_LIMITATIONS,
            deferred_recommendation_generation_boundaries=sorted(
                RECOMMENDATION_ELIGIBILITY_DEFERRED_BOUNDARIES
            ),
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A through Phase 3G views, AI grounding, "
                "runtime view foundations, and current /api/* contracts remain unchanged; this is an additive Phase 3H recommendation-readiness gate."
            ),
        ))

    def _basic_advisory_recommendation_basis(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_section_keys: Optional[List[str]] = None,
        recommendation_category_refs: Optional[List[str]] = None,
        prerequisite_refs: Optional[List[str]] = None,
        eligibility_refs: Optional[List[str]] = None,
        topology_refs: Optional[List[str]] = None,
        equipment_refs: Optional[List[str]] = None,
        provenance_refs: Optional[List[str]] = None,
        permission_refs: Optional[List[str]] = None,
        professional_boundary_refs: Optional[List[str]] = None,
        blocked_deferred_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinBasicAdvisoryRecommendationBasis:
        return TwinBasicAdvisoryRecommendationBasis(
            source_views=self._sorted_unique(
                source_views
                or [
                    "twin_planning_context",
                    "topology_snapshot",
                    "planning_intelligence_readiness",
                    "advisory_context_assembly",
                    "constraint_risk_reasoning",
                    "scenario_comparison_readiness",
                    "pre_recommendation_advisory",
                    "recommendation_eligibility_readiness",
                ]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            recommendation_category_refs=self._sorted_unique(recommendation_category_refs or []),
            prerequisite_refs=self._sorted_unique(prerequisite_refs or []),
            eligibility_refs=self._sorted_unique(eligibility_refs or []),
            topology_refs=self._sorted_unique(topology_refs or []),
            equipment_refs=self._sorted_unique(equipment_refs or []),
            provenance_refs=self._sorted_unique(provenance_refs or []),
            permission_refs=self._sorted_unique(permission_refs or []),
            professional_boundary_refs=self._sorted_unique(professional_boundary_refs or []),
            blocked_deferred_refs=self._sorted_unique(blocked_deferred_refs or []),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=BASIC_ADVISORY_RECOMMENDATIONS_LIMITATIONS,
        )

    def _basic_advisory_recommendation_item(
        self,
        *,
        recommendation_category: TwinBasicAdvisoryRecommendationCategory,
        recommendation_statement: str,
        prerequisite_refs: Optional[List[str]] = None,
        blocked_deferred: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinBasicAdvisoryRecommendationBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinBasicAdvisoryRecommendationItem:
        return TwinBasicAdvisoryRecommendationItem(
            recommendation_category=recommendation_category,
            recommendation_statement=recommendation_statement,
            prerequisite_refs=self._sorted_unique(prerequisite_refs or []),
            blocked_deferred=self._sorted_unique(blocked_deferred or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or BASIC_ADVISORY_RECOMMENDATIONS_LIMITATIONS,
        )

    def _basic_advisory_recommendation_item_sort_key(
        self, item: TwinBasicAdvisoryRecommendationItem
    ) -> str:
        return item.recommendation_category.value

    def build_basic_advisory_recommendations_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
        advisory_view: Optional[TwinAdvisoryContextAssemblyView] = None,
        risk_view: Optional[TwinConstraintRiskReasoningView] = None,
        scenario_view: Optional[TwinScenarioComparisonReadinessView] = None,
        pre_recommendation_view: Optional[TwinPreRecommendationAdvisoryView] = None,
        eligibility_view: Optional[TwinRecommendationEligibilityReadinessView] = None,
    ) -> Optional[TwinBasicAdvisoryRecommendationsView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
        )
        if readiness_view is None:
            return None
        advisory_view = advisory_view or self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None
        risk_view = risk_view or self.build_constraint_risk_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
        )
        if risk_view is None:
            return None
        scenario_view = scenario_view or self.build_scenario_comparison_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
        )
        if scenario_view is None:
            return None
        pre_recommendation_view = pre_recommendation_view or self.build_pre_recommendation_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
        )
        if pre_recommendation_view is None:
            return None
        eligibility_view = eligibility_view or self.build_recommendation_eligibility_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
        )
        if eligibility_view is None:
            return None

        source_section_keys = [section.section_key for section in context.sections]
        topology_refs = self._sorted_unique(
            [f"topology_node:{node.entity_type}:{node.node_id}" for node in snapshot.nodes]
            + [
                f"topology_edge:{edge.source_node_id}->{edge.target_node_id}:{edge.relationship}"
                for edge in snapshot.edges
            ]
        )
        equipment_refs = eligibility_view.source_basis.equipment_refs
        provenance_refs = eligibility_view.source_basis.provenance_refs
        permission_refs = eligibility_view.source_basis.permission_refs
        professional_boundaries = self._sorted_unique(
            eligibility_view.source_basis.professional_boundary_refs
            + [
                boundary
                for risk_item in risk_view.constraint_risk_items
                for boundary in risk_item.professional_review_boundaries
            ]
        )
        missing_prerequisites = eligibility_view.missing_prerequisites
        equipment_missing = (
            eligibility_view.equipment_spec_sufficiency[0].missing_prerequisites
            if eligibility_view.equipment_spec_sufficiency
            else ["complete_equipment_specs", "verified_equipment_spec_sources"]
        )
        permission_provenance_missing = self._sorted_unique(
            [
                "active_permission_grants",
                "active_consent_artifacts",
                "permission_enforcement_layer",
                "complete_field_level_provenance",
                "verification_workflow",
            ]
        )
        scenario_prerequisites = scenario_view.missing_prerequisites or [
            "approved_scenario_comparison_boundary"
        ]
        eligibility_refs = [item.eligibility_area.value for item in eligibility_view.eligibility_items]
        category_refs = [category.value for category in TwinBasicAdvisoryRecommendationCategory]
        source_basis = self._basic_advisory_recommendation_basis(
            source_section_keys=source_section_keys,
            recommendation_category_refs=category_refs,
            prerequisite_refs=missing_prerequisites,
            eligibility_refs=eligibility_refs,
            topology_refs=topology_refs,
            equipment_refs=equipment_refs,
            provenance_refs=provenance_refs,
            permission_refs=permission_refs,
            professional_boundary_refs=professional_boundaries,
            blocked_deferred_refs=BASIC_ADVISORY_RECOMMENDATIONS_DEFERRED_BOUNDARIES,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinPlanningIntelligenceReadinessView",
                "TwinAdvisoryContextAssemblyView",
                "TwinConstraintRiskReasoningView",
                "TwinScenarioComparisonReadinessView",
                "TwinPreRecommendationAdvisoryView",
                "TwinRecommendationEligibilityReadinessView",
            ],
        )
        common_unsafe_assumptions = [
            "Treating prerequisite/remediation recommendations as design, product, proposal, ranking, optimization, or operational guidance would be unsafe.",
        ]
        collect_item = self._basic_advisory_recommendation_item(
            recommendation_category=TwinBasicAdvisoryRecommendationCategory.collect_missing_data,
            recommendation_statement=(
                "Collect missing data before broader recommendations are allowed; this is a prerequisite/remediation recommendation only."
            ),
            prerequisite_refs=missing_prerequisites,
            blocked_deferred=BASIC_ADVISORY_RECOMMENDATIONS_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="missing_prerequisites_visible",
            basis=self._basic_advisory_recommendation_basis(
                source_section_keys=source_section_keys,
                recommendation_category_refs=[
                    TwinBasicAdvisoryRecommendationCategory.collect_missing_data.value
                ],
                prerequisite_refs=missing_prerequisites,
                eligibility_refs=eligibility_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.missing_prerequisites",
                    "TwinPreRecommendationAdvisoryView.missing_data_before_advice",
                ],
            ),
        )
        topology_item = self._basic_advisory_recommendation_item(
            recommendation_category=TwinBasicAdvisoryRecommendationCategory.verify_topology,
            recommendation_statement=(
                "Verify topology before design or proposal recommendations are allowed; this does not approve topology or choose a design."
            ),
            prerequisite_refs=["field_verified_topology"],
            blocked_deferred=["final_design_recommendations", "proposal_generation", "operational_behavior"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating topology verification advice as field-verified topology would be unsafe."],
            confidence_posture="topology_available_not_verified",
            basis=self._basic_advisory_recommendation_basis(
                source_section_keys=source_section_keys,
                recommendation_category_refs=[
                    TwinBasicAdvisoryRecommendationCategory.verify_topology.value
                ],
                prerequisite_refs=["field_verified_topology"],
                topology_refs=topology_refs,
                eligibility_refs=["topology_sufficiency"],
                derived_from=[
                    "TwinTopologySnapshot.nodes",
                    "TwinTopologySnapshot.edges",
                    "TwinRecommendationEligibilityReadinessView.topology_sufficiency",
                ],
            ),
        )
        equipment_item = self._basic_advisory_recommendation_item(
            recommendation_category=(
                TwinBasicAdvisoryRecommendationCategory.verify_equipment_spec_information
            ),
            recommendation_statement=(
                "Verify equipment/spec information before product, compatibility, or design recommendations are allowed."
            ),
            prerequisite_refs=equipment_missing,
            blocked_deferred=[
                "product_recommendations",
                "compatibility_engine",
                "final_design_recommendations",
            ],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating available equipment records as verified specs would be unsafe."],
            confidence_posture="equipment_spec_prerequisites_visible",
            basis=self._basic_advisory_recommendation_basis(
                source_section_keys=source_section_keys,
                recommendation_category_refs=[
                    TwinBasicAdvisoryRecommendationCategory.verify_equipment_spec_information.value
                ],
                prerequisite_refs=equipment_missing,
                equipment_refs=equipment_refs,
                eligibility_refs=["equipment_spec_sufficiency"],
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.equipment_spec_sufficiency",
                    "TwinConstraintRiskReasoningView.missing_equipment_specs",
                ],
            ),
        )
        spec_sheet_item = self._basic_advisory_recommendation_item(
            recommendation_category=TwinBasicAdvisoryRecommendationCategory.request_spec_sheet,
            recommendation_statement=(
                "Request source-backed spec sheets for equipment/spec gaps before compatibility or product recommendations are allowed."
            ),
            prerequisite_refs=equipment_missing or ["source_backed_spec_sheet"],
            blocked_deferred=["product_recommendations", "compatibility_engine"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating a spec sheet request as a product recommendation would be unsafe."],
            confidence_posture="spec_sheet_needed_for_source_backing",
            basis=self._basic_advisory_recommendation_basis(
                source_section_keys=source_section_keys,
                recommendation_category_refs=[
                    TwinBasicAdvisoryRecommendationCategory.request_spec_sheet.value
                ],
                prerequisite_refs=equipment_missing or ["source_backed_spec_sheet"],
                equipment_refs=equipment_refs,
                provenance_refs=provenance_refs,
                eligibility_refs=["equipment_spec_sufficiency", "provenance_sufficiency"],
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.equipment_spec_sufficiency",
                    "TwinRecommendationEligibilityReadinessView.provenance_sufficiency",
                ],
            ),
            limitations=BASIC_ADVISORY_RECOMMENDATIONS_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
        )
        contractor_item = self._basic_advisory_recommendation_item(
            recommendation_category=TwinBasicAdvisoryRecommendationCategory.contractor_review_required,
            recommendation_statement=(
                "Contractor review is required before contractor-scoped design or proposal recommendations can be made; this is not a contractor directive."
            ),
            prerequisite_refs=["contractor_reviewed_scope"],
            blocked_deferred=["contractor_directives", "proposal_generation", "final_design_recommendations"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating contractor review requirement as a contractor directive would be unsafe."],
            confidence_posture="contractor_review_boundary_visible",
            basis=self._basic_advisory_recommendation_basis(
                source_section_keys=source_section_keys,
                recommendation_category_refs=[
                    TwinBasicAdvisoryRecommendationCategory.contractor_review_required.value
                ],
                prerequisite_refs=["contractor_reviewed_scope"],
                professional_boundary_refs=professional_boundaries,
                eligibility_refs=["professional_review_boundaries"],
                derived_from=[
                    "TwinConstraintRiskReasoningView.contractor_install_complexity_risks",
                    "TwinRecommendationEligibilityReadinessView.professional_review_boundaries",
                ],
            ),
        )
        professional_item = self._basic_advisory_recommendation_item(
            recommendation_category=TwinBasicAdvisoryRecommendationCategory.professional_review_required,
            recommendation_statement=(
                "Professional review is required before engineering, final design, safety, or approval recommendations can be made."
            ),
            prerequisite_refs=[
                "engineer_review_artifact",
                "field_verification_artifact",
                "professional_load_review",
            ],
            blocked_deferred=[
                "final_design_recommendations",
                "homeowner_directives",
                "contractor_directives",
                "operational_behavior",
            ],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating basic advisory recommendations as professional review would be unsafe."],
            confidence_posture="professional_review_deferred",
            basis=self._basic_advisory_recommendation_basis(
                source_section_keys=source_section_keys,
                recommendation_category_refs=[
                    TwinBasicAdvisoryRecommendationCategory.professional_review_required.value
                ],
                prerequisite_refs=[
                    "engineer_review_artifact",
                    "field_verification_artifact",
                    "professional_load_review",
                ],
                professional_boundary_refs=professional_boundaries,
                eligibility_refs=["professional_review_boundaries", "load_data_sufficiency"],
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.professional_review_boundaries",
                    "TwinPreRecommendationAdvisoryView.professional_verification_boundaries",
                ],
            ),
        )
        cannot_recommend_item = self._basic_advisory_recommendation_item(
            recommendation_category=(
                TwinBasicAdvisoryRecommendationCategory.cannot_recommend_yet_missing_prerequisites
            ),
            recommendation_statement=(
                "Cannot recommend products, final designs, ranked options, proposals, scenarios, or outcomes yet because prerequisites are missing."
            ),
            prerequisite_refs=missing_prerequisites,
            blocked_deferred=BASIC_ADVISORY_RECOMMENDATIONS_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="recommendation_blockers_visible",
            basis=self._basic_advisory_recommendation_basis(
                source_section_keys=source_section_keys,
                recommendation_category_refs=[
                    TwinBasicAdvisoryRecommendationCategory.cannot_recommend_yet_missing_prerequisites.value
                ],
                prerequisite_refs=missing_prerequisites,
                blocked_deferred_refs=BASIC_ADVISORY_RECOMMENDATIONS_DEFERRED_BOUNDARIES,
                eligibility_refs=[item.eligibility_area.value for item in eligibility_view.blocked_deferred_categories],
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.blocked_deferred_categories",
                    "TwinRecommendationEligibilityReadinessView.missing_prerequisites",
                ],
            ),
        )
        permission_provenance_item = self._basic_advisory_recommendation_item(
            recommendation_category=(
                TwinBasicAdvisoryRecommendationCategory.permission_provenance_limitations_prevent_recommendation
            ),
            recommendation_statement=(
                "Permission/provenance limitations prevent broader recommendations until source visibility, consent, and enforcement prerequisites are addressed."
            ),
            prerequisite_refs=permission_provenance_missing,
            blocked_deferred=["permission_enforcement", "exports", "product_recommendations", "final_design_recommendations"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating permission-readiness metadata or provenance presence as authorization or verification would be unsafe."],
            confidence_posture="permission_and_provenance_limitations_visible",
            basis=self._basic_advisory_recommendation_basis(
                source_section_keys=source_section_keys,
                recommendation_category_refs=[
                    TwinBasicAdvisoryRecommendationCategory.permission_provenance_limitations_prevent_recommendation.value
                ],
                prerequisite_refs=permission_provenance_missing,
                provenance_refs=provenance_refs,
                permission_refs=permission_refs,
                eligibility_refs=["permission_readiness_basis", "provenance_sufficiency"],
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.permission_readiness_basis",
                    "TwinRecommendationEligibilityReadinessView.provenance_sufficiency",
                ],
            ),
            limitations=(
                BASIC_ADVISORY_RECOMMENDATIONS_LIMITATIONS
                + PROVENANCE_GAP_LIMITATIONS
                + PERMISSION_READINESS_LIMITATIONS
            ),
        )
        scenario_item = self._basic_advisory_recommendation_item(
            recommendation_category=TwinBasicAdvisoryRecommendationCategory.scenario_comparison_not_ready,
            recommendation_statement=(
                "Scenario comparison is not ready yet; do not compare scenarios, calculate changes, or use scenario outcomes as recommendation basis."
            ),
            prerequisite_refs=scenario_prerequisites,
            blocked_deferred=[
                "scenario_comparison_execution",
                "scenario_intelligence",
                "simulation",
                "what_if_analysis",
                "outcome_calculation",
            ],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating scenario readiness as scenario comparison would be unsafe."],
            confidence_posture="scenario_comparison_deferred",
            basis=self._basic_advisory_recommendation_basis(
                source_section_keys=source_section_keys,
                recommendation_category_refs=[
                    TwinBasicAdvisoryRecommendationCategory.scenario_comparison_not_ready.value
                ],
                prerequisite_refs=scenario_prerequisites,
                eligibility_refs=["scenario_readiness"],
                blocked_deferred_refs=[
                    "scenario_comparison_execution",
                    "scenario_intelligence",
                    "simulation",
                    "what_if_analysis",
                    "outcome_calculation",
                ],
                derived_from=[
                    "TwinScenarioComparisonReadinessView.missing_prerequisites",
                    "TwinRecommendationEligibilityReadinessView.scenario_readiness",
                ],
            ),
        )
        proposal_item = self._basic_advisory_recommendation_item(
            recommendation_category=TwinBasicAdvisoryRecommendationCategory.proposal_generation_deferred,
            recommendation_statement=(
                "Proposal generation remains deferred; basic advisory recommendations cannot create bids, scopes, designs, or contractor sales outputs."
            ),
            blocked_deferred=["proposal_generation", "contractor_directives", "final_design_recommendations"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating this view as proposal generation would be unsafe."],
            confidence_posture="proposal_generation_deferred",
            basis=self._basic_advisory_recommendation_basis(
                source_section_keys=source_section_keys,
                recommendation_category_refs=[
                    TwinBasicAdvisoryRecommendationCategory.proposal_generation_deferred.value
                ],
                blocked_deferred_refs=["proposal_generation", "contractor_directives", "final_design_recommendations"],
                eligibility_refs=["deferred_recommendation_generation"],
                derived_from=[
                    "TwinPreRecommendationAdvisoryView.deferred_recommendation_boundaries",
                    "TwinRecommendationEligibilityReadinessView.deferred_recommendation_generation_boundaries",
                ],
            ),
        )
        items = sorted(
            [
                collect_item,
                topology_item,
                equipment_item,
                spec_sheet_item,
                contractor_item,
                professional_item,
                cannot_recommend_item,
                permission_provenance_item,
                scenario_item,
                proposal_item,
            ],
            key=self._basic_advisory_recommendation_item_sort_key,
        )
        return self._attach_trust_provenance_readiness_summary(TwinBasicAdvisoryRecommendationsView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3I basic advisory recommendations view built request-time from existing TwinPlanningContext, "
                "topology snapshot, and approved Phase 3 readiness/advisory views; emits only prerequisite/remediation "
                "recommendations and does not recommend products, final designs, ranked options, best options, scenarios, "
                "economic paths, utility-readiness paths, proposals, directives, enforce permissions, export data, persist state, "
                "create graph behavior, create twin_id, or operate devices."
            ),
            source_basis=source_basis,
            recommendation_scope=TwinBasicAdvisoryRecommendationScope(
                limitations=BASIC_ADVISORY_RECOMMENDATIONS_LIMITATIONS,
            ),
            recommendation_items=items,
            collect_missing_data=[
                item
                for item in items
                if item.recommendation_category == TwinBasicAdvisoryRecommendationCategory.collect_missing_data
            ],
            verify_topology=[
                item
                for item in items
                if item.recommendation_category == TwinBasicAdvisoryRecommendationCategory.verify_topology
            ],
            verify_equipment_spec_information=[
                item
                for item in items
                if item.recommendation_category
                == TwinBasicAdvisoryRecommendationCategory.verify_equipment_spec_information
            ],
            request_spec_sheet=[
                item
                for item in items
                if item.recommendation_category == TwinBasicAdvisoryRecommendationCategory.request_spec_sheet
            ],
            contractor_review_required=[
                item
                for item in items
                if item.recommendation_category
                == TwinBasicAdvisoryRecommendationCategory.contractor_review_required
            ],
            professional_review_required=[
                item
                for item in items
                if item.recommendation_category
                == TwinBasicAdvisoryRecommendationCategory.professional_review_required
            ],
            cannot_recommend_yet=[
                item
                for item in items
                if item.recommendation_category
                == TwinBasicAdvisoryRecommendationCategory.cannot_recommend_yet_missing_prerequisites
            ],
            permission_provenance_limitations=[
                item
                for item in items
                if item.recommendation_category
                == TwinBasicAdvisoryRecommendationCategory.permission_provenance_limitations_prevent_recommendation
            ],
            scenario_comparison_not_ready=[
                item
                for item in items
                if item.recommendation_category
                == TwinBasicAdvisoryRecommendationCategory.scenario_comparison_not_ready
            ],
            proposal_generation_deferred=[
                item
                for item in items
                if item.recommendation_category
                == TwinBasicAdvisoryRecommendationCategory.proposal_generation_deferred
            ],
            limitations=BASIC_ADVISORY_RECOMMENDATIONS_LIMITATIONS,
            deferred_recommendation_boundaries=sorted(
                BASIC_ADVISORY_RECOMMENDATIONS_DEFERRED_BOUNDARIES
            ),
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A through Phase 3H views, AI grounding, "
                "runtime view foundations, and current /api/* contracts remain unchanged; this is an additive Phase 3I prerequisite/remediation recommendation view."
            ),
        ))

    def _contractor_facing_advisory_basis(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_section_keys: Optional[List[str]] = None,
        known_refs: Optional[List[str]] = None,
        unknown_refs: Optional[List[str]] = None,
        field_verification_refs: Optional[List[str]] = None,
        install_readiness_refs: Optional[List[str]] = None,
        equipment_refs: Optional[List[str]] = None,
        topology_refs: Optional[List[str]] = None,
        provenance_refs: Optional[List[str]] = None,
        permission_refs: Optional[List[str]] = None,
        professional_boundary_refs: Optional[List[str]] = None,
        prerequisite_recommendation_refs: Optional[List[str]] = None,
        blocked_deferred_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinContractorFacingAdvisoryBasis:
        return TwinContractorFacingAdvisoryBasis(
            source_views=self._sorted_unique(
                source_views
                or [
                    "twin_planning_context",
                    "topology_snapshot",
                    "planning_intelligence_readiness",
                    "advisory_context_assembly",
                    "constraint_risk_reasoning",
                    "scenario_comparison_readiness",
                    "pre_recommendation_advisory",
                    "recommendation_eligibility_readiness",
                    "basic_advisory_recommendations",
                ]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            known_refs=self._sorted_unique(known_refs or []),
            unknown_refs=self._sorted_unique(unknown_refs or []),
            field_verification_refs=self._sorted_unique(field_verification_refs or []),
            install_readiness_refs=self._sorted_unique(install_readiness_refs or []),
            equipment_refs=self._sorted_unique(equipment_refs or []),
            topology_refs=self._sorted_unique(topology_refs or []),
            provenance_refs=self._sorted_unique(provenance_refs or []),
            permission_refs=self._sorted_unique(permission_refs or []),
            professional_boundary_refs=self._sorted_unique(professional_boundary_refs or []),
            prerequisite_recommendation_refs=self._sorted_unique(prerequisite_recommendation_refs or []),
            blocked_deferred_refs=self._sorted_unique(blocked_deferred_refs or []),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=CONTRACTOR_FACING_ADVISORY_LIMITATIONS,
        )

    def _contractor_facing_advisory_item(
        self,
        *,
        advisory_area: TwinContractorFacingAdvisoryArea,
        posture: str,
        statement: str,
        contractor_visible_knowns: Optional[List[str]] = None,
        contractor_visible_unknowns: Optional[List[str]] = None,
        field_verification_needs: Optional[List[str]] = None,
        install_readiness_signals: Optional[List[str]] = None,
        prerequisite_recommendation_refs: Optional[List[str]] = None,
        blocked_deferred: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinContractorFacingAdvisoryBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinContractorFacingAdvisoryItem:
        return TwinContractorFacingAdvisoryItem(
            advisory_area=advisory_area,
            posture=posture,
            statement=statement,
            contractor_visible_knowns=self._sorted_unique(contractor_visible_knowns or []),
            contractor_visible_unknowns=self._sorted_unique(contractor_visible_unknowns or []),
            field_verification_needs=self._sorted_unique(field_verification_needs or []),
            install_readiness_signals=self._sorted_unique(install_readiness_signals or []),
            prerequisite_recommendation_refs=self._sorted_unique(prerequisite_recommendation_refs or []),
            blocked_deferred=self._sorted_unique(blocked_deferred or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or CONTRACTOR_FACING_ADVISORY_LIMITATIONS,
        )

    def _contractor_facing_advisory_item_sort_key(
        self, item: TwinContractorFacingAdvisoryItem
    ) -> str:
        return item.advisory_area.value

    def build_contractor_facing_advisory_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
        advisory_view: Optional[TwinAdvisoryContextAssemblyView] = None,
        risk_view: Optional[TwinConstraintRiskReasoningView] = None,
        scenario_view: Optional[TwinScenarioComparisonReadinessView] = None,
        pre_recommendation_view: Optional[TwinPreRecommendationAdvisoryView] = None,
        eligibility_view: Optional[TwinRecommendationEligibilityReadinessView] = None,
        basic_recommendations_view: Optional[TwinBasicAdvisoryRecommendationsView] = None,
    ) -> Optional[TwinContractorFacingAdvisoryView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
        )
        if readiness_view is None:
            return None
        advisory_view = advisory_view or self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None
        risk_view = risk_view or self.build_constraint_risk_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
        )
        if risk_view is None:
            return None
        scenario_view = scenario_view or self.build_scenario_comparison_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
        )
        if scenario_view is None:
            return None
        pre_recommendation_view = pre_recommendation_view or self.build_pre_recommendation_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
        )
        if pre_recommendation_view is None:
            return None
        eligibility_view = eligibility_view or self.build_recommendation_eligibility_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
        )
        if eligibility_view is None:
            return None
        basic_recommendations_view = basic_recommendations_view or self.build_basic_advisory_recommendations_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
        )
        if basic_recommendations_view is None:
            return None

        source_section_keys = [section.section_key for section in context.sections]
        known_refs = self._sorted_unique(
            [f"section:{section.section_key}:records:{len(section.records)}" for section in context.sections]
            + [
                f"topology_nodes:{len(snapshot.nodes)}",
                f"topology_edges:{len(snapshot.edges)}",
                f"phase_3i_prerequisite_recommendations:{len(basic_recommendations_view.recommendation_items)}",
            ]
        )
        unknown_refs = self._sorted_unique(
            eligibility_view.missing_prerequisites
            + pre_recommendation_view.missing_data_before_advice[0].missing_data
            if pre_recommendation_view.missing_data_before_advice
            else eligibility_view.missing_prerequisites
        )
        field_verification_refs = self._sorted_unique(
            ref
            for item in risk_view.field_verification_needs
            for ref in item.missing_inputs + item.observed_constraint_refs
        )
        install_readiness_refs = self._sorted_unique(
            ref
            for item in risk_view.contractor_install_complexity_risks
            for ref in item.observed_constraint_refs + item.missing_inputs
        )
        equipment_refs = self._sorted_unique(
            eligibility_view.source_basis.equipment_refs
            + [
                ref
                for item in risk_view.missing_equipment_specs
                for ref in item.missing_inputs + item.observed_constraint_refs
            ]
        )
        topology_refs = self._sorted_unique(
            [f"topology_node:{node.entity_type}:{node.node_id}" for node in snapshot.nodes]
            + [
                f"topology_edge:{edge.source_node_id}->{edge.target_node_id}:{edge.relationship}"
                for edge in snapshot.edges
            ]
        )
        provenance_refs = eligibility_view.source_basis.provenance_refs
        permission_refs = eligibility_view.source_basis.permission_refs
        professional_boundary_refs = self._sorted_unique(
            eligibility_view.source_basis.professional_boundary_refs
            + [
                boundary
                for item in risk_view.professional_review_boundaries + risk_view.field_verification_needs
                for boundary in item.professional_review_boundaries
            ]
        )
        prerequisite_recommendation_refs = [
            item.recommendation_category.value
            for item in basic_recommendations_view.recommendation_items
        ]
        source_basis = self._contractor_facing_advisory_basis(
            source_section_keys=source_section_keys,
            known_refs=known_refs,
            unknown_refs=unknown_refs,
            field_verification_refs=field_verification_refs,
            install_readiness_refs=install_readiness_refs,
            equipment_refs=equipment_refs,
            topology_refs=topology_refs,
            provenance_refs=provenance_refs,
            permission_refs=permission_refs,
            professional_boundary_refs=professional_boundary_refs,
            prerequisite_recommendation_refs=prerequisite_recommendation_refs,
            blocked_deferred_refs=CONTRACTOR_FACING_ADVISORY_DEFERRED_BOUNDARIES,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinPlanningIntelligenceReadinessView",
                "TwinAdvisoryContextAssemblyView",
                "TwinConstraintRiskReasoningView",
                "TwinScenarioComparisonReadinessView",
                "TwinPreRecommendationAdvisoryView",
                "TwinRecommendationEligibilityReadinessView",
                "TwinBasicAdvisoryRecommendationsView",
            ],
        )
        common_unsafe_assumptions = [
            "Treating contractor-facing advisory translation as a contractor directive, bid, proposal, final design, or product recommendation would be unsafe.",
        ]
        known_unknown_item = self._contractor_facing_advisory_item(
            advisory_area=TwinContractorFacingAdvisoryArea.contractor_visible_known_unknown_summary,
            posture="contractor_scoping_context_only",
            statement=(
                "Contractor-visible known and unknown context is summarized from existing planning records and derived readiness views only."
            ),
            contractor_visible_knowns=known_refs,
            contractor_visible_unknowns=unknown_refs,
            blocked_deferred=CONTRACTOR_FACING_ADVISORY_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="known_unknown_summary_planning_only",
            basis=self._contractor_facing_advisory_basis(
                source_section_keys=source_section_keys,
                known_refs=known_refs,
                unknown_refs=unknown_refs,
                derived_from=[
                    "TwinPlanningContext.sections",
                    "TwinRecommendationEligibilityReadinessView.missing_prerequisites",
                    "TwinPreRecommendationAdvisoryView.missing_data_before_advice",
                ],
            ),
        )
        field_item = self._contractor_facing_advisory_item(
            advisory_area=TwinContractorFacingAdvisoryArea.field_verification_needs,
            posture="field_verification_needed_before_directing_work",
            statement=(
                "Field-verification needs are visible for contractor scoping context only; this view does not direct field work."
            ),
            contractor_visible_unknowns=field_verification_refs,
            field_verification_needs=field_verification_refs,
            blocked_deferred=["contractor_action_directives", "proposal_generation", "operational_behavior"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating field-verification need context as completed field verification would be unsafe."],
            confidence_posture="field_verification_not_present",
            basis=self._contractor_facing_advisory_basis(
                field_verification_refs=field_verification_refs,
                professional_boundary_refs=professional_boundary_refs,
                derived_from=["TwinConstraintRiskReasoningView.field_verification_needs"],
            ),
        )
        install_item = self._contractor_facing_advisory_item(
            advisory_area=TwinContractorFacingAdvisoryArea.install_readiness_signals,
            posture="install_readiness_context_planning_only",
            statement=(
                "Install-readiness signals are planning-only context from existing pathway and scenario fields, not an install plan."
            ),
            install_readiness_signals=install_readiness_refs,
            field_verification_needs=["contractor_reviewed_scope", "field_surveyed_route"],
            blocked_deferred=["contractor_action_directives", "proposal_generation", "pricing", "bid_logic"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating install-readiness signals as contractor scope or pricing logic would be unsafe."],
            confidence_posture="install_readiness_context_present_not_reviewed",
            basis=self._contractor_facing_advisory_basis(
                install_readiness_refs=install_readiness_refs,
                derived_from=["TwinConstraintRiskReasoningView.contractor_install_complexity_risks"],
            ),
        )
        equipment_item = self._contractor_facing_advisory_item(
            advisory_area=TwinContractorFacingAdvisoryArea.missing_equipment_spec_information,
            posture="equipment_spec_information_incomplete",
            statement=(
                "Missing equipment/spec information is translated for contractor scoping context only and is not product recommendation logic."
            ),
            contractor_visible_unknowns=equipment_refs,
            field_verification_needs=["source_backed_spec_sheet", "verified_equipment_spec_sources"],
            prerequisite_recommendation_refs=[
                TwinBasicAdvisoryRecommendationCategory.verify_equipment_spec_information.value,
                TwinBasicAdvisoryRecommendationCategory.request_spec_sheet.value,
            ],
            blocked_deferred=["product_recommendations", "compatibility_engine", "final_design_recommendations"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating missing spec translation as product compatibility or product selection would be unsafe."],
            confidence_posture="equipment_spec_prerequisites_visible",
            basis=self._contractor_facing_advisory_basis(
                equipment_refs=equipment_refs,
                prerequisite_recommendation_refs=[
                    TwinBasicAdvisoryRecommendationCategory.verify_equipment_spec_information.value,
                    TwinBasicAdvisoryRecommendationCategory.request_spec_sheet.value,
                ],
                derived_from=[
                    "TwinConstraintRiskReasoningView.missing_equipment_specs",
                    "TwinBasicAdvisoryRecommendationsView.verify_equipment_spec_information",
                    "TwinBasicAdvisoryRecommendationsView.request_spec_sheet",
                ],
            ),
        )
        topology_item = self._contractor_facing_advisory_item(
            advisory_area=TwinContractorFacingAdvisoryArea.topology_verification_needs,
            posture="topology_verification_needed_before_directing_work",
            statement=(
                "Topology verification needs are visible for contractor scoping context only; topology is not field-verified by this view."
            ),
            contractor_visible_knowns=topology_refs,
            contractor_visible_unknowns=field_verification_refs,
            field_verification_needs=["field_verified_topology"],
            prerequisite_recommendation_refs=[TwinBasicAdvisoryRecommendationCategory.verify_topology.value],
            blocked_deferred=["final_design_recommendations", "proposal_generation", "operational_behavior"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating planning topology as contractor-verified topology would be unsafe."],
            confidence_posture="topology_context_available_not_verified",
            basis=self._contractor_facing_advisory_basis(
                topology_refs=topology_refs,
                field_verification_refs=field_verification_refs,
                prerequisite_recommendation_refs=[TwinBasicAdvisoryRecommendationCategory.verify_topology.value],
                derived_from=[
                    "TwinTopologySnapshot.nodes",
                    "TwinTopologySnapshot.edges",
                    "TwinConstraintRiskReasoningView.incomplete_topology",
                    "TwinBasicAdvisoryRecommendationsView.verify_topology",
                ],
            ),
        )
        provenance_item = self._contractor_facing_advisory_item(
            advisory_area=TwinContractorFacingAdvisoryArea.provenance_basis,
            posture="provenance_visible_not_verification",
            statement=(
                "Provenance basis is source context for contractor scoping only; provenance presence is not field verification."
            ),
            contractor_visible_knowns=provenance_refs,
            contractor_visible_unknowns=["complete_field_level_provenance", "verification_workflow"],
            blocked_deferred=["verification_workflow", "product_recommendations", "final_design_recommendations"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating provenance presence as verification would be unsafe."],
            confidence_posture="provenance_context_visible_not_verified",
            basis=self._contractor_facing_advisory_basis(
                provenance_refs=provenance_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.provenance_sufficiency",
                    "TwinPreRecommendationAdvisoryView.provenance_basis",
                ],
            ),
            limitations=CONTRACTOR_FACING_ADVISORY_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
        )
        permission_item = self._contractor_facing_advisory_item(
            advisory_area=TwinContractorFacingAdvisoryArea.permission_readiness_metadata,
            posture="permission_readiness_metadata_only",
            statement=(
                "Permission-readiness metadata is visible for contractor-facing advisory context only and is not authorization or enforcement."
            ),
            contractor_visible_knowns=permission_refs,
            contractor_visible_unknowns=["active_permission_grants", "active_consent_artifacts"],
            blocked_deferred=["permission_enforcement", "auth", "rbac_abac", "exports"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating permission-readiness metadata as authorization would be unsafe."],
            confidence_posture="permission_metadata_only_not_authorization",
            basis=self._contractor_facing_advisory_basis(
                permission_refs=permission_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.permission_readiness_basis",
                    "TwinPreRecommendationAdvisoryView.permission_readiness_basis",
                ],
            ),
            limitations=CONTRACTOR_FACING_ADVISORY_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
        )
        professional_item = self._contractor_facing_advisory_item(
            advisory_area=TwinContractorFacingAdvisoryArea.professional_review_boundaries,
            posture="professional_review_boundary_visible",
            statement=(
                "Professional-review boundaries are visible for contractor scoping context only and do not approve work."
            ),
            contractor_visible_unknowns=professional_boundary_refs,
            field_verification_needs=["contractor_reviewed_scope", "engineer_review_artifact", "field_verification_artifact"],
            blocked_deferred=["contractor_action_directives", "final_design_recommendations", "proposal_generation"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating professional-review boundaries as completed review would be unsafe."],
            confidence_posture="professional_review_required_not_present",
            basis=self._contractor_facing_advisory_basis(
                professional_boundary_refs=professional_boundary_refs,
                derived_from=[
                    "TwinConstraintRiskReasoningView.professional_review_boundaries",
                    "TwinRecommendationEligibilityReadinessView.professional_review_boundaries",
                    "TwinPreRecommendationAdvisoryView.professional_verification_boundaries",
                ],
            ),
        )
        prerequisite_item = self._contractor_facing_advisory_item(
            advisory_area=TwinContractorFacingAdvisoryArea.prerequisite_advisory_recommendations,
            posture="phase_3i_prerequisite_remediation_only",
            statement=(
                "Phase 3I prerequisite/remediation recommendations are translated for contractor context only; they are not design advice or contractor directives."
            ),
            prerequisite_recommendation_refs=prerequisite_recommendation_refs,
            contractor_visible_unknowns=basic_recommendations_view.source_basis.prerequisite_refs,
            blocked_deferred=BASIC_ADVISORY_RECOMMENDATIONS_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating prerequisite/remediation recommendations as contractor action directives would be unsafe."],
            confidence_posture="prerequisite_recommendations_visible_not_design_advice",
            basis=self._contractor_facing_advisory_basis(
                prerequisite_recommendation_refs=prerequisite_recommendation_refs,
                blocked_deferred_refs=BASIC_ADVISORY_RECOMMENDATIONS_DEFERRED_BOUNDARIES,
                derived_from=["TwinBasicAdvisoryRecommendationsView.recommendation_items"],
            ),
        )
        deferred_item = self._contractor_facing_advisory_item(
            advisory_area=TwinContractorFacingAdvisoryArea.deferred_contractor_workflow_boundaries,
            posture="contractor_workflows_deferred",
            statement=(
                "Contractor workflow behavior remains deferred; this view does not create proposals, bids, CRM tasks, exports, or directives."
            ),
            blocked_deferred=CONTRACTOR_FACING_ADVISORY_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="contractor_workflow_boundaries_preserved",
            basis=source_basis,
        )
        items = sorted(
            [
                known_unknown_item,
                field_item,
                install_item,
                equipment_item,
                topology_item,
                provenance_item,
                permission_item,
                professional_item,
                prerequisite_item,
                deferred_item,
            ],
            key=self._contractor_facing_advisory_item_sort_key,
        )
        return self._attach_trust_provenance_readiness_summary(TwinContractorFacingAdvisoryView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3J contractor-facing advisory view built request-time from existing TwinPlanningContext, "
                "topology snapshot, and approved Phase 3 readiness/advisory views; translates existing context into "
                "contractor-facing field-verification and install-readiness language only, and does not direct contractor action, "
                "generate proposals, generate pricing or bids, rank options, choose designs, recommend products, recommend final designs, "
                "optimize, simulate, compare scenarios, create marketplace behavior, integrate CRM workflows, enforce permissions, export data, "
                "persist state, create graph behavior, create twin_id, or operate devices."
            ),
            source_basis=source_basis,
            advisory_scope=TwinContractorFacingAdvisoryScope(
                limitations=CONTRACTOR_FACING_ADVISORY_LIMITATIONS,
            ),
            advisory_items=items,
            contractor_visible_known_unknown_summary=[
                item
                for item in items
                if item.advisory_area
                == TwinContractorFacingAdvisoryArea.contractor_visible_known_unknown_summary
            ],
            field_verification_needs=[
                item for item in items if item.advisory_area == TwinContractorFacingAdvisoryArea.field_verification_needs
            ],
            install_readiness_signals=[
                item for item in items if item.advisory_area == TwinContractorFacingAdvisoryArea.install_readiness_signals
            ],
            missing_equipment_spec_information=[
                item
                for item in items
                if item.advisory_area == TwinContractorFacingAdvisoryArea.missing_equipment_spec_information
            ],
            topology_verification_needs=[
                item for item in items if item.advisory_area == TwinContractorFacingAdvisoryArea.topology_verification_needs
            ],
            provenance_basis=[
                item for item in items if item.advisory_area == TwinContractorFacingAdvisoryArea.provenance_basis
            ],
            permission_readiness_metadata=[
                item
                for item in items
                if item.advisory_area == TwinContractorFacingAdvisoryArea.permission_readiness_metadata
            ],
            professional_review_boundaries=[
                item
                for item in items
                if item.advisory_area == TwinContractorFacingAdvisoryArea.professional_review_boundaries
            ],
            prerequisite_advisory_recommendations=[
                item
                for item in items
                if item.advisory_area == TwinContractorFacingAdvisoryArea.prerequisite_advisory_recommendations
            ],
            limitations=CONTRACTOR_FACING_ADVISORY_LIMITATIONS,
            deferred_contractor_workflow_boundaries=sorted(
                CONTRACTOR_FACING_ADVISORY_DEFERRED_BOUNDARIES
            ),
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A through Phase 3I views, AI grounding, "
                "runtime view foundations, and current /api/* contracts remain unchanged; this is an additive Phase 3J contractor-facing translation view."
            ),
        ))

    def _homeowner_facing_advisory_basis(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_section_keys: Optional[List[str]] = None,
        known_refs: Optional[List[str]] = None,
        unknown_refs: Optional[List[str]] = None,
        missing_information_refs: Optional[List[str]] = None,
        question_refs: Optional[List[str]] = None,
        professional_boundary_refs: Optional[List[str]] = None,
        provenance_refs: Optional[List[str]] = None,
        permission_refs: Optional[List[str]] = None,
        prerequisite_recommendation_refs: Optional[List[str]] = None,
        blocked_deferred_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinHomeownerFacingAdvisoryBasis:
        return TwinHomeownerFacingAdvisoryBasis(
            source_views=self._sorted_unique(
                source_views
                or [
                    "twin_planning_context",
                    "topology_snapshot",
                    "planning_intelligence_readiness",
                    "advisory_context_assembly",
                    "constraint_risk_reasoning",
                    "scenario_comparison_readiness",
                    "pre_recommendation_advisory",
                    "recommendation_eligibility_readiness",
                    "basic_advisory_recommendations",
                ]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            known_refs=self._sorted_unique(known_refs or []),
            unknown_refs=self._sorted_unique(unknown_refs or []),
            missing_information_refs=self._sorted_unique(missing_information_refs or []),
            question_refs=self._sorted_unique(question_refs or []),
            professional_boundary_refs=self._sorted_unique(professional_boundary_refs or []),
            provenance_refs=self._sorted_unique(provenance_refs or []),
            permission_refs=self._sorted_unique(permission_refs or []),
            prerequisite_recommendation_refs=self._sorted_unique(prerequisite_recommendation_refs or []),
            blocked_deferred_refs=self._sorted_unique(blocked_deferred_refs or []),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=HOMEOWNER_FACING_ADVISORY_LIMITATIONS,
        )

    def _homeowner_facing_advisory_item(
        self,
        *,
        advisory_area: TwinHomeownerFacingAdvisoryArea,
        posture: str,
        statement: str,
        homeowner_visible_knowns: Optional[List[str]] = None,
        homeowner_visible_unknowns: Optional[List[str]] = None,
        missing_information: Optional[List[str]] = None,
        questions_to_ask_contractor: Optional[List[str]] = None,
        prerequisite_recommendation_refs: Optional[List[str]] = None,
        blocked_deferred: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinHomeownerFacingAdvisoryBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinHomeownerFacingAdvisoryItem:
        return TwinHomeownerFacingAdvisoryItem(
            advisory_area=advisory_area,
            posture=posture,
            statement=statement,
            homeowner_visible_knowns=self._sorted_unique(homeowner_visible_knowns or []),
            homeowner_visible_unknowns=self._sorted_unique(homeowner_visible_unknowns or []),
            missing_information=self._sorted_unique(missing_information or []),
            questions_to_ask_contractor=self._sorted_unique(questions_to_ask_contractor or []),
            prerequisite_recommendation_refs=self._sorted_unique(prerequisite_recommendation_refs or []),
            blocked_deferred=self._sorted_unique(blocked_deferred or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or HOMEOWNER_FACING_ADVISORY_LIMITATIONS,
        )

    def _homeowner_facing_advisory_item_sort_key(
        self, item: TwinHomeownerFacingAdvisoryItem
    ) -> str:
        return item.advisory_area.value

    def build_homeowner_facing_advisory_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
        advisory_view: Optional[TwinAdvisoryContextAssemblyView] = None,
        risk_view: Optional[TwinConstraintRiskReasoningView] = None,
        scenario_view: Optional[TwinScenarioComparisonReadinessView] = None,
        pre_recommendation_view: Optional[TwinPreRecommendationAdvisoryView] = None,
        eligibility_view: Optional[TwinRecommendationEligibilityReadinessView] = None,
        basic_recommendations_view: Optional[TwinBasicAdvisoryRecommendationsView] = None,
    ) -> Optional[TwinHomeownerFacingAdvisoryView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
        )
        if readiness_view is None:
            return None
        advisory_view = advisory_view or self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None
        risk_view = risk_view or self.build_constraint_risk_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
        )
        if risk_view is None:
            return None
        scenario_view = scenario_view or self.build_scenario_comparison_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
        )
        if scenario_view is None:
            return None
        pre_recommendation_view = pre_recommendation_view or self.build_pre_recommendation_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
        )
        if pre_recommendation_view is None:
            return None
        eligibility_view = eligibility_view or self.build_recommendation_eligibility_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
        )
        if eligibility_view is None:
            return None
        basic_recommendations_view = basic_recommendations_view or self.build_basic_advisory_recommendations_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
        )
        if basic_recommendations_view is None:
            return None

        source_section_keys = [section.section_key for section in context.sections]
        known_refs = self._sorted_unique(
            [f"section:{section.section_key}:records:{len(section.records)}" for section in context.sections]
            + [
                f"topology_nodes:{len(snapshot.nodes)}",
                f"topology_edges:{len(snapshot.edges)}",
                f"phase_3i_prerequisite_recommendations:{len(basic_recommendations_view.recommendation_items)}",
            ]
        )
        missing_refs = self._sorted_unique(
            eligibility_view.missing_prerequisites
            + (
                pre_recommendation_view.missing_data_before_advice[0].missing_data
                if pre_recommendation_view.missing_data_before_advice
                else []
            )
            + basic_recommendations_view.source_basis.prerequisite_refs
        )
        professional_boundary_refs = self._sorted_unique(
            eligibility_view.source_basis.professional_boundary_refs
            + [
                boundary
                for item in risk_view.professional_review_boundaries + risk_view.field_verification_needs
                for boundary in item.professional_review_boundaries
            ]
        )
        provenance_refs = eligibility_view.source_basis.provenance_refs
        permission_refs = eligibility_view.source_basis.permission_refs
        prerequisite_recommendation_refs = [
            item.recommendation_category.value
            for item in basic_recommendations_view.recommendation_items
        ]
        question_refs = [
            "which_information_is_missing_or_uncertain",
            "which_topology_or_equipment_details_need_professional_review",
            "which_source_documents_support_the_current_context",
            "which_review_artifacts_are_needed_before_design_or_proposal_decisions",
        ]
        source_basis = self._homeowner_facing_advisory_basis(
            source_section_keys=source_section_keys,
            known_refs=known_refs,
            unknown_refs=missing_refs,
            missing_information_refs=missing_refs,
            question_refs=question_refs,
            professional_boundary_refs=professional_boundary_refs,
            provenance_refs=provenance_refs,
            permission_refs=permission_refs,
            prerequisite_recommendation_refs=prerequisite_recommendation_refs,
            blocked_deferred_refs=HOMEOWNER_FACING_ADVISORY_DEFERRED_BOUNDARIES,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinPlanningIntelligenceReadinessView",
                "TwinAdvisoryContextAssemblyView",
                "TwinConstraintRiskReasoningView",
                "TwinScenarioComparisonReadinessView",
                "TwinPreRecommendationAdvisoryView",
                "TwinRecommendationEligibilityReadinessView",
                "TwinBasicAdvisoryRecommendationsView",
            ],
        )
        common_unsafe_assumptions = [
            "Treating homeowner-facing advisory translation as homeowner action direction, final design guidance, a product recommendation, a proposal, or a sales claim would be unsafe.",
        ]
        known_unknown_item = self._homeowner_facing_advisory_item(
            advisory_area=TwinHomeownerFacingAdvisoryArea.homeowner_visible_known_unknown_summary,
            posture="homeowner_context_summary_only",
            statement=(
                "Homeowner-visible known and unknown context is summarized from existing planning records and derived readiness views only."
            ),
            homeowner_visible_knowns=known_refs,
            homeowner_visible_unknowns=missing_refs,
            missing_information=missing_refs,
            blocked_deferred=HOMEOWNER_FACING_ADVISORY_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="known_unknown_summary_planning_only",
            basis=self._homeowner_facing_advisory_basis(
                source_section_keys=source_section_keys,
                known_refs=known_refs,
                unknown_refs=missing_refs,
                missing_information_refs=missing_refs,
                derived_from=[
                    "TwinPlanningContext.sections",
                    "TwinRecommendationEligibilityReadinessView.missing_prerequisites",
                    "TwinPreRecommendationAdvisoryView.missing_data_before_advice",
                    "TwinBasicAdvisoryRecommendationsView.source_basis.prerequisite_refs",
                ],
            ),
        )
        safe_context_item = self._homeowner_facing_advisory_item(
            advisory_area=TwinHomeownerFacingAdvisoryArea.safe_context_explanation,
            posture="safe_explanation_language_only",
            statement=(
                "Current context can explain missing data, source basis, permission-readiness metadata, topology uncertainty, and professional-review boundaries in plain language only."
            ),
            homeowner_visible_knowns=[
                "known_and_unknown_summary_available",
                "missing_information_visible",
                "professional_review_boundaries_visible",
                "provenance_basis_visible",
                "permission_readiness_metadata_visible",
            ],
            homeowner_visible_unknowns=missing_refs,
            blocked_deferred=["homeowner_action_directives", "final_design_guidance", "sales_claims"],
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="safe_explanation_context_present_not_design_guidance",
            basis=self._homeowner_facing_advisory_basis(
                known_refs=known_refs,
                unknown_refs=missing_refs,
                derived_from=[
                    "TwinAdvisoryContextAssemblyView",
                    "TwinConstraintRiskReasoningView",
                    "TwinRecommendationEligibilityReadinessView",
                ],
            ),
        )
        missing_information_item = self._homeowner_facing_advisory_item(
            advisory_area=TwinHomeownerFacingAdvisoryArea.missing_information,
            posture="missing_information_visible_before_design_decisions",
            statement=(
                "Missing information is translated for homeowner understanding only and is not final design guidance."
            ),
            homeowner_visible_unknowns=missing_refs,
            missing_information=missing_refs,
            blocked_deferred=["final_design_guidance", "product_recommendations", "proposal_generation"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating missing information context as enough for design decisions would be unsafe."],
            confidence_posture="missing_information_prerequisites_visible",
            basis=self._homeowner_facing_advisory_basis(
                missing_information_refs=missing_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.missing_prerequisites",
                    "TwinPreRecommendationAdvisoryView.missing_data_before_advice",
                    "TwinBasicAdvisoryRecommendationsView.source_basis.prerequisite_refs",
                ],
            ),
        )
        questions_item = self._homeowner_facing_advisory_item(
            advisory_area=TwinHomeownerFacingAdvisoryArea.questions_to_ask_contractor,
            posture="conversation_prompts_only",
            statement=(
                "Questions to ask a contractor are planning conversation prompts only and are not homeowner instructions or contractor directives."
            ),
            questions_to_ask_contractor=[
                "Which equipment or spec details still need source-backed confirmation?",
                "Which topology facts need field or professional review before design decisions?",
                "Which source documents or review artifacts would be needed before proposal or installation decisions?",
                "Which limitations should remain visible until professional review is complete?",
            ],
            blocked_deferred=["homeowner_action_directives", "contractor_directives", "proposal_generation"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating conversation prompts as instructions to perform work would be unsafe."],
            confidence_posture="questions_are_prompts_not_directives",
            basis=self._homeowner_facing_advisory_basis(
                question_refs=question_refs,
                missing_information_refs=missing_refs,
                professional_boundary_refs=professional_boundary_refs,
                derived_from=[
                    "TwinConstraintRiskReasoningView",
                    "TwinRecommendationEligibilityReadinessView",
                    "TwinBasicAdvisoryRecommendationsView",
                ],
            ),
        )
        professional_item = self._homeowner_facing_advisory_item(
            advisory_area=TwinHomeownerFacingAdvisoryArea.professional_review_boundaries,
            posture="professional_review_boundary_visible",
            statement=(
                "Professional-review boundaries explain where qualified review is still needed; this view does not approve work or provide final design guidance."
            ),
            homeowner_visible_unknowns=professional_boundary_refs,
            missing_information=professional_boundary_refs,
            blocked_deferred=["final_design_guidance", "contractor_directives", "operational_behavior"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating professional-review boundaries as completed review would be unsafe."],
            confidence_posture="professional_review_required_not_present",
            basis=self._homeowner_facing_advisory_basis(
                professional_boundary_refs=professional_boundary_refs,
                derived_from=[
                    "TwinConstraintRiskReasoningView.professional_review_boundaries",
                    "TwinRecommendationEligibilityReadinessView.professional_review_boundaries",
                    "TwinPreRecommendationAdvisoryView.professional_verification_boundaries",
                ],
            ),
        )
        provenance_item = self._homeowner_facing_advisory_item(
            advisory_area=TwinHomeownerFacingAdvisoryArea.provenance_basis_plain_language,
            posture="provenance_visible_not_verification",
            statement=(
                "Provenance basis explains where current context came from in plain language; provenance presence is not field verification."
            ),
            homeowner_visible_knowns=provenance_refs,
            homeowner_visible_unknowns=["complete_field_level_provenance", "verification_workflow"],
            blocked_deferred=["verification_workflow", "final_design_guidance", "sales_claims"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating provenance presence as verification would be unsafe."],
            confidence_posture="provenance_context_visible_not_verified",
            basis=self._homeowner_facing_advisory_basis(
                provenance_refs=provenance_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.provenance_sufficiency",
                    "TwinPreRecommendationAdvisoryView.provenance_basis",
                ],
            ),
            limitations=HOMEOWNER_FACING_ADVISORY_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
        )
        permission_item = self._homeowner_facing_advisory_item(
            advisory_area=TwinHomeownerFacingAdvisoryArea.permission_readiness_metadata,
            posture="permission_readiness_metadata_only",
            statement=(
                "Permission-readiness metadata is visible for homeowner-facing readiness context only and is not authorization or enforcement."
            ),
            homeowner_visible_knowns=permission_refs,
            homeowner_visible_unknowns=["active_permission_grants", "active_consent_artifacts"],
            blocked_deferred=["permission_enforcement", "auth", "rbac_abac", "exports"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating permission-readiness metadata as authorization would be unsafe."],
            confidence_posture="permission_metadata_only_not_authorization",
            basis=self._homeowner_facing_advisory_basis(
                permission_refs=permission_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.permission_readiness_basis",
                    "TwinPreRecommendationAdvisoryView.permission_readiness_basis",
                ],
            ),
            limitations=HOMEOWNER_FACING_ADVISORY_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
        )
        prerequisite_item = self._homeowner_facing_advisory_item(
            advisory_area=TwinHomeownerFacingAdvisoryArea.prerequisite_advisory_recommendations,
            posture="phase_3i_prerequisite_remediation_only",
            statement=(
                "Phase 3I prerequisite/remediation recommendations are translated for homeowner understanding only; they are not design advice, product recommendations, or homeowner directives."
            ),
            prerequisite_recommendation_refs=prerequisite_recommendation_refs,
            homeowner_visible_unknowns=basic_recommendations_view.source_basis.prerequisite_refs,
            missing_information=basic_recommendations_view.source_basis.prerequisite_refs,
            blocked_deferred=BASIC_ADVISORY_RECOMMENDATIONS_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating prerequisite/remediation recommendations as homeowner action directives would be unsafe."],
            confidence_posture="prerequisite_recommendations_visible_not_design_advice",
            basis=self._homeowner_facing_advisory_basis(
                prerequisite_recommendation_refs=prerequisite_recommendation_refs,
                blocked_deferred_refs=BASIC_ADVISORY_RECOMMENDATIONS_DEFERRED_BOUNDARIES,
                derived_from=["TwinBasicAdvisoryRecommendationsView.recommendation_items"],
            ),
        )
        deferred_item = self._homeowner_facing_advisory_item(
            advisory_area=TwinHomeownerFacingAdvisoryArea.deferred_homeowner_workflow_boundaries,
            posture="homeowner_workflows_deferred",
            statement=(
                "Homeowner workflow behavior remains deferred; this view does not create action directives, design guidance, proposals, sales claims, exports, or operational behavior."
            ),
            blocked_deferred=HOMEOWNER_FACING_ADVISORY_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="homeowner_workflow_boundaries_preserved",
            basis=source_basis,
        )
        items = sorted(
            [
                known_unknown_item,
                safe_context_item,
                missing_information_item,
                questions_item,
                professional_item,
                provenance_item,
                permission_item,
                prerequisite_item,
                deferred_item,
            ],
            key=self._homeowner_facing_advisory_item_sort_key,
        )
        return self._attach_trust_provenance_readiness_summary(TwinHomeownerFacingAdvisoryView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3K homeowner-facing advisory view built request-time from existing TwinPlanningContext, "
                "topology snapshot, and approved Phase 3 readiness/advisory views; translates existing context into "
                "homeowner-facing safe explanation language only, and does not direct homeowner action, generate final design guidance, "
                "recommend products or specific equipment, rank options, choose designs, compare scenarios, simulate outcomes, "
                "calculate savings or payback, generate proposals, create sales claims, create contractor directives, enforce permissions, "
                "export data, persist state, create graph behavior, create twin_id, or operate devices."
            ),
            source_basis=source_basis,
            advisory_scope=TwinHomeownerFacingAdvisoryScope(
                limitations=HOMEOWNER_FACING_ADVISORY_LIMITATIONS,
            ),
            advisory_items=items,
            homeowner_visible_known_unknown_summary=[
                item
                for item in items
                if item.advisory_area
                == TwinHomeownerFacingAdvisoryArea.homeowner_visible_known_unknown_summary
            ],
            safe_context_explanation=[
                item for item in items if item.advisory_area == TwinHomeownerFacingAdvisoryArea.safe_context_explanation
            ],
            missing_information=[
                item for item in items if item.advisory_area == TwinHomeownerFacingAdvisoryArea.missing_information
            ],
            questions_to_ask_contractor=[
                item for item in items if item.advisory_area == TwinHomeownerFacingAdvisoryArea.questions_to_ask_contractor
            ],
            professional_review_boundaries=[
                item
                for item in items
                if item.advisory_area == TwinHomeownerFacingAdvisoryArea.professional_review_boundaries
            ],
            provenance_basis_plain_language=[
                item
                for item in items
                if item.advisory_area == TwinHomeownerFacingAdvisoryArea.provenance_basis_plain_language
            ],
            permission_readiness_metadata=[
                item
                for item in items
                if item.advisory_area == TwinHomeownerFacingAdvisoryArea.permission_readiness_metadata
            ],
            prerequisite_advisory_recommendations=[
                item
                for item in items
                if item.advisory_area == TwinHomeownerFacingAdvisoryArea.prerequisite_advisory_recommendations
            ],
            limitations=HOMEOWNER_FACING_ADVISORY_LIMITATIONS,
            deferred_homeowner_workflow_boundaries=sorted(
                HOMEOWNER_FACING_ADVISORY_DEFERRED_BOUNDARIES
            ),
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A through Phase 3I views, AI grounding, "
                "runtime view foundations, and current /api/* contracts remain unchanged; this is an additive Phase 3K homeowner-facing translation view."
            ),
        ))

    def _energy_goal_reasoning_basis(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_section_keys: Optional[List[str]] = None,
        goal_refs: Optional[List[str]] = None,
        known_fact_refs: Optional[List[str]] = None,
        missing_prerequisite_refs: Optional[List[str]] = None,
        advisory_context_refs: Optional[List[str]] = None,
        provenance_refs: Optional[List[str]] = None,
        permission_refs: Optional[List[str]] = None,
        professional_boundary_refs: Optional[List[str]] = None,
        unsafe_assumption_refs: Optional[List[str]] = None,
        blocked_deferred_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinEnergyGoalReasoningBasis:
        return TwinEnergyGoalReasoningBasis(
            source_views=self._sorted_unique(
                source_views
                or [
                    "twin_planning_context",
                    "topology_snapshot",
                    "advisory_context_assembly",
                    "constraint_risk_reasoning",
                    "pre_recommendation_advisory",
                    "recommendation_eligibility_readiness",
                    "basic_advisory_recommendations",
                    "contractor_facing_advisory",
                    "homeowner_facing_advisory",
                ]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            goal_refs=self._sorted_unique(goal_refs or []),
            known_fact_refs=self._sorted_unique(known_fact_refs or []),
            missing_prerequisite_refs=self._sorted_unique(missing_prerequisite_refs or []),
            advisory_context_refs=self._sorted_unique(advisory_context_refs or []),
            provenance_refs=self._sorted_unique(provenance_refs or []),
            permission_refs=self._sorted_unique(permission_refs or []),
            professional_boundary_refs=self._sorted_unique(professional_boundary_refs or []),
            unsafe_assumption_refs=self._sorted_unique(unsafe_assumption_refs or []),
            blocked_deferred_refs=self._sorted_unique(blocked_deferred_refs or []),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=ENERGY_GOAL_REASONING_LIMITATIONS,
        )

    def _energy_goal_reasoning_item(
        self,
        *,
        reasoning_area: TwinEnergyGoalReasoningArea,
        posture: str,
        statement: str,
        recorded_goal_refs: Optional[List[str]] = None,
        known_fact_alignment: Optional[List[str]] = None,
        missing_prerequisite_gaps: Optional[List[str]] = None,
        advisory_context_links: Optional[List[str]] = None,
        blocked_deferred: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinEnergyGoalReasoningBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinEnergyGoalReasoningItem:
        return TwinEnergyGoalReasoningItem(
            reasoning_area=reasoning_area,
            posture=posture,
            statement=statement,
            recorded_goal_refs=self._sorted_unique(recorded_goal_refs or []),
            known_fact_alignment=self._sorted_unique(known_fact_alignment or []),
            missing_prerequisite_gaps=self._sorted_unique(missing_prerequisite_gaps or []),
            advisory_context_links=self._sorted_unique(advisory_context_links or []),
            blocked_deferred=self._sorted_unique(blocked_deferred or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or ENERGY_GOAL_REASONING_LIMITATIONS,
        )

    def _energy_goal_reasoning_item_sort_key(
        self, item: TwinEnergyGoalReasoningItem
    ) -> str:
        return item.reasoning_area.value

    def build_energy_goal_reasoning_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
        advisory_view: Optional[TwinAdvisoryContextAssemblyView] = None,
        risk_view: Optional[TwinConstraintRiskReasoningView] = None,
        scenario_view: Optional[TwinScenarioComparisonReadinessView] = None,
        pre_recommendation_view: Optional[TwinPreRecommendationAdvisoryView] = None,
        eligibility_view: Optional[TwinRecommendationEligibilityReadinessView] = None,
        basic_recommendations_view: Optional[TwinBasicAdvisoryRecommendationsView] = None,
        contractor_advisory_view: Optional[TwinContractorFacingAdvisoryView] = None,
        homeowner_advisory_view: Optional[TwinHomeownerFacingAdvisoryView] = None,
    ) -> Optional[TwinEnergyGoalReasoningView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
        )
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
        )
        if readiness_view is None:
            return None
        advisory_view = advisory_view or self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None
        risk_view = risk_view or self.build_constraint_risk_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
        )
        if risk_view is None:
            return None
        scenario_view = scenario_view or self.build_scenario_comparison_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
        )
        if scenario_view is None:
            return None
        pre_recommendation_view = pre_recommendation_view or self.build_pre_recommendation_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
        )
        if pre_recommendation_view is None:
            return None
        eligibility_view = eligibility_view or self.build_recommendation_eligibility_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
        )
        if eligibility_view is None:
            return None
        basic_recommendations_view = basic_recommendations_view or self.build_basic_advisory_recommendations_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
        )
        if basic_recommendations_view is None:
            return None
        contractor_advisory_view = contractor_advisory_view or self.build_contractor_facing_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
        )
        if contractor_advisory_view is None:
            return None
        homeowner_advisory_view = homeowner_advisory_view or self.build_homeowner_facing_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
        )
        if homeowner_advisory_view is None:
            return None

        source_section_keys = [section.section_key for section in context.sections]
        goal_refs = self._sorted_unique(
            goal
            for goal_item in advisory_view.homeowner_goals
            for goal in goal_item.assembled_inputs + goal_item.missing_inputs
        )
        known_fact_refs = self._sorted_unique(
            [f"section:{section.section_key}:records:{len(section.records)}" for section in context.sections]
            + [
                f"topology_nodes:{len(snapshot.nodes)}",
                f"topology_edges:{len(snapshot.edges)}",
                f"advisory_goal_items:{len(advisory_view.homeowner_goals)}",
                f"contractor_advisory_items:{len(contractor_advisory_view.advisory_items)}",
                f"homeowner_advisory_items:{len(homeowner_advisory_view.advisory_items)}",
            ]
        )
        missing_prerequisite_refs = self._sorted_unique(
            eligibility_view.missing_prerequisites
            + (
                pre_recommendation_view.missing_data_before_advice[0].missing_data
                if pre_recommendation_view.missing_data_before_advice
                else []
            )
            + basic_recommendations_view.source_basis.prerequisite_refs
            + [
                missing
                for goal_item in advisory_view.homeowner_goals
                for missing in goal_item.missing_inputs
            ]
        )
        advisory_context_refs = self._sorted_unique(
            [
                "TwinAdvisoryContextAssemblyView.homeowner_goals",
                "TwinContractorFacingAdvisoryView.contractor_visible_known_unknown_summary",
                "TwinContractorFacingAdvisoryView.professional_review_boundaries",
                "TwinHomeownerFacingAdvisoryView.homeowner_visible_known_unknown_summary",
                "TwinHomeownerFacingAdvisoryView.questions_to_ask_contractor",
                "TwinBasicAdvisoryRecommendationsView.recommendation_items",
            ]
        )
        provenance_refs = eligibility_view.source_basis.provenance_refs
        permission_refs = eligibility_view.source_basis.permission_refs
        professional_boundary_refs = self._sorted_unique(
            eligibility_view.source_basis.professional_boundary_refs
            + [
                boundary
                for item in risk_view.professional_review_boundaries + risk_view.field_verification_needs
                for boundary in item.professional_review_boundaries
            ]
        )
        unsafe_assumption_refs = self._sorted_unique(
            list(scenario_view.unsafe_assumptions)
            + [
                assumption
                for goal_item in advisory_view.homeowner_goals
                for assumption in goal_item.unsafe_assumptions
            ]
            + [
                assumption
                for item in risk_view.constraint_risk_items
                for assumption in item.unsafe_assumptions
            ]
        )
        source_basis = self._energy_goal_reasoning_basis(
            source_section_keys=source_section_keys,
            goal_refs=goal_refs,
            known_fact_refs=known_fact_refs,
            missing_prerequisite_refs=missing_prerequisite_refs,
            advisory_context_refs=advisory_context_refs,
            provenance_refs=provenance_refs,
            permission_refs=permission_refs,
            professional_boundary_refs=professional_boundary_refs,
            unsafe_assumption_refs=unsafe_assumption_refs,
            blocked_deferred_refs=ENERGY_GOAL_REASONING_DEFERRED_BOUNDARIES,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinAdvisoryContextAssemblyView",
                "TwinConstraintRiskReasoningView",
                "TwinPreRecommendationAdvisoryView",
                "TwinRecommendationEligibilityReadinessView",
                "TwinBasicAdvisoryRecommendationsView",
                "TwinContractorFacingAdvisoryView",
                "TwinHomeownerFacingAdvisoryView",
            ],
        )
        common_unsafe_assumptions = [
            "Treating energy goal reasoning as product selection, final design guidance, goal ranking, proposal generation, economic reasoning, or directive behavior would be unsafe.",
        ]
        recorded_goal_item = self._energy_goal_reasoning_item(
            reasoning_area=TwinEnergyGoalReasoningArea.recorded_homeowner_goals,
            posture="recorded_goal_context_only",
            statement="Recorded homeowner goals are represented only when existing planning context contains recorded design goal fields.",
            recorded_goal_refs=goal_refs,
            missing_prerequisite_gaps=[
                "recorded_design_goal"
            ] if not goal_refs or "recorded_design_goal" in goal_refs else [],
            blocked_deferred=ENERGY_GOAL_REASONING_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions
            + ["Inventing homeowner energy goals would be unsafe."],
            confidence_posture="recorded_goal_context_planning_only",
            basis=self._energy_goal_reasoning_basis(
                source_section_keys=source_section_keys,
                goal_refs=goal_refs,
                derived_from=["TwinAdvisoryContextAssemblyView.homeowner_goals"],
            ),
        )
        known_alignment_item = self._energy_goal_reasoning_item(
            reasoning_area=TwinEnergyGoalReasoningArea.goal_to_known_fact_alignment,
            posture="categorical_traceable_alignment_only",
            statement=(
                "Goal alignment is categorical and traceable to known context facts; it is not numeric, ranked, optimized, or ordered by desirability."
            ),
            recorded_goal_refs=goal_refs,
            known_fact_alignment=known_fact_refs,
            blocked_deferred=["goal_ranking", "solution_ranking", "optimization", "final_design_recommendations"],
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="known_fact_alignment_context_present",
            basis=self._energy_goal_reasoning_basis(
                goal_refs=goal_refs,
                known_fact_refs=known_fact_refs,
                derived_from=[
                    "TwinPlanningContext.sections",
                    "TwinTopologySnapshot.nodes",
                    "TwinTopologySnapshot.edges",
                    "TwinAdvisoryContextAssemblyView.homeowner_goals",
                ],
            ),
        )
        missing_gap_item = self._energy_goal_reasoning_item(
            reasoning_area=TwinEnergyGoalReasoningArea.goal_to_missing_prerequisite_gaps,
            posture="missing_prerequisites_visible_before_goal_reasoning_expansion",
            statement=(
                "Goal-to-missing-prerequisite gaps identify what context is missing before broader goal reasoning can safely expand."
            ),
            recorded_goal_refs=goal_refs,
            missing_prerequisite_gaps=missing_prerequisite_refs,
            blocked_deferred=["final_design_recommendations", "proposal_generation", "optimization"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating missing prerequisite context as resolved would be unsafe."],
            confidence_posture="missing_prerequisites_traceable",
            basis=self._energy_goal_reasoning_basis(
                goal_refs=goal_refs,
                missing_prerequisite_refs=missing_prerequisite_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.missing_prerequisites",
                    "TwinPreRecommendationAdvisoryView.missing_data_before_advice",
                    "TwinBasicAdvisoryRecommendationsView.source_basis.prerequisite_refs",
                ],
            ),
        )
        readiness_item = self._energy_goal_reasoning_item(
            reasoning_area=TwinEnergyGoalReasoningArea.goal_readiness_posture,
            posture="context_readiness_for_goal_reasoning_only",
            statement=(
                "Goal-readiness means context readiness for goal reasoning; it does not mean design readiness, proposal readiness, approval, verification, or recommendation authority."
            ),
            recorded_goal_refs=goal_refs,
            known_fact_alignment=known_fact_refs,
            missing_prerequisite_gaps=missing_prerequisite_refs,
            blocked_deferred=ENERGY_GOAL_REASONING_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="goal_readiness_is_context_readiness_only",
            basis=source_basis,
        )
        provenance_item = self._energy_goal_reasoning_item(
            reasoning_area=TwinEnergyGoalReasoningArea.provenance_basis,
            posture="provenance_visible_not_verification",
            statement="Provenance basis is source context for energy goal reasoning only; provenance presence is not verification.",
            recorded_goal_refs=goal_refs,
            known_fact_alignment=provenance_refs,
            blocked_deferred=["verification_workflow", "final_design_recommendations", "proposal_generation"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating provenance presence as verification would be unsafe."],
            confidence_posture="provenance_context_visible_not_verified",
            basis=self._energy_goal_reasoning_basis(
                goal_refs=goal_refs,
                provenance_refs=provenance_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.provenance_sufficiency",
                    "TwinHomeownerFacingAdvisoryView.provenance_basis_plain_language",
                    "TwinContractorFacingAdvisoryView.provenance_basis",
                ],
            ),
            limitations=ENERGY_GOAL_REASONING_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
        )
        permission_item = self._energy_goal_reasoning_item(
            reasoning_area=TwinEnergyGoalReasoningArea.permission_readiness_metadata,
            posture="permission_readiness_metadata_only",
            statement="Permission-readiness metadata is visible for energy goal reasoning context only and is not authorization or enforcement.",
            recorded_goal_refs=goal_refs,
            known_fact_alignment=permission_refs,
            blocked_deferred=["permission_enforcement", "auth", "rbac_abac", "exports"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating permission-readiness metadata as authorization would be unsafe."],
            confidence_posture="permission_metadata_only_not_authorization",
            basis=self._energy_goal_reasoning_basis(
                goal_refs=goal_refs,
                permission_refs=permission_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.permission_readiness_basis",
                    "TwinHomeownerFacingAdvisoryView.permission_readiness_metadata",
                    "TwinContractorFacingAdvisoryView.permission_readiness_metadata",
                ],
            ),
            limitations=ENERGY_GOAL_REASONING_LIMITATIONS + PERMISSION_READINESS_LIMITATIONS,
        )
        advisory_links_item = self._energy_goal_reasoning_item(
            reasoning_area=TwinEnergyGoalReasoningArea.contractor_homeowner_advisory_context_links,
            posture="advisory_context_links_only",
            statement=(
                "Contractor and homeowner advisory context links connect goal reasoning to existing translation views without creating directives or proposal logic."
            ),
            recorded_goal_refs=goal_refs,
            advisory_context_links=advisory_context_refs,
            blocked_deferred=["contractor_directives", "homeowner_directives", "proposal_generation"],
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="advisory_context_links_present_not_directives",
            basis=self._energy_goal_reasoning_basis(
                goal_refs=goal_refs,
                advisory_context_refs=advisory_context_refs,
                derived_from=[
                    "TwinContractorFacingAdvisoryView",
                    "TwinHomeownerFacingAdvisoryView",
                    "TwinBasicAdvisoryRecommendationsView",
                ],
            ),
        )
        professional_item = self._energy_goal_reasoning_item(
            reasoning_area=TwinEnergyGoalReasoningArea.professional_review_boundaries,
            posture="professional_review_boundary_visible",
            statement="Professional-review boundaries remain visible; this view does not approve goals, designs, proposals, or work.",
            recorded_goal_refs=goal_refs,
            missing_prerequisite_gaps=professional_boundary_refs,
            blocked_deferred=["final_design_recommendations", "proposal_generation", "operational_behavior"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating professional-review boundaries as completed review would be unsafe."],
            confidence_posture="professional_review_required_not_present",
            basis=self._energy_goal_reasoning_basis(
                goal_refs=goal_refs,
                professional_boundary_refs=professional_boundary_refs,
                derived_from=[
                    "TwinConstraintRiskReasoningView.professional_review_boundaries",
                    "TwinRecommendationEligibilityReadinessView.professional_review_boundaries",
                ],
            ),
        )
        unsafe_item = self._energy_goal_reasoning_item(
            reasoning_area=TwinEnergyGoalReasoningArea.unsafe_assumptions,
            posture="unsafe_assumptions_visible",
            statement="Unsafe assumptions remain visible before goal reasoning can be treated as broader recommendation or proposal context.",
            recorded_goal_refs=goal_refs,
            missing_prerequisite_gaps=unsafe_assumption_refs,
            blocked_deferred=ENERGY_GOAL_REASONING_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions + unsafe_assumption_refs,
            confidence_posture="unsafe_assumptions_not_resolved",
            basis=self._energy_goal_reasoning_basis(
                goal_refs=goal_refs,
                unsafe_assumption_refs=unsafe_assumption_refs,
                derived_from=[
                    "TwinAdvisoryContextAssemblyView.homeowner_goals",
                    "TwinConstraintRiskReasoningView.constraint_risk_items",
                    "TwinScenarioComparisonReadinessView.unsafe_assumptions",
                ],
            ),
        )
        deferred_item = self._energy_goal_reasoning_item(
            reasoning_area=TwinEnergyGoalReasoningArea.deferred_goal_optimization_proposal_boundaries,
            posture="goal_optimization_and_proposals_deferred",
            statement="Goal optimization, proposal generation, economic reasoning, ranking, design guidance, and directives remain deferred.",
            recorded_goal_refs=goal_refs,
            blocked_deferred=ENERGY_GOAL_REASONING_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="deferred_goal_boundaries_preserved",
            basis=source_basis,
        )
        items = sorted(
            [
                recorded_goal_item,
                known_alignment_item,
                missing_gap_item,
                readiness_item,
                provenance_item,
                permission_item,
                advisory_links_item,
                professional_item,
                unsafe_item,
                deferred_item,
            ],
            key=self._energy_goal_reasoning_item_sort_key,
        )
        return self._attach_trust_provenance_readiness_summary(TwinEnergyGoalReasoningView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3L energy goal reasoning view built request-time from existing TwinPlanningContext, "
                "topology snapshot, and approved Phase 3 readiness/advisory views; connects recorded homeowner energy goals "
                "to known facts, missing prerequisites, advisory context, and prerequisite-only recommendations. Goal-readiness "
                "means context readiness for goal reasoning and does not mean design readiness, proposal readiness, approval, "
                "verification, or recommendation authority. Goal alignment is categorical and traceable, not numeric, ranked, "
                "optimized, or ordered by desirability. This view does not recommend products, recommend final designs, rank goals, "
                "rank solutions, optimize, simulate, compare scenarios, calculate savings or payback, generate proposals, create "
                "contractor or homeowner directives, perform utility-readiness logic, enforce permissions, export data, persist "
                "state, create graph behavior, create twin_id, or operate devices."
            ),
            source_basis=source_basis,
            reasoning_scope=TwinEnergyGoalReasoningScope(
                limitations=ENERGY_GOAL_REASONING_LIMITATIONS,
            ),
            reasoning_items=items,
            recorded_homeowner_goals=[
                item for item in items if item.reasoning_area == TwinEnergyGoalReasoningArea.recorded_homeowner_goals
            ],
            goal_to_known_fact_alignment=[
                item
                for item in items
                if item.reasoning_area == TwinEnergyGoalReasoningArea.goal_to_known_fact_alignment
            ],
            goal_to_missing_prerequisite_gaps=[
                item
                for item in items
                if item.reasoning_area == TwinEnergyGoalReasoningArea.goal_to_missing_prerequisite_gaps
            ],
            goal_readiness_posture=[
                item for item in items if item.reasoning_area == TwinEnergyGoalReasoningArea.goal_readiness_posture
            ],
            provenance_basis=[
                item for item in items if item.reasoning_area == TwinEnergyGoalReasoningArea.provenance_basis
            ],
            permission_readiness_metadata=[
                item
                for item in items
                if item.reasoning_area == TwinEnergyGoalReasoningArea.permission_readiness_metadata
            ],
            contractor_homeowner_advisory_context_links=[
                item
                for item in items
                if item.reasoning_area == TwinEnergyGoalReasoningArea.contractor_homeowner_advisory_context_links
            ],
            professional_review_boundaries=[
                item
                for item in items
                if item.reasoning_area == TwinEnergyGoalReasoningArea.professional_review_boundaries
            ],
            unsafe_assumptions=[
                item for item in items if item.reasoning_area == TwinEnergyGoalReasoningArea.unsafe_assumptions
            ],
            limitations=ENERGY_GOAL_REASONING_LIMITATIONS,
            deferred_goal_optimization_proposal_boundaries=sorted(
                ENERGY_GOAL_REASONING_DEFERRED_BOUNDARIES
            ),
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A through Phase 3K views, AI grounding, "
                "runtime view foundations, and current /api/* contracts remain unchanged; this is an additive Phase 3L energy goal reasoning view."
            ),
        ))

    def _proposal_readiness_foundation_basis(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_section_keys: Optional[List[str]] = None,
        proposal_readiness_refs: Optional[List[str]] = None,
        goal_refs: Optional[List[str]] = None,
        contractor_context_refs: Optional[List[str]] = None,
        topology_refs: Optional[List[str]] = None,
        missing_prerequisite_refs: Optional[List[str]] = None,
        product_spec_refs: Optional[List[str]] = None,
        risk_refs: Optional[List[str]] = None,
        provenance_refs: Optional[List[str]] = None,
        permission_refs: Optional[List[str]] = None,
        professional_boundary_refs: Optional[List[str]] = None,
        unsafe_assumption_refs: Optional[List[str]] = None,
        blocked_deferred_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinProposalReadinessFoundationBasis:
        return TwinProposalReadinessFoundationBasis(
            source_views=self._sorted_unique(
                source_views
                or [
                    "twin_planning_context",
                    "topology_snapshot",
                    "constraint_risk_reasoning",
                    "recommendation_eligibility_readiness",
                    "basic_advisory_recommendations",
                    "contractor_facing_advisory",
                    "energy_goal_reasoning",
                ]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            proposal_readiness_refs=self._sorted_unique(proposal_readiness_refs or []),
            goal_refs=self._sorted_unique(goal_refs or []),
            contractor_context_refs=self._sorted_unique(contractor_context_refs or []),
            topology_refs=self._sorted_unique(topology_refs or []),
            missing_prerequisite_refs=self._sorted_unique(missing_prerequisite_refs or []),
            product_spec_refs=self._sorted_unique(product_spec_refs or []),
            risk_refs=self._sorted_unique(risk_refs or []),
            provenance_refs=self._sorted_unique(provenance_refs or []),
            permission_refs=self._sorted_unique(permission_refs or []),
            professional_boundary_refs=self._sorted_unique(professional_boundary_refs or []),
            unsafe_assumption_refs=self._sorted_unique(unsafe_assumption_refs or []),
            blocked_deferred_refs=self._sorted_unique(blocked_deferred_refs or []),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=PROPOSAL_READINESS_FOUNDATION_LIMITATIONS,
        )

    def _proposal_readiness_foundation_item(
        self,
        *,
        readiness_area: TwinProposalReadinessFoundationArea,
        posture: str,
        statement: str,
        readiness_refs: Optional[List[str]] = None,
        missing_prerequisites: Optional[List[str]] = None,
        blockers: Optional[List[str]] = None,
        blocked_deferred: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinProposalReadinessFoundationBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinProposalReadinessFoundationItem:
        return TwinProposalReadinessFoundationItem(
            readiness_area=readiness_area,
            posture=posture,
            statement=statement,
            readiness_refs=self._sorted_unique(readiness_refs or []),
            missing_prerequisites=self._sorted_unique(missing_prerequisites or []),
            blockers=self._sorted_unique(blockers or []),
            blocked_deferred=self._sorted_unique(blocked_deferred or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or PROPOSAL_READINESS_FOUNDATION_LIMITATIONS,
        )

    def _proposal_readiness_foundation_item_sort_key(
        self, item: TwinProposalReadinessFoundationItem
    ) -> str:
        return item.readiness_area.value

    def build_proposal_readiness_foundation_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
        advisory_view: Optional[TwinAdvisoryContextAssemblyView] = None,
        risk_view: Optional[TwinConstraintRiskReasoningView] = None,
        scenario_view: Optional[TwinScenarioComparisonReadinessView] = None,
        pre_recommendation_view: Optional[TwinPreRecommendationAdvisoryView] = None,
        eligibility_view: Optional[TwinRecommendationEligibilityReadinessView] = None,
        basic_recommendations_view: Optional[TwinBasicAdvisoryRecommendationsView] = None,
        contractor_advisory_view: Optional[TwinContractorFacingAdvisoryView] = None,
        homeowner_advisory_view: Optional[TwinHomeownerFacingAdvisoryView] = None,
        energy_goal_reasoning_view: Optional[TwinEnergyGoalReasoningView] = None,
    ) -> Optional[TwinProposalReadinessFoundationView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(db, home_id, context=context, snapshot=snapshot)
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db, home_id, context=context, snapshot=snapshot, impact_view=impact_view
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db, home_id, context=context, snapshot=snapshot, impact_view=impact_view, reasoning_view=reasoning_view
        )
        if readiness_view is None:
            return None
        advisory_view = advisory_view or self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None
        risk_view = risk_view or self.build_constraint_risk_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
        )
        if risk_view is None:
            return None
        scenario_view = scenario_view or self.build_scenario_comparison_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
        )
        if scenario_view is None:
            return None
        pre_recommendation_view = pre_recommendation_view or self.build_pre_recommendation_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
        )
        if pre_recommendation_view is None:
            return None
        eligibility_view = eligibility_view or self.build_recommendation_eligibility_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
        )
        if eligibility_view is None:
            return None
        basic_recommendations_view = basic_recommendations_view or self.build_basic_advisory_recommendations_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
        )
        if basic_recommendations_view is None:
            return None
        contractor_advisory_view = contractor_advisory_view or self.build_contractor_facing_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
        )
        if contractor_advisory_view is None:
            return None
        homeowner_advisory_view = homeowner_advisory_view or self.build_homeowner_facing_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
        )
        if homeowner_advisory_view is None:
            return None
        energy_goal_reasoning_view = energy_goal_reasoning_view or self.build_energy_goal_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
            contractor_advisory_view=contractor_advisory_view,
            homeowner_advisory_view=homeowner_advisory_view,
        )
        if energy_goal_reasoning_view is None:
            return None

        source_section_keys = [section.section_key for section in context.sections]
        proposal_readiness_refs = [
            TwinBasicAdvisoryRecommendationCategory.proposal_generation_deferred.value,
            "proposal_context_readiness_only",
            f"phase_3l_goal_readiness_items:{len(energy_goal_reasoning_view.goal_readiness_posture)}",
        ]
        goal_refs = energy_goal_reasoning_view.source_basis.goal_refs
        contractor_context_refs = contractor_advisory_view.source_basis.known_refs + [
            f"contractor_advisory_items:{len(contractor_advisory_view.advisory_items)}"
        ]
        topology_refs = self._sorted_unique(
            [f"topology_node:{node.entity_type}:{node.node_id}" for node in snapshot.nodes]
            + [f"topology_edge:{edge.source_node_id}->{edge.target_node_id}:{edge.relationship}" for edge in snapshot.edges]
            + eligibility_view.source_basis.topology_refs
        )
        missing_prerequisite_refs = self._sorted_unique(
            eligibility_view.missing_prerequisites
            + basic_recommendations_view.source_basis.prerequisite_refs
            + energy_goal_reasoning_view.source_basis.missing_prerequisite_refs
            + [
                item
                for item in contractor_advisory_view.prerequisite_advisory_recommendations
                for item in item.contractor_visible_unknowns
            ]
        )
        product_spec_refs = self._sorted_unique(
            eligibility_view.source_basis.equipment_refs
            + [
                ref
                for item in risk_view.missing_equipment_specs
                for ref in item.missing_inputs + item.observed_constraint_refs
            ]
            + basic_recommendations_view.source_basis.equipment_refs
        )
        risk_refs = self._sorted_unique(
            item.risk_area.value for item in risk_view.constraint_risk_items
        )
        provenance_refs = eligibility_view.source_basis.provenance_refs
        permission_refs = eligibility_view.source_basis.permission_refs
        professional_boundary_refs = self._sorted_unique(
            eligibility_view.source_basis.professional_boundary_refs
            + energy_goal_reasoning_view.source_basis.professional_boundary_refs
        )
        unsafe_assumption_refs = self._sorted_unique(
            energy_goal_reasoning_view.source_basis.unsafe_assumption_refs
            + [
                assumption
                for item in risk_view.constraint_risk_items
                for assumption in item.unsafe_assumptions
            ]
        )
        source_basis = self._proposal_readiness_foundation_basis(
            source_section_keys=source_section_keys,
            proposal_readiness_refs=proposal_readiness_refs,
            goal_refs=goal_refs,
            contractor_context_refs=contractor_context_refs,
            topology_refs=topology_refs,
            missing_prerequisite_refs=missing_prerequisite_refs,
            product_spec_refs=product_spec_refs,
            risk_refs=risk_refs,
            provenance_refs=provenance_refs,
            permission_refs=permission_refs,
            professional_boundary_refs=professional_boundary_refs,
            unsafe_assumption_refs=unsafe_assumption_refs,
            blocked_deferred_refs=PROPOSAL_READINESS_FOUNDATION_DEFERRED_BOUNDARIES,
            derived_from=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinConstraintRiskReasoningView",
                "TwinRecommendationEligibilityReadinessView",
                "TwinBasicAdvisoryRecommendationsView",
                "TwinContractorFacingAdvisoryView",
                "TwinEnergyGoalReasoningView",
            ],
        )
        common_unsafe_assumptions = [
            "Treating proposal-readiness reporting as proposal generation, pricing, quoting, package generation, sales copy, product recommendation, final design recommendation, or CRM workflow would be unsafe.",
        ]
        proposal_item = self._proposal_readiness_foundation_item(
            readiness_area=TwinProposalReadinessFoundationArea.proposal_readiness_posture,
            posture="proposal_readiness_only_not_proposal_generation",
            statement="Proposal-readiness posture reports whether current context can support future proposal generation; it does not generate a proposal.",
            readiness_refs=proposal_readiness_refs,
            missing_prerequisites=missing_prerequisite_refs,
            blockers=PROPOSAL_READINESS_FOUNDATION_DEFERRED_BOUNDARIES,
            blocked_deferred=PROPOSAL_READINESS_FOUNDATION_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="proposal_generation_deferred_readiness_only",
            basis=source_basis,
        )
        goal_item = self._proposal_readiness_foundation_item(
            readiness_area=TwinProposalReadinessFoundationArea.homeowner_goal_readiness,
            posture="goal_context_readiness_for_proposal_context_only",
            statement="Homeowner goal readiness is proposal-context readiness only and is not design readiness, proposal readiness approval, or recommendation authority.",
            readiness_refs=goal_refs,
            missing_prerequisites=energy_goal_reasoning_view.source_basis.missing_prerequisite_refs,
            blocked_deferred=["proposal_generation", "final_design_recommendations", "sales_copy"],
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="goal_context_available_for_readiness_not_proposal",
            basis=self._proposal_readiness_foundation_basis(
                goal_refs=goal_refs,
                missing_prerequisite_refs=energy_goal_reasoning_view.source_basis.missing_prerequisite_refs,
                derived_from=["TwinEnergyGoalReasoningView"],
            ),
        )
        contractor_item = self._proposal_readiness_foundation_item(
            readiness_area=TwinProposalReadinessFoundationArea.contractor_advisory_context_readiness,
            posture="contractor_context_available_not_crm_or_directive",
            statement="Contractor advisory context can inform readiness reporting only; it does not create contractor directives, CRM workflow, bids, quotes, or proposals.",
            readiness_refs=contractor_context_refs,
            missing_prerequisites=contractor_advisory_view.source_basis.unknown_refs,
            blocked_deferred=["contractor_crm_workflow", "quote_generation", "proposal_generation"],
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="contractor_context_visible_not_workflow",
            basis=self._proposal_readiness_foundation_basis(
                contractor_context_refs=contractor_context_refs,
                missing_prerequisite_refs=contractor_advisory_view.source_basis.unknown_refs,
                derived_from=["TwinContractorFacingAdvisoryView"],
            ),
        )
        topology_item = self._proposal_readiness_foundation_item(
            readiness_area=TwinProposalReadinessFoundationArea.topology_readiness,
            posture="topology_readiness_context_only",
            statement="Topology readiness reports whether topology context is available for future proposal context; it is not field-verified topology or design approval.",
            readiness_refs=topology_refs,
            missing_prerequisites=eligibility_view.source_basis.topology_refs,
            blockers=["field_verified_topology"],
            blocked_deferred=["proposal_generation", "final_design_recommendations", "operational_behavior"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating topology readiness as field-verified topology would be unsafe."],
            confidence_posture="topology_context_available_not_verified",
            basis=self._proposal_readiness_foundation_basis(
                topology_refs=topology_refs,
                missing_prerequisite_refs=eligibility_view.source_basis.topology_refs,
                derived_from=["TwinTopologySnapshot", "TwinRecommendationEligibilityReadinessView.topology_sufficiency"],
            ),
        )
        missing_item = self._proposal_readiness_foundation_item(
            readiness_area=TwinProposalReadinessFoundationArea.missing_proposal_prerequisites,
            posture="proposal_prerequisites_missing",
            statement="Missing proposal prerequisites are listed for readiness only; resolving them is outside this view.",
            missing_prerequisites=missing_prerequisite_refs,
            blockers=missing_prerequisite_refs,
            blocked_deferred=PROPOSAL_READINESS_FOUNDATION_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="proposal_prerequisites_not_complete",
            basis=self._proposal_readiness_foundation_basis(
                missing_prerequisite_refs=missing_prerequisite_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.missing_prerequisites",
                    "TwinBasicAdvisoryRecommendationsView.source_basis.prerequisite_refs",
                    "TwinEnergyGoalReasoningView.source_basis.missing_prerequisite_refs",
                ],
            ),
        )
        product_item = self._proposal_readiness_foundation_item(
            readiness_area=TwinProposalReadinessFoundationArea.missing_product_spec_data,
            posture="product_spec_data_incomplete",
            statement="Missing product/spec data can block future proposal context; this view does not recommend, price, select, or package products.",
            readiness_refs=product_spec_refs,
            missing_prerequisites=product_spec_refs or ["source_backed_spec_sheet", "verified_equipment_spec_sources"],
            blockers=product_spec_refs,
            blocked_deferred=["product_recommendations", "pricing", "proposal_generation"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating product/spec readiness as product selection or pricing would be unsafe."],
            confidence_posture="product_spec_prerequisites_visible",
            basis=self._proposal_readiness_foundation_basis(
                product_spec_refs=product_spec_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.equipment_spec_sufficiency",
                    "TwinConstraintRiskReasoningView.missing_equipment_specs",
                    "TwinBasicAdvisoryRecommendationsView.verify_equipment_spec_information",
                ],
            ),
        )
        risk_item = self._proposal_readiness_foundation_item(
            readiness_area=TwinProposalReadinessFoundationArea.risk_provenance_blockers,
            posture="risk_and_provenance_blockers_visible",
            statement="Risk and provenance blockers are basis context only; provenance presence is not verification and risk visibility is not proposal approval.",
            readiness_refs=risk_refs + provenance_refs,
            blockers=risk_refs + provenance_refs,
            blocked_deferred=["proposal_generation", "final_design_recommendations", "quote_generation"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating provenance basis as verification or proposal approval would be unsafe."],
            confidence_posture="risk_provenance_context_visible_not_verified",
            basis=self._proposal_readiness_foundation_basis(
                risk_refs=risk_refs,
                provenance_refs=provenance_refs,
                permission_refs=permission_refs,
                derived_from=[
                    "TwinConstraintRiskReasoningView",
                    "TwinRecommendationEligibilityReadinessView.provenance_sufficiency",
                    "TwinRecommendationEligibilityReadinessView.permission_readiness_basis",
                ],
            ),
            limitations=PROPOSAL_READINESS_FOUNDATION_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
        )
        professional_item = self._proposal_readiness_foundation_item(
            readiness_area=TwinProposalReadinessFoundationArea.professional_review_boundaries,
            posture="professional_review_boundary_visible",
            statement="Professional-review boundaries remain visible and are not completed review, approval, quote authority, or proposal authority.",
            missing_prerequisites=professional_boundary_refs,
            blockers=professional_boundary_refs,
            blocked_deferred=["proposal_generation", "quote_generation", "final_design_recommendations"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating professional-review boundaries as completed review would be unsafe."],
            confidence_posture="professional_review_required_not_present",
            basis=self._proposal_readiness_foundation_basis(
                professional_boundary_refs=professional_boundary_refs,
                derived_from=[
                    "TwinConstraintRiskReasoningView.professional_review_boundaries",
                    "TwinRecommendationEligibilityReadinessView.professional_review_boundaries",
                ],
            ),
        )
        unsafe_item = self._proposal_readiness_foundation_item(
            readiness_area=TwinProposalReadinessFoundationArea.unsafe_assumptions,
            posture="unsafe_assumptions_visible",
            statement="Unsafe assumptions remain visible before proposal readiness can be interpreted beyond planning context.",
            blockers=unsafe_assumption_refs,
            blocked_deferred=PROPOSAL_READINESS_FOUNDATION_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions + unsafe_assumption_refs,
            confidence_posture="unsafe_assumptions_not_resolved",
            basis=self._proposal_readiness_foundation_basis(
                unsafe_assumption_refs=unsafe_assumption_refs,
                derived_from=[
                    "TwinEnergyGoalReasoningView.source_basis.unsafe_assumption_refs",
                    "TwinConstraintRiskReasoningView.constraint_risk_items",
                ],
            ),
        )
        deferred_item = self._proposal_readiness_foundation_item(
            readiness_area=TwinProposalReadinessFoundationArea.deferred_proposal_generation_boundaries,
            posture="proposal_generation_deferred",
            statement="Proposal generation, pricing, quotes, packages, sales copy, CRM workflows, exports, and recommendations remain deferred.",
            blockers=PROPOSAL_READINESS_FOUNDATION_DEFERRED_BOUNDARIES,
            blocked_deferred=PROPOSAL_READINESS_FOUNDATION_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="proposal_boundaries_preserved",
            basis=source_basis,
        )
        items = sorted(
            [
                proposal_item,
                goal_item,
                contractor_item,
                topology_item,
                missing_item,
                product_item,
                risk_item,
                professional_item,
                unsafe_item,
                deferred_item,
            ],
            key=self._proposal_readiness_foundation_item_sort_key,
        )
        return self._attach_trust_provenance_readiness_summary(TwinProposalReadinessFoundationView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3M proposal readiness foundation view built request-time from existing TwinPlanningContext, "
                "topology snapshot, and approved Phase 3 readiness/advisory views; reports proposal-readiness posture only and "
                "does not generate proposals, pricing, quotes, good/better/best packages, sales copy, savings/payback, financing logic, "
                "ranked options, best design selection, product recommendations, final design recommendations, contractor CRM workflows, "
                "exports, permission enforcement, persistence, graph behavior, twin_id, or operational behavior."
            ),
            source_basis=source_basis,
            readiness_scope=TwinProposalReadinessFoundationScope(
                limitations=PROPOSAL_READINESS_FOUNDATION_LIMITATIONS,
            ),
            readiness_items=items,
            proposal_readiness_posture=[
                item for item in items if item.readiness_area == TwinProposalReadinessFoundationArea.proposal_readiness_posture
            ],
            homeowner_goal_readiness=[
                item for item in items if item.readiness_area == TwinProposalReadinessFoundationArea.homeowner_goal_readiness
            ],
            contractor_advisory_context_readiness=[
                item for item in items if item.readiness_area == TwinProposalReadinessFoundationArea.contractor_advisory_context_readiness
            ],
            topology_readiness=[
                item for item in items if item.readiness_area == TwinProposalReadinessFoundationArea.topology_readiness
            ],
            missing_proposal_prerequisites=[
                item for item in items if item.readiness_area == TwinProposalReadinessFoundationArea.missing_proposal_prerequisites
            ],
            missing_product_spec_data=[
                item for item in items if item.readiness_area == TwinProposalReadinessFoundationArea.missing_product_spec_data
            ],
            risk_provenance_blockers=[
                item for item in items if item.readiness_area == TwinProposalReadinessFoundationArea.risk_provenance_blockers
            ],
            professional_review_boundaries=[
                item for item in items if item.readiness_area == TwinProposalReadinessFoundationArea.professional_review_boundaries
            ],
            unsafe_assumptions=[
                item for item in items if item.readiness_area == TwinProposalReadinessFoundationArea.unsafe_assumptions
            ],
            limitations=PROPOSAL_READINESS_FOUNDATION_LIMITATIONS,
            deferred_proposal_generation_boundaries=sorted(
                PROPOSAL_READINESS_FOUNDATION_DEFERRED_BOUNDARIES
            ),
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A through Phase 3L views, AI grounding, "
                "runtime view foundations, and current /api/* contracts remain unchanged; this is an additive Phase 3M proposal readiness view."
            ),
        ))

    def _product_spec_readiness_basis(
        self,
        *,
        source_views: Optional[List[str]] = None,
        source_section_keys: Optional[List[str]] = None,
        product_refs: Optional[List[str]] = None,
        manufacturer_model_refs: Optional[List[str]] = None,
        spec_sheet_refs: Optional[List[str]] = None,
        missing_spec_refs: Optional[List[str]] = None,
        source_trust_refs: Optional[List[str]] = None,
        compatibility_prerequisite_refs: Optional[List[str]] = None,
        equipment_gap_refs: Optional[List[str]] = None,
        professional_boundary_refs: Optional[List[str]] = None,
        unsafe_assumption_refs: Optional[List[str]] = None,
        blocked_deferred_refs: Optional[List[str]] = None,
        derived_from: Optional[List[str]] = None,
    ) -> TwinProductSpecReadinessBasis:
        return TwinProductSpecReadinessBasis(
            source_views=self._sorted_unique(
                source_views
                or [
                    "twin_planning_context",
                    "topology_snapshot",
                    "constraint_risk_reasoning",
                    "recommendation_eligibility_readiness",
                    "basic_advisory_recommendations",
                    "proposal_readiness_foundation",
                ]
            ),
            source_section_keys=self._sorted_unique(source_section_keys or []),
            product_refs=self._sorted_unique(product_refs or []),
            manufacturer_model_refs=self._sorted_unique(manufacturer_model_refs or []),
            spec_sheet_refs=self._sorted_unique(spec_sheet_refs or []),
            missing_spec_refs=self._sorted_unique(missing_spec_refs or []),
            source_trust_refs=self._sorted_unique(source_trust_refs or []),
            compatibility_prerequisite_refs=self._sorted_unique(compatibility_prerequisite_refs or []),
            equipment_gap_refs=self._sorted_unique(equipment_gap_refs or []),
            professional_boundary_refs=self._sorted_unique(professional_boundary_refs or []),
            unsafe_assumption_refs=self._sorted_unique(unsafe_assumption_refs or []),
            blocked_deferred_refs=self._sorted_unique(blocked_deferred_refs or []),
            derived_from=self._sorted_unique(derived_from or []),
            limitations=PRODUCT_SPEC_READINESS_LIMITATIONS,
        )

    def _product_spec_readiness_item(
        self,
        *,
        readiness_area: TwinProductSpecReadinessArea,
        posture: str,
        statement: str,
        readiness_refs: Optional[List[str]] = None,
        missing_spec_refs: Optional[List[str]] = None,
        blockers: Optional[List[str]] = None,
        blocked_deferred: Optional[List[str]] = None,
        unsafe_assumptions: Optional[List[str]] = None,
        confidence_posture: str,
        basis: TwinProductSpecReadinessBasis,
        limitations: Optional[List[str]] = None,
    ) -> TwinProductSpecReadinessItem:
        return TwinProductSpecReadinessItem(
            readiness_area=readiness_area,
            posture=posture,
            statement=statement,
            readiness_refs=self._sorted_unique(readiness_refs or []),
            missing_spec_refs=self._sorted_unique(missing_spec_refs or []),
            blockers=self._sorted_unique(blockers or []),
            blocked_deferred=self._sorted_unique(blocked_deferred or []),
            unsafe_assumptions=self._sorted_unique(unsafe_assumptions or []),
            confidence_posture=confidence_posture,
            basis=basis,
            limitations=limitations or PRODUCT_SPEC_READINESS_LIMITATIONS,
        )

    def _product_spec_readiness_item_sort_key(
        self, item: TwinProductSpecReadinessItem
    ) -> str:
        return item.readiness_area.value

    def build_product_spec_readiness_view(
        self,
        db,
        home_id: str,
        *,
        context: Optional[TwinPlanningContext] = None,
        snapshot: Optional[TwinTopologySnapshot] = None,
        impact_view: Optional[TwinDependencyImpactReadinessView] = None,
        reasoning_view: Optional[TwinDependencyReasoningView] = None,
        readiness_view: Optional[TwinPlanningIntelligenceReadinessView] = None,
        advisory_view: Optional[TwinAdvisoryContextAssemblyView] = None,
        risk_view: Optional[TwinConstraintRiskReasoningView] = None,
        scenario_view: Optional[TwinScenarioComparisonReadinessView] = None,
        pre_recommendation_view: Optional[TwinPreRecommendationAdvisoryView] = None,
        eligibility_view: Optional[TwinRecommendationEligibilityReadinessView] = None,
        basic_recommendations_view: Optional[TwinBasicAdvisoryRecommendationsView] = None,
        contractor_advisory_view: Optional[TwinContractorFacingAdvisoryView] = None,
        homeowner_advisory_view: Optional[TwinHomeownerFacingAdvisoryView] = None,
        energy_goal_reasoning_view: Optional[TwinEnergyGoalReasoningView] = None,
        proposal_readiness_view: Optional[TwinProposalReadinessFoundationView] = None,
    ) -> Optional[TwinProductSpecReadinessView]:
        context = context or self.build(db, home_id)
        if context is None:
            return None
        snapshot = snapshot or self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None
        impact_view = impact_view or self.build_dependency_impact_readiness_view(db, home_id, context=context, snapshot=snapshot)
        if impact_view is None:
            return None
        reasoning_view = reasoning_view or self.build_dependency_reasoning_view(
            db, home_id, context=context, snapshot=snapshot, impact_view=impact_view
        )
        if reasoning_view is None:
            return None
        readiness_view = readiness_view or self.build_planning_intelligence_readiness_view(
            db, home_id, context=context, snapshot=snapshot, impact_view=impact_view, reasoning_view=reasoning_view
        )
        if readiness_view is None:
            return None
        advisory_view = advisory_view or self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None
        risk_view = risk_view or self.build_constraint_risk_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
        )
        if risk_view is None:
            return None
        scenario_view = scenario_view or self.build_scenario_comparison_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
        )
        if scenario_view is None:
            return None
        pre_recommendation_view = pre_recommendation_view or self.build_pre_recommendation_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
        )
        if pre_recommendation_view is None:
            return None
        eligibility_view = eligibility_view or self.build_recommendation_eligibility_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
        )
        if eligibility_view is None:
            return None
        basic_recommendations_view = basic_recommendations_view or self.build_basic_advisory_recommendations_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
        )
        if basic_recommendations_view is None:
            return None
        proposal_readiness_view = proposal_readiness_view or self.build_proposal_readiness_foundation_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
            contractor_advisory_view=contractor_advisory_view,
            homeowner_advisory_view=homeowner_advisory_view,
            energy_goal_reasoning_view=energy_goal_reasoning_view,
        )
        if proposal_readiness_view is None:
            return None

        section_records = self._all_context_records_with_sections(context)
        product_records = [
            (section_key, record)
            for section_key, record in section_records
            if record.entity_type in {"equipment_product", "design_equipment"}
        ]
        source_section_keys = [section.section_key for section in context.sections]
        product_refs = self._sorted_unique(
            f"{record.entity_type}:{record.entity_id or 'unknown'}" for _section_key, record in product_records
        )
        manufacturer_model_refs = self._sorted_unique(
            f"{record.entity_type}:{record.entity_id or 'unknown'}:manufacturer_model:{record.record.get('manufacturer') or 'missing'}:{record.record.get('model') or 'missing'}"
            for _section_key, record in product_records
        )
        spec_sheet_refs = self._sorted_unique(
            f"{record.entity_type}:{record.entity_id or 'unknown'}:specs_present"
            for _section_key, record in product_records
            if record.record.get("specs")
        )
        missing_spec_refs = self._sorted_unique(
            [
                f"{record.entity_type}:{record.entity_id or 'unknown'}:{field}"
                for _section_key, record in product_records
                for field in record.missing_fields
            ]
            + [
                f"{record.entity_type}:{record.entity_id or 'unknown'}:specs"
                for _section_key, record in product_records
                if not record.record.get("specs")
            ]
        )
        source_trust_refs = self._sorted_unique(
            [
                f"{record.entity_type}:{record.entity_id or 'unknown'}:origin:{record.data_origin}"
                for _section_key, record in product_records
            ]
            + [
                self._provenance_gap_ref(gap)
                for _section_key, record in product_records
                for gap in record.provenance_gaps
            ]
        )
        compatibility_prerequisite_refs = self._sorted_unique(
            eligibility_view.source_basis.equipment_refs
            + basic_recommendations_view.source_basis.equipment_refs
            + [
                TwinBasicAdvisoryRecommendationCategory.verify_equipment_spec_information.value,
                TwinBasicAdvisoryRecommendationCategory.request_spec_sheet.value,
                "complete_equipment_specs",
                "verified_equipment_spec_sources",
            ]
        )
        equipment_gap_refs = self._sorted_unique(
            [
                ref
                for item in risk_view.missing_equipment_specs
                for ref in item.missing_inputs + item.observed_constraint_refs
            ]
            + proposal_readiness_view.source_basis.product_spec_refs
        )
        professional_boundary_refs = self._sorted_unique(
            eligibility_view.source_basis.professional_boundary_refs
            + proposal_readiness_view.source_basis.professional_boundary_refs
        )
        unsafe_assumption_refs = self._sorted_unique(
            proposal_readiness_view.source_basis.unsafe_assumption_refs
            + [
                assumption
                for item in risk_view.missing_equipment_specs
                for assumption in item.unsafe_assumptions
            ]
        )
        deferred_refs = self._sorted_unique(
            PRODUCT_SPEC_READINESS_COMPATIBILITY_DEFERRED_BOUNDARIES
            + PRODUCT_SPEC_READINESS_VENDOR_DEFERRED_BOUNDARIES
        )
        source_basis = self._product_spec_readiness_basis(
            source_section_keys=source_section_keys,
            product_refs=product_refs,
            manufacturer_model_refs=manufacturer_model_refs,
            spec_sheet_refs=spec_sheet_refs,
            missing_spec_refs=missing_spec_refs,
            source_trust_refs=source_trust_refs,
            compatibility_prerequisite_refs=compatibility_prerequisite_refs,
            equipment_gap_refs=equipment_gap_refs,
            professional_boundary_refs=professional_boundary_refs,
            unsafe_assumption_refs=unsafe_assumption_refs,
            blocked_deferred_refs=deferred_refs,
            derived_from=[
                "TwinPlanningContext.equipment_products",
                "TwinPlanningContext.design_equipment",
                "TwinConstraintRiskReasoningView.missing_equipment_specs",
                "TwinRecommendationEligibilityReadinessView.equipment_spec_sufficiency",
                "TwinBasicAdvisoryRecommendationsView",
                "TwinProposalReadinessFoundationView",
            ],
        )
        common_unsafe_assumptions = [
            "Treating product/spec readiness as autonomous spec engineering, compatibility conclusions, product selection, product ranking, pricing, vendor procurement, or marketplace behavior would be unsafe.",
        ]
        identity_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.product_identity_readiness,
            posture="product_identity_context_visible",
            statement="Product identity readiness reports whether product/equipment records exist; it does not select or recommend products.",
            readiness_refs=product_refs,
            missing_spec_refs=["equipment_product_records"] if not product_refs else [],
            blocked_deferred=["product_recommendations", "equipment_selection", "product_ranking"],
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="product_identity_context_available" if product_refs else "product_identity_context_missing",
            basis=self._product_spec_readiness_basis(
                product_refs=product_refs,
                derived_from=["TwinPlanningContext.equipment_products", "TwinPlanningContext.design_equipment"],
            ),
        )
        manufacturer_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.manufacturer_model_readiness,
            posture="manufacturer_model_context_visible",
            statement="Manufacturer/model readiness reports available identity fields only and does not imply compatibility or equipment selection.",
            readiness_refs=manufacturer_model_refs,
            missing_spec_refs=[ref for ref in manufacturer_model_refs if ":missing" in ref],
            blocked_deferred=["compatibility_engine", "equipment_selection", "product_recommendations"],
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="manufacturer_model_context_planning_only",
            basis=self._product_spec_readiness_basis(
                manufacturer_model_refs=manufacturer_model_refs,
                derived_from=["TwinPlanningContextRecord.record.manufacturer", "TwinPlanningContextRecord.record.model"],
            ),
        )
        spec_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.spec_sheet_provenance,
            posture="spec_sheet_provenance_context_only",
            statement="Spec-sheet provenance is source context only and is not verification, engineering approval, or autonomous spec interpretation.",
            readiness_refs=spec_sheet_refs + source_trust_refs,
            missing_spec_refs=missing_spec_refs,
            blockers=["verified_equipment_spec_sources"] if missing_spec_refs else [],
            blocked_deferred=["autonomous_spec_engineering", "compatibility_engine", "product_recommendations"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating spec-sheet provenance as verified engineering data would be unsafe."],
            confidence_posture="spec_sheet_provenance_visible_not_verified",
            basis=self._product_spec_readiness_basis(
                spec_sheet_refs=spec_sheet_refs,
                missing_spec_refs=missing_spec_refs,
                source_trust_refs=source_trust_refs,
                derived_from=["TwinPlanningContextRecord.record.specs", "TwinPlanningContextRecord.provenance_gaps"],
            ),
            limitations=PRODUCT_SPEC_READINESS_LIMITATIONS + PROVENANCE_GAP_LIMITATIONS,
        )
        missing_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.missing_spec_fields,
            posture="missing_spec_fields_visible",
            statement="Missing spec fields are reported as prerequisites only and are not compatibility failures or product recommendations.",
            missing_spec_refs=missing_spec_refs,
            blockers=missing_spec_refs,
            blocked_deferred=["compatibility_engine", "product_recommendations", "proposal_generation"],
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="missing_specs_require_source_backing",
            basis=self._product_spec_readiness_basis(
                missing_spec_refs=missing_spec_refs,
                derived_from=["TwinPlanningContextRecord.missing_fields", "TwinPlanningContextRecord.record.specs"],
            ),
        )
        trust_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.source_trust_indicators,
            posture="source_trust_context_visible",
            statement="Source/trust indicators are readiness context only and do not verify product data or certify compatibility.",
            readiness_refs=source_trust_refs,
            blockers=[ref for ref in source_trust_refs if "provenance_gap" in ref],
            blocked_deferred=["autonomous_spec_engineering", "compatibility_engine", "vendor_marketplace_behavior"],
            unsafe_assumptions=common_unsafe_assumptions
            + ["Treating source/trust indicators as verified specs would be unsafe."],
            confidence_posture="source_trust_visible_not_verified",
            basis=self._product_spec_readiness_basis(
                source_trust_refs=source_trust_refs,
                derived_from=["TwinPlanningContextRecord.data_origin", "TwinPlanningContextRecord.provenance_gaps"],
            ),
        )
        compatibility_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.compatibility_prerequisites,
            posture="compatibility_prerequisites_visible_engine_deferred",
            statement="Compatibility prerequisites are visible for future readiness only; no compatibility engine or autonomous engineering is implemented.",
            readiness_refs=compatibility_prerequisite_refs,
            missing_spec_refs=missing_spec_refs,
            blockers=compatibility_prerequisite_refs,
            blocked_deferred=PRODUCT_SPEC_READINESS_COMPATIBILITY_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="compatibility_engine_deferred",
            basis=self._product_spec_readiness_basis(
                compatibility_prerequisite_refs=compatibility_prerequisite_refs,
                missing_spec_refs=missing_spec_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.equipment_spec_sufficiency",
                    "TwinBasicAdvisoryRecommendationsView.verify_equipment_spec_information",
                    "TwinBasicAdvisoryRecommendationsView.request_spec_sheet",
                ],
            ),
        )
        gap_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.equipment_spec_gaps,
            posture="equipment_spec_gaps_visible",
            statement="Equipment/spec gaps are reported for readiness only and do not select equipment or produce compatibility conclusions.",
            readiness_refs=equipment_gap_refs,
            missing_spec_refs=equipment_gap_refs,
            blockers=equipment_gap_refs,
            blocked_deferred=["equipment_selection", "compatibility_engine", "product_recommendations"],
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="equipment_spec_gaps_not_resolved",
            basis=self._product_spec_readiness_basis(
                equipment_gap_refs=equipment_gap_refs,
                derived_from=[
                    "TwinConstraintRiskReasoningView.missing_equipment_specs",
                    "TwinProposalReadinessFoundationView.missing_product_spec_data",
                ],
            ),
        )
        professional_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.professional_review_boundaries,
            posture="professional_review_boundary_visible",
            statement="Professional-review boundaries remain visible and are not completed review, compatibility approval, or product approval.",
            blockers=professional_boundary_refs,
            blocked_deferred=["compatibility_engine", "equipment_selection", "proposal_generation"],
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="professional_review_required_not_present",
            basis=self._product_spec_readiness_basis(
                professional_boundary_refs=professional_boundary_refs,
                derived_from=[
                    "TwinRecommendationEligibilityReadinessView.professional_review_boundaries",
                    "TwinProposalReadinessFoundationView.professional_review_boundaries",
                ],
            ),
        )
        unsafe_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.unsafe_assumptions,
            posture="unsafe_assumptions_visible",
            statement="Unsafe assumptions remain visible before product/spec readiness can be used by future spec reasoning.",
            blockers=unsafe_assumption_refs,
            blocked_deferred=deferred_refs,
            unsafe_assumptions=common_unsafe_assumptions + unsafe_assumption_refs,
            confidence_posture="unsafe_assumptions_not_resolved",
            basis=self._product_spec_readiness_basis(
                unsafe_assumption_refs=unsafe_assumption_refs,
                derived_from=[
                    "TwinConstraintRiskReasoningView.missing_equipment_specs",
                    "TwinProposalReadinessFoundationView.unsafe_assumptions",
                ],
            ),
        )
        compatibility_deferred_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.deferred_compatibility_engine_boundaries,
            posture="compatibility_engine_deferred",
            statement="Autonomous spec engineering, compatibility engines, product recommendations, equipment selection, product ranking, proposals, and pricing remain deferred.",
            blockers=PRODUCT_SPEC_READINESS_COMPATIBILITY_DEFERRED_BOUNDARIES,
            blocked_deferred=PRODUCT_SPEC_READINESS_COMPATIBILITY_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="compatibility_boundaries_preserved",
            basis=source_basis,
        )
        vendor_deferred_item = self._product_spec_readiness_item(
            readiness_area=TwinProductSpecReadinessArea.deferred_vendor_procurement_boundaries,
            posture="vendor_procurement_deferred",
            statement="Vendor scraping, supplier integrations, marketplace behavior, procurement logic, exports, persistence, and operational behavior remain deferred.",
            blockers=PRODUCT_SPEC_READINESS_VENDOR_DEFERRED_BOUNDARIES,
            blocked_deferred=PRODUCT_SPEC_READINESS_VENDOR_DEFERRED_BOUNDARIES,
            unsafe_assumptions=common_unsafe_assumptions,
            confidence_posture="vendor_procurement_boundaries_preserved",
            basis=source_basis,
        )
        items = sorted(
            [
                identity_item,
                manufacturer_item,
                spec_item,
                missing_item,
                trust_item,
                compatibility_item,
                gap_item,
                professional_item,
                unsafe_item,
                compatibility_deferred_item,
                vendor_deferred_item,
            ],
            key=self._product_spec_readiness_item_sort_key,
        )
        return self._attach_trust_provenance_readiness_summary(TwinProductSpecReadinessView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 3N product/spec readiness view built request-time from existing TwinPlanningContext, topology snapshot, "
                "and approved Phase 3 readiness/advisory views; reports whether product/spec context is available, missing, traceable, or blocked. "
                "It does not perform autonomous engineering from spec sheets, create a compatibility engine, recommend products, select equipment, "
                "rank products, generate proposals, generate pricing, scrape vendors, integrate supplier data, create marketplace behavior, "
                "create procurement logic, enforce permissions, persist state, export data, create graph behavior, create twin_id, or operate devices."
            ),
            source_basis=source_basis,
            readiness_scope=TwinProductSpecReadinessScope(
                limitations=PRODUCT_SPEC_READINESS_LIMITATIONS,
            ),
            readiness_items=items,
            product_identity_readiness=[
                item for item in items if item.readiness_area == TwinProductSpecReadinessArea.product_identity_readiness
            ],
            manufacturer_model_readiness=[
                item for item in items if item.readiness_area == TwinProductSpecReadinessArea.manufacturer_model_readiness
            ],
            spec_sheet_provenance=[
                item for item in items if item.readiness_area == TwinProductSpecReadinessArea.spec_sheet_provenance
            ],
            missing_spec_fields=[
                item for item in items if item.readiness_area == TwinProductSpecReadinessArea.missing_spec_fields
            ],
            source_trust_indicators=[
                item for item in items if item.readiness_area == TwinProductSpecReadinessArea.source_trust_indicators
            ],
            compatibility_prerequisites=[
                item for item in items if item.readiness_area == TwinProductSpecReadinessArea.compatibility_prerequisites
            ],
            equipment_spec_gaps=[
                item for item in items if item.readiness_area == TwinProductSpecReadinessArea.equipment_spec_gaps
            ],
            professional_review_boundaries=[
                item for item in items if item.readiness_area == TwinProductSpecReadinessArea.professional_review_boundaries
            ],
            unsafe_assumptions=[
                item for item in items if item.readiness_area == TwinProductSpecReadinessArea.unsafe_assumptions
            ],
            limitations=PRODUCT_SPEC_READINESS_LIMITATIONS,
            deferred_compatibility_engine_boundaries=sorted(
                PRODUCT_SPEC_READINESS_COMPATIBILITY_DEFERRED_BOUNDARIES
            ),
            deferred_vendor_procurement_boundaries=sorted(
                PRODUCT_SPEC_READINESS_VENDOR_DEFERRED_BOUNDARIES
            ),
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 3A through Phase 3M views, AI grounding, "
                "runtime view foundations, and current /api/* contracts remain unchanged; this is an additive Phase 3N product/spec readiness view."
            ),
        ))

    def _record_ref(self, section_key: str, record: TwinPlanningContextRecord) -> str:
        return f"{section_key}:{record.entity_type}:{record.entity_id or record.label}"

    def _shared_compatibility_context_evidence(
        self,
        context: TwinPlanningContext,
    ) -> Dict[str, List[str]]:
        evidence: Dict[str, List[str]] = {
            "battery": [],
            "essential_loads": [],
            "generator": [],
            "gateway_or_transfer": [],
            "load_management": [],
            "panel_context": [],
            "preferred_loads": [],
            "service_upgrade": [],
            "solar": [],
            "spare_spaces": [],
            "whole_home_backup": [],
        }
        for section in context.sections:
            for record in section.records:
                record_ref = self._record_ref(section.section_key, record)
                payload = record.record or {}
                product_type = str(payload.get("product_type", "")).lower()
                role = str(payload.get("role_in_system", "")).lower()
                design_goal = str(payload.get("design_goal", "")).lower()
                architecture_type = str(payload.get("architecture_type", "")).lower()
                backup_priority = str(payload.get("backup_priority", "")).lower()

                if "solar" in product_type or "solar" in role:
                    evidence["solar"].append(record_ref)
                if "battery" in product_type or "battery" in role or "storage" in role:
                    evidence["battery"].append(record_ref)
                if "generator" in product_type or "generator" in role:
                    evidence["generator"].append(record_ref)
                if (
                    "gateway" in product_type
                    or "transfer" in role
                    or "interlock" in role
                    or "gateway" in role
                ):
                    evidence["gateway_or_transfer"].append(record_ref)
                if "smart_panel" in product_type or "load_management" in role:
                    evidence["load_management"].append(record_ref)
                if backup_priority == "essential":
                    evidence["essential_loads"].append(record_ref)
                if backup_priority == "preferred":
                    evidence["preferred_loads"].append(record_ref)
                if record.entity_type == "electrical_panel":
                    evidence["panel_context"].append(record_ref)
                    spaces = payload.get("breaker_spaces_available")
                    if isinstance(spaces, int) and spaces > 0:
                        evidence["spare_spaces"].append(record_ref)
                if record.entity_type == "home":
                    service_size = payload.get("service_size")
                    if isinstance(service_size, int) and service_size < 200:
                        evidence["service_upgrade"].append(record_ref)
                if "whole_home" in design_goal or "whole_home" in architecture_type:
                    evidence["whole_home_backup"].append(record_ref)
        return {
            key: self._sorted_unique(values)
            for key, values in evidence.items()
        }

    def _shared_compatibility_basis(
        self,
        *,
        source_refs: Optional[List[str]] = None,
        source_ref_categories: Optional[Dict[str, List[str]]] = None,
        topology_refs: Optional[List[str]] = None,
        readiness_refs: Optional[List[str]] = None,
        confirmation_gate_refs: Optional[List[str]] = None,
        install_complexity_signal_refs: Optional[List[str]] = None,
        exchange_section_refs: Optional[List[str]] = None,
        missing_information_refs: Optional[List[str]] = None,
        basis_quality: str = "request_time_derived_from_existing_context",
        basis_notes: Optional[List[str]] = None,
    ) -> TwinSharedCompatibilityBasis:
        return TwinSharedCompatibilityBasis(
            source_views=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "ContractorConfirmationGateProjectionView",
                "ContractorInstallComplexityView",
                "PlanningExchangeObjectView",
            ],
            source_fields=[
                "TwinPlanningContext.sections",
                "TwinTopologySnapshot.lifecycle_readiness_hints",
                "TwinTopologySnapshot.missing_readiness_indicators",
                "ContractorConfirmationGateProjectionView.gates",
                "ContractorInstallComplexityView.signals",
                "PlanningExchangeObjectView.section_mappings",
                "PlanningExchangeObjectView.missing_information",
            ],
            source_refs=self._sorted_unique(source_refs or []),
            source_ref_categories={
                key: self._sorted_unique(values)
                for key, values in (source_ref_categories or {}).items()
                if values
            },
            topology_refs=self._sorted_unique(topology_refs or []),
            readiness_refs=self._sorted_unique(readiness_refs or []),
            confirmation_gate_refs=self._sorted_unique(confirmation_gate_refs or []),
            install_complexity_signal_refs=self._sorted_unique(install_complexity_signal_refs or []),
            exchange_section_refs=self._sorted_unique(exchange_section_refs or []),
            missing_information_refs=self._sorted_unique(missing_information_refs or []),
            basis_quality=basis_quality,
            request_time_derived=True,
            verified_fact_claim_present=False,
            basis_notes=self._sorted_unique(
                basis_notes
                or [
                    "Basis is assembled from existing request-time planning views.",
                    "Basis references are not field verification, contractor confirmation, AHJ approval, or utility approval.",
                ]
            ),
            derived_from=[
                "existing_home_id_anchored_twin_planning_context",
                "phase_2c_topology_readiness_outputs",
                "phase_5_confirmation_gate_projection",
                "phase_5_install_complexity_signals",
                "phase_6_planning_exchange_object",
            ],
            limitations=SHARED_COMPATIBILITY_LIMITATIONS,
        )

    def _shared_compatibility_status(
        self,
        *,
        path_key: str,
        present_features: List[str],
        missing_features: List[str],
        gate_refs: List[str],
        blocked_gate_refs: List[str],
    ) -> TwinSharedCompatibilityStatus:
        if path_key in {"pv_battery_whole_home_backup", "pv_generator_interlock"} and blocked_gate_refs:
            return TwinSharedCompatibilityStatus.blocked
        if path_key == "pv_only" and not missing_features:
            return TwinSharedCompatibilityStatus.likely_compatible
        if path_key == "service_upgrade_likely":
            return TwinSharedCompatibilityStatus.unknown
        if path_key == "load_management" and missing_features:
            return TwinSharedCompatibilityStatus.unknown
        if path_key == "existing_panel_reuse" and not missing_features:
            return TwinSharedCompatibilityStatus.compatible
        if not missing_features and gate_refs:
            return TwinSharedCompatibilityStatus.requires_contractor_confirmation
        if present_features and missing_features:
            return TwinSharedCompatibilityStatus.likely_compatible
        return TwinSharedCompatibilityStatus.unknown

    def _shared_compatibility_reason(
        self,
        *,
        path_label: str,
        status: TwinSharedCompatibilityStatus,
        missing_features: List[str],
        blocked_gate_refs: List[str],
    ) -> str:
        if status == TwinSharedCompatibilityStatus.compatible:
            return (
                f"{path_label} has current planning evidence for the required path ingredients, but it still remains "
                "planning-only and subject to contractor confirmation before design use."
            )
        if status == TwinSharedCompatibilityStatus.likely_compatible:
            return (
                f"{path_label} has partial current planning evidence, but missing information prevents a stronger "
                "compatibility classification."
            )
        if status == TwinSharedCompatibilityStatus.blocked:
            return (
                f"{path_label} is blocked in this view because authority-dependent or final-review gates remain unresolved: "
                f"{', '.join(blocked_gate_refs)}."
            )
        if status == TwinSharedCompatibilityStatus.requires_contractor_confirmation:
            return (
                f"{path_label} has relevant planning evidence but depends on contractor, professional, AHJ, utility, "
                "or field confirmation before it can be used for design work."
            )
        return (
            f"{path_label} cannot be classified from current planning data without assuming missing inputs: "
            f"{', '.join(missing_features)}."
        )

    def _shared_compatibility_path_status_groups(
        self,
        paths: List[TwinSharedCompatibilityPath],
    ) -> Dict[str, List[str]]:
        groups = {
            status.value: []
            for status in TwinSharedCompatibilityStatus
        }
        for path in paths:
            groups[path.status.value].append(path.path_key)
        return {
            status: self._sorted_unique(path_keys)
            for status, path_keys in groups.items()
        }

    def _shared_compatibility_audience_interpretation(
        self,
        *,
        audience: str,
        path_label: Optional[str] = None,
        status: Optional[TwinSharedCompatibilityStatus] = None,
        missing_information: Optional[List[str]] = None,
        required_confirmations: Optional[List[str]] = None,
        blockers: Optional[List[str]] = None,
        paths: Optional[List[TwinSharedCompatibilityPath]] = None,
    ) -> TwinSharedCompatibilityAudienceInterpretation:
        missing = self._sorted_unique(missing_information or [])
        confirmations = self._sorted_unique(required_confirmations or [])
        blocker_refs = self._sorted_unique(blockers or [])
        status_groups = self._shared_compatibility_path_status_groups(paths or [])
        if path_label and status:
            if audience == "homeowner":
                summary = (
                    f"{path_label} currently appears as {status.value}; this is planning-only and needs the listed "
                    "contractor or authority review before design decisions."
                )
                next_steps = [
                    "Ask a contractor to review the listed confirmation gates.",
                    "Resolve missing information before treating this path as design-ready.",
                ]
            else:
                summary = (
                    f"{path_label} is classified as {status.value} from current planning context, missing inputs, "
                    "and confirmation gates."
                )
                next_steps = [
                    "Review open confirmation gates as review topics only.",
                    "Validate source-backed specs, nameplates, site conditions, routing, load assumptions, and authority requirements before design use.",
                ]
        elif audience == "homeowner":
            summary = (
                "Shared compatibility summarizes which paths appear possible, uncertain, blocked, or contractor-review dependent from current planning data."
            )
            next_steps = [
                "Use the summary to prepare contractor questions.",
                "Do not treat any path as approved or field-verified until qualified review is complete.",
            ]
        else:
            summary = (
                "Shared compatibility groups install paths by planning-only status and exposes basis, missing inputs, blockers, and confirmation gates for review preparation."
            )
            next_steps = [
                "Review confirmation gates before relying on any path for scoping.",
                "Treat AHJ/utility, product, nameplate, routing, load, disconnect/OCPD, and field conditions as unresolved review dependencies.",
            ]
        return TwinSharedCompatibilityAudienceInterpretation(
            audience=audience,
            interpretation_scope=(
                "homeowner_safe_planning_summary"
                if audience == "homeowner"
                else "contractor_facing_review_metadata"
            ),
            summary=summary,
            path_status_groups=status_groups,
            next_verification_steps=self._sorted_unique(next_steps + confirmations),
            assumptions=[
                "Interpretation is derived from the same shared compatibility object.",
                "Interpretation metadata does not enforce roles, permissions, sharing, exports, or authorization.",
            ],
            limitations=SHARED_COMPATIBILITY_LIMITATIONS
            + [
                "Audience interpretation is wording metadata only, not a separate permissioned view.",
                "No auth, sharing, export, or permission enforcement is implemented.",
            ],
        )

    def _shared_compatibility_summary(
        self,
        paths: List[TwinSharedCompatibilityPath],
        *,
        missing_information: List[str],
        required_confirmations: List[str],
        contractor_confirmation_gates: List[str],
    ) -> TwinSharedCompatibilitySummary:
        status_counts = Counter(path.status.value for path in paths)
        path_keys_by_status = {
            status: [
                path.path_key
                for path in paths
                if path.status == status
            ]
            for status in TwinSharedCompatibilityStatus
        }
        blocked_or_uncertain = (
            path_keys_by_status[TwinSharedCompatibilityStatus.blocked]
            + path_keys_by_status[TwinSharedCompatibilityStatus.unknown]
            + path_keys_by_status[TwinSharedCompatibilityStatus.requires_contractor_confirmation]
        )
        return TwinSharedCompatibilitySummary(
            total_paths=len(paths),
            status_counts={
                status.value: status_counts.get(status.value, 0)
                for status in TwinSharedCompatibilityStatus
            },
            compatible_path_keys=self._sorted_unique(path_keys_by_status[TwinSharedCompatibilityStatus.compatible]),
            likely_compatible_path_keys=self._sorted_unique(
                path_keys_by_status[TwinSharedCompatibilityStatus.likely_compatible]
            ),
            blocked_path_keys=self._sorted_unique(path_keys_by_status[TwinSharedCompatibilityStatus.blocked]),
            unknown_path_keys=self._sorted_unique(path_keys_by_status[TwinSharedCompatibilityStatus.unknown]),
            confirmation_required_path_keys=self._sorted_unique(
                path_keys_by_status[TwinSharedCompatibilityStatus.requires_contractor_confirmation]
            ),
            blocked_or_uncertain_path_keys=self._sorted_unique(blocked_or_uncertain),
            missing_information_count=len(self._sorted_unique(missing_information)),
            required_confirmation_count=len(self._sorted_unique(required_confirmations)),
            contractor_confirmation_gate_count=len(self._sorted_unique(contractor_confirmation_gates)),
            summary_boundary_note=(
                "Summary counts are planning-only rollups and are not ranking, approval, readiness certification, "
                "field verification, permit readiness, or final design guidance."
            ),
        )

    def _shared_compatibility_path(
        self,
        *,
        path_key: str,
        path_label: str,
        required_features: List[str],
        required_gate_ids: List[str],
        evidence: Dict[str, List[str]],
        gate_by_id: Dict[str, object],
        blocked_gate_refs: List[str],
        complexity_signal_refs: List[str],
        exchange_section_refs: List[str],
        global_missing_information: List[str],
        topology_refs: List[str],
        readiness_refs: List[str],
    ) -> TwinSharedCompatibilityPath:
        present_features = [
            feature
            for feature in required_features
            if evidence.get(feature)
        ]
        missing_features = [
            feature
            for feature in required_features
            if not evidence.get(feature)
        ]
        source_refs = [
            ref
            for feature in required_features
            for ref in evidence.get(feature, [])
        ]
        source_ref_categories = {
            feature: evidence.get(feature, [])
            for feature in required_features
            if evidence.get(feature)
        }
        gate_refs = [
            gate_id
            for gate_id in required_gate_ids
            if gate_id in gate_by_id
        ]
        path_blocked_gate_refs = [
            gate_id
            for gate_id in gate_refs
            if gate_id in blocked_gate_refs
        ]
        missing_information = self._sorted_unique(
            [f"missing_feature:{feature}" for feature in missing_features]
        )
        blockers = self._sorted_unique(
            path_blocked_gate_refs
            + (
                missing_information
                if path_key in {"service_upgrade_likely", "load_management"}
                else []
            )
        )
        required_site_product_verifications = self._sorted_unique(
            gate_refs
            + [
                "product_specs_verified",
                "nameplate_ratings_verified",
                "manufacturer_install_manual_reviewed",
                "load_current_assumptions_confirmed",
                "conduit_routing_path_confirmed",
                "disconnect_requirements_reviewed",
                "overcurrent_protection_reviewed",
                "utility_ahj_requirements_reviewed",
            ]
        )
        status = self._shared_compatibility_status(
            path_key=path_key,
            present_features=present_features,
            missing_features=missing_features,
            gate_refs=gate_refs,
            blocked_gate_refs=path_blocked_gate_refs,
        )
        basis = self._shared_compatibility_basis(
            source_refs=source_refs,
            source_ref_categories=source_ref_categories,
            topology_refs=topology_refs,
            readiness_refs=readiness_refs,
            confirmation_gate_refs=gate_refs,
            install_complexity_signal_refs=complexity_signal_refs,
            exchange_section_refs=exchange_section_refs,
            missing_information_refs=missing_information,
            basis_quality=(
                "current_planning_evidence_with_confirmation_gates"
                if source_refs
                else "missing_or_unknown_planning_evidence"
            ),
            basis_notes=[
                "Path basis uses current planning records only where feature evidence exists.",
                "Missing feature refs are surfaced as missing information and do not become inferred compatibility facts.",
                "Confirmation gates are review requirements, not completed contractor confirmations.",
            ],
        )
        reason = self._shared_compatibility_reason(
            path_label=path_label,
            status=status,
            missing_features=missing_features,
            blocked_gate_refs=path_blocked_gate_refs,
        )
        return TwinSharedCompatibilityPath(
            path_key=path_key,
            path_label=path_label,
            status=status,
            reason=reason,
            basis=basis,
            missing_information=missing_information,
            blockers=blockers,
            required_confirmations=gate_refs,
            contractor_confirmation_gates=gate_refs,
            required_site_product_verifications=required_site_product_verifications,
            confidence_posture=(
                "planning_evidence_with_open_confirmation_gates"
                if source_refs
                else "unknown_until_missing_information_is_resolved"
            ),
            assumptions=[
                "Planning evidence is derived from current recorded context and request-time derived views only.",
                "Missing feature labels are assumptions-not-allowed markers, not inferred facts.",
                "Path status is not final design guidance, approval, or a contractor directive.",
            ],
            homeowner_safe_interpretation=self._shared_compatibility_audience_interpretation(
                audience="homeowner",
                path_label=path_label,
                status=status,
                missing_information=missing_information,
                required_confirmations=gate_refs,
                blockers=blockers,
            ),
            contractor_facing_interpretation=self._shared_compatibility_audience_interpretation(
                audience="contractor",
                path_label=path_label,
                status=status,
                missing_information=missing_information,
                required_confirmations=gate_refs,
                blockers=blockers,
            ),
            limitations=SHARED_COMPATIBILITY_LIMITATIONS,
        )

    def build_shared_compatibility_view(
        self,
        db,
        home_id: str,
        contractor_context=None,
        confirmation_gates=None,
        install_complexity=None,
        exchange_object=None,
    ) -> Optional[TwinSharedCompatibilityView]:
        from app.services.contractor_context import contractor_context_service
        from app.services.planning_exchange import planning_exchange_service

        context = self.build(db, home_id)
        if context is None:
            return None
        snapshot = self.build_topology_snapshot_view(db, home_id)
        if contractor_context is None:
            contractor_context = contractor_context_service.build_contractor_planning_context(db, home_id)
        if confirmation_gates is None:
            confirmation_gates = contractor_context_service.build_confirmation_gate_projection(
                db, home_id, contractor_context=contractor_context
            )
        if install_complexity is None:
            install_complexity = contractor_context_service.build_install_complexity_view(
                db, home_id, contractor_context=contractor_context, gate_projection=confirmation_gates
            )
        if exchange_object is None:
            exchange_object = planning_exchange_service.build_planning_exchange_object(
                db,
                home_id,
                contractor_context=contractor_context,
                confirmation_gates=confirmation_gates,
                install_complexity=install_complexity,
            )
        if snapshot is None or confirmation_gates is None or install_complexity is None or exchange_object is None:
            return None

        evidence = self._shared_compatibility_context_evidence(context)
        gate_by_id = {gate.gate_id: gate for gate in confirmation_gates.gates}
        blocked_gate_refs = [
            gate.gate_id
            for gate in confirmation_gates.gates
            if gate.status == "ahj_or_utility_dependent" or gate.blocker_level == "blocked"
        ]
        complexity_signal_refs = [
            signal.signal_id
            for signal in install_complexity.signals
            if signal.severity in {"high", "blocked", "unknown"}
        ]
        exchange_section_refs = [mapping.section_key for mapping in exchange_object.section_mappings]
        global_missing_information = self._sorted_unique(
            [
                missing
                for item in exchange_object.missing_information
                for missing in item.missing_inputs
            ]
        )
        topology_refs = self._sorted_unique(
            [node.node_id for node in snapshot.nodes]
            + [edge.edge_id for edge in snapshot.edges]
        )
        readiness_refs = self._sorted_unique(
            [hint.lifecycle_domain.value for hint in snapshot.lifecycle_readiness_hints]
            + [indicator.indicator for indicator in snapshot.missing_readiness_indicators]
            + [indicator.indicator for indicator in snapshot.missing_relationship_indicators]
        )
        paths = [
            self._shared_compatibility_path(
                path_key=path_key,
                path_label=path_label,
                required_features=required_features,
                required_gate_ids=required_gate_ids,
                evidence=evidence,
                gate_by_id=gate_by_id,
                blocked_gate_refs=blocked_gate_refs,
                complexity_signal_refs=complexity_signal_refs,
                exchange_section_refs=exchange_section_refs,
                global_missing_information=global_missing_information,
                topology_refs=topology_refs,
                readiness_refs=readiness_refs,
            )
            for path_key, path_label, required_features, required_gate_ids in SHARED_COMPATIBILITY_PATH_SPECS
        ]
        source_basis = self._shared_compatibility_basis(
            source_refs=[
                ref
                for refs in evidence.values()
                for ref in refs
            ],
            source_ref_categories=evidence,
            topology_refs=topology_refs,
            readiness_refs=readiness_refs,
            confirmation_gate_refs=[gate.gate_id for gate in confirmation_gates.gates],
            install_complexity_signal_refs=[signal.signal_id for signal in install_complexity.signals],
            exchange_section_refs=exchange_section_refs,
            missing_information_refs=global_missing_information,
            basis_quality="view_level_request_time_rollup_from_existing_planning_views",
            basis_notes=[
                "Top-level basis includes all known feature evidence, topology/readiness refs, confirmation gates, install complexity signals, and exchange sections used by the view.",
                "Top-level missing information may include broad provenance/readiness gaps inherited from existing planning views.",
                "Path-level missing information remains narrower and only includes missing path ingredients.",
            ],
        )
        required_confirmations = self._sorted_unique(
            [
                confirmation
                for path in paths
                for confirmation in path.required_confirmations
            ]
        )
        contractor_confirmation_gates = self._sorted_unique(
            [
                gate
                for path in paths
                for gate in path.contractor_confirmation_gates
            ]
        )
        missing_information = self._sorted_unique(
            [
                missing
                for path in paths
                for missing in path.missing_information
            ]
            + global_missing_information
        )
        blockers = self._sorted_unique(
            [
                blocker
                for path in paths
                for blocker in path.blockers
            ]
        )
        summary = self._shared_compatibility_summary(
            paths,
            missing_information=missing_information,
            required_confirmations=required_confirmations,
            contractor_confirmation_gates=contractor_confirmation_gates,
        )
        view = TwinSharedCompatibilityView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 7A shared compatibility view built request-time from existing TwinPlanningContext, "
                "topology/readiness outputs, Phase 5 contractor confirmation gates and install complexity signals, and "
                "Phase 6 planning exchange object metadata. It classifies planning/install paths only; it does not persist "
                "state, write data, enforce permissions, export data, create twin_id, rewrite graph behavior, generate "
                "proposals, price work, rank paths, recommend a final design, calculate final wire/conduit/breaker sizing, "
                "approve disconnect/OCPD requirements, produce permit-ready design, confirm field verification, or imply "
                "AHJ/utility/contractor approval."
            ),
            compatibility_scope=TwinSharedCompatibilityScope(limitations=SHARED_COMPATIBILITY_LIMITATIONS),
            source_basis=source_basis,
            summary=summary,
            compatibility_paths=paths,
            blocked_paths=[
                path for path in paths if path.status == TwinSharedCompatibilityStatus.blocked
            ],
            uncertain_paths=[
                path
                for path in paths
                if path.status
                in {
                    TwinSharedCompatibilityStatus.unknown,
                    TwinSharedCompatibilityStatus.requires_contractor_confirmation,
                }
            ],
            required_confirmations=required_confirmations,
            contractor_confirmation_gates=contractor_confirmation_gates,
            assumptions=[
                "Structured planning records and existing derived views are authoritative over generated text.",
                "Compatibility status is derived from known/missing planning ingredients and existing contractor review gates.",
                "Unknown and missing inputs are surfaced instead of inferred.",
            ],
            missing_information=missing_information,
            blockers=blockers,
            homeowner_interpretation=self._shared_compatibility_audience_interpretation(
                audience="homeowner",
                missing_information=missing_information,
                required_confirmations=required_confirmations,
                blockers=blockers,
                paths=paths,
            ),
            contractor_interpretation=self._shared_compatibility_audience_interpretation(
                audience="contractor",
                missing_information=missing_information,
                required_confirmations=required_confirmations,
                blockers=blockers,
                paths=paths,
            ),
            provenance_basis=source_basis,
            limitations=SHARED_COMPATIBILITY_LIMITATIONS,
            deferred_boundaries=sorted(SHARED_COMPATIBILITY_DEFERRED_BOUNDARIES),
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 5 contractor-context, and Phase 6 planning-exchange "
                "routes remain unchanged; this is an additive Phase 7A shared compatibility GET view."
            ),
        )
        return self._attach_trust_provenance_readiness_summary(view)

    def _topology_takeoff_context_evidence(
        self,
        context: TwinPlanningContext,
        snapshot: TwinTopologySnapshot,
        shared_compatibility: TwinSharedCompatibilityView,
    ) -> Dict[str, List[str]]:
        evidence: Dict[str, List[str]] = {
            "backup_loads": [],
            "battery_equipment": [],
            "battery_location": [],
            "generator_equipment": [],
            "generator_location": [],
            "generator_pathway": [],
            "inverter_equipment": [],
            "panel_context": [],
            "pathway_distance": [],
            "power_electronics_location": [],
            "pv_location": [],
            "pv_pathway": [],
            "roof_location": [],
            "solar_equipment": [],
            "trench_pathway": [],
        }
        product_type_by_id: Dict[str, str] = {}
        location_type_by_id: Dict[str, str] = {}
        location_ref_by_id: Dict[str, str] = {}
        product_ref_by_id: Dict[str, str] = {}

        for section in context.sections:
            for record in section.records:
                record_ref = self._record_ref(section.section_key, record)
                payload = record.record or {}
                if record.entity_type == "equipment_product":
                    product_type = str(payload.get("product_type", "")).lower()
                    if record.entity_id:
                        product_type_by_id[record.entity_id] = product_type
                        product_ref_by_id[record.entity_id] = record_ref
                    if product_type == "solar_panel":
                        evidence["solar_equipment"].append(record_ref)
                    if "inverter" in product_type:
                        evidence["inverter_equipment"].append(record_ref)
                    if product_type == "battery":
                        evidence["battery_equipment"].append(record_ref)
                    if product_type == "generator":
                        evidence["generator_equipment"].append(record_ref)
                if record.entity_type == "equipment_location":
                    location_type = str(payload.get("location_type", "")).lower()
                    if record.entity_id:
                        location_type_by_id[record.entity_id] = location_type
                        location_ref_by_id[record.entity_id] = record_ref
                    if location_type == "roof":
                        evidence["roof_location"].append(record_ref)
                        evidence["pv_location"].append(record_ref)
                    if location_type == "battery_area":
                        evidence["battery_location"].append(record_ref)
                        evidence["power_electronics_location"].append(record_ref)
                    if location_type == "generator_pad":
                        evidence["generator_location"].append(record_ref)
                if record.entity_type == "electrical_panel":
                    evidence["panel_context"].append(record_ref)
                if record.entity_type == "load":
                    backup_priority = str(payload.get("backup_priority", "")).lower()
                    if backup_priority in {"essential", "preferred"}:
                        evidence["backup_loads"].append(record_ref)
                if record.entity_type == "estimated_pathway":
                    evidence["pathway_distance"].append(record_ref)
                    route_type = str(payload.get("route_type", "")).lower()
                    source_location = str(payload.get("source_location", "")).lower()
                    destination_location = str(payload.get("destination_location", "")).lower()
                    if "roof" in source_location or "battery" in destination_location:
                        evidence["pv_pathway"].append(record_ref)
                    if "generator" in destination_location:
                        evidence["generator_pathway"].append(record_ref)
                    if "trench" in route_type:
                        evidence["trench_pathway"].append(record_ref)

        for section in context.sections:
            for record in section.records:
                if record.entity_type != "design_equipment":
                    continue
                record_ref = self._record_ref(section.section_key, record)
                payload = record.record or {}
                product_id = payload.get("product_id")
                location_id = payload.get("location_id")
                product_type = product_type_by_id.get(str(product_id), "")
                location_type = location_type_by_id.get(str(location_id), "")
                refs = [record_ref, product_ref_by_id.get(str(product_id)), location_ref_by_id.get(str(location_id))]
                if product_type == "solar_panel":
                    evidence["solar_equipment"].extend(refs)
                    if location_type == "roof":
                        evidence["pv_location"].append(location_ref_by_id.get(str(location_id)))
                if "inverter" in product_type:
                    evidence["inverter_equipment"].extend(refs)
                    if location_type:
                        evidence["power_electronics_location"].append(location_ref_by_id.get(str(location_id)))
                if product_type == "battery":
                    evidence["battery_equipment"].extend(refs)
                    if location_type == "battery_area":
                        evidence["battery_location"].append(location_ref_by_id.get(str(location_id)))
                if product_type == "generator":
                    evidence["generator_equipment"].extend(refs)
                    if location_type == "generator_pad":
                        evidence["generator_location"].append(location_ref_by_id.get(str(location_id)))

        for path in shared_compatibility.compatibility_paths:
            if path.status.value in {"compatible", "likely_compatible", "requires_contractor_confirmation", "blocked"}:
                evidence.setdefault(f"shared_compatibility:{path.path_key}", []).append(
                    f"shared_compatibility:{path.path_key}"
                )

        return {
            key: self._sorted_unique(values)
            for key, values in evidence.items()
        }

    def _topology_takeoff_quantity_hints(self, context: TwinPlanningContext) -> Dict[str, Dict[str, object]]:
        product_type_by_id: Dict[str, str] = {}
        for section in context.sections:
            for record in section.records:
                if record.entity_type == "equipment_product" and record.entity_id:
                    product_type_by_id[record.entity_id] = str((record.record or {}).get("product_type", "")).lower()

        hints: Dict[str, Dict[str, object]] = {
            "battery_equipment": {"value": 0.0, "refs": [], "unit": "recorded_design_equipment_count"},
            "generator_equipment": {"value": 0.0, "refs": [], "unit": "recorded_design_equipment_count"},
            "inverter_equipment": {"value": 0.0, "refs": [], "unit": "recorded_design_equipment_count"},
            "panel_context": {"value": 0.0, "refs": [], "unit": "recorded_panel_count"},
            "pathway_distance": {"value": 0.0, "refs": [], "unit": "estimated_pathway_feet"},
            "solar_equipment": {"value": 0.0, "refs": [], "unit": "recorded_design_equipment_count"},
        }
        for section in context.sections:
            for record in section.records:
                record_ref = self._record_ref(section.section_key, record)
                payload = record.record or {}
                if record.entity_type == "design_equipment":
                    product_type = product_type_by_id.get(str(payload.get("product_id")), "")
                    quantity = payload.get("quantity")
                    if not isinstance(quantity, (int, float)):
                        continue
                    if product_type == "solar_panel":
                        key = "solar_equipment"
                    elif "inverter" in product_type:
                        key = "inverter_equipment"
                    elif product_type == "battery":
                        key = "battery_equipment"
                    elif product_type == "generator":
                        key = "generator_equipment"
                    else:
                        continue
                    hints[key]["value"] = float(hints[key]["value"]) + float(quantity)
                    hints[key]["refs"].append(record_ref)
                if record.entity_type == "electrical_panel":
                    hints["panel_context"]["value"] = float(hints["panel_context"]["value"]) + 1.0
                    hints["panel_context"]["refs"].append(record_ref)
                if record.entity_type == "estimated_pathway":
                    distance = payload.get("estimated_distance_ft")
                    if isinstance(distance, (int, float)):
                        hints["pathway_distance"]["value"] = float(hints["pathway_distance"]["value"]) + float(distance)
                        hints["pathway_distance"]["refs"].append(record_ref)
        return hints

    def _topology_takeoff_basis(
        self,
        *,
        source_refs: Optional[List[str]] = None,
        source_ref_categories: Optional[Dict[str, List[str]]] = None,
        topology_refs: Optional[List[str]] = None,
        compatibility_path_refs: Optional[List[str]] = None,
        confirmation_gate_refs: Optional[List[str]] = None,
        install_complexity_signal_refs: Optional[List[str]] = None,
        exchange_section_refs: Optional[List[str]] = None,
        missing_information_refs: Optional[List[str]] = None,
        basis_quality: str = "request_time_derived_from_existing_topology_context",
        basis_notes: Optional[List[str]] = None,
    ) -> TwinTopologyTakeoffBasis:
        return TwinTopologyTakeoffBasis(
            source_views=[
                "TwinPlanningContext",
                "TwinTopologySnapshot",
                "TwinSharedCompatibilityView",
                "ContractorConfirmationGateProjectionView",
                "ContractorInstallComplexityView",
                "PlanningExchangeObjectView",
            ],
            source_fields=[
                "TwinPlanningContext.sections",
                "TwinTopologySnapshot.nodes",
                "TwinTopologySnapshot.edges",
                "TwinSharedCompatibilityView.compatibility_paths",
                "ContractorConfirmationGateProjectionView.gates",
                "ContractorInstallComplexityView.signals",
                "PlanningExchangeObjectView.section_mappings",
                "PlanningExchangeObjectView.missing_information",
            ],
            source_refs=self._sorted_unique(source_refs or []),
            source_ref_categories={
                key: self._sorted_unique(values)
                for key, values in (source_ref_categories or {}).items()
                if values
            },
            topology_refs=self._sorted_unique(topology_refs or []),
            compatibility_path_refs=self._sorted_unique(compatibility_path_refs or []),
            confirmation_gate_refs=self._sorted_unique(confirmation_gate_refs or []),
            install_complexity_signal_refs=self._sorted_unique(install_complexity_signal_refs or []),
            exchange_section_refs=self._sorted_unique(exchange_section_refs or []),
            missing_information_refs=self._sorted_unique(missing_information_refs or []),
            basis_quality=basis_quality,
            request_time_derived=True,
            verified_fact_claim_present=False,
            basis_notes=self._sorted_unique(
                basis_notes
                or [
                    "Basis is assembled from existing request-time planning and topology views.",
                    "Basis references are not field verification, contractor confirmation, AHJ approval, utility approval, pricing, or final material quantities.",
                ]
            ),
            derived_from=[
                "existing_home_id_anchored_twin_planning_context",
                "phase_2c_topology_snapshot",
                "phase_5_confirmation_gate_projection",
                "phase_5_install_complexity_signals",
                "phase_6_planning_exchange_object",
                "phase_7_shared_compatibility_view",
            ],
            limitations=TOPOLOGY_TAKEOFF_LIMITATIONS,
        )

    def _topology_takeoff_quantity_basis(
        self,
        category: TwinTopologyTakeoffLineCategory,
        quantity_hints: Dict[str, Dict[str, object]],
    ) -> TwinTopologyTakeoffQuantityBasis:
        hint_key_by_category = {
            TwinTopologyTakeoffLineCategory.battery_ess: "battery_equipment",
            TwinTopologyTakeoffLineCategory.generator_integration: "generator_equipment",
            TwinTopologyTakeoffLineCategory.inverter_power_electronics: "inverter_equipment",
            TwinTopologyTakeoffLineCategory.panel_subpanel_load_center: "panel_context",
            TwinTopologyTakeoffLineCategory.pv_source_circuit_array_side: "solar_equipment",
            TwinTopologyTakeoffLineCategory.conduit_raceway_pathway: "pathway_distance",
            TwinTopologyTakeoffLineCategory.routing_trenching_structural_mounting: "pathway_distance",
        }
        hint_key = hint_key_by_category.get(category)
        hint = quantity_hints.get(hint_key or "", {})
        value = hint.get("value")
        refs = self._sorted_unique(hint.get("refs", []) if isinstance(hint.get("refs"), list) else [])
        if isinstance(value, (int, float)) and value > 0:
            if hint_key == "pathway_distance":
                return TwinTopologyTakeoffQuantityBasis(
                    quantity_basis_status="estimated_pathway_distance_available_not_route_takeoff",
                    quantity_value=float(value),
                    quantity_unit="ft",
                    quantity_label="sum_of_recorded_estimated_pathway_distances",
                    quantity_refs=refs,
                    missing_quantity_inputs=[
                        "field_measured_route",
                        "raceway_type",
                        "fittings_count",
                        "routing_conditions",
                    ],
                    notes=[
                        "Distance is an existing pathway planning estimate only.",
                        "Distance is not a conduit, raceway, trenching, conductor, or fittings quantity.",
                    ],
                    limitations=TOPOLOGY_TAKEOFF_LIMITATIONS,
                )
            return TwinTopologyTakeoffQuantityBasis(
                quantity_basis_status="recorded_design_or_panel_count_available_not_material_count",
                quantity_value=float(value),
                quantity_unit=str(hint.get("unit") or "recorded_count"),
                quantity_label="recorded_planning_context_count",
                quantity_refs=refs,
                missing_quantity_inputs=[
                    "field_verified_equipment_count",
                    "manufacturer_install_requirements",
                    "contractor_material_count",
                ],
                notes=[
                    "Quantity is a recorded planning count only.",
                    "Quantity is not a final material takeoff count or procurement quantity.",
                ],
                limitations=TOPOLOGY_TAKEOFF_LIMITATIONS,
            )
        return TwinTopologyTakeoffQuantityBasis(
            quantity_basis_status="missing_final_quantity_basis",
            quantity_label="requires_contractor_or_manufacturer_quantity_basis",
            quantity_refs=[],
            missing_quantity_inputs=[
                "field_verified_topology",
                "site_measurements",
                "manufacturer_install_requirements",
                "contractor_material_count",
            ],
            notes=[
                "Current topology context can identify this scope category but cannot quantify final materials.",
            ],
            limitations=TOPOLOGY_TAKEOFF_LIMITATIONS,
        )

    def _topology_takeoff_cost_basis(
        self,
        *,
        source_refs: Optional[List[str]] = None,
    ) -> TwinTopologyTakeoffCostBasis:
        return TwinTopologyTakeoffCostBasis(
            cost_basis_status=TwinTopologyTakeoffCostBasisStatus.unavailable_requires_contractor_pricing,
            amount_present=False,
            cost_range_present=False,
            total_present=False,
            currency=None,
            source_refs=self._sorted_unique(source_refs or []),
            missing_cost_inputs=[
                "contractor_pricing",
                "verified_material_quantities",
                "manufacturer_requirements",
                "site_conditions",
                "labor_scope",
                "AHJ_or_utility_requirements",
            ],
            cost_notes=[
                "No source-backed material or labor pricing is available in this topology takeoff view.",
                "Existing placeholder estimate fields are not reused as contractor pricing or final estimate totals.",
            ],
            limitations=TOPOLOGY_TAKEOFF_LIMITATIONS,
        )

    def _topology_takeoff_audience_interpretation(
        self,
        *,
        audience: str,
        label: Optional[str] = None,
        line_count: Optional[int] = None,
        missing_information: Optional[List[str]] = None,
        required_confirmations: Optional[List[str]] = None,
    ) -> TwinTopologyTakeoffAudienceInterpretation:
        missing = self._sorted_unique(missing_information or [])
        confirmations = self._sorted_unique(required_confirmations or [])
        if label and audience == "homeowner":
            summary = (
                f"{label} is a planning-grade scope category derived from current topology context. "
                "It is not a final estimate, final bill of materials, or permit-ready design."
            )
            hidden = [
                "final conductor sizing",
                "final conduit sizing",
                "final breaker sizing",
                "final disconnect/OCPD decisions",
                "contractor pricing",
            ]
        elif label:
            summary = (
                f"{label} is contractor-facing review metadata for scoping preparation only. "
                "Confirm topology, quantities, specs, route conditions, and authority requirements before estimate or design use."
            )
            hidden = [
                "completed contractor review",
                "permit-ready bill of materials",
                "final electrical design",
            ]
        elif audience == "homeowner":
            summary = (
                f"Topology takeoff currently identifies {line_count or 0} planning-grade scope categories. "
                "Missing information blocks accurate estimates and final material lists."
            )
            hidden = [
                "contractor-only design decisions",
                "final electrical sizing",
                "pricing and proposal generation",
            ]
        else:
            summary = (
                f"Topology takeoff exposes {line_count or 0} scope categories with basis refs, quantity-basis posture, "
                "cost-basis gaps, and confirmation gates for contractor review preparation."
            )
            hidden = [
                "authority approval",
                "field verification completion",
                "final estimate or BOM approval",
            ]
        return TwinTopologyTakeoffAudienceInterpretation(
            audience=audience,
            interpretation_scope=(
                "homeowner_safe_planning_takeoff_summary"
                if audience == "homeowner"
                else "contractor_facing_takeoff_review_metadata"
            ),
            summary=summary,
            safe_to_show=True,
            next_verification_steps=self._sorted_unique(
                confirmations
                + [
                    "contractor_review_required",
                    "manufacturer_requirements_reviewed",
                    "field_verified_topology",
                ]
            ),
            hidden_or_deferred_details=self._sorted_unique(hidden),
            assumptions=[
                "Interpretation is derived from the same topology takeoff object.",
                "Audience interpretation metadata does not enforce permissions, sharing, exports, or authorization.",
            ],
            limitations=TOPOLOGY_TAKEOFF_LIMITATIONS
            + [
                "Audience interpretation is wording metadata only, not a separate permissioned view.",
                "No auth, sharing, export, or permission enforcement is implemented.",
            ]
            + missing,
        )

    def _topology_takeoff_line_item(
        self,
        *,
        category: TwinTopologyTakeoffLineCategory,
        label: str,
        required_features: List[str],
        required_gate_ids: List[str],
        evidence: Dict[str, List[str]],
        gate_ids: List[str],
        blocked_gate_refs: List[str],
        quantity_hints: Dict[str, Dict[str, object]],
        topology_refs: List[str],
        compatibility_path_refs: List[str],
        install_complexity_signal_refs: List[str],
        exchange_section_refs: List[str],
    ) -> Optional[TwinTopologyTakeoffLineItem]:
        source_ref_categories = {
            feature: evidence.get(feature, [])
            for feature in required_features
            if evidence.get(feature)
        }
        source_refs = [
            ref
            for refs in source_ref_categories.values()
            for ref in refs
        ]
        gate_refs = [
            gate_id
            for gate_id in required_gate_ids
            if gate_id in gate_ids
        ]
        if not source_refs and not gate_refs:
            return None

        missing_features = [
            f"missing_feature:{feature}"
            for feature in required_features
            if not evidence.get(feature)
        ]
        quantity_basis = self._topology_takeoff_quantity_basis(category, quantity_hints)
        cost_basis = self._topology_takeoff_cost_basis(source_refs=source_refs)
        missing_information = self._sorted_unique(
            missing_features
            + quantity_basis.missing_quantity_inputs
            + cost_basis.missing_cost_inputs
        )
        blockers = self._sorted_unique(
            [
                gate_ref
                for gate_ref in gate_refs
                if gate_ref in blocked_gate_refs
            ]
            + (
                ["missing_final_quantity_basis"]
                if quantity_basis.quantity_basis_status == "missing_final_quantity_basis"
                else []
            )
            + ["cost_basis_unavailable_requires_contractor_pricing"]
        )
        basis = self._topology_takeoff_basis(
            source_refs=source_refs,
            source_ref_categories=source_ref_categories,
            topology_refs=topology_refs,
            compatibility_path_refs=compatibility_path_refs,
            confirmation_gate_refs=gate_refs,
            install_complexity_signal_refs=install_complexity_signal_refs,
            exchange_section_refs=exchange_section_refs,
            missing_information_refs=missing_information,
            basis_quality=(
                "topology_supported_scope_with_quantity_basis"
                if quantity_basis.quantity_value is not None
                else "topology_supported_scope_missing_quantity_basis"
            ),
            basis_notes=[
                "Line item is emitted because current topology/planning context implicates this material or scope category.",
                "Line item is not a final material list, contractor estimate, or electrical design decision.",
                "Quantity and cost basis are intentionally separated from scope presence.",
            ],
        )
        uncertainty = (
            "planning_scope_with_recorded_quantity_signal_not_final_material_count"
            if quantity_basis.quantity_value is not None
            else "planning_scope_identified_quantity_missing"
        )
        reason = (
            f"{label} is present because current topology context includes source refs "
            f"{', '.join(source_refs[:4]) or 'confirmation-gate evidence'}."
        )
        return TwinTopologyTakeoffLineItem(
            line_id=f"topology_takeoff:{category.value}",
            category=category,
            label=label,
            reason=reason,
            basis=basis,
            quantity_basis=quantity_basis,
            cost_basis=cost_basis,
            uncertainty=uncertainty,
            missing_information=missing_information,
            blockers=blockers,
            required_confirmations=gate_refs,
            contractor_confirmation_gates=gate_refs,
            homeowner_safe_interpretation=self._topology_takeoff_audience_interpretation(
                audience="homeowner",
                label=label,
                missing_information=missing_information,
                required_confirmations=gate_refs,
            ),
            contractor_facing_interpretation=self._topology_takeoff_audience_interpretation(
                audience="contractor",
                label=label,
                missing_information=missing_information,
                required_confirmations=gate_refs,
            ),
            assumptions=[
                "Scope category presence is derived from current topology/planning evidence only.",
                "Placeholder line categories require contractor/manufacturer/AHJ confirmation before estimate or design use.",
                "No market pricing, vendor pricing, final quantities, or final electrical sizing are inferred.",
            ],
            limitations=TOPOLOGY_TAKEOFF_LIMITATIONS,
        )

    def _topology_takeoff_summary(
        self,
        line_items: List[TwinTopologyTakeoffLineItem],
        *,
        missing_information: List[str],
        blockers: List[str],
        confirmation_gates: List[str],
    ) -> TwinTopologyTakeoffSummary:
        category_counts = Counter(item.category.value for item in line_items)
        line_ids_by_category: Dict[str, List[str]] = {}
        for item in line_items:
            line_ids_by_category.setdefault(item.category.value, []).append(item.line_id)
        return TwinTopologyTakeoffSummary(
            total_line_items=len(line_items),
            category_counts=dict(sorted(category_counts.items())),
            line_ids_by_category={
                key: self._sorted_unique(values)
                for key, values in sorted(line_ids_by_category.items())
            },
            lines_with_quantity_basis_count=sum(
                1 for item in line_items if item.quantity_basis.quantity_value is not None
            ),
            lines_missing_quantity_basis_count=sum(
                1 for item in line_items if item.quantity_basis.quantity_value is None
            ),
            lines_with_cost_basis_count=0,
            lines_requiring_contractor_pricing_count=len(line_items),
            missing_information_count=len(self._sorted_unique(missing_information)),
            blocker_count=len(self._sorted_unique(blockers)),
            confirmation_gate_count=len(self._sorted_unique(confirmation_gates)),
            summary_boundary_note=(
                "Summary counts are planning-grade takeoff rollups only. They are not final estimates, final bills of materials, "
                "contractor-approved scope, final design guidance, permit-ready material lists, or pricing totals."
            ),
        )

    def build_topology_takeoff_view(
        self,
        db,
        home_id: str,
    ) -> Optional[TwinTopologyTakeoffView]:
        from app.services.contractor_context import contractor_context_service
        from app.services.planning_exchange import planning_exchange_service

        context = self.build(db, home_id)
        if context is None:
            return None
        snapshot = self.build_topology_snapshot_view(db, home_id)
        contractor_context = contractor_context_service.build_contractor_planning_context(db, home_id)
        confirmation_gates = contractor_context_service.build_confirmation_gate_projection(
            db, home_id, contractor_context=contractor_context
        )
        install_complexity = contractor_context_service.build_install_complexity_view(
            db, home_id, contractor_context=contractor_context, gate_projection=confirmation_gates
        )
        exchange_object = planning_exchange_service.build_planning_exchange_object(
            db,
            home_id,
            contractor_context=contractor_context,
            confirmation_gates=confirmation_gates,
            install_complexity=install_complexity,
        )
        shared_compatibility = self.build_shared_compatibility_view(
            db,
            home_id,
            contractor_context=contractor_context,
            confirmation_gates=confirmation_gates,
            install_complexity=install_complexity,
            exchange_object=exchange_object,
        )
        if (
            snapshot is None
            or shared_compatibility is None
            or confirmation_gates is None
            or install_complexity is None
            or exchange_object is None
        ):
            return None

        evidence = self._topology_takeoff_context_evidence(context, snapshot, shared_compatibility)
        quantity_hints = self._topology_takeoff_quantity_hints(context)
        gate_ids = [gate.gate_id for gate in confirmation_gates.gates]
        blocked_gate_refs = [
            gate.gate_id
            for gate in confirmation_gates.gates
            if gate.status == "ahj_or_utility_dependent" or gate.blocker_level == "blocked"
        ]
        topology_refs = self._sorted_unique(
            [node.node_id for node in snapshot.nodes]
            + [edge.edge_id for edge in snapshot.edges]
        )
        compatibility_path_refs = [path.path_key for path in shared_compatibility.compatibility_paths]
        install_complexity_signal_refs = [
            signal.signal_id
            for signal in install_complexity.signals
            if signal.category in {"material_takeoff_uncertainty", "routing_path_uncertainty", "field_verification_burden"}
        ]
        exchange_section_refs = [mapping.section_key for mapping in exchange_object.section_mappings]
        line_items = [
            item
            for item in [
                self._topology_takeoff_line_item(
                    category=category,
                    label=label,
                    required_features=required_features,
                    required_gate_ids=required_gate_ids,
                    evidence=evidence,
                    gate_ids=gate_ids,
                    blocked_gate_refs=blocked_gate_refs,
                    quantity_hints=quantity_hints,
                    topology_refs=topology_refs,
                    compatibility_path_refs=compatibility_path_refs,
                    install_complexity_signal_refs=install_complexity_signal_refs,
                    exchange_section_refs=exchange_section_refs,
                )
                for category, label, required_features, required_gate_ids in TOPOLOGY_TAKEOFF_CATEGORY_SPECS
            ]
            if item is not None
        ]
        missing_information = self._sorted_unique(
            [
                missing
                for item in line_items
                for missing in item.missing_information
            ]
            + shared_compatibility.missing_information
            + [
                missing
                for item in exchange_object.missing_information
                for missing in item.missing_inputs
            ]
        )
        blockers = self._sorted_unique(
            [
                blocker
                for item in line_items
                for blocker in item.blockers
            ]
            + shared_compatibility.blockers
        )
        required_confirmations = self._sorted_unique(
            [
                confirmation
                for item in line_items
                for confirmation in item.required_confirmations
            ]
        )
        topology_basis = self._topology_takeoff_basis(
            source_refs=[
                ref
                for refs in evidence.values()
                for ref in refs
            ],
            source_ref_categories=evidence,
            topology_refs=topology_refs,
            compatibility_path_refs=compatibility_path_refs,
            confirmation_gate_refs=gate_ids,
            install_complexity_signal_refs=install_complexity_signal_refs,
            exchange_section_refs=exchange_section_refs,
            missing_information_refs=missing_information,
            basis_quality="view_level_rollup_from_existing_topology_takeoff_inputs",
            basis_notes=[
                "Top-level basis includes all known topology, compatibility, contractor-gate, install-complexity, and planning-exchange refs used by the view.",
                "Top-level basis is sufficient for planning-grade scope discovery only, not final material quantification or pricing.",
            ],
        )
        takeoff_summary = self._topology_takeoff_summary(
            line_items,
            missing_information=missing_information,
            blockers=blockers,
            confirmation_gates=required_confirmations,
        )
        view = TwinTopologyTakeoffView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 8 topology takeoff view built request-time from existing TwinPlanningContext, topology snapshot, "
                "Phase 7 shared compatibility, Phase 5 contractor gates/install complexity, and Phase 6 planning exchange metadata. "
                "It identifies planning-grade material/scope categories and cost-basis gaps only; it does not persist takeoff data, "
                "write data, enforce permissions, export data, create twin_id, generate proposals, calculate prices or totals, "
                "produce final estimates or contractor-approved bills of materials, calculate final wire/conduit/breaker sizing, "
                "approve disconnect/OCPD requirements, produce permit-ready design, or imply NEC/AHJ/utility/contractor approval."
            ),
            takeoff_scope=TwinTopologyTakeoffScope(limitations=TOPOLOGY_TAKEOFF_LIMITATIONS),
            topology_basis=topology_basis,
            takeoff_summary=takeoff_summary,
            line_items=line_items,
            missing_information=missing_information,
            blockers=blockers,
            uncertainty=self._sorted_unique([item.uncertainty for item in line_items]),
            required_confirmations=required_confirmations,
            contractor_confirmation_gates=required_confirmations,
            cost_basis=self._topology_takeoff_cost_basis(source_refs=topology_basis.source_refs),
            homeowner_interpretation=self._topology_takeoff_audience_interpretation(
                audience="homeowner",
                line_count=len(line_items),
                missing_information=missing_information,
                required_confirmations=required_confirmations,
            ),
            contractor_interpretation=self._topology_takeoff_audience_interpretation(
                audience="contractor",
                line_count=len(line_items),
                missing_information=missing_information,
                required_confirmations=required_confirmations,
            ),
            provenance_basis=topology_basis,
            assumptions=[
                "Structured planning records and existing derived topology views are authoritative over generated text.",
                "Line items are included only as planning-grade scope categories supported by current topology/planning context.",
                "Missing quantities, missing pricing, and confirmation gates block accurate estimates and final material lists.",
            ],
            limitations=TOPOLOGY_TAKEOFF_LIMITATIONS,
            deferred_boundaries=sorted(TOPOLOGY_TAKEOFF_DEFERRED_BOUNDARIES),
            compatibility_note=(
                "Existing TwinPlanningContext, topology snapshot, Phase 7 shared compatibility, Phase 5 contractor-context, "
                "Phase 6 planning-exchange, and existing /api/takeoffs/* routes remain unchanged; this is an additive Phase 8 GET view."
            ),
        )
        return self._attach_trust_provenance_readiness_summary(view)

    def _trust_provenance_readiness_index_entry(
        self,
        *,
        source_view_name: str,
        source_phase: str,
        source_endpoint_path: str,
        summary: TwinTrustProvenanceReadinessSummary,
    ) -> TwinTrustProvenanceReadinessIndexEntry:
        return TwinTrustProvenanceReadinessIndexEntry(
            source_view_name=source_view_name,
            source_phase=source_phase,
            source_endpoint_path=source_endpoint_path,
            summary=summary,
            normalized_gap_categories=summary.normalized_gap_categories,
            normalized_source_field_paths=summary.normalized_source_field_paths,
            normalized_provenance_field_paths=summary.normalized_provenance_field_paths,
            normalized_readiness_field_paths=summary.normalized_readiness_field_paths,
            hardened_readiness_boundary=summary.hardened_readiness_boundary,
            gap_notes=summary.gap_notes,
            limitations=summary.limitations
            + [
                "Index entry mirrors existing Phase 4A summary metadata only.",
            ],
        )

    def _phase4_index_entry_values(
        self,
        entries: Iterable[TwinTrustProvenanceReadinessIndexEntry],
        field_name: str,
    ) -> List[str]:
        values = []
        for entry in entries:
            values.extend(getattr(entry, field_name))
        return self._sorted_unique(values)

    def _phase3_index_entries(
        self,
        view_by_name: Dict[str, object],
    ) -> tuple:
        entries = []
        missing_view_names = []
        for source_view_name, source_phase, source_endpoint_path in PHASE_3_DERIVED_VIEW_INDEX_SPECS:
            source_view = view_by_name.get(source_view_name)
            summary = getattr(source_view, "trust_provenance_readiness_summary", None)
            if source_view is None or summary is None:
                missing_view_names.append(source_view_name)
                continue
            entries.append(
                self._trust_provenance_readiness_index_entry(
                    source_view_name=source_view_name,
                    source_phase=source_phase,
                    source_endpoint_path=source_endpoint_path,
                    summary=summary,
                )
            )
        return entries, missing_view_names

    def build_trust_provenance_readiness_index_view(
        self,
        db,
        home_id: str,
    ) -> Optional[TwinTrustProvenanceReadinessIndexView]:
        context = self.build(db, home_id)
        if context is None:
            return None
        snapshot = self.build_topology_snapshot_view(db, home_id)
        if snapshot is None:
            return None

        impact_view = self.build_dependency_impact_readiness_view(db, home_id, context=context, snapshot=snapshot)
        if impact_view is None:
            return None
        reasoning_view = self.build_dependency_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
        )
        if reasoning_view is None:
            return None
        readiness_view = self.build_planning_intelligence_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
        )
        if readiness_view is None:
            return None
        advisory_view = self.build_advisory_context_assembly_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
        )
        if advisory_view is None:
            return None
        risk_view = self.build_constraint_risk_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
        )
        if risk_view is None:
            return None
        scenario_view = self.build_scenario_comparison_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
        )
        if scenario_view is None:
            return None
        pre_recommendation_view = self.build_pre_recommendation_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
        )
        if pre_recommendation_view is None:
            return None
        eligibility_view = self.build_recommendation_eligibility_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
        )
        if eligibility_view is None:
            return None
        basic_recommendations_view = self.build_basic_advisory_recommendations_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
        )
        if basic_recommendations_view is None:
            return None
        contractor_advisory_view = self.build_contractor_facing_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
        )
        if contractor_advisory_view is None:
            return None
        homeowner_advisory_view = self.build_homeowner_facing_advisory_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
        )
        if homeowner_advisory_view is None:
            return None
        energy_goal_reasoning_view = self.build_energy_goal_reasoning_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
            contractor_advisory_view=contractor_advisory_view,
            homeowner_advisory_view=homeowner_advisory_view,
        )
        if energy_goal_reasoning_view is None:
            return None
        proposal_readiness_view = self.build_proposal_readiness_foundation_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
            contractor_advisory_view=contractor_advisory_view,
            energy_goal_reasoning_view=energy_goal_reasoning_view,
        )
        if proposal_readiness_view is None:
            return None
        product_spec_readiness_view = self.build_product_spec_readiness_view(
            db,
            home_id,
            context=context,
            snapshot=snapshot,
            impact_view=impact_view,
            reasoning_view=reasoning_view,
            readiness_view=readiness_view,
            advisory_view=advisory_view,
            risk_view=risk_view,
            scenario_view=scenario_view,
            pre_recommendation_view=pre_recommendation_view,
            eligibility_view=eligibility_view,
            basic_recommendations_view=basic_recommendations_view,
            proposal_readiness_view=proposal_readiness_view,
        )
        if product_spec_readiness_view is None:
            return None

        view_by_name = {
            view.view_name: view
            for view in [
                impact_view,
                reasoning_view,
                readiness_view,
                advisory_view,
                risk_view,
                scenario_view,
                pre_recommendation_view,
                eligibility_view,
                basic_recommendations_view,
                contractor_advisory_view,
                homeowner_advisory_view,
                energy_goal_reasoning_view,
                proposal_readiness_view,
                product_spec_readiness_view,
            ]
        }
        indexed_views, missing_indexed_views = self._phase3_index_entries(view_by_name)
        expected_view_count = len(PHASE_3_DERIVED_VIEW_INDEX_SPECS)
        return TwinTrustProvenanceReadinessIndexView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 4B trust/provenance/readiness index built request-time from existing Phase 3 "
                "derived views and their Phase 4A trust_provenance_readiness_summary metadata only; not scoring, ranking, "
                "pass/fail verdicts, approval claims, verification claims, proposal generation, pricing, product selection, "
                "compatibility claims, export packaging, scenario simulation, permission enforcement, or operational behavior."
            ),
            index_scope=TwinTrustProvenanceReadinessIndexScope(
                limitations=TRUST_PROVENANCE_READINESS_INDEX_LIMITATIONS,
            ),
            indexed_views=indexed_views,
            indexed_view_count=len(indexed_views),
            expected_view_count=expected_view_count,
            missing_indexed_views=missing_indexed_views,
            normalized_gap_categories=self._phase4_index_entry_values(
                indexed_views,
                "normalized_gap_categories",
            ),
            normalized_source_field_paths=self._phase4_index_entry_values(
                indexed_views,
                "normalized_source_field_paths",
            ),
            normalized_provenance_field_paths=self._phase4_index_entry_values(
                indexed_views,
                "normalized_provenance_field_paths",
            ),
            normalized_readiness_field_paths=self._phase4_index_entry_values(
                indexed_views,
                "normalized_readiness_field_paths",
            ),
            hardened_readiness_boundary="advisory_metadata_only",
            deferred_boundaries=sorted(TRUST_PROVENANCE_READINESS_INDEX_DEFERRED_BOUNDARIES),
            limitations=TRUST_PROVENANCE_READINESS_INDEX_LIMITATIONS,
            compatibility_note=(
                "Existing Phase 3 derived view routes and response fields remain unchanged; this is an additive Phase 4B "
                "cross-view metadata index over Phase 4A summaries."
            ),
        )

    def _runtime_role(self, role: TwinRuntimeParticipantRole) -> Optional[TwinRuntimeParticipantRole]:
        try:
            return TwinRuntimeParticipantRole(role)
        except ValueError:
            return None

    def _runtime_view_context(self, role: TwinRuntimeParticipantRole) -> TwinRuntimeViewContext:
        return TwinRuntimeViewContext(
            view_name=f"{role.value}_runtime_projection",
            role=role,
            visibility_scope=RUNTIME_VIEW_SCOPE[role],
            purpose=RUNTIME_VIEW_PURPOSE[role],
            minimum_necessary=role == TwinRuntimeParticipantRole.contractor,
        )

    def _runtime_view_permission_readiness(
        self, role: TwinRuntimeParticipantRole
    ) -> TwinPlanningPermissionReadiness:
        if role == TwinRuntimeParticipantRole.homeowner:
            return self._permission_readiness(
                permission_required=False,
                audience=role.value,
                purpose=RUNTIME_VIEW_PURPOSE[role],
                minimum_necessary=False,
                view_name=f"{role.value}_runtime_projection",
                visibility_scope=RUNTIME_VIEW_SCOPE[role],
                visibility_limitations=[
                    "Homeowner projection is owner-facing planning context, not a permission grant or export package.",
                    "It may include private planning fields that are excluded from external scoped projections.",
                ],
            )
        if role == TwinRuntimeParticipantRole.contractor:
            return self._permission_readiness(
                permission_required=True,
                audience=role.value,
                purpose=RUNTIME_VIEW_PURPOSE[role],
                minimum_necessary=True,
                view_name=f"{role.value}_runtime_projection",
                visibility_scope=RUNTIME_VIEW_SCOPE[role],
                visibility_limitations=[
                    "Contractor projection is a minimized planning/scoping view only.",
                    "It is not a contractor portal, authorization grant, bid packet, stamped design, or export package.",
                    "Homeowner account scaffolding, private notes, full address fields, and internal unknown markers are excluded.",
                ],
            )
        return self._permission_readiness(
            permission_required=True,
            audience=role.value,
            purpose=RUNTIME_VIEW_PURPOSE[role],
            minimum_necessary=False,
            view_name=f"{role.value}_runtime_projection",
            visibility_scope=RUNTIME_VIEW_SCOPE[role],
            visibility_limitations=[
                "Internal/system projection supports runtime governance inspection only.",
                "Internal visibility metadata does not create tenant isolation, audit policy, or authorization enforcement.",
            ],
        )

    def _runtime_record_permission_readiness(
        self, role: TwinRuntimeParticipantRole, record: TwinPlanningContextRecord
    ) -> TwinPlanningPermissionReadiness:
        limitations = [
            "Projection record visibility metadata does not authorize sharing or export.",
            "Future permission enforcement may further narrow fields, source documents, and derived outputs.",
        ]
        if role == TwinRuntimeParticipantRole.contractor:
            limitations.append("Contractor-scoped records remain planning-only and do not imply professional review.")
        if record.classification in {
            TwinPlanningRecordClassification.derived_output,
            TwinPlanningRecordClassification.advisory_output,
        }:
            limitations.append("Derived and advisory outputs remain downstream of recorded planning context.")
        return self._permission_readiness(
            permission_required=role != TwinRuntimeParticipantRole.homeowner,
            audience=role.value,
            purpose=f"{record.entity_type}_{RUNTIME_VIEW_PURPOSE[role]}",
            minimum_necessary=role == TwinRuntimeParticipantRole.contractor,
            view_name=f"{role.value}_runtime_projection:{record.entity_type}",
            visibility_scope=RUNTIME_VIEW_SCOPE[role],
            visibility_limitations=limitations,
        )

    def _runtime_view_fields(
        self, role: TwinRuntimeParticipantRole, record: TwinPlanningContextRecord
    ) -> Dict[str, object]:
        if role in {
            TwinRuntimeParticipantRole.homeowner,
            TwinRuntimeParticipantRole.internal_system,
        }:
            return dict(record.record)
        allowed_fields = RUNTIME_FIELD_ALLOWLIST.get(role, {}).get(record.entity_type, set())
        return {
            field: value
            for field, value in record.record.items()
            if field in allowed_fields
        }

    def _runtime_data_classification(
        self, role: TwinRuntimeParticipantRole, record: TwinPlanningContextRecord
    ) -> DataClassification:
        if role == TwinRuntimeParticipantRole.contractor:
            return DataClassification.contractor_scoped
        if role == TwinRuntimeParticipantRole.internal_system:
            return DataClassification.internal_governance
        return record.data_classification

    def _runtime_contribution_identity(
        self, role: TwinRuntimeParticipantRole, record: TwinPlanningContextRecord
    ) -> TwinRuntimeContributionIdentity:
        contributor_ref = None
        if role in {
            TwinRuntimeParticipantRole.homeowner,
            TwinRuntimeParticipantRole.internal_system,
        }:
            contributor_ref = record.record.get("account_id")

        if record.rule_keys or record.classification in {
            TwinPlanningRecordClassification.derived_output,
            TwinPlanningRecordClassification.advisory_output,
        }:
            contributor_type = "deterministic_rule_or_advisory_runtime"
        elif record.source_document_ids:
            contributor_type = "source_document"
        elif record.data_origin:
            contributor_type = record.data_origin.value if hasattr(record.data_origin, "value") else record.data_origin
        else:
            contributor_type = "unknown"

        return TwinRuntimeContributionIdentity(
            contributor_type=contributor_type,
            contributor_ref=contributor_ref,
            data_origin=record.data_origin,
            source_document_ids=record.source_document_ids,
            limitations=[
                "Contributor identity is limited to available runtime provenance and data_origin metadata.",
                "Absence of contributor_ref does not mean the value is owner-authorized, verified, or externally shareable.",
            ],
        )

    def _runtime_projection_record(
        self,
        *,
        role: TwinRuntimeParticipantRole,
        section_key: str,
        record: TwinPlanningContextRecord,
    ) -> Optional[TwinRuntimeProjectionRecord]:
        fields = self._runtime_view_fields(role, record)
        if (
            role != TwinRuntimeParticipantRole.internal_system
            and not fields
            and not record.rule_keys
            and not record.dependency_hooks
        ):
            return None

        return TwinRuntimeProjectionRecord(
            section_key=section_key,
            entity_type=record.entity_type,
            entity_id=record.entity_id,
            label=record.label,
            visibility_scope=RUNTIME_VIEW_SCOPE[role],
            classification=record.classification,
            authority_layer=record.authority_layer,
            data_classification=self._runtime_data_classification(role, record),
            data_origin=record.data_origin,
            fields=fields,
            provenance_summary=record.provenance_summary,
            source_document_ids=record.source_document_ids,
            contributor_identity=self._runtime_contribution_identity(role, record),
            rule_keys=record.rule_keys,
            dependency_hooks=record.dependency_hooks,
            missing_fields=record.missing_fields,
            provenance_gaps=record.provenance_gaps,
            dependency_awareness=record.dependency_awareness,
            change_impact_hints=record.change_impact_hints,
            planning_dependency_warnings=record.planning_dependency_warnings,
            permission_readiness=self._runtime_record_permission_readiness(role, record),
            limitations=record.limitations,
        )

    def build_runtime_projection_view(
        self, db, home_id: str, role: TwinRuntimeParticipantRole
    ) -> Optional[TwinRuntimeProjectionView]:
        role = self._runtime_role(role)
        if role not in RUNTIME_VIEW_SECTION_ALLOWLIST:
            return None

        context = self.build(db, home_id)
        if context is None:
            return None

        projection_records: List[TwinRuntimeProjectionRecord] = []
        allowed_sections = RUNTIME_VIEW_SECTION_ALLOWLIST[role]
        all_sections = {section.section_key for section in context.sections}

        for section in context.sections:
            if section.section_key not in allowed_sections:
                continue
            for record in section.records:
                projection_record = self._runtime_projection_record(
                    role=role,
                    section_key=section.section_key,
                    record=record,
                )
                if projection_record is not None:
                    projection_records.append(projection_record)

        classification_counts = Counter(record.classification for record in projection_records)
        classification_summary = {
            classification.value: classification_counts.get(classification, 0)
            for classification in TwinPlanningRecordClassification
        }

        provenance_gap_map = {}
        for record in projection_records:
            for gap in record.provenance_gaps:
                key = (
                    gap.gap_type.value,
                    gap.entity_type,
                    gap.entity_id,
                    gap.field_name,
                    gap.reason,
                )
                provenance_gap_map.setdefault(key, gap)
        provenance_gaps = sorted(
            provenance_gap_map.values(),
            key=lambda gap: (
                gap.gap_type.value,
                gap.entity_type,
                gap.entity_id or "",
                gap.field_name or "",
                gap.reason,
            ),
        )

        dependency_hooks = [
            hook
            for record in projection_records
            for hook in record.dependency_hooks
        ]

        included_sections = sorted({record.section_key for record in projection_records})
        return TwinRuntimeProjectionView(
            home_id=home_id,
            participant=TwinRuntimeParticipant(
                role=role,
                relationship_to_home=(
                    "owner_or_owner_authorized_household"
                    if role == TwinRuntimeParticipantRole.homeowner
                    else role.value
                ),
            ),
            view_context=self._runtime_view_context(role),
            implementation_boundary=(
                "Read-only role-aware projection over one existing home_id-anchored Twin Planning Context; "
                "not a separate portal, product codebase, export, permission grant, or canonical ResidentialEnergyTwin model."
            ),
            included_sections=included_sections,
            excluded_sections=sorted(all_sections - set(included_sections)),
            projection_records=projection_records,
            classification_summary=classification_summary,
            provenance_gaps=provenance_gaps,
            dependency_hooks=dependency_hooks,
            dependency_awareness_summary=self._dependency_awareness_summary(projection_records),
            permission_readiness=self._runtime_view_permission_readiness(role),
            limitations=[
                "No twin_id is created or inferred.",
                "The canonical source remains the home_id-anchored Twin Planning Context composed from existing planner records.",
                "This projection does not enforce permissions, authenticate actors, create grants, create exports, or transfer ownership.",
                "This projection does not imply engineering approval, utility approval, safety approval, procurement readiness, or operational control.",
                "Pilot, partner, registry, marketplace, utility sharing, and external partner API behavior remain deferred.",
            ],
            compatibility_note=(
                "Existing TwinPlanningContext, AI grounding, and current /api/* contracts remain unchanged; "
                "this is an additive runtime projection view."
            ),
        )

    def build_ai_design_grounding_view(
        self, db, home_id: str, design_id: Optional[str] = None
    ) -> Optional[AIDesignGroundingView]:
        context = self.build(db, home_id)
        if context is None:
            return None

        if design_id:
            design_found = any(
                record.entity_id == design_id
                for section in context.sections
                if section.section_key == "designs"
                for record in section.records
            )
            if not design_found:
                return None

        related_ids = self._ai_grounding_related_ids(context, design_id)
        grounding_records: List[AIDesignGroundingRecord] = []
        for section in context.sections:
            for record in section.records:
                if not self._include_ai_grounding_record(
                    section_key=section.section_key,
                    record=record,
                    design_id=design_id,
                    related_ids=related_ids,
                ):
                    continue
                grounding_record = self._ai_grounding_record(section.section_key, record)
                if grounding_record.fields or grounding_record.rule_keys or grounding_record.dependency_hooks:
                    grounding_records.append(grounding_record)

        included_sections = sorted({record.section_key for record in grounding_records})
        all_sections = {section.section_key for section in context.sections}
        excluded_sections = sorted(all_sections - set(included_sections))

        provenance_gap_map = {}
        for record in grounding_records:
            for gap in record.provenance_gaps:
                key = (
                    gap.gap_type.value,
                    gap.entity_type,
                    gap.entity_id,
                    gap.field_name,
                    gap.reason,
                )
                provenance_gap_map.setdefault(key, gap)
        provenance_gaps = sorted(
            provenance_gap_map.values(),
            key=lambda gap: (
                gap.gap_type.value,
                gap.entity_type,
                gap.entity_id or "",
                gap.field_name or "",
                gap.reason,
            ),
        )

        dependency_hooks = [
            hook
            for record in grounding_records
            for hook in record.dependency_hooks
        ]

        return AIDesignGroundingView(
            home_id=home_id,
            target_design_id=design_id,
            implementation_boundary=(
                "Read-only minimized AI/design grounding projection over existing Twin Planning Context records; "
                "not the full Twin Planning Context and not a canonical ResidentialEnergyTwin runtime model."
            ),
            included_sections=included_sections,
            excluded_sections=excluded_sections,
            grounding_records=grounding_records,
            provenance_gaps=provenance_gaps,
            dependency_hooks=dependency_hooks,
            dependency_awareness_summary=self._dependency_awareness_summary(grounding_records),
            permission_readiness=self._ai_view_permission_readiness(),
            limitations=[
                "No twin_id is created or inferred.",
                "This AI grounding view is a minimized planning-only projection and is not complete Twin authority.",
                "No permission enforcement, export authorization, utility authority, operational control, or field verification is implemented.",
                "AI may use this view to ground explanations and recommendations, but it must not create canonical facts.",
                "Advisor output remains derived or advisory planning intelligence and is not persisted as Twin truth.",
                "This view does not imply completeness, correctness, safety approval, utility approval, or engineering approval.",
            ],
            compatibility_note=(
                "Existing TwinPlanningContext payloads and current /api/* contracts remain unchanged; "
                "this is an additive AI grounding view."
            ),
        )

    def build(self, db, home_id: str) -> Optional[TwinPlanningContext]:
        home = repository.get_home_by_id(db, home_id)
        if home is None:
            return None

        buildings = repository.list_buildings(db, home_id=home_id)
        panels = repository.list_panels(db, home_id=home_id)
        loads = repository.list_loads(db, home_id=home_id)
        locations = repository.list_equipment_locations(db, home_id=home_id)
        designs = [design for design in repository.list_designs(db) if design.home_id == home_id]
        pathways = repository.list_estimated_pathways(db, home_id=home_id)
        scenarios = [scenario for scenario in repository.list_scenario_models(db) if scenario.home_id == home_id]

        design_equipment = [equipment for design in designs for equipment in design.equipment]
        products_by_id = {
            equipment.product.id: equipment.product
            for equipment in design_equipment
            if equipment.product is not None
        }
        designs_by_id = {design.id: design for design in designs}
        locations_by_id = {location.id: location for location in locations}
        scenarios_by_id = {scenario.id: scenario for scenario in scenarios}
        panels_by_building: Dict[str, List[object]] = {}
        loads_by_building: Dict[str, List[object]] = {}
        for panel in panels:
            panels_by_building.setdefault(panel.building_id, []).append(panel)
        for load in loads:
            loads_by_building.setdefault(load.building_id, []).append(load)
        scenario_revisions = [revision for scenario in scenarios for revision in scenario.revisions]

        sections: List[TwinPlanningContextSection] = []
        unknown_records: List[TwinPlanningContextRecord] = []
        provenance_gaps: List[str] = []

        def add_unknown_if_needed(record: TwinPlanningContextRecord):
            if self._has_provenance(record.provenance_summary):
                return
            gap = f"{record.entity_type}:{record.entity_id} has no linked field-level provenance summary."
            provenance_gaps.append(gap)
            unknown_records.append(
                self._unknown_record(
                    record.entity_type,
                    record.entity_id or "unknown",
                    f"Missing provenance for {record.label}",
                    gap,
                )
            )

        premise_records = [
            self._record(
                db=db,
                entity_type="home",
                entity_id=home.id,
                label=home.name,
                data_origin=home.data_origin,
                record_snapshot=self._record_snapshot(
                    home,
                    [
                        "id",
                        "account_id",
                        "name",
                        "address_line_1",
                        "address_line_2",
                        "city",
                        "state",
                        "postal_code",
                        "country",
                        "utility_provider",
                        "service_size",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=[
                    "Home records are premise planning context, not legal title, utility account authority, or verified service status.",
                ],
            )
        ]
        for record in premise_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="premise", label="Premise", records=premise_records))

        structure_records = [
            self._record(
                db=db,
                entity_type="building",
                entity_id=building.id,
                label=building.name,
                data_origin=building.data_origin,
                record_snapshot=self._record_snapshot(
                    building,
                    [
                        "id",
                        "home_id",
                        "name",
                        "type",
                        "approximate_distance_from_main_service",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=["Building distances and notes remain planning assumptions unless source-backed."],
            )
            for building in buildings
        ]
        for record in structure_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(section_key="structures", label="Structures", records=structure_records)
        )

        panel_records = []
        for panel in panels:
            panel_hooks, panel_hints, panel_warnings = self._panel_load_dependency_metadata(panel, loads_by_building)
            panel_records.append(
                self._record(
                    db=db,
                    entity_type="electrical_panel",
                    entity_id=panel.id,
                    label=f"{panel.panel_type} {panel.amperage}A",
                    data_origin=panel.data_origin,
                    record_snapshot=self._record_snapshot(
                        panel,
                        [
                            "id",
                            "home_id",
                            "building_id",
                            "panel_type",
                            "amperage",
                            "busbar_rating",
                            "breaker_spaces_total",
                            "breaker_spaces_available",
                            "indoor_outdoor",
                            "notes",
                            "data_origin",
                            "created_at",
                            "updated_at",
                        ],
                    ),
                    dependency_hooks=panel_hooks,
                    change_impact_hints=panel_hints,
                    planning_dependency_warnings=panel_warnings,
                    limitations=[
                        "Panel records are electrical planning context, not NEC compliance, AHJ approval, or engineering approval.",
                    ],
                )
            )
        for record in panel_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(
                section_key="electrical_infrastructure",
                label="Electrical Infrastructure",
                records=panel_records,
            )
        )

        load_records = []
        for load in loads:
            load_hooks, load_hints, load_warnings = self._load_panel_dependency_metadata(load, panels_by_building)
            load_records.append(
                self._record(
                    db=db,
                    entity_type="load",
                    entity_id=load.id,
                    label=load.name,
                    data_origin=load.data_origin,
                    record_snapshot=self._record_snapshot(
                        load,
                        [
                            "id",
                            "home_id",
                            "building_id",
                            "name",
                            "category",
                            "running_watts",
                            "surge_watts",
                            "estimated_daily_hours",
                            "backup_priority",
                            "phase_type",
                            "notes",
                            "data_origin",
                            "created_at",
                            "updated_at",
                        ],
                    ),
                    dependency_hooks=load_hooks,
                    change_impact_hints=load_hints,
                    planning_dependency_warnings=load_warnings,
                    limitations=[
                        "Load records are modeled planning loads, not verified circuit inventory, load study, or telemetry.",
                    ],
                )
            )
        for record in load_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="loads", label="Loads", records=load_records))

        location_records = [
            self._record(
                db=db,
                entity_type="equipment_location",
                entity_id=location.id,
                label=location.name,
                data_origin=location.data_origin,
                record_snapshot=self._record_snapshot(
                    location,
                    [
                        "id",
                        "home_id",
                        "building_id",
                        "name",
                        "location_type",
                        "approximate_coordinates",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=["Equipment locations are planning/siting context, not field-verified placement."],
            )
            for location in locations
        ]
        for record in location_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(
                section_key="equipment_locations", label="Equipment Locations", records=location_records
            )
        )

        product_records = [
            self._record(
                db=db,
                entity_type="equipment_product",
                entity_id=product.id,
                label=f"{product.manufacturer} {product.model}",
                data_origin=product.data_origin,
                record_snapshot=self._record_snapshot(
                    product,
                    [
                        "id",
                        "manufacturer",
                        "model",
                        "product_type",
                        "ecosystem",
                        "specs",
                        "documentation_url",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=[
                    "Product records are reference planning data and do not guarantee compatibility, procurement, warranty, or availability.",
                ],
            )
            for product in products_by_id.values()
        ]
        for record in product_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(section_key="equipment_products", label="Equipment Products", records=product_records)
        )

        design_records = [
            self._record(
                db=db,
                entity_type="energy_system_design",
                entity_id=design.id,
                label=design.name,
                data_origin=design.data_origin,
                record_snapshot=self._record_snapshot(
                    design,
                    [
                        "id",
                        "home_id",
                        "name",
                        "design_goal",
                        "architecture_type",
                        "status",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=["Design records are planning intent, not final electrical design or installation approval."],
            )
            for design in designs
        ]
        for record in design_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="designs", label="Designs", records=design_records))

        design_equipment_records = []
        for equipment in design_equipment:
            equipment_hooks, equipment_hints, equipment_warnings = self._design_equipment_dependency_metadata(
                equipment,
                designs_by_id,
                products_by_id,
                locations_by_id,
            )
            design_equipment_records.append(
                self._record(
                    db=db,
                    entity_type="design_equipment",
                    entity_id=equipment.id,
                    label=equipment.role_in_system,
                    data_origin=equipment.data_origin,
                    record_snapshot=self._record_snapshot(
                        equipment,
                        [
                            "id",
                            "design_id",
                            "product_id",
                            "quantity",
                            "location_id",
                            "role_in_system",
                            "notes",
                            "data_origin",
                            "created_at",
                            "updated_at",
                        ],
                    ),
                    dependency_hooks=equipment_hooks,
                    change_impact_hints=equipment_hints,
                    planning_dependency_warnings=equipment_warnings,
                    limitations=[
                        "Design equipment assignments are design composition, not procurement or installed equipment status."
                    ],
                )
            )
        for record in design_equipment_records:
            add_unknown_if_needed(record)
        sections.append(
            TwinPlanningContextSection(section_key="design_equipment", label="Design Equipment", records=design_equipment_records)
        )

        pathway_records = [
            self._record(
                db=db,
                entity_type="estimated_pathway",
                entity_id=pathway.id,
                label=pathway.name,
                data_origin=pathway.data_origin,
                record_snapshot=self._record_snapshot(
                    pathway,
                    [
                        "id",
                        "home_id",
                        "design_id",
                        "name",
                        "description",
                        "lifecycle_stage",
                        "source_location",
                        "destination_location",
                        "estimated_distance_ft",
                        "route_type",
                        "route_difficulty",
                        "visibility_level",
                        "confidence_level",
                        "upfront_cost_placeholder",
                        "estimated_monthly_savings_placeholder",
                        "resilience_score",
                        "notes",
                        "data_origin",
                        "created_at",
                        "updated_at",
                    ],
                ),
                limitations=["Pathways are route planning assumptions, not surveyed construction routes."],
            )
            for pathway in pathways
        ]
        for record in pathway_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="pathways", label="Pathways", records=pathway_records))

        scenario_records = []
        for scenario in scenarios:
            scenario_hooks, scenario_hints, scenario_warnings = self._scenario_dependency_metadata(
                scenario,
                designs_by_id,
            )
            scenario_records.append(
                self._record(
                    db=db,
                    entity_type="scenario",
                    entity_id=scenario.id,
                    label=scenario.name,
                    data_origin=scenario.data_origin,
                    record_snapshot=self._record_snapshot(
                        scenario,
                        [
                            "id",
                            "home_id",
                            "name",
                            "description",
                            "linked_design_id",
                            "upfront_cost_placeholder",
                            "future_expansion_score",
                            "install_complexity_score",
                            "backup_capability_score",
                            "notes",
                            "data_origin",
                            "created_at",
                            "updated_at",
                        ],
                    ),
                    dependency_hooks=scenario_hooks,
                    change_impact_hints=scenario_hints,
                    planning_dependency_warnings=scenario_warnings,
                    limitations=[
                        "Scenario records are planning futures; placeholder scores and costs are not bids, quotes, or financial guarantees.",
                    ],
                )
            )
        for record in scenario_records:
            add_unknown_if_needed(record)
        sections.append(TwinPlanningContextSection(section_key="scenarios", label="Scenarios", records=scenario_records))

        revision_records = []
        for revision in scenario_revisions:
            revision_hooks, revision_hints, revision_warnings = self._scenario_revision_dependency_metadata(
                revision,
                scenarios_by_id,
                designs_by_id,
            )
            revision_records.append(
                self._record(
                    db=db,
                    entity_type="scenario_revision",
                    entity_id=revision.id,
                    label=revision.revision_label,
                    data_origin=revision.data_origin,
                    authority_layer=AuthorityLayer.historical,
                    default_classification=TwinPlanningRecordClassification.derived_output,
                    record_snapshot=self._record_snapshot(
                        revision,
                        [
                            "id",
                            "scenario_id",
                            "parent_revision_id",
                            "revision_number",
                            "revision_label",
                            "revision_status",
                            "linked_design_id",
                            "design_goal_snapshot",
                            "design_status_snapshot",
                            "recommended_profile_snapshot",
                            "planning_summary",
                            "planning_state_snapshot",
                            "data_origin",
                            "created_at",
                            "updated_at",
                        ],
                    ),
                    dependency_hooks=revision_hooks,
                    change_impact_hints=revision_hints,
                    planning_dependency_warnings=revision_warnings,
                    extra_reasons=["Scenario revisions are compact historical planning snapshots."],
                    limitations=[
                        "Scenario revisions preserve compact planning-state framing, not full advisor replay.",
                    ],
                )
            )
        sections.append(
            TwinPlanningContextSection(
                section_key="scenario_revisions", label="Scenario Revisions", records=revision_records
            )
        )

        advisor_records: List[TwinPlanningContextRecord] = []
        for design in designs:
            advisor = design_advisor_service.explain(db, design.id)
            recommendation = advisor["recommendation_profiles"]
            hooks = self._dependency_hooks_from_recommendation(design.id, recommendation)
            advisor_records.append(
                self._advisor_record(design_id=design.id, recommendation=recommendation, dependency_hooks=hooks)
            )
            advisor_records.append(self._advisor_note_record(design.id, advisor["advisor_note"]))

        sections.append(
            TwinPlanningContextSection(
                section_key="derived_intelligence",
                label="Derived And Advisory Intelligence",
                records=advisor_records,
                notes=[
                    "Derived intelligence is regenerated read-only from current planner records.",
                    "No derived output is promoted into canonical facts by this planning context.",
                ],
            )
        )

        sections.append(
            TwinPlanningContextSection(
                section_key="unknowns",
                label="Unknowns And Provenance Gaps",
                records=unknown_records,
                notes=["Unknown records mark missing provenance or missing planning evidence."],
            )
        )

        self._attach_dependency_awareness(sections)
        self._attach_permission_readiness(sections)

        all_records = [record for section in sections for record in section.records]
        context_dependency_hooks = [
            hook
            for record in all_records
            for hook in record.dependency_hooks
        ]

        classification_counts = Counter(
            record.classification for record in all_records
        )
        classification_summary = {
            classification.value: classification_counts.get(classification, 0)
            for classification in TwinPlanningRecordClassification
        }
        typed_provenance_gap_map = {}
        for section in sections:
            for record in section.records:
                for gap in record.provenance_gaps:
                    key = (
                        gap.gap_type.value,
                        gap.entity_type,
                        gap.entity_id,
                        gap.field_name,
                        gap.reason,
                    )
                    typed_provenance_gap_map.setdefault(key, gap)
        typed_provenance_gaps = sorted(
            typed_provenance_gap_map.values(),
            key=lambda gap: (
                gap.gap_type.value,
                gap.entity_type,
                gap.entity_id or "",
                gap.field_name or "",
                gap.reason,
            ),
        )

        return TwinPlanningContext(
            context_id=f"home-planning-context-{home_id}",
            home_id=home_id,
            context_label=f"{home.name} Twin Planning Context",
            implementation_boundary=(
                "Read-only home_id-anchored planning context over existing planner records; "
                "not a canonical ResidentialEnergyTwin runtime model."
            ),
            sections=sections,
            classification_summary=classification_summary,
            provenance_gaps=sorted(set(provenance_gaps)),
            typed_provenance_gaps=typed_provenance_gaps,
            continuity_gaps=[
                "Scenario revisions preserve compact planning-state snapshots, not full historical advisor replay.",
                "No general lifecycle event log, stale-state marker, supersession model, or permission continuity model exists yet.",
            ],
            dependency_hooks=context_dependency_hooks,
            dependency_awareness_summary=self._dependency_awareness_summary(
                all_records
            ),
            permission_readiness=self._context_permission_readiness(),
            limitations=[
                "No twin_id is created or inferred.",
                "This endpoint is not a canonical ResidentialEnergyTwin API.",
                "No permission enforcement, scoped export, utility authority, operational control, or field verification is implemented.",
                "Existing /api/* contracts remain unchanged and are not reclassified as Twin APIs.",
            ],
        )


twin_planning_context_service = TwinPlanningContextService()
