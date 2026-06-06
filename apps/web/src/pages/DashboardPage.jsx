import { useState } from "react";

import { EmptyState, ErrorState, LoadingState } from "../components/AsyncState";
import { Badge } from "../components/Badge";
import { PageSection } from "../components/PageSection";
import { StatCard } from "../components/StatCard";
import { api } from "../lib/api";
import { useApiQuery } from "../lib/useApiQuery";

const TRUST_BOUNDARY_LABELS = [
  "Derived view",
  "Request-time planning signal",
  "Based on available inputs",
  "Needs confirmation",
  "Contractor review needed",
  "Not a final quote",
  "Not a final design",
  "Not a final estimate",
  "Not utility approval",
  "Not permit approval",
  "Not interconnection approval",
];

function formatLabel(value) {
  if (value === null || value === undefined || value === "") {
    return "Not available";
  }

  return String(value)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function statusTone(value) {
  const status = String(value || "").toLowerCase();
  if (status.includes("blocked") || status.includes("not_ready")) return "danger";
  if (status.includes("needs") || status.includes("review") || status.includes("partial")) return "warning";
  if (status.includes("ready") || status.includes("available") || status.includes("known")) return "success";
  return "info";
}

function normalizeListItem(item) {
  if (!item) return null;
  if (typeof item === "string" || typeof item === "number" || typeof item === "boolean") {
    return String(item);
  }
  if (item.gate_name) return `${item.gate_name}: ${formatLabel(item.status || "needs_confirmation")}`;
  if (item.category && item.status) return `${formatLabel(item.category)}: ${formatLabel(item.status)}`;
  if (item.contractor_program_review_prompt) return item.contractor_program_review_prompt;
  if (item.homeowner_explanation) return item.homeowner_explanation;
  if (item.contractor_notes) return item.contractor_notes;
  if (item.contractor_review_note) return item.contractor_review_note;
  if (item.summary) return item.summary;
  return "Additional review detail reported by backend.";
}

function asArray(value) {
  if (!value) return [];
  return Array.isArray(value) ? value : [value];
}

function firstItems(items = [], count = 3) {
  const sourceItems = asArray(items);
  return sourceItems.map(normalizeListItem).filter(Boolean).slice(0, count);
}

function homeDisplayLabel(home) {
  if (!home) return "No home context";
  return [home.name, home.city, home.state].filter(Boolean).join(" - ") || home.id || "Unnamed home";
}

function IntelligenceStateCard({ title, children, data, error, loading }) {
  if (loading) {
    return (
      <article className="panel intelligence-card">
        <h3>{title}</h3>
        <LoadingState label={`Loading ${title.toLowerCase()}...`} />
      </article>
    );
  }

  if (error) {
    return (
      <article className="panel intelligence-card">
        <h3>{title}</h3>
        <ErrorState error={error} label={`${title} unavailable.`} />
      </article>
    );
  }

  if (!data) {
    return (
      <article className="panel intelligence-card">
        <h3>{title}</h3>
        <EmptyState label="Missing endpoint data for this view." />
      </article>
    );
  }

  return <article className="panel intelligence-card">{children}</article>;
}

function SignalMetric({ label, value, detail }) {
  return (
    <div className="intelligence-metric">
      <span>{label}</span>
      <strong>{value}</strong>
      {detail ? <small>{detail}</small> : null}
    </div>
  );
}

function MiniList({ title, items, emptyLabel = "No items reported." }) {
  const visibleItems = firstItems(items);

  return (
    <div className="mini-list">
      <strong>{title}</strong>
      {visibleItems.length ? (
        <ul>
          {visibleItems.map((item, index) => (
            <li key={`${item}-${index}`}>{item}</li>
          ))}
        </ul>
      ) : (
        <small>{emptyLabel}</small>
      )}
    </div>
  );
}

function HomeContextSelector({ homes, selectedHome, onSelectHomeId }) {
  const homesForSelection = selectedHome && homes.length === 0 ? [selectedHome] : homes;
  const hasMultipleHomes = homesForSelection.length > 1;

  return (
    <article className="panel home-selector-panel">
      <div>
        <div className="panel-header">
          <h3>Home context selector</h3>
          <Badge tone="info">Read-only dashboard state</Badge>
        </div>
        <p className="home-selector-copy">
          Select which existing home anchors the planning intelligence cards. This only changes the displayed
          dashboard context and does not write, approve, or persist planning data.
        </p>
      </div>
      {hasMultipleHomes ? (
        <label className="field home-selector-control">
          <span>Dashboard home context</span>
          <select value={selectedHome?.id || ""} onChange={(event) => onSelectHomeId(event.target.value)}>
            {homesForSelection.map((home) => (
              <option key={home.id} value={home.id}>
                {homeDisplayLabel(home)}
              </option>
            ))}
          </select>
        </label>
      ) : (
        <div className="home-selector-meta">
          <span>Single home context</span>
          <strong>{homeDisplayLabel(selectedHome)}</strong>
        </div>
      )}
    </article>
  );
}

function ReviewChip({ label, value }) {
  return (
    <span className="review-chip">
      {label}: <strong>{value}</strong>
    </span>
  );
}

function ReviewDetailCard({ title, badge, tone = "info", summary, metrics = [], lists = [] }) {
  return (
    <div className="review-detail-card">
      <div className="review-detail-header">
        <strong>{title}</strong>
        {badge ? <Badge tone={tone}>{badge}</Badge> : null}
      </div>
      {summary ? <p>{summary}</p> : null}
      {metrics.length ? (
        <div className="review-chip-row">
          {metrics.map((metric) => (
            <ReviewChip key={metric.label} label={metric.label} value={metric.value} />
          ))}
        </div>
      ) : null}
      {lists.map((list) => (
        <MiniList
          key={list.title}
          title={list.title}
          items={list.items}
          emptyLabel={list.emptyLabel}
        />
      ))}
    </div>
  );
}

export function DashboardPage() {
  const [selectedHomeId, setSelectedHomeId] = useState("");
  const homeQuery = useApiQuery("home", api.getHome);
  const allHomesQuery = useApiQuery("homes-all", api.getAllHomes);
  const loadsQuery = useApiQuery("loads-summary", api.getLoadSummary);
  const designsQuery = useApiQuery("designs", api.getDesigns);
  const productsQuery = useApiQuery("products", api.getProductLibrary);
  const scenariosQuery = useApiQuery("scenarios", api.getScenarios);

  const allHomes = Array.isArray(allHomesQuery.data) ? allHomesQuery.data : [];
  const selectableHomes = allHomes.length ? allHomes : homeQuery.data ? [homeQuery.data] : [];
  const selectedHome =
    selectableHomes.find((home) => home?.id === selectedHomeId) || selectableHomes[0] || null;
  const activeHomeId = selectedHome?.id || null;

  const estimateReadinessQuery = useApiQuery(
    `estimate-readiness-${activeHomeId || "none"}`,
    () => api.getEstimateReadiness(activeHomeId),
    { enabled: Boolean(activeHomeId) },
  );
  const proposalOptionSetsQuery = useApiQuery(
    `proposal-option-sets-${activeHomeId || "none"}`,
    () => api.getProposalOptionSets(activeHomeId),
    { enabled: Boolean(activeHomeId) },
  );
  const energyPassportQuery = useApiQuery(
    `energy-passport-${activeHomeId || "none"}`,
    () => api.getEnergyPassport(activeHomeId),
    { enabled: Boolean(activeHomeId) },
  );
  const programIntelligenceQuery = useApiQuery(
    `program-intelligence-${activeHomeId || "none"}`,
    () => api.getProgramIntelligence(activeHomeId),
    { enabled: Boolean(activeHomeId) },
  );

  const isLoading =
    homeQuery.loading ||
    allHomesQuery.loading ||
    loadsQuery.loading ||
    designsQuery.loading ||
    productsQuery.loading ||
    scenariosQuery.loading;

  const homeContextError = allHomesQuery.error && !selectedHome;
  const error =
    homeContextError ||
    loadsQuery.error ||
    designsQuery.error ||
    productsQuery.error ||
    scenariosQuery.error;

  const loadSummary = loadsQuery.data;
  const designs = designsQuery.data || [];
  const products = productsQuery.data || [];
  const scenarios = scenariosQuery.data || [];
  const noHomes = !isLoading && !homeContextError && allHomes.length === 0 && !selectedHome;
  const noSelectedHome = !isLoading && !error && selectableHomes.length > 0 && !activeHomeId;

  const intelligenceQueries = [
    estimateReadinessQuery,
    proposalOptionSetsQuery,
    energyPassportQuery,
    programIntelligenceQuery,
  ];
  const intelligenceLoading = intelligenceQueries.some((query) => query.loading);
  const intelligenceErrors = intelligenceQueries.filter((query) => query.error);
  const intelligenceDataCount = intelligenceQueries.filter((query) => query.data).length;
  const intelligencePartial =
    Boolean(activeHomeId) &&
    !intelligenceLoading &&
    (intelligenceErrors.length > 0 || intelligenceDataCount < intelligenceQueries.length);

  const estimateReadiness = estimateReadinessQuery.data;
  const proposalOptionSets = proposalOptionSetsQuery.data;
  const energyPassport = energyPassportQuery.data;
  const programIntelligence = programIntelligenceQuery.data;
  const estimateSummary = estimateReadiness?.readiness_summary;
  const proposalSummary = proposalOptionSets?.summary;
  const programSummary = programIntelligence?.summary;
  const transferReadiness = energyPassport?.transfer_readiness;
  const openEstimateGates = asArray(estimateReadiness?.confirmation_gates).filter(
    (gate) => String(gate?.status || "").toLowerCase() !== "confirmed",
  );
  const estimateReviewNotes = [
    estimateReadiness?.contractor_summary,
    ...asArray(estimateReadiness?.blockers).map((blocker) => blocker?.contractor_notes),
  ];
  const proposalReviewNotes = [
    proposalOptionSets?.contractor_summary,
    ...asArray(proposalOptionSets?.option_candidates).flatMap((candidate) =>
      asArray(candidate?.contractor_review_notes),
    ),
  ];
  const programReviewPrompts = [
    ...asArray(programIntelligence?.interpretation?.contractor_program_review_prompts),
    ...asArray(programIntelligence?.interpretation?.verification_recommendations),
  ];
  const combinedMissingInputs = [
    ...asArray(estimateReadiness?.missing_inputs),
    ...asArray(proposalOptionSets?.missing_inputs),
    ...asArray(programIntelligence?.missing_inputs),
    ...asArray(transferReadiness?.missing_transfer_inputs),
  ];

  return (
    <>
      <PageSection
        title="Planning Frame"
        description="The dashboard should become the living summary of a home, the active designs, and the next decisions that matter."
      >
        {isLoading ? <LoadingState label="Loading dashboard summary..." /> : null}
        {error ? <ErrorState error={error} label="Unable to load dashboard summary." /> : null}
        {!isLoading && !error && selectedHome ? (
          <div className="stat-grid">
            <StatCard
              label="Homes in workspace"
              value={String(selectableHomes.length || 1)}
              detail={selectedHome.name}
            />
            <StatCard
              label="Structures modeled"
              value={String(selectedHome.buildings?.length || 0)}
              detail={`${selectedHome.panels?.length || 0} electrical panels tracked`}
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
        {noHomes ? <EmptyState label="No home model is available yet." /> : null}
      </PageSection>
      <PageSection
        title="What This App Is For"
        description="This product should preserve the house model and the reasoning around it so the homeowner and contractor can keep building on the same system understanding."
      >
        {isLoading ? null : !error && selectedHome ? (
          <div className="card-grid">
            <article className="panel">
              <div className="panel-header">
                <h3>Live property summary</h3>
                <Badge tone="info">Read-only prototype</Badge>
              </div>
              <p>{selectedHome.address_line_1}, {selectedHome.city}, {selectedHome.state}</p>
              <p>Utility: {selectedHome.utility_provider || "Placeholder"}</p>
              <p>Service size: {selectedHome.service_size ? `${selectedHome.service_size}A` : "Unknown"}</p>
            </article>
            <article className="panel">
              <h3>Workspace planning signals</h3>
              <p>Total running load: {loadSummary?.total_running_watts || 0} W</p>
              <p>Total surge load: {loadSummary?.total_surge_watts || 0} W</p>
              <p>Scenarios available: {scenarios.length}</p>
              <p>Home-specific planning intelligence appears in the selected-home view below.</p>
            </article>
          </div>
        ) : null}
        {!isLoading && !error && !selectedHome ? <EmptyState label="No home model available yet." /> : null}
      </PageSection>
      <PageSection
        title="Planning Intelligence"
        description="A read-only dashboard slice over backend planning intelligence. These are derived, request-time planning signals for review, not final decisions."
      >
        <div className="intelligence-boundary-strip">
          {TRUST_BOUNDARY_LABELS.map((label) => (
            <Badge key={label} tone="info">{label}</Badge>
          ))}
        </div>

        {isLoading ? <LoadingState label="Loading selected home context..." /> : null}
        {error ? <ErrorState error={error} label="Backend unavailable for dashboard context." /> : null}
        {noHomes ? <EmptyState label="No homes are available for planning intelligence yet." /> : null}
        {noSelectedHome ? <EmptyState label="No selected home context is available for this read-only view." /> : null}
        {!isLoading && !error && selectedHome ? (
          <HomeContextSelector
            homes={selectableHomes}
            selectedHome={selectedHome}
            onSelectHomeId={setSelectedHomeId}
          />
        ) : null}
        {intelligencePartial ? (
          <div className="state-card warning-panel">
            This view is based on available planning inputs. Some planning context is incomplete or unavailable, so
            additional contractor, customer, utility, or program confirmation may be needed.
          </div>
        ) : null}

        {activeHomeId ? (
          <div className="intelligence-grid">
            <article className="panel intelligence-card intelligence-card-context">
              <div className="panel-header">
                <h3>Home context</h3>
                <Badge tone="info">Based on available inputs</Badge>
              </div>
              <p>{selectedHome.name}</p>
              <div className="intelligence-metric-grid">
                <SignalMetric label="Home ID" value={selectedHome.id} detail="Source for home-anchored endpoints" />
                <SignalMetric
                  label="Utility context"
                  value={selectedHome.utility_provider || "Needs confirmation"}
                  detail="Not utility approval"
                />
                <SignalMetric
                  label="Service size"
                  value={selectedHome.service_size ? `${selectedHome.service_size}A` : "Missing input"}
                  detail="Not a final design"
                />
              </div>
            </article>

            <IntelligenceStateCard
              title="Estimate readiness"
              data={estimateReadiness}
              error={estimateReadinessQuery.error}
              loading={estimateReadinessQuery.loading}
            >
              <div className="panel-header">
                <h3>Estimate readiness</h3>
                <Badge tone={statusTone(estimateReadiness?.overall_status)}>
                  {formatLabel(estimateReadiness?.overall_status)}
                </Badge>
              </div>
              <p>{estimateReadiness?.homeowner_summary || "Estimate readiness is unavailable for this home."}</p>
              <div className="intelligence-metric-grid">
                <SignalMetric
                  label="Confidence"
                  value={formatLabel(estimateReadiness?.confidence_level)}
                  detail="Not a final estimate"
                />
                <SignalMetric
                  label="Open blockers"
                  value={String(estimateReadiness?.readiness_summary?.blocker_count ?? 0)}
                  detail={`${estimateReadiness?.readiness_summary?.pending_gate_count ?? 0} pending gates`}
                />
              </div>
              <MiniList title="Missing inputs" items={estimateReadiness?.missing_inputs} />
            </IntelligenceStateCard>

            <IntelligenceStateCard
              title="Proposal option sets"
              data={proposalOptionSets}
              error={proposalOptionSetsQuery.error}
              loading={proposalOptionSetsQuery.loading}
            >
              <div className="panel-header">
                <h3>Proposal option sets</h3>
                <Badge tone={statusTone(proposalOptionSets?.summary?.overall_status)}>
                  {formatLabel(proposalOptionSets?.summary?.overall_status)}
                </Badge>
              </div>
              <p>{proposalOptionSets?.homeowner_summary || "Proposal option readiness is unavailable for this home."}</p>
              <div className="intelligence-metric-grid">
                <SignalMetric
                  label="Option candidates"
                  value={String(proposalOptionSets?.summary?.option_candidate_count ?? 0)}
                  detail="Not a final proposal"
                />
                <SignalMetric
                  label="Review needed"
                  value={proposalOptionSets?.summary?.contractor_review_required ? "Yes" : "Not reported"}
                  detail="Contractor review needed"
                />
              </div>
              <MiniList title="Deferred boundaries" items={proposalOptionSets?.deferred_boundaries} />
            </IntelligenceStateCard>

            <IntelligenceStateCard
              title="Energy passport preview"
              data={energyPassport}
              error={energyPassportQuery.error}
              loading={energyPassportQuery.loading}
            >
              <div className="panel-header">
                <h3>Energy passport preview</h3>
                <Badge tone={statusTone(energyPassport?.summary?.overall_status)}>
                  {formatLabel(energyPassport?.summary?.overall_status)}
                </Badge>
              </div>
              <p>{energyPassport?.summary?.non_authoritative_summary || "Energy Passport context is unavailable."}</p>
              <div className="intelligence-metric-grid">
                <SignalMetric
                  label="Systems summarized"
                  value={String(energyPassport?.summary?.system_count ?? 0)}
                  detail="Derived view"
                />
                <SignalMetric
                  label="Transfer readiness"
                  value={formatLabel(energyPassport?.transfer_readiness?.readiness_level)}
                  detail="Not legal or financial advice"
                />
              </div>
              <MiniList title="Confirmation needed" items={energyPassport?.transfer_readiness?.confirmation_needed} />
            </IntelligenceStateCard>

            <IntelligenceStateCard
              title="Program / grid edge intelligence"
              data={programIntelligence}
              error={programIntelligenceQuery.error}
              loading={programIntelligenceQuery.loading}
            >
              <div className="panel-header">
                <h3>Program / grid edge intelligence</h3>
                <Badge tone={statusTone(programIntelligence?.summary?.overall_status)}>
                  {formatLabel(programIntelligence?.summary?.overall_status)}
                </Badge>
              </div>
              <p>
                {programIntelligence?.interpretation?.homeowner_safe_summary ||
                  "Program and grid edge intelligence is unavailable for this home."}
              </p>
              <div className="intelligence-metric-grid">
                <SignalMetric
                  label="Program signals"
                  value={String(programIntelligence?.summary?.program_awareness_count ?? 0)}
                  detail="Not utility approval"
                />
                <SignalMetric
                  label="Grid-edge signals"
                  value={String(programIntelligence?.summary?.grid_edge_readiness_count ?? 0)}
                  detail="Not interconnection approval"
                />
              </div>
              <MiniList title="Program verification needed" items={programIntelligence?.confirmation_gates} />
            </IntelligenceStateCard>

            <article className="panel intelligence-card intelligence-card-wide">
              <div className="panel-header">
                <h3>Contractor review summary</h3>
                <Badge tone="warning">Needs confirmation</Badge>
              </div>
              <div className="contractor-review-intro">
                <p>
                  This read-only dashboard organizes backend planning signals for contractor review. It does not
                  approve scope, pricing, design, utility participation, permits, or interconnection.
                </p>
                <div className="review-chip-row">
                  <ReviewChip label="View" value="Derived" />
                  <ReviewChip label="Authority" value="Non-final" />
                  <ReviewChip label="Action" value="Contractor review needed" />
                </div>
              </div>
              <div className="contractor-review-grid">
                <ReviewDetailCard
                  title="Estimate gates"
                  badge={formatLabel(estimateReadiness?.overall_status)}
                  tone={statusTone(estimateReadiness?.overall_status)}
                  summary={estimateReadiness?.contractor_summary}
                  metrics={[
                    { label: "Open blockers", value: String(estimateSummary?.blocker_count ?? 0) },
                    { label: "Pending gates", value: String(estimateSummary?.pending_gate_count ?? 0) },
                    { label: "Missing inputs", value: String(estimateSummary?.missing_input_count ?? 0) },
                  ]}
                  lists={[
                    {
                      title: "Open confirmation gates",
                      items: openEstimateGates,
                      emptyLabel: "No open estimate gates reported.",
                    },
                    {
                      title: "Estimate review notes",
                      items: estimateReviewNotes,
                      emptyLabel: "No estimate review notes reported.",
                    },
                  ]}
                />
                <ReviewDetailCard
                  title="Proposal option review"
                  badge={formatLabel(proposalSummary?.overall_status)}
                  tone={statusTone(proposalSummary?.overall_status)}
                  summary={proposalOptionSets?.contractor_summary}
                  metrics={[
                    { label: "Candidates", value: String(proposalSummary?.option_candidate_count ?? 0) },
                    { label: "Review needed", value: String(proposalSummary?.candidates_requiring_review_count ?? 0) },
                    { label: "Open gates", value: String(proposalSummary?.confirmation_gate_count ?? 0) },
                  ]}
                  lists={[
                    {
                      title: "Proposal review notes",
                      items: proposalReviewNotes,
                      emptyLabel: "No proposal review notes reported.",
                    },
                    {
                      title: "Proposal blockers",
                      items: proposalOptionSets?.blockers,
                      emptyLabel: "No proposal blockers reported.",
                    },
                  ]}
                />
                <ReviewDetailCard
                  title="Program and install review prompts"
                  badge={formatLabel(programSummary?.overall_status)}
                  tone={statusTone(programSummary?.overall_status)}
                  summary={programIntelligence?.interpretation?.homeowner_safe_summary}
                  metrics={[
                    { label: "Program signals", value: String(programSummary?.program_awareness_count ?? 0) },
                    { label: "Grid signals", value: String(programSummary?.grid_edge_readiness_count ?? 0) },
                    { label: "Verification gates", value: String(programSummary?.confirmation_gate_count ?? 0) },
                  ]}
                  lists={[
                    {
                      title: "Contractor prompts",
                      items: programReviewPrompts,
                      emptyLabel: "No program review prompts reported.",
                    },
                    {
                      title: "Missing input watchlist",
                      items: combinedMissingInputs,
                      emptyLabel: "No missing inputs reported across loaded dashboard endpoints.",
                    },
                  ]}
                />
              </div>
            </article>
          </div>
        ) : null}
      </PageSection>
    </>
  );
}
