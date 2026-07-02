import unittest
from datetime import datetime

from sqlalchemy.orm import Session  # noqa: E402

import tests.fast_db  # noqa: F401, E402  must precede app imports
from app.core import models  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.core.types import FactConfidenceTier, FactSource  # noqa: E402
from app.main import app  # noqa: E402
from app.nec_load_calculation.router import get_nec_220_load_calculation  # noqa: E402

HOME_ID = "home_001"


class NecLoadCalculationTests(unittest.TestCase):
    def setUp(self):
        with Session(engine) as db:
            db.query(models.Fact).delete()
            db.commit()

    def _add_fact(self, key, value, unit=None, tier=FactConfidenceTier.known, source=FactSource.contractor_measured):
        with Session(engine) as db:
            fact = models.Fact(
                id=f"fact_{key.replace('.', '_')}",
                home_id=HOME_ID,
                key=key,
                value=value,
                unit=unit,
                source=source.value,
                confidence_tier=tier.value,
                verified_at=datetime(2026, 6, 13),
                derived_from=[],
            )
            db.add(fact)
            db.commit()

    def _seed_worked_example(self):
        self._add_fact("home.conditioned_floor_area_sqft", 2000, "sqft")
        self._add_fact("service.main_breaker_amps", 200, "A")
        self._add_fact("load.fixed_appliance_va", 6000, "VA")
        self._add_fact("load.range_va", 12000, "VA")
        self._add_fact("load.dryer_va", 5000, "VA")
        self._add_fact("load.hvac_heating_va", 8000, "VA")
        self._add_fact("load.hvac_cooling_va", 6000, "VA")

    def test_route_registration(self):
        paths = set(app.openapi()["paths"])
        self.assertIn("/api/homes/{home_id}/load-calculations/nec-220", paths)

    def test_220_82_worked_example_returns_stage_values_and_headroom(self):
        self._seed_worked_example()

        with Session(engine) as db:
            response = get_nec_220_load_calculation(HOME_ID, db)

        result = next(item for item in response.results if item.method == "220.82")
        stages = {stage.stage: stage.va for stage in result.stages}

        self.assertTrue(result.calculation_ready)
        self.assertEqual(27400.0, result.calculated_service_load_va)
        self.assertEqual(114.17, result.calculated_service_load_amps)
        self.assertEqual(85.83, result.headroom_amps)
        self.assertEqual(6000.0, stages["general_lighting"])
        self.assertEqual(4500.0, stages["small_appliance_and_laundry"])
        self.assertEqual(23000.0, stages["appliance_and_other_loads"])
        self.assertEqual(19400.0, stages["general_load_demand"])
        self.assertEqual(8000.0, stages["larger_of_heating_or_cooling"])

    def test_220_83_uses_existing_dwelling_demand_threshold(self):
        self._seed_worked_example()

        with Session(engine) as db:
            response = get_nec_220_load_calculation(HOME_ID, db)

        result = next(item for item in response.results if item.method == "220.83")

        self.assertTrue(result.calculation_ready)
        self.assertEqual(26200.0, result.calculated_service_load_va)
        self.assertEqual(109.17, result.calculated_service_load_amps)
        self.assertEqual(90.83, result.headroom_amps)

    def test_missing_required_facts_report_gaps_without_calculation(self):
        self._add_fact("home.conditioned_floor_area_sqft", 1800, "sqft")

        with Session(engine) as db:
            response = get_nec_220_load_calculation(HOME_ID, db)

        for result in response.results:
            self.assertFalse(result.calculation_ready)
            self.assertIsNone(result.calculated_service_load_amps)
            self.assertEqual(["service.main_breaker_amps"], [gap.key for gap in result.gaps])
            self.assertEqual(FactConfidenceTier.missing, result.output_confidence_tier)

    def test_defaultable_inputs_are_reported_as_assumptions_and_confidence_floor(self):
        self._add_fact("home.conditioned_floor_area_sqft", 1000, "sqft")
        self._add_fact("service.main_breaker_amps", 100, "A")

        with Session(engine) as db:
            response = get_nec_220_load_calculation(HOME_ID, db)

        result = next(item for item in response.results if item.method == "220.82")
        assumption_keys = {assumption.key for assumption in result.assumptions}

        self.assertTrue(result.calculation_ready)
        self.assertIn("load.small_appliance_circuits", assumption_keys)
        self.assertIn("load.laundry_circuits", assumption_keys)
        self.assertEqual(FactConfidenceTier.assumed, result.output_confidence_tier)

    def test_response_preserves_non_authoritative_boundary(self):
        self._seed_worked_example()

        with Session(engine) as db:
            response = get_nec_220_load_calculation(HOME_ID, db)

        self.assertIn("Planning calculation only", response.compliance_boundary)
        self.assertIn("professional review", response.results[0].limitations[0])
        self.assertTrue(response.source_basis)


if __name__ == "__main__":
    unittest.main()
