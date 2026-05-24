import { useState } from "react";

import { EmptyState, ErrorState, LoadingState } from "../components/AsyncState";
import { Badge } from "../components/Badge";
import { MetricRow } from "../components/MetricRow";
import { PageSection } from "../components/PageSection";
import { TrustBadge } from "../components/TrustBadge";
import { api } from "../lib/api";
import { getTakeoffTrustStates } from "../lib/trust";
import { useApiQuery } from "../lib/useApiQuery";

export function TakeoffEstimatePage() {
  const designsQuery = useApiQuery("takeoff-designs", api.getDesigns);
  const designs = designsQuery.data || [];
  const defaultDesignId = designs[0]?.id || "";
  const [selectedDesignId, setSelectedDesignId] = useState("");
  const activeDesignId = selectedDesignId || defaultDesignId;
  const takeoffQuery = useApiQuery(
    `takeoff-${activeDesignId}`,
    () => (activeDesignId ? api.generateTakeoff(activeDesignId) : api.getTakeoff()),
    { enabled: Boolean(activeDesignId) || !designsQuery.loading }
  );
  const estimateQuery = useApiQuery("estimate-placeholder", api.getEstimatePlaceholder);

  return (
    <>
      <PageSection
        title="Takeoff / Estimate"
        description="This remains intentionally early-stage. The prototype now derives takeoff structure from persisted design equipment, while estimate values remain placeholders."
      >
        {designsQuery.loading ? <LoadingState label="Loading design options..." /> : null}
        {designsQuery.error ? <ErrorState error={designsQuery.error} label="Unable to load design options." /> : null}
        {!designsQuery.loading && !designsQuery.error && designs.length ? (
          <div className="toolbar">
            <label className="field">
              <span>Takeoff design</span>
              <select value={activeDesignId} onChange={(event) => setSelectedDesignId(event.target.value)}>
                {designs.map((design) => (
                  <option key={design.id} value={design.id}>
                    {design.name}
                  </option>
                ))}
              </select>
            </label>
            <div className="trust-row">
              <TrustBadge state="derived_estimate" />
              <TrustBadge state="placeholder" label="Planning estimate only" />
            </div>
          </div>
        ) : null}
      </PageSection>

      <PageSection
        title="Takeoff Request"
        description="Line items are generated from the selected design composition, but product costs and procurement details remain placeholders."
      >
        {takeoffQuery.loading ? <LoadingState label="Loading takeoff..." /> : null}
        {takeoffQuery.error ? <ErrorState error={takeoffQuery.error} label="Unable to load takeoff." /> : null}
        {!takeoffQuery.loading && !takeoffQuery.error && takeoffQuery.data ? (
          <div className="card-grid">
            <article className="panel">
              <h3>Request</h3>
              <div className="trust-row">
                {takeoffQuery.data.request?.trust_notes?.map((note) => (
                  <Badge key={note} tone="warning">{note}</Badge>
                ))}
              </div>
              <MetricRow label="Request ID" value={takeoffQuery.data.request?.id || "Unknown"} />
              <MetricRow label="Design ID" value={takeoffQuery.data.request?.design_id || "Unknown"} />
              <MetricRow label="Status" value={takeoffQuery.data.request?.status || "Unknown"} />
              <MetricRow label="Requested by" value={takeoffQuery.data.request?.requested_by || "Unknown"} />
              <p>{takeoffQuery.data.request?.notes || "No notes yet."}</p>
              {takeoffQuery.data.request?.provenance_summary ? (
                <div className="solution-list">
                  <strong>Provenance</strong>
                  <ul>
                    <li>Basis: {takeoffQuery.data.request.provenance_summary.basis}</li>
                    <li>Source types: {(takeoffQuery.data.request.provenance_summary.source_types || []).join(", ")}</li>
                    <li>Rule keys: {(takeoffQuery.data.request.provenance_summary.rule_keys || []).join(", ")}</li>
                  </ul>
                </div>
              ) : null}
              {takeoffQuery.data.request?.missing_information?.length ? (
                <div className="solution-list">
                  <strong>Missing information</strong>
                  <ul>
                    {takeoffQuery.data.request.missing_information.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </article>
            <article className="panel">
              <h3>Estimate posture</h3>
              <p>{estimateQuery.data?.message || "Estimate placeholder unavailable."}</p>
              <div className="trust-row">
                <TrustBadge state="placeholder" label="Requires site verification" />
                <TrustBadge state="placeholder" label="Pathways are approximate" />
              </div>
            </article>
          </div>
        ) : null}
      </PageSection>

      <PageSection
        title="Line Items"
        description="These line items are illustrative only and not yet suitable for procurement or firm pricing."
      >
        {!takeoffQuery.loading && !takeoffQuery.error && takeoffQuery.data?.line_items?.length ? (
          <div className="list-panel">
            {takeoffQuery.data.line_items.map((item) => (
              <div key={item.id} className="list-row list-row-stack">
                <div>
                  <strong>{item.item_name}</strong>
                  <p>{item.category}</p>
                  <div className="trust-row">
                    {getTakeoffTrustStates(item).map((state) => (
                      <TrustBadge
                        key={`${item.id}-${state}`}
                        state={state}
                        label={state === "placeholder" ? "Placeholder line item" : undefined}
                      />
                    ))}
                  </div>
                  {item.derivation_basis ? <p>{item.derivation_basis}</p> : null}
                  {item.provenance_summary ? (
                    <div className="solution-list">
                      <strong>Provenance</strong>
                      <ul>
                        <li>Basis: {item.provenance_summary.basis}</li>
                        <li>Source types: {(item.provenance_summary.source_types || []).join(", ")}</li>
                        <li>Rule keys: {(item.provenance_summary.rule_keys || []).join(", ") || "Not recorded"}</li>
                      </ul>
                    </div>
                  ) : null}
                </div>
                <div className="takeoff-meta">
                  <span>{item.quantity} {item.unit}</span>
                  <span>
                    {item.unit_cost_placeholder != null ? `$${item.unit_cost_placeholder}` : "No unit cost"}
                  </span>
                  <span>
                    {item.total_cost_placeholder != null ? `$${item.total_cost_placeholder}` : "No total cost"}
                  </span>
                </div>
                {item.missing_information?.length ? (
                  <div className="solution-list">
                    <strong>Missing information</strong>
                    <ul>
                      {item.missing_information.map((detail) => (
                        <li key={detail}>{detail}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}
              </div>
            ))}
          </div>
        ) : null}
        {!takeoffQuery.loading && !takeoffQuery.error && !takeoffQuery.data?.line_items?.length ? (
          <EmptyState label="No line items available yet." />
        ) : null}
      </PageSection>
    </>
  );
}
