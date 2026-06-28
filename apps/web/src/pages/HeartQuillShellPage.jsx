import { useMemo, useState } from "react";
import { Link, NavLink } from "react-router-dom";

import { api } from "../lib/api";
import {
  builderReadiness,
  capabilities,
  catalogItems,
  comparisonRows,
  draftTemplates,
  fallbackTemplateOverlay,
  goals,
  homeFacts as staticHomeFacts,
  homeRecord as staticHomeRecord,
  learnTopics,
  liveTemplateFallback,
  sandboxDrafts,
  templateOverlays,
  twinEdges,
  twinNodes,
  upgradePath,
} from "../lib/heartQuillMockData";
import { useApiQuery } from "../lib/useApiQuery";

const navItems = [
  { to: "/", label: "Home", sub: "Energy Twin" },
  { to: "/explore", label: "Explore", sub: "Goals + Learn" },
  { to: "/planner", label: "Planner", sub: "Templates + Drafts" },
  { to: "/builder", label: "Builder", sub: "Build readiness" },
];

const iconPaths = {
  home: <path d="M4 11l8-6 8 6M6 10v9h12v-9M10 19v-5h4v5" />,
  search: <path d="M10.8 17.6a6.8 6.8 0 1 1 0-13.6 6.8 6.8 0 0 1 0 13.6ZM16 16l4 4" />,
  layers: <path d="M12 3l8 4.5-8 4.5-8-4.5ZM4 12l8 4.5 8-4.5M4 16.5 12 21l8-4.5" />,
  builder: <path d="M4 20h16M6 20V8l6-4 6 4v12M9 20v-6h6v6" />,
  spark: <path d="M13 3 8 13h4l-1 8 5-11h-4l1-7Z" />,
  shield: <path d="M12 3 20 7v5c0 4.5-3.2 7.5-8 9-4.8-1.5-8-4.5-8-9V7l8-4Z" />,
  check: <path d="m5 12.5 4.2 4.2L19 7" />,
  plus: <path d="M12 5v14M5 12h14" />,
  arrow: <path d="M5 12h14m-6-6 6 6-6 6" />,
  grid: <path d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z" />,
};

function formatLabel(value) {
  if (value === null || value === undefined || value === "") return "Not available";
  return String(value).replaceAll("_", " ");
}

function formatHomeAddress(home) {
  if (!home) return staticHomeRecord.address;
  return [home.address_line_1, home.city, home.state].filter(Boolean).join(", ") || staticHomeRecord.address;
}

function getHomeRecord(home) {
  if (!home) return staticHomeRecord;
  return {
    name: home.name || staticHomeRecord.name,
    address: formatHomeAddress(home),
    service: home.service_size ? `${home.service_size}A service` : "Service size not recorded",
    utility: home.utility_provider || "Utility context not recorded",
    status: "Read-only planning record",
    provenance: `Backend ${formatLabel(home.data_origin)}`,
  };
}

function isNoHomeError(error) {
  return error?.message?.startsWith("404");
}

function getFactSummary(facts = []) {
  return {
    total: facts.length,
    known: facts.filter((fact) => fact.effective_confidence_tier === "known").length,
    needs: facts.filter((fact) => ["assumed", "stale"].includes(fact.effective_confidence_tier)).length,
    missing: facts.filter((fact) => fact.effective_confidence_tier === "missing").length,
  };
}

function formatFactValue(fact) {
  const value = Array.isArray(fact.value) ? fact.value.join(", ") : fact.value;
  return `${formatLabel(value)}${fact.unit ? ` ${fact.unit}` : ""}`;
}

function getFactRows(facts = []) {
  if (!facts.length) {
    return staticHomeFacts.map(([label, value]) => ({
      label,
      value,
      basis: "Static shell placeholder",
    }));
  }

  return facts.slice(0, 6).map((fact) => ({
    label: formatLabel(fact.key),
    value: formatFactValue(fact),
    basis: `${formatLabel(fact.source)} / ${formatLabel(fact.effective_confidence_tier)}`,
  }));
}

