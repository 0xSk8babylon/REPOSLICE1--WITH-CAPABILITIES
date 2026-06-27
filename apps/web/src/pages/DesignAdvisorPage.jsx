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

function getStateTone(state) {
  if (state === "existing" || state === "recorded") {
    return "success";
  }
  if (state === "proposed" || state === "planning_assumption" || state === "rule_based") {
    return "warning";
  }
  if (state === "missing" || state === "unknown") {
    return "danger";
  }
  return "info";
}

function getDependencyTone(relationship) {
  if (relationship.includes("grounds") || relationship.includes("anchors")) {
    return "info";
  }
  if (relationship.includes("bounds") || relationship.includes("constrains")) {
    return "warning";
  }
  return "default";
}

function getProfileFamily(profileKey) {
  if (!profileKey) {
    return { label: "planning pathway", tone: "info" };
  }
  if (profileKey.includes("premium")) {
    return { label: "future ready", tone: "warning" };
  }
  if (profileKey.includes("critical")) {
    return { label: "constrained", tone: "danger" };
  }
  if (profileKey.includes("balanced") || profileKey.includes("conservative")) {
    return { label: "staged", tone: "info" };
  }
  return { label: "planning pathway", tone: "info" };
}

function getPathwayRole(profile) {
  if (profile?.recommended) {
    return { label: "recommended pathway", tone: "warning" };
  }
  return getProfileFamily(profile?.profile);
}

function getPlanningStateTone(role) {
  if (role === "current_state") {
    return "success";
  }
  if (role === "future_ready_pathway") {
    return "warning";
  }
  if (role === "constrained_pathway") {
    return "danger";
  }
  return "info";
}

function formatStateLabel(value) {
  if (!value) {
    return "not recorded";
  }
  return value.replaceAll("_", " ");
}

function formatInlineList(items, fallback = "Not recorded") {
  return (items || []).length ? items.join(", ") : fallback;
}

