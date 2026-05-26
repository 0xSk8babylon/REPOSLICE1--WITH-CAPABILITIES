import { useEffect, useState } from "react";

import { EmptyState, ErrorState, LoadingState } from "../components/AsyncState";
import { Badge } from "../components/Badge";
import { MetricRow } from "../components/MetricRow";
import { PageSection } from "../components/PageSection";
import { ScoreCard } from "../components/ScoreCard";
import { TrustBadge } from "../components/TrustBadge";
import { FormActions } from "../components/form/FormActions";
import { FormStatus } from "../components/form/FormStatus";
import { NumberInput, SelectInput, TextAreaInput, TextInput } from "../components/form/Inputs";
import { api } from "../lib/api";
import { createId } from "../lib/ids";
import { getScenarioTrustStates } from "../lib/trust";
import { useApiMutation } from "../lib/useApiMutation";
import { useApiQuery } from "../lib/useApiQuery";

function buildScenarioState(homeId, linkedDesignId, scenario) {
  return {
    home_id: scenario?.home_id || homeId || "",
    name: scenario?.name || "",
    description: scenario?.description || "",
    linked_design_id: scenario?.linked_design_id || linkedDesignId || "",
    upfront_cost_placeholder: scenario?.upfront_cost_placeholder ?? "",
    future_expansion_score: scenario?.future_expansion_score ?? "",
    install_complexity_score: scenario?.install_complexity_score ?? "",
    backup_capability_score: scenario?.backup_capability_score ?? "",
    notes: scenario?.notes || "",
  };
}

function getRevisionIdentityLabel(scenario) {
  const revisionOverview = scenario?.revision_overview;
  if (!revisionOverview?.latest_revision_label) {
    return "No saved revision yet";
  }
  return `${revisionOverview.latest_revision_label} (#${revisionOverview.latest_revision_number})`;
}

function formatRevisionDate(value) {
  if (!value) {
    return "Timestamp not recorded";
  }
  return new Date(value).toLocaleString();
}

function getRevisionVariant(snapshot, variantKey) {
  return (snapshot?.variants || []).find((variant) => variant.variant_key === variantKey);
}

function formatConfidenceChange(previous, current) {
  if (!previous && !current) {
    return "Confidence not recorded";
  }
  if (previous === current) {
    return current ? `${current} confidence retained` : "Confidence unchanged";
  }
  return `${previous || "unknown"} -> ${current || "unknown"}`;
}

function buildRevisionComparison(revisions) {
  if (!revisions?.length || revisions.length < 2) {
    return null;
  }

  const latest = revisions[0];
  const previous = revisions[1];
  const latestSnapshot = latest.planning_state_snapshot || {};
  const previousSnapshot = previous.planning_state_snapshot || {};
  const latestCurrentState = getRevisionVariant(latestSnapshot, "current_state");
  const previousCurrentState = getRevisionVariant(previousSnapshot, "current_state");
  const latestProposed = getRevisionVariant(latestSnapshot, "proposed_pathway");
  const previousProposed = getRevisionVariant(previousSnapshot, "proposed_pathway");
  const latestFutureReady = getRevisionVariant(latestSnapshot, "future_ready_pathway");
  const previousFutureReady = getRevisionVariant(previousSnapshot, "future_ready_pathway");
  const latestConstrained = getRevisionVariant(latestSnapshot, "constrained_pathway");
  const previousConstrained = getRevisionVariant(previousSnapshot, "constrained_pathway");

  return {
    latest,
    previous,
    driftItems: [
      {
        label: "Linked design",
        previous: previous.linked_design_id,
        current: latest.linked_design_id,
      },
      {
        label: "Design goal",
        previous: previous.design_goal_snapshot?.replaceAll("_", " ") || "Not recorded",
        current: latest.design_goal_snapshot?.replaceAll("_", " ") || "Not recorded",
      },
      {
        label: "Design status",
        previous: previous.design_status_snapshot?.replaceAll("_", " ") || "Not recorded",
        current: latest.design_status_snapshot?.replaceAll("_", " ") || "Not recorded",
      },
      {
        label: "Recommended pathway",
        previous: previous.recommended_profile_snapshot?.replaceAll("_", " ") || "Not recorded",
        current: latest.recommended_profile_snapshot?.replaceAll("_", " ") || "Not recorded",
      },
      {
        label: "Current-state architecture",
        previous: previousCurrentState?.summary || "Not recorded",
        current: latestCurrentState?.summary || "Not recorded",
      },
      {
        label: "Proposed pathway confidence",
        previous: previousProposed?.confidence_level || "unknown",
        current: latestProposed?.confidence_level || "unknown",
        type: "confidence",
      },
      {
        label: "Future-ready pathway",
        previous: previousFutureReady?.profile?.replaceAll("_", " ") || "Not recorded",
        current: latestFutureReady?.profile?.replaceAll("_", " ") || "Not recorded",
      },
      {
        label: "Constrained pathway",
        previous: previousConstrained?.profile?.replaceAll("_", " ") || "Not recorded",
        current: latestConstrained?.profile?.replaceAll("_", " ") || "Not recorded",
      },
    ],
    scopeNote:
      "Historical revision comparison is interpretive and uses stored planning-state framing from saved revisions. It does not replay advisor logic against the older revision.",
  };
}

