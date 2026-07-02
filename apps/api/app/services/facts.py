from datetime import datetime
from typing import Dict, Iterable, List, Optional

from sqlalchemy.orm import Session

from app.core import models
from app.core.repository import repository
from app.core.types import FactConfidenceTier, FactDecayPolicy
from app.facts.schemas import EffectiveFact, Fact, FactGap, FactGapsResponse

CONFIDENCE_SCORES = {
    FactConfidenceTier.known: 1.0,
    FactConfidenceTier.derived: 0.72,
    FactConfidenceTier.assumed: 0.38,
    FactConfidenceTier.missing: 0.0,
}

DEFAULT_DECAY_BY_KEY = {
    "service.main_breaker_amps": FactDecayPolicy.no_decay,
    "service.busbar_rating_amps": FactDecayPolicy.no_decay,
    "roof.azimuth_degrees": FactDecayPolicy.slow_decay,
    "roof.pitch_degrees": FactDecayPolicy.slow_decay,
    "load.monthly_kwh": FactDecayPolicy.fast_decay,
    "load.hvac_tonnage": FactDecayPolicy.standard_decay,
}

CALCULATION_REQUIREMENTS = {
    "nec_220_82": {
        "required": [
            "home.conditioned_floor_area_sqft",
            "service.main_breaker_amps",
        ],
        "defaultable": [
            "service.nominal_voltage",
            "load.small_appliance_circuits",
            "load.laundry_circuits",
            "load.range_va",
            "load.dryer_va",
            "load.evse_va",
            "load.other_va",
            "load.added_load_va",
            "load.hvac_heating_va",
            "load.hvac_cooling_va",
            "load.fixed_appliance_va",
        ],
    },
    "nec_220_83": {
        "required": [
            "home.conditioned_floor_area_sqft",
            "service.main_breaker_amps",
        ],
        "defaultable": [
            "service.nominal_voltage",
            "load.small_appliance_circuits",
            "load.laundry_circuits",
            "load.range_va",
            "load.dryer_va",
            "load.evse_va",
            "load.other_va",
            "load.added_load_va",
            "load.hvac_heating_va",
            "load.hvac_cooling_va",
            "load.fixed_appliance_va",
        ],
    },
    "battery_backup_sizing": {
        "required": [
            "load.critical_continuous_watts",
            "load.critical_peak_watts",
            "backup.target_autonomy_hours",
        ],
        "defaultable": [
            "battery.round_trip_efficiency",
            "battery.depth_of_discharge_floor",
        ],
    },
}


def _tier_from_score(score: float) -> FactConfidenceTier:
    if score >= 0.8:
        return FactConfidenceTier.known
    if score >= 0.55:
        return FactConfidenceTier.derived
    if score >= 0.2:
        return FactConfidenceTier.assumed
    return FactConfidenceTier.missing


