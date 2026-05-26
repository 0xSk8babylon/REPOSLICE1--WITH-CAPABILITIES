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

function WorkspaceSection({ title, description, children }) {
  return (
    <section className="solution-list">
      <strong>{title}</strong>
      {description ? <p className="callout-copy">{description}</p> : null}
      {children}
    </section>
  );
}

function InspectabilityDetails({ label, inspectability, trustLabel }) {
  if (!inspectability) {
    return null;
  }

  return (
    <details className="solution-list">
      <summary>{label}</summary>
      <div className="trust-row">
        <TrustBadge state={inspectability.trust_state} label={trustLabel || "Planning estimate"} />
        <Badge tone={getConfidenceTone(inspectability.confidence_level)}>
          Confidence: {inspectability.confidence_level}
        </Badge>
      </div>
      <ul>
        {(inspectability.input_signals || []).map((signal) => (
          <li key={signal.key}>
            {signal.label}: {signal.value} ({signal.status.replaceAll("_", " ")})
          </li>
        ))}
      </ul>
      {(inspectability.estimated_inputs || []).length ? (
        <>
          <strong>Estimated inputs</strong>
          <ul>
            {inspectability.estimated_inputs.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </>
      ) : null}
      {(inspectability.incomplete_inputs || []).length ? (
        <>
          <strong>Missing or incomplete inputs</strong>
          <ul>
            {inspectability.incomplete_inputs.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </>
      ) : null}
      {inspectability.partial_provenance_warning ? (
        <p className="callout-copy">{inspectability.partial_provenance_warning}</p>
      ) : null}
    </details>
  );
}

function ConsistencyDetails({ title, consistency }) {
  if (!consistency) {
    return null;
  }

  return (
    <details className="solution-list">
      <summary>{title}</summary>
      <ul>
        <li>Status: {consistency.status}</li>
        <li>Summary: {consistency.summary}</li>
        <li>Reason: {consistency.reason}</li>
        {(consistency.warnings || []).map((item) => (
          <li key={item}>Warning: {item}</li>
        ))}
      </ul>
    </details>
  );
}

function RecommendationSummaryPanel({ recommendation }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <div>
          <h3>Recommended Planning Path</h3>
          <p className="callout-copy">{recommendation.scope_note}</p>
        </div>
        <div className="badge-row">
          {recommendation.recommended_profile ? (
            <Badge tone="info">
              Recommended: {recommendation.recommended_profile.replaceAll("_", " ")}
            </Badge>
          ) : (
            <Badge tone="warning">Recommendation unavailable</Badge>
          )}
          <TrustBadge state="derived_estimate" label="Deterministic planning guidance" />
          <Badge tone={getConfidenceTone(recommendation.confidence_level)}>
            Confidence: {recommendation.confidence_level || "unknown"}
          </Badge>
        </div>
      </div>
      <div className="metric-stack">
        <MetricRow label="Basis" value={recommendation.basis} />
      </div>
    </article>
  );
}

function RecommendationEvidencePanel({ recommendation }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h3>Confidence, Provenance, And Assumptions</h3>
        <div className="badge-row">
          <TrustBadge state="derived_estimate" label="Planning-only trust boundary" />
        </div>
      </div>
      <p className="callout-copy">
        Use the sections below to distinguish known facts, inferred posture, heuristic estimates, and missing inputs before treating the recommendation as actionable.
      </p>
      {recommendation.provenance_summary ? (
        <div className="solution-list">
          <strong>Recommendation provenance</strong>
          <ul>
            <li>Rule basis: {(recommendation.provenance_summary.rule_keys || []).join(", ") || "Not recorded"}</li>
            <li>Source types: {(recommendation.provenance_summary.source_types || []).join(", ") || "Not recorded"}</li>
            <li>Trust posture: {(recommendation.provenance_summary.trust_states || []).join(", ") || "Not recorded"}</li>
          </ul>
        </div>
      ) : null}
      <p className="callout-copy">
        Planning-only framing remains explicit throughout the workspace. The page explains architecture posture and recommendation logic; it does not provide final electrical design, permitting, or utility approval.
      </p>
    </article>
  );
}

