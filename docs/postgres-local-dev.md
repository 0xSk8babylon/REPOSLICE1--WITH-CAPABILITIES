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

Before future smoke reruns, confirm the active Docker bridge subnet. Docker may recreate the Compose network on a different subnet, so the firewall allow rule must match the current subnet:

```bash
docker network inspect residential-energy-planner_default --format '{{range .IPAM.Config}}{{.Subnet}}{{end}}'
```

The next boundary is PG-5A Disposable Baseline Upgrade Test planning. Before any runtime switch or persistence planning, the existing Alembic baseline still needs a disposable local Postgres test. That future test may run `alembic upgrade head` only against a disposable local Postgres database/container, with no runtime `DATABASE_URL` switch, no FastAPI startup against Postgres, no `.env` change, no persistence wiring, no production database, and no downgrade.

## Cleanup

Stop the local service without deleting data:

```bash
docker compose -f compose.postgres.yml --profile postgres down
```

Deleting the named volume removes local Postgres data and should be an explicit owner-controlled cleanup action.
