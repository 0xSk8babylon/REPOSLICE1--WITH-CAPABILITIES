# Planner Intelligence Slice 1 Closeout

## Summary

The first reasoning tools / planner intelligence slice is complete and committed
locally on `fix/github-workflow`. It adds a single design-scoped, authorized,
audited, provenance-backed read facade over existing deterministic reasoning
outputs. Verified booting in Python 3.11 + pydantic 2.13. Not pushed by owner
decision.

## Scope

- New backend module `apps/api/app/planner_intelligence/` (router + schemas)
- New aggregator service `apps/api/app/services/planner_intelligence.py`
- Single endpoint: `GET /api/planner-intelligence/designs/{design_id}/summary`
- Focused backend tests `apps/api/tests/test_planner_intelligence.py`
- Composition only: no new reasoning math, no LLM, no external calls, no
  persistence, no migration
- Upgrade ladder sourced from public `design_advisor_service.explain()["planning_state"]`;
  no private `_build_planning_state` call, no re-derivation
- Home-scoped `twin_planning_context` readiness/dependency views composed via the
  design's `home_id` as enrichment/context only

## Commits

- `d688988` docs: plan planner intelligence first slice (C0, docs-only plan +
  block-(d) source/authorization patch)
- `8a9930d` feat: planner intelligence read facade (slice 1, C1, backend facade)
- `7db4c6b` test: verify planner intelligence auth audit and provenance (C3,
  focused tests)

Stacked on prior local work: `5551ba9` feat: add frontend address onboarding flow.

## Verification

- Environment: ephemeral `python:3.11-slim` container (host has only Python 3.8 /
  pydantic 1, which cannot import project config; Docker is the established path)
- Boot: app imports; route mounted at `/api/planner-intelligence/designs/{design_id}/summary`
  (confirmed via `app.openapi()` since FastAPI >=0.138 uses lazy router inclusion)
- Endpoint: owner read assembles all six trust-enveloped blocks against seeded
  `design_001` / `home_001` (recommendations, constraints, readiness_explanation,
  upgrade_path_explanation, scenario_comparison_explanation, provenance_summary)
- Auth: owner read 200; cross-account read 403 (authenticated-forbidden, not 401)
- Audit: one `planner_intelligence.read` event per read (allowed and denied);
  `object_type=design`, `source_surface=planner_intelligence`; `provenance_refs`
  include `home_id`; event context holds ids/counts/decision/refs only, no raw
  advisory text; degrading `_safe_record_audit` keeps a failed audit write from
  500-ing a valid read
- Tests: `Ran 13 tests ... OK` (the logged `RuntimeError: simulated audit backend
  failure` is the intentional degrade-path test, which passes)
- No production code changed by the tests; the only test fix was test-internal
  (capture the facade's first `explain` call; static source check for the private
  builder)

## Boundaries Preserved

- Push: no (owner declined GitHub push for now)
- Deploy: no
- Migration: no (none created; production migration must remain not-rerun)
- Production DB: not touched (any production DB work is verification-only)
- Production commands: none run
- Remotes changed: no
- Force push: no
- LLM / external API / secrets added: no
- UI: no (frontend deferred to a later UI-quality pass)

## Production / Runtime Status

- Production runtime credential verification - PASS:
  - 1Password `op run` resolved production `DATABASE_URL`.
  - `DATABASE_URL` was not printed.
  - Read-only `select 1` passed.
  - No production write occurred.
  - No migration, Alembic command, seed, deploy, push, or production mutation
    occurred.
- Production DB verification-only closeout - PASS:
  - Alembic version observed: `20260523_0001`.
  - Public base table count: 26.
  - Baseline row counts matched:
    - accounts: 1
    - homes: 1
    - source_documents: 5
    - data_provenance: 7
    - rule_provenance: 25
    - equipment_products: 8
    - energy_system_designs: 2
    - scenarios: 2
  - audit_events observed: 0 at verification time.
  - Foreign key constraints: 27.
  - Unvalidated foreign keys: 0.
  - FK orphan checks: all 0.
  - Schema note: scenarios use `home_id` and `linked_design_id`; do not assume
    `scenarios.design_id`.
  - PG-8E must not be rerun. Production is populated and verified; future work is
    verification/operation only unless explicitly approved.
- Local `.env` contains no `DATABASE_URL`, so no stale local DB credential can be
  picked up by the runtime path; `apps/api/app/core/config.py` reads `DATABASE_URL`
  from env only (no hardcoded fallback).
- Production DB appears already populated; the PG-8E migration must NOT be rerun.
  Any production DB activity is verification-only.

## Repo State

- Branch: `fix/github-workflow`
- Status: clean, local-only
- Ahead of origin by: 63
- Remote note: `origin` (`0xSk8babylon/resi-twin`) is stale/deleted on GitHub
  (`Repository not found`); the local `origin/fix/github-workflow` tracking ref is
  stale. No remote was changed.

## Next Safe Step

Keep the completed slice local on `fix/github-workflow`. A GitHub push is deferred
by owner decision; revisit only when the owner repoints `origin` to a valid
repository or explicitly approves a target. Production is populated and verified;
PG-8E must not be rerun. Future production work is verification/operation only
unless explicitly approved.