function getNecSummary(loadCalculation) {
  const result = loadCalculation?.results?.[0];
  if (!result) {
    return {
      amps: "Gap",
      posture: "No load calculation read",
      missing: "Not read",
      confidence: "not assessed",
      boundary: "Professional review boundary remains active",
    };
  }

  return {
    amps: result.calculated_service_load_amps ? `${Math.round(result.calculated_service_load_amps)}A` : "Gap",
    posture: result.calculation_ready ? "Planning calculation available" : "Needs facts",
    missing: loadCalculation.missing_data?.length || result.gaps?.length || 0,
    confidence: formatLabel(result.output_confidence_tier),
    boundary: loadCalculation.compliance_boundary || "Professional review boundary remains active",
  };
}

function toTemplateCard(template) {
  if (!template.template_id) return template;

  const requiredInputCount = (template.draft_input_definitions || []).filter((input) => input.required).length;
  return {
    id: template.template_id,
    architecture: formatLabel(template.authority_layer || "advisory"),
    intent: template.name,
    backup: `${requiredInputCount} required inputs`,
    cost: Math.min(4, Math.max(1, requiredInputCount || 1)),
    complexity: Math.min(4, Math.max(1, template.steps?.length || 1)),
    blurb: template.summary,
    basis: template.non_authoritative_note,
    isDraft: false,
    source: "backend",
  };
}

function ApiStatus({ query, label, fallbackLabel = "Static placeholders remain visible" }) {
  if (query.loading) {
    return <Badge tone="info">Reading {label}</Badge>;
  }
  if (query.error) {
    return <Badge tone="warn">{fallbackLabel}</Badge>;
  }
  if (query.data) {
    return <Badge tone="info">Backend read-only</Badge>;
  }
  return <Badge tone="warn">{fallbackLabel}</Badge>;
}

function Icon({ name, size = 18 }) {
  return (
    <svg className="hq-icon" width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <g stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
        {iconPaths[name] || iconPaths.spark}
      </g>
    </svg>
  );
}

function Badge({ children, tone = "info" }) {
  return <span className={`hq-badge hq-badge-${tone}`}>{children}</span>;
}

function Pips({ value, max = 4 }) {
  return (
    <span className="hq-pips" aria-label={`${value} of ${max}`}>
      {Array.from({ length: max }).map((_, index) => (
        <span key={index} className={index < value ? "hq-pip hq-pip-on" : "hq-pip"} />
      ))}
    </span>
  );
}

function statusTone(status) {
  if (status === "known" || status === "ready") return "ok";
  if (status === "needs" || status === "draft") return "warn";
  if (status === "blocked") return "blocked";
  return "muted";
}

function nodeById(nodes) {
  return Object.fromEntries(nodes.map((node) => [node.id, node]));
}

function HomeDiagram({ selectedId, onSelect, overlay }) {
  const byId = useMemo(() => nodeById(twinNodes), []);
  const hub = twinNodes.find((node) => node.hub);

  return (
    <div className="hq-diagram" aria-label="Mock Energy Twin diagram">
      <svg className="hq-diagram-lines" viewBox="0 0 100 100" preserveAspectRatio="none">
        {twinEdges.map(([from, to]) => {
          const a = byId[from];
          const b = byId[to];
          if (!a || !b) return null;
          const active = selectedId === from || selectedId === to;
          return (
            <line
              key={`${from}-${to}`}
              x1={a.x}
              y1={a.y}
              x2={b.x}
              y2={b.y}
              className={active ? "hq-edge hq-edge-active" : "hq-edge"}
            />
          );
        })}
        {overlay && hub
          ? overlay.nodes.map((id) => {
              const target = byId[id];
              if (!target || target.id === hub.id) return null;
              return (
                <line
                  key={`overlay-${id}`}
                  x1={hub.x}
                  y1={hub.y}
                  x2={target.x}
                  y2={target.y}
                  className="hq-edge-overlay"
                  stroke={overlay.color}
                />
              );
            })
          : null}
      </svg>

      {twinNodes.map((node) => {
        const selected = selectedId === node.id;
        return (
          <button
            key={node.id}
            type="button"
            className={`hq-node hq-node-${statusTone(node.status)} ${node.hub ? "hq-node-hub" : ""} ${
              selected ? "hq-node-selected" : ""
            }`}
            style={{ left: `${node.x}%`, top: `${node.y}%` }}
            onClick={() => onSelect(node)}
          >
            <span className="hq-node-dot">{node.label.slice(0, 1)}</span>
            <span className="hq-node-label">{node.label}</span>
          </button>
        );
      })}
    </div>
  );
}

