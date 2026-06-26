# Planner Intelligence Plan

## Status

Docs-only planning approved by Matt on 2026-06-26.

No implementation is approved by this document. This is a planning gate on top of the completed provider-neutral auth foundation, account-membership ownership enforcement, audit/trust foundation (Alembic `20260625_0003_audit_trust_foundation.py`), and backend/frontend address onboarding slices.

This plan records the approved boundary for the first reasoning tools / planner intelligence slice. It composes existing, verified reasoning service entry points behind a new authorized, audited, provenance-backed read facade. It introduces no new reasoning math, no LLM, no persistence, and no migration.

Production DB changes, Railway runtime wiring, deploy, smoke, provider SDKs, external APIs/secrets, and push remain unapproved and out of scope.

## Approved Direction

Structured data and rules remain authoritative. Planner intelligence is a non-authoritative, source-linked consumer of existing derived and rule outputs.

Approved trust path for a planner-intelligence read:

```text
OIDC/app principal
-> active app-owned account_membership
-> explicit design-scoped authorization (can_access_design)
-> facade composition of existing verified service entry points
-> trust envelope + provenance summary on every block
-> audit event with app-owned actor and object scope (allowed or denied)
```

Planner intelligence must not claim engineering sign-off, permitting status, utility authority, code compliance, pricing authority, or operational truth. Every recommendation/constraint block must carry provenance references; blocks that cannot expose lineage must be downgraded or marked provisional.

## Current Findings

The reasoning layer already exists and is mature. The gap is not additional reasoning; it is consistent authorization, audit, and a uniform trust/provenance envelope around outputs that are scattered across modules.

### Reasoning behavior classification

- Deterministic: scenario ranking, sizing ranges, readiness scoring, dependency impact.
- Rule-based: compatibility issues, product-preference install logic, recommendation profiles (rule provenance seeds exist).
- Derived (inspectable): advisor profiles, planning-state snapshots, scenario comparison, all carrying confidence and missing-inputs.
- Display/context only: AI context view and homeowner/contractor-facing advisory copy.
- Not yet trusted reasoning: operational/Zone 4 concerns; field-level provenance is not exhaustive; no LLM is present anywhere (correct per doctrine).

### Structural gaps this slice targets

1. Inconsistent authorization. `design_advisor` router calls `permissions.require_allowed(can_access_design(...))` with `current_principal`, but several `twin_planning_context` views depend only on `get_db` plus the global `HomeAccessMiddleware`, with no explicit per-object check at the route.
2. No audit on reasoning reads. `audit_service.record` is currently invoked only in auth middleware, onboarding, and privacy. No advisory/derived read is audited today, even though the audit schema already supports `object_type`, `object_id`, `decision`, `source_surface`, and `provenance_refs`.

### Verified service entry points (composition surface)

Design-scoped public entry points:

- `design_advisor_service.explain(db, design_id)` — recommendation profiles and upgrade-path context (this is the same public method the `/design-advisor/summary/{design_id}` route uses).
- `compatibility_service.evaluate_design(db, design_id)` -> `List[CompatibilityExplanation]` — constraints.
- `design_completeness_service.evaluate(db, design_id)` — readiness explanation.
- `scenario_comparison_service.compare(db, scenarios)` — scenario comparison explanation (operates on a scenario list resolved from the design's home).
- `provenance_service.summarize_entity(db, entity_type, entity_id)` — provenance aggregation.

Home-scoped public builders on `twin_planning_context_service`, composed using the design's `home_id`:

- `build_planning_intelligence_readiness_view(db, home_id)`
- `build_constraint_risk_reasoning_view(db, home_id)`
- `build_dependency_impact_readiness_view(db, home_id)`
- `build_dependency_reasoning_view(db, home_id)`

Design-to-home resolution uses `repository.get_design(db, design_id).home_id`. Authorization is enforced with `permissions.can_access_design` at the facade boundary, independent of `HomeAccessMiddleware`.

Explicitly excluded from slice 1: the legacy private `DesignAdvisorService._build_planning_state` / `PlanningStateSnapshot` path. Slice 1 uses only the public `design_advisor_service.explain(...)` output. If that exact legacy snapshot becomes necessary, stop and propose the smallest extraction before implementing.

## Approved Slice Boundary

In scope:

- New module `app/planner_intelligence/` exposing a single endpoint.
- `GET /api/planner-intelligence/designs/{design_id}/summary`.
- Backend only. No UI panel in slice 1.
- Composition of the verified service entry points above; no new reasoning math.
- Explicit `can_access_design` authorization at the facade boundary.
- One audit event per read (allowed and denied), with graceful degradation.
- Uniform trust envelope and aggregated provenance summary on every block.

Out of scope for slice 1:

- Home-level and scenario-level planner-intelligence endpoints.
- Any write, persistence, or versioning of planner-intelligence output.
- New scoring, new reasoning math, or new domain rules.
- New migrations or schema changes.
- LLM or tool-execution integration.
- Internal HTTP calls between services (compose in-process via service singletons only).
- Re-walking or refactoring the 14k-line `twin_planning_context.py`. Only call its public builder methods.
- Frontend (DesignAdvisorPage panel, api.js, uiRegistry) — deferred to a later UI-quality pass once the response contract is proven by tests.

## Architecture

```text
/api/planner-intelligence/designs/{design_id}/summary
  app/planner_intelligence/router.py
    - current_principal dependency
    - repository.get_design -> 404 if missing
    - permissions.require_allowed(can_access_design(db, principal, design_id))
    - safe audit (allowed or denied)
  app/planner_intelligence/schemas.py
    - PlannerIntelligenceDesignSummary
    - per-block trust envelope
  app/services/planner_intelligence.py  (aggregator only)
    - composes: design_advisor_service.explain,
                compatibility_service.evaluate_design,
                design_completeness_service.evaluate,
                scenario_comparison_service.compare (home-scoped scenarios),
                twin_planning_context_service.build_* (home-scoped readiness),
                provenance_service.summarize_entity
    - attaches trust envelope + provenance refs to each block
    - NO new domain math
```

The service is a composition layer. It must not duplicate or re-derive logic owned by the underlying services, and must not reach into private methods.

## API Proposal

Endpoint: `GET /api/planner-intelligence/designs/{design_id}/summary`.

Illustrative response shape:

```jsonc
{
  "view_boundary": {
    "view_name": "planner_intelligence_design_summary",
    "audience": "planner",
    "authority_layer": "advisory",
    "trust_zone": "advisory_explanation",
    "data_classification": "planning_private"
  },
  "design_id": "…",
  "blocks": {
    "recommendations":                { "items": [ … ], "trust_envelope": { … } },
    "constraints":                    { "items": [ … ], "trust_envelope": { … } },
    "readiness_explanation":          { "…": "…",       "trust_envelope": { … } },
    "upgrade_path_explanation":       { "…": "…",       "trust_envelope": { … } },
    "scenario_comparison_explanation":{ "…": "…",       "trust_envelope": { … } },
    "provenance_summary": {
      "source_objects": [ … ], "rule_keys": [ … ], "source_document_ids": [ … ],
      "missing_inputs": [ … ], "assumptions": [ … ], "confidence_level": "medium"
    }
  },
  "limitations": [
    "Advisory planning intelligence. Not engineering, permitting, utility, or pricing authority."
  ]
}
```

Per-block `trust_envelope`: `authority_layer`, `trust_zone`, `data_classification`, `confidence_level`, `missing_inputs`, `assumptions`, `scope_limitations`, `provenance_refs`. The scenario comparison block is included only when the design's home has scenarios.

### Block (d) upgrade_path_explanation — source and authorization

> Block (d) upgrade_path_explanation — source. The upgrade ladder
> (current → recommended → future-ready → constrained) is consumed directly from
> design_advisor_service.explain()["planning_state"] — a PlanningStateSnapshot already
> present in the public return of an approved composition method. The facade does NOT
> call the private _build_planning_state and does NOT re-derive the ladder from
> recommendation_profiles; re-derivation is rejected because it would create a second,
> drift-prone source of truth for the ladder and point provenance_refs at a
> non-canonical object. provenance_refs for this block reference the snapshot variants.
> The home-scoped dependency/readiness views (build_dependency_*,
> build_constraint_risk_reasoning_view) and the expansion score attach
> readiness/constraint context and feed confidence/missing-inputs only — they enrich the
> path, they do not originate it. The block is marked provisional when
> current_home_energy_architecture is missing or snapshot confidence_level is low, per
> the lineage downgrade rule.
>
> Exclusion revised. The prior exclusion of PlanningStateSnapshot was predicated on it
> being reachable only via the private _build_planning_state path. Verified false: the
> snapshot is public via explain(). The exclusion is narrowed to: the private
> _build_planning_state method is not called directly; the snapshot is consumed only as
> the public return of explain().

> Design-scoped authorization over home-scoped composition. The endpoint authorizes via
> can_access_design(design_id) and audits with object_type="design", object_id=design_id.
> Several composed readiness/dependency views are home-scoped and reached via the design's
> home_id. Design access is treated as implying access to the parent home's advisory views
> under the home-rooted access model; this is intentional and stated here rather than left
> implicit. Because the read reaches home-scoped reasoning, the audit event's
> provenance_refs MUST include the home_id and the home-scoped source-object refs actually
> touched — not only the design_id — so the audit record does not understate the scope of
> what was accessed.

## Trust And Provenance Requirements

- No LLM and no external call; purely deterministic in-process composition of existing rule and derived outputs.
- Every recommendation and constraint block must carry `provenance_refs`. If a contributing builder cannot expose lineage, downgrade `confidence_level` and mark the block provisional, per the lineage derivation rule.
- Keep the four fact classes distinct in the payload: user-entered (recorded facts via provenance source types), derived (scores and ranges), rule outputs (compatibility and profile rule keys), and advisory copy (authority layer advisory).
- The top-level `limitations` array must state non-authority explicitly; never imply engineering, permitting, utility, or pricing sign-off.

## Audit Requirements

- Audit every planner-intelligence read, including allowed and denied reads, as one event per call.
- Audit failure must not 500 an otherwise valid read. Wrap audit recording in a safe/degrading helper (for example `safe_record_audit(...)` or equivalent) so failed audit writes are logged but do not block the response. This pattern keeps a future move to async/queued auditing easy.
- Reuse the existing `audit_service` and the existing audit schema. No migration.
- Event fields: `action="planner_intelligence.read"`, `object_type="design"`, `object_id=design_id`, `source_surface="planner_intelligence"`, `decision` derived as today (allowed / denied / not_authenticated), and `provenance_refs` set to the returned source object references.
- Context minimization: store only ids, counts, decisions, source refs, and provenance refs in `event_context`. Do not store raw advisory text, recommendation copy, or sensitive derived claims.

## Migration Recommendation

None. Slice 1 introduces no schema changes and reuses the audit columns added in `20260625_0003`. No migration is to be created during this slice.

## Deferred Items

- Home-level and scenario-level planner-intelligence endpoints.
- Persisted or versioned planner-intelligence records.
- Frontend why/source panel and UI wiring (later UI-quality pass).
- External LLM integration and tool execution.
- Real-time web/program lookup.
- Utility territory intelligence.
- Contractor-specific workflows.
- Automated permit/AHJ logic.
- New audit query API or admin UI.
- Async/queued audit writing.
- Production runtime wiring, deploy, smoke, and push.

## Test Strategy

New `apps/api/tests/test_planner_intelligence.py` against the fast SQLite test DB (`tests/fast_db.py`):

- Auth: owner allowed; cross-account denied (403); unauthenticated mapped to 401/not_authenticated; unknown design 404.
- Audit: one event per successful read with correct `object_type`, `object_id`, `source_surface`, and `decision`; denial writes a denied event; a simulated audit write failure does not break the read; no sensitive context is stored.
- Trust/provenance: every block carries a trust envelope; blocks without lineage are downgraded or provisional; top-level `limitations` present; no authority-claim markers in copy (reuse the `planner_sandbox` authority-claim-marker check pattern).
- Composition correctness: payload values match the underlying services for seeded sample data, without re-deriving them in the test.

## Files Likely To Change (implementation, not this slice)

- New backend: `apps/api/app/planner_intelligence/__init__.py`, `router.py`, `schemas.py`; `apps/api/app/services/planner_intelligence.py`; `apps/api/tests/test_planner_intelligence.py`.
- Edited backend: `apps/api/app/main.py` (register router under `/api`); a small shared safe-audit helper (location to be confirmed at implementation time, reusing `app/security/audit.py`).
- No frontend changes in slice 1.

## Risks And Blockers

- Several existing `twin_planning_context` views rely on `HomeAccessMiddleware` rather than explicit per-object checks. The facade must perform its own `can_access_design` authorization and must not assume middleware coverage.
- `twin_planning_context.py` is ~14k lines. Composition must call only public builder methods; do not re-walk internals or refactor.
- Provenance lineage is not field-exhaustive, so some blocks will legitimately be provisional. This must remain visible, not hidden.
- Read-path auditing adds one write per call. Acceptable at slice-1 volume only because the write is wrapped to degrade gracefully; note for later batching/async.
- The legacy private planning-state snapshot path is off-limits in slice 1; if it appears necessary, stop and propose the smallest extraction first.

## Decisions (resolved with Matt, 2026-06-26)

- API shape: new `/api/planner-intelligence/...` module; do not extend `/design-advisor` or `/twin-planning-context`.
- Slice scope: design-scoped summary only; single endpoint `GET /api/planner-intelligence/designs/{design_id}/summary`.
- Audit depth: audit every read (allowed and denied) with graceful degradation; reuse existing audit schema and `audit_service`.
- Frontend: backend-only for slice 1; no UI panel yet.
- Docs: write this planning file before any code (this document).

## Non-Goals

- No LLM and no provider SDKs.
- No internal HTTP calls between services.
- No new reasoning math or domain rules.
- No persistence or versioning of planner-intelligence output.
- No migration or production DB change.
- No Railway runtime wiring, deploy, or smoke.
- No push.
- No use of the legacy private `_build_planning_state` / `PlanningStateSnapshot` path in slice 1.

## Suggested Commit Plan

- C0 (this step): `docs: plan planner intelligence first slice` — this docs-only file.
- C1: `feat: add planner intelligence read facade (backend)` — module, aggregator service, `main.py` registration.
- C2: `feat: enforce auth + safe audit on planner intelligence reads`.
- C3: `test: verify planner intelligence auth, audit, and provenance`.

No push. Branch remains `fix/github-workflow` unless directed otherwise. Stop after the docs-only change for this step.
