from collections import Counter
from typing import List, Optional

from app.core.types import ConfidenceLevel
from app.crm_handoff.schemas import (
    CRMHandoffField,
    CRMHandoffFieldCategory,
    CRMHandoffScope,
    CRMHandoffSourceBasis,
    CRMHandoffStatus,
    CRMHandoffSummary,
    CRMHandoffView,
)
from app.post_install.schemas import PostInstallStatus

CRM_HANDOFF_LIMITATIONS = [
    "The CRM handoff object is read-only request-time metadata for manual review only.",
    "It does not connect to a CRM, write CRM records, create CRM tasks, sync external systems, send email, create drip campaigns, push notifications, score leads, score sales opportunities, rank follow-ups, or choose a best upsell.",
    "It does not persist state, create exports, create share links, enforce permissions, or mutate source records.",
    "Handoff fields are derived from existing planning views and Phase 13 post-install readiness metadata.",
]

CRM_HANDOFF_DEFERRED_BOUNDARIES = [
    "auth",
    "best_upsell_logic",
    "crm_integration",
    "crm_record_creation",
    "crm_writes",
    "email_drip_campaigns",
    "external_crm_sync",
    "external_services",
    "exports",
    "frontend",
    "lead_scoring",
    "migrations",
    "permission_enforcement",
    "persistence",
    "push_behavior",
    "ranking",
    "sales_scoring",
    "secrets",
    "share_links",
    "task_creation",
    "twin_id",
    "write_endpoints",
]