function CurrentHomeEnergyArchitecturePanel({ architecture }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h3>Current Home Energy Architecture</h3>
        <div className="badge-row">
          <Badge tone="info">{architecture.inverter_topology}</Badge>
          <TrustBadge
            state={architecture.inspectability?.trust_state || "derived_estimate"}
            label="Planning-only current-state model"
          />
          <Badge tone={getConfidenceTone(architecture.topology_confidence || architecture.inspectability?.confidence_level)}>
            Confidence: {architecture.topology_confidence || architecture.inspectability?.confidence_level || "unknown"}
          </Badge>
        </div>
      </div>
      <div className="metric-stack">
        <MetricRow label="Solar existing state" value={architecture.solar_existing_state} />
        <MetricRow label="Current topology" value={architecture.inverter_topology} />
      </div>
      <p className="callout-copy">{architecture.current_vs_proposed_architecture}</p>
      <p className="callout-copy">{architecture.topology_confidence_reason}</p>
      <p className="callout-copy">{architecture.outage_solar_behavior_note}</p>
      <p className="callout-copy">{architecture.battery_retrofit_implication}</p>
      <p className="callout-copy">{architecture.expansion_implication}</p>
      <p className="callout-copy">{architecture.generator_coexistence_note}</p>
      <details className="solution-list">
        <summary>View architecture relationships</summary>
        <ul>
          {(architecture.architecture_components || []).map((component) => (
            <li key={component.component_key}>
              {component.label}: {component.state.replaceAll("_", " ")}. {component.relationship} {component.note}
            </li>
          ))}
        </ul>
      </details>
      <InspectabilityDetails
        label="View topology evidence and missing inputs"
        inspectability={architecture.inspectability}
        trustLabel="Current topology remains a planning estimate"
      />
      <p className="callout-copy">{architecture.scope_note}</p>
    </article>
  );
}

function BackupScopePanel({ selection }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h3>Backup Scope Posture</h3>
        <div className="badge-row">
          <Badge tone="info">{selection.selected_scope_label}</Badge>
          <TrustBadge
            state={selection.inspectability?.trust_state || "derived_estimate"}
            label="Planning-only outage posture"
          />
          <Badge tone={getConfidenceTone(selection.confidence_level || selection.inspectability?.confidence_level)}>
            Confidence: {selection.confidence_level || selection.inspectability?.confidence_level || "unknown"}
          </Badge>
        </div>
      </div>
      <div className="metric-stack">
        <MetricRow label="Selected load count" value={String(selection.selected_load_count)} />
        <MetricRow label="Selection basis" value={selection.selection_basis.replaceAll("_", " ")} />
        <MetricRow label="Priority band" value={selection.selected_priority_band.replaceAll("_", " ")} />
        <MetricRow label="Outage posture" value={selection.outage_posture} />
        <MetricRow label="Coverage of recorded loads" value={formatCoveragePercent(selection.coverage_ratio_of_recorded_loads)} />
      </div>
      <p className="callout-copy">{selection.selection_reason}</p>
      <p className="callout-copy">{selection.outage_posture_reason}</p>
      <p className="callout-copy">{selection.confidence_reason}</p>
      {selection.planning_gap_warning ? <p className="callout-copy">{selection.planning_gap_warning}</p> : null}
      <InspectabilityDetails
        label="View backup scope evidence and missing inputs"
        inspectability={selection.inspectability}
        trustLabel="Backup scope remains a planning estimate"
      />
      <p className="callout-copy">{selection.scope_note}</p>
    </article>
  );
}

function PanelServicePanel({ architecture }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h3>Panel And Service Posture</h3>
        <div className="badge-row">
          <Badge tone="warning">{architecture.recommended_backup_architecture}</Badge>
          <TrustBadge state="derived_estimate" label="Planning-only architecture direction" />
          <Badge tone={getConfidenceTone(architecture.inspectability?.confidence_level)}>
            Confidence: {architecture.inspectability?.confidence_level || "unknown"}
          </Badge>
        </div>
      </div>
      <div className="metric-stack">
        <MetricRow label="Likely panel/service posture" value={architecture.main_service_panel_posture} />
        <MetricRow label="Current planning direction" value={architecture.recommended_backup_architecture} />
        <MetricRow label="Panel upgrade likelihood" value={architecture.panel_upgrade_likelihood} />
      </div>
      <p className="callout-copy">{architecture.service_upgrade_caution}</p>
      <p className="callout-copy">{architecture.smart_panel_readiness_note}</p>
      <p className="callout-copy">{architecture.generator_integration_readiness_note}</p>
      <ConsistencyDetails title="View architecture consistency" consistency={architecture.architecture_consistency} />
      <InspectabilityDetails
        label="View panel/service evidence and missing inputs"
        inspectability={architecture.inspectability}
        trustLabel="Panel/service posture remains a planning estimate"
      />
      <p className="callout-copy">{architecture.scope_note}</p>
    </article>
  );
}

