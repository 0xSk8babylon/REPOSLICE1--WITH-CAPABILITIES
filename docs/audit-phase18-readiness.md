# Phase 18 Readiness Audit — Architecture Review for the Reasoning Layer

**Date:** 2026-06-11
**Scope:** Read-only audit of `apps/api` ahead of building `engines/` (deterministic calculation engines) and a planning orchestrator on top of phases 1–15.
**Method:** Static import-graph analysis, model review, service-layer reading, seed-system review, full local test run.

---

## Fixes Applied (2026-06-11, post-audit)

All blocking findings below were addressed in seven commits on `fix/github-workflow`; the codebase is now ready for Phase 18 engine development. Suite: **225 tests passing in ~3.5 minutes** (was 23 minutes).

1. **Boundary violation fixed** — `core/repository.py` no longer imports `scenarios.schemas` or `services.scenario_revision`; scenario serialization lives in `scenarios/router.py`. Core imports nothing above itself.
2. **Trust vocabulary consolidated** — `FactLifecycleState` (core/types.py) is the canonical 10-state lifecycle enum (`demo_seed, placeholder, claimed, user_created, derived_estimate, imported, photo_verified, contractor_verified, verified, expired`); `DataOrigin` is a compatibility alias; `trust_state` is explicitly typed; `VERIFICATION_STATUS_TO_LIFECYCLE` crosswalks the document axis. All 37 lifecycle string-literal sites in logic code now reference the enum (the audit's "~125" estimate included prose and field names).
3. **New lifecycle states classify explicitly** — `_classify_record` maps `photo_verified`/`contractor_verified` → `source_backed_fact` and `expired` → `unknown` (no more silent fall-through to `recorded_fact`).
4. **Twin performance pathology fixed** — `_metadata_paths` (44.7M calls/test) now runs against an `lru_cache`'d frozen-payload walker with bit-identical output, and contractor-context builders accept pre-built views instead of rebuilding (28×→1× per takeoff view). Single takeoff build: 60.6s → 2.3s.
5. **Test suite rebuilt for speed** — in-memory SQLite with snapshot-restore reseeds (`tests/fast_db.py`); per-reset cost 0.1ms.
6. **Golden-home contamination guard** — `_backfill_global_rule_provenance_rows` is skipped when `GOLDEN_HOME_TEST=true`.
7. **Engines package started** — `app/engines/resilience/calc.py` holds the pure battery/solar sizing math and coefficient tables (no DB, no prose, no service imports); `resilience_recommendation.py` delegates to it.

Remaining known items for Phase 18 (non-blocking): the phase 9–15 deferred-import web still exists (fence engines away from it), Alembic vs `create_all()` schema authority is undecided, `ScenarioRevision.planning_state_snapshot` JSON has no schema version, and phase 1–8 primitives still lack direct tests (golden homes are the planned vehicle).

---

## (a) Verdict: **Build after specific fixes**

The foundation is better than average for a project this size — thin routers, a repository layer, stateless deterministic services, typed enums, real regression tests for phases 9–15, and CI that runs them. You do **not** need to restructure first.

But three things will directly hurt a new `engines/` package if you start today:

1. The numeric calculations you want to make "deterministic engines" are currently **interleaved with explanation prose** inside `resilience_recommendation.py` (3,042 lines), not isolated.
2. The phase 9–15 service layer is a **circular dependency web held together by ~30 function-local deferred imports**. Anything that imports `twin_planning_context` (14,269 lines) pulls in the whole web.
3. The planning **primitives the engines will sit on (phases 1–8) have zero direct tests** — all 225 existing tests target phases 9–15.

Fix the short list in section (c) first (roughly: extract pure math, pin down the trust vocabulary, add primitive tests, keep engines out of the import web). None of it is a restructure; it's mostly extraction and fencing.

---

## 1. Module Boundaries

### Layout

Three layers, mostly clean:

```
app/<domain>/router.py + schemas.py   (24 thin HTTP modules)
        │ imports
        ▼
app/services/<name>.py                (27 flat service modules, singleton instances)
        │ imports
        ▼
app/core/{models, repository, database, config, types, schemas}
```

### What's good

- **Routers are uniformly thin.** Every router delegates to a service or `repository`. No calculations live in route handlers. The heaviest router logic is cross-entity referential validation in `designs/router.py:44-80` (product/location existence + home-ownership checks) — acceptable, but it belongs in the repository/service layer once engines create designs programmatically.
- **Phase 1–8 services form a clean DAG:** `design_analysis` is the shared base; `compatibility`, `design_completeness`, `backup_capability`, `expansion_readiness`, `install_complexity` sit on it; `design_advisor` and `ai_context` aggregate. No cycles, top-level imports only.
- No service imports a router. No router imports another router.

### What's broken

- **Circular service dependencies (phases 9–15), masked by deferred imports.** These pairs/groups are mutually dependent, with the cycle "broken" only by function-local imports:
  - `twin_planning_context` ↔ `contractor_context` ↔ `planning_exchange` (`twin_planning_context.py:12091`, `contractor_context.py:13`, `planning_exchange.py:4-5`)
  - `contractor_workflow` ↔ {`contractor_context`, `estimate_readiness`, `planning_exchange`, `proposal_option_sets`, `twin_planning_context`} (`contractor_workflow.py:443-447`)
  - `energy_passport` → 6 services including `contractor_workflow` (`energy_passport.py:390-395`)
  - `post_install` ↔ `crm_handoff` (`post_install.py:197`, `crm_handoff.py:128`)
  - `product_preferences` ↔ `estimate_readiness` ↔ `proposal_option_sets` (`product_preferences.py:553-555`, `proposal_option_sets.py:428-430`)

  These are real architectural cycles. They work at runtime, but they mean there is no safe "import just the part I need" entry point into the phase 9–15 layer.

- **Layering inversion in core.** `core/repository.py:7` imports `app.scenarios.schemas`, and `core/repository.py:19` defer-imports `app.services.scenario_revision` so that `_serialize_scenario` can embed revision overviews. The core data-access layer reaches *up* into the feature layer and mixes persistence with presentation. This is the single worst boundary violation in the codebase.

- **God modules.** `services/twin_planning_context.py` is **14,269 lines / 198 methods** — roughly 54% of the entire service layer by volume. `resilience_recommendation.py` is 3,042 lines; `system_visibility.py` (uncommitted) is 1,370.

- **Internals-reaching:** services freely import other domains' Pydantic schemas (e.g., `contractor_context.py` imports `twin_planning_context.schemas`). In practice schemas *are* the public interface here, so this is tolerable — but nothing enforces it, and there is no `__all__`/interface convention distinguishing public from private service methods (the 198 `_`-prefixed methods in twin context are at least consistently underscored).

- **Import-time side effects.** `core/database.py:11-17` creates the engine and the data directory at import; `core/config.py:25` freezes settings at import. Tests only work because they set `DATA_DIR`/`DATABASE_FILE` env vars *before* the first `app.*` import (see `tests/test_resilience_recommendation.py:5-6`). Your engines test harness will inherit this import-order trap.

## 2. Test Coverage

### What exists

225 tests in 11 files, all `unittest`-style, run by CI (`.github/workflows/ci.yml`, Python 3.11, `unittest discover`):

| Test file | Tests | Covers |
|---|---|---|
| test_twin_planning_context.py | 155 | Phase 9–10 twin context, AI grounding, topology, advisory views |
| test_system_visibility.py | 9 | Phase 16/17 (uncommitted work on this branch) |
| test_resilience_recommendation.py | 8 | Resilience profiles + battery/solar sizing via `design_advisor` |
| test_contractor_workflow.py | 8 | Phase 11 |
| test_product_preferences.py | 8 | Phase 12 |
| test_proposal_option_sets.py | 8 | Phase 12 |
| test_estimate_readiness.py | 7 | Phase 11 |
| test_energy_passport.py | 7 | Phase 14 |
| test_phase13_post_install_crm.py | 6 | Phase 13 |
| test_program_intelligence.py | 6 | Phase 15 |
| test_scenario_revisions.py | 3 | Scenario revision lineage |

The tests are good: golden-style regression assertions against the demo seed with exact expected values (e.g., `coverage_ratio == 0.67`, specific rule keys, specific prose fragments). This is exactly the precedent you want for golden homes.

### What's missing — the part engines will sit on

**Zero direct tests** for any phase 1–8 primitive:

- `services/load_calculation.py` — the only "calculation service" (17 lines)
- `services/compatibility.py` — the rule engine
- `services/design_analysis.py` — the shared analysis context every service consumes
- `services/design_completeness.py`, `scenario_comparison.py`, `takeoff_generation.py`, `provenance.py`, `ai_context.py`
- `core/repository.py`, the seed system, and every router (no HTTP-level tests at all — no `TestClient` usage anywhere)

`design_advisor` gets meaningful *indirect* coverage through the resilience tests; everything else in the engines' future substrate is untested.

### Test run result

Suite executed locally via `PYTHONPATH=.vendor python3 -m unittest discover -s tests` (Python 3.8):

> **Result: ✅ Ran 225 tests in 1400.9s (23.3 minutes) — all passed (OK), exit code 0.**

**Operational findings from running it:**

- `pytest` is **not in `requirements.txt` and not installed** in `.venv` or `.vendor`; the suite only runs under `unittest`. CI does the same, so this is consistent — but undocumented.
- The suite is **extremely slow**: every test method calls `reset_and_reseed()` in `setUp`, which deletes the SQLite file, recreates all tables, reseeds the full demo dataset, and regenerates scenario revisions — averaging ~6.2s per test, 23+ minutes total locally. This will be a real drag on engine development iteration speed.
- Module-level `os.environ.setdefault("DATABASE_FILE", ...)` in each test file means that when the whole suite runs in one process, the **first imported module's DB filename wins** for everything — harmless today because every test reseeds, but it's a latent isolation trap.
- Local Python is 3.8 while CI is 3.11 — both currently pass, but the skew is worth closing before adding an engines package.

## 3. Data Models

### The good news: adding lifecycle states is cheap at the schema level

- Every status/origin column (`data_origin`, `verification_status`, `trust_state`, `lifecycle_stage`, `status`) is a plain `String` — **no DB-level enums, no CHECK constraints**. Adding `photo_verified`, `contractor_verified`, `expired` requires *no column migration at all*; only the Python `Enum` in `core/types.py:135-160` needs new members.
- `DataProvenance.verified_at` **already exists** (`core/models.py:401`). Adding `verified_at` to `SourceDocument` or any domain table is a single additive Alembic migration (nullable DateTime), which SQLite handles trivially.
- The models themselves are well-normalized and loosely coupled. `SourceDocument` has no back-references; `DataProvenance` and `RuleProvenance` link to it via nullable FKs and use generic `(entity_type, entity_id)` addressing — nothing structurally resists migration.

### The bad news: the *vocabulary*, not the schema, is the migration hazard

1. **Three overlapping trust vocabularies with no single owner:**
   - `data_origin` (badge: `demo_seed`/`user_created`/`imported`/`verified`/`derived_estimate`/`placeholder`)
   - `SourceDocument.verification_status` (`unverified`/`user_entered`/`imported`/`manufacturer_verified`/`deprecated`)
   - `DataProvenance.trust_state` — which is **typed as `DataOrigin`** in `provenance/schemas.py:61`, silently fusing two vocabularies the README insists are distinct.

   Before adding `photo_verified`/`contractor_verified`/`expired` you must decide which vocabulary each belongs to. `verified` already exists in `DataOrigin` and `manufacturer_verified` in `VerificationStatus` — the new states straddle both. If `photo_verified` goes into `DataOrigin`, it leaks into `trust_state` everywhere via that schema coupling.

2. **~125 hardcoded origin-literal usages** scattered across the service layer (string comparisons, badge formatting, set membership like `trust_state in {"placeholder", "demo_seed", "derived_estimate"}` in `ai_context.py:184`). New states won't break anything loudly — they'll silently fall through every one of these comparisons. That's worse than a migration error.

3. **JSON snapshots freeze the old vocabulary.** `ScenarioRevision.planning_state_snapshot` (JSON) and `DataProvenance.value_snapshot` embed origin/trust values with no snapshot schema version. Historical revisions will contain pre-expansion vocabulary forever; any engine reading old snapshots must tolerate unknown states.

4. **Schema management is ambiguous.** Tables are created by `Base.metadata.create_all()` on startup, while Alembic has exactly one migration (`20260523_0001_phase2a_hardening.py`). Two sources of schema truth = drift risk the moment engines add tables. Pick one path (Alembic) before phase 18 adds models.

5. **Aging stack note:** Pydantic is pinned `<2.0`, local Python is 3.8, models use `datetime.utcnow` (deprecated), and `app.main` uses deprecated `@app.on_event("startup")`. None of this blocks phase 18, but a new engines package will lock in Pydantic v1 idioms — decide deliberately whether that's acceptable.

## 4. Service Layer — README claim vs. reality

README claims "service boundaries for rules, calculations, explanations, and AI context." Reality, boundary by boundary:

| Claimed boundary | Verdict | Evidence |
|---|---|---|
| **Calculations** | ❌ Not a real boundary | `load_calculation.py` is 17 lines (two sums). The *actual* math — battery sizing, autonomy windows, reserve/growth margins, backup-energy kWh, coverage ratios, solar recovery factors — lives inside `resilience_recommendation.py` (e.g., lines 540, 619–626, 2062–2090, 2216–2219), interleaved in the same methods with scope-note prose and confidence narration. Scenario scores (`backup_capability_score`, etc.) are *stored placeholder columns*, not computed values. |
| **Rules** | ⚠️ Half-true | `compatibility.py` is genuinely rule-based evaluation over `design_analysis`, and rule keys are tracked in `RuleProvenance`. But each rule constructs its explanation prose (`issue`/`why_it_matters`/`tradeoff`) inline at fire time — rule logic and rule copywriting are one thing. |
| **Explanations** | ❌ Not a layer | Explanation text is generated in *every* service (f-strings in resilience, STATUS_EXPLANATIONS in `design_analysis.py:4-13`, scope notes in twin context). There is no separation between "what is true" and "how we say it." |
| **AI context** | ✅ Genuine boundary | `ai_context.py` is a pure aggregator: it computes nothing, only assembles grounded views with provenance and explicit limitations. This is the cleanest module in the service layer — and the model for what engine *output adapters* should look like. Note `twin_planning_context` has grown a parallel, much larger AI-grounding view that partially supersedes it. |

**The redeeming quality:** every service is a stateless singleton computing pure functions of `(db, id)` — no caching, no mutable state, no I/O beyond the session. The math in `resilience_recommendation` is already deterministic, coefficient-table-driven (`AUTONOMY_HOUR_RANGES`, `RESERVE_MARGIN_FACTORS`, `GROWTH_MARGIN_FACTORS` as class constants), and *extractable*. The engines refactor is an extraction job, not a rewrite.

## 5. Seed System

### How it works

- `seed/sample_data.py` (954 lines): one hardcoded demo dataset as module constants (`SAMPLE_HOME`, `SAMPLE_LOADS`, …).
- `seed/runtime.py`: `seed_database(db, force)` inserts the constants iff **no Home row exists**; `reset_and_reseed()` deletes the entire SQLite file and reseeds; two backfill functions patch provenance rows into existing DBs.
- DB location is controlled by `DATA_DIR`/`DATABASE_FILE` env vars (`core/config.py`) — this is how the existing tests get isolated databases.

### Can you build golden homes without modifying the framework? **Yes — by going around it, not through it.**

- **Viable today, zero framework changes:** a new `tests/fixtures/golden_homes.py` (or `seed/golden.py` — a new file is not a framework modification) that sets the env vars, calls `init_database()`, and inserts curated `models.*` rows directly. This is exactly the pattern your own tests already prove out, and the resilience tests already demonstrate "known-correct expected output" assertions against seeded data.
- **Not viable:** extending `seed_database` itself — it has no dataset registry, no parametrization, and its idempotence check is "does any home exist," so it cannot host multiple named datasets.

### Two gotchas to design around (flagging, not fixing)

1. **Startup contamination:** `app/main.py` runs `initialize_and_seed` on startup, and `_backfill_global_rule_provenance_rows` (`runtime.py:69`) runs against **any** existing database unconditionally — it will inject demo `SourceDocument` and `RuleProvenance` rows into a golden-home DB the moment the app serves it. `ensure_revisions_for_existing_scenarios` likewise touches any scenarios it finds. Golden fixtures used only inside tests (never served via app startup) are safe; golden homes you want to *browse in the app* are not, without a guard.
2. **Demo-seed coupling of expected values:** 225 existing tests assert exact outputs derived from `sample_data.py`. Golden homes should define their *own* curated inputs and expectations rather than referencing demo entities, or every demo-data tweak breaks both suites.

---

## (b) Top 5 Risks, Ranked by Pain to a New `engines/` Package

### 1. Calculation logic is fused with explanation prose (highest pain)
`resilience_recommendation.py` holds the real deterministic math, inline with narrative generation. A new engine must either (a) re-implement the math — guaranteeing drift between engine numbers and advisor numbers — or (b) import the 3k-line module and inherit everything attached to it. Extract the pure functions (sizing, coverage, energy-need math + coefficient tables) into a dependency-free module *first*; the engines package then becomes its primary consumer, and the advisor becomes a formatter over engine outputs.

### 2. The phase 9–15 circular-import web, anchored by a 14k-line god module
The orchestrator will be most tempted to call `twin_planning_context`, `contractor_workflow`, `estimate_readiness` — exactly the modules that are mutually entangled via deferred imports. One careless top-level import from `engines/` into this web (or from the web into `engines/`) and the new package joins the cycle. Rule to enforce from day one: **engines import only `core.*` and extracted pure-calculation modules; never `app/services/*` from phases 9–15.** The web itself doesn't need untangling for phase 18 — it needs a fence.

### 3. Trust/lifecycle vocabulary fragmentation
Three overlapping state vocabularies, `trust_state` typed as `DataOrigin`, ~125 scattered string-literal comparisons, and versionless JSON snapshots. The schema change for `photo_verified`/`contractor_verified`/`expired` + `verified_at` is a one-day job; the *semantic* change silently falls through every hardcoded comparison. Engines that branch on trust states (and a verification lifecycle certainly will) need one canonical enum module and a "unknown state = lowest trust" defensive default before the new states ship.

### 4. No tests under the engines' feet, and a 30+-minute suite
The primitives engines will consume — `design_analysis`, `load_calculation`, `compatibility`, `provenance` — have zero direct tests, so engine development gets no regression signal when it touches them. Meanwhile the per-test file-delete-and-reseed pattern makes the existing suite slow enough that people will stop running it locally. Golden homes (risk-free to add, per section 5) plus session-scoped or in-memory seeding solve both.

### 5. Import-time side effects and dual schema management
Engine creation and settings freeze at import; test isolation depends on env-var ordering; `create_all()` and Alembic both claim schema authority with only one migration written. Engines packages typically want notebook/CLI/worker entry points — each one will trip over import-order configuration, and the first engine-owned table forces the Alembic-vs-create_all decision anyway. Cheap to fix now (lazy engine/session factory, declare Alembic authoritative), annoying forever if deferred.

---

## (c) Specific Files Needing Attention Before You Start

**Must touch (blocking-ish):**

| File | Why | Action shape |
|---|---|---|
| `app/services/resilience_recommendation.py` | All real math lives here, fused with prose | Extract pure calculation functions + coefficient tables into a dependency-free module engines can import |
| `app/core/types.py` | `DataOrigin`/`VerificationStatus` must absorb the new lifecycle states coherently | Decide the single vocabulary (or explicit mapping) for `photo_verified`/`contractor_verified`/`expired` before any engine branches on trust |
| `app/provenance/schemas.py:61` | `trust_state: DataOrigin` fuses two vocabularies | Give `trust_state` its own enum (additive, non-breaking) |
| `app/core/repository.py` | Core layer imports `scenarios.schemas` + `services.scenario_revision` upward; `_serialize_scenario` mixes persistence with presentation | Move serialization out of the repository so engines can depend on core cleanly |
| `apps/api/requirements.txt` | No test runner declared | Add the test dependency story (pytest or document unittest-only) |

**Should touch (high leverage, not blocking):**

| File | Why |
|---|---|
| `app/services/twin_planning_context.py` | 14,269 lines; don't split it now, but **freeze it** — no engine imports, no new responsibilities added to it during phase 18 |
| `app/seed/runtime.py` | `_backfill_global_rule_provenance_rows` contaminates any non-demo DB on app startup — guard it (e.g., demo-dataset check like the entity backfill already has) before golden homes are ever served through the app |
| `tests/` (suite-wide) | Per-test `reset_and_reseed` file deletion → tens of minutes; switch to session-scoped seed or in-memory SQLite before adding engine test volume |
| `app/core/database.py` / `config.py` | Import-time engine/settings creation; engines' CLI/worker entry points will want a lazy factory |
| `migrations/` | One migration vs. `create_all()` on startup — declare Alembic authoritative before engines add tables |
| `app/services/contractor_workflow.py`, `energy_passport.py`, `product_preferences.py`, `proposal_option_sets.py`, `estimate_readiness.py`, `post_install.py`, `crm_handoff.py` | The deferred-import cycle web — document it and fence engines away from it; untangle opportunistically, not as a phase 18 prerequisite |

**No action needed (verified healthy):** all routers (thin), `core/models.py` (clean, additive-migration-friendly), `app/services/ai_context.py` (the pattern engines' output adapters should copy), seed usage for test fixtures via env-var isolation.

---

*Audit performed read-only; no code was modified. Uncommitted phase 16/17 work (`system_visibility`, `uiRegistry`, ArchitecturePage) was present on branch `fix/github-workflow` during the audit and is reflected in file counts but was not separately reviewed.*
