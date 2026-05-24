# Session Restore Template

## Purpose

Use this template at the start of a new ChatGPT/Codex session to quickly restore project context and reduce architectural drift.

## Step 1: Read These Files First

1. `AGENTS.md`
2. `docs/PROJECT_OVERVIEW.md`
3. `docs/CURRENT_STATE.md`
4. `docs/NEXT_STEPS.md`
5. `docs/ACTIVE_TASKS.md`
6. `docs/SESSION_LOG.md`
7. `docs/session-continuity/project-state.md`
8. `docs/session-continuity/architecture-principles.md`
9. `docs/session-continuity/domain-map.md`
10. `docs/session-continuity/current-roadmap.md`
11. `docs/session-continuity/active-pressure-points.md`
12. `docs/philosophy/CORE_PHILOSOPHY.md`
13. `docs/philosophy/MENTAL_MODELS.md`
14. `docs/philosophy/NON_GOALS.md`
15. `docs/philosophy/AI_PHILOSOPHY.md`
16. `docs/philosophy/TRUST_AND_PROVENANCE_PHILOSOPHY.md`
17. `docs/philosophy/SYSTEM_BOUNDARIES.md`
18. `docs/philosophy/UX_PRINCIPLES.md`
19. `docs/adr/README.md`

If present, also read the latest file in `docs/handoffs/` and any ADRs relevant to the planned change.

## Step 2: Reconfirm The Live Entry Points

Backend:

- `apps/api/app/main.py`
- `apps/api/app/core/database.py`
- `apps/api/app/core/models.py`
- `apps/api/app/core/repository.py`
- `apps/api/app/seed/runtime.py`

Frontend:

- `apps/web/src/lib/api.js`
- `apps/web/src/app/App.jsx`
- `apps/web/src/pages/*`

## Step 3: Reconfirm What Must Stay Stable

- Existing frontend GET routes should remain compatible unless explicitly changing the frontend too.
- `/api/*` is the preferred route base for future clients, but legacy unprefixed routes still exist.
- AI must remain grounded in structured persisted state.
- Placeholder product facts, scores, and takeoff logic must not be documented as authoritative.
- Ownership scaffolding exists, but auth and billing do not.
- `data_origin` must be respected when distinguishing demo records from future user/imported/verified data.
- Doctrine and ADR files are strategic constraints, not optional commentary.

## Step 4: Reconfirm Current Next Target

Default next implementation target unless the user redirects:

- extend provenance coverage across more entity fields and derived outputs, keep takeoffs transient until provenance is stronger, and preserve the planning-only boundary around completeness/advisor reasoning
- preserve the doctrine layer while doing so: structured data decides, trust visibility precedes stronger claims, and planning guidance must not drift into engineering authority

## Step 5: Reconfirm Verification Expectations

When backend changes are made:

- run `python3 -m compileall app`
- run a backend smoke/import check if dependencies are available

When frontend changes are made:

- run `npm run build`

## Step 6: Restore Session Summary Format

At the end of the session, summarize:

- what changed
- whether architecture changed
- whether API contracts changed
- what still remains placeholder
- what the next recommended step is
- whether continuity docs must be updated

## Step 7: Drift Questions

Before making major changes, ask:

- Does this preserve structured-facts-first architecture?
- Does this keep read contracts stable where required?
- Does this introduce silent authority where only placeholders exist?
- Does this require continuity doc updates?
- Does this violate any philosophy or ADR file that should constrain the change?