function InverterSystemPanel({ architecture }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h3>Inverter And System Architecture</h3>
        <div className="badge-row">
          <Badge tone="warning">{architecture.recommended_system_architecture}</Badge>
          <TrustBadge state="derived_estimate" label="Planning-only system direction" />
          <Badge tone={getConfidenceTone(architecture.inspectability?.confidence_level)}>
            Confidence: {architecture.inspectability?.confidence_level || "unknown"}
          </Badge>
        </div>
      </div>
      <div className="metric-stack">
        <MetricRow label="Recorded architecture type" value={architecture.recorded_architecture_type} />
        <MetricRow label="Inverter pathway posture" value={architecture.inverter_pathway_posture} />
        <MetricRow label="AC-coupled suitability" value={architecture.ac_coupled_pathway_suitability} />
        <MetricRow label="Hybrid suitability" value={architecture.hybrid_inverter_pathway_suitability} />
      </div>
      <p className="callout-copy">{architecture.battery_integration_assumption}</p>
      <p className="callout-copy">{architecture.solar_integration_assumption}</p>
      <p className="callout-copy">{architecture.generator_coexistence_assumption}</p>
      <p className="callout-copy">{architecture.expansion_path_posture}</p>
      <p className="callout-copy">{architecture.confidence_reason}</p>
      <ConsistencyDetails title="View system architecture consistency" consistency={architecture.architecture_consistency} />
      <InspectabilityDetails
        label="View inverter/system evidence and missing inputs"
        inspectability={architecture.inspectability}
        trustLabel="System direction remains a planning estimate"
      />
      <p className="callout-copy">{architecture.scope_note}</p>
    </article>
  );
}

function ReasoningGraphPanel({ graph }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h3>Reasoning Graph / Dependency Trace</h3>
        <div className="badge-row">
          <Badge tone="info">{graph.scope_label}</Badge>
          <TrustBadge
            state={graph.inspectability?.trust_state || "derived_estimate"}
            label="Planning-only dependency trace"
          />
          <Badge tone={getConfidenceTone(graph.inspectability?.confidence_level)}>
            Confidence: {graph.inspectability?.confidence_level || "unknown"}
          </Badge>
        </div>
      </div>
      <p className="callout-copy">{graph.summary}</p>
      <details className="solution-list" open>
        <summary>View reasoning nodes</summary>
        <ul>
          {(graph.nodes || []).map((node) => (
            <li key={node.node_id}>
              {node.label}: {node.status.replaceAll("_", " ")}. {node.summary}
            </li>
          ))}
        </ul>
      </details>
      <details className="solution-list" open>
        <summary>View dependency relationships</summary>
        <ul>
          {(graph.dependencies || []).map((dependency) => (
            <li key={`${dependency.source_node_id}-${dependency.target_node_id}-${dependency.relationship}`}>
              {`${dependency.source_node_id} -> ${dependency.target_node_id}: ${dependency.relationship}. ${dependency.summary}`}
            </li>
          ))}
        </ul>
      </details>
      <InspectabilityDetails
        label="View graph evidence and missing inputs"
        inspectability={graph.inspectability}
        trustLabel="Reasoning graph remains a planning trace"
      />
      <p className="callout-copy">{graph.scope_note}</p>
    </article>
  );
}