function RevisionComparisonCard({ scenario }) {
  const comparison = buildRevisionComparison(scenario?.revisions);

  if (!comparison) {
    return (
      <article className="panel revision-comparison-card">
        <div className="panel-header">
          <div>
            <h3>{scenario.name}</h3>
            <p>Historical comparison becomes available after a second saved revision exists.</p>
          </div>
          <div className="badge-row">
            <Badge tone="warning">single revision</Badge>
            <TrustBadge state="derived_estimate" label="Planning-only revision framing" />
          </div>
        </div>
      </article>
    );
  }

  return (
    <article className="panel revision-comparison-card">
      <div className="panel-header">
        <div>
          <h3>{scenario.name}</h3>
          <p>
            Compare saved planning-state drift between {comparison.previous.revision_label} and {comparison.latest.revision_label}.
          </p>
        </div>
        <div className="badge-row">
          <Badge tone="warning">{comparison.latest.revision_label}</Badge>
          <Badge tone="info">{comparison.previous.revision_label}</Badge>
          <TrustBadge state="derived_estimate" label="Stored revision comparison" />
        </div>
      </div>
      <div className="revision-pair-grid">
        <div className="revision-pair-card">
          <span>Previous saved state</span>
          <strong>{comparison.previous.revision_label}</strong>
          <small>{formatRevisionDate(comparison.previous.created_at)}</small>
        </div>
        <div className="revision-pair-card">
          <span>Latest saved state</span>
          <strong>{comparison.latest.revision_label}</strong>
          <small>{formatRevisionDate(comparison.latest.created_at)}</small>
        </div>
      </div>
      <div className="revision-drift-grid">
        {comparison.driftItems.map((item) => {
          const changed = item.previous !== item.current;
          const driftValue =
            item.type === "confidence"
              ? formatConfidenceChange(item.previous, item.current)
              : changed
                ? `${item.previous} -> ${item.current}`
                : `${item.current}`;

          return (
            <article key={item.label} className="revision-drift-card">
              <div className="revision-drift-header">
                <strong>{item.label}</strong>
                <Badge tone={changed ? "warning" : "success"}>
                  {changed ? "drift detected" : "stable"}
                </Badge>
              </div>
              <p>{driftValue}</p>
            </article>
          );
        })}
      </div>
      <details className="solution-list">
        <summary>View stored revision summaries</summary>
        <ul>
          <li>{comparison.previous.revision_label}: {comparison.previous.planning_summary}</li>
          <li>{comparison.latest.revision_label}: {comparison.latest.planning_summary}</li>
        </ul>
      </details>
      <p className="callout-copy">{comparison.scopeNote}</p>
    </article>
  );
}

