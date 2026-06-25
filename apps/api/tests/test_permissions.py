import unittest
from datetime import datetime

from tests.fast_db import reset_and_reseed  # noqa: E402  must precede app imports

from fastapi import HTTPException  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.ai_context import router as ai_context_router  # noqa: E402
from app.buildings import router as buildings_router  # noqa: E402
from app.compatibility_rules import router as compatibility_router  # noqa: E402
from app.core import models  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.designs import router as designs_router  # noqa: E402
from app.design_advisor import router as design_advisor_router  # noqa: E402
from app.equipment import router as equipment_router  # noqa: E402
from app.homes import router as homes_router  # noqa: E402
from app.homes.schemas import BuildingStructureCreate, HomeUpdate  # noqa: E402
from app.loads import router as loads_router  # noqa: E402
from app.loads.schemas import LoadUpdate  # noqa: E402
from app.panels import router as panels_router  # noqa: E402
from app.planning import router as planning_router  # noqa: E402
from app.privacy import router as privacy_router  # noqa: E402
from app.product_library import router as product_library_router  # noqa: E402
from app.scenarios import router as scenarios_router  # noqa: E402
from app.security.principal import VerifiedIdentityClaims, principal_from_verified_claims  # noqa: E402
from app.takeoffs import router as takeoffs_router  # noqa: E402


