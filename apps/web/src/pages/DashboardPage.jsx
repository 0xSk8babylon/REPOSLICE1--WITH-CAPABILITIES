import { EmptyState, ErrorState, LoadingState } from "../components/AsyncState";
import { Badge } from "../components/Badge";
import { PageSection } from "../components/PageSection";
import { StatCard } from "../components/StatCard";
import { api } from "../lib/api";
import { useApiQuery } from "../lib/useApiQuery";

export function DashboardPage() {
  const homeQuery = useApiQuery("home", api.getHome);
  const loadsQuery = useApiQuery("loads-summary", api.getLoadSummary);
  const designsQuery = useApiQuery("designs", api.getDesigns);
  const productsQuery = useApiQuery("products", api.getProductLibrary);
  const scenariosQuery = useApiQuery("scenarios", api.getScenarios);

  const isLoading =
    homeQuery.loading ||
    loadsQuery.loading ||
    designsQuery.loading ||
    productsQuery.loading ||
    scenariosQuery.loading;

  const error =
    homeQuery.error ||
    loadsQuery.error ||
    designsQuery.error ||
    productsQuery.error ||
    scenariosQuery.error;

  const home = homeQuery.data;
  const loadSummary = loadsQuery.data;
  const designs = designsQuery.data || [];
  const products = productsQuery.data || [];
  const scenarios = scenariosQuery.data || [];

  return (
    <>
      <PageSection
        title="Planning Frame"
        description="The dashboard should become the living summary of a home, the active designs, and the next decisions that matter."
      >
        {isLoading ? <LoadingState label="Loading dashboard summary..." /> : null}
        {error ? <ErrorState error={error} label="Unable to load dashboard summary." /> : null}
        {!isLoading && !error && home ? (
          <div className="stat-grid">
            <StatCard label="Homes in workspace" value="1" detail={home.name} />
            <StatCard
              label="Structures modeled"
              value={String(home.buildings?.length || 0)}
              detail={`${home.panels?.length || 0} electrical panels tracked`}
            />
            <StatCard
              label="Design pathways"
              value={String(designs.length)}
              detail="Live seed designs from the API"
            />
            <StatCard
              label="Product records"
              value={String(products.length)}
              detail="Placeholder specs only until verified data ingestion exists"
            />
          </div>
        ) : null}
      </PageSection>
      <PageSection
        title="What This App Is For"
        description="This product should preserve the house model and the reasoning around it so the homeowner and contractor can keep building on the same system understanding."
      >
        {isLoading ? null : !error && home ? (
          <div className="card-grid">
            <article className="panel">
              <div className="panel-header">
                <h3>Live property summary</h3>
                <Badge tone="info">Read-only prototype</Badge>
              </div>
              <p>{home.address_line_1}, {home.city}, {home.state}</p>
              <p>Utility: {home.utility_provider || "Placeholder"}</p>
              <p>Service size: {home.service_size ? `${home.service_size}A` : "Unknown"}</p>
            </article>
            <article className="panel">
              <h3>Current planning signals</h3>
              <p>Total running load: {loadSummary?.total_running_watts || 0} W</p>
              <p>Total surge load: {loadSummary?.total_surge_watts || 0} W</p>
              <p>Scenarios available: {scenarios.length}</p>
            </article>
          </div>
        ) : null}
        {!isLoading && !error && !home ? <EmptyState label="No home model available yet." /> : null}
      </PageSection>
    </>
  );
}
