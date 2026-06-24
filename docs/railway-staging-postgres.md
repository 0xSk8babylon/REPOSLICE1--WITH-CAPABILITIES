# Railway Staging Postgres Runbook

Related secrets boundary: `docs/secrets-management.md`.
Production planning boundary: `docs/railway-production-postgres.md`.

## Current Railway State

- Repo Railway config: none found.
- Railway CLI: installed and authenticated for inspection.
- Workspace: `0xsk8babylon's Projects`.
- Project: `rep-postgres-staging`.
- Environment: `staging`.
- Existing Railway Postgres service: `Postgres`.
- Existing Railway FastAPI service: `rep-api-staging`.
- Public staging URL: `https://rep-api-staging-staging.up.railway.app`.
- Logical DB / app target label: `rep_pg8e_staging`.
- Repo status before Railway staging FastAPI smoke closeout docs: clean on `fix/github-workflow`, ahead of origin by 35.

## Staging Resource

- Railway environment: `staging`
- Railway project: `rep-postgres-staging`
- Railway Postgres service: `Postgres`
- Railway FastAPI service: `rep-api-staging`
- Public staging URL: `https://rep-api-staging-staging.up.railway.app`
- Logical DB / app target label: `rep_pg8e_staging`

This is a staging-only managed Postgres target. It is not a production database and should not be treated as a production cutover.

## Future FastAPI Environment Variables

When a staging FastAPI service is later approved, it should use Railway-managed Postgres connection settings with these app-level variables:

```text
APP_ENV=staging
DATABASE_URL
DATABASE_CREATE_ALL_ON_STARTUP=false
DATABASE_SEED_DEMO_DATA_ON_STARTUP=false
DEBUG=false
```

Do not print or commit resolved connection strings. Do not copy Railway secrets into the repo.

## Approval Gate

Owner approval is required before any new Railway resource, FastAPI deploy, Railway env-var wiring, production operation, or future migration step because those actions happen outside the repo and may create managed infrastructure, cost, runtime exposure, or data changes.

Before further Railway action, confirm:

- target environment is `staging`
- target project is `rep-postgres-staging`
- target Postgres service is the existing `Postgres` service
- no production environment, service, or database is selected
- no app deploy, migration, env-var change, or data copy is being bundled into an unrelated step

## Guardrails

- Staging only.
- Do not create production Railway resources.
- Do not deploy FastAPI without separate owner approval.
- Do not set Railway FastAPI env vars without separate owner approval.
- Do not run additional migrations without separate owner approval.
- Do not touch production SQLite.
- Do not touch production Postgres.
- Do not edit secrets or vault material.
- Do not introduce frontend Supabase SDKs.
- Do not push without explicit approval.

## PG-8E Staging Migration Status

Railway staging Postgres migration passed.

- Alembic upgrade head: PASS
- Alembic revision: `20260523_0001`
- Public schema table count after Alembic: `26`
- PG-8E dry-run: PASS
- PG-8E execute: PASS
- FK validation: PASS
- Provenance validation: PASS
- Unexpected writes: no
- Production touched: no
- Secrets printed: no
- FastAPI Railway deploy: PASS
- Railway FastAPI env vars set: yes, values redacted

Validated staging row counts:

```text
accounts=1
homes=1
source_documents=5
data_provenance=7
rule_provenance=25
equipment_products=8
energy_system_designs=2
scenarios=2
```

Integrity validation:

```text
source_sqlite_fk_issue_count=0
postgres_unvalidated_fk_constraint_count=0
data_provenance_orphan_count=0
rule_provenance_orphan_count=0
```

## Local FastAPI Smoke Status

Local FastAPI TestClient smoke passed against the migrated Railway staging database with `DATABASE_CREATE_ALL_ON_STARTUP=false` and `DATABASE_SEED_DEMO_DATA_ON_STARTUP=false`.

Unprotected GET smoke:

