import { useMemo, useState } from "react";

import { ErrorState, LoadingState } from "../components/AsyncState";
import { api } from "../lib/api";
import { useApiQuery } from "../lib/useApiQuery";

const surfaces = ["Explore", "Twin", "Plan", "Build"];

function HomeDiagram({ geometry }) {
  const planes = geometry?.roof_planes || [];
  const shading = geometry?.per_plane_shading || [];
  return (
    <div className="home-diagram" aria-label="Home energy diagram">
      <svg viewBox="0 0 420 260" role="img">
        <defs>
          <linearGradient id="glassShell" x1="0" x2="1">
            <stop offset="0%" stopColor="#d8eef7" stopOpacity="0.28" />
            <stop offset="100%" stopColor="#ffffff" stopOpacity="0.62" />
          </linearGradient>
        </defs>
        <rect x="0" y="0" width="420" height="260" rx="8" fill="#111820" />
        <path d="M58 138 L210 50 L362 138 L362 222 L58 222 Z" fill="url(#glassShell)" stroke="#b8d7e8" />
        <path d="M88 136 L210 74 L332 136" fill="none" stroke="#5dd6a7" strokeWidth="5" />
        <path d="M126 126 L210 86 L294 126" fill="none" stroke="#f2c94c" strokeWidth="7" />
        <rect x="172" y="158" width="76" height="64" fill="#18232d" stroke="#c9d7df" />
        <circle cx="96" cy="198" r="10" fill="#5dd6a7" />
        <circle cx="324" cy="198" r="10" fill="#f2c94c" />
        <path d="M96 198 C145 176 166 176 210 190 C250 204 278 210 324 198" fill="none" stroke="#8fbfe0" strokeWidth="3" />
      </svg>
      <div className="diagram-meta">
        <span>{planes.length} roof plane{planes.length === 1 ? "" : "s"}</span>
        <span>{shading.length ? `${Math.round((shading[0].production_factor || 0) * 100)}% plane factor` : "No shading trace"}</span>
      </div>
    </div>
  );
}

export function C1ExperiencePage() {
  const [activeSurface, setActiveSurface] = useState("Explore");
  const homeQuery = useApiQuery("c1-home", api.getHome);
  const homeId = homeQuery.data?.id;
  const factsQuery = useApiQuery(["c1-facts", homeId].join(":"), () => api.getFacts(homeId), { enabled: Boolean(homeId), initialData: [] });
  const geometryQuery = useApiQuery(["c1-geometry", homeId].join(":"), () => api.getGeometryExport(homeId), { enabled: Boolean(homeId) });
  const loadCalcQuery = useApiQuery(["c1-nec", homeId].join(":"), () => api.getNec220LoadCalculation(homeId), { enabled: Boolean(homeId) });

  const selectedResult = loadCalcQuery.data?.results?.[0];
  const factSummary = useMemo(() => {
    const facts = factsQuery.data || [];
    return {
      total: facts.length,
      known: facts.filter((fact) => fact.effective_confidence_tier === "known").length,
      assumed: facts.filter((fact) => fact.effective_confidence_tier === "assumed").length,
    };
  }, [factsQuery.data]);

  const loading = homeQuery.loading || factsQuery.loading || geometryQuery.loading || loadCalcQuery.loading;
  const error = homeQuery.error || factsQuery.error || geometryQuery.error || loadCalcQuery.error;

  return (
    <section className="c1-workspace">
      <div className="surface-tabs" role="tablist" aria-label="Home workflow surfaces">
        {surfaces.map((surface) => (
          <button
            key={surface}
            className={surface === activeSurface ? "surface-tab active" : "surface-tab"}
            type="button"
            onClick={() => setActiveSurface(surface)}
          >
            {surface}
          </button>
        ))}
      </div>

      {loading ? <LoadingState label="Reading authenticated home data..." /> : null}
      {error ? <ErrorState error={error} label="Unable to load the C1 workspace." /> : null}

      {!loading && !error ? (
        <div className="surface-layout">
          <div className="surface-primary">
            <p className="eyebrow">C1 homeowner shell</p>
            <h2>{activeSurface}</h2>
            <HomeDiagram geometry={geometryQuery.data} />
          </div>
          <div className="surface-side">
            <div className="surface-metric">
              <span>Fact confidence</span>
              <strong>{factSummary.known} known</strong>
              <small>{factSummary.assumed} assumed of {factSummary.total} total facts</small>
            </div>
            <div className="surface-metric">
              <span>Load calculation</span>
              <strong>{selectedResult?.calculated_service_load_amps ?? "Gap"}</strong>
              <small>{selectedResult?.method || "220 readiness"} planning amps</small>
            </div>
            <div className="surface-metric">
              <span>Build posture</span>
              <strong>{selectedResult?.calculation_ready ? "Review ready" : "Needs facts"}</strong>
              <small>Professional review boundary remains active</small>
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}
