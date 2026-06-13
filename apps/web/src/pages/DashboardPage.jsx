import { Link } from "react-router-dom";

import { ErrorState, LoadingState } from "../components/AsyncState";
import { api } from "../lib/api";
import { useApiQuery } from "../lib/useApiQuery";

function buildKnownFacts(home, loadSummary, designs, scenarios) {
  const facts = [];

  if (home?.address_line_1 || home?.city || home?.state) {
    facts.push({
      label: "Home record",
      value: [home.address_line_1, home.city, home.state].filter(Boolean).join(", "),
    });
  }

  if (home?.utility_provider) {
    facts.push({
      label: "Utility context",
      value: home.utility_provider,
    });
  }

  if (home?.service_size) {
    facts.push({
      label: "Electrical service",
      value: `${home.service_size}A service is recorded`,
    });
  }

  if (home?.buildings?.length || home?.panels?.length) {
    facts.push({
      label: "Modeled home systems",
      value: `${home.buildings?.length || 0} structure${
        home.buildings?.length === 1 ? "" : "s"
      } and ${home.panels?.length || 0} panel${home.panels?.length === 1 ? "" : "s"} are in the Twin`,
    });
  }

  if (loadSummary?.total_running_watts) {
    facts.push({
      label: "Load context",
      value: "Some household load information is already available",
    });
  }

  if (designs.length || scenarios.length) {
    facts.push({
      label: "Planning paths",
      value: `${designs.length} design path${designs.length === 1 ? "" : "s"} and ${
        scenarios.length
      } scenario${scenarios.length === 1 ? "" : "s"} can be explored`,
    });
  }

  if (!facts.length) {
    return [
      {
        label: "Energy Twin started",
        value: "A homeowner planning record is ready for more details",
      },
    ];
  }

  return facts.slice(0, 4);
}

function buildOpportunityPaths(home, loadSummary, designs, scenarios) {
  return [
    {
      label: "Solar",
      summary:
        home?.utility_provider || designs.length
          ? "The Twin can frame a solar planning path from your home record and available utility context."
          : "The Twin can start a solar path once the home and utility context are more complete.",
    },
    {
      label: "Battery",
      summary:
        loadSummary?.total_running_watts || scenarios.length
          ? "Known load and scenario context can help explain what battery questions should be reviewed next."
          : "Battery planning improves when important household loads and backup goals are recorded.",
    },
    {
      label: "Backup",
      summary:
        home?.panels?.length || loadSummary?.total_running_watts
          ? "Panel and load context can help separate backup planning questions from final electrical decisions."
          : "Backup planning needs panel details, key loads, and homeowner priorities before it can be useful.",
    },
    {
      label: "Upgrades",
      summary:
        home?.service_size || home?.panels?.length
          ? "Recorded service and panel details can help surface upgrade paths that may need professional review."
          : "Upgrade paths become clearer after service size and panel information are added.",
    },
  ];
}

function buildMissingActions(home, loadSummary, designs) {
  const actions = [];

  if (!home?.service_size) {
    actions.push({
      label: "Add main service size",
      detail: "This helps the Twin explain upgrade and backup planning questions more clearly.",
    });
  }

  if (!home?.utility_provider) {
    actions.push({
      label: "Add utility provider",
      detail: "This gives solar, program, and utility-context guidance a better starting point.",
    });
  }

  if (!home?.panels?.length) {
    actions.push({
      label: "Add panel details",
      detail: "This helps separate known electrical context from items a contractor still needs to confirm.",
    });
  }

  if (!loadSummary?.total_running_watts) {
    actions.push({
      label: "Add important household loads",
      detail: "This improves battery and backup planning without turning the plan into a final design.",
    });
  }

  if (!designs.length) {
    actions.push({
      label: "Start a planning path",
      detail: "Choose the first solar, battery, backup, or upgrade path you want the Twin to explore.",
    });
  }

  if (!actions.length) {
    return [
      {
        label: "Review goals and timing",
        detail: "Your next details can focus on backup goals, equipment preferences, or future upgrade timing.",
      },
    ];
  }

  return actions.slice(0, 4);
}

