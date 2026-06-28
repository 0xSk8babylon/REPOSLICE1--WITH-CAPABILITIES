# Lovable Reference Parity Protocol

Status: active reference protocol. Created during the guarded Lovable visual/card parity pass
(2026-06-27). This document is the authority for **how** future parity passes use the Lovable
screenshots — it does not grant the screenshots any implementation authority.

## 1. Stable reference path

Lovable screenshots live at:

```
~/TwinEnergy/references/lovable-references/
  home/                 home*                main Home / Energy Twin references
  explore/              explore*             main Explore / Goals / Learn references
  planner/              planner*             main Planner references
  builder/              builder*             main Builder references
  capabilities-unsorted/ capabilities-*      derived-view / "Product Objects" references (unsorted)
```

Originals remain in `~/Pictures/lovable-references/`. The reference set was copied (not moved),
filenames preserved, md5-verified. The folder's own `README.md` carries the per-file classification.

> The original brief spelled the path `reference` (singular). The canonical stable folder is
> `references` (plural). Use the plural path.

## 2. Authority order

1. **owner-workflows** — process / governance authority
2. **residential-energy-planner current code/contracts** — implementation authority
3. **heart-quill source repo** — source UI/template reference
4. **Lovable screenshots** — visual/card parity reference **evidence only**

Rules that follow from this order:

- Screenshots are **not a source of backend truth.**
- Screenshots **must not override owner-workflows or current repo contracts.**
- Do **not** overwrite the wired app with the Lovable mockup, and do **not** blindly copy mockup
  structure into implementation. The Lovable planner/home/builder mockups are intentionally richer
  than the current minimal object-view shell; richness in a screenshot is not a parity defect.

## 3. Screenshot classification rules

When a new screenshot is added, classify it before using it:

- **Main section reference** — filename `home*`, `explore*`, `planner*`, `builder*`. Visual intent
  for that primary section.
- **`capabilities-*` derived view** — unsorted. Classify the underlying object into one of:
  - Home / Energy Twin
  - Explore / Learn / Goals
  - Planner / Scenario / Sandbox
  - Builder / Readiness
  - Internal / Debug
  - Deferred / Legacy

## 4. `capabilities-*` unsorted derived-view rule

`capabilities-*` screenshots are the Lovable "Product Objects" view (each object + the backend
capabilities that back it). They are **classification references, not automatic main-UI cards.**

- Do **not** bulk-promote `capabilities-*` cards into main UI.
- Keep `/capabilities` and `/internal/capabilities` reachable as internal/debug visibility.
- Do **not** expose Capabilities in primary homeowner nav.

Current classification:

| File | Object | Classification |
| --- | --- | --- |
| `capabilities-energytwin1.png` | Energy Twin | Home / Energy Twin |
| `capabilities-explore1.png` | Learn | Explore / Learn / Goals |
| `capabilities-explore2.png` | Goals | Explore / Learn / Goals |
| `capabilities-planner1.png` | Scenario | Planner / Scenario / Sandbox |
| `capabilities-builder1.png` | Project | Builder / Readiness (contractor handoff portions → Deferred/Legacy) |

## 5. Planner draft-template protection rule

- The **2 backend templates** (`guided_backup_basics_v0`, `guided_solar_storage_sketch_v0`) are the
  **only finalized** templates.
- The **3 mock-only templates** are **unfinalized drafts**.
- Drafts must be **render-only** until explicitly finalized:
  - tagged `isDraft: true`, `source: "mock"`,
  - rendered with reduced opacity and a "Draft" badge,
  - selection disabled, with an early-return `isDraft` guard so a draft can never enter the real
    scenario path,
  - merged alongside the 2 live backend templates in `PlannerShellPage` **for display only**,
  - canvas overlay chips derived from the merged list so chips and cards match.
- Drafts must **not** be ported to `PlannerSandboxService._templates()`, must **not** create backend
  records, and must **not** be POSTed or validated.
- A template graduates to the backend only when explicitly finalized. **None are finalized in this
  pass.**

## 6. Home empty-Postgres rule

- Empty Postgres is **valid**. Do **not** seed Postgres by default to make the UI look full. Fix the
  UI branch, not the seed policy.
