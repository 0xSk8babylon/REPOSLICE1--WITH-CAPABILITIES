import unittest

from app.engines.sizers import (
    check_transformer_headroom,
    size_battery,
    size_generator,
    size_v2h_coverage,
)


class SizerTests(unittest.TestCase):
    def test_battery_hours_to_kwh_includes_efficiency_and_dod(self):
        result = size_battery(
            critical_load_kwh_per_hour=1.5,
            target_autonomy_hours=8,
            round_trip_efficiency=0.92,
            depth_of_discharge_fraction=0.9,
            confidence_tier="derived",
        )

        self.assertEqual(13.04, result.required_usable_kwh)
        self.assertEqual(14.49, result.required_nameplate_kwh)
        self.assertEqual((13.77, 16.67), result.recommended_capacity_band_kwh)
        self.assertIn("No SGIP", result.assumptions[2])

    def test_generator_standalone_sizes_to_surge_with_derate(self):
        result = size_generator(continuous_load_kw=6, surge_load_kw=10, derate_factor=0.8, mode="standalone", confidence_tier="known")

        self.assertEqual(12.5, result.recommended_kw)

    def test_generator_hybrid_assumes_battery_surge_support(self):
        result = size_generator(continuous_load_kw=6, surge_load_kw=10, derate_factor=0.8, mode="hybrid", confidence_tier="known")

        self.assertEqual(7.5, result.recommended_kw)

    def test_v2h_reports_power_limited_coverage(self):
        result = size_v2h_coverage(vehicle_usable_kwh=60, discharge_power_kw=5, critical_load_kw=6, confidence_tier="assumed")

        self.assertEqual(10.0, result.coverage_hours)
        self.assertTrue(result.power_limited)
        self.assertEqual("V2H/V2L power-limit review", result.architecture_implication)

    def test_transformer_headroom_statuses(self):
        available = check_transformer_headroom(50, proposed_peak_kw=10, existing_peak_kw=20, power_factor=0.9, confidence_tier="derived")
        tight = check_transformer_headroom(50, proposed_peak_kw=20, existing_peak_kw=24, power_factor=0.9, confidence_tier="derived")
        review = check_transformer_headroom(50, proposed_peak_kw=30, existing_peak_kw=20, power_factor=0.9, confidence_tier="derived")

        self.assertEqual("headroom_available", available.status)
        self.assertEqual("tight_review_needed", tight.status)
        self.assertEqual("utility_review_needed", review.status)


if __name__ == "__main__":
    unittest.main()
