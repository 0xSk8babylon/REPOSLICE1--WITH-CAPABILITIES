import unittest

import tests.fast_db  # noqa: F401, E402  must precede app imports (binds in-memory DB)

from app.main import app  # noqa: E402
from app.services.system_visibility import system_visibility_service  # noqa: E402
from app.system_visibility.router import get_architecture_visibility  # noqa: E402


class SystemVisibilityTests(unittest.TestCase):
    def _build(self):
        return system_visibility_service.build_architecture_graph()

    def test_route_registration_and_response_shape(self):
        paths = {getattr(route, "path", None) for route in app.routes}
        self.assertIn("/api/system-visibility/architecture", paths)

        response = get_architecture_visibility()
        self.assertEqual("system_architecture_visibility", response.view_name)
        self.assertEqual("request_time_static_not_persisted", response.generated_at)
        self.assertEqual("internal_read_only_visibility_app", response.implementation_boundary)

    def test_scope_flags_preserve_read_only_boundary(self):
        scope = self._build().scope
        self.assertTrue(scope.read_only)
        self.assertTrue(scope.additive_only)
        self.assertTrue(scope.request_time_only)
        self.assertTrue(scope.deterministic_for_same_inputs)

        for attr in [
            "persistence_present",
            "migrations_present",
            "write_endpoints_present",
            "auth_security_changes_present",
            "external_services_present",
            "package_changes_present",
            "runtime_introspection_present",
            "graph_database_present",
        ]:
            self.assertFalse(getattr(scope, attr), attr)

    def test_output_is_deterministic(self):
        first = self._build().dict()
        second = self._build().dict()

        self.assertEqual(first, second)

    def test_requested_node_layers_and_filters_are_present(self):
        graph = self._build()
        kinds = {node.kind.value for node in graph.nodes}
        self.assertIn("frontend_page", kinds)
        self.assertIn("frontend_component", kinds)
        self.assertIn("api_route", kinds)
        self.assertIn("backend_router", kinds)
        self.assertIn("backend_service", kinds)
        self.assertIn("backend_schema", kinds)
        self.assertIn("test", kinds)
        self.assertIn("doc", kinds)
        self.assertIn("phase", kinds)

        for expected in [
            "frontend",
            "backend",
            "api_routes",
            "services",
            "schemas",
            "tests",
            "docs",
            "phases",
            "product",
            "ui",
            "home",
            "planner",
            "build",
            "hidden_internal",
        ]:
            self.assertIn(expected, graph.filters)

        for expected in ["Product", "UI"]:
            self.assertIn(expected, graph.view_modes)

    def test_requested_edge_relationships_are_present(self):
        edge_kinds = {edge.kind.value for edge in self._build().edges}

        for expected in [
            "frontend_route_to_api_route",
            "route_to_router",
            "router_to_service",
            "router_to_schema",
            "service_to_schema",
            "endpoint_to_test",
            "phase_doc_to_file",
            "capability_to_ui_section",
            "technical_to_product_capability",
        ]:
            self.assertIn(expected, edge_kinds)

    def test_architecture_endpoint_links_to_test_and_metadata(self):
        graph = self._build()
        nodes = {node.id: node for node in graph.nodes}
        edges = {(edge.source, edge.target, edge.kind.value) for edge in graph.edges}

        endpoint_node = nodes["api-route-system-visibility-architecture"]
        self.assertIn("/api/system-visibility/architecture", endpoint_node.metadata.related_endpoints)
        self.assertIn("apps/api/tests/test_system_visibility.py", endpoint_node.metadata.related_tests)
        self.assertEqual("internal", endpoint_node.metadata.audience)
        self.assertEqual("read_only_visibility_metadata", endpoint_node.metadata.read_write_boundary)

        self.assertIn(
            (
                "api-route-system-visibility-architecture",
                "test-system-visibility",
                "endpoint_to_test",
            ),
            edges,
        )

    def test_source_basis_labels_manual_static_limitations(self):
        source_basis = self._build().source_basis

        self.assertEqual("manual_static_repo_inventory_v1", source_basis.basis_quality)
        self.assertTrue(source_basis.source_files)
        self.assertTrue(source_basis.assumptions)
        self.assertIn("No live import graph extraction is performed.", source_basis.missing_data)

    def test_product_mapping_inventory_groups_and_exports_are_present(self):
        graph = self._build()
        capability_nodes = [node for node in graph.nodes if node.kind.value == "product_capability"]

        self.assertGreaterEqual(len(capability_nodes), 14)
        self.assertEqual(len(capability_nodes), graph.product_inventory.total_capabilities)
        self.assertEqual(4, graph.product_inventory.home_capabilities)
        self.assertEqual(4, graph.product_inventory.planner_capabilities)
        self.assertEqual(5, graph.product_inventory.build_capabilities)
        self.assertGreaterEqual(graph.product_inventory.internal_capabilities, 1)

        group_map = {group.ui_section: [item.product_name for item in group.capabilities] for group in graph.product_groups}
        self.assertEqual(
            ["Energy Twin", "Energy Passport", "Readiness", "Home Facts"],
            group_map["Home"],
        )
        self.assertEqual(
            ["Compatibility", "Scenario Builder", "Product Preferences", "Planning Intelligence"],
            group_map["Planner"],
        )
        self.assertEqual(
            [
                "Proposal Options",
                "Contractor Context",
                "Estimate Readiness",
                "Install Path",
                "Program Intelligence",
            ],
            group_map["Build"],
        )

        self.assertEqual(len(capability_nodes), len(graph.exports.ui_capability_map))
        self.assertEqual(4, len(graph.exports.home_section_inventory))
        self.assertEqual(4, len(graph.exports.planner_section_inventory))
        self.assertEqual(5, len(graph.exports.build_section_inventory))

    def test_product_mapping_metadata_fields_are_attached_to_meaningful_nodes(self):
        graph = self._build()
        nodes = {node.id: node for node in graph.nodes}
        energy_twin = nodes["capability-energy-twin"].metadata.product_mapping
        program_router = nodes["backend-router-program-intelligence"].metadata.product_mapping

        self.assertEqual("Energy Twin", energy_twin.product_name)
        self.assertEqual("Home", energy_twin.ui_section)
        self.assertEqual("Energy Twin", energy_twin.ui_card)
        self.assertTrue(energy_twin.visible_in_v1)
        self.assertEqual("durable_record", energy_twin.data_type.value)
        self.assertTrue(energy_twin.homeowner_question_answered)
        self.assertTrue(energy_twin.empty_state_message)

        self.assertEqual("Program Intelligence", program_router.product_name)
        self.assertEqual("Build", program_router.ui_section)
        self.assertEqual("derived_view", program_router.data_type.value)


if __name__ == "__main__":
    unittest.main()
