"""Focused backend tests for the planner-intelligence read facade (slice 1, C1).

These tests reuse the project's in-memory seeded harness and call the facade
handler/service directly (the pattern used by test_permissions). They assert the
auth/audit/provenance/trust contract of:

    GET /api/planner-intelligence/designs/{design_id}/summary
"""

import json
import unittest
from types import SimpleNamespace
from unittest import mock

from fastapi import HTTPException  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

import tests.fast_db  # noqa: E402  must precede app imports
from app.auth.router import current_principal  # noqa: E402
from app.core import models  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.core.repository import repository  # noqa: E402
from app.main import app  # noqa: E402
from app.planner_intelligence.router import get_design_planner_intelligence_summary  # noqa: E402
from app.security.audit import audit_service  # noqa: E402
from app.security.principal import scaffold_principal_from_headers  # noqa: E402
from app.services.design_advisor import design_advisor_service  # noqa: E402
from app.services.planner_intelligence import planner_intelligence_service  # noqa: E402
from tests.fast_db import reset_and_reseed  # noqa: E402

DESIGN_ID = "design_001"
HOME_ID = "home_001"
ROUTE = "/api/planner-intelligence/designs/{design_id}/summary"
ACTION = "planner_intelligence.read"

ALLOWED_CONTEXT_KEYS = {
    "design_id",
    "home_id",
    "constraint_count",
    "recommendation_present",
    "scenario_comparison_present",
    "provenance_source_count",
    "outcome",
}

# Advisory copy that must never leak into the audit event context.
ADVISORY_LEAK_MARKERS = [
    "advisor composes",
    "fit_reason",
    "best for",
    "ui_description",
    "behavioral_assumptions",
    "why_it_matters",
]


