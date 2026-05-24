# Session Restore Template

## Purpose

Use this template at the start of a new ChatGPT/Codex session to quickly restore project context and reduce architectural drift.

## Step 1: Read These Files First

1. `AGENTS.md`
2. `docs/CURRENT_STATE.md`
3. `docs/NEXT_STEPS.md`
4. `docs/ACTIVE_TASKS.md`
5. `docs/SESSION_LOG.md`
6. `docs/session-continuity/project-state.md`
7. `docs/session-continuity/architecture-principles.md`
8. `docs/session-continuity/domain-map.md`
9. `docs/session-continuity/current-roadmap.md`
10. `docs/session-continuity/active-pressure-points.md`

If present, also read the latest file in `docs/handoffs/`.

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

## Step 4: Reconfirm Current Next Target

Default next implementation target unless the user redirects:

- extend provenance coverage across more entity fields and derived outputs, keep takeoffs transient until provenance is stronger, and preserve the planning-only boundary around completeness/advisor reasoning

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
