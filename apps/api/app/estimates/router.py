from fastapi import APIRouter

router = APIRouter(prefix="/estimates", tags=["estimates"])


@router.get("/placeholder")
def estimate_placeholder():
    return {
        "status": "placeholder",
        "message": "Estimate generation is intentionally deferred until takeoff structure and pricing sources are formalized.",
    }

