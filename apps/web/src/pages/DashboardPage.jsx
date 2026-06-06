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
  if (item.homeowner_explanation) return item.homeowner_explanation;
  if (item.contractor_notes) return item.contractor_notes;
  if (item.contractor_review_note) return item.contractor_review_note;
  if (item.summary) return item.summary;
  return "Additional review detail reported by backend.";
}

function firstItems(items = [], count = 3) {
  const sourceItems = Array.isArray(items) ? items : [items];
  return sourceItems.map(normalizeListItem).filter(Boolean).slice(0, count);
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

export function DashboardPage() {
  const homeQuery = useApiQuery("home", api.getHome);
  const allHomesQuery = useApiQuery("homes-all", api.getAllHomes);
  const loadsQuery = useApiQuery("loads-summary", api.getLoadSummary);
  const designsQuery = useApiQuery("designs", api.getDesigns);
  const productsQuery = useApiQuery("products", api.getProductLibrary);
  const scenariosQuery = useApiQuery("scenarios", api.getScenarios);

  const allHomes = Array.isArray(allHomesQuery.data) ? allHomesQuery.data : [];
  const selectedHome = allHomes[0] || homeQuery.data || null;
  const selectedHomeId = selectedHome?.id || null;

  const estimateReadinessQuery = useApiQuery(
    `estimate-readiness-${selectedHomeId || "none"}`,
    () => api.getEstimateReadiness(selectedHomeId),
    { enabled: Boolean(selectedHomeId) },
  );
  const proposalOptionSetsQuery = useApiQuery(
    `proposal-option-sets-${selectedHomeId || "none"}`,
    () => api.getProposalOptionSets(selectedHomeId),
    { enabled: Boolean(selectedHomeId) },
  );
  const energyPassportQuery = useApiQuery(
    `energy-passport-${selectedHomeId || "none"}`,
    () => api.getEnergyPassport(selectedHomeId),
    { enabled: Boolean(selectedHomeId) },
  );
  const programIntelligenceQuery = useApiQuery(
    `program-intelligence-${selectedHomeId || "none"}`,
    () => api.getProgramIntelligence(selectedHomeId),
    { enabled: Boolean(selectedHomeId) },
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
  const noSelectedHome = !isLoading && !error && allHomes.length > 0 && !selectedHomeId;

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
    Boolean(selectedHomeId) &&
    !intelligenceLoading &&
    (intelligenceErrors.length > 0 || intelligenceDataCount < intelligenceQueries.length);

  const estimateReadiness = estimateReadinessQuery.data;
  const proposalOptionSets = proposalOptionSetsQuery.data;
  const energyPassport = energyPassportQuery.data;
  const programIntelligence = programIntelligenceQuery.data;

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
            <StatCard label="Homes in workspace" value={String(allHomes.length || 1)} detail={selectedHome.name} />
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
              <h3>Current planning signals</h3>
              <p>Total running load: {loadSummary?.total_running_watts || 0} W</p>
              <p>Total surge load: {loadSummary?.total_surge_watts || 0} W</p>
              <p>Scenarios available: {scenarios.length}</p>
            </article>
          </div>
        ) : null}
        {!isLoading && !error && !selectedHome ? <EmptyState label="No home model available yet." /> : null}
      </PageSection>
      <PageSection
        title="Planning Intelligence"
        description="A first read-only slice over backend planning intelligence. These are derived, request-time planning signals for review, not final decisions."
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
        {intelligencePartial ? (
          <div className="state-card warning-panel">
            This view is based on available planning inputs. Some planning context is incomplete or unavailable, so
            additional contractor, customer, utility, or program confirmation may be needed.
          </div>
        ) : null}

        {selectedHomeId ? (
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
              <p>
                This read-only dashboard organizes backend planning signals for review. It does not approve scope,
                pricing, design, utility participation, permits, or interconnection.
              </p>
              <div className="contractor-review-grid">
                <MiniList
                  title="Estimate review"
                  items={[
                    estimateReadiness?.contractor_summary,
                    ...(estimateReadiness?.blockers || []).map((blocker) => blocker.contractor_notes),
                  ]}
                  emptyLabel="No estimate review notes reported."
                />
                <MiniList
                  title="Proposal review"
                  items={[
                    proposalOptionSets?.contractor_summary,
                    ...(proposalOptionSets?.option_candidates || []).flatMap(
                      (candidate) => candidate.contractor_review_notes || [],
                    ),
                  ]}
                  emptyLabel="No proposal review notes reported."
                />
                <MiniList
                  title="Program review"
                  items={programIntelligence?.interpretation?.contractor_program_review_prompts}
                  emptyLabel="No program review prompts reported."
                />
              </div>
            </article>
          </div>
        ) : null}
      </PageSection>
    </>
  );
}