class PlannerIntelligenceTests(unittest.TestCase):
    def setUp(self):
        reset_and_reseed()
        with Session(engine) as db:
            db.query(models.AuditEvent).delete()
            db.commit()

    # ---- helpers ----
    def _owner(self):
        return scaffold_principal_from_headers("user_owner_test", HOME_ID)

    def _outsider(self):
        return scaffold_principal_from_headers("user_outsider_test", "home_not_owned")

    def _read_as(self, principal, design_id=DESIGN_ID):
        with Session(engine) as db:
            return get_design_planner_intelligence_summary(design_id, db, principal)

    def _planner_audit_rows(self):
        with Session(engine) as db:
            return (
                db.query(models.AuditEvent)
                .filter(models.AuditEvent.action == ACTION)
                .all()
            )

    # ---- route registration ----
    def test_route_is_registered(self):
        paths = app.openapi()["paths"]
        self.assertIn(ROUTE, paths)
        self.assertIn("get", paths[ROUTE])

    # ---- allowed owner read ----
    def test_owner_read_returns_payload_with_all_six_blocks(self):
        result = self._read_as(self._owner())
        payload = result.model_dump()
        blocks = payload["blocks"]
        for name in (
            "recommendations",
            "constraints",
            "readiness_explanation",
            "upgrade_path_explanation",
            "scenario_comparison_explanation",
            "provenance_summary",
        ):
            self.assertIn(name, blocks)
        self.assertEqual(DESIGN_ID, payload["design_id"])
        self.assertEqual(HOME_ID, payload["home_id"])

    def test_every_returned_block_has_a_trust_envelope(self):
        blocks = self._read_as(self._owner()).model_dump()["blocks"]
        for name, value in blocks.items():
            if value is None:  # an omitted optional block is acceptable
                continue
            self.assertIn("trust_envelope", value, f"{name} missing trust_envelope")
            self.assertIn("authority_layer", value["trust_envelope"])

    # ---- upgrade path provenance discipline ----
    def test_upgrade_path_consumes_public_planning_state_without_private_builder(self):
        import inspect

        # 1) Static guarantee: the facade source never names the private builder.
        #    (explain() may call _build_planning_state internally and transitively
        #    several times via scenario comparison, so counting calls cannot isolate
        #    a facade-direct call -- a source check is the unambiguous proof.)
        facade_src = inspect.getsource(planner_intelligence_service.__class__)
        self.assertNotIn("_build_planning_state", facade_src)

        # 2) Behavioral identity: the snapshot in the response is the exact object
        #    returned by the facade's own public explain(DESIGN_ID) call. explain()
        #    is invoked multiple times (the facade's call first, then again per
        #    linked-scenario design via scenario comparison), each returning a fresh
        #    snapshot instance -- so capture the FIRST call per design_id, which is
        #    the facade's own call.
        real_explain = design_advisor_service.explain
        captured = {}

        def spy_explain(db, design_id):
            out = real_explain(db, design_id)
            captured.setdefault(design_id, out["planning_state"])
            return out

        with mock.patch.object(design_advisor_service, "explain", side_effect=spy_explain):
            with Session(engine) as db:
                design = repository.get_design(db, DESIGN_ID)
                result = planner_intelligence_service.build_design_summary(db, design, HOME_ID)

        self.assertIs(
            result.blocks.upgrade_path_explanation.planning_state,
            captured[DESIGN_ID],
        )

    def test_upgrade_path_provenance_refs_are_planning_state_variants(self):
        block = self._read_as(self._owner()).model_dump()["blocks"]["upgrade_path_explanation"]
        refs = block["trust_envelope"]["provenance_refs"]
        self.assertTrue(refs, "upgrade path should carry variant provenance refs")
        self.assertTrue(all(r["entity_type"] == "planning_state_variant" for r in refs))

    # ---- audit: allowed ----
    def test_allowed_read_writes_one_allowed_audit_event(self):
        self._read_as(self._owner())
        rows = self._planner_audit_rows()
        self.assertEqual(1, len(rows))
        row = rows[0]
        self.assertEqual("allowed", row.decision)
        self.assertEqual("true", row.authorized)
        self.assertEqual(200, row.status_code)
        self.assertEqual("design", row.object_type)
        self.assertEqual(DESIGN_ID, row.object_id)
        self.assertEqual("planner_intelligence", row.source_surface)
        self.assertEqual(ROUTE, row.route_template)

    # ---- audit: forbidden ----
    def test_cross_account_read_returns_403_and_writes_one_denied_event(self):
        with self.assertRaises(HTTPException) as ctx:
            self._read_as(self._outsider())
        self.assertEqual(403, ctx.exception.status_code)

        rows = self._planner_audit_rows()
        self.assertEqual(1, len(rows))
        self.assertEqual("denied", rows[0].decision)
        self.assertEqual(403, rows[0].status_code)
        self.assertEqual(DESIGN_ID, rows[0].object_id)
        self.assertEqual("planner_intelligence", rows[0].source_surface)

    # ---- 401 is the auth layer, not the planner-intelligence handler ----
    def test_unauthenticated_is_handled_by_current_principal_not_the_facade(self):
        # An unauthenticated request never reaches the planner-intelligence
        # handler: current_principal raises 401 first, so no planner_intelligence
        # audit row is the responsibility of (or written by) this facade.
        request = SimpleNamespace(headers={})
        with Session(engine) as db:
            with self.assertRaises(HTTPException) as ctx:
                current_principal(request, db)
        self.assertEqual(401, ctx.exception.status_code)
        self.assertEqual([], self._planner_audit_rows())

    # ---- audit degrade: a failed audit write must not 500 a valid read ----
    def test_audit_write_failure_does_not_break_a_valid_read(self):
        with mock.patch.object(
            audit_service,
            "record_with_new_session",
            side_effect=RuntimeError("simulated audit backend failure"),
        ):
            result = self._read_as(self._owner())  # must not raise
        # the read still produced a full payload
        self.assertEqual(DESIGN_ID, result.design_id)
        self.assertIsNotNone(result.blocks.provenance_summary)
        # and the degraded write left no audit row
        self.assertEqual([], self._planner_audit_rows())

    # ---- audit context minimization ----
    def test_audit_context_holds_only_ids_counts_decision_refs(self):
        self._read_as(self._owner())
        row = self._planner_audit_rows()[0]

        self.assertTrue(set(row.event_context.keys()).issubset(ALLOWED_CONTEXT_KEYS))
        for value in row.event_context.values():
            self.assertIsInstance(value, (str, int, bool))

        blob = json.dumps(row.event_context).lower()
        for marker in ADVISORY_LEAK_MARKERS:
            self.assertNotIn(marker, blob, f"advisory text leaked into audit: {marker}")

    # ---- provenance refs breadth ----
    def test_audit_provenance_refs_cover_design_home_variant_and_home_scoped_sources(self):
        self._read_as(self._owner())
        refs = self._planner_audit_rows()[0].provenance_refs
        self.assertIsInstance(refs, list)

        def has(entity_type, entity_id=None):
            return any(
                r.get("entity_type") == entity_type
                and (entity_id is None or r.get("entity_id") == entity_id)
                for r in refs
            )

        self.assertTrue(has("design", DESIGN_ID), "design ref missing")
        self.assertTrue(has("home", HOME_ID), "home ref missing")
        self.assertTrue(has("planning_state_variant"), "planning-state variant refs missing")
        # home-scoped source objects actually touched (seeded home has scenarios)
        self.assertTrue(has("scenario"), "home-scoped scenario refs missing")

    def test_upgrade_readiness_context_reflects_home_scoped_composition(self):
        ctx = self._read_as(self._owner()).model_dump()["blocks"]["upgrade_path_explanation"][
            "readiness_context"
        ]
        self.assertEqual(HOME_ID, ctx["home_id"])
        for flag in (
            "planning_intelligence_readiness_available",
            "constraint_risk_available",
            "dependency_impact_available",
            "dependency_reasoning_available",
        ):
            self.assertIn(flag, ctx)
            self.assertIsInstance(ctx[flag], bool)

    # ---- no authority inflation ----
    def test_no_block_claims_engineering_permitting_utility_or_pricing_authority(self):
        payload = self._read_as(self._owner()).model_dump()

        # The whole view is advisory; nothing canonical/operational is asserted.
        self.assertEqual("advisory", payload["view_boundary"]["authority_layer"])
        for name, value in payload["blocks"].items():
            if value is None:
                continue
            layer = value["trust_envelope"]["authority_layer"]
            self.assertIn(layer, {"derived", "advisory"}, f"{name} over-claims authority: {layer}")

        # Explicit non-authority disclaimer is present at the top level.
        joined = " ".join(payload["limitations"]).lower()
        self.assertIn("not engineering", joined)
        self.assertIn("authority", joined)


if __name__ == "__main__":
    unittest.main()
