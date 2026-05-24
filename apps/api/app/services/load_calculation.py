from typing import Dict, List

from app.loads.schemas import Load


class LoadCalculationService:
    def summarize(self, loads: List[Load]) -> Dict[str, float]:
        total_running_watts = sum(item.running_watts for item in loads)
        total_surge_watts = sum(item.surge_watts or item.running_watts for item in loads)
        return {
            "total_running_watts": total_running_watts,
            "total_surge_watts": total_surge_watts,
        }


load_calculation_service = LoadCalculationService()

