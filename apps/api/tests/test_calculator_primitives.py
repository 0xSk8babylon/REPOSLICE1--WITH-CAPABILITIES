import unittest

from app.engines.calculator_primitives import (
    LoadCandidate,
    calculate_120_percent_backfeed,
    calculate_supply_side_tap,
    decide_coupling,
    estimate_solar_production,
    identify_critical_loads,
    tier1_shading_derate,
)


class CalculatorPrimitivesTests(unittest.TestCase):
    def test_backfeed_rule_passes_at_exact_limit(self):
        result = calculate_120_percent_backfeed(200, 200, requested_backfeed_amps=40)

        self.assertTrue(result.passes)
        self.assertEqual(40.0, result.maximum_backfeed_amps)
        self.assertFalse(result.supply_side_tap_alternative)

    def test_backfeed_rule_returns_supply_side_alternative_on_failure(self):
        result = calculate_120_percent_backfeed(200, 200, requested_backfeed_amps=60)

        self.assertFalse(result.passes)
        self.assertTrue(result.supply_side_tap_alternative)

    def test_supply_side_tap_flags_review_items(self):
        result = calculate_supply_side_tap(200, 60)

        self.assertEqual("requires_professional_review", result.planning_status)
        self.assertIn("overcurrent_protection", result.required_review_items)

    def test_supply_side_tap_blocks_non_positive_request(self):
        result = calculate_supply_side_tap(200, 0)

        self.assertEqual("blocked", result.planning_status)

    def test_coupling_decision_favors_ac_for_retrofit_pv(self):
        result = decide_coupling(array_kw_dc=8, battery_kwh=13.5, has_existing_pv=True, retrofit=True)

        self.assertEqual("ac_coupled", result.recommended_coupling)
        self.assertFalse(result.review_flags)

    def test_critical_loads_selects_by_backup_goal(self):
        loads = [
            LoadCandidate("fridge", "Fridge", 600, 1200, "essential"),
            LoadCandidate("lights", "Lights", 300, None, "preferred"),
            LoadCandidate("spa", "Spa", 5000, 7000, "non_backup"),
        ]

        result = identify_critical_loads(loads, backup_goal="partial_home")

        self.assertEqual(("fridge", "lights"), result.selected_load_ids)
        self.assertEqual(900, result.continuous_watts)
        self.assertEqual(1500, result.peak_watts)

    def test_tier1_shading_zero_and_full_boundaries(self):
        no_shade = tier1_shading_derate([(90, 0), (180, 0)])
        full_shade = tier1_shading_derate([(90, 90), (180, 90)])

        self.assertEqual(0.0, no_shade.derate_fraction)
        self.assertEqual(1.0, no_shade.production_factor)
        self.assertEqual(1.0, full_shade.derate_fraction)
        self.assertEqual(0.0, full_shade.production_factor)

    def test_tier1_shading_clamps_obstruction_elevations(self):
        result = tier1_shading_derate([(90, -10), (180, 120)])

        self.assertEqual(0.5, result.derate_fraction)
        self.assertEqual(0.5, result.production_factor)

    def test_solar_production_uses_simplified_model(self):
        result = estimate_solar_production(
            array_kw_dc=10,
            derate_factor=0.8,
            monthly_specific_yield=[100] * 12,
        )

        self.assertEqual(9600.0, result.annual_kwh)
        self.assertEqual(800.0, result.monthly_kwh[0])
        self.assertEqual("simplified_specific_yield_model", result.source)

    def test_solar_production_uses_injected_estimator_without_network(self):
        calls = []

        def fake_pvwatts(array_kw_dc, derate_factor):
            calls.append((array_kw_dc, derate_factor))
            return [array_kw_dc * derate_factor] * 12

        result = estimate_solar_production(7.5, 0.9, pvwatts_estimator=fake_pvwatts)

        self.assertEqual([(7.5, 0.9)], calls)
        self.assertEqual(81.0, result.annual_kwh)
        self.assertEqual("injected_pvwatts_estimator", result.source)


if __name__ == "__main__":
    unittest.main()
