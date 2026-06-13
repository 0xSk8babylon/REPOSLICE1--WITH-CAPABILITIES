from enum import Enum
from typing import List, Optional

from pydantic import Field

from app.core.schemas import ORMModel


class ArchitectureNodeKind(str, Enum):
    api_route = "api_route"
    backend_router = "backend_router"
    backend_schema = "backend_schema"
    backend_service = "backend_service"
    doc = "doc"
    frontend_component = "frontend_component"
    frontend_page = "frontend_page"
    phase = "phase"
    product_capability = "product_capability"
    test = "test"
    ui_section = "ui_section"


class ArchitectureEdgeKind(str, Enum):
    capability_to_ui_section = "capability_to_ui_section"
    endpoint_to_test = "endpoint_to_test"
    frontend_route_to_api_route = "frontend_route_to_api_route"
    implements_phase = "implements_phase"
    phase_doc_to_file = "phase_doc_to_file"
    route_to_router = "route_to_router"
    router_to_schema = "router_to_schema"
    router_to_service = "router_to_service"
    service_to_schema = "service_to_schema"
    technical_to_product_capability = "technical_to_product_capability"
    ui_composes_component = "ui_composes_component"


class ProductDataType(str, Enum):
    durable_record = "durable_record"
    derived_view = "derived_view"
    workflow = "workflow"
    internal = "internal"


class ArchitectureVisibilityScope(ORMModel):
    scope_name: str = "architecture_visibility_v1"
    read_only: bool = True
    additive_only: bool = True
    request_time_only: bool = True
    deterministic_for_same_inputs: bool = True
    persistence_present: bool = False
    migrations_present: bool = False
    write_endpoints_present: bool = False
    auth_security_changes_present: bool = False
    external_services_present: bool = False
    package_changes_present: bool = False
    runtime_introspection_present: bool = False
    graph_database_present: bool = False
    limitations: List[str] = Field(default_factory=list)


class ProductMappingMetadata(ORMModel):
    product_name: str = "Internal architecture visibility"
    homeowner_label: str = "Internal planning surface"
    contractor_label: str = "Internal planning surface"
    ui_section: str = "Hidden/Internal"
    ui_card: str = "Internal architecture"
    ui_priority: int = 999
    visible_in_v1: bool = False
    data_type: ProductDataType = ProductDataType.internal
    homeowner_question_answered: str = "What internal system surface supports this capability?"
    empty_state_message: str = "This capability is internal and is not shown as a homeowner-facing card."


class ArchitectureNodeMetadata(ORMModel):
    layer: str
    file_path: str
    phase: Optional[str] = None
    read_write_boundary: str
    audience: str = "internal"
    related_endpoints: List[str] = Field(default_factory=list)
    related_tests: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    product_mapping: ProductMappingMetadata = Field(default_factory=ProductMappingMetadata)


class ArchitectureNode(ORMModel):
    id: str
    label: str
    kind: ArchitectureNodeKind
    metadata: ArchitectureNodeMetadata


class ArchitectureEdge(ORMModel):
    id: str
    source: str
    target: str
    kind: ArchitectureEdgeKind
    label: str


class ArchitectureVisibilitySummary(ORMModel):
    node_count: int
    edge_count: int
    frontend_node_count: int
    backend_node_count: int
    api_route_node_count: int
    service_node_count: int
    schema_node_count: int
    test_node_count: int
    doc_node_count: int
    phase_node_count: int
    product_capability_node_count: int
    ui_section_node_count: int


class ProductInventorySummary(ORMModel):
    total_capabilities: int
    home_capabilities: int
    planner_capabilities: int
    build_capabilities: int
    internal_capabilities: int
    visible_in_v1_capabilities: int


class ProductCapabilityExport(ORMModel):
    node_id: str
    product_name: str
    homeowner_label: str
    contractor_label: str
    ui_section: str
    ui_card: str
    ui_priority: int
    visible_in_v1: bool
    data_type: ProductDataType
    homeowner_question_answered: str
    empty_state_message: str
    related_endpoints: List[str] = Field(default_factory=list)
    related_tests: List[str] = Field(default_factory=list)


class ProductGroup(ORMModel):
    ui_section: str
    capabilities: List[ProductCapabilityExport] = Field(default_factory=list)


class ProductExportBundle(ORMModel):
    ui_capability_map: List[ProductCapabilityExport] = Field(default_factory=list)
    home_section_inventory: List[ProductCapabilityExport] = Field(default_factory=list)
    planner_section_inventory: List[ProductCapabilityExport] = Field(default_factory=list)
    build_section_inventory: List[ProductCapabilityExport] = Field(default_factory=list)
    internal_section_inventory: List[ProductCapabilityExport] = Field(default_factory=list)


class ArchitectureVisibilitySourceBasis(ORMModel):
    basis_quality: str = "manual_static_repo_inventory_v1"
    source_files: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    missing_data: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class ArchitectureVisibilityGraph(ORMModel):
    view_name: str = "system_architecture_visibility"
    generated_at: str = "request_time_static_not_persisted"
    implementation_boundary: str = "internal_read_only_visibility_app"
    scope: ArchitectureVisibilityScope
    summary: ArchitectureVisibilitySummary
    nodes: List[ArchitectureNode] = Field(default_factory=list)
    edges: List[ArchitectureEdge] = Field(default_factory=list)
    filters: List[str] = Field(default_factory=list)
    view_modes: List[str] = Field(default_factory=list)
    product_inventory: ProductInventorySummary
    product_groups: List[ProductGroup] = Field(default_factory=list)
    exports: ProductExportBundle
    source_basis: ArchitectureVisibilitySourceBasis