function formatEntityRef(ref) {
  const role = ref.role ? ` (${formatStateLabel(ref.role)})` : "";
  return `${ref.entity_type}:${ref.entity_id}${role}`;
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

function TrustEnvelopeSummary({ envelope }) {
  if (!envelope) {
    return (
      <div className="solution-list">
        <strong>Trust and source context</strong>
        <p className="callout-copy">No trust envelope was returned for this block, so its advisory details are not shown here.</p>
      </div>
    );
  }

  const provenanceRefs = envelope.provenance_refs || [];

  return (
    <div className="solution-list">
      <strong>Trust and source context</strong>
      <div className="trust-row">
        <Badge tone="info">{formatStateLabel(envelope.authority_layer)}</Badge>
        <Badge tone={getConfidenceTone(envelope.confidence_level)}>
          Confidence: {envelope.confidence_level || "not recorded"}
        </Badge>
        <Badge tone={envelope.provisional ? "warning" : "success"}>
          {envelope.provisional ? "provisional" : "not provisional"}
        </Badge>
        <Badge>{formatStateLabel(envelope.trust_zone)}</Badge>
      </div>
      <ul>
        <li>Data classification: {formatStateLabel(envelope.data_classification)}</li>
        <li>Provenance refs: {provenanceRefs.length}</li>
        <li>Missing inputs: {formatInlineList(envelope.missing_inputs)}</li>
        <li>Assumptions: {formatInlineList(envelope.assumptions)}</li>
        <li>Scope limits: {formatInlineList(envelope.scope_limitations)}</li>
      </ul>
      {provenanceRefs.length ? (
        <details>
          <summary>View source references</summary>
          <ul>
            {provenanceRefs.map((ref, index) => (
              <li key={`${ref.entity_type}-${ref.entity_id}-${ref.role || "source"}-${index}`}>
                {formatEntityRef(ref)}
              </li>
            ))}
          </ul>
        </details>
      ) : null}
    </div>
  );
}

function PlannerBlockPanel({ title, description, envelope, children }) {
  if (!envelope) {
    return null;
  }

  return (
    <article className="panel">
      <div className="panel-header">
        <div>
          <h3>{title}</h3>
          {description ? <p className="callout-copy">{description}</p> : null}
        </div>
        <div className="badge-row">
          <TrustBadge state="derived_estimate" label="Source-linked planning view" />
          <Badge tone={getConfidenceTone(envelope.confidence_level)}>
            Confidence: {envelope.confidence_level || "not recorded"}
          </Badge>
        </div>
      </div>
      <TrustEnvelopeSummary envelope={envelope} />
      {children}
    </article>
  );
}

function PlannerIntelligencePanel({ summary }) {
  const blocks = summary?.blocks || {};
  const recommendations = blocks.recommendations;
  const recommendation = recommendations?.recommendation;
  const constraints = blocks.constraints;
  const readiness = blocks.readiness_explanation;
  const completeness = readiness?.completeness || {};
  const upgradePath = blocks.upgrade_path_explanation;
  const planningState = upgradePath?.planning_state;
  const readinessContext = upgradePath?.readiness_context || {};
  const scenarioComparison = blocks.scenario_comparison_explanation;
  const comparison = scenarioComparison?.comparison || {};
  const provenance = blocks.provenance_summary;

  return (
    <div className="solution-list">
      <div className="panel-header">
        <div>
          <h3>Why / Sources</h3>
          <p className="callout-copy">
            Read-only source context from the backend summary. This panel explains why planner-intelligence blocks
            exist; it does not direct homeowner action, choose a design, create a proposal, or replace professional
            review.
          </p>
        </div>
        <div className="badge-row">
          <Badge tone="danger">Not engineering approval</Badge>
          <TrustBadge state="derived_estimate" label="Advisory explanation" />
        </div>
      </div>

      {(summary.limitations || []).length ? (
        <div className="solution-list">
          <strong>View boundary</strong>
          <ul>
            {summary.limitations.map((limitation) => (
              <li key={limitation}>{limitation}</li>
            ))}
          </ul>
        </div>
      ) : null}
      <p className="callout-copy">
        Owner workflow boundary: recommendation and comparison fields are displayed only as traceable planning
        context. They are not homeowner directives, final design guidance, product recommendations, ranked choices,
        savings/payback estimates, permission grants, exports, or operational behavior.
      </p>

      <div className="card-grid">
        <PlannerBlockPanel
          title="Recommendations summary"
          description="Existing backend recommendation-profile context, shown only with its trust envelope."
          envelope={recommendations?.trust_envelope}
        >
          <div className="metric-stack">
            <MetricRow
              label="Profile signal"
              value={recommendation?.recommended_profile?.replaceAll("_", " ") || "Not returned"}
            />
            <MetricRow label="Basis" value={recommendation?.basis || "Not recorded"} />
            <MetricRow label="Scope" value={recommendation?.scope_note || "Not recorded"} />
          </div>
        </PlannerBlockPanel>

        <PlannerBlockPanel
          title="Constraints summary"
          description="Rule-derived compatibility constraints and warnings."
          envelope={constraints?.trust_envelope}
        >
          {(constraints?.items || []).length ? (
            <ul>
              {constraints.items.slice(0, 4).map((item, index) => (
                <li key={`${item.issue}-${index}`}>
                  {item.severity || "severity not recorded"}: {item.issue}
                </li>
              ))}
            </ul>
          ) : (
            <p className="callout-copy">No constraints were returned for this design.</p>
          )}
          {(constraints?.items || []).length > 4 ? (
            <p className="callout-copy">{constraints.items.length - 4} additional constraints remain in the backend payload.</p>
          ) : null}
        </PlannerBlockPanel>

        <PlannerBlockPanel
          title="Readiness explanation"
          description="Completeness and missing-input state from the advisor summary."
          envelope={readiness?.trust_envelope}
        >
          <div className="metric-stack">
            <MetricRow label="Completeness" value={`${completeness.completeness_score ?? "N/A"}/100`} />
            <MetricRow label="Scope" value={completeness.scope_note || "Not recorded"} />
            <MetricRow label="Missing categories" value={formatInlineList(completeness.missing_categories)} />
          </div>
          {(completeness.recommended_next_steps || []).length ? (
            <details className="solution-list">
              <summary>View next steps</summary>
              <ul>
                {completeness.recommended_next_steps.map((step) => (
                  <li key={step}>{step}</li>
                ))}
              </ul>
            </details>
          ) : null}
        </PlannerBlockPanel>

        <PlannerBlockPanel
          title="Upgrade path explanation"
          description="Planning-state variant summary with readiness context."
          envelope={upgradePath?.trust_envelope}
        >
          <div className="metric-stack">
            <MetricRow label="Planning state" value={planningState?.summary || "Not returned"} />
            <MetricRow label="Design goal" value={planningState?.design_goal?.replaceAll("_", " ") || "Not recorded"} />
            <MetricRow
              label="Expansion basis"
              value={readinessContext.expansion_basis || "Not recorded"}
            />
          </div>
          {(planningState?.variants || []).length ? (
            <details className="solution-list">
              <summary>View planning variants</summary>
              <ul>
                {planningState.variants.map((variant) => (
                  <li key={variant.variant_key}>
                    {variant.label}: {formatStateLabel(variant.state_role)}; confidence {variant.confidence_level || "not recorded"}
                  </li>
                ))}
              </ul>
            </details>
          ) : null}
        </PlannerBlockPanel>

        {scenarioComparison ? (
          <PlannerBlockPanel
            title="Scenario comparison"
            description="Home-scoped comparison context if the backend returned one; not a homeowner ranking or choice."
            envelope={scenarioComparison.trust_envelope}
          >
            <div className="metric-stack">
              <MetricRow label="Status" value={comparison.status || "Not recorded"} />
              <MetricRow label="Scenario count" value={String(comparison.summary?.scenario_count ?? "N/A")} />
              <MetricRow label="Average completeness" value={String(comparison.summary?.average_completeness_score ?? "N/A")} />
            </div>
            {comparison.comparison_note ? <p className="callout-copy">{comparison.comparison_note}</p> : null}
            {(comparison.warnings || []).length ? (
              <details className="solution-list">
                <summary>View comparison warnings</summary>
                <ul>
                  {comparison.warnings.map((warning) => (
                    <li key={warning}>{warning}</li>
                  ))}
                </ul>
              </details>
            ) : null}
          </PlannerBlockPanel>
        ) : null}

        <PlannerBlockPanel
          title="Provenance and missing inputs"
          description="Aggregated source, rule, assumption, and missing-input metadata."
          envelope={provenance?.trust_envelope}
        >
          <div className="metric-stack">
            <MetricRow label="Source documents" value={String((provenance?.source_document_ids || []).length)} />
            <MetricRow label="Rule keys" value={formatInlineList(provenance?.rule_keys)} />
            <MetricRow label="Missing inputs" value={formatInlineList(provenance?.missing_inputs)} />
            <MetricRow label="Assumptions" value={formatInlineList(provenance?.assumptions)} />
          </div>
          {(provenance?.contributing || []).length ? (
            <details className="solution-list">
              <summary>View contributing source summaries</summary>
              <ul>
                {provenance.contributing.map((item) => (
                  <li key={`${item.entity_type}-${item.entity_id}`}>
                    {item.entity_type}:{item.entity_id} - source types {formatInlineList(item.source_types)};
                    trust {formatInlineList(item.trust_states)}
                  </li>
                ))}
              </ul>
            </details>
          ) : null}
        </PlannerBlockPanel>
      </div>
    </div>
  );
}

function VisualizationLegend({ items }) {
  return (
    <div className="workspace-legend">
      {items.map((item) => (
        <div key={item.label} className="workspace-legend-item">
          <Badge tone={item.tone}>{item.label}</Badge>
          <span>{item.note}</span>
        </div>
      ))}
    </div>
  );
}

function ArchitectureComponentCard({ component }) {
  return (
    <article key={component.component_key} className={`architecture-card state-${component.state}`}>
      <div className="architecture-card-header">
        <strong>{component.label}</strong>
        <Badge tone={getStateTone(component.state)}>{formatStateLabel(component.state)}</Badge>
      </div>
      <p>{component.relationship}</p>
      <small>{component.note}</small>
    </article>
  );
}

function ArchitectureMap({ architecture }) {
  const existingComponents = (architecture.architecture_components || []).filter(
    (component) => component.state === "existing"
  );
  const proposedComponents = (architecture.architecture_components || []).filter(
    (component) => component.state === "proposed" || component.state === "planning_assumption"
  );
  const unresolvedComponents = (architecture.architecture_components || []).filter(
    (component) => !["existing", "proposed", "planning_assumption"].includes(component.state)
  );

  return (
    <div className="architecture-map">
      <div className="architecture-column">
        <div className="architecture-column-header">
          <h4>Existing home architecture</h4>
          <p>Structured current-state signals that appear grounded in recorded equipment context.</p>
        </div>
        <div className="architecture-card-stack">
          {existingComponents.map((component) => (
            <ArchitectureComponentCard key={component.component_key} component={component} />
          ))}
        </div>
      </div>
      <div className="architecture-flow">
        <div className="architecture-flow-label">Current-state planning view</div>
        <div className="architecture-flow-step">
          <Badge tone="info">{architecture.solar_existing_state}</Badge>
          <strong>{architecture.inverter_topology}</strong>
          <span>{architecture.current_vs_proposed_architecture}</span>
        </div>
        <div className="architecture-flow-arrow">{"->"}</div>
        <div className="architecture-flow-step">
          <Badge tone="warning">planning implications</Badge>
          <strong>Battery, outage, expansion, and generator posture</strong>
          <span>{architecture.battery_retrofit_implication}</span>
        </div>
      </div>
      <div className="architecture-column">
        <div className="architecture-column-header">
          <h4>Proposed or planning-only path</h4>
          <p>Future-facing equipment and planning assumptions kept separate from current-state evidence.</p>
        </div>
        <div className="architecture-card-stack">
          {proposedComponents.map((component) => (
            <ArchitectureComponentCard key={component.component_key} component={component} />
          ))}
          {unresolvedComponents.map((component) => (
            <ArchitectureComponentCard key={component.component_key} component={component} />
          ))}
        </div>
      </div>
    </div>
  );
}

function CurrentArchitectureRelationshipGrid({ architecture }) {
  const componentByKey = new Map(
    (architecture.architecture_components || []).map((component) => [component.component_key, component])
  );
  const orderedKeys = [
    "solar_array",
    "inverter_topology",
    "main_service_panel",
    "backup_loads",
    "battery",
    "generator",
    "smart_panel",
    "service_upgrade_path",
  ];

  return (
    <div className="relationship-grid">
      {orderedKeys.map((key) => {
        const component = componentByKey.get(key);
        const label = component?.label || formatStateLabel(key);
        const note = component?.relationship || "Not yet recorded in the current architecture output.";
        const state = component?.state || "missing";

        return (
          <article key={key} className={`relationship-card state-${state}`}>
            <div className="relationship-card-header">
              <strong>{label}</strong>
              <Badge tone={getStateTone(state)}>{formatStateLabel(state)}</Badge>
            </div>
            <p>{note}</p>
            {component?.note ? <small>{component.note}</small> : <small>Missing inputs stay explicit.</small>}
          </article>
        );
      })}
    </div>
  );
}

function ReasoningGraphTrace({ graph }) {
  return (
    <div className="reasoning-trace">
      <div className="reasoning-node-rail">
        {(graph.nodes || []).map((node) => (
          <article key={node.node_id} className="reasoning-node-card">
            <div className="reasoning-node-header">
              <strong>{node.label}</strong>
              <Badge tone={getConfidenceTone(node.confidence_level)}>{node.confidence_level}</Badge>
            </div>
            <div className="trust-row">
              <Badge tone={getStateTone(node.status)}>{node.status.replaceAll("_", " ")}</Badge>
              <Badge>{node.category.replaceAll("_", " ")}</Badge>
            </div>
            <p>{node.summary}</p>
          </article>
        ))}
      </div>
      <div className="reasoning-dependency-grid">
        {(graph.dependencies || []).map((dependency) => (
          <article
            key={`${dependency.source_node_id}-${dependency.target_node_id}-${dependency.relationship}`}
            className="reasoning-edge-card"
          >
            <div className="reasoning-edge-header">
              <Badge tone={getDependencyTone(dependency.relationship)}>{dependency.relationship}</Badge>
              <Badge tone={getConfidenceTone(dependency.confidence_level)}>{dependency.confidence_level}</Badge>
            </div>
            <strong>{`${dependency.source_node_id} -> ${dependency.target_node_id}`}</strong>
            <p>{dependency.summary}</p>
          </article>
        ))}
      </div>
    </div>
  );
}

function CompactDependencyChain({ graph }) {
  return (
    <div className="dependency-chain">
      {(graph.dependencies || []).map((dependency) => (
        <article
          key={`${dependency.source_node_id}-${dependency.target_node_id}-${dependency.relationship}-compact`}
          className="dependency-chain-card"
        >
          <div className="dependency-chain-path">
            <strong>{dependency.source_node_id}</strong>
              <span aria-hidden="true">{"->"}</span>
            <strong>{dependency.target_node_id}</strong>
          </div>
          <div className="trust-row">
            <Badge tone={getDependencyTone(dependency.relationship)}>{dependency.relationship}</Badge>
            <Badge tone={getConfidenceTone(dependency.confidence_level)}>{dependency.confidence_level}</Badge>
          </div>
          <p>{dependency.summary}</p>
        </article>
      ))}
    </div>
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

function PlanningStateSnapshotPanel({ planningState }) {
  if (!planningState) {
    return null;
  }

  return (
    <article className="panel">
      <div className="panel-header">
        <div>
          <h3>Planning State Snapshot</h3>
          <p className="callout-copy">{planningState.summary}</p>
        </div>
        <div className="badge-row">
          <Badge tone="info">{planningState.snapshot_kind.replaceAll("_", " ")}</Badge>
          <Badge tone="warning">{planningState.version_label}</Badge>
          <TrustBadge state="derived_estimate" label="Snapshot framing only" />
        </div>
      </div>
      <div className="comparison-context-grid">
        <div className="comparison-context-card">
          <span>Snapshot label</span>
          <strong>{planningState.snapshot_label}</strong>
          <small>{planningState.snapshot_id}</small>
        </div>
        <div className="comparison-context-card">
          <span>Linked design</span>
          <strong>{planningState.design_name}</strong>
          <small>{planningState.design_id}</small>
        </div>
        <div className="comparison-context-card">
          <span>Design goal</span>
          <strong>{planningState.design_goal.replaceAll("_", " ")}</strong>
          <small>{planningState.design_status.replaceAll("_", " ")}</small>
        </div>
        <div className="comparison-context-card">
          <span>Saved scenario links</span>
          <strong>{planningState.scenario_count}</strong>
          <small>Persistent scenario records linked to this design state</small>
        </div>
      </div>
      <div className="snapshot-variant-grid">
        {(planningState.variants || []).map((variant) => (
          <article key={variant.variant_key} className="snapshot-variant-card">
            <div className="snapshot-variant-header">
              <strong>{variant.label}</strong>
              <Badge tone={getPlanningStateTone(variant.state_role)}>
                {variant.state_role.replaceAll("_", " ")}
              </Badge>
            </div>
            <div className="trust-row">
              {variant.profile ? <Badge tone="info">{variant.profile.replaceAll("_", " ")}</Badge> : null}
              <Badge tone={getConfidenceTone(variant.confidence_level)}>
                Confidence: {variant.confidence_level}
              </Badge>
              <TrustBadge state={variant.trust_state} />
            </div>
            <p>{variant.summary}</p>
            <small>{variant.note}</small>
          </article>
        ))}
      </div>
      {(planningState.linked_scenarios || []).length ? (
        <details className="solution-list">
          <summary>View saved scenario links</summary>
          <div className="scenario-link-grid">
            {planningState.linked_scenarios.map((scenario) => (
              <article key={scenario.scenario_id} className="scenario-link-card">
                <div className="scenario-link-header">
                  <strong>{scenario.scenario_name}</strong>
                  <Badge tone="info">{scenario.state_label}</Badge>
                </div>
                <p>{scenario.description}</p>
                <div className="trust-row">
                  <Badge>{scenario.updated_at_label}</Badge>
                  {scenario.latest_revision_label ? (
                    <Badge tone="warning">
                      {scenario.latest_revision_label}#{scenario.latest_revision_number}
                    </Badge>
                  ) : null}
                  <TrustBadge state={scenario.data_origin} />
                </div>
                <small>{scenario.note}</small>
              </article>
            ))}
          </div>
        </details>
      ) : (
        <p className="callout-copy">
          No saved scenario records are linked to this design yet. The advisor still treats the current design as a named planning snapshot.
        </p>
      )}
      <p className="callout-copy">{planningState.scope_note}</p>
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
      <VisualizationLegend
        items={[
          { label: "existing", tone: "success", note: "Known current-state equipment or posture" },
          { label: "proposed", tone: "warning", note: "Future equipment or planning path" },
          { label: "missing", tone: "danger", note: "Unknown or unresolved input" },
          { label: "planning assumption", tone: "warning", note: "Derived workspace posture, not installed equipment" },
        ]}
      />
      <ArchitectureMap architecture={architecture} />
      <div className="panel-subsection architecture-relationship-panel">
        <div className="panel-header">
          <h4>Architecture relationship map</h4>
          <Badge tone="info">Current state vs planning path</Badge>
        </div>
        <p className="callout-copy">
          This view keeps recorded equipment, proposed equipment, missing inputs, and planning assumptions in separate visual lanes so current topology does not blur into future recommendations.
        </p>
        <CurrentArchitectureRelationshipGrid architecture={architecture} />
      </div>
      <details className="solution-list">
        <summary>View architecture relationships</summary>
        <ul>
          {(architecture.architecture_components || []).map((component) => (
            <li key={component.component_key}>
              {component.label}: {formatStateLabel(component.state)}. {component.relationship} {component.note}
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
      <div className="panel-subsection reasoning-visual-panel">
        <div className="panel-header">
          <h4>Dependency chain overview</h4>
          <Badge tone="info">Inspectable reasoning flow</Badge>
        </div>
        <p className="callout-copy">
          Follow the compact chain first, then open the detailed node and evidence views if you need to inspect why a downstream planning posture appears.
        </p>
        <CompactDependencyChain graph={graph} />
      </div>
      <ReasoningGraphTrace graph={graph} />
      <details className="solution-list" open>
        <summary>View reasoning nodes</summary>
        <ul>
          {(graph.nodes || []).map((node) => (
            <li key={node.node_id}>
              {node.label}: {formatStateLabel(node.status)}. {node.summary}
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

function CurrentStateAnchorCard({ recommendation }) {
  const architecture = recommendation.current_home_energy_architecture;
  const backup = recommendation.backup_load_selection;
  const panel = recommendation.panel_service_architecture;
  const inverter = recommendation.inverter_system_architecture;

  return (
    <article className="comparison-anchor-card">
      <div className="panel-header">
        <div>
          <h3>Current state anchor</h3>
          <p className="callout-copy">
            Use this card as the fixed current-home context before reading alternate planning pathways.
          </p>
        </div>
        <div className="badge-row">
          <Badge tone="success">current state</Badge>
          <TrustBadge
            state={architecture?.inspectability?.trust_state || "derived_estimate"}
            label="Planning-only current-state model"
          />
        </div>
      </div>
      <div className="comparison-context-grid">
        <div className="comparison-context-card">
          <span>Current topology</span>
          <strong>{architecture?.inverter_topology || "Not recorded"}</strong>
          <small>{architecture?.solar_existing_state || "Solar state not recorded"}</small>
        </div>
        <div className="comparison-context-card">
          <span>Backup posture</span>
          <strong>{backup?.selected_scope_label || "Not recorded"}</strong>
          <small>{backup?.outage_posture || "Outage posture not recorded"}</small>
        </div>
        <div className="comparison-context-card">
          <span>Panel and service</span>
          <strong>{panel?.recommended_backup_architecture || "Not recorded"}</strong>
          <small>{panel?.panel_upgrade_likelihood || "Upgrade likelihood not recorded"}</small>
        </div>
        <div className="comparison-context-card">
          <span>Inverter pathway</span>
          <strong>{inverter?.recommended_system_architecture || "Not recorded"}</strong>
          <small>{inverter?.inverter_pathway_posture || "Pathway posture not recorded"}</small>
        </div>
      </div>
    </article>
  );
}

function PathwayComparisonCard({ profile, recommendation }) {
  const role = getPathwayRole(profile);
  const family = getProfileFamily(profile.profile);
  const backup = recommendation.backup_load_selection;
  const panel = recommendation.panel_service_architecture;
  const inverter = recommendation.inverter_system_architecture;
  const architecture = recommendation.current_home_energy_architecture;

  return (
    <article key={profile.profile} className="pathway-card">
      <div className="panel-header">
        <div>
          <h3>{profile.label}</h3>
          <p className="callout-copy">{profile.ui_description}</p>
        </div>
        <div className="badge-row">
          <Badge tone={role.tone}>{role.label}</Badge>
          <Badge tone={family.tone}>{family.label}</Badge>
          <Badge tone={getConfidenceTone(profile.inspectability?.confidence_level)}>
            Confidence: {profile.inspectability?.confidence_level || "unknown"}
          </Badge>
        </div>
      </div>
      <div className="pathway-chip-row">
        <Badge tone="info">{profile.profile.replaceAll("_", " ")}</Badge>
        <Badge>{profile.intent}</Badge>
        <TrustBadge state={profile.inspectability?.trust_state || "derived_estimate"} label="Interpretive comparison" />
      </div>
      <div className="comparison-context-grid">
        <div className="comparison-context-card">
          <span>Current-home compatibility</span>
          <strong>{profile.architecture_fit?.status || "Not recorded"}</strong>
          <small>{profile.architecture_fit?.summary || architecture?.current_vs_proposed_architecture || "No compatibility summary recorded"}</small>
        </div>
        <div className="comparison-context-card">
          <span>Backup-scope context</span>
          <strong>{backup?.selected_scope_label || "Not recorded"}</strong>
          <small>{profile.architecture_fit?.backup_path_summary || backup?.selection_reason || "Backup tradeoff not recorded"}</small>
        </div>
        <div className="comparison-context-card">
          <span>Inverter pathway</span>
          <strong>{inverter?.recommended_system_architecture || "Not recorded"}</strong>
          <small>{inverter?.inverter_pathway_posture || "No inverter posture recorded"}</small>
        </div>
        <div className="comparison-context-card">
          <span>Panel/service implication</span>
          <strong>{panel?.panel_upgrade_likelihood || "Not recorded"}</strong>
          <small>{panel?.main_service_panel_posture || "No panel posture recorded"}</small>
        </div>
      </div>
      <div className="pathway-compare-grid">
        <div className="comparison-key-card">
          <span>Battery posture</span>
          <strong>{profile.battery_sizing_posture.replaceAll("_", " ")}</strong>
        </div>
        <div className="comparison-key-card">
          <span>Solar posture</span>
          <strong>{profile.solar_sizing_posture.replaceAll("_", " ")}</strong>
        </div>
        <div className="comparison-key-card">
          <span>Growth margin</span>
          <strong>{profile.future_growth_margin_posture.replaceAll("_", " ")}</strong>
        </div>
        <div className="comparison-key-card">
          <span>Reserve posture</span>
          <strong>{profile.autonomy_reserve_posture.replaceAll("_", " ")}</strong>
        </div>
      </div>
      <div className="solution-list">
        <strong>Planning tradeoff snapshot</strong>
        <ul>
          <li>Reasoning focus: {profile.fit_reason}</li>
          <li>Expansion direction: {inverter?.expansion_path_posture || "Not recorded"}</li>
          <li>Battery retrofit implication: {architecture?.battery_retrofit_implication || "Not recorded"}</li>
          <li>Generator coexistence note: {architecture?.generator_coexistence_note || inverter?.generator_coexistence_assumption || "Not recorded"}</li>
        </ul>
      </div>
      {(profile.architecture_fit?.tradeoffs || []).length || (profile.architecture_fit?.warnings || []).length ? (
        <details className="solution-list">
          <summary>View pathway-specific tradeoffs</summary>
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
      <ConsistencyDetails title="View architecture consistency" consistency={panel?.architecture_consistency || inverter?.architecture_consistency} />
      <InspectabilityDetails
        label="View pathway evidence and missing inputs"
        inspectability={profile.inspectability}
        trustLabel="Comparison remains a planning interpretation"
      />
    </article>
  );
}

function PathwayComparisonWorkspace({ recommendation }) {
  const profiles = recommendation.profiles || [];

  return (
    <div className="comparison-workspace">
      <CurrentStateAnchorCard recommendation={recommendation} />
      <div className="panel-subsection">
        <div className="panel-header">
          <div>
            <h4>Planning pathway comparison</h4>
            <p className="callout-copy">
              Compare the same current-home context against multiple deterministic planning postures. This view explains tradeoffs; it does not introduce new recommendation logic.
            </p>
          </div>
          <div className="badge-row">
            <Badge tone="info">current vs proposed</Badge>
            <Badge tone="warning">tradeoffs at a glance</Badge>
          </div>
        </div>
        <div className="pathway-grid">
          {profiles.map((profile) => (
            <PathwayComparisonCard key={profile.profile} profile={profile} recommendation={recommendation} />
          ))}
        </div>
      </div>
    </div>
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
    </article>
  );
}

function RecommendationWorkspace({ recommendation, planningState }) {
  const recommendedProfile = (recommendation.profiles || []).find((profile) => profile.recommended);
  const alternateProfiles = (recommendation.profiles || []).filter((profile) => !profile.recommended);

  return (
    <article className="panel">
      <RecommendationSummaryPanel recommendation={recommendation} />
      <PlanningStateSnapshotPanel planningState={planningState} />

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
        description="Compare deterministic planning pathways against the same current-home architecture context before diving into the recommended path detail."
      >
        <PathwayComparisonWorkspace recommendation={recommendation} />
        {recommendedProfile ? <RecommendedProfilePanel profile={recommendedProfile} /> : null}
        {alternateProfiles.length ? (
          <details className="solution-list">
            <summary>View alternate profile labels</summary>
            <div className="card-grid">
              {alternateProfiles.map((profile) => (
                <ComparisonProfileCard key={profile.profile} profile={profile} />
              ))}
            </div>
          </details>
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

  const plannerIntelligenceQuery = useApiQuery(
    `planner-intelligence-${activeDesignId}`,
    () => api.getPlannerIntelligence(activeDesignId),
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
              <RecommendationWorkspace
                recommendation={advisorQuery.data.recommendation_profiles}
                planningState={advisorQuery.data.planning_state}
              />
            ) : null}
          </>
        ) : null}
      </PageSection>

      <PageSection
        title="Why / Sources"
        description="Planner-intelligence explanations stay read-only and source-linked; missing inputs and assumptions remain visible next to the claims they qualify."
      >
        {!activeDesignId ? <EmptyState label="Select a design to review planner intelligence sources." /> : null}
        {plannerIntelligenceQuery.loading ? <LoadingState label="Loading planner intelligence sources..." /> : null}
        {plannerIntelligenceQuery.error ? (
          <ErrorState error={plannerIntelligenceQuery.error} label="Unable to load planner intelligence sources." />
        ) : null}
        {!plannerIntelligenceQuery.loading && !plannerIntelligenceQuery.error && plannerIntelligenceQuery.data ? (
          <PlannerIntelligencePanel summary={plannerIntelligenceQuery.data} />
        ) : null}
        {!plannerIntelligenceQuery.loading && !plannerIntelligenceQuery.error && activeDesignId && !plannerIntelligenceQuery.data ? (
          <EmptyState label="No planner intelligence summary is available for this design yet." />
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
