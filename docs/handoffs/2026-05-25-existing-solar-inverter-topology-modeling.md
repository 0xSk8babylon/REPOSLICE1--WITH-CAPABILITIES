# 2026-05-25 Existing Solar / Inverter Topology Modeling

## Session Metadata

- Session date: 2026-05-25
- Starting commit: `314e4ef`
- Current head commit before next commit: `314e4ef`
- Repo commits created this session:
  - none yet

## Implementation Summary

- Added an additive `current_home_energy_architecture` layer to the advisor recommendation output.
- The new layer classifies planning-only current-state solar/inverter topology across:
  - microinverter system
  - string inverter system
  - optimizer-based system
  - hybrid inverter system
  - AC-coupled battery retrofit
  - DC-coupled battery system
  - unknown / not recorded topology
  - mixed or unclear topology
- Current-state modeling now distinguishes:
  - existing solar recorded
  - proposed solar only recorded
  - unclear stage
  - not recorded
- Added explicit existing-vs-proposed architecture summaries, outage-solar behavior cautions, battery retrofit implications, expansion implications, generator coexistence notes, topology source inputs, and architecture relationship components for UI visualization.
- Threaded the current-state topology layer into the future-looking inverter/system architecture output so existing microinverter and other current-home conditions inform AC-coupled vs hybrid planning posture.
- Expanded the structured reasoning graph to include current topology as an inspectable dependency node.
- Updated seeded demo data so `design_001` now represents an existing microinverter solar system with a proposed battery retrofit path.

## Files Changed

- `PROJECT_STATE.md`
- `SESSION_HANDOFF.md`
- `apps/api/app/design_advisor/schemas.py`
- `apps/api/app/seed/sample_data.py`
- `apps/api/app/services/resilience_recommendation.py`
- `apps/api/tests/test_resilience_recommendation.py`
- `apps/web/src/pages/DesignAdvisorPage.jsx`
- `docs/ACTIVE_TASKS.md`
- `docs/API_CONTRACTS.md`
- `docs/CURRENT_STATE.md`
- `docs/NEXT_STEPS.md`
- `docs/SESSION_LOG.md`
- `docs/handoffs/2026-05-25-existing-solar-inverter-topology-modeling.md`
- `docs/session-continuity/active-pressure-points.md`
- `docs/session-continuity/current-roadmap.md`
- `docs/session-continuity/project-state.md`

## Verification Commands And Results

- `python3 -m unittest discover -s tests -p 'test_*.py'` passed in `apps/api`
- `python3 -m compileall app` passed in `apps/api`
- `npm run build` passed in `apps/web`
- `git diff --check` passed

## Deterministic / Provenance / Trust Protections Verified

- The new topology layer is deterministic and assembled from current role markers, current product signals, architecture type, and backup/control-path context only.
- Unknown current-state evidence is preserved as unknown rather than guessed from future recommendations.
- Microinverter handling remains planning-only and explicitly avoids assuming outage capability without compatible gateway, grid-forming, and storage architecture.
- API evolution stayed additive and current UI/API contracts remained compatible.

## Remaining Risks

- Current-state topology still depends on role markers and recorded product signals rather than a verified field inventory.
- Optimizer-based topology remains inferred from product context because there is no dedicated optimizer product type yet.
- Existing local DBs may need reseeding to expose `recommendation.current_home_energy_architecture_v1` and the updated seeded microinverter example.
- Generator coexistence and outage-solar behavior remain planning cautions rather than operating guarantees.

## Next Recommended Boundary

Deepen the solar-readiness and roof-capacity-realism slice behind the current recommendation architecture while preserving the new current-state topology model and planning-only trust boundary.
