import unittest
from datetime import datetime, timedelta

import tests.fast_db  # noqa: F401, E402  must precede app imports

from sqlalchemy.orm import Session  # noqa: E402

from app.core import models  # noqa: E402
from app.core.database import engine  # noqa: E402
from app.core.types import FactConfidenceTier, FactDecayPolicy, FactSource  # noqa: E402
from app.facts.router import create_fact, get_fact_gaps, list_facts, update_fact  # noqa: E402
from app.facts.schemas import FactCreate, FactUpdate  # noqa: E402
from app.main import app  # noqa: E402
from app.services.facts import fact_lifecycle_service  # noqa: E402


HOME_ID = "home_001"


class FactLifecycleTests(unittest.TestCase):
    def setUp(self):
        with Session(engine) as db:
            db.query(models.Fact).delete()
            db.commit()

    def _create_fact_model(
        self,
        fact_id,
        key,
        confidence_tier=FactConfidenceTier.known,
        decay_policy=None,
        verified_at=None,
        derived_from=None,
        expires_at=None,
    ):
        fact = models.Fact(
            id=fact_id,
            home_id=HOME_ID,
            key=key,
            value={"value": 200},
            unit="A",
            source=FactSource.photo_verified.value,
            confidence_tier=confidence_tier.value,
            verified_at=verified_at or datetime.utcnow(),
            expires_at=expires_at,
            decay_policy=decay_policy.value if decay_policy else None,
            derived_from=derived_from or [],
        )
        with Session(engine) as db:
            db.add(fact)
            db.commit()
            db.refresh(fact)
            return fact

    def test_route_registration(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn("/api/homes/{home_id}/facts", paths)
        self.assertIn("/api/homes/{home_id}/facts/{fact_id}", paths)
        self.assertIn("/api/homes/{home_id}/facts/gaps/{calculation_name}", paths)

    def test_create_fact_sets_verified_at_and_lists_effective_confidence(self):
        payload = FactCreate(
            id="fact_service_main",
            key="service.main_breaker_amps",
            value=200,
            unit="A",
            source=FactSource.photo_verified,
            confidence_tier=FactConfidenceTier.known,
        )

        with Session(engine) as db:
            created = create_fact(HOME_ID, payload, db)
            facts = list_facts(HOME_ID, db)

        self.assertEqual("fact_service_main", created.id)
        self.assertIsNotNone(created.verified_at)
        self.assertEqual(1, len(facts))
        self.assertEqual(FactConfidenceTier.known, facts[0].effective_confidence_tier)
        self.assertEqual(FactDecayPolicy.no_decay, facts[0].decay_policy_applied)

    def test_update_fact_resets_verified_at(self):
        original = datetime.utcnow() - timedelta(days=90)
        self._create_fact_model(
            "fact_update",
            "load.monthly_kwh",
            confidence_tier=FactConfidenceTier.assumed,
            decay_policy=FactDecayPolicy.fast_decay,
            verified_at=original,
        )

        with Session(engine) as db:
            updated = update_fact(
                HOME_ID,
                "fact_update",
                FactUpdate(value=850, confidence_tier=FactConfidenceTier.derived),
                db,
            )

        self.assertEqual(850, updated.value)
        self.assertEqual(FactConfidenceTier.derived.value, updated.confidence_tier)
        self.assertGreater(updated.verified_at, original)

    def test_derived_fact_preserves_parent_fact_ids(self):
        self._create_fact_model("parent_a", "load.critical_continuous_watts")
        self._create_fact_model("parent_b", "backup.target_autonomy_hours")

        payload = FactCreate(
            id="derived_backup_energy",
            key="backup.required_usable_kwh",
            value=13.5,
            unit="kWh",
            source=FactSource.derived,
            confidence_tier=FactConfidenceTier.derived,
            derived_from=["parent_a", "parent_b"],
        )

        with Session(engine) as db:
            created = create_fact(HOME_ID, payload, db)

        self.assertEqual(["parent_a", "parent_b"], created.derived_from)

    def test_decay_policies_cover_no_slow_standard_and_fast(self):
        now = datetime(2026, 6, 13)
        cases = [
            (FactDecayPolicy.no_decay, now - timedelta(days=3650), FactConfidenceTier.known),
            (FactDecayPolicy.slow_decay, now - timedelta(days=365), FactConfidenceTier.known),
            (FactDecayPolicy.standard_decay, now - timedelta(days=730), FactConfidenceTier.assumed),
            (FactDecayPolicy.fast_decay, now - timedelta(days=120), FactConfidenceTier.derived),
        ]

        for index, (policy, verified_at, expected) in enumerate(cases):
            fact = self._create_fact_model(
                f"fact_decay_{index}",
                f"load.decay_case_{index}",
                decay_policy=policy,
                verified_at=verified_at,
            )
            effective = fact_lifecycle_service.apply_effective_confidence(fact, now=now)
            self.assertEqual(expected, effective.effective_confidence_tier)

    def test_known_fact_transitions_to_missing_after_fast_decay_window(self):
        fact = self._create_fact_model(
            "fact_old_load",
            "load.monthly_kwh",
            confidence_tier=FactConfidenceTier.known,
            decay_policy=FactDecayPolicy.fast_decay,
            verified_at=datetime(2020, 1, 1),
        )

        effective = fact_lifecycle_service.apply_effective_confidence(fact, now=datetime(2026, 6, 13))

        self.assertEqual(0.0, effective.effective_confidence_score)
        self.assertEqual(FactConfidenceTier.missing, effective.effective_confidence_tier)

    def test_expires_at_forces_effective_missing(self):
        fact = self._create_fact_model(
            "fact_expired",
            "load.utility_bill_snapshot",
            expires_at=datetime(2025, 1, 1),
        )

        effective = fact_lifecycle_service.apply_effective_confidence(fact, now=datetime(2026, 6, 13))

        self.assertEqual(FactConfidenceTier.missing, effective.effective_confidence_tier)
        self.assertIn("expired", effective.effective_confidence_reason)

    def test_fact_gaps_reports_missing_and_effectively_missing_keys(self):
        self._create_fact_model("fact_sqft", "home.conditioned_floor_area_sqft")
        self._create_fact_model(
            "fact_service_old",
            "service.main_breaker_amps",
            decay_policy=FactDecayPolicy.fast_decay,
            verified_at=datetime(2020, 1, 1),
        )

        with Session(engine) as db:
            response = get_fact_gaps(HOME_ID, "nec_220_82", db)

        gap_status_by_key = {gap.key: gap.status for gap in response.gaps}
        self.assertFalse(response.ready)
        self.assertEqual("effectively_missing", gap_status_by_key["service.main_breaker_amps"])
        self.assertEqual("missing", gap_status_by_key["load.small_appliance_circuits"])


if __name__ == "__main__":
    unittest.main()