class CRMHandoffService:
    def _sorted_unique(self, values: List[str]) -> List[str]:
        return sorted({value for value in values if value})

    def _basis(
        self,
        *,
        source_refs: Optional[List[str]] = None,
        post_install_refs: Optional[List[str]] = None,
        lifecycle_event_refs: Optional[List[str]] = None,
        retention_opportunity_refs: Optional[List[str]] = None,
        missing_input_refs: Optional[List[str]] = None,
        blocker_refs: Optional[List[str]] = None,
        confirmation_gate_refs: Optional[List[str]] = None,
        handoff_field_refs: Optional[List[str]] = None,
        deferred_boundary_refs: Optional[List[str]] = None,
        unavailable_source_refs: Optional[List[str]] = None,
        basis_quality: str = "request_time_derived_from_phase_13_post_install_view",
    ) -> CRMHandoffSourceBasis:
        return CRMHandoffSourceBasis(
            source_views=["PostInstallView"],
            source_fields=[
                "PostInstallView.summary",
                "PostInstallView.opportunities",
                "PostInstallView.lifecycle_events",
                "PostInstallView.missing_inputs",
                "PostInstallView.blockers",
                "PostInstallView.confirmation_gate_ids",
            ],
            source_refs=self._sorted_unique(source_refs or []),
            post_install_refs=self._sorted_unique(post_install_refs or []),
            lifecycle_event_refs=self._sorted_unique(lifecycle_event_refs or []),
            retention_opportunity_refs=self._sorted_unique(retention_opportunity_refs or []),
            missing_input_refs=self._sorted_unique(missing_input_refs or []),
            blocker_refs=self._sorted_unique(blocker_refs or []),
            confirmation_gate_refs=self._sorted_unique(confirmation_gate_refs or []),
            handoff_field_refs=self._sorted_unique(handoff_field_refs or []),
            deferred_boundary_refs=self._sorted_unique(deferred_boundary_refs or []),
            unavailable_source_refs=self._sorted_unique(unavailable_source_refs or []),
            basis_quality=basis_quality,
            request_time_derived=True,
            verified_fact_claim_present=False,
            limitations=CRM_HANDOFF_LIMITATIONS,
        )

    def _field(
        self,
        *,
        field_key: str,
        category: CRMHandoffFieldCategory,
        label: str,
        value: str,
        source_refs: Optional[List[str]] = None,
        missing_inputs: Optional[List[str]] = None,
    ) -> CRMHandoffField:
        return CRMHandoffField(
            field_id=f"phase_13_crm_handoff:{field_key}",
            field_key=field_key,
            category=category,
            label=label,
            value=value,
            source_refs=self._sorted_unique(source_refs or []),
            missing_inputs=self._sorted_unique(missing_inputs or []),
            limitations=CRM_HANDOFF_LIMITATIONS,
        )

    def _status_from_post_install(self, post_install_view) -> CRMHandoffStatus:
        if post_install_view.summary.overall_status == PostInstallStatus.unavailable:
            return CRMHandoffStatus.unavailable
        if post_install_view.summary.overall_status == PostInstallStatus.source_limited:
            return CRMHandoffStatus.source_limited
        if post_install_view.missing_inputs:
            return CRMHandoffStatus.blocked_by_missing_inputs
        if post_install_view.blockers or post_install_view.confirmation_gate_ids:
            return CRMHandoffStatus.review_required
        return CRMHandoffStatus.manual_handoff_object_ready

    def build_home_crm_handoff(self, db, home_id: str) -> Optional[CRMHandoffView]:
        from app.services.post_install import post_install_service

        post_install_view = post_install_service.build_home_post_install_view(db, home_id)
        if post_install_view is None:
            return None

        lifecycle_event_refs = self._sorted_unique(
            [event.event_id for event in post_install_view.lifecycle_events if event.detected]
        )
        retention_opportunity_refs = self._sorted_unique(
            [opportunity.opportunity_id for opportunity in post_install_view.opportunities]
        )
        blocker_refs = self._sorted_unique([blocker.blocker_id for blocker in post_install_view.blockers])
        missing_inputs = self._sorted_unique(post_install_view.missing_inputs)
        confirmation_gate_ids = self._sorted_unique(post_install_view.confirmation_gate_ids)
        status = self._status_from_post_install(post_install_view)
        confidence = ConfidenceLevel.low if missing_inputs else ConfidenceLevel.medium
        handoff_fields = sorted(
            [
                self._field(
                    field_key="home_anchor",
                    category=CRMHandoffFieldCategory.home_anchor,
                    label="Home anchor",
                    value=home_id,
                    source_refs=["PostInstallView.home_id"],
                ),
                self._field(
                    field_key="post_install_status",
                    category=CRMHandoffFieldCategory.follow_up_readiness,
                    label="Post-install status",
                    value=post_install_view.summary.overall_status.value,
                    source_refs=["PostInstallView.summary.overall_status"],
                ),
                self._field(
                    field_key="manual_review_summary",
                    category=CRMHandoffFieldCategory.review_context,
                    label="Manual review summary",
                    value=post_install_view.contractor_summary,
                    source_refs=["PostInstallView.contractor_summary"],
                ),
                self._field(
                    field_key="retention_opportunity_refs",
                    category=CRMHandoffFieldCategory.retention_context,
                    label="Retention opportunity refs",
                    value=", ".join(retention_opportunity_refs) or "none",
                    source_refs=retention_opportunity_refs,
                ),
                self._field(
                    field_key="lifecycle_event_refs",
                    category=CRMHandoffFieldCategory.lifecycle_context,
                    label="Lifecycle event refs",
                    value=", ".join(lifecycle_event_refs) or "none",
                    source_refs=lifecycle_event_refs,
                ),
                self._field(
                    field_key="missing_input_refs",
                    category=CRMHandoffFieldCategory.missing_input_context,
                    label="Missing input refs",
                    value=", ".join(missing_inputs) or "none",
                    source_refs=["PostInstallView.missing_inputs"],
                    missing_inputs=missing_inputs,
                ),
                self._field(
                    field_key="source_basis",
                    category=CRMHandoffFieldCategory.source_basis,
                    label="Source basis",
                    value=post_install_view.source_basis.basis_quality,
                    source_refs=post_install_view.source_basis.source_views,
                ),
                self._field(
                    field_key="boundary",
                    category=CRMHandoffFieldCategory.boundary,
                    label="Boundary",
                    value="manual_handoff_object_only_no_crm_write_no_task_no_email_no_score_no_rank_no_push",
                    source_refs=["Phase 13 boundary"],
                ),
            ],
            key=lambda field: field.field_key,
        )
        source_basis = self._basis(
            source_refs=post_install_view.source_basis.source_refs,
            post_install_refs=["PostInstallView"],
            lifecycle_event_refs=lifecycle_event_refs,
            retention_opportunity_refs=retention_opportunity_refs,
            missing_input_refs=missing_inputs,
            blocker_refs=blocker_refs,
            confirmation_gate_refs=confirmation_gate_ids,
            handoff_field_refs=[field.field_id for field in handoff_fields],
            deferred_boundary_refs=CRM_HANDOFF_DEFERRED_BOUNDARIES,
            basis_quality="home_level_phase_13_crm_handoff_rollup",
        )
        summary = CRMHandoffSummary(
            overall_status=status,
            confidence_level=confidence,
            handoff_field_count=len(handoff_fields),
            retention_opportunity_count=len(retention_opportunity_refs),
            lifecycle_event_count=len(lifecycle_event_refs),
            blocker_count=len(blocker_refs),
            missing_input_count=len(missing_inputs),
            confirmation_gate_count=len(confirmation_gate_ids),
            manual_crm_review_ready=True,
            crm_write_allowed=False,
            external_crm_sync_allowed=False,
            email_campaign_allowed=False,
            task_creation_allowed=False,
            scoring_allowed=False,
            ranking_allowed=False,
            push_allowed=False,
            summary_boundary_note=(
                "CRM handoff is a read-only object for manual review. It does not write CRM data, create records, "
                "create tasks, sync external systems, send email, score, rank, choose upsells, or push notifications."
            ),
        )
        return CRMHandoffView(
            home_id=home_id,
            implementation_boundary=(
                "Read-only Phase 13 CRM handoff object built request-time from the Phase 13 post-install view. "
                "It shapes manual handoff metadata only; it does not persist state, run migrations, enforce permissions, "
                "integrate with CRM, write CRM records, create CRM tasks, sync external systems, send email, create drip "
                "campaigns, score leads or sales opportunities, rank follow-ups, choose a best upsell, push notifications, "
                "add secrets, create twin_id, create graph behavior, or create operational behavior."
            ),
            handoff_object_id=f"crm_handoff:home:{home_id}:phase_13_request_time",
            handoff_scope=CRMHandoffScope(limitations=CRM_HANDOFF_LIMITATIONS),
            summary=summary,
            handoff_fields=handoff_fields,
            lifecycle_event_refs=lifecycle_event_refs,
            retention_opportunity_refs=retention_opportunity_refs,
            missing_inputs=missing_inputs,
            blockers=blocker_refs,
            confirmation_gate_ids=confirmation_gate_ids,
            manual_review_summary=(
                "Manual CRM review metadata is available as a request-time object only; no CRM action was taken."
            ),
            homeowner_safe_summary=post_install_view.homeowner_summary,
            contractor_review_summary=post_install_view.contractor_summary,
            source_basis=source_basis,
            field_category_counts=dict(sorted(Counter(field.category.value for field in handoff_fields).items())),
            assumptions=[
                "The handoff object uses fixed deterministic fields and is not ranked or scored.",
                "The Phase 13 post-install view is authoritative over this handoff projection.",
                "No external CRM, email, task, push, or scoring behavior is present.",
            ],
            limitations=CRM_HANDOFF_LIMITATIONS,
            deferred_boundaries=sorted(CRM_HANDOFF_DEFERRED_BOUNDARIES),
            compatibility_note="Existing post-install, product-preference, contractor-workflow, proposal, estimate, and planning routes remain unchanged.",
        )


crm_handoff_service = CRMHandoffService()