function ScenarioEditor({ homeId, designs, scenario, onSaved, isNew = false }) {
  const defaultDesignId = designs[0]?.id || "";
  const [formState, setFormState] = useState(buildScenarioState(homeId, defaultDesignId, scenario));
  const mutation = useApiMutation();

  useEffect(() => {
    setFormState(buildScenarioState(homeId, defaultDesignId, scenario));
  }, [homeId, defaultDesignId, scenario]);

  async function handleSubmit(event) {
    event.preventDefault();
    const payload = {
      ...(isNew ? { id: createId("scenario") } : {}),
      ...formState,
      upfront_cost_placeholder: formState.upfront_cost_placeholder === "" ? null : Number(formState.upfront_cost_placeholder),
      future_expansion_score: formState.future_expansion_score === "" ? null : Number(formState.future_expansion_score),
      install_complexity_score: formState.install_complexity_score === "" ? null : Number(formState.install_complexity_score),
      backup_capability_score: formState.backup_capability_score === "" ? null : Number(formState.backup_capability_score),
    };

    await mutation.run(() =>
      isNew ? api.createScenario(payload) : api.updateScenario(scenario.id, payload)
    );
    onSaved();
    if (isNew) {
      setFormState(buildScenarioState(homeId, defaultDesignId, null));
    }
  }

  const linkedDesign = designs.find((design) => design.id === formState.linked_design_id);

  return (
    <form className="panel form-panel scenario-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <div>
          <h3>{isNew ? "Create Scenario" : formState.name || "Edit Scenario"}</h3>
          {!isNew && linkedDesign ? <p>{linkedDesign.name}</p> : null}
        </div>
        {!isNew ? (
          <div className="trust-row">
            {getScenarioTrustStates(scenario).map((state) => (
              <TrustBadge
                key={`${scenario.id}-${state}`}
                state={state}
                label={state === "placeholder" ? "Placeholder scoring" : undefined}
              />
            ))}
            {scenario?.data_origin === "user_created" && scenario?.upfront_cost_placeholder != null ? (
              <TrustBadge state="user_created" label="User-entered estimate" />
            ) : null}
            {scenario?.revision_overview?.latest_revision_label ? (
              <Badge tone="warning">{getRevisionIdentityLabel(scenario)}</Badge>
            ) : null}
          </div>
        ) : null}
      </div>
      <div className="form-grid">
        <TextInput label="Scenario name" value={formState.name} onChange={(event) => setFormState((current) => ({ ...current, name: event.target.value }))} />
        <SelectInput label="Linked design" value={formState.linked_design_id} onChange={(event) => setFormState((current) => ({ ...current, linked_design_id: event.target.value }))} options={designs.map((design) => ({ value: design.id, label: design.name }))} />
        <NumberInput label="Upfront cost placeholder" value={formState.upfront_cost_placeholder} onChange={(event) => setFormState((current) => ({ ...current, upfront_cost_placeholder: event.target.value }))} min="0" />
        <NumberInput label="Future expansion score" value={formState.future_expansion_score} onChange={(event) => setFormState((current) => ({ ...current, future_expansion_score: event.target.value }))} min="0" />
        <NumberInput label="Install complexity score" value={formState.install_complexity_score} onChange={(event) => setFormState((current) => ({ ...current, install_complexity_score: event.target.value }))} min="0" />
        <NumberInput label="Backup capability score" value={formState.backup_capability_score} onChange={(event) => setFormState((current) => ({ ...current, backup_capability_score: event.target.value }))} min="0" />
      </div>
      <TextAreaInput label="Description" value={formState.description} onChange={(event) => setFormState((current) => ({ ...current, description: event.target.value }))} />
      <TextAreaInput label="Notes" value={formState.notes} onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))} />
      {!isNew ? (
        <div className="score-grid">
          <ScoreCard label="Expansion readiness" value={formState.future_expansion_score || "N/A"} />
          <ScoreCard label="Install complexity" value={formState.install_complexity_score || "N/A"} />
          <ScoreCard label="Backup capability" value={formState.backup_capability_score || "N/A"} />
        </div>
      ) : null}
      {!isNew ? (
        <details className="solution-list">
          <summary>View revision framing</summary>
          <div className="metric-stack">
            <MetricRow label="Revision count" value={scenario?.revision_overview?.revision_count ?? 0} />
            <MetricRow label="Latest revision" value={getRevisionIdentityLabel(scenario)} />
            <MetricRow label="Revision note" value={scenario?.revision_overview?.note || "No revision note yet"} />
          </div>
        </details>
      ) : null}
      <FormStatus saving={mutation.saving} error={mutation.error} />
      <FormActions saving={mutation.saving} onCancel={() => setFormState(buildScenarioState(homeId, defaultDesignId, scenario))} saveLabel={isNew ? "Create Scenario" : "Save Scenario"} />
    </form>
  );
}