- A missing home (`404 /api/homes`) must render the **full Home shell plus** an additive onboarding
  prompt — never replace the shell with a single onboarding card:
  - Energy Twin intro/shell,
  - known facts / current status placeholders,
  - readiness / next-step placeholders already part of the shell,
  - a "Record address" onboarding prompt,
  - a clear note that calculations/data are unavailable until a home exists.
- Preserve `401`/access errors as access/unavailable warnings, **not** onboarding.

## 7. Catalog rule

- Keep `/catalog` reachable. Do **not** add Catalog to primary nav yet. Do **not** wire real product
  catalog persistence in this pass.

## 8. Parity table (2026-06-27 pass)

Reference = Lovable screenshot intent. Current = wired app at the time of the pass.
Data-source classes: **backend registry item**, **static shell/explainer card**, **real persisted
DB-backed data**, **internal/debug derived view**, **deferred/legacy**.

### `/` — Home / Energy Twin (`home1`, `home2`, `capabilities-energytwin1`)

| Reference card/view | Current | Status | Destination | Data source |
| --- | --- | --- | --- | --- |
| Energy Twin shell (intro + diagram) | Present | parity | Home | static shell |
| Known home facts | Present (fact table) | parity | Home | backend registry (`facts`) |
| Single-line diagram | Present (`HomeDiagram`) | parity | Home | static shell |
| Readiness snapshot | Partial (NEC load read) | parity-ish | Home | backend registry (`nec_load_calculation`) |
| Energy passport | Surfaced in Builder | deferred on Home | Builder | backend registry |
| Confidence & provenance | Present (fact basis) | parity | Home | backend registry (`provenance`) |
| Missing facts / constraint summary | Present (KPI + facts) | parity | Home | backend registry |
| Upgrade readiness | Partial | parity-ish | Home | backend registry |
| **Empty-state: full shell + "Record address"** | **Defect → single card** | **FIXED this pass** | Home | static shell + onboarding |

### `/explore` — Explore / Goals / Learn (`explore1`, `explore2`, `capabilities-explore*`)

| Reference card/view | Current | Status | Destination | Data source |
| --- | --- | --- | --- | --- |
| Goal cards (10 in mockup) | 6 goal cards | restored to 10 this pass | Explore | static shell (local-UI only) |
| Learn topic cards | Present (4) | parity | Explore | static shell / backend `source_documents` later |
| Product ingestion (CSV/JSON upload) | Absent | deferred | Explore (future) | deferred/legacy (no catalog persistence this pass) |

### `/planner` — Planner (`planner1`, `planner2`, `capabilities-planner1`)

| Reference card/view | Current | Status | Destination | Data source |
| --- | --- | --- | --- | --- |
| Guided template cards | 2 backend OR 5 static (chips mismatched cards) | restored: 2 live + 3 draft, chips derived from merged list | Planner | backend registry (2 live) + static draft (3) |
| Architecture columns / 20 patterns | Minimal pattern set | intentionally not rebuilt | — | deferred (do not copy mockup structure) |
| Sandbox drafts | Present | parity | Planner | static shell |
| Comparisons | Present | parity | Planner | static shell |

### `/builder` — Builder / Readiness (`builder*`, `capabilities-builder1`)

| Reference card/view | Current | Status | Destination | Data source |
| --- | --- | --- | --- | --- |
| Readiness lanes (estimate/product/program/passport) | Present | parity | Builder | backend registry |
| Contractor workflow / notes / proposal handoff | Absent | deferred (hard boundary) | — | deferred/legacy |
| CRM handoff / post-install / site photos | Absent | deferred (hard boundary) | — | deferred/legacy |

### `/capabilities`, `/internal/capabilities`

Reachable; internal/debug visibility only; not in primary nav. `capabilities-*` references map here
as classification evidence, not as promoted homeowner cards.

### `/catalog`

Reachable; static categories only; not in primary nav; no persistence wired.

## 9. What changed in the 2026-06-27 pass

Minimal, guarded fixes only:

1. Planner: merged 3 render-only draft templates with the 2 live backend templates; draft tagging,
   disabled selection, `isDraft` guard, chips derived from the merged list.
2. Home: 404 `/api/homes` now renders the full shell + additive onboarding prompt instead of
   replacing the shell.
3. Explore: restored the 4 missing static goal cards (local-UI only) to reach card parity.

No migrations, no new tables, no runtime seed changes, no auth changes, no save/load wiring, no
backend template promotion, no fake DB records.
