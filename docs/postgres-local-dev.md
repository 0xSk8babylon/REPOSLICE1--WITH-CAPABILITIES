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

## Cleanup

Stop the local service without deleting data:

```bash
docker compose -f compose.postgres.yml --profile postgres down
```

Deleting the named volume removes local Postgres data and should be an explicit owner-controlled cleanup action.
