# Residential Energy Planner

Initial scaffold for a residential energy infrastructure planning platform. This repository is intentionally structured around durable house data, structured product facts, rule-based compatibility logic, and explanation layers that AI can consume without becoming the source of truth.

## Monorepo Layout

- `apps/api`: FastAPI backend with modular domain folders
- `apps/web`: React/Vite frontend shell
- `docs`: product, architecture, and roadmap documentation

## Product Direction

This is not a final engineering, permitting, or NEC-compliance tool. The current scaffold establishes:

- persistent home and design domain models
- structured product library placeholders
- service boundaries for rules, calculations, explanations, and AI context
- a frontend shell for evolving into a multi-workflow planning application

## Quick Start

### Backend

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

If `python3 -m venv` is unavailable on your machine, install the platform `python3-venv` package first or use a project-local fallback:

```bash
cd apps/api
python3 -m pip install --target .vendor -r requirements.txt
PYTHONPATH=.vendor uvicorn app.main:app --reload
```

### Frontend

```bash
cd apps/web
npm install
echo "VITE_API_BASE_URL=http://localhost:8000" > .env.local
npm run dev
```

If `.env.local` is omitted, the frontend defaults to `http://localhost:8000`.

## Lint

```bash
# Python (from apps/api/)
ruff check .

# JavaScript (from apps/web/)
npm run lint
```

Both run in CI on every pull request and push to main.

## SQLite Persistence

- The local development database lives at `apps/api/data/residential_energy_planner.sqlite3`.
- Tables are created automatically on backend startup.
- On first run, the app seeds demo data into the database if no home records exist.
- Current persistence now covers accounts, homes, structures, panels, loads, designs, equipment locations, product library records, scenarios, takeoffs, load templates, design goal presets, and estimated pathways.
- Persisted planning records now include a `data_origin` field where practical:
  - `demo_seed`
  - `user_created`
  - `imported`
  - `verified`
  - `derived_estimate`
  - `placeholder`

## Provenance Foundation

Phase 2E adds an initial source-lineage layer behind the trust-visibility UI:

- `SourceDocument`: where a fact or assumption came from
- `DataProvenance`: which entity field was informed by which source
- `RuleProvenance`: which internal planning rules influenced derived outputs

What is tracked now:

- demo product/spec examples and placeholder manufacturer references
- user-entered planning assumptions
- internal planning rules for completeness/advisor/takeoff logic
- transient derived-takeoff basis records and provenance summaries

What is not tracked yet:

- full audit/change history
- automated manufacturer ingestion
- exhaustive field-level provenance for every calculation
- persisted takeoff snapshots

Verification status is not the same thing as a trust badge:

- verification status describes the state of a source document such as `unverified`, `user_entered`, or `manufacturer_verified`
- trust badges describe how the app should present current data such as `demo_seed`, `placeholder`, or `derived_estimate`

Future AI responses should cite structured provenance and source summaries rather than guessing or smoothing over uncertainty.

## Reset And Reseed

Using an activated backend environment:

```bash
cd apps/api
python3 -m app.seed.cli reseed
```

To print the local DB path:

```bash
cd apps/api
python3 -m app.seed.cli path
```

Fallback if using the local `.vendor` dependency folder:

```bash
cd apps/api
PYTHONPATH=.vendor python3 -m app.seed.cli reseed
```

You can also remove `apps/api/data/residential_energy_planner.sqlite3` and restart the backend.

## Ops Session Reports

Email delivery for manual session closeout reports has been removed. Session reports should be written to repository docs or handoff files only. Reintroducing email delivery requires a new owner-approved provider setup, new scripts, and fresh secrets.

## Migrations

- Alembic is now scaffolded for the backend in `apps/api/alembic.ini` and `apps/api/migrations/`.
- The current setup is intentionally lightweight and aimed at local SQLite development hardening before editable workflows begin.
- Current baseline upgrade command:

```bash
cd apps/api
alembic upgrade head
```

Fallback with the local `.vendor` dependency folder:

```bash
cd apps/api
PYTHONPATH=.vendor alembic upgrade head
```

For existing pre-hardening local databases, reseeding is the simplest recovery path.

## Account Scaffolding

Phase 2A includes persisted account ownership scaffolding for future multi-user workflows:

- `Account.role`: `homeowner`, `contractor`, `admin`
- `Account.subscription_status`: `trialing`, `active`, `paused`, `canceled`
- `Account.plan_type`: `demo`, `homeowner`, `contractor`, `contractor_team`
- `Home.account_id`: nullable for now

These fields are persisted but not yet connected to login, access control, billing, or subscription enforcement.

## API Versioning Policy

- Existing unprefixed routes remain supported to avoid breaking the current frontend.
- `/api/*` aliases are now also available and are the preferred base path for future clients.
- `/api/v1` is reserved for the first explicit versioned contract if a breaking API evolution becomes necessary later.
- Current policy is additive-first: avoid breaking existing GET contracts unless frontend, docs, and migration guidance move together.

## Current State

- Working API routes expose SQLite-backed data with first-run seed loading and placeholder service outputs.
- Working frontend routes fetch live persisted data from the API and now support core editable planning workflows for the house model, loads, designs, scenarios, equipment locations, and estimated pathways.
- Product specs, cost values, engineering logic, and code guidance are placeholders by design.

See `docs/` for the detailed vision and system philosophy.

## Secrets Management

Use `.env.example` for placeholder variable names only. Real secrets belong outside the repo, with `~/.secrets/residential-energy-planner/` as the preferred local working path and 1Password as the current source of truth. Repo-local `.env` files are gitignored runtime delivery files only. The current runbook is `docs/secrets-management.md`.
