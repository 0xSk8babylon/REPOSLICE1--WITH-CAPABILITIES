from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter

from app.accounts.router import router as accounts_router
from app.ai_context.router import router as ai_context_router
from app.buildings.router import router as buildings_router
from app.compatibility_rules.router import router as compatibility_router
from app.contractor_context.router import router as contractor_context_router
from app.contractor_workflow.router import router as contractor_workflow_router
from app.core.config import settings
from app.core.database import db_session
from app.crm_handoff.router import router as crm_handoff_router
from app.design_advisor.router import router as design_advisor_router
from app.designs.router import router as designs_router
from app.equipment.router import router as equipment_router
from app.estimates.router import router as estimates_router
from app.estimate_readiness.router import router as estimate_readiness_router
from app.homes.router import router as homes_router
from app.loads.router import router as loads_router
from app.panels.router import router as panels_router
from app.planning_exchange.router import router as planning_exchange_router
from app.post_install.router import router as post_install_router
from app.product_preferences.router import router as product_preferences_router
from app.proposal_option_sets.router import router as proposal_option_sets_router
from app.planning.router import (
    design_goal_presets_router,
    estimated_pathways_router,
    load_templates_router,
)
from app.product_library.router import router as product_library_router
from app.provenance.router import router as provenance_router
from app.rule_provenance.router import router as rule_provenance_router
from app.scenarios.router import router as scenarios_router
from app.seed.runtime import initialize_and_seed
from app.source_documents.router import router as source_documents_router
from app.takeoffs.router import router as takeoffs_router
from app.twin_planning_context.router import router as twin_planning_context_router

app = FastAPI(title=settings.app_name, version=settings.api_version, debug=settings.debug)
api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    with db_session() as db:
        initialize_and_seed(db)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": settings.api_version,
        "message": "Residential energy planning scaffold. Structured data and rules are authoritative; AI is a consumer of grounded context.",
        "database_url": settings.resolved_database_url,
        "api_policy": {
            "legacy_routes_remain_supported": True,
            "preferred_base_prefix": "/api",
            "reserved_future_version_prefix": "/api/v1",
        },
    }

for router in [
    accounts_router,
    homes_router,
    buildings_router,
    panels_router,
    designs_router,
    equipment_router,
    loads_router,
    product_library_router,
    source_documents_router,
    provenance_router,
    rule_provenance_router,
    compatibility_router,
    design_advisor_router,
    scenarios_router,
    takeoffs_router,
    estimates_router,
    ai_context_router,
    estimated_pathways_router,
    load_templates_router,
    design_goal_presets_router,
]:
    app.include_router(router)
    api_router.include_router(router)

api_router.include_router(twin_planning_context_router)
api_router.include_router(contractor_context_router)
api_router.include_router(contractor_workflow_router)
api_router.include_router(planning_exchange_router)
api_router.include_router(estimate_readiness_router)
api_router.include_router(proposal_option_sets_router)
api_router.include_router(product_preferences_router)
api_router.include_router(post_install_router)
api_router.include_router(crm_handoff_router)
app.include_router(api_router)
