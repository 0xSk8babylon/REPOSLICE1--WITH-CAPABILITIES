import { useMemo, useState } from "react";

import { ErrorState, LoadingState } from "../components/AsyncState";
import { Badge } from "../components/Badge";
import { MetricRow } from "../components/MetricRow";
import { PageSection } from "../components/PageSection";
import { api } from "../lib/api";
import { useApiQuery } from "../lib/useApiQuery";

const FILTER_LABELS = {
  frontend: "Frontend",
  backend: "Backend",
  api_routes: "API routes",
  services: "Services",
  schemas: "Schemas",
  tests: "Tests",
  docs: "Docs",
  phases: "Phases",
  product: "Product",
  ui: "UI",
  home: "Home",
  explore: "Explore",
  planner: "Planner",
  builder: "Builder",
  build: "Builder alias",
  internal: "Internal/Debug",
  hidden_internal: "Hidden/Internal",
  deferred: "Deferred/Legacy",
};

const VIEW_MODE_FILTERS = {
  Frontend: ["frontend"],
  Backend: ["backend"],
  "API Routes": ["api_routes"],
  Services: ["services"],
  Schemas: ["schemas"],
  Tests: ["tests"],
  Docs: ["docs"],
  Phases: ["phases"],
  Product: ["product", "home", "explore", "planner", "builder", "internal", "hidden_internal", "deferred"],
  UI: ["ui", "product", "home", "explore", "planner", "builder", "internal", "hidden_internal", "deferred"],
};

const KIND_TONES = {
  api_route: "info",
  backend_router: "default",
  backend_schema: "warning",
  backend_service: "success",
  doc: "default",
  frontend_component: "info",
  frontend_page: "info",
  phase: "warning",
  product_capability: "success",
  test: "success",
  ui_section: "info",
};

const LAYER_X = {
  phase: 80,
  ui: 80,
  docs: 190,
  product: 330,
  frontend: 330,
  api: 470,
  routers: 590,
  services: 710,
  schemas: 830,
  tests: 950,
};

function nodeMatchesFilters(node, activeFilters) {
  return (node.metadata?.tags || []).some((tag) => activeFilters.includes(tag));
}

function getLayoutGroup(node) {
  if (node.kind === "backend_router") {
    return "routers";
  }
  if (node.kind === "backend_service") {
    return "services";
  }
  if (node.kind === "backend_schema") {
    return "schemas";
  }
  if (node.kind === "ui_section") {
    return "ui";
  }
  if (node.kind === "product_capability") {
    return "product";
  }
  return node.metadata?.layer || "backend";
}

function getNodePosition(node, index, layerCounts) {
  const layer = getLayoutGroup(node);
  const count = layerCounts[layer] || 1;
  const currentIndex = index[layer] || 0;
  index[layer] = currentIndex + 1;

  const availableHeight = 520;
  const topInset = 44;
  const y = count === 1 ? 300 : topInset + (currentIndex * availableHeight) / (count - 1);

  return {
    x: LAYER_X[layer] || 500,
    y,
  };
}

function buildLayout(nodes) {
  const layerCounts = nodes.reduce((counts, node) => {
    const layer = getLayoutGroup(node);
    return { ...counts, [layer]: (counts[layer] || 0) + 1 };
  }, {});
  const index = {};

  return nodes.reduce((positions, node) => {
    return { ...positions, [node.id]: getNodePosition(node, index, layerCounts) };
  }, {});
}

function shortNodeLabel(label) {
  if (label.length <= 26) {
    return label;
  }
  return `${label.slice(0, 23)}...`;
}