```text
/                    200
/api/accounts        200, count 1
/api/product-library 200, count 8
```

Protected GET smoke with expected audit-only writes:

```text
/api/homes/all 200, count 1
/api/designs   200, count 2
/api/scenarios 200, count 2
```

`audit_events` increased from `0` to `3` as expected for protected GET access. Core migrated table counts remained unchanged after protected smoke.

## Staging Verification Automation

Use the local staging secret file from `~/.secrets/residential-energy-planner/staging.env`. These scripts must not print `DATABASE_URL` or secret values.

Read-only staging readiness check:

```bash
scripts/check_staging_readiness.sh
```

This verifies the repo is clean, the staging env file exists, env file permissions are closed to group/other access, required key names are present, `APP_ENV=staging`, `DEBUG=false`, startup create/seed flags are disabled, the Postgres target is reachable, Alembic is at `20260523_0001`, expected tables exist, expected row counts match, provenance orphan counts are zero, and public FK constraints are validated. It uses SELECT-only database checks.

The local verification scripts normalize bare `postgres://` or `postgresql://` values to SQLAlchemy's `postgresql+psycopg://` dialect inside the running process because the API dependency set installs `psycopg`. They do not edit the secret file or print the resolved URL.

Local FastAPI smoke against the staging database:

```bash
python3 scripts/smoke_staging_fastapi.py
```

The default smoke verifies the repo is clean, exercises `/`, `/api/accounts`, and `/api/product-library`, and expects no database writes. It requires the API runtime dependencies from `apps/api/requirements.txt`; if a usable `apps/api/.venv/bin/python` exists, the script can re-execute itself with that venv interpreter.

If the local host Python environment is stale, use the established ephemeral Docker Python runtime and install dependencies inside the disposable container, not on the host:

```bash
docker run --rm \
  -v "$PWD":/work \
  -v "$HOME/.secrets":/root/.secrets:ro \
  -w /work \
  python:3.11-slim \
  sh -lc 'python -m pip install -q -r apps/api/requirements.txt && python scripts/smoke_staging_fastapi.py'
```

Protected GET smoke is available only when the expected audit-only writes are explicitly approved:

```bash
python3 scripts/smoke_staging_fastapi.py --include-protected-audit-smoke
```

With that flag, the script also exercises `/api/homes/all`, `/api/designs`, and `/api/scenarios`; it requires exactly three `audit_events` inserts and verifies core migrated table counts remain unchanged.

## Railway Staging FastAPI Deploy And Public Smoke

Railway staging FastAPI deploy passed for service `rep-api-staging`.

- Public staging URL: `https://rep-api-staging-staging.up.railway.app`
- Runtime database backend reported by `/`: `postgresql`
- Startup create-all disabled: yes
- Startup seed disabled: yes
- Migrations run during deploy/smoke: no
- Seed run during deploy/smoke: no
- Secrets printed: no
- Production touched: no
- Push performed: no

Deployed public HTTP smoke:

```text
/                         200, backend postgresql
/api/accounts             200, count 1
/api/product-library      200, count 8
/api/homes/all            200, count 1
/api/designs              200, count 2
/api/scenarios            200, count 2
```

Protected GET smoke produced only expected audit writes:

```text
audit_events_before=6
audit_events_after=9
audit_events_delta=3
```

Post-smoke readiness gate: PASS.

```text
alembic_version=20260523_0001
accounts=1
homes=1
source_documents=5
data_provenance=7
rule_provenance=25
equipment_products=8
energy_system_designs=2
scenarios=2
data_provenance_orphan_count=0
rule_provenance_orphan_count=0
```

Core migrated counts remained unchanged. FK and provenance checks passed.

## Next Step

Next required approval: production Gate 1 only, as defined in `docs/railway-production-postgres.md`. Do not create production Railway resources, run production migrations, migrate production data, deploy production services, set production env vars, run public production smoke, touch staging resources, or push until Matt explicitly approves the exact next boundary.
