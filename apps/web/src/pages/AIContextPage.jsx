import { useMemo, useState } from "react";

import { EmptyState, ErrorState, LoadingState } from "../components/AsyncState";
import { Badge } from "../components/Badge";
import { MetricRow } from "../components/MetricRow";
import { PageSection } from "../components/PageSection";
import { TrustBadge } from "../components/TrustBadge";
import { api } from "../lib/api";
import { useApiQuery } from "../lib/useApiQuery";

export function AIContextPage() {
  const designsQuery = useApiQuery("designs", api.getDesigns);
  const designs = designsQuery.data || [];
  const defaultDesignId = designs[0]?.id || "";
  const [selectedDesignId, setSelectedDesignId] = useState("");
  const activeDesignId = selectedDesignId || defaultDesignId;

  const aiContextQuery = useApiQuery(
    `ai-context-${activeDesignId}`,
    () => api.getAIContext(activeDesignId),
    { enabled: Boolean(activeDesignId) }
  );

  const groundingEntries = useMemo(() => {
    if (!aiContextQuery.data?.grounding_policy) {
      return [];
    }

    return Object.entries(aiContextQuery.data.grounding_policy);
  }, [aiContextQuery.data]);

  return (
    <>
      <PageSection
        title="AI Grounding Context"
        description="Future AI responses should be built from this structured context, not from generic guessing."
      >
        {designsQuery.loading ? <LoadingState label="Loading design options..." /> : null}
        {designsQuery.error ? <ErrorState error={designsQuery.error} label="Unable to load design options." /> : null}
        {!designsQuery.loading && !designsQuery.error && designs.length ? (
          <div className="toolbar">
            <label className="field">
              <span>Current design</span>
              <select value={activeDesignId} onChange={(event) => setSelectedDesignId(event.target.value)}>
                {designs.map((design) => (
                  <option key={design.id} value={design.id}>
                    {design.name}
                  </option>
                ))}
              </select>
            </label>
            <div className="trust-row">
              <Badge tone="info">AI must cite structured context</Badge>
              <TrustBadge state="derived_estimate" label="Derived trust states preserved" />
            </div>
          </div>
        ) : null}
        {!designsQuery.loading && !designsQuery.error && !designs.length ? (
          <EmptyState label="No designs available for AI grounding yet." />
        ) : null}
      </PageSection>

      <PageSection
        title="Structured Context"
        description="This payload is the shape a future conversational layer should consume and reference."
      >
        {aiContextQuery.loading ? <LoadingState label="Building AI context..." /> : null}
        {aiContextQuery.error ? <ErrorState error={aiContextQuery.error} label="Unable to build AI context." /> : null}
        {!aiContextQuery.loading && !aiContextQuery.error && aiContextQuery.data ? (
          <div className="card-grid">
            <article className="panel">
              <h3>Design</h3>
              <MetricRow label="Name" value={aiContextQuery.data.design?.name || "Unknown"} />
              <MetricRow label="Architecture" value={aiContextQuery.data.design?.architecture_type || "Unknown"} />
              <MetricRow label="Goal" value={aiContextQuery.data.design?.design_goal || "Unknown"} />
              <MetricRow label="Status" value={aiContextQuery.data.design_maturity?.effective_status || "Unknown"} />
            </article>
            <article className="panel">
              <h3>Home Scope</h3>
              <MetricRow label="Home" value={aiContextQuery.data.home?.name || "Unknown"} />
              <MetricRow
                label="Structures"
                value={String(aiContextQuery.data.home?.buildings?.length || 0)}
              />
              <MetricRow label="Panels" value={String(aiContextQuery.data.home?.panels?.length || 0)} />
            </article>
            <article className="panel">
              <h3>Grounding Policy</h3>
              <div className="metric-stack">
                {groundingEntries.map(([key, value]) => (
                  <MetricRow key={key} label={key} value={String(value)} />
                ))}
              </div>
            </article>
            <article className="panel">
              <h3>Trust + Completeness</h3>
              <MetricRow label="Completeness score" value={String(aiContextQuery.data.design_completeness?.completeness_score || 0)} />
              <MetricRow label="Advisor issues" value={String(aiContextQuery.data.advisor_issues?.length || 0)} />
              <MetricRow label="Assigned products" value={String(aiContextQuery.data.assigned_products?.length || 0)} />
              <MetricRow label="Source documents" value={String(aiContextQuery.data.source_documents?.length || 0)} />
              <MetricRow label="Provenance records" value={String(aiContextQuery.data.provenance_records?.length || 0)} />
              <p className="callout-copy">
                AI responses should reference these records and explicitly separate known facts from assumptions.
              </p>
            </article>
          </div>
        ) : null}
      </PageSection>

      <PageSection
        title="Trust Summary"
        description="Future conversational AI should surface these uncertainty markers instead of smoothing over them."
      >
        {!aiContextQuery.loading && !aiContextQuery.error && aiContextQuery.data ? (
          <div className="card-grid">
            <article className="panel">
              <h3>Origins</h3>
              <div className="trust-row">
                {aiContextQuery.data.trust_summary?.design_data_origin ? (
                  <TrustBadge state={aiContextQuery.data.trust_summary.design_data_origin} />
                ) : null}
                {(aiContextQuery.data.trust_summary?.assigned_product_origins || []).map((state) => (
                  <TrustBadge key={state} state={state} />
                ))}
              </div>
              <MetricRow
                label="Ecosystem mixing"
                value={String(aiContextQuery.data.trust_summary?.ecosystem_mixing || false)}
              />
            </article>
            <article className="panel">
              <h3>Missing categories</h3>
              <div className="solution-list">
                <ul>
                  {(aiContextQuery.data.missing_categories || []).map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </article>
            <article className="panel">
              <h3>Pathway confidence</h3>
              <MetricRow
                label="Linked pathways"
                value={String(aiContextQuery.data.pathway_summary?.linked_pathway_count || 0)}
              />
              <MetricRow
                label="Confidence levels"
                value={(aiContextQuery.data.trust_summary?.pathway_confidence_levels || []).join(", ") || "Unknown"}
              />
            </article>
            <article className="panel">
              <h3>Grounding warnings</h3>
              <div className="solution-list">
                <ul>
                  {(aiContextQuery.data.grounding_warnings || []).map((warning) => (
                    <li key={warning}>{warning}</li>
                  ))}
                </ul>
              </div>
            </article>
            <article className="panel">
              <h3>Provenance posture</h3>
              <MetricRow
                label="Unverified fields"
                value={(aiContextQuery.data.unverified_fields || []).join(", ") || "None listed"}
              />
              <MetricRow
                label="Placeholder assumptions"
                value={String(aiContextQuery.data.placeholder_assumptions?.length || 0)}
              />
              <MetricRow
                label="Rule provenance"
                value={String(aiContextQuery.data.rule_provenance?.length || 0)}
              />
            </article>
          </div>
        ) : null}
      </PageSection>

      <PageSection
        title="Context Snapshot"
        description="Read-only payload preview for prototyping and prompt-shaping."
      >
        {!aiContextQuery.loading && !aiContextQuery.error && aiContextQuery.data ? (
          <pre className="code-panel">{JSON.stringify(aiContextQuery.data, null, 2)}</pre>
        ) : null}
      </PageSection>
    </>
  );
}
