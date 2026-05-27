from fastapi import APIRouter

router = APIRouter(prefix="/estimates", tags=["estimates"])


@router.get("/placeholder")
def estimate_placeholder():
    return {
        "status": "placeholder",
        "authority_layer": "advisory",
        "data_classification": "planning_private",
        "derivation_type": "not_available",
        "message": "Estimate generation is intentionally deferred until takeoff structure and pricing sources are formalized.",
        "limitations": [
            "No estimate engine, pricing source, contractor packet, utility export, or operational authorization exists for this endpoint.",
        ],
    }
