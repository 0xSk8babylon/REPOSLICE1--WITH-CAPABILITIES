# Local Postgres Development

This is an optional local-only Postgres service for future approved migration and runtime smoke checks. SQLite remains the default runtime when `DATABASE_URL` is unset.

## Boundary

- Do not commit `.env` or machine-specific secrets.
- Do not use these placeholder credentials outside local development.
- Do not run `alembic upgrade head` against Postgres until the migration baseline strategy is approved.
- Do not switch the app runtime to Postgres unless Matt explicitly approves the runtime switch plan.
- Do not use this service for production data.

## Service

```bash
docker compose -f compose.postgres.yml config
docker compose -f compose.postgres.yml --profile postgres up -d
docker compose -f compose.postgres.yml ps
docker compose -f compose.postgres.yml exec postgres pg_isready -U rep_dev -d residential_energy_planner
```

The Compose service uses a fixed local bridge network named `residential-energy-planner-postgres-dev` with subnet `172.25.0.0/16`. This keeps local Postgres smoke checks aligned with host firewall rules instead of depending on Docker's automatic subnet allocation.

Host UFW must allow outbound traffic to `172.25.0.0/16` on port `5432/tcp`, and that allow rule must be ordered before the broad outbound deny for `172.16.0.0/12`. If Docker reports that `172.25.0.0/16` conflicts with another local Docker network, stop and report the conflict; do not broaden firewall rules automatically.

The service uses:

```text
POSTGRES_DB=residential_energy_planner
POSTGRES_USER=rep_dev
POSTGRES_PASSWORD=rep_dev_password
HOST_PORT=54329
```

## One-Shot Environment

Use one-shot shell variables for approved checks. Do not commit them to `.env`.

```bash
DATABASE_URL='postgresql+psycopg://rep_dev:rep_dev_password@localhost:54329/residential_energy_planner' \
DATABASE_CREATE_ALL_ON_STARTUP=false \
DATABASE_SEED_DEMO_DATA_ON_STARTUP=false \
python3 -m alembic history
```

For connection-only smoke checks in a later approved phase:

```bash
DATABASE_URL='postgresql+psycopg://rep_dev:rep_dev_password@localhost:54329/residential_energy_planner' \
python3 - <<'PY'
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.database import engine_kwargs_for_url, redact_database_url

print(redact_database_url(settings.resolved_database_url))
engine = create_engine(settings.resolved_database_url, **engine_kwargs_for_url(settings.resolved_database_url))
with engine.connect() as conn:
    print(conn.execute(text("select 1")).scalar_one())
PY
```

This smoke check should not create schema, seed data, stamp a database, or apply migrations.

## PG-5 Smoke Status

PG-5 connection-only smoke is resolved/passed for the local environment after a host firewall correction. The failure cause was environmental: UFW had a broad outbound DROP for `172.16.0.0/12`, which blocked Docker bridge traffic. The manual fix was an outbound allow rule for the active Docker network subnet, `172.25.0.0/16`, on Postgres port `5432/tcp`, ordered before the broad DROP. After that correction, DBAPI psycopg and SQLAlchemy `SELECT 1` smoke checks passed manually.

Before future smoke reruns, confirm the fixed Docker bridge subnet:

```bash
docker network inspect residential-energy-planner-postgres-dev --format '{{range .IPAM.Config}}{{.Subnet}}{{end}}'
```

Expected output: `172.25.0.0/16`.

## PG-5A Baseline Test Status

PG-5A disposable baseline upgrade test passed against local database `rep_pg5a_baseline_test`. The test ran `alembic upgrade head` only against that disposable local Postgres database, then `alembic current` reported `20260523_0001 (head)`.

Schema inspection found `alembic_version` plus the 25 SQLAlchemy metadata tables. The disposable database remains in the preserved Docker volume unless later cleanup is explicitly approved.

Codex sandbox Python still has host-networking limitations and failed DBAPI/SQLAlchemy host checks, but outside-sandbox host Python passed DBAPI and SQLAlchemy `SELECT 1` against `rep_pg5a_baseline_test`.

PG-5A does not approve a runtime `DATABASE_URL` switch, FastAPI startup against Postgres, persistence wiring, SQLite migration, downgrade, stamp, production database use, migration file creation, or `.env` changes.

## PG-6A-3 Runtime Smoke Status

PG-6A-3 test-only FastAPI/TestClient Postgres runtime smoke passed against disposable local database `rep_pg6a_runtime_smoke`. The database was already at Alembic `20260523_0001 (head)`, and `alembic upgrade head` completed as a no-op against that disposable database only.

The TestClient root endpoint `/` returned `200` with redacted URL `postgresql+psycopg://rep_dev:***@127.0.0.1:54329/rep_pg6a_runtime_smoke`. The response reported `create_all_on_startup=false` and `seed_demo_data_on_startup=false`.

Authenticated `GET /api/homes/all` using `x-user-id: pg6a_smoke` and `x-home-access: *` returned `200` with `[]`, and `audit_events` contained an authorized `200` event for `/api/homes/all`.

PG-6A-3 does not approve a runtime `DATABASE_URL` switch, `.env` changes, FastAPI dev/prod server startup against Postgres, persistence wiring, sandbox draft persistence, SQLite-to-Postgres migration, downgrade, stamp, production database use, or migration file creation.

## Cleanup

Stop the local service without deleting data:

```bash
docker compose -f compose.postgres.yml --profile postgres down
```

Deleting the named volume removes local Postgres data and should be an explicit owner-controlled cleanup action.

Do not run `docker compose -f compose.postgres.yml --profile postgres down -v` unless Matt explicitly approves Docker volume deletion.
