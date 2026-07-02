from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.core.types import FactConfidenceTier
from app.facts.schemas import EffectiveFact, FactGap
from app.nec_load_calculation.schemas import (
    CalculationAssumption,
    ConsumedFact,
    NecLoadCalculationResponse,
    NecLoadMethodResult,
    NecLoadStage,
)
from app.services.facts import fact_lifecycle_service

REQUIRED_FACT_KEYS = [
    "home.conditioned_floor_area_sqft",
    "service.main_breaker_amps",
]

DEFAULTS = {
    "service.nominal_voltage": (240, "V", "Default residential split-phase service voltage for planning calculation."),
    "load.small_appliance_circuits": (2, "circuits", "Minimum dwelling small-appliance branch-circuit count used for planning."),
    "load.laundry_circuits": (1, "circuits", "Minimum dwelling laundry branch-circuit count used for planning."),
    "load.fixed_appliance_va": (0, "VA", "No fixed-appliance load fact was supplied."),
    "load.range_va": (0, "VA", "No range/cooking equipment load fact was supplied."),
    "load.dryer_va": (0, "VA", "No dryer load fact was supplied."),
    "load.evse_va": (0, "VA", "No EVSE load fact was supplied."),
    "load.other_va": (0, "VA", "No other load fact was supplied."),
    "load.added_load_va": (0, "VA", "No additional existing-dwelling load fact was supplied."),
    "load.hvac_heating_va": (0, "VA", "No heating load fact was supplied."),
    "load.hvac_cooling_va": (0, "VA", "No cooling load fact was supplied."),
}

CONFIDENCE_ORDER = {
    FactConfidenceTier.known: 4,
    FactConfidenceTier.derived: 3,
    FactConfidenceTier.assumed: 2,
    FactConfidenceTier.missing: 1,
}