function ShellHeader() {
  return (
    <header className="hq-topbar">
      <Link className="hq-brand" to="/" aria-label="Residential Energy Planner home">
        <span className="hq-brand-mark">
          <Icon name="spark" size={17} />
        </span>
        <span>
          <strong>Residential Energy Planner</strong>
          <small>Object-view shell</small>
        </span>
      </Link>
      <nav className="hq-primary-nav" aria-label="Primary">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) => (isActive ? "hq-nav-item hq-nav-item-active" : "hq-nav-item")}
          >
            <span>{item.label}</span>
            <small>{item.sub}</small>
          </NavLink>
        ))}
      </nav>
      <div className="hq-shell-meta">
        <Badge tone="info">Read-only shell</Badge>
      </div>
    </header>
  );
}

export function HeartQuillAppShell({ children }) {
  return (
    <div className="hq-app">
      <ShellHeader />
      <main className="hq-stage">{children}</main>
    </div>
  );
}

function HomeOnboardingNotice() {
  // Additive (not substitutive): rendered alongside the full Home shell when no home
  // record exists yet (404 /api/homes). Empty Postgres is valid; this prompts the
  // homeowner to record an address without seeding data or hiding the shell.
  return (
    <section className="hq-panel hq-onboarding-notice" aria-label="Record a home address">
      <div className="hq-panel-head">
        <div>
          <p className="hq-eyebrow">Start here</p>
          <h2>No home record yet</h2>
        </div>
        <Badge tone="warn">Needs address</Badge>
      </div>
      <p>
        No account-scoped home record is available, so the Energy Twin below shows static placeholders.
        Record a user-entered address to create the Energy Twin foundation — without geocoding, property
        enrichment, or utility inference. Calculations and backend data stay unavailable until a home exists.
      </p>
      <div className="hq-actions">
        <Link className="hq-btn hq-btn-primary" to="/onboarding/address">
          Record address <Icon name="arrow" size={15} />
        </Link>
      </div>
    </section>
  );
}

