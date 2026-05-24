from typing import Dict, List

from app.scenarios.schemas import Scenario


class ScenarioComparisonService:
    def compare(self, scenarios: List[Scenario]) -> Dict[str, object]:
        return {
            "status": "placeholder",
            "comparison_dimensions": [
                "upfront_cost_placeholder",
                "future_expansion_score",
                "install_complexity_score",
                "backup_capability_score",
            ],
            "scenarios": [Scenario.from_orm(scenario).dict() for scenario in scenarios],
        }


scenario_comparison_service = ScenarioComparisonService()