function RecommendedProfilePanel({ profile }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h3>{profile.label}</h3>
        <div className="badge-row">
          <Badge tone="warning">Current best fit</Badge>
          <TrustBadge state={profile.inspectability?.trust_state || "derived_estimate"} label="Planning-only recommendation" />
        </div>
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
          <strong>Architecture-fit summary</strong>
          <ul>
            <li>Status: {profile.architecture_fit.status}</li>
            <li>Equipment mix: {profile.architecture_fit.equipment_mix_summary}</li>
            <li>Backup path: {profile.architecture_fit.backup_path_summary}</li>
            <li>Summary: {profile.architecture_fit.summary}</li>
            <li>Reason: {profile.architecture_fit.reason}</li>
          </ul>
        </div>
      ) : null}
      <InspectabilityDetails
        label="View recommendation evidence and missing inputs"
        inspectability={profile.inspectability}
        trustLabel="Recommendation remains a planning estimate"
      />
      {profile.battery_sizing_estimate ? (
        <details className="solution-list">
          <summary>View battery planning range</summary>
          <ul>
            <li>
              Backup load energy need:{" "}
              {profile.battery_sizing_estimate.backup_load_energy_need_kwh != null
                ? `${profile.battery_sizing_estimate.backup_load_energy_need_kwh} kWh/day`
                : "Not enough load data yet"}
            </li>
            <li>
              Autonomy target: {profile.battery_sizing_estimate.autonomy_duration_hours_min}-
              {profile.battery_sizing_estimate.autonomy_duration_hours_max} hours
            </li>
            <li>
              Usable capacity posture:{" "}
              {profile.battery_sizing_estimate.usable_battery_capacity_range_kwh
                ? `${profile.battery_sizing_estimate.usable_battery_capacity_range_kwh.min_kwh}-${profile.battery_sizing_estimate.usable_battery_capacity_range_kwh.max_kwh} kWh`
                : "Not enough load data yet"}
            </li>
            <li>
              Recommended battery range:{" "}
              {profile.battery_sizing_estimate.recommended_battery_capacity_range_kwh
                ? `${profile.battery_sizing_estimate.recommended_battery_capacity_range_kwh.min_kwh}-${profile.battery_sizing_estimate.recommended_battery_capacity_range_kwh.max_kwh} kWh`
                : "Not enough load data yet"}
            </li>
          </ul>
          <InspectabilityDetails
            label="View battery sizing evidence"
            inspectability={profile.battery_sizing_estimate.inspectability}
            trustLabel="Battery guidance remains a planning estimate"
          />
          <p className="callout-copy">{profile.battery_sizing_estimate.scope_note}</p>
        </details>
      ) : null}
      {profile.solar_sizing_estimate ? (
        <details className="solution-list">
          <summary>View solar planning range</summary>
          <ul>
            <li>
              Recommended solar range:{" "}
              {profile.solar_sizing_estimate.recommended_solar_capacity_range_kw
                ? `${profile.solar_sizing_estimate.recommended_solar_capacity_range_kw.min_kw}-${profile.solar_sizing_estimate.recommended_solar_capacity_range_kw.max_kw} kW`
                : "Not enough load data yet"}
            </li>
            <li>Recovery posture: {profile.solar_sizing_estimate.recovery_strength.replaceAll("_", " ")}</li>
            <li>Battery recovery relationship: {profile.solar_sizing_estimate.battery_recovery_relationship}</li>
            <li>Site capacity posture: {profile.solar_sizing_estimate.site_capacity_posture}</li>
            <li>Roof sizing confidence: {profile.solar_sizing_estimate.roof_geometry_readiness?.roof_measurement_confidence || "unknown"}</li>
            <li>Measured vs estimated: {profile.solar_sizing_estimate.roof_geometry_readiness?.measured_geometry_status || "unknown"}</li>
          </ul>
          <InspectabilityDetails
            label="View solar sizing evidence"
            inspectability={profile.solar_sizing_estimate.inspectability}
            trustLabel="Solar guidance remains a planning estimate"
          />
          <p className="callout-copy">{profile.solar_sizing_estimate.shading_obstruction_caution}</p>
          <p className="callout-copy">{profile.solar_sizing_estimate.seasonal_production_caution}</p>
          <p className="callout-copy">{profile.solar_sizing_estimate.roof_geometry_readiness?.missing_geometry_warning}</p>
          <p className="callout-copy">{profile.solar_sizing_estimate.low_solar_resilience_note}</p>
          <p className="callout-copy">{profile.solar_sizing_estimate.scope_note}</p>
        </details>
      ) : null}
      {profile.architecture_fit?.tradeoffs?.length || profile.architecture_fit?.warnings?.length ? (
        <details className="solution-list">
          <summary>View tradeoffs and warnings</summary>
          <ul>
            {(profile.architecture_fit?.tradeoffs || []).map((item) => (
              <li key={item}>Tradeoff: {item}</li>
            ))}
            {(profile.architecture_fit?.warnings || []).map((item) => (
              <li key={item}>Warning: {item}</li>
            ))}
          </ul>
        </details>
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
  );
}

