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

## PG-7 Opt-In Local Runtime Mode

PG-7 local runtime mode is explicit and local-only. SQLite remains the default when `DATABASE_URL` is unset. Do not commit these values to `.env`, and do not use the Compose placeholder credentials outside local development.

Use a dedicated local runtime-smoke database instead of the Compose default database:

```text
rep_pg7_local_runtime
```

Prepare the database only after the local Postgres service is running and the fixed Docker subnet is confirmed as `172.25.0.0/16`:

```bash
docker compose -f compose.postgres.yml --profile postgres up -d
docker network inspect residential-energy-planner-postgres-dev --format '{{range .IPAM.Config}}{{.Subnet}}{{end}}'
docker compose -f compose.postgres.yml --profile postgres exec postgres pg_isready -U rep_dev -d residential_energy_planner
```

Host UFW must allow `172.25.0.0/16` on `5432/tcp` before any broad `172.16.0.0/12` deny before running host-side Postgres checks.

Create the local runtime-smoke database if needed:

```bash
docker compose -f compose.postgres.yml --profile postgres exec postgres \
  createdb -U rep_dev rep_pg7_local_runtime
```

If it already exists, continue without dropping it.

Apply the current Alembic head only to the dedicated local runtime-smoke database:

```bash
cd apps/api
DATABASE_URL='postgresql+psycopg://rep_dev:rep_dev_password@127.0.0.1:54329/rep_pg7_local_runtime' \
DATABASE_CREATE_ALL_ON_STARTUP=false \
DATABASE_SEED_DEMO_DATA_ON_STARTUP=false \
python3 -m alembic upgrade head
```

Start FastAPI in opt-in local Postgres mode with one-shot environment variables only:

```bash
cd apps/api
DATABASE_URL='postgresql+psycopg://rep_dev:rep_dev_password@127.0.0.1:54329/rep_pg7_local_runtime' \
DATABASE_CREATE_ALL_ON_STARTUP=false \
DATABASE_SEED_DEMO_DATA_ON_STARTUP=false \
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The local runtime smoke checklist is:

- `GET /` returns `200`, a redacted Postgres URL, `create_all_on_startup=false`, and `seed_demo_data_on_startup=false`.
- `GET /api/homes/all` with `x-user-id` and `x-home-access: *` returns `200`.
- `POST /api/homes` creates one local smoke home.
- `POST /api/homes/{home_id}/facts` creates one fact attached to that home.
- `GET /api/homes/{home_id}/facts` reads the fact back.
- `audit_events` contains authorized events for the tested paths.

Postgres demo seeding remains disabled for PG-7. Seed behavior on Postgres requires a separate approval gate.

Rollback is command-level: stop the FastAPI process and restart without `DATABASE_URL` to return to the SQLite default. Stop the local container without deleting volumes:

```bash
docker compose -f compose.postgres.yml --profile postgres down
```

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

## PG-6B Write Smoke Status

PG-6B disposable Postgres Home + Fact write/read smoke passed against local database `rep_pg6b_write_smoke`. The test ran `alembic upgrade head` only against that disposable local database, then `alembic current` reported `20260523_0001 (head)`.

The smoke used existing APIs only:

- `POST /api/homes` returned `200` and created a disposable smoke home.
- `GET /api/homes/all` returned `200` and included the created home.
- `POST /api/homes/{home_id}/facts` returned `200` and created a disposable smoke fact attached to the home.
- `GET /api/homes/{home_id}/facts` returned `200`, found the created fact, and reported effective confidence tier `known` with score `1.0`.

`audit_events` contained authorized events for `/api/homes`, `/api/homes/all`, and `/api/homes/{home_id}/facts`.

The disposable database remains in the preserved Docker volume unless later cleanup is explicitly approved.

PG-6B does not approve a runtime `DATABASE_URL` switch, `.env` Postgres default, FastAPI dev/prod server startup against Postgres, persistence wiring, sandbox draft persistence, SQLite-to-Postgres migration, downgrade, stamp, production database use, migration file creation, or broader endpoint compatibility.

## PG-8E Local SQLite-to-Postgres Rehearsal Status

PG-8E local rehearsal passed against the owned Docker Postgres service only. The disposable local rehearsal database was:

```text
rep_pg8e_rehearsal
```

The rehearsal used the existing SQLite backup:

```text
apps/api/data/backups/residential_energy_planner.pg8e.20260623T070201Z.sqlite3
sha256 b9cf2b94c3a13b4a66352688a8a19338ef2a6aba86b184d9d218a1e4a4056c9d
```

`alembic upgrade head` ran only against `rep_pg8e_rehearsal` and the target revision was verified as `20260523_0001`.

The committed SQLite-to-Postgres migration helper then passed dry-run and execute mode against `rep_pg8e_rehearsal`:

- dry-run: PASS
- execute: PASS
- `count_mismatches`: `{}`
- source SQLite foreign-key issue count: `0`
- target provenance/source-document orphan checks: PASS
- `data_provenance` source-document orphans: `0`
- `rule_provenance` source-document orphans: `0`

Post-migration row-count validation:

```text
accounts=1
source_documents=5
design_goal_presets=2
load_templates=6
homes=1
audit_events=0 before smoke, 3 after smoke
consent_records=0
buildings=2
electrical_panels=1
loads=3
facts=0
roof_planes=0
geometry_obstructions=0
equipment_locations=3
equipment_products=8
energy_system_designs=2
design_equipment=5
compatibility_issues=2
scenarios=2
scenario_revisions=2
takeoff_requests=1
takeoff_line_items=2
estimated_pathways=2
data_provenance=7
rule_provenance=25
```

FastAPI TestClient smoke ran against `rep_pg8e_rehearsal` with `DATABASE_CREATE_ALL_ON_STARTUP=false` and `DATABASE_SEED_DEMO_DATA_ON_STARTUP=false`:

```text
/                       200
/api/accounts           200
/api/homes/all          200
/api/designs            200
/api/scenarios          200
/api/product-library    200
```

Sample migrated IDs included `account_demo`, `home_001`, `design_001`, `design_002`, `scenario_001`, `scenario_002`, `product_ecoflow_system`, `product_eg4_hybrid`, `product_enphase_micro`, `source_doc_demo_seed_catalog`, `source_doc_internal_rulebook`, and `source_doc_pathway_walkthrough_note`.

The rehearsal did not touch Railway, Supabase, production SQLite, production Postgres, vault/secrets, frontend Supabase SDKs, or remote git. No repo code changed during the rehearsal. The repo was clean afterward on `fix/github-workflow`, ahead of origin by 28.

`rep_pg8e_rehearsal` remains in the local Docker Postgres volume for inspection. Do not clean it up unless Matt explicitly approves disposable rehearsal DB cleanup.

## Cleanup

Stop the local service without deleting data:

```bash
docker compose -f compose.postgres.yml --profile postgres down
```

Deleting the named volume removes local Postgres data and should be an explicit owner-controlled cleanup action.

Do not run `docker compose -f compose.postgres.yml --profile postgres down -v` unless Matt explicitly approves Docker volume deletion.
