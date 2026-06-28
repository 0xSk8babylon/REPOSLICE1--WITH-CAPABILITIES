# Lovable Reference Parity Closeout

## Summary

Stabilized the Lovable screenshot reference set into a documented, authority-bounded
folder and ran a guarded visual/card parity pass against the database-wired shell.
Only minimal, additive, frontend-safe fixes were applied. No backend, persistence,
seed, auth, migration, or dependency changes. Not committed; not pushed (owner review
pending).

## Authority model (recorded, unchanged ordering)

1. owner-workflows — process/governance authority
2. residential-energy-planner current code/contracts — implementation authority
3. heart-quill source repo — source UI/template reference
4. Lovable screenshots — visual/card parity reference evidence only (not backend truth;
   must not override owner-workflows or current repo contracts)

## Reference folder stabilization

- Stable path: `~/TwinEnergy/references/lovable-references/` (plural `references`).
  The brief named the singular `reference`; the canonical pre-existing folder is plural,
  so the plural path is authoritative to avoid a near-duplicate.
- Copied (not moved) from `~/Pictures/lovable-references/`; 15 files; filenames preserved;
  md5-verified against originals; originals untouched.
- Subfolders: `home/`, `explore/`, `planner/`, `builder/`, `capabilities-unsorted/`.
- `capabilities-*` are the Lovable "Product Objects" derived-view set; classified as
  classification references only (not promoted to homeowner UI):
  energytwin1→Home, explore1→Learn, explore2→Goals, planner1→Scenario,
  builder1→Project (contractor/CRM/post-install portions → Deferred/Legacy).
- Folder manifest written at `~/TwinEnergy/references/lovable-references/README.md`.

## Scope of code changes (frontend only)

- `apps/web/src/lib/heartQuillMockData.js`
  - Split the 5 mock templates into 2 live-fallback (`ac-solar`, `ac-partial`) and
    3 render-only drafts (`dc-tou`, `hy-whole`, `off-gen`) tagged `isDraft:true`,
    `source:"mock"`.
  - Added overlay entries for the 2 live backend template IDs plus a fallback overlay.
  - Restored 4 missing static Explore goal cards (10 total): partial off-grid,
    full off-grid, resale value, reduce emissions (local-UI only).
- `apps/web/src/pages/HeartQuillShellPage.jsx`
  - Planner: merged 2 live backend templates with the 3 mock drafts for display only;
    `toTemplateCard` tags live items `isDraft:false, source:"backend"`; canvas chips
    derived from the merged list; `selectTemplate()` early-returns on `isDraft`; draft
    chips disabled; "2 live · 3 draft" status badge; drafts have no seed action.
  - Home: removed the substitutive empty-state early return. A `404 /api/homes` now
    renders the full Energy Twin shell plus an additive `HomeOnboardingNotice`
    ("Record address" + unavailability note). 401/other errors still surface as the
    access-warning strip (unchanged).
- `apps/web/src/styles/heartQuillShell.css`
  - `.hq-card-draft`, `.hq-overlay-choice-draft` (reduced opacity, dashed), and
    `.hq-onboarding-notice` styles.

## Planner draft protection (confirmed at runtime)

- Backend `PlannerSandboxService._templates()` unchanged — still returns exactly the 2
  finalized templates (`guided_backup_basics_v0`, `guided_solar_storage_sketch_v0`).
- Drafts are render-only: not ported to backend, no backend records, never POSTed or
  validated, cannot enter the scenario path (guarded), selection disabled.
- None of the 3 drafts were finalized in this pass.

## Home empty-Postgres rule (confirmed)

- Empty Postgres remains valid; no default seeding; UI branch fixed, not seed policy.
- Onboarding is additive, not substitutive; calculations/data labeled unavailable until
  a home exists.

## Docs updated

- Added `docs/lovable-reference-parity.md` (protocol + parity table).
- Appended parity sections to `PROJECT_STATE.md`, `discovery-index.md`,
  `docs/UI_REGISTRY.md`.
- Closeout: `docs/CURRENT_STATE.md`, `docs/NEXT_STEPS.md`, `docs/ACTIVE_TASKS.md`,
  `docs/SESSION_LOG.md`, `docs/session-continuity/{project-state,current-roadmap}.md`,
  and this dated handoff.
- NOTE: `SESSION_HANDOFF.md` is `.gitignore`d (repo line 18); its appended parity note
  lives on disk only and is not git-tracked. This dated handoff is the tracked record.

## Verification

- Frontend build: `npm run build` in `apps/web` — passed (59 modules).
- Backend tests: `test_planner_sandbox.py`, `test_address_onboarding.py`,
  `test_system_visibility.py` — 23 passed (pre-existing Pydantic v2 `.dict()`
  deprecation warnings only).
- `git diff --check` — clean.
- Routes reachable: `/`, `/explore`, `/planner`, `/builder`, `/capabilities`,
  `/internal/capabilities`, `/catalog`.
- Visual confirmation: headless Firefox screenshots of `/`, `/planner`, `/explore`
  against a scratchpad mock API (the live `:8000` backend has a pre-existing audit-table
  schema 500 — `audit_events` missing `actor_user_id` — unrelated to this pass).
  Confirmed: additive Home onboarding; Planner 2 live + 3 disabled drafts with matching
  chips; Explore 10 goal cards.

## Not done / open

- Pre-existing `:8000` audit-schema 500 (`audit_events.actor_user_id`) — out of scope,
  not touched. Flag for a separate fix if a live-backend demo is needed.
- Builder/Capabilities/Catalog left as-is (reachable, off primary nav). Contractor
  handoff / CRM / post-install cards remain deferred by hard boundary.
- Explore "Product ingestion" (CSV/JSON upload) deferred (no catalog persistence /
  external services this pass).

## Next action

Owner review of the uncommitted diff and `docs/lovable-reference-parity.md`. On
approval, commit on a branch (nothing committed or pushed yet).
