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
  const scenarios = scenariosQuery.data || [];
  const designs = designsQuery.data || [];
  const home = homeQuery.data;

  return (
    <>
      <PageSection
        title="Scenario Comparison"
        description="Scenario comparison should help users evaluate tradeoffs, not just rankings."
      >
        {homeQuery.loading || scenariosQuery.loading || designsQuery.loading ? <LoadingState label="Loading scenarios..." /> : null}
        {homeQuery.error || scenariosQuery.error || designsQuery.error ? (
          <ErrorState error={homeQuery.error || scenariosQuery.error || designsQuery.error} label="Unable to load scenarios." />
        ) : null}
        {!homeQuery.loading && !scenariosQuery.loading && !designsQuery.loading && home ? (
          <div className="stack-grid">
            <ScenarioEditor homeId={home.id} designs={designs} onSaved={() => setRefreshKey((current) => current + 1)} isNew />
            {scenarios.map((scenario) => (
              <ScenarioEditor key={scenario.id} homeId={home.id} designs={designs} scenario={scenario} onSaved={() => setRefreshKey((current) => current + 1)} />
            ))}
          </div>
        ) : null}
        {!homeQuery.loading && !scenariosQuery.loading && !designsQuery.loading && !home ? (
          <EmptyState label="No home profile is available for scenarios yet." />
        ) : null}
      </PageSection>

      {!homeQuery.loading && !scenariosQuery.loading && !designsQuery.loading && scenarios.length ? (
        <PageSection
          title="Scenario Read View"
          description="The comparison summary remains visible while editable scenario records now sit above it."
        >
          <div className="page-section">
            {scenarios.map((scenario) => {
              const linkedDesign = designs.find((design) => design.id === scenario.linked_design_id);

              return (
                <article key={`summary-${scenario.id}`} className="panel scenario-panel">
                  <div className="panel-header">
                    <div>
                      <h3>{scenario.name}</h3>
                      <p>{scenario.description}</p>
                    </div>
                    <div className="badge-row">
                      <Badge tone="info">{linkedDesign?.design_goal || "Unknown goal"}</Badge>
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
                    <MetricRow
                      label="Upfront cost placeholder"
                      value={scenario.upfront_cost_placeholder != null ? `$${scenario.upfront_cost_placeholder.toLocaleString()}` : "Not set"}
                    />
                  </div>
                  <div className="score-grid">
                    <ScoreCard label="Expansion readiness" value={scenario.future_expansion_score ?? "N/A"} />
                    <ScoreCard label="Install complexity" value={scenario.install_complexity_score ?? "N/A"} />
                    <ScoreCard label="Backup capability" value={scenario.backup_capability_score ?? "N/A"} />
                  </div>
                </article>
              );
            })}
          </div>
        </PageSection>
      ) : null}
    </>
  );
}