export function ScenarioComparisonPage() {
  const [refreshKey, setRefreshKey] = useState(0);
  const homeQuery = useApiQuery(`scenario-home-${refreshKey}`, api.getHome);
  const scenariosQuery = useApiQuery(`scenarios-${refreshKey}`, api.getScenarios);
  const designsQuery = useApiQuery(`scenario-designs-${refreshKey}`, api.getDesigns);
  const comparisonQuery = useApiQuery(`scenario-comparison-${refreshKey}`, api.compareScenarios);
  const scenarios = scenariosQuery.data || [];
  const designs = designsQuery.data || [];
  const home = homeQuery.data;
  const comparison = comparisonQuery.data;
  const comparisonScenarios = comparison?.scenarios || [];

  return (
    <>
      <PageSection
        title="Scenario Comparison"
        description="Scenario comparison should help users evaluate tradeoffs, not just rankings."
      >
        {homeQuery.loading || scenariosQuery.loading || designsQuery.loading || comparisonQuery.loading ? <LoadingState label="Loading scenarios..." /> : null}
        {homeQuery.error || scenariosQuery.error || designsQuery.error || comparisonQuery.error ? (
          <ErrorState error={homeQuery.error || scenariosQuery.error || designsQuery.error || comparisonQuery.error} label="Unable to load scenarios." />
        ) : null}
        {!homeQuery.loading && !scenariosQuery.loading && !designsQuery.loading && !comparisonQuery.loading && home ? (
          <div className="stack-grid">
            <ScenarioEditor homeId={home.id} designs={designs} onSaved={() => setRefreshKey((current) => current + 1)} isNew />
            {scenarios.map((scenario) => (
              <ScenarioEditor key={scenario.id} homeId={home.id} designs={designs} scenario={scenario} onSaved={() => setRefreshKey((current) => current + 1)} />
            ))}
          </div>
        ) : null}
        {!homeQuery.loading && !scenariosQuery.loading && !designsQuery.loading && !comparisonQuery.loading && !home ? (
          <EmptyState label="No home profile is available for scenarios yet." />
        ) : null}
      </PageSection>

      {!homeQuery.loading && !scenariosQuery.loading && !designsQuery.loading && !comparisonQuery.loading && comparison ? (
        <PageSection
          title="Comparison Summary"
          description={comparison.comparison_note}
        >
          <div className="page-section">
            <div className="score-grid">
              <ScoreCard label="Scenario count" value={comparison.summary?.scenario_count ?? 0} />
              <ScoreCard label="Avg. placeholder cost" value={comparison.summary?.average_upfront_cost_placeholder != null ? `$${comparison.summary.average_upfront_cost_placeholder.toLocaleString()}` : "N/A"} />
              <ScoreCard label="Avg. completeness" value={comparison.summary?.average_completeness_score ?? "N/A"} />
            </div>
            {comparison.warnings?.length ? (
              <article className="panel">
                <div className="panel-header">
                  <div>
                    <h3>Shared Warnings</h3>
                    <p>These conditions affect comparison confidence across one or more scenarios.</p>
                  </div>
                </div>
                <div className="metric-stack">
                  {comparison.warnings.map((warning) => (
                    <MetricRow key={warning} label="Warning" value={warning} />
                  ))}
                </div>
              </article>
            ) : null}
            <div className="stack-grid">
              {Object.entries(comparison.rankings || {}).map(([key, entries]) => (
                <article key={key} className="panel">
                  <div className="panel-header">
                    <div>
                      <h3>{key.replaceAll("_", " ")}</h3>
                      <p>Deterministic ordering from current planning records.</p>
                    </div>
                  </div>
                  <div className="metric-stack">
                    {entries.length ? (
                      entries.map((entry, index) => (
                        <MetricRow
                          key={`${key}-${entry.scenario_id}`}
                          label={`${index + 1}. ${entry.scenario_name}`}
                          value={entry.value}
                        />
                      ))
                    ) : (
                      <MetricRow label="Status" value="No comparable values yet" />
                    )}
                  </div>
                </article>
              ))}
            </div>
          </div>
        </PageSection>
      ) : null}

      {!homeQuery.loading && !scenariosQuery.loading && !designsQuery.loading && !comparisonQuery.loading && comparisonScenarios.length ? (
        <PageSection
          title="Historical Revision Comparison"
          description="Saved revision drift stays separate from the live scenario editor so historical comparison remains inspectable without overwhelming the primary workflow."
        >
          <div className="page-section">
            {comparisonScenarios.map((scenario) => (
              <RevisionComparisonCard key={`revision-compare-${scenario.id}`} scenario={scenario} />
            ))}
          </div>
        </PageSection>
      ) : null}

      {!homeQuery.loading && !scenariosQuery.loading && !designsQuery.loading && !comparisonQuery.loading && comparisonScenarios.length ? (
        <PageSection
          title="Scenario Read View"
          description="The comparison summary remains visible while editable scenario records now sit above it."
        >
          <div className="page-section">
            {comparisonScenarios.map((scenario) => {
              const linkedDesign = scenario.linked_design || designs.find((design) => design.id === scenario.linked_design_id);

              return (
                <article key={`summary-${scenario.id}`} className="panel scenario-panel">
                  <div className="panel-header">
                    <div>
                      <h3>{scenario.name}</h3>
                      <p>{scenario.description}</p>
                    </div>
                    <div className="badge-row">
                      <Badge tone="info">{linkedDesign?.design_goal || "Unknown goal"}</Badge>
                      {scenario.revision_overview?.latest_revision_label ? (
                        <Badge tone="warning">{getRevisionIdentityLabel(scenario)}</Badge>
                      ) : null}
                      {getScenarioTrustStates(scenario).map((state) => (
                        <TrustBadge
                          key={`summary-${scenario.id}-${state}`}
                          state={state}
                          label={state === "placeholder" ? "Placeholder scoring" : undefined}
                        />
                      ))}
                    </div>
                  </div>
                  <div className="metric-stack">
                    <MetricRow label="Linked design" value={linkedDesign?.name || scenario.linked_design_id} />
                    <MetricRow label="Design status" value={linkedDesign?.effective_status || linkedDesign?.status || "Unknown"} />
                    <MetricRow
                      label="Upfront cost placeholder"
                      value={scenario.upfront_cost_placeholder != null ? `$${scenario.upfront_cost_placeholder.toLocaleString()}` : "Not set"}
                    />
                    <MetricRow label="Planning completeness" value={scenario.design_completeness?.completeness_score ?? "N/A"} />
                    <MetricRow label="Linked pathways" value={scenario.comparison_summary?.pathway_count ?? 0} />
                    <MetricRow label="Low-confidence pathways" value={scenario.comparison_summary?.low_confidence_pathway_count ?? 0} />
                    <MetricRow label="Provenance documents" value={scenario.lineage_summary?.source_document_ids?.length ?? 0} />
                    <MetricRow label="Revision count" value={scenario.revision_overview?.revision_count ?? 0} />
                  </div>
                  <div className="score-grid">
                    <ScoreCard label="Expansion readiness" value={scenario.future_expansion_score ?? "N/A"} />
                    <ScoreCard label="Install complexity" value={scenario.install_complexity_score ?? "N/A"} />
                    <ScoreCard label="Backup capability" value={scenario.backup_capability_score ?? "N/A"} />
                  </div>
                  <div className="badge-row">
                    {(scenario.lineage_summary?.trust_states || []).map((state) => (
                      <TrustBadge key={`lineage-${scenario.id}-${state}`} state={state} />
                    ))}
                  </div>
                  <div className="metric-stack">
                    <MetricRow
                      label="Unverified fields"
                      value={scenario.lineage_summary?.unverified_fields?.length ? scenario.lineage_summary.unverified_fields.join(", ") : "None listed"}
                    />
                    <MetricRow
                      label="Rule lineage"
                      value={scenario.lineage_summary?.rule_keys?.length ? scenario.lineage_summary.rule_keys.join(", ") : "None linked"}
                    />
                    <MetricRow
                      label="Notes"
                      value={scenario.lineage_summary?.notes?.length ? scenario.lineage_summary.notes.join(" | ") : "No lineage notes yet"}
                    />
                  </div>
                  {scenario.revisions?.length ? (
                    <details className="solution-list">
                      <summary>View saved revisions</summary>
                      <div className="metric-stack">
                        {scenario.revisions.map((revision) => (
                          <MetricRow
                            key={revision.id}
                            label={`${revision.revision_label} (${revision.revision_status.replaceAll("_", " ")})`}
                            value={`${revision.created_at} | ${revision.recommended_profile_snapshot || "No profile snapshot"} | ${revision.design_status_snapshot || "No status snapshot"}`}
                          />
                        ))}
                      </div>
                    </details>
                  ) : null}
                  {scenario.warnings?.length ? (
                    <div className="metric-stack">
                      {scenario.warnings.map((warning) => (
                        <MetricRow key={`${scenario.id}-${warning}`} label="Warning" value={warning} />
                      ))}
                    </div>
                  ) : null}
                </article>
              );
            })}
          </div>
        </PageSection>
      ) : null}
    </>
  );
}
