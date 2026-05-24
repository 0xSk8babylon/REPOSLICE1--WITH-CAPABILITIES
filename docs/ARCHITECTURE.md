# Architecture

## Monorepo Shape

- `apps/api`: FastAPI backend, persistence, rules/services, seed runtime
- `apps/web`: React/Vite frontend, live planning UI
- `docs`: product vision, architecture, continuity, handoffs

## Architectural Boundaries

- Property facts: homes, buildings, panels, loads
- Design facts: energy system designs, design equipment, scenarios, estimated pathways
- Product facts: equipment products and future ingestion metadata
- Rule outputs: compatibility issues and advisor explanations
- Estimate artifacts: takeoff requests and line items
- AI context: grounded summaries assembled from persisted structured state

## Persistence Architecture

- SQLAlchemy ORM models in `apps/api/app/core/models.py`
- Session and engine setup in `apps/api/app/core/database.py`
- Repository access in `apps/api/app/core/repository.py`
- SQLite local DB in `apps/api/data/residential_energy_planner.sqlite3`
- First-run seed loading in `apps/api/app/seed/runtime.py`

## Frontend Architecture

- Shared API client in `apps/web/src/lib/api.js`
- Query helpers in `apps/web/src/lib/useApiQuery.js`
- Mutation helpers in `apps/web/src/lib/useApiMutation.js`
- Workflow pages in `apps/web/src/pages/*`
- Lightweight shared form components in `apps/web/src/components/form/*`

## API Stability Policy

- Preserve current GET contracts unless frontend and docs change together.
- Prefer additive evolution.
- Prefer `/api/*` for clients.
- Reserve `/api/v1` for the first intentional breaking version boundary.

## Architectural Constraints

- Do not collapse structured facts, rules, calculations, and AI into one layer.
- Do not treat placeholder values as engineering truth.
- Do not introduce auth/billing-driven complexity before planning workflows are stable.