function DetailList({ title, items }) {
  if (!items?.length) {
    return null;
  }

  return (
    <div className="architecture-detail-list">
      <strong>{title}</strong>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function ArchitectureDetailPanel({ node, connectedEdges, nodeLabels }) {
  if (!node) {
    return (
      <aside className="architecture-detail-panel">
        <h3>Select a node</h3>
        <p>Inspect file path, phase, visibility boundary, related endpoints, tests, and graph relationships.</p>
      </aside>
    );
  }

  const metadata = node.metadata || {};
  const productMapping = metadata.product_mapping || {};

  return (
    <aside className="architecture-detail-panel">
      <div className="architecture-detail-heading">
        <Badge tone={KIND_TONES[node.kind] || "default"}>{node.kind.replaceAll("_", " ")}</Badge>
        <h3>{node.label}</h3>
      </div>
      <MetricRow label="Product Meaning" value={productMapping.product_name || "Internal architecture visibility"} />
      <MetricRow label="Homeowner Label" value={productMapping.homeowner_label || "Internal planning surface"} />
      <MetricRow label="UI Section" value={productMapping.ui_section || "Internal/Debug"} />
      <MetricRow label="Card Name" value={productMapping.ui_card || "Internal architecture"} />
      <MetricRow label="Priority" value={String(productMapping.ui_priority ?? "Not set")} />
      <MetricRow label="Visible in V1" value={String(productMapping.visible_in_v1 || false)} />
      <MetricRow label="Layer" value={metadata.layer || "Unknown"} />
      <MetricRow label="Audience" value={metadata.audience || "internal"} />
      <MetricRow label="Boundary" value={metadata.read_write_boundary || "Unknown"} />
      <MetricRow label="Phase" value={metadata.phase || "Not labeled"} />
      <MetricRow label="File" value={metadata.file_path || "Unknown"} />
      <DetailList title="Question answered" items={[productMapping.homeowner_question_answered].filter(Boolean)} />
      <DetailList title="Empty state" items={[productMapping.empty_state_message].filter(Boolean)} />
      <DetailList title="Related endpoints" items={metadata.related_endpoints} />
      <DetailList title="Related tests" items={metadata.related_tests} />
      <DetailList
        title="Connected edges"
        items={connectedEdges.map((edge) => {
          const otherId = edge.source === node.id ? edge.target : edge.source;
          return `${edge.label}: ${nodeLabels[otherId] || otherId}`;
        })}
      />
    </aside>
  );
}

export function ArchitecturePage() {
  const architectureQuery = useApiQuery("architecture-visibility", api.getArchitectureVisibility);
  const graph = architectureQuery.data;
  const filterOptions = graph?.filters || Object.keys(FILTER_LABELS);
  const [activeFilters, setActiveFilters] = useState(filterOptions);
  const [activeMode, setActiveMode] = useState("All");
  const [exportKey, setExportKey] = useState("ui_capability_map");
  const [selectedNodeId, setSelectedNodeId] = useState(null);

  const visibleNodes = useMemo(() => {
    if (!graph?.nodes) {
      return [];
    }
    return graph.nodes.filter((node) => nodeMatchesFilters(node, activeFilters));
  }, [graph, activeFilters]);
  const visibleNodeIds = useMemo(() => new Set(visibleNodes.map((node) => node.id)), [visibleNodes]);
  const visibleEdges = useMemo(() => {
    if (!graph?.edges) {
      return [];
    }
    return graph.edges.filter((edge) => visibleNodeIds.has(edge.source) && visibleNodeIds.has(edge.target));
  }, [graph, visibleNodeIds]);
  const positions = useMemo(() => buildLayout(visibleNodes), [visibleNodes]);
  const nodeLabels = useMemo(() => {
    return (graph?.nodes || []).reduce((labels, node) => ({ ...labels, [node.id]: node.label }), {});
  }, [graph]);
  const selectedNode = useMemo(() => {
    if (!graph?.nodes?.length) {
      return null;
    }
    const visibleSelected = visibleNodes.find((node) => node.id === selectedNodeId);
    return visibleSelected || visibleNodes[0] || null;
  }, [graph, selectedNodeId, visibleNodes]);
  const connectedEdges = useMemo(() => {
    if (!selectedNode) {
      return [];
    }
    return (graph?.edges || []).filter((edge) => edge.source === selectedNode.id || edge.target === selectedNode.id);
  }, [graph, selectedNode]);

  function toggleFilter(filter) {
    setActiveFilters((current) => {
      if (current.includes(filter)) {
        return current.filter((item) => item !== filter);
      }
      return [...current, filter];
    });
    setActiveMode("Custom");
  }

  function applyViewMode(mode) {
    setActiveMode(mode);
    setActiveFilters(VIEW_MODE_FILTERS[mode] || filterOptions);
  }

  return (
    <>
      <PageSection
        title="Architecture Visibility"
        description="Internal read-only map of selected frontend, backend, test, documentation, and phase relationships."
      >
        {architectureQuery.loading ? <LoadingState label="Loading architecture graph..." /> : null}
        {architectureQuery.error ? (
          <ErrorState error={architectureQuery.error} label="Unable to load architecture graph." />
        ) : null}
        {!architectureQuery.loading && !architectureQuery.error && graph ? (
          <div className="architecture-summary-grid">
            <article className="stat-card">
              <span>Nodes</span>
              <strong>{graph.summary?.node_count || 0}</strong>
              <p>Curated architecture entities</p>
            </article>
            <article className="stat-card">
              <span>Edges</span>
              <strong>{graph.summary?.edge_count || 0}</strong>
              <p>Known implementation relationships</p>
            </article>
            <article className="stat-card">
              <span>Backend</span>
              <strong>{graph.summary?.backend_node_count || 0}</strong>
              <p>Routes, routers, services, schemas</p>
            </article>
            <article className="stat-card">
              <span>Verification</span>
              <strong>{graph.summary?.test_node_count || 0}</strong>
              <p>Focused test surfaces</p>
            </article>
          </div>
        ) : null}
      </PageSection>

      {!architectureQuery.loading && !architectureQuery.error && graph ? (
        <PageSection
          title="Product Inventory"
          description="Capabilities are mapped into the future homeowner-facing information architecture without creating new planner pages."
        >
          <div className="architecture-summary-grid">
            <article className="stat-card">
              <span>Total capabilities</span>
              <strong>{graph.product_inventory?.total_capabilities || 0}</strong>
              <p>Mapped product surfaces</p>
            </article>
            <article className="stat-card">
              <span>Home</span>
              <strong>{graph.product_inventory?.home_capabilities || 0}</strong>
              <p>Homeowner record and summary surfaces</p>
            </article>
            <article className="stat-card">
              <span>Explore</span>
              <strong>{graph.product_inventory?.explore_capabilities || 0}</strong>
              <p>Goals and learn surfaces</p>
            </article>
            <article className="stat-card">
              <span>Planner</span>
              <strong>{graph.product_inventory?.planner_capabilities || 0}</strong>
              <p>Templates, drafts, and comparisons</p>
            </article>
            <article className="stat-card">
              <span>Builder</span>
              <strong>{graph.product_inventory?.builder_capabilities ?? graph.product_inventory?.build_capabilities ?? 0}</strong>
              <p>Project and build-readiness surfaces</p>
            </article>
            <article className="stat-card">
              <span>Internal</span>
              <strong>{graph.product_inventory?.internal_capabilities || 0}</strong>
              <p>Hidden cockpit and governance surfaces</p>
            </article>
            <article className="stat-card">
              <span>Deferred</span>
              <strong>{graph.product_inventory?.deferred_capabilities || 0}</strong>
              <p>Legacy and future route surfaces</p>
            </article>
          </div>
        </PageSection>
      ) : null}

      {!architectureQuery.loading && !architectureQuery.error && graph ? (
        <PageSection
          title="Product / Architecture Map"
          description="Switch modes or filter by section, then click a node to inspect product meaning, UI placement, implementation files, endpoints, and tests."
        >
          <div className="architecture-mode-bar">
            <button
              type="button"
              className={activeMode === "All" ? "architecture-mode active" : "architecture-mode"}
              onClick={() => applyViewMode("All")}
            >
              All
            </button>
            {(graph.view_modes || []).map((mode) => (
              <button
                key={mode}
                type="button"
                className={activeMode === mode ? "architecture-mode active" : "architecture-mode"}
                onClick={() => applyViewMode(mode)}
              >
                {mode}
              </button>
            ))}
          </div>
          <div className="architecture-filter-bar">
            {filterOptions.map((filter) => (
              <label key={filter} className="architecture-filter">
                <input
                  type="checkbox"
                  checked={activeFilters.includes(filter)}
                  onChange={() => toggleFilter(filter)}
                />
                <span>{FILTER_LABELS[filter] || filter}</span>
              </label>
            ))}
          </div>

          <div className="architecture-workspace">
            <div className="architecture-map-panel">
              <svg className="architecture-map" viewBox="0 0 1020 640" role="img" aria-label="Architecture graph">
                <defs>
                  <marker id="architecture-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                    <path d="M 0 0 L 8 4 L 0 8 z" />
                  </marker>
                </defs>
                {visibleEdges.map((edge) => {
                  const source = positions[edge.source];
                  const target = positions[edge.target];
                  if (!source || !target) {
                    return null;
                  }
                  return (
                    <line
                      key={edge.id}
                      className="architecture-edge"
                      x1={source.x}
                      y1={source.y}
                      x2={target.x}
                      y2={target.y}
                      markerEnd="url(#architecture-arrow)"
                    />
                  );
                })}
                {visibleNodes.map((node) => {
                  const position = positions[node.id];
                  const isSelected = selectedNode?.id === node.id;
                  return (
                    <g
                      key={node.id}
                      className={`architecture-node architecture-node-${node.kind} ${isSelected ? "selected" : ""}`}
                      transform={`translate(${position.x} ${position.y})`}
                      role="button"
                      tabIndex="0"
                      onClick={() => setSelectedNodeId(node.id)}
                      onKeyDown={(event) => {
                        if (event.key === "Enter" || event.key === " ") {
                          setSelectedNodeId(node.id);
                        }
                      }}
                    >
                      <circle r="18" />
                      <text y="36">{shortNodeLabel(node.label)}</text>
                    </g>
                  );
                })}
              </svg>
            </div>
            <ArchitectureDetailPanel node={selectedNode} connectedEdges={connectedEdges} nodeLabels={nodeLabels} />
          </div>
        </PageSection>
      ) : null}

      {!architectureQuery.loading && !architectureQuery.error && graph ? (
        <PageSection
          title="Product Grouping"
          description="This is the intended cockpit grouping: technical architecture mapped upward into product capabilities and UI sections."
        >
          <div className="architecture-product-groups">
            {(graph.product_groups || []).map((group) => (
              <article className="panel" key={group.ui_section}>
                <h3>{group.ui_section}</h3>
                <div className="architecture-capability-list">
                  {(group.capabilities || []).map((capability) => (
                    <div className="architecture-capability-row" key={capability.node_id}>
                      <div>
                        <strong>{capability.homeowner_label}</strong>
                        <p>{capability.homeowner_question_answered}</p>
                      </div>
                      <div className="trust-row">
                        <Badge tone={capability.visible_in_v1 ? "success" : "default"}>
                          {capability.visible_in_v1 ? "V1 visible" : "Hidden"}
                        </Badge>
                        <Badge tone="info">{capability.data_type}</Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </PageSection>
      ) : null}

      {!architectureQuery.loading && !architectureQuery.error && graph ? (
        <PageSection
          title="Product Map Export"
          description="JSON export preview for organizing backend capabilities into UI sections. No download or persistence is performed."
        >
          <div className="toolbar">
            <label className="field">
              <span>Export</span>
              <select value={exportKey} onChange={(event) => setExportKey(event.target.value)}>
                <option value="ui_capability_map">UI Capability Map</option>
                <option value="home_section_inventory">Home section inventory</option>
                <option value="explore_section_inventory">Explore section inventory</option>
                <option value="planner_section_inventory">Planner section inventory</option>
                <option value="builder_section_inventory">Builder section inventory</option>
                <option value="build_section_inventory">Build alias inventory</option>
                <option value="internal_section_inventory">Internal/debug inventory</option>
                <option value="deferred_section_inventory">Deferred/legacy inventory</option>
              </select>
            </label>
          </div>
          <pre className="code-panel">{JSON.stringify(graph.exports?.[exportKey] || [], null, 2)}</pre>
        </PageSection>
      ) : null}

      {!architectureQuery.loading && !architectureQuery.error && graph ? (
        <PageSection
          title="Source Basis"
          description="This v1 map is intentionally manual and static. Missing coverage stays explicit."
        >
          <div className="card-grid">
            <article className="panel">
              <h3>Boundary</h3>
              <MetricRow label="Read only" value={String(graph.scope?.read_only)} />
              <MetricRow label="Persistence" value={String(graph.scope?.persistence_present)} />
              <MetricRow label="Migrations" value={String(graph.scope?.migrations_present)} />
              <MetricRow label="External services" value={String(graph.scope?.external_services_present)} />
              <MetricRow label="Package changes" value={String(graph.scope?.package_changes_present)} />
            </article>
            <article className="panel">
              <h3>Assumptions</h3>
              <div className="solution-list">
                <ul>
                  {(graph.source_basis?.assumptions || []).map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </article>
            <article className="panel">
              <h3>Missing Data</h3>
              <div className="solution-list">
                <ul>
                  {(graph.source_basis?.missing_data || []).map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </article>
            <article className="panel">
              <h3>Source Files</h3>
              <div className="solution-list">
                <ul>
                  {(graph.source_basis?.source_files || []).map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </article>
          </div>
        </PageSection>
      ) : null}
    </>
  );
}