class AccountMembershipPermissionsTests(unittest.TestCase):
    def setUp(self):
        reset_and_reseed()
        with Session(engine) as db:
            self._add_extra_scope_records(db)

    def test_home_collection_filters_by_account_membership_and_hides_null_account_homes(self):
        with Session(engine) as db:
            principal = self._principal(db, role="owner")

            homes = homes_router.list_homes(db, principal)

        home_ids = {home.id for home in homes}
        self.assertIn("home_001", home_ids)
        self.assertNotIn("home_other", home_ids)
        self.assertNotIn("home_null", home_ids)

    def test_provider_identity_without_app_membership_cannot_list_homes(self):
        with Session(engine) as db:
            principal = self._principal_without_membership(db)

            homes = homes_router.list_homes(db, principal)
            with self.assertRaises(HTTPException) as takeoff_error:
                takeoffs_router.get_takeoff(db, principal)

        self.assertEqual([], homes)
        self.assertEqual(404, takeoff_error.exception.status_code)

    def test_viewer_can_read_but_cannot_write_home(self):
        with Session(engine) as db:
            principal = self._principal(db, role="viewer")

            homes = homes_router.list_homes(db, principal)
            with self.assertRaises(HTTPException) as error:
                homes_router.update_home("home_001", HomeUpdate(notes="viewer attempted write"), db, principal)

        self.assertIn("home_001", {home.id for home in homes})
        self.assertEqual(403, error.exception.status_code)

    def test_member_can_write_home(self):
        with Session(engine) as db:
            principal = self._principal(db, role="member")

            updated = homes_router.update_home("home_001", HomeUpdate(notes="member write allowed"), db, principal)

        self.assertEqual("member write allowed", updated.notes)

    def test_design_collection_filters_by_authorized_homes_and_denies_cross_account_equipment(self):
        with Session(engine) as db:
            principal = self._principal(db, role="owner")

            designs = designs_router.list_designs(db, principal)
            with self.assertRaises(HTTPException) as error:
                designs_router.list_design_equipment("design_other", db, principal)

        design_ids = {design.id for design in designs}
        self.assertIn("design_001", design_ids)
        self.assertIn("design_002", design_ids)
        self.assertNotIn("design_other", design_ids)
        self.assertNotIn("design_null", design_ids)
        self.assertEqual(403, error.exception.status_code)

    def test_scenario_collection_filters_and_cross_account_revisions_are_denied(self):
        with Session(engine) as db:
            principal = self._principal(db, role="owner")

            scenarios = scenarios_router.list_scenarios(db, principal)
            with self.assertRaises(HTTPException) as error:
                scenarios_router.list_scenario_revisions("scenario_other", db, principal)

        scenario_ids = {scenario["id"] for scenario in scenarios}
        self.assertIn("scenario_001", scenario_ids)
        self.assertIn("scenario_002", scenario_ids)
        self.assertNotIn("scenario_other", scenario_ids)
        self.assertNotIn("scenario_null", scenario_ids)
        self.assertEqual(403, error.exception.status_code)

    def test_global_product_library_read_remains_available(self):
        with Session(engine) as db:
            products = product_library_router.list_products(db)

        self.assertGreater(len(products), 0)

    def test_remaining_collections_filter_by_authorized_homes_and_designs(self):
        with Session(engine) as db:
            principal = self._principal(db, role="owner")

            buildings = buildings_router.list_buildings(db=db, principal=principal)
            panels = panels_router.list_panels(db=db, principal=principal)
            loads = loads_router.list_loads(db, principal)
            summary = loads_router.load_summary(db, principal)
            locations = equipment_router.list_equipment_locations(db, principal)
            pathways = planning_router.list_estimated_pathways(db=db, principal=principal)
            issues = compatibility_router.list_issues(db, principal)
            takeoff = takeoffs_router.get_takeoff(db, principal)

        self.assertEqual({"home_001"}, {building.home_id for building in buildings})
        self.assertEqual({"home_001"}, {panel.home_id for panel in panels})
        self.assertEqual({"home_001"}, {load.home_id for load in loads})
        self.assertEqual(3680, summary["total_running_watts"])
        self.assertEqual({"home_001"}, {location.home_id for location in locations})
        self.assertEqual({"home_001"}, {pathway.home_id for pathway in pathways})
        self.assertEqual({"design_001", "design_002"}, {issue.design_id for issue in issues})
        self.assertEqual("design_001", takeoff["request"].design_id)
        self.assertNotIn("issue_other", {issue.id for issue in issues})
        self.assertNotIn("issue_null", {issue.id for issue in issues})

    def test_design_scoped_derived_routes_deny_cross_account_designs(self):
        with Session(engine) as db:
            principal = self._principal(db, role="owner")

            route_calls = (
                lambda: compatibility_router.evaluate_design("design_other", db, principal),
                lambda: takeoffs_router.generate_takeoff("design_other", db, principal),
                lambda: ai_context_router.design_context("design_other", db, principal),
                lambda: design_advisor_router.advisor_summary("design_other", db, principal),
            )

            for route_call in route_calls:
                with self.assertRaises(HTTPException) as error:
                    route_call()
                self.assertEqual(403, error.exception.status_code)

    def test_viewer_writes_denied_and_member_writes_allowed_on_remaining_routes(self):
        with Session(engine) as db:
            viewer = self._principal(db, role="viewer")
            with self.assertRaises(HTTPException) as error:
                buildings_router.create_building(
                    BuildingStructureCreate(
                        id="building_viewer_attempt",
                        home_id="home_001",
                        name="Viewer Attempt",
                        type="workshop",
                    ),
                    db,
                    viewer,
                )

        self.assertEqual(403, error.exception.status_code)

        with Session(engine) as db:
            member = self._principal(db, role="member")
            created = buildings_router.create_building(
                BuildingStructureCreate(
                    id="building_member_allowed",
                    home_id="home_001",
                    name="Member Allowed",
                    type="workshop",
                ),
                db,
                member,
            )
            with self.assertRaises(HTTPException) as cross_home_error:
                loads_router.update_load("load_001", LoadUpdate(building_id="building_other"), db, member)

        self.assertEqual("building_member_allowed", created.id)
        self.assertEqual(403, cross_home_error.exception.status_code)

    def test_privacy_export_and_delete_are_owner_only(self):
        with Session(engine) as db:
            viewer = self._principal(db, role="viewer")
            owner = self._principal(db, role="owner")

            with self.assertRaises(HTTPException) as export_error:
                privacy_router.export_homeowner_record("home_001", db, viewer)
            with self.assertRaises(HTTPException) as delete_error:
                privacy_router.delete_homeowner_record("home_001", db, viewer)
            exported = privacy_router.export_homeowner_record("home_001", db, owner)
            deleted = privacy_router.delete_homeowner_record("home_001", db, owner)

        self.assertEqual(403, export_error.exception.status_code)
        self.assertEqual(403, delete_error.exception.status_code)
        self.assertEqual("home_001", exported.exported_sections["home"]["id"])
        self.assertTrue(deleted.deleted)

    def _principal(self, db, role):
        self._add_user_identity_membership(db, f"user_test_{role}", f"subject_test_{role}", role=role)
        principal = principal_from_verified_claims(
            db,
            VerifiedIdentityClaims(issuer="test_issuer", subject=f"subject_test_{role}"),
            auth_source="fake_oidc_bearer",
        )
        self.assertIsNotNone(principal)
        return principal

    def _principal_without_membership(self, db):
        now = datetime.utcnow()
        db.add(
            models.User(
                id="user_no_membership",
                primary_email="nomembership@example.com",
                display_name="No Membership",
                status="active",
            )
        )
        db.add(
            models.OAuthIdentity(
                id="identity_no_membership",
                user_id="user_no_membership",
                provider="fake_oidc",
                issuer="test_issuer",
                subject="subject_no_membership",
                email="nomembership@example.com",
                email_verified=True,
                last_seen_at=now,
            )
        )
        db.commit()
        principal = principal_from_verified_claims(
            db,
            VerifiedIdentityClaims(issuer="test_issuer", subject="subject_no_membership"),
            auth_source="fake_oidc_bearer",
        )
        self.assertIsNotNone(principal)
        return principal

    def _add_user_identity_membership(self, db, user_id, subject, role):
        now = datetime.utcnow()
        db.add(
            models.User(
                id=user_id,
                primary_email=f"{user_id}@example.com",
                display_name=f"{role.title()} User",
                status="active",
            )
        )
        db.add(
            models.OAuthIdentity(
                id=f"identity_{user_id}",
                user_id=user_id,
                provider="fake_oidc",
                issuer="test_issuer",
                subject=subject,
                email=f"{user_id}@example.com",
                email_verified=True,
                last_seen_at=now,
            )
        )
        db.add(
            models.AccountMembership(
                id=f"membership_{user_id}",
                account_id="account_demo",
                user_id=user_id,
                role=role,
                status="active",
            )
        )
        db.commit()

    def _add_extra_scope_records(self, db):
        db.add(
            models.Account(
                id="account_other",
                email="other@example.com",
                name="Other Account",
                role="homeowner",
                subscription_status="active",
                plan_type="demo",
            )
        )
        db.add(
            models.Home(
                id="home_other",
                account_id="account_other",
                name="Other Home",
                address_line_1="2 Other St",
                city="Other",
                state="CA",
                postal_code="90002",
                country="US",
            )
        )
        db.add(
            models.Home(
                id="home_null",
                account_id=None,
                name="Unassigned Home",
                address_line_1="3 Null St",
                city="Nowhere",
                state="CA",
                postal_code="90003",
                country="US",
            )
        )
        db.add(
            models.EnergySystemDesign(
                id="design_other",
                home_id="home_other",
                name="Other Design",
                design_goal="partial_backup",
                architecture_type="ac_coupled",
                status="draft",
            )
        )
        db.add(
            models.EnergySystemDesign(
                id="design_null",
                home_id="home_null",
                name="Null Home Design",
                design_goal="partial_backup",
                architecture_type="ac_coupled",
                status="draft",
            )
        )
        db.add(
            models.Scenario(
                id="scenario_other",
                home_id="home_other",
                name="Other Scenario",
                description="Other account scenario.",
                linked_design_id="design_other",
            )
        )
        db.add(
            models.Scenario(
                id="scenario_null",
                home_id="home_null",
                name="Null Home Scenario",
                description="Unassigned home scenario.",
                linked_design_id="design_null",
            )
        )
        db.add(
            models.BuildingStructure(
                id="building_other",
                home_id="home_other",
                name="Other Building",
                type="main_house",
            )
        )
        db.add(
            models.BuildingStructure(
                id="building_null",
                home_id="home_null",
                name="Null Building",
                type="main_house",
            )
        )
        db.add(
            models.ElectricalPanel(
                id="panel_other",
                home_id="home_other",
                building_id="building_other",
                panel_type="main_service_panel",
                amperage=200,
                breaker_spaces_total=40,
                breaker_spaces_available=8,
                indoor_outdoor="indoor",
            )
        )
        db.add(
            models.ElectricalPanel(
                id="panel_null",
                home_id="home_null",
                building_id="building_null",
                panel_type="main_service_panel",
                amperage=200,
                breaker_spaces_total=40,
                breaker_spaces_available=8,
                indoor_outdoor="indoor",
            )
        )
        db.add(
            models.Load(
                id="load_other",
                home_id="home_other",
                building_id="building_other",
                name="Other Load",
                category="other",
                running_watts=9999,
                backup_priority="optional",
                phase_type="split_phase",
            )
        )
        db.add(
            models.Load(
                id="load_null",
                home_id="home_null",
                building_id="building_null",
                name="Null Load",
                category="other",
                running_watts=8888,
                backup_priority="optional",
                phase_type="split_phase",
            )
        )
        db.add(
            models.EquipmentLocation(
                id="location_other",
                home_id="home_other",
                building_id="building_other",
                name="Other Location",
                location_type="other",
            )
        )
        db.add(
            models.EquipmentLocation(
                id="location_null",
                home_id="home_null",
                building_id="building_null",
                name="Null Location",
                location_type="other",
            )
        )
        db.add(
            models.EstimatedPathway(
                id="pathway_other",
                home_id="home_other",
                design_id="design_other",
                name="Other Pathway",
                description="Other account pathway.",
                lifecycle_stage="concept",
            )
        )
        db.add(
            models.EstimatedPathway(
                id="pathway_null",
                home_id="home_null",
                design_id="design_null",
                name="Null Pathway",
                description="Unassigned pathway.",
                lifecycle_stage="concept",
            )
        )
        db.add(
            models.CompatibilityIssue(
                id="issue_other",
                design_id="design_other",
                severity="warning",
                category="expansion",
                issue="Other account issue.",
                why_it_matters="Other account issue.",
                possible_solutions=["Keep separate."],
                tradeoff="Other account tradeoff.",
                related_equipment_ids=[],
            )
        )
        db.add(
            models.CompatibilityIssue(
                id="issue_null",
                design_id="design_null",
                severity="warning",
                category="expansion",
                issue="Null account issue.",
                why_it_matters="Null account issue.",
                possible_solutions=["Assign account before access."],
                tradeoff="Null account tradeoff.",
                related_equipment_ids=[],
            )
        )
        db.add(
            models.TakeoffRequest(
                id="takeoff_other",
                design_id="design_other",
                status="placeholder",
                requested_by="test",
            )
        )
        db.add(
            models.TakeoffLineItem(
                id="takeoff_line_other",
                takeoff_request_id="takeoff_other",
                category="other",
                item_name="Other Line",
                quantity=1,
                unit="each",
            )
        )
        db.commit()


if __name__ == "__main__":
    unittest.main()