class FactLifecycleService:
    def create_fact(self, db: Session, home_id: str, payload):
        now = datetime.utcnow()
        fact = models.Fact(
            home_id=home_id,
            verified_at=now,
            **payload.model_dump(),
        )
        return repository.create_fact(db, fact)

    def update_fact(self, db: Session, fact_id: str, payload):
        fact = repository.get_fact(db, fact_id)
        if fact is None:
            return None
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(fact, field, value)
        fact.verified_at = datetime.utcnow()
        return repository.save_fact(db, fact)

    def effective_facts_for_home(
        self,
        db: Session,
        home_id: str,
        now: Optional[datetime] = None,
    ) -> List[EffectiveFact]:
        return [self.apply_effective_confidence(fact, now=now) for fact in repository.list_facts(db, home_id)]

    def apply_effective_confidence(
        self,
        fact: models.Fact,
        now: Optional[datetime] = None,
    ) -> EffectiveFact:
        now = now or datetime.utcnow()
        stored_tier = FactConfidenceTier(fact.confidence_tier)
        policy = self._policy_for_fact(fact)
        base_score = CONFIDENCE_SCORES[stored_tier]

        if stored_tier == FactConfidenceTier.missing:
            factor = 0.0
            reason = "Stored confidence tier is missing."
        elif fact.expires_at and fact.expires_at <= now:
            factor = 0.0
            reason = "Fact expired before the read timestamp."
        else:
            factor = self._decay_factor(policy, fact.verified_at, now)
            reason = f"Applied {policy.value} from verified_at to read time."

        effective_score = round(base_score * factor, 4)
        stored_fact = Fact.model_validate(fact)
        return EffectiveFact(
            **stored_fact.model_dump(),
            effective_confidence_score=effective_score,
            effective_confidence_tier=_tier_from_score(effective_score),
            effective_confidence_reason=reason,
            decay_policy_applied=policy,
        )

    def fact_gaps(self, db: Session, home_id: str, calculation_name: str) -> Optional[FactGapsResponse]:
        requirement = CALCULATION_REQUIREMENTS.get(calculation_name)
        if requirement is None:
            return None

        effective_by_key: Dict[str, EffectiveFact] = {
            fact.key: fact for fact in self.effective_facts_for_home(db, home_id)
        }
        present_keys = sorted(effective_by_key.keys())
        gaps = self._build_gaps(
            requirement["required"],
            requirement["defaultable"],
            effective_by_key,
        )
        return FactGapsResponse(
            home_id=home_id,
            calculation_name=calculation_name,
            required_keys=requirement["required"],
            defaultable_keys=requirement["defaultable"],
            present_keys=present_keys,
            gaps=gaps,
            ready=not any(gap.required and gap.status != "present" for gap in gaps),
            limitations=[
                "Gap readiness reflects fact availability and effective confidence only.",
                "It is not engineering approval, field verification, AHJ approval, or permission enforcement.",
            ],
        )

    def _policy_for_fact(self, fact: models.Fact) -> FactDecayPolicy:
        if fact.decay_policy:
            return FactDecayPolicy(fact.decay_policy)
        return DEFAULT_DECAY_BY_KEY.get(fact.key, FactDecayPolicy.standard_decay)

    def _decay_factor(
        self,
        policy: FactDecayPolicy,
        verified_at: datetime,
        now: datetime,
    ) -> float:
        if policy == FactDecayPolicy.no_decay:
            return 1.0

        elapsed_days = max((now - verified_at).total_seconds() / 86400, 0)
        windows = {
            FactDecayPolicy.slow_decay: 3650,
            FactDecayPolicy.standard_decay: 1095,
            FactDecayPolicy.fast_decay: 365,
        }
        window = windows[policy]
        return max(1.0 - (elapsed_days / window), 0.0)

    def _build_gaps(
        self,
        required_keys: Iterable[str],
        defaultable_keys: Iterable[str],
        effective_by_key: Dict[str, EffectiveFact],
    ) -> List[FactGap]:
        gaps: List[FactGap] = []
        for key in required_keys:
            fact = effective_by_key.get(key)
            status = self._status_for_fact(fact)
            if status != "present":
                gaps.append(
                    FactGap(
                        key=key,
                        required=True,
                        defaultable=False,
                        status=status,
                        reason=self._gap_reason(status, defaultable=False),
                    )
                )
        for key in defaultable_keys:
            fact = effective_by_key.get(key)
            status = self._status_for_fact(fact)
            if status != "present":
                gaps.append(
                    FactGap(
                        key=key,
                        required=False,
                        defaultable=True,
                        status=status,
                        reason=self._gap_reason(status, defaultable=True),
                    )
                )
        return gaps

    def _status_for_fact(self, fact: Optional[EffectiveFact]) -> str:
        if fact is None:
            return "missing"
        if fact.effective_confidence_tier == FactConfidenceTier.missing:
            return "effectively_missing"
        return "present"

    def _gap_reason(self, status: str, defaultable: bool) -> str:
        if status == "effectively_missing":
            basis = "Recorded fact exists but confidence has decayed to missing."
        else:
            basis = "No recorded fact is available for this calculation key."
        if defaultable:
            return f"{basis} A documented default may be substituted by the calculation."
        return f"{basis} The calculation should report a gap until this fact is supplied."


fact_lifecycle_service = FactLifecycleService()
