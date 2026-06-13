import unittest

from app.engines.hourly_simulation import BatterySpec, RateStructure, run_hourly_simulation


class HourlySimulationTests(unittest.TestCase):
    def test_flat_rate_simulation_conserves_energy_and_tracks_cycles(self):
        result = run_hourly_simulation(
            load_profile_kwh=[2, 2, 2, 2],
            solar_profile_kwh=[0, 4, 4, 0],
            battery=BatterySpec(usable_kwh=4, power_kw=2, round_trip_efficiency=1.0),
            rate=RateStructure(kind="flat", flat_import_rate=0.25, export_rate=0.05),
            starting_soc_kwh=0,
            input_confidence_tiers=["known", "derived"],
        )

        for flow in result.hours:
            self.assertAlmostEqual(
                flow.solar_kwh + flow.grid_import_kwh + flow.battery_discharge_kwh,
                flow.load_kwh + flow.grid_export_kwh + flow.battery_charge_kwh,
                places=5,
            )
        self.assertEqual(8, result.annual_load_kwh)
        self.assertEqual(8, result.annual_solar_kwh)
        self.assertEqual(2.0, result.annual_grid_import_kwh)
        self.assertEqual(0, result.annual_grid_export_kwh)
        self.assertEqual(100.0, result.self_consumption_percent)
        self.assertEqual(2.0, result.annual_bill_without_system)
        self.assertEqual(1.5, result.annual_bill_delta)
        self.assertEqual(0.5, result.battery_cycles_per_year)
        self.assertEqual("derived", result.confidence_tier)

    def test_tou_rate_uses_hourly_prices(self):
        rates = [0.10] * 24
        rates[1] = 0.50
        result = run_hourly_simulation(
            load_profile_kwh=[1, 1],
            solar_profile_kwh=[0, 0],
            battery=BatterySpec(usable_kwh=0, power_kw=0, round_trip_efficiency=1.0),
            rate=RateStructure(kind="tou", tou_import_rates=rates),
        )

        self.assertEqual(0.60, result.annual_bill)

    def test_tiered_rate_uses_progressive_blocks(self):
        result = run_hourly_simulation(
            load_profile_kwh=[3, 3, 4],
            solar_profile_kwh=[0, 0, 0],
            battery=BatterySpec(usable_kwh=0, power_kw=0, round_trip_efficiency=1.0),
            rate=RateStructure(kind="tiered", tiered_import_rates=[(5, 0.10), (5, 0.20)]),
        )

        self.assertEqual(1.5, result.annual_bill)

    def test_backup_coverage_counts_partial_hour(self):
        result = run_hourly_simulation(
            load_profile_kwh=[1, 1, 1],
            solar_profile_kwh=[0, 0, 0],
            battery=BatterySpec(usable_kwh=2.5, power_kw=2, round_trip_efficiency=1.0),
            rate=RateStructure(kind="flat", flat_import_rate=0.0),
            critical_load_profile_kwh=[1, 1, 1],
        )

        self.assertEqual(2.5, result.backup_coverage_hours)

    def test_rejects_mismatched_profiles(self):
        with self.assertRaises(ValueError):
            run_hourly_simulation(
                load_profile_kwh=[1],
                solar_profile_kwh=[1, 1],
                battery=BatterySpec(usable_kwh=1, power_kw=1, round_trip_efficiency=1.0),
                rate=RateStructure(kind="flat"),
            )


if __name__ == "__main__":
    unittest.main()