export function DashboardPage() {
  const homeQuery = useApiQuery("home", api.getHome);
  const loadsQuery = useApiQuery("loads-summary", api.getLoadSummary);
  const designsQuery = useApiQuery("designs", api.getDesigns);
  const scenariosQuery = useApiQuery("scenarios", api.getScenarios);

  const isLoading = homeQuery.loading || loadsQuery.loading || designsQuery.loading || scenariosQuery.loading;
  const error = homeQuery.error || loadsQuery.error || designsQuery.error || scenariosQuery.error;

  const home = homeQuery.data;
  const loadSummary = loadsQuery.data;
  const designs = designsQuery.data || [];
  const scenarios = scenariosQuery.data || [];
  const knownFacts = buildKnownFacts(home, loadSummary, designs, scenarios);
  const opportunityPaths = buildOpportunityPaths(home, loadSummary, designs, scenarios);
  const missingActions = buildMissingActions(home, loadSummary, designs);

  return (
    <main className="homeowner-entry">
      <section className="twin-stage" aria-labelledby="twin-welcome-title">
        <div className="twin-stage-copy">
          <p className="twin-eyebrow">Energy Twin</p>
          <h1 id="twin-welcome-title" className="twin-welcome">
            Welcome home,
          </h1>
          <p className="twin-prompt">are you ready?</p>
          <Link className="twin-begin" to="/home-model">
            lets begin...
            <span className="twin-begin-arrow" aria-hidden="true">
              &#8594;
            </span>
          </Link>
        </div>

        <div className="twin-stage-visual" aria-hidden="true">
          <div className="twin-pixels" />
          <svg className="twin-home-svg" viewBox="0 0 200 200" role="presentation" focusable="false">
            <polygon className="twin-home-fill" points="40,92 100,44 160,92" />
            <rect className="twin-home-fill" x="56" y="92" width="88" height="76" />
            <polygon className="twin-home-edge" points="40,92 100,44 160,92" />
            <rect className="twin-home-edge" x="56" y="92" width="88" height="76" />
            <rect className="twin-home-detail" x="90" y="128" width="20" height="40" />
            <rect className="twin-home-detail" x="68" y="110" width="18" height="18" />
            <rect className="twin-home-detail" x="116" y="110" width="18" height="18" />
            <line className="twin-home-detail" x1="70" y1="78" x2="118" y2="59" />
            <line className="twin-home-detail" x1="82" y1="86" x2="130" y2="67" />
            <circle className="twin-home-node" cx="100" cy="44" r="3.4" />
            <circle className="twin-home-node" cx="40" cy="92" r="3" />
            <circle className="twin-home-node" cx="160" cy="92" r="3" />
            <circle className="twin-home-node" cx="56" cy="168" r="3" />
            <circle className="twin-home-node" cx="144" cy="168" r="3" />
          </svg>
          <div className="twin-scan" />
        </div>

        <div className="twin-stage-outline" aria-hidden="true">
          <svg
            className="twin-outline-svg"
            viewBox="0 0 120 120"
            role="presentation"
            focusable="false"
          >
            <path className="twin-outline-stroke" d="M12 60 L60 20 L108 60" />
            <path className="twin-outline-stroke" d="M24 56 L24 104 L96 104 L96 56" />
            <path className="twin-outline-stroke" d="M50 104 L50 78 L70 78 L70 104" />
          </svg>
          <p className="twin-outline-caption">Current twin outline</p>
        </div>
      </section>

      <section id="energy-twin-next" className="twin-narrative-section twin-known-section" aria-labelledby="known-title">
        <div className="twin-section-heading">
          <h2 id="known-title">Here's what your home already tells us.</h2>
          <p>
            These are planning facts or placeholders from the current home record. They are not approvals,
            estimates, or final design guidance.
          </p>
        </div>
        {isLoading ? <LoadingState label="Reading the Energy Twin..." /> : null}
        {error ? <ErrorState error={error} label="Unable to read the Energy Twin." /> : null}
        {!isLoading && !error ? (
          <div className="twin-fact-list">
            {knownFacts.map((fact) => (
              <div className="twin-fact-row" key={fact.label}>
                <span>{fact.label}</span>
                <strong>{fact.value}</strong>
              </div>
            ))}
          </div>
        ) : null}
      </section>

      <section className="twin-narrative-section twin-opportunity-section" aria-labelledby="opportunity-title">
        <div className="twin-section-heading">
          <h2 id="opportunity-title">See what your home may be ready to explore.</h2>
          <p>
            These paths are homeowner-safe planning areas. They do not rank options, select equipment,
            calculate savings, or replace contractor and professional review.
          </p>
        </div>
        <div className="twin-path-list">
          {opportunityPaths.map((path) => (
            <div className="twin-path-row" key={path.label}>
              <span>{path.label}</span>
              <p>{path.summary}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="twin-narrative-section twin-complete-section" aria-labelledby="detail-title">
        <div className="twin-section-heading">
          <h2 id="detail-title">Complete the Twin in a few simple steps.</h2>
          <p>
            The Twin gets more useful when missing details are added to the home record. Each step improves
            planning context without treating the plan as approved or final.
          </p>
        </div>
        <div className="twin-action-list">
          {missingActions.map((action, index) => (
            <div className="twin-action-row" key={action.label}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <div>
                <strong>{action.label}</strong>
                <p>{action.detail}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="twin-narrative-section twin-grounding-section" aria-labelledby="grounding-title">
        <div className="twin-section-heading">
          <h2 id="grounding-title">Guidance stays grounded in the home record.</h2>
          <p>
            The overview is based on home inputs, known constraints, utility and program context where
            available, and readiness logic. It keeps internal diagnostics out of the homeowner experience
            and keeps uncertainty visible before decisions are made.
          </p>
        </div>
        <div className="twin-grounding-copy">
          <p>
            The Twin can explain what is known, what is missing, and which planning paths need review. It
            does not claim utility approval, permit readiness, savings, eligibility, final design, or field
            verification.
          </p>
          <p className="twin-caption">
            Guidance remains planning context until the right contractor, utility, or professional review is complete.
          </p>
        </div>
      </section>

      <section className="twin-final-cta" aria-labelledby="final-cta-title">
        <h2 id="final-cta-title">Keep building your home's Energy Twin.</h2>
        <p>
          Add the next few details so the plan can become clearer before contractor, utility, or engineering
          review.
        </p>
        <Link className="twin-primary-action" to="/home-model">
          Continue building the Twin
        </Link>
      </section>
    </main>
  );
}
