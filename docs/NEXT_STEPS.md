# Next Steps

## Highest-Leverage Next Implementation Step

Deepen provenance coverage across more entity fields and derived outputs now that scenario comparison consumes source-lineage summaries, while still keeping takeoff snapshots transient until provenance and verification depth are stronger.

## Why This Is Next

- Trust visibility now makes uncertainty obvious, and scenario comparison now exposes lineage, but the underlying provenance model is still thin.
- A provenance foundation now exists, but it still does not cover every field or every derived output path.
- Generated takeoffs are intentionally transient and placeholder-priced until stronger source lineage exists.
- Advisor intelligence is broader, but it still depends on planning heuristics rather than verified engineering inputs.
- The new doctrine layer now makes the strategic direction explicit; the next implementation step should strengthen provenance and trust without reopening architecture planning.

## Near-Term Follow-On Work

1. Expand provenance coverage to more planning entities and derived fields.
2. Expand field-level provenance and lineage summaries for scenarios, pathways, loads, and design facts.
3. Add delete/archive workflows for mutable planning records.
4. Tighten migration discipline beyond the baseline scaffold.

## Strategic Guardrail

Future implementation should read `docs/philosophy/*` and `docs/adr/*` during restore so work stays aligned with living-house-model, planning-only, and trust-first doctrine.

## Deferred Until Later

- Auth
- Billing
- Provenance ledger
- Audit trail
- NEC/permitting logic
