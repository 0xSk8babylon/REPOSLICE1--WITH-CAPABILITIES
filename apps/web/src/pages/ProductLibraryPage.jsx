import { EmptyState, ErrorState, LoadingState } from "../components/AsyncState";
import { Badge } from "../components/Badge";
import { MetricRow } from "../components/MetricRow";
import { PageSection } from "../components/PageSection";
import { TrustBadge } from "../components/TrustBadge";
import { api } from "../lib/api";
import { getProductTrustStates } from "../lib/trust";
import { useApiQuery } from "../lib/useApiQuery";

function formatDate(value) {
  if (!value) {
    return "Unknown";
  }
  return new Date(value).toLocaleDateString();
}

export function ProductLibraryPage() {
  const productsQuery = useApiQuery("products", api.getProductLibrary);
  const products = productsQuery.data || [];

  const ecosystemOrder = ["Tesla", "Enphase", "EG4", "Schneider", "EcoFlow", "Other", "Generac"];
  const groupedProducts = ecosystemOrder
    .map((ecosystem) => ({
      ecosystem,
      items: products.filter((product) => product.ecosystem === ecosystem),
    }))
    .filter((group) => group.items.length);

  return (
    <>
      <PageSection
        title="Product Library"
        description="Verified structured product data should become the factual backbone of design, takeoffs, rules, and AI explanations."
      >
        {productsQuery.loading ? <LoadingState label="Loading product library..." /> : null}
        {productsQuery.error ? <ErrorState error={productsQuery.error} label="Unable to load product library." /> : null}
        {!productsQuery.loading && !productsQuery.error && products.length ? (
          <div className="panel warning-panel">
            <div className="panel-header">
              <h3>Placeholder specs only</h3>
              <Badge tone="warning">Do not treat as verified manufacturer data</Badge>
            </div>
            <p>
              This seed library is intentionally non-authoritative. Real product ingestion should replace placeholder values before any engineering or procurement workflow exists.
            </p>
            <div className="trust-row">
              <TrustBadge state="demo_seed" />
              <TrustBadge state="placeholder" label="Placeholder specs" />
            </div>
          </div>
        ) : null}
        {!productsQuery.loading && !productsQuery.error && !products.length ? (
          <EmptyState label="No products available yet." />
        ) : null}
      </PageSection>

      {groupedProducts.map((group) => (
        <PageSection
          key={group.ecosystem}
          title={group.ecosystem === "Other" || group.ecosystem === "Generac" ? "Generic / Other" : group.ecosystem}
          description="Products are grouped by ecosystem first, then labeled by product type."
        >
          {Object.entries(
            group.items.reduce((accumulator, product) => {
              const key = product.product_type;
              accumulator[key] = accumulator[key] || [];
              accumulator[key].push(product);
              return accumulator;
            }, {})
          ).map(([productType, items]) => (
            <div key={productType} className="type-group">
              <div className="panel-header">
                <h3>{productType}</h3>
                <Badge>{items.length} records</Badge>
              </div>
              <div className="stack-grid">
                {items.map((product) => (
                  <article key={product.id} className="panel">
                    <div className="panel-header">
                      <div>
                        <h3>{product.model}</h3>
                        <p>{product.manufacturer}</p>
                      </div>
                      <div className="badge-row">
                        <Badge tone="info">{product.product_type}</Badge>
                        {getProductTrustStates(product).map((state) => (
                          <TrustBadge
                            key={`${product.id}-${state}`}
                            state={state}
                            label={state === "placeholder" ? "Placeholder specs" : undefined}
                          />
                        ))}
                      </div>
                    </div>
                    <pre className="specs-panel">{JSON.stringify(product.specs, null, 2)}</pre>
                    <div className="metric-stack">
                      <MetricRow
                        label="Source types"
                        value={(product.provenance_summary?.source_types || []).join(", ") || "Not recorded"}
                      />
                      <MetricRow
                        label="Verification status"
                        value={(product.provenance_summary?.verification_statuses || []).join(", ") || "Unverified"}
                      />
                      <MetricRow
                        label="Last retrieved"
                        value={formatDate(product.provenance_summary?.last_retrieved_at)}
                      />
                      <MetricRow
                        label="Last verified"
                        value={formatDate(product.provenance_summary?.last_verified_at)}
                      />
                    </div>
                    {product.source_documents?.length ? (
                      <div className="solution-list">
                        <strong>Source summary</strong>
                        <ul>
                          {product.source_documents.map((document) => (
                            <li key={document.id}>
                              {document.title} ({document.source_type}, {document.verification_status})
                            </li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                    <p>{product.notes || "No notes yet."}</p>
                  </article>
                ))}
              </div>
            </div>
          ))}
        </PageSection>
      ))}
    </>
  );
}
