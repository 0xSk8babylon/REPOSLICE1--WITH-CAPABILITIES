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

function getConfidenceTone(confidenceLevel) {
  if (confidenceLevel === "high") {
    return "info";
  }
  if (confidenceLevel === "medium") {
    return "warning";
  }
  return "danger";
}

function formatCoveragePercent(ratio) {
  if (typeof ratio !== "number") {
    return "Not recorded";
  }
  return `${Math.round(ratio * 100)}%`;
}

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
            {advisorQuery.data.recommendation_profiles ? (
              <article className="panel">
                <div className="panel-header">
                  <div>
                    <h3>Recommendation Profiles</h3>
                    <p className="callout-copy">{advisorQuery.data.recommendation_profiles.scope_note}</p>
                  </div>
                  <div className="badge-row">
                    {advisorQuery.data.recommendation_profiles.recommended_profile ? (
                      <Badge tone="info">
                        Recommended: {advisorQuery.data.recommendation_profiles.recommended_profile.replaceAll("_", " ")}
                      </Badge>
                    ) : (
                      <Badge tone="warning">Recommendation unavailable</Badge>
                    )}
                    <TrustBadge state="derived_estimate" label="Deterministic planning guidance" />
                  </div>
                </div>
                <div className="metric-stack">
                  <MetricRow label="Confidence" value={advisorQuery.data.recommendation_profiles.confidence_level || "unknown"} />
                  <MetricRow label="Basis" value={advisorQuery.data.recommendation_profiles.basis} />
                </div>
                {advisorQuery.data.recommendation_profiles.provenance_summary ? (
                  <div className="solution-list">
                    <strong>Recommendation provenance</strong>
                    <ul>
                      <li>Rule basis: {(advisorQuery.data.recommendation_profiles.provenance_summary.rule_keys || []).join(", ") || "Not recorded"}</li>
                      <li>Source types: {(advisorQuery.data.recommendation_profiles.provenance_summary.source_types || []).join(", ") || "Not recorded"}</li>
                      <li>Trust posture: {(advisorQuery.data.recommendation_profiles.provenance_summary.trust_states || []).join(", ") || "Not recorded"}</li>
                    </ul>
                  </div>
                ) : null}
                {advisorQuery.data.recommendation_profiles.backup_load_selection ? (
                  <div className="panel">
                    <div className="panel-header">
                      <h3>Backup Scope Selection</h3>
                      <div className="badge-row">
                        <Badge tone="info">
                          {advisorQuery.data.recommendation_profiles.backup_load_selection.selected_scope_label}
                        </Badge>
                        <TrustBadge
                          state={advisorQuery.data.recommendation_profiles.backup_load_selection.inspectability?.trust_state || "derived_estimate"}
                          label="Planning-only outage posture"
                        />
                        <Badge
                          tone={getConfidenceTone(
                            advisorQuery.data.recommendation_profiles.backup_load_selection.confidence_level ||
                              advisorQuery.data.recommendation_profiles.backup_load_selection.inspectability?.confidence_level
                          )}
                        >
                          Confidence:{" "}
                          {advisorQuery.data.recommendation_profiles.backup_load_selection.confidence_level ||
                            advisorQuery.data.recommendation_profiles.backup_load_selection.inspectability?.confidence_level ||
                            "unknown"}
                        </Badge>
                      </div>
                    </div>
                    <div className="metric-stack">
                      <MetricRow
                        label="Selected load count"
                        value={String(advisorQuery.data.recommendation_profiles.backup_load_selection.selected_load_count)}
                      />
                      <MetricRow
                        label="Selection basis"
                        value={advisorQuery.data.recommendation_profiles.backup_load_selection.selection_basis.replaceAll("_", " ")}
                      />
                      <MetricRow
                        label="Priority band"
                        value={advisorQuery.data.recommendation_profiles.backup_load_selection.selected_priority_band.replaceAll("_", " ")}
                      />
                      <MetricRow
                        label="Outage posture"
                        value={advisorQuery.data.recommendation_profiles.backup_load_selection.outage_posture}
                      />
                      <MetricRow
                        label="Coverage of recorded loads"
                        value={formatCoveragePercent(
                          advisorQuery.data.recommendation_profiles.backup_load_selection.coverage_ratio_of_recorded_loads
                        )}
                      />
                    </div>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.backup_load_selection.selection_reason}
                    </p>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.backup_load_selection.outage_posture_reason}
                    </p>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.backup_load_selection.confidence_reason}
                    </p>
                    {advisorQuery.data.recommendation_profiles.backup_load_selection.planning_gap_warning ? (
                      <p className="callout-copy">
                        {advisorQuery.data.recommendation_profiles.backup_load_selection.planning_gap_warning}
                      </p>
                    ) : null}
                    {advisorQuery.data.recommendation_profiles.backup_load_selection.inspectability ? (
                      <div className="solution-list">
                        <strong>Selection basis</strong>
                        <ul>
                          {(advisorQuery.data.recommendation_profiles.backup_load_selection.inspectability.input_signals || []).map((signal) => (
                            <li key={signal.key}>
                              {signal.label}: {signal.value} ({signal.status.replaceAll("_", " ")})
                            </li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                    {advisorQuery.data.recommendation_profiles.backup_load_selection.inspectability?.partial_provenance_warning ? (
                      <p className="callout-copy">
                        {advisorQuery.data.recommendation_profiles.backup_load_selection.inspectability.partial_provenance_warning}
                      </p>
                    ) : null}
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.backup_load_selection.scope_note}
                    </p>
                  </div>
                ) : null}
                {advisorQuery.data.recommendation_profiles.panel_service_architecture ? (
                  <div className="panel">
                    <div className="panel-header">
                      <h3>Panel And Service Posture</h3>
                      <div className="badge-row">
                        <Badge tone="warning">
                          {advisorQuery.data.recommendation_profiles.panel_service_architecture.recommended_backup_architecture}
                        </Badge>
                        <TrustBadge state="derived_estimate" label="Planning-only architecture direction" />
                        <Badge
                          tone={getConfidenceTone(
                            advisorQuery.data.recommendation_profiles.panel_service_architecture.inspectability?.confidence_level
                          )}
                        >
                          Confidence:{" "}
                          {advisorQuery.data.recommendation_profiles.panel_service_architecture.inspectability?.confidence_level || "unknown"}
                        </Badge>
                      </div>
                    </div>
                    <div className="metric-stack">
                      <MetricRow
                        label="Likely panel/service posture"
                        value={advisorQuery.data.recommendation_profiles.panel_service_architecture.main_service_panel_posture}
                      />
                      <MetricRow
                        label="Current planning direction"
                        value={advisorQuery.data.recommendation_profiles.panel_service_architecture.recommended_backup_architecture}
                      />
                      <MetricRow
                        label="Panel upgrade likelihood"
                        value={advisorQuery.data.recommendation_profiles.panel_service_architecture.panel_upgrade_likelihood}
                      />
                    </div>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.panel_service_architecture.service_upgrade_caution}
                    </p>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.panel_service_architecture.smart_panel_readiness_note}
                    </p>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.panel_service_architecture.generator_integration_readiness_note}
                    </p>
                    {advisorQuery.data.recommendation_profiles.panel_service_architecture.architecture_consistency ? (
                      <div className="solution-list">
                        <strong>Architecture consistency</strong>
                        <ul>
                          <li>
                            Status:{" "}
                            {advisorQuery.data.recommendation_profiles.panel_service_architecture.architecture_consistency.status}
                          </li>
                          <li>
                            Summary:{" "}
                            {advisorQuery.data.recommendation_profiles.panel_service_architecture.architecture_consistency.summary}
                          </li>
                          <li>
                            Reason:{" "}
                            {advisorQuery.data.recommendation_profiles.panel_service_architecture.architecture_consistency.reason}
                          </li>
                          {(
                            advisorQuery.data.recommendation_profiles.panel_service_architecture.architecture_consistency.warnings || []
                          ).map((item) => (
                            <li key={item}>Warning: {item}</li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                    {advisorQuery.data.recommendation_profiles.panel_service_architecture.inspectability ? (
                      <div className="solution-list">
                        <strong>Architecture basis</strong>
                        <ul>
                          {(
                            advisorQuery.data.recommendation_profiles.panel_service_architecture.inspectability.input_signals || []
                          ).map((signal) => (
                            <li key={signal.key}>
                              {signal.label}: {signal.value} ({signal.status.replaceAll("_", " ")})
                            </li>
                          ))}
                        </ul>
                        {(
                          advisorQuery.data.recommendation_profiles.panel_service_architecture.inspectability.estimated_inputs || []
                        ).length ? (
                          <>
                            <strong>Estimated inputs</strong>
                            <ul>
                              {advisorQuery.data.recommendation_profiles.panel_service_architecture.inspectability.estimated_inputs.map((item) => (
                                <li key={item}>{item}</li>
                              ))}
                            </ul>
                          </>
                        ) : null}
                        {(
                          advisorQuery.data.recommendation_profiles.panel_service_architecture.inspectability.incomplete_inputs || []
                        ).length ? (
                          <>
                            <strong>Incomplete inputs</strong>
                            <ul>
                              {advisorQuery.data.recommendation_profiles.panel_service_architecture.inspectability.incomplete_inputs.map((item) => (
                                <li key={item}>{item}</li>
                              ))}
                            </ul>
                          </>
                        ) : null}
                      </div>
                    ) : null}
                    {advisorQuery.data.recommendation_profiles.panel_service_architecture.inspectability?.partial_provenance_warning ? (
                      <p className="callout-copy">
                        {advisorQuery.data.recommendation_profiles.panel_service_architecture.inspectability.partial_provenance_warning}
                      </p>
                    ) : null}
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.panel_service_architecture.scope_note}
                    </p>
                  </div>
                ) : null}
                {advisorQuery.data.recommendation_profiles.inverter_system_architecture ? (
                  <div className="panel">
                    <div className="panel-header">
                      <h3>Inverter And System Architecture</h3>
                      <div className="badge-row">
                        <Badge tone="warning">
                          {advisorQuery.data.recommendation_profiles.inverter_system_architecture.recommended_system_architecture}
                        </Badge>
                        <TrustBadge state="derived_estimate" label="Planning-only system direction" />
                        <Badge
                          tone={getConfidenceTone(
                            advisorQuery.data.recommendation_profiles.inverter_system_architecture.inspectability?.confidence_level
                          )}
                        >
                          Confidence:{" "}
                          {advisorQuery.data.recommendation_profiles.inverter_system_architecture.inspectability?.confidence_level || "unknown"}
                        </Badge>
                      </div>
                    </div>
                    <div className="metric-stack">
                      <MetricRow
                        label="Recorded architecture type"
                        value={advisorQuery.data.recommendation_profiles.inverter_system_architecture.recorded_architecture_type}
                      />
                      <MetricRow
                        label="Inverter pathway posture"
                        value={advisorQuery.data.recommendation_profiles.inverter_system_architecture.inverter_pathway_posture}
                      />
                      <MetricRow
                        label="AC-coupled suitability"
                        value={advisorQuery.data.recommendation_profiles.inverter_system_architecture.ac_coupled_pathway_suitability}
                      />
                      <MetricRow
                        label="Hybrid suitability"
                        value={advisorQuery.data.recommendation_profiles.inverter_system_architecture.hybrid_inverter_pathway_suitability}
                      />
                    </div>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.inverter_system_architecture.battery_integration_assumption}
                    </p>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.inverter_system_architecture.solar_integration_assumption}
                    </p>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.inverter_system_architecture.generator_coexistence_assumption}
                    </p>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.inverter_system_architecture.expansion_path_posture}
                    </p>
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.inverter_system_architecture.confidence_reason}
                    </p>
                    {advisorQuery.data.recommendation_profiles.inverter_system_architecture.architecture_consistency ? (
                      <div className="solution-list">
                        <strong>System architecture consistency</strong>
                        <ul>
                          <li>
                            Status:{" "}
                            {advisorQuery.data.recommendation_profiles.inverter_system_architecture.architecture_consistency.status}
                          </li>
                          <li>
                            Summary:{" "}
                            {advisorQuery.data.recommendation_profiles.inverter_system_architecture.architecture_consistency.summary}
                          </li>
                          <li>
                            Reason:{" "}
                            {advisorQuery.data.recommendation_profiles.inverter_system_architecture.architecture_consistency.reason}
                          </li>
                          {(
                            advisorQuery.data.recommendation_profiles.inverter_system_architecture.architecture_consistency.warnings || []
                          ).map((item) => (
                            <li key={item}>Warning: {item}</li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                    {advisorQuery.data.recommendation_profiles.inverter_system_architecture.inspectability ? (
                      <div className="solution-list">
                        <strong>System architecture basis</strong>
                        <ul>
                          {(
                            advisorQuery.data.recommendation_profiles.inverter_system_architecture.inspectability.input_signals || []
                          ).map((signal) => (
                            <li key={signal.key}>
                              {signal.label}: {signal.value} ({signal.status.replaceAll("_", " ")})
                            </li>
                          ))}
                        </ul>
                        {(
                          advisorQuery.data.recommendation_profiles.inverter_system_architecture.inspectability.estimated_inputs || []
                        ).length ? (
                          <>
                            <strong>Estimated inputs</strong>
                            <ul>
                              {advisorQuery.data.recommendation_profiles.inverter_system_architecture.inspectability.estimated_inputs.map((item) => (
                                <li key={item}>{item}</li>
                              ))}
                            </ul>
                          </>
                        ) : null}
                        {(
                          advisorQuery.data.recommendation_profiles.inverter_system_architecture.inspectability.incomplete_inputs || []
                        ).length ? (
                          <>
                            <strong>Incomplete inputs</strong>
                            <ul>
                              {advisorQuery.data.recommendation_profiles.inverter_system_architecture.inspectability.incomplete_inputs.map((item) => (
                                <li key={item}>{item}</li>
                              ))}
                            </ul>
                          </>
                        ) : null}
                      </div>
                    ) : null}
                    {advisorQuery.data.recommendation_profiles.inverter_system_architecture.inspectability?.partial_provenance_warning ? (
                      <p className="callout-copy">
                        {advisorQuery.data.recommendation_profiles.inverter_system_architecture.inspectability.partial_provenance_warning}
                      </p>
                    ) : null}
                    <p className="callout-copy">
                      {advisorQuery.data.recommendation_profiles.inverter_system_architecture.scope_note}
                    </p>
                  </div>
                ) : null}
                {advisorQuery.data.recommendation_profiles.reasoning_graph ? (
                  <div className="panel">
                    <div className="panel-header">
                      <h3>Structured Reasoning Graph</h3>
                      <div className="badge-row">
                        <Badge tone="info">
                          {advisorQuery.data.recommendation_profiles.reasoning_graph.scope_label}
                        </Badge>
                        <TrustBadge
                          state={advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability?.trust_state || "derived_estimate"}
                          label="Planning-only dependency trace"
                        />
                        <Badge
                          tone={getConfidenceTone(
                            advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability?.confidence_level
                          )}
                        >
                          Confidence:{" "}
                          {advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability?.confidence_level || "unknown"}
                        </Badge>
                      </div>
                    </div>
                    <p className="callout-copy">{advisorQuery.data.recommendation_profiles.reasoning_graph.summary}</p>
                    <div className="solution-list">
                      <strong>Reasoning nodes</strong>
                      <ul>
                        {(advisorQuery.data.recommendation_profiles.reasoning_graph.nodes || []).map((node) => (
                          <li key={node.node_id}>
                            {node.label}: {node.status.replaceAll("_", " ")}. {node.summary}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div className="solution-list">
                      <strong>Reasoning dependencies</strong>
                      <ul>
                        {(advisorQuery.data.recommendation_profiles.reasoning_graph.dependencies || []).map((dependency) => (
                          <li key={`${dependency.source_node_id}-${dependency.target_node_id}-${dependency.relationship}`}>
                            {`${dependency.source_node_id} -> ${dependency.target_node_id}: ${dependency.relationship}. ${dependency.summary}`}
                          </li>
                        ))}
                      </ul>
                    </div>
                    {advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability ? (
                      <div className="solution-list">
                        <strong>Graph basis</strong>
                        <ul>
                          {(advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability.input_signals || []).map((signal) => (
                            <li key={signal.key}>
                              {signal.label}: {signal.value} ({signal.status.replaceAll("_", " ")})
                            </li>
                          ))}
                        </ul>
                        {(advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability.estimated_inputs || []).length ? (
                          <>
                            <strong>Estimated inputs</strong>
                            <ul>
                              {advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability.estimated_inputs.map((item) => (
                                <li key={item}>{item}</li>
                              ))}
                            </ul>
                          </>
                        ) : null}
                        {(advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability.incomplete_inputs || []).length ? (
                          <>
                            <strong>Incomplete inputs</strong>
                            <ul>
                              {advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability.incomplete_inputs.map((item) => (
                                <li key={item}>{item}</li>
                              ))}
                            </ul>
                          </>
                        ) : null}
                      </div>
                    ) : null}
                    {advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability?.partial_provenance_warning ? (
                      <p className="callout-copy">
                        {advisorQuery.data.recommendation_profiles.reasoning_graph.inspectability.partial_provenance_warning}
                      </p>
                    ) : null}
                    <p className="callout-copy">{advisorQuery.data.recommendation_profiles.reasoning_graph.scope_note}</p>
                  </div>
                ) : null}
                <div className="card-grid">
                  {(advisorQuery.data.recommendation_profiles.profiles || []).map((profile) => (
                    <article key={profile.profile} className="panel">
                      <div className="panel-header">
                        <h3>{profile.label}</h3>
                        {profile.recommended ? <Badge tone="warning">Current best fit</Badge> : null}
                      </div>
                      <p>{profile.ui_description}</p>
                      <div className="metric-stack">
                        <MetricRow label="Intent" value={profile.intent} />
                        <MetricRow label="Battery posture" value={profile.battery_sizing_posture.replaceAll("_", " ")} />
                        <MetricRow label="Solar posture" value={profile.solar_sizing_posture.replaceAll("_", " ")} />
                        <MetricRow label="Reserve posture" value={profile.autonomy_reserve_posture.replaceAll("_", " ")} />
                        <MetricRow label="Growth margin" value={profile.future_growth_margin_posture.replaceAll("_", " ")} />
                        <MetricRow label="Low-solar stance" value={profile.low_solar_assumption_posture.replaceAll("_", " ")} />
                      </div>
                      {profile.architecture_fit ? (
                        <div className="solution-list">
                          <strong>Architecture-fit tradeoffs</strong>
                          <ul>
                            <li>Status: {profile.architecture_fit.status}</li>
                            <li>Equipment mix: {profile.architecture_fit.equipment_mix_summary}</li>
                            <li>Backup path: {profile.architecture_fit.backup_path_summary}</li>
                            <li>Summary: {profile.architecture_fit.summary}</li>
                            <li>Reason: {profile.architecture_fit.reason}</li>
                            {(profile.architecture_fit.tradeoffs || []).map((item) => (
                              <li key={item}>Tradeoff: {item}</li>
                            ))}
                            {(profile.architecture_fit.warnings || []).map((item) => (
                              <li key={item}>Warning: {item}</li>
                            ))}
                          </ul>
                        </div>
                      ) : null}
                      {profile.recommended && profile.inspectability ? (
                        <div className="solution-list">
                          <strong>What this recommendation is based on</strong>
                          <ul>
                            {(profile.inspectability.input_signals || []).map((signal) => (
                              <li key={signal.key}>
                                {signal.label}: {signal.value} ({signal.status.replaceAll("_", " ")})
                              </li>
                            ))}
                          </ul>
                          <div className="trust-row">
                            <TrustBadge state={profile.inspectability.trust_state} label="Recommendation remains a planning estimate" />
                            <Badge tone={profile.inspectability.confidence_level === "high" ? "info" : profile.inspectability.confidence_level === "medium" ? "warning" : "danger"}>
                              Confidence: {profile.inspectability.confidence_level}
                            </Badge>
                          </div>
                          {(profile.inspectability.estimated_inputs || []).length ? (
                            <>
                              <strong>Estimated inputs</strong>
                              <ul>
                                {profile.inspectability.estimated_inputs.map((item) => (
                                  <li key={item}>{item}</li>
                                ))}
                              </ul>
                            </>
                          ) : null}
                          {(profile.inspectability.incomplete_inputs || []).length ? (
                            <>
                              <strong>Incomplete inputs</strong>
                              <ul>
                                {profile.inspectability.incomplete_inputs.map((item) => (
                                  <li key={item}>{item}</li>
                                ))}
                              </ul>
                            </>
                          ) : null}
                          {profile.inspectability.partial_provenance_warning ? (
                            <p className="callout-copy">{profile.inspectability.partial_provenance_warning}</p>
                          ) : null}
                        </div>
                      ) : null}
                      {profile.battery_sizing_estimate ? (
                        <div className="solution-list">
                          <strong>Battery planning range</strong>
                          <ul>
                            <li>Backup load energy need: {profile.battery_sizing_estimate.backup_load_energy_need_kwh != null ? `${profile.battery_sizing_estimate.backup_load_energy_need_kwh} kWh/day` : "Not enough load data yet"}</li>
                            <li>Autonomy target: {profile.battery_sizing_estimate.autonomy_duration_hours_min}-{profile.battery_sizing_estimate.autonomy_duration_hours_max} hours</li>
                            <li>Usable capacity posture: {profile.battery_sizing_estimate.usable_battery_capacity_range_kwh ? `${profile.battery_sizing_estimate.usable_battery_capacity_range_kwh.min_kwh}-${profile.battery_sizing_estimate.usable_battery_capacity_range_kwh.max_kwh} kWh` : "Not enough load data yet"}</li>
                            <li>Recommended battery range: {profile.battery_sizing_estimate.recommended_battery_capacity_range_kwh ? `${profile.battery_sizing_estimate.recommended_battery_capacity_range_kwh.min_kwh}-${profile.battery_sizing_estimate.recommended_battery_capacity_range_kwh.max_kwh} kWh` : "Not enough load data yet"}</li>
                          </ul>
                          {profile.recommended && profile.battery_sizing_estimate.inspectability ? (
                            <>
                              <strong>Battery guidance basis</strong>
                              <ul>
                                {(profile.battery_sizing_estimate.inspectability.input_signals || []).map((signal) => (
                                  <li key={signal.key}>
                                    {signal.label}: {signal.value} ({signal.status.replaceAll("_", " ")})
                                  </li>
                                ))}
                              </ul>
                              {(profile.battery_sizing_estimate.inspectability.estimated_inputs || []).length ? (
                                <ul>
                                  {profile.battery_sizing_estimate.inspectability.estimated_inputs.map((item) => (
                                    <li key={item}>{item}</li>
                                  ))}
                                </ul>
                              ) : null}
                              {(profile.battery_sizing_estimate.inspectability.incomplete_inputs || []).length ? (
                                <ul>
                                  {profile.battery_sizing_estimate.inspectability.incomplete_inputs.map((item) => (
                                    <li key={item}>{item}</li>
                                  ))}
                                </ul>
                              ) : null}
                              {profile.battery_sizing_estimate.inspectability.partial_provenance_warning ? (
                                <p className="callout-copy">{profile.battery_sizing_estimate.inspectability.partial_provenance_warning}</p>
                              ) : null}
                            </>
                          ) : null}
                          <p className="callout-copy">{profile.battery_sizing_estimate.scope_note}</p>
                        </div>
                      ) : null}
                      {profile.solar_sizing_estimate ? (
                        <div className="solution-list">
                          <strong>Solar planning range</strong>
                          <ul>
                            <li>Recommended solar range: {profile.solar_sizing_estimate.recommended_solar_capacity_range_kw ? `${profile.solar_sizing_estimate.recommended_solar_capacity_range_kw.min_kw}-${profile.solar_sizing_estimate.recommended_solar_capacity_range_kw.max_kw} kW` : "Not enough load data yet"}</li>
                            <li>Recovery posture: {profile.solar_sizing_estimate.recovery_strength.replaceAll("_", " ")}</li>
                            <li>Battery recovery relationship: {profile.solar_sizing_estimate.battery_recovery_relationship}</li>
                            <li>Site capacity posture: {profile.solar_sizing_estimate.site_capacity_posture}</li>
                            <li>Roof sizing confidence: {profile.solar_sizing_estimate.roof_geometry_readiness?.roof_measurement_confidence || "unknown"}</li>
                            <li>Measured vs estimated: {profile.solar_sizing_estimate.roof_geometry_readiness?.measured_geometry_status || "unknown"}</li>
                          </ul>
                          {profile.recommended && profile.solar_sizing_estimate.inspectability ? (
                            <>
                              <strong>Solar guidance basis</strong>
                              <ul>
                                {(profile.solar_sizing_estimate.inspectability.input_signals || []).map((signal) => (
                                  <li key={signal.key}>
                                    {signal.label}: {signal.value} ({signal.status.replaceAll("_", " ")})
                                  </li>
                                ))}
                              </ul>
                              {(profile.solar_sizing_estimate.inspectability.estimated_inputs || []).length ? (
                                <ul>
                                  {profile.solar_sizing_estimate.inspectability.estimated_inputs.map((item) => (
                                    <li key={item}>{item}</li>
                                  ))}
                                </ul>
                              ) : null}
                              {(profile.solar_sizing_estimate.inspectability.incomplete_inputs || []).length ? (
                                <ul>
                                  {profile.solar_sizing_estimate.inspectability.incomplete_inputs.map((item) => (
                                    <li key={item}>{item}</li>
                                  ))}
                                </ul>
                              ) : null}
                              {profile.solar_sizing_estimate.inspectability.partial_provenance_warning ? (
                                <p className="callout-copy">{profile.solar_sizing_estimate.inspectability.partial_provenance_warning}</p>
                              ) : null}
                            </>
                          ) : null}
                          <p className="callout-copy">{profile.solar_sizing_estimate.shading_obstruction_caution}</p>
                          <p className="callout-copy">{profile.solar_sizing_estimate.seasonal_production_caution}</p>
                          <p className="callout-copy">{profile.solar_sizing_estimate.roof_geometry_readiness?.missing_geometry_warning}</p>
                          <p className="callout-copy">{profile.solar_sizing_estimate.low_solar_resilience_note}</p>
                          <p className="callout-copy">{profile.solar_sizing_estimate.scope_note}</p>
                        </div>
                      ) : null}
                      <div className="solution-list">
                        <strong>Behavioral assumptions</strong>
                        <ul>
                          {(profile.behavioral_assumptions || []).map((assumption) => (
                            <li key={assumption}>{assumption}</li>
                          ))}
                        </ul>
                      </div>
                      <p className="callout-copy">{profile.fit_reason}</p>
                    </article>
                  ))}
                </div>
              </article>
            ) : null}
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