export function HomeShellPage() {
  const [selected, setSelected] = useState(twinNodes.find((node) => node.hub));
  const homeQuery = useApiQuery("hq-home", api.getHome);
  const homeLoadNoHome = isNoHomeError(homeQuery.error);
  const homeId = homeQuery.data?.id;
  const factsQuery = useApiQuery(`hq-facts:${homeId || "none"}`, () => api.getFacts(homeId), {
    enabled: Boolean(homeId),
  });
  const loadCalcQuery = useApiQuery(`hq-nec:${homeId || "none"}`, () => api.getNec220LoadCalculation(homeId), {
    enabled: Boolean(homeId),
  });
  const homeRecord = getHomeRecord(homeQuery.data);
  const factSummary = getFactSummary(factsQuery.data || []);
  const factRows = getFactRows(factsQuery.data || []);
  const necSummary = getNecSummary(loadCalcQuery.data);
  const knownCount = factsQuery.data?.length ? factSummary.known : twinNodes.filter((node) => node.status === "known").length;
  const needsCount = factsQuery.data?.length ? factSummary.needs : twinNodes.filter((node) => node.status === "needs").length;
  const missingCount = loadCalcQuery.data ? necSummary.missing : twinNodes.filter((node) => node.status === "missing").length;

  const showOnboarding = !homeQuery.loading && homeLoadNoHome;

  return (
    <div className="hq-page hq-home-page">
      {showOnboarding ? <HomeOnboardingNotice /> : null}
      <section className="hq-hero">
        <div className="hq-hero-copy">
          <p className="hq-eyebrow">Home</p>
          <h1>{showOnboarding ? "Your home will have an Energy Twin." : "Your home has an Energy Twin."}</h1>
          <p>
            Start from the durable record: known facts, current status, missing inputs, and the next
            homeowner-safe step. Backend reads are read-only; placeholder data stays labeled when a read is unavailable.
          </p>
          <div className="hq-actions">
            <Link className="hq-btn hq-btn-primary" to="/explore">
              Explore goals <Icon name="arrow" size={15} />
            </Link>
            <Link className="hq-btn hq-btn-secondary" to="/planner">
              Open Planner
            </Link>
          </div>
        </div>
        <section className="hq-panel hq-record-panel">
          <div className="hq-panel-head">
            <div>
              <p className="hq-eyebrow">Current status</p>
              <h2>{homeRecord.name}</h2>
            </div>
            <ApiStatus query={homeQuery} label="home record" fallbackLabel={homeRecord.provenance} />
          </div>
          <dl className="hq-record-list">
            <div>
              <dt>Address</dt>
              <dd>{homeRecord.address}</dd>
            </div>
            <div>
              <dt>Service</dt>
              <dd>{homeRecord.service}</dd>
            </div>
            <div>
              <dt>Utility</dt>
              <dd>{homeRecord.utility}</dd>
            </div>
            <div>
              <dt>Status</dt>
              <dd>{homeRecord.status}</dd>
            </div>
          </dl>
        </section>
      </section>

      <section className="hq-api-strip" aria-label="Read-only backend wiring status">
        <ApiStatus query={homeQuery} label="home record" />
        <ApiStatus query={factsQuery} label="fact lifecycle" />
        <ApiStatus query={loadCalcQuery} label="NEC planning load calculation" />
      </section>
      {homeQuery.error && !homeLoadNoHome ? (
        <section className="hq-api-strip hq-api-strip-warn" aria-label="Home backend read issue">
          <Badge tone="warn">Home read unavailable</Badge>
          <span>Address onboarding is not shown for authentication or server errors.</span>
        </section>
      ) : null}

      <section className="hq-dashboard-grid">
        <article className="hq-panel hq-diagram-panel">
          <div className="hq-panel-head">
            <div>
              <p className="hq-eyebrow">Energy Twin</p>
              <h2>Known systems and open gaps</h2>
            </div>
            <Badge tone="info">Read-only</Badge>
          </div>
          <HomeDiagram selectedId={selected?.id} onSelect={setSelected} />
          <div className="hq-legend">
            <span><i className="hq-dot hq-dot-ok" />Known</span>
            <span><i className="hq-dot hq-dot-warn" />Needs confirmation</span>
            <span><i className="hq-dot hq-dot-muted" />Missing</span>
          </div>
        </article>

        <aside className="hq-side-stack">
          <article className="hq-panel">
            <p className="hq-eyebrow">Selected object</p>
            <h2>{selected?.title}</h2>
            <p className="hq-muted">{selected?.detail}</p>
            <p className="hq-source">Basis: {selected?.basis}</p>
          </article>
          <article className="hq-panel hq-kpi-grid">
            <div>
              <strong>{knownCount}</strong>
              <span>{factsQuery.data?.length ? "backend known facts" : "placeholder known objects"}</span>
            </div>
            <div>
              <strong>{needsCount}</strong>
              <span>needs confirmation</span>
            </div>
            <div>
              <strong>{missingCount}</strong>
              <span>{loadCalcQuery.data ? "load-calc missing inputs" : "placeholder missing objects"}</span>
            </div>
          </article>
        </aside>
      </section>

      <section className="hq-panel">
        <div className="hq-panel-head">
          <div>
            <p className="hq-eyebrow">Planning load read</p>
            <h2>{necSummary.posture}</h2>
          </div>
          <Badge tone={loadCalcQuery.data ? "info" : "warn"}>{necSummary.confidence}</Badge>
        </div>
        <div className="hq-data-grid">
          <div>
            <span>Calculated service load</span>
            <strong>{necSummary.amps}</strong>
          </div>
          <div>
            <span>Missing inputs</span>
            <strong>{necSummary.missing}</strong>
          </div>
          <div>
            <span>Boundary</span>
            <strong>{necSummary.boundary}</strong>
          </div>
        </div>
      </section>

      <section className="hq-panel">
        <div className="hq-panel-head">
          <div>
            <p className="hq-eyebrow">Known facts</p>
            <h2>What the shell can safely say now</h2>
          </div>
          <ApiStatus query={factsQuery} label="facts" fallbackLabel="Placeholder-safe" />
        </div>
        <div className="hq-fact-table">
          {factRows.map((fact) => (
            <div key={fact.label}>
              <span>{fact.label}</span>
              <strong>{fact.value}</strong>
              <small>{fact.basis}</small>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export function ExploreShellPage() {
  const [selectedGoals, setSelectedGoals] = useState([]);

  function toggleGoal(goalId) {
    setSelectedGoals((current) =>
      current.includes(goalId) ? current.filter((id) => id !== goalId) : [...current, goalId],
    );
  }

  return (
    <div className="hq-page">
      <header className="hq-page-head">
        <p className="hq-eyebrow">Explore</p>
        <h1>Start with homeowner goals.</h1>
        <p>
          Explore leads with intent. Learn stays inside this section as supporting context, not as a
          primary navigation object.
        </p>
      </header>

      <section className="hq-panel">
        <div className="hq-panel-head">
          <div>
            <p className="hq-eyebrow">Goals</p>
            <h2>What should the home do next?</h2>
          </div>
          <Badge tone="warn">Selections are local UI only</Badge>
        </div>
        <div className="hq-goals-grid">
          {goals.map((goal) => {
            const active = selectedGoals.includes(goal.id);
            return (
              <button
                key={goal.id}
                type="button"
                className={active ? "hq-goal-card hq-goal-card-active" : "hq-goal-card"}
                onClick={() => toggleGoal(goal.id)}
                aria-pressed={active}
              >
                <span className="hq-goal-icon"><Icon name="spark" /></span>
                <span>
                  <strong>{goal.title}</strong>
                  <small>{goal.blurb}</small>
                </span>
                <span className="hq-goal-seeds">
                  {goal.seeds.map((seed) => (
                    <Badge key={seed} tone={seed === "Sandbox" ? "warn" : "info"}>{seed}</Badge>
                  ))}
                </span>
              </button>
            );
          })}
        </div>
        <div className="hq-selection-bar">
          <span>
            <strong>{selectedGoals.length}</strong> goals selected
          </span>
          <Link className="hq-btn hq-btn-secondary" to="/planner">
            Take goals to Planner <Icon name="arrow" size={14} />
          </Link>
        </div>
      </section>

      <section className="hq-panel">
        <div className="hq-panel-head">
          <div>
            <p className="hq-eyebrow">Learn</p>
            <h2>Plain-language context tied to the Twin</h2>
          </div>
          <Badge tone="info">Sub-section</Badge>
        </div>
        <div className="hq-learn-grid">
          {learnTopics.map((topic) => (
            <article key={topic.title} className="hq-card">
              <h3>{topic.title}</h3>
              <p>{topic.summary}</p>
              <small>{topic.ties}</small>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}

export function PlannerShellPage() {
  const [tab, setTab] = useState("templates");
  const [overlayId, setOverlayId] = useState(null);
  const templateQuery = useApiQuery("hq-planner-sandbox-templates", api.getPlannerSandboxTemplates);
  // Two finalized live templates from the backend registry (or static fallback when the
  // read is unavailable), merged with three render-only mock drafts for display only.
  const liveTemplates = templateQuery.data?.templates?.length
    ? templateQuery.data.templates.map(toTemplateCard)
    : liveTemplateFallback;
  const plannerTemplates = [...liveTemplates, ...draftTemplates];
  const selectableTemplates = plannerTemplates.filter((template) => !template.isDraft);
  // Drafts can never drive the canvas overlay; only a finalized live template can be selected.
  const activeOverlayId =
    overlayId && selectableTemplates.some((template) => template.id === overlayId)
      ? overlayId
      : selectableTemplates[0]?.id;
  const overlay = templateOverlays[activeOverlayId] || fallbackTemplateOverlay;

  // Early-return guard: a draft template must not enter the real scenario path.
  function selectTemplate(template) {
    if (template.isDraft) return;
    setOverlayId(template.id);
  }

  return (
    <div className="hq-page">
      <header className="hq-page-head hq-planner-head">
        <div>
          <p className="hq-eyebrow">Planner</p>
          <h1>Plan, sketch, compare.</h1>
          <p>
            Guided Templates, Sandbox Drafts, and Comparisons are read-only shell surfaces. No draft
            save, validation persistence, or project promotion is wired.
          </p>
        </div>
        <ApiStatus query={templateQuery} label="sandbox template registry" fallbackLabel="Static planner data" />
      </header>

      <section className="hq-panel hq-planner-canvas">
        <div className="hq-panel-head">
          <div>
            <p className="hq-eyebrow">Scenario canvas</p>
            <h2>How a template touches the home</h2>
          </div>
          <Badge tone="info">{overlay.caption}</Badge>
        </div>
        <div className="hq-canvas-grid">
          <HomeDiagram selectedId={null} onSelect={() => {}} overlay={overlay} />
          <div className="hq-overlay-list">
            {plannerTemplates.map((template) => {
              const active = template.id === activeOverlayId;
              const chipClass = [
                "hq-overlay-choice",
                active ? "hq-overlay-choice-active" : "",
                template.isDraft ? "hq-overlay-choice-draft" : "",
              ]
                .filter(Boolean)
                .join(" ");
              return (
                <button
                  type="button"
                  key={template.id}
                  className={chipClass}
                  onClick={() => selectTemplate(template)}
                  disabled={template.isDraft}
                  aria-disabled={template.isDraft}
                >
                  <i style={{ background: (templateOverlays[template.id] || fallbackTemplateOverlay).color }} />
                  <span>{template.architecture}</span>
                  <strong>{template.intent}{template.isDraft ? " · Draft" : ""}</strong>
                </button>
              );
            })}
          </div>
        </div>
      </section>

      <section className="hq-upgrade-strip" aria-label="Maturity path">
        {upgradePath.map(([label, detail, state], index) => (
          <article key={label} className={`hq-upgrade-step hq-upgrade-${state}`}>
            <span>{index + 1}</span>
            <strong>{label}</strong>
            <small>{detail}</small>
          </article>
        ))}
      </section>

      <nav className="hq-subtabs" aria-label="Planner sections">
        <button type="button" className={tab === "templates" ? "active" : ""} onClick={() => setTab("templates")}>
          Guided Templates
        </button>
        <button type="button" className={tab === "sandbox" ? "active" : ""} onClick={() => setTab("sandbox")}>
          Sandbox Drafts
        </button>
        <button type="button" className={tab === "comparisons" ? "active" : ""} onClick={() => setTab("comparisons")}>
          Comparisons
        </button>
      </nav>

      {tab === "templates" ? <TemplatesView templates={plannerTemplates} registry={templateQuery.data} query={templateQuery} /> : null}
      {tab === "sandbox" ? <SandboxView /> : null}
      {tab === "comparisons" ? <ComparisonsView /> : null}
    </div>
  );
}

function TemplatesView({ templates, registry, query }) {
  const liveCount = templates.filter((template) => !template.isDraft).length;
  const draftCount = templates.filter((template) => template.isDraft).length;
  return (
    <>
      <section className="hq-api-strip" aria-label="Planner backend wiring status">
        <ApiStatus query={query} label="guided template registry" fallbackLabel="Static template placeholders" />
        <Badge tone={registry?.read_only ? "info" : "warn"}>
          {registry?.read_only ? "Registry is read-only" : "No registry mutation wired"}
        </Badge>
        <Badge tone="info">{liveCount} live · {draftCount} draft</Badge>
        <Badge tone="warn">Drafts are render-only — no save, validate, or promotion</Badge>
      </section>
      <section className="hq-grid-section">
        {templates.map((template) => (
          <article key={template.id} className={template.isDraft ? "hq-card hq-card-draft" : "hq-card"}>
            <div className="hq-card-head">
              <Badge tone="info">{template.architecture}</Badge>
              {template.isDraft ? (
                <Badge tone="warn">Draft</Badge>
              ) : (
                <Badge tone={template.backup === "None" ? "muted" : "warn"}>{template.backup}</Badge>
              )}
            </div>
            <h3>{template.intent}</h3>
            <p>{template.blurb}</p>
            <dl className="hq-mini-stats">
              <div>
                <dt>Input tier</dt>
                <dd><Pips value={template.cost} /></dd>
              </div>
              <div>
                <dt>Step depth</dt>
                <dd><Pips value={template.complexity} /></dd>
              </div>
            </dl>
            {template.basis ? <p className="hq-source">Basis: {template.basis}</p> : null}
            {template.isDraft ? (
              <p className="hq-source">Draft pattern — render-only mock, not a finalized backend template.</p>
            ) : (
              <button type="button" className="hq-link-button">Seed draft placeholder</button>
            )}
          </article>
        ))}
      </section>
    </>
  );
}

function SandboxView() {
  return (
    <section className="hq-grid-section hq-sandbox-grid">
      {sandboxDrafts.map((draft) => (
        <article key={draft.name} className="hq-card">
          <div className="hq-card-head">
            <Badge tone="warn">{draft.maturity}</Badge>
            <small>{draft.templateId}</small>
          </div>
          <h3>{draft.name}</h3>
          <p>{draft.goal}</p>
          <FieldList label="Selected categories" items={draft.fields} />
          <FieldList label="Assumptions" items={draft.assumptions} />
          <FieldList label="Missing facts" items={draft.missing} warn />
        </article>
      ))}
      <article className="hq-card hq-empty-card">
        <Icon name="plus" size={24} />
        <h3>Start a new sandbox draft</h3>
        <p>Placeholder only. Draft creation and persistence are intentionally deferred.</p>
      </article>
    </section>
  );
}

function FieldList({ label, items, warn = false }) {
  return (
    <div className={warn ? "hq-field-list hq-field-list-warn" : "hq-field-list"}>
      <strong>{label}</strong>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function ComparisonsView() {
  return (
    <section className="hq-panel">
      <div className="hq-panel-head">
        <div>
          <p className="hq-eyebrow">Comparisons</p>
          <h2>Templates and drafts on the same fields</h2>
        </div>
        <Badge tone="warn">Illustrative only</Badge>
      </div>
      <div className="hq-compare-wrap">
        <table className="hq-compare-table">
          <thead>
            <tr>
              <th>Field</th>
              <th>Summer resilience</th>
              <th>EV + heat pump</th>
              <th>TOU pattern</th>
            </tr>
          </thead>
          <tbody>
            {comparisonRows.map(([field, one, two, three]) => (
              <tr key={field}>
                <th>{field}</th>
                <td>{one}</td>
                <td>{two}</td>
                <td>{three}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function getBuilderRows(estimateReadiness, productPreferences, programIntelligence, energyPassport) {
  if (!estimateReadiness && !productPreferences && !programIntelligence && !energyPassport) {
    return builderReadiness;
  }

  return [
    [
      "Estimate posture",
      formatLabel(estimateReadiness?.readiness_summary?.overall_status || "not available"),
      estimateReadiness?.estimate_allowed ? "draft" : "blocked",
    ],
    [
      "Confirmation gates",
      `${estimateReadiness?.readiness_summary?.pending_gate_count ?? 0} pending`,
      estimateReadiness?.readiness_summary?.pending_gate_count ? "needs" : "draft",
    ],
    [
      "Product guidance",
      formatLabel(productPreferences?.summary?.overall_status || "not available"),
      productPreferences?.summary?.product_selection_allowed ? "draft" : "blocked",
    ],
    [
      "Program awareness",
      formatLabel(programIntelligence?.summary?.overall_status || "not available"),
      programIntelligence?.summary?.eligibility_determined ? "draft" : "needs",
    ],
    [
      "Energy passport",
      formatLabel(energyPassport?.summary?.overall_status || "not available"),
      energyPassport?.summary?.transfer_ready ? "draft" : "needs",
    ],
    ["Contractor handoff", "Deferred", "blocked"],
  ];
}

export function BuilderShellPage() {
  const homeQuery = useApiQuery("hq-builder-home", api.getHome);
  const homeId = homeQuery.data?.id;
  const estimateQuery = useApiQuery(`hq-estimate-readiness:${homeId || "none"}`, () => api.getEstimateReadiness(homeId), {
    enabled: Boolean(homeId),
  });
  const productQuery = useApiQuery(`hq-product-preferences:${homeId || "none"}`, () => api.getProductPreferences(homeId), {
    enabled: Boolean(homeId),
  });
  const programQuery = useApiQuery(`hq-program-intelligence:${homeId || "none"}`, () => api.getProgramIntelligence(homeId), {
    enabled: Boolean(homeId),
  });
  const passportQuery = useApiQuery(`hq-energy-passport:${homeId || "none"}`, () => api.getEnergyPassport(homeId), {
    enabled: Boolean(homeId),
  });
  const readinessRows = getBuilderRows(estimateQuery.data, productQuery.data, programQuery.data, passportQuery.data);
  const missingInputs =
    (estimateQuery.data?.missing_inputs?.length || 0) +
    (productQuery.data?.missing_inputs?.length || 0) +
    (programQuery.data?.missing_inputs?.length || 0) +
    (passportQuery.data?.transfer_readiness?.missing_transfer_inputs?.length || 0);
  const backendSummaryLoaded = Boolean(estimateQuery.data || productQuery.data || programQuery.data || passportQuery.data);

  return (
    <div className="hq-page">
      <header className="hq-page-head">
        <p className="hq-eyebrow">Builder</p>
        <h1>Build readiness, not contractor workflow yet.</h1>
        <p>
          Builder frames what would need to become true before a project can move forward. It avoids
          contractor handoff, proposal, persistence, save/edit, and project promotion behavior.
        </p>
      </header>

      <section className="hq-panel">
        <div className="hq-panel-head">
          <div>
            <p className="hq-eyebrow">Project readiness</p>
            <h2>Selected draft context</h2>
          </div>
          <ApiStatus query={estimateQuery} label="estimate readiness" fallbackLabel="Not project-promoted" />
        </div>
        <div className="hq-builder-grid">
          {readinessRows.map(([label, value, state]) => (
            <article key={label} className={`hq-builder-item hq-builder-${state}`}>
              <span>{label}</span>
              <strong>{value}</strong>
            </article>
          ))}
        </div>
      </section>

      <section className="hq-api-strip" aria-label="Builder backend wiring status">
        <ApiStatus query={estimateQuery} label="estimate readiness" />
        <ApiStatus query={productQuery} label="product preference metadata" />
        <ApiStatus query={programQuery} label="program intelligence metadata" />
        <ApiStatus query={passportQuery} label="energy passport metadata" />
      </section>

      <section className="hq-panel">
        <div className="hq-panel-head">
          <div>
            <p className="hq-eyebrow">Backend readiness summary</p>
            <h2>{backendSummaryLoaded ? `${missingInputs} missing inputs surfaced` : "Backend readiness not loaded"}</h2>
          </div>
          <Badge tone="warn">Planning-only</Badge>
        </div>
        <div className="hq-data-grid">
          <div>
            <span>Estimate allowed</span>
            <strong>{estimateQuery.data ? (estimateQuery.data.estimate_allowed ? "Yes" : "No") : "Not read"}</strong>
          </div>
          <div>
            <span>Product selection</span>
            <strong>{productQuery.data ? (productQuery.data.summary?.product_selection_allowed ? "Allowed" : "Deferred") : "Not read"}</strong>
          </div>
          <div>
            <span>Program eligibility</span>
            <strong>{programQuery.data ? (programQuery.data.summary?.eligibility_determined ? "Determined" : "Not determined") : "Not read"}</strong>
          </div>
          <div>
            <span>Transfer ready</span>
            <strong>{passportQuery.data ? (passportQuery.data.summary?.transfer_ready ? "Yes" : "No") : "Not read"}</strong>
          </div>
        </div>
      </section>

      <section className="hq-panel">
        <div className="hq-panel-head">
          <div>
            <p className="hq-eyebrow">Readiness lane</p>
            <h2>What must be resolved first</h2>
          </div>
          <Badge tone="info">Homeowner-oriented</Badge>
        </div>
        <ol className="hq-checklist">
          <li><Icon name="shield" /> Confirm backup-load priorities and missing electrical facts.</li>
          <li><Icon name="shield" /> Keep pricing, permitting, AHJ, and utility approval claims out of the shell.</li>
          <li><Icon name="shield" /> Preserve provenance and placeholder labels when this is later wired.</li>
        </ol>
      </section>
    </div>
  );
}

export function CapabilitiesShellPage({ internal = false }) {
  return (
    <div className="hq-page">
      <header className="hq-page-head">
        <p className="hq-eyebrow">{internal ? "Internal capabilities" : "Capabilities"}</p>
        <h1>Capability map is preserved off primary navigation.</h1>
        <p>
          This route remains reachable for inspection, but homeowner navigation stays focused on
          Home, Explore, Planner, and Builder.
        </p>
      </header>
      <section className="hq-grid-section">
        {capabilities.map(([name, description]) => (
          <article className="hq-card" key={name}>
            <Badge tone={internal ? "warn" : "info"}>{internal ? "Internal" : "Capability"}</Badge>
            <h3>{name}</h3>
            <p>{description}</p>
          </article>
        ))}
      </section>
    </div>
  );
}

export function CatalogShellPage() {
  return (
    <div className="hq-page">
      <header className="hq-page-head">
        <p className="hq-eyebrow">Catalog</p>
        <h1>Catalog remains reachable, outside primary navigation.</h1>
        <p>Items here are static categories only. No product facts, prices, availability, or compatibility claims are made.</p>
      </header>
      <section className="hq-grid-section">
        {catalogItems.map(([name, posture]) => (
          <article className="hq-card" key={name}>
            <Badge tone="warn">Static</Badge>
            <h3>{name}</h3>
            <p>{posture}</p>
          </article>
        ))}
      </section>
    </div>
  );
}