function ComparisonProfileCard({ profile }) {
  return (
    <article key={profile.profile} className="panel">
      <div className="panel-header">
        <h3>{profile.label}</h3>
        <Badge tone="info">{profile.profile.replaceAll("_", " ")}</Badge>
      </div>
      <p>{profile.ui_description}</p>
      <div className="metric-stack">
        <MetricRow label="Battery posture" value={profile.battery_sizing_posture.replaceAll("_", " ")} />
        <MetricRow label="Solar posture" value={profile.solar_sizing_posture.replaceAll("_", " ")} />
        <MetricRow label="Growth margin" value={profile.future_growth_margin_posture.replaceAll("_", " ")} />
      </div>
      {profile.architecture_fit ? (
        <div className="solution-list">
          <strong>Architecture-fit snapshot</strong>
          <ul>
            <li>Status: {profile.architecture_fit.status}</li>
            <li>Summary: {profile.architecture_fit.summary}</li>
            <li>Reason: {profile.architecture_fit.reason}</li>
          </ul>
        </div>
      ) : null}
    </article>
  );
}

function RecommendationWorkspace({ recommendation }) {
  const recommendedProfile = (recommendation.profiles || []).find((profile) => profile.recommended);
  const alternateProfiles = (recommendation.profiles || []).filter((profile) => !profile.recommended);

  return (
    <article className="panel">
      <RecommendationSummaryPanel recommendation={recommendation} />

      <WorkspaceSection
        title="Current State"
        description="Understand what the home appears to have today before reading the future architecture path."
      >
        <div className="card-grid">
          {recommendation.current_home_energy_architecture ? (
            <CurrentHomeEnergyArchitecturePanel architecture={recommendation.current_home_energy_architecture} />
          ) : null}
          {recommendation.backup_load_selection ? (
            <BackupScopePanel selection={recommendation.backup_load_selection} />
          ) : null}
        </div>
      </WorkspaceSection>

      <WorkspaceSection
        title="Existing Vs Proposed System Posture"
        description="Read the current architecture constraints first, then the future backup and inverter direction they support."
      >
        <div className="card-grid">
          {recommendation.panel_service_architecture ? (
            <PanelServicePanel architecture={recommendation.panel_service_architecture} />
          ) : null}
          {recommendation.inverter_system_architecture ? (
            <InverterSystemPanel architecture={recommendation.inverter_system_architecture} />
          ) : null}
        </div>
      </WorkspaceSection>

      <WorkspaceSection
        title="Recommendation Workspace"
        description="The recommended profile stays in the primary path. Alternate profiles remain visible as comparison material, not competing primary calls to action."
      >
        {recommendedProfile ? <RecommendedProfilePanel profile={recommendedProfile} /> : null}
        {alternateProfiles.length ? (
          <>
            <p className="callout-copy">Alternate planning profiles remain available for comparison if priorities shift.</p>
            <div className="card-grid">
              {alternateProfiles.map((profile) => (
                <ComparisonProfileCard key={profile.profile} profile={profile} />
              ))}
            </div>
          </>
        ) : null}
      </WorkspaceSection>

      <WorkspaceSection
        title="Reasoning And Evidence"
        description="Dependency trace, provenance, and missing-input review stay available without turning the whole page into an inspectability dump."
      >
        <div className="card-grid">
          {recommendation.reasoning_graph ? <ReasoningGraphPanel graph={recommendation.reasoning_graph} /> : null}
          <RecommendationEvidencePanel recommendation={recommendation} />
        </div>
      </WorkspaceSection>
    </article>
  );
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
        description="A deterministic energy planning workspace: current state first, proposed system path second, reasoning and trust boundaries always visible."
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
        description="Current-state architecture, proposed planning path, and dependency trace stay separate so the workspace explains the system without acting like a generic dashboard."
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
                <details className="solution-list">
                  <summary>View recommended next steps</summary>
                  <ul>
                    {(advisorQuery.data.completeness?.recommended_next_steps || []).map((step) => (
                      <li key={step}>{step}</li>
                    ))}
                  </ul>
                </details>
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
              <RecommendationWorkspace recommendation={advisorQuery.data.recommendation_profiles} />
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
                  <details className="solution-list">
                    <summary>View provenance</summary>
                    <ul>
                      <li>Basis: {issue.provenance_summary.basis}</li>
                      <li>Source types: {(issue.provenance_summary.source_types || []).join(", ") || "Not recorded"}</li>
                      <li>Rule keys: {(issue.provenance_summary.rule_keys || []).join(", ") || "Not recorded"}</li>
                    </ul>
                  </details>
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
              <MetricRow label="Compatibility issues" value={String(aiContextQuery.data.compatibility_issues?.length || 0)} />
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