class NecLoadCalculationService:
    def calculate(self, db: Session, home_id: str) -> NecLoadCalculationResponse:
        facts = fact_lifecycle_service.effective_facts_for_home(db, home_id)
        fact_by_key = {fact.key: fact for fact in facts}
        voltage, voltage_consumed, voltage_assumption = self._value_for_key(
            fact_by_key,
            "service.nominal_voltage",
        )

        results = [
            self._calculate_method("220.82", fact_by_key, voltage),
            self._calculate_method("220.83", fact_by_key, voltage),
        ]
        if voltage_consumed is not None:
            for result in results:
                if result.calculation_ready:
                    result.consumed_facts.append(voltage_consumed)
        if voltage_assumption is not None:
            for result in results:
                if result.calculation_ready:
                    result.assumptions.append(voltage_assumption)
                    result.output_confidence_tier = self._weakest_confidence(result)

        missing_data = sorted({gap.key for result in results for gap in result.gaps})
        return NecLoadCalculationResponse(
            home_id=home_id,
            voltage=float(voltage),
            results=results,
            source_basis=[
                "NFPA 70 National Electrical Code Article 220 dwelling service/feeder load calculation concepts.",
                "B1 Fact Lifecycle effective confidence values and derived-from lineage.",
                "Matt-approved session override for NEC/calculation implementation; output remains non-authoritative.",
            ],
            compliance_boundary=(
                "Planning calculation only. It is not a stamped load calculation, permit-ready design, "
                "field verification, AHJ approval, utility approval, or substitute for a qualified electrician or engineer."
            ),
            missing_data=missing_data,
        )

    def _calculate_method(
        self,
        method: str,
        fact_by_key: Dict[str, EffectiveFact],
        voltage: float,
    ) -> NecLoadMethodResult:
        consumed: List[ConsumedFact] = []
        assumptions: List[CalculationAssumption] = []
        gaps = self._required_gaps(fact_by_key)
        if gaps:
            return NecLoadMethodResult(
                method=method,
                calculation_ready=False,
                consumed_facts=consumed,
                assumptions=assumptions,
                gaps=gaps,
                limitations=self._limitations(),
            )

        values = {}
        for key in REQUIRED_FACT_KEYS + list(DEFAULTS.keys()):
            if key == "service.nominal_voltage":
                continue
            value, consumed_fact, assumption = self._value_for_key(fact_by_key, key)
            values[key] = value
            if consumed_fact is not None:
                consumed.append(consumed_fact)
            if assumption is not None:
                assumptions.append(assumption)

        general_lighting_va = values["home.conditioned_floor_area_sqft"] * 3
        small_appliance_va = values["load.small_appliance_circuits"] * 1500
        laundry_va = values["load.laundry_circuits"] * 1500
        appliance_va = (
            values["load.fixed_appliance_va"]
            + values["load.range_va"]
            + values["load.dryer_va"]
            + values["load.evse_va"]
            + values["load.other_va"]
        )
        if method == "220.83":
            appliance_va += values["load.added_load_va"]

        general_total = general_lighting_va + small_appliance_va + laundry_va + appliance_va
        threshold = 10000 if method == "220.82" else 8000
        demand_va = min(general_total, threshold) + max(general_total - threshold, 0) * 0.4
        hvac_va = max(values["load.hvac_heating_va"], values["load.hvac_cooling_va"])
        total_va = demand_va + hvac_va
        amps = total_va / voltage
        service_amps = values["service.main_breaker_amps"]

        return NecLoadMethodResult(
            method=method,
            calculation_ready=True,
            calculated_service_load_va=round(total_va, 2),
            calculated_service_load_amps=round(amps, 2),
            existing_service_amps=float(service_amps),
            headroom_amps=round(service_amps - amps, 2),
            stages=[
                NecLoadStage(
                    stage="general_lighting",
                    va=round(general_lighting_va, 2),
                    formula="conditioned_floor_area_sqft * 3 VA",
                    basis_keys=["home.conditioned_floor_area_sqft"],
                ),
                NecLoadStage(
                    stage="small_appliance_and_laundry",
                    va=round(small_appliance_va + laundry_va, 2),
                    formula="small_appliance_circuits * 1500 VA + laundry_circuits * 1500 VA",
                    basis_keys=["load.small_appliance_circuits", "load.laundry_circuits"],
                ),
                NecLoadStage(
                    stage="appliance_and_other_loads",
                    va=round(appliance_va, 2),
                    formula="sum of fixed appliance, range, dryer, EVSE, other, and method-specific added load facts",
                    basis_keys=[
                        "load.fixed_appliance_va",
                        "load.range_va",
                        "load.dryer_va",
                        "load.evse_va",
                        "load.other_va",
                        "load.added_load_va",
                    ],
                ),
                NecLoadStage(
                    stage="general_load_demand",
                    va=round(demand_va, 2),
                    formula=f"first {threshold} VA at 100%, remainder at 40%",
                    basis_keys=["general_lighting", "small_appliance_and_laundry", "appliance_and_other_loads"],
                ),
                NecLoadStage(
                    stage="larger_of_heating_or_cooling",
                    va=round(hvac_va, 2),
                    formula="max(hvac_heating_va, hvac_cooling_va)",
                    basis_keys=["load.hvac_heating_va", "load.hvac_cooling_va"],
                ),
            ],
            consumed_facts=consumed,
            assumptions=assumptions,
            output_confidence_tier=self._weakest_confidence_values(consumed, assumptions),
            limitations=self._limitations(),
        )

    def _required_gaps(self, fact_by_key: Dict[str, EffectiveFact]) -> List[FactGap]:
        gaps = []
        for key in REQUIRED_FACT_KEYS:
            fact = fact_by_key.get(key)
            if fact is None:
                gaps.append(
                    FactGap(
                        key=key,
                        required=True,
                        defaultable=False,
                        status="missing",
                        reason="No recorded fact is available and no planning default is used for this required input.",
                    )
                )
            elif fact.effective_confidence_tier == FactConfidenceTier.missing:
                gaps.append(
                    FactGap(
                        key=key,
                        required=True,
                        defaultable=False,
                        status="effectively_missing",
                        reason="Recorded fact exists but effective confidence has decayed to missing.",
                    )
                )
        return gaps

    def _value_for_key(self, fact_by_key: Dict[str, EffectiveFact], key: str):
        fact = fact_by_key.get(key)
        if fact is not None and fact.effective_confidence_tier != FactConfidenceTier.missing:
            return self._numeric_value(fact.value), self._consumed_fact(fact), None

        default = DEFAULTS.get(key)
        if default is None:
            return None, None, None
        value, unit, reason = default
        return (
            value,
            None,
            CalculationAssumption(key=key, value=value, unit=unit, reason=reason),
        )

    def _numeric_value(self, value: Any) -> float:
        if isinstance(value, dict):
            for field in ["value", "amount", "va", "amps"]:
                if field in value:
                    return float(value[field])
        return float(value)

    def _consumed_fact(self, fact: EffectiveFact) -> ConsumedFact:
        return ConsumedFact(
            key=fact.key,
            value=fact.value,
            unit=fact.unit,
            source=fact.source.value if hasattr(fact.source, "value") else str(fact.source),
            confidence_tier=fact.confidence_tier,
            effective_confidence_score=fact.effective_confidence_score,
            effective_confidence_tier=fact.effective_confidence_tier,
            derived_from=fact.derived_from,
        )

    def _weakest_confidence(self, result: NecLoadMethodResult) -> FactConfidenceTier:
        return self._weakest_confidence_values(result.consumed_facts, result.assumptions)

    def _weakest_confidence_values(
        self,
        consumed: List[ConsumedFact],
        assumptions: List[CalculationAssumption],
    ) -> FactConfidenceTier:
        tiers = [fact.effective_confidence_tier for fact in consumed]
        tiers.extend(assumption.confidence_tier for assumption in assumptions)
        if not tiers:
            return FactConfidenceTier.missing
        return min(tiers, key=lambda tier: CONFIDENCE_ORDER[tier])

    def _limitations(self) -> List[str]:
        return [
            "Planning calculation only; professional review remains required.",
            "The calculation depends on B1 fact quality and labeled defaults.",
            "Local amendments, AHJ interpretation, equipment-specific instructions, and field conditions are not evaluated.",
        ]


nec_load_calculation_service = NecLoadCalculationService()
