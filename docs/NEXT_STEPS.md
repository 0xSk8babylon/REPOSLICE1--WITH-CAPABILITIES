# Next Steps

## Highest-Leverage Next Implementation Step

Extend the inspectable recommendation-profile model beyond current battery and solar planning ranges into richer recommendation behavior and broader design/scenario lineage coverage, while keeping formulas internal, outputs provenance-aware, and the new panel/service and roof-readiness layers explicit about what they do not yet prove.

## Why This Is Next

- Trust visibility now makes uncertainty obvious, and scenario comparison now exposes lineage, but the underlying provenance model is still thin.
- A provenance foundation now exists, but it still does not cover every field or every derived output path.
- Generated takeoffs are intentionally transient and placeholder-priced until stronger source lineage exists.
- Advisor intelligence is broader, but it still depends on planning heuristics rather than verified engineering inputs.
- The new doctrine layer now makes the strategic direction explicit; the next implementation step should strengthen provenance and trust without reopening architecture planning.

## Near-Term Follow-On Work

1. Refine backup-load selection and backup-scope realism so the new panel/service architecture layer rests on stronger deterministic load intent before inverter sizing begins.
2. Add the next recommendation slice that explains how current architecture choices and equipment mix shift profile fit without exposing deeper engineering math.
3. Deepen the solar readiness layer with better internal roof-capacity and placement realism before introducing inverter sizing.
4. Add future geometry-ingest hooks for traced polygons, roof planes, and usable-area estimates without replacing the current recommendation system.
5. Extend field-level provenance and lineage summaries for design facts, scenario inputs, and broader home-model records beyond the current products, loads, pathways, and recommendation inspectability layer.
6. Add delete/archive workflows for mutable planning records.

## Strategic Guardrail

Future implementation should load philosophy or ADR files only when the task touches strategic doctrine, trust posture, or architecture boundaries that those files constrain.

## Deferred Until Later

- Auth
- Billing
- Provenance ledger
- Audit trail
- NEC/permitting logic
