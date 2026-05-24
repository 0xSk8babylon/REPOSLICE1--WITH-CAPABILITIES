import { useState } from "react";

import { EmptyState, ErrorState, LoadingState } from "../components/AsyncState";
import { Badge } from "../components/Badge";
import { MetricRow } from "../components/MetricRow";
import { PageSection } from "../components/PageSection";
import { ScoreCard } from "../components/ScoreCard";
import { TrustBadge } from "../components/TrustBadge";
import { api } from "../lib/api";
import { getAdvisorTrustStates } from "../lib/trust";
import { useApiQuery } from "../lib/useApiQuery";

export function DesignAdvisorPage() {
  const designsQuery = useApiQuery("designs", api.getDesigns);
  const designs = designsQuery.data || [];
  const defaultDesignId = designs[0]?.id || "";
  const [selectedDesignId, setSelectedDesignId] = useState("");
  const activeDesignId = selectedDesignId || defaultDesignId;

  const advisorQuery = useApiQuery(
    `advisor-${activeDesignId}`,
    () => api.getDesignAdvisor(activeDesignId),
    { enabled: Boolean(activeDesignId) }
  );

  const aiContextQuery = useApiQuery(
    `advisor-ai-${activeDesignId}`,
    () => api.getAIContext(activeDesignId),
    { enabled: Boolean(activeDesignId) }
  );

  return (
    <>
      <PageSection
        title="Design Advisor"
        description="This should be the heart of the product: grounded explanations of why a design fits, where it strains, and what solution paths exist."
      >
        {designsQuery.loading ? <LoadingState label="Loading design options..." /> : null}
        {designsQuery.error ? <ErrorState error={designsQuery.error} label="Unable to load designs." /> : null}
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
              <Badge tone="danger">Structured guidance, not engineering approval</Badge>
              <TrustBadge state="derived_estimate" label="Planning reasoning only" />
            </div>
          </div>
        ) : null}
      </PageSection>

      <PageSection
        title="Advisor Summary"
        description="Deterministic service outputs should feed the advisor layer before any future conversational wrapper is added."
      >
        {advisorQuery.loading ? <LoadingState label="Loading advisor summary..." /> : null}
        {advisorQuery.error ? <ErrorState error={advisorQuery.error} label="Unable to load advisor summary." /> : null}
        {!advisorQuery.loading && !advisorQuery.error && advisorQuery.data ? (
          <>
            <div className="card-grid">
              <article className="panel">
                <div className="panel-header">
                  <h3>Design maturity</h3>
                  <Badge tone="info">{advisorQuery.data.design_status?.effective_status?.replaceAll("_", " ") || "Unknown"}</Badge>
                </div>
                <p>{advisorQuery.data.design_status?.explanation}</p>
                <div className="trust-row">
                  <TrustBadge state="placeholder" label="Maturity, not engineering approval" />
                </div>
              </article>
              <article className="panel">
                <div className="panel-header">
                  <h3>Planning completeness</h3>
                  <Badge tone="warning">{advisorQuery.data.completeness?.completeness_score ?? 0}/100</Badge>
                </div>
                <p>{advisorQuery.data.completeness?.scope_note}</p>
                <div className="solution-list">
                  <strong>Recommended next steps</strong>
                  <ul>
                    {(advisorQuery.data.completeness?.recommended_next_steps || []).map((step) => (
                      <li key={step}>{step}</li>
                    ))}
                  </ul>
                </div>
              </article>
            </div>
            <div className="score-grid">
              <ScoreCard
                label="Backup capability"
                value={advisorQuery.data.backup?.backup_capability_score ?? "N/A"}
                detail={advisorQuery.data.backup?.status}
              />
              <ScoreCard
                label="Expansion readiness"
                value={advisorQuery.data.expansion?.future_expansion_score ?? "N/A"}
                detail={advisorQuery.data.expansion?.status}
              />
              <ScoreCard
                label="Install complexity"
                value={advisorQuery.data.install_complexity?.install_complexity_score ?? "N/A"}
                detail={advisorQuery.data.install_complexity?.status}
              />
            </div>
          </>
        ) : null}
      </PageSection>

      <PageSection
        title="Compatibility Explanations"
        description="Issues are rendered in the same structured pattern the rules engine should continue to produce."
      >
        {!advisorQuery.loading && !advisorQuery.error && advisorQuery.data?.compatibility?.length ? (
          <div className="stack-grid">
            {advisorQuery.data.compatibility.map((issue, index) => (
              <article key={`${issue.issue}-${index}`} className="panel advisor-issue">
                <div className="panel-header">
                  <h3>Issue</h3>
                  <div className="badge-row">
                    <Badge tone={issue.severity === "blocker" ? "danger" : issue.severity === "warning" ? "warning" : "info"}>
                      {issue.severity}
                    </Badge>
                    <Badge>{issue.category}</Badge>
                    {getAdvisorTrustStates(issue).map((state) => (
                      <TrustBadge key={`${issue.issue}-${state}`} state={state} />
                    ))}
                  </div>
                </div>
                <div className="metric-stack">
                  <MetricRow label="Issue" value={issue.issue} />
                  <MetricRow label="Why it matters" value={issue.why_it_matters} />
                  <MetricRow label="Tradeoff" value={issue.tradeoff} />
                </div>
                <div className="solution-list">
                  <strong>Possible solutions</strong>
                  <ul>
                    {issue.possible_solutions.map((solution) => (
                      <li key={solution}>{solution}</li>
                    ))}
                  </ul>
                </div>
                {issue.provenance_summary ? (
                  <div className="solution-list">
                    <strong>Provenance</strong>
                    <ul>
                      <li>Basis: {issue.provenance_summary.basis}</li>
                      <li>Source types: {(issue.provenance_summary.source_types || []).join(", ") || "Not recorded"}</li>
                      <li>Rule keys: {(issue.provenance_summary.rule_keys || []).join(", ") || "Not recorded"}</li>
                    </ul>
                  </div>
                ) : null}
              </article>
            ))}
          </div>
        ) : null}
        {!advisorQuery.loading && !advisorQuery.error && !advisorQuery.data?.compatibility?.length ? (
          <EmptyState label="No compatibility explanations available for this design." />
        ) : null}
      </PageSection>

      <PageSection
        title="AI Grounding Panel"
        description="The future AI assistant should read from this context and cite it, not improvise around it."
      >
        {aiContextQuery.loading ? <LoadingState label="Loading grounding context..." /> : null}
        {aiContextQuery.error ? <ErrorState error={aiContextQuery.error} label="Unable to load grounding context." /> : null}
        {!aiContextQuery.loading && !aiContextQuery.error && aiContextQuery.data ? (
          <div className="card-grid">
            <article className="panel">
              <h3>Context counts</h3>
              <MetricRow label="Products" value={String(aiContextQuery.data.products?.length || 0)} />
              <MetricRow
                label="Compatibility issues"
                value={String(aiContextQuery.data.compatibility_issues?.length || 0)}
              />
              <MetricRow label="Source documents" value={String(aiContextQuery.data.source_documents?.length || 0)} />
              <MetricRow label="Structures" value={String(aiContextQuery.data.home?.buildings?.length || 0)} />
            </article>
            <article className="panel">
              <h3>Grounding policy</h3>
              <MetricRow
                label="Structured facts authoritative"
                value={String(aiContextQuery.data.grounding_policy?.structured_facts_are_authoritative)}
              />
              <MetricRow
                label="AI explains, not invents"
                value={String(aiContextQuery.data.grounding_policy?.ai_should_explain_not_invent)}
              />
              <MetricRow
                label="Rule outputs cited"
                value={String(aiContextQuery.data.grounding_policy?.rule_outputs_must_be_cited_in_explanations)}
              />
              <MetricRow
                label="Transient takeoffs only"
                value={String(aiContextQuery.data.grounding_policy?.takeoff_snapshots_remain_transient)}
              />
            </article>
          </div>
        ) : null}
      </PageSection>
    </>
  );
}
