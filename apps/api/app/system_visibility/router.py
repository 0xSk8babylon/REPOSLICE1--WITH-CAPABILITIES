from fastapi import APIRouter

from app.services.system_visibility import system_visibility_service
from app.system_visibility.schemas import ArchitectureVisibilityGraph

router = APIRouter(prefix="/system-visibility", tags=["system_visibility"])


@router.get("/architecture", response_model=ArchitectureVisibilityGraph)
def get_architecture_visibility():
    return system_visibility_service.build_architecture_graph()
