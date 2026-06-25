# Railway Production Postgres Plan

Related runbooks:

- Secrets boundary: `docs/secrets-management.md`
- Staging baseline: `docs/railway-staging-postgres.md`
- Local rehearsal baseline: `docs/postgres-local-dev.md`

## Boundary

This is a production planning runbook only. It does not approve or perform production provisioning, migrations, data copy, FastAPI deployment, Railway environment-variable changes, public smoke, push, or commit.

Production must be handled as five separate approval gates:

1. Production Postgres creation.
2. Production Alembic upgrade.
3. SQLite-to-Postgres data migration.
4. Production FastAPI deploy and environment-variable wiring.
5. Public production smoke.

Do not bundle these gates. Each gate requires a fresh owner approval with the exact target, action, and expected write behavior.

## Production-Only Railway Names

Production-only labels:

```text
Railway workspace: 0xsk8babylon's Projects
Railway project: rep-postgres-production
Railway environment: production
Railway Postgres service: Postgres
Railway FastAPI service: rep-api-production
Logical DB / app target label: rep_pg8e_production
Public production URL: TBD after production FastAPI deploy approval
```

Production must not reuse the staging project, staging environment, staging Postgres service, staging FastAPI service, staging public URL, local Docker database, Supabase attempt target, or disposable rehearsal database.

## Secret-Handling Boundary

- Do not print, paste, commit, log, or summarize resolved production secrets.
- Do not open, edit, or create repo-local `.env` files for production.
- Do not copy production Railway credentials into docs, chat, scripts, tests, commits, or local shell history.
- Prefer Railway-managed variable references inside Railway over copied resolved credentials.
- If a local production env file is explicitly approved later, keep it outside the repo under `~/.secrets/residential-energy-planner/`, with closed group/other permissions, and never print its values.
- Treat `DATABASE_URL` as secret when it contains managed database credentials.
- Treat `RAILWAY_*` platform variables as Railway-managed runtime delivery values, not repo configuration.
- If any production secret is printed or committed, stop and rotate it at the source before continuing.

## Required Production Environment Variables

When production FastAPI env-var wiring is separately approved, use only production values:

```text
APP_ENV=production
DATABASE_URL=<Railway-managed production Postgres connection string>
DATABASE_CREATE_ALL_ON_STARTUP=false
DATABASE_SEED_DEMO_DATA_ON_STARTUP=false
DEBUG=false
```

Required checks before any production runtime starts:

- `APP_ENV` is exactly `production`.
- `DATABASE_URL` points to the production Railway Postgres service only.
- `DATABASE_CREATE_ALL_ON_STARTUP=false`.
- `DATABASE_SEED_DEMO_DATA_ON_STARTUP=false`.
- `DEBUG=false`.
- No staging, local Docker, Supabase staging, or rehearsal database URL is present.

## Production Approval Gates

Every production gate must confirm:

- exact Railway workspace, project, environment, and service names
- exact command or Railway UI action to perform
- whether the step creates infrastructure, writes schema, writes data, writes audit rows, deploys code, or changes public runtime exposure
- expected rollback or stop point
- confirmation that staging resources are not selected
- confirmation that no secrets will be printed
- confirmation that no push or commit is included unless separately approved

Stop immediately if the selected Railway target, environment name, service name, or database identity differs from the approved gate.

## Gate 1: Production Postgres Creation Checklist

Purpose: create an empty production Railway Postgres service only.

Approval required before this gate:

- Create production Railway project `rep-postgres-production`, if it does not already exist.
- Create/use Railway environment `production`.
- Create production Postgres service `Postgres`.

Allowed actions after approval:

- Inspect Railway account/project/environment selection.
- Create the production project/environment/Postgres service if explicitly included in the approval.
- Record only non-secret production labels and creation status in docs after verification.

Forbidden during this gate:

- No Alembic upgrade.
- No PG-8E data migration.
- No FastAPI production deploy.
- No Railway FastAPI env-var wiring.
- No seed.
- No public smoke.
- No staging changes.
- No production data copy.
- No secret printing.

Stop point:

- Stop after the empty production Postgres service exists and the target identity is confirmed without exposing credentials.

Rollback posture:

- If the empty production Postgres service was created incorrectly and contains no application schema or migrated data, owner may approve deleting or recreating it. Do not delete it without explicit approval.

## Gate 2: Production Alembic Upgrade Checklist

Purpose: create the production schema at the current Alembic head on the approved empty production Postgres target.

Approval required before this gate:

- Exact production `DATABASE_URL` delivery method is available without printing it.
- Production target identity is confirmed.
- Production Postgres service is empty or intentionally schema-ready.
- Current Alembic head remains `20260523_0001`.

Preferred local secret delivery for this gate:

```bash
op run --env-file scripts/templates/production-op.env.tpl -- bash -lc 'cd apps/api && python3 -m alembic upgrade head'
```

The template maps `DATABASE_PUBLIC_URL` from 1Password to runtime `DATABASE_URL` for local Alembic access. It contains only `op://` references and non-secret flags. Run `scripts/check_production_op_secrets.sh` first to verify `op` auth, item existence, and required field-title presence without printing secret values.

Preflight:

- Confirm no staging Railway service is selected.
- Confirm startup create/seed flags are disabled.
- Confirm target public schema state is understood before upgrade.
- Confirm no app deployment or PG-8E data copy is bundled into this gate.

Allowed actions after approval:

- Run `alembic upgrade head` only against the approved production Postgres target.
- Verify `alembic_version=20260523_0001`.
- Verify expected public tables exist.
- Verify no seed was run.

Forbidden during this gate:

- No PG-8E data migration.
- No FastAPI production deploy.
- No Railway FastAPI env-var wiring.
- No seed.
- No public smoke.
- No staging changes.
- No secret printing.

Stop point:

- Stop after schema and Alembic revision are verified.

Rollback posture:

- Alembic downgrade/rollback is not approved by this plan. If the upgrade targets the wrong database or fails mid-step, stop and document observed state. Any corrective schema action requires separate approval.

## Gate 3: PG-8E Production Data Migration Checklist

Purpose: copy approved SQLite data into the schema-ready production Postgres database using the committed PG-8E migration helper.

Approval required before this gate:

- Exact source SQLite backup path and checksum are approved.
- Exact production target is approved.
- Production Alembic revision is verified as `20260523_0001`.
- Application target tables expected by PG-8E are empty or explicitly approved for copy behavior.
- Dry-run and execute mode are approved as separate sub-steps or explicitly approved together.

Preflight:

- Confirm source SQLite foreign-key issue count is zero.
- Confirm source provenance/source-document orphan checks pass.
- Confirm production target table counts are compatible with migration preconditions.
- Confirm no FastAPI production deploy or public smoke is bundled into this gate.

Allowed actions after approval:

- Run PG-8E dry-run against production with redacted target reporting.
- Stop for review after dry-run unless execute is explicitly approved.
- Run PG-8E execute only after approval.
- Validate count mismatches are empty.
- Validate source-document provenance orphan counts are zero.
- Validate public FK constraints are validated.
- Record non-secret row counts only.

Forbidden during this gate:

- No Alembic migration beyond the approved head check.
- No seed.
- No FastAPI production deploy.
- No Railway FastAPI env-var wiring.
- No public smoke.
- No staging changes.
- No secret printing.

Stop point:

- Stop after production data counts and integrity checks are recorded without secrets.

Rollback posture:

- PG-8E production copy is not automatically reversible. If copy fails or counts mismatch, stop and preserve the target for inspection. Any truncation, drop, restore, rerun, or service deletion requires separate explicit approval.

## Gate 3 Precheck Result

Owner-run production PG-8E precheck from a signed-in terminal reached the production database without printing secrets and stopped before dry-run or execute because PG-8E target tables are already non-empty.

Interpretation:

- PG-8E execute remains blocked by the helper's empty-target precondition.
- The observed production counts match the known PG-8E local/staging migrated baseline for all migrated data tables, with `audit_events=9`.
- `audit_events=9` is consistent with prior deployed staging smoke behavior, where protected GET smoke created audit-only writes while core migrated table counts remained unchanged.
- Treat production as effectively already populated pending verification-only closeout, not as a fresh PG-8E execute performed during this gate.

Observed non-secret precheck facts:

```text
production_db_connection=PASS
alembic_version=20260523_0001
expected_alembic_version=20260523_0001
missing_pg8e_tables=[]
non_empty_pg8e_tables_present=true
accounts=1
homes=1
source_documents=5
data_provenance=7
rule_provenance=25
equipment_products=8
energy_system_designs=2
scenarios=2
audit_events=9
```

Full observed target counts:

```text
accounts=1
source_documents=5
design_goal_presets=2
load_templates=6
homes=1
audit_events=9
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

Read-only verification-only command for the owner to run from a signed-in terminal:

```bash
SOURCE="data/backups/residential_energy_planner.pg8e.production-cutover.20260625T064247Z.sqlite3"

op run --env-file scripts/templates/production-op.env.tpl -- bash -s -- "$SOURCE" <<'BASH'
set -euo pipefail
SOURCE="$1"
cd apps/api

python3 - "$SOURCE" <<'PY'
import json
import os
import sqlite3
import sys
from sqlalchemy import create_engine, text
from scripts.sqlite_to_postgres import TABLE_ORDER, EXPECTED_ALEMBIC_HEAD

source = sys.argv[1]
url = os.environ["DATABASE_URL"]
if url.startswith("postgresql://"):
    url = "postgresql+psycopg://" + url[len("postgresql://"):]
elif url.startswith("postgres://"):
    url = "postgresql+psycopg://" + url[len("postgres://"):]

def q(name):
    return '"' + name.replace('"', '""') + '"'

with sqlite3.connect(f"file:{source}?mode=ro", uri=True) as sqlite:
    source_counts = {
        table: sqlite.execute(f"select count(*) from {q(table)}").fetchone()[0]
        for table in TABLE_ORDER
    }
    sqlite_fk_issue_count = len(sqlite.execute("pragma foreign_key_check").fetchall())

engine = create_engine(url, future=True)
with engine.connect() as conn:
    target_counts = {
        table: int(conn.execute(text(f"select count(*) from {q(table)}")).scalar_one())
        for table in TABLE_ORDER
    }
    versions = [
        row[0]
        for row in conn.execute(text("select version_num from alembic_version order by version_num"))
    ]
    data_orphans = int(conn.execute(text("""
        select count(*)
        from data_provenance provenance
        left join source_documents source on provenance.source_document_id = source.id
        where provenance.source_document_id is not null and source.id is null
    """)).scalar_one())
    rule_orphans = int(conn.execute(text("""
        select count(*)
        from rule_provenance provenance
        left join source_documents source on provenance.source_document_id = source.id
        where provenance.source_document_id is not null and source.id is null
    """)).scalar_one())
    unvalidated_fk_constraints = int(conn.execute(text("""
        select count(*)
        from pg_constraint c
        join pg_namespace n on n.oid = c.connamespace
        where n.nspname = 'public'
          and c.contype = 'f'
          and not c.convalidated
    """)).scalar_one())

count_mismatches = {
    table: {"source": source_counts[table], "target": target_counts[table]}
    for table in TABLE_ORDER
    if source_counts[table] != target_counts[table]
}

print(json.dumps({
    "stage": "production_pg8e_verification_only",
    "alembic_version": ",".join(versions),
    "expected_alembic_version": EXPECTED_ALEMBIC_HEAD,
    "count_mismatches": count_mismatches,
    "source_sqlite_fk_issue_count": sqlite_fk_issue_count,
    "postgres_unvalidated_fk_constraint_count": unvalidated_fk_constraints,
    "data_provenance_orphan_count": data_orphans,
    "rule_provenance_orphan_count": rule_orphans,
    "target_counts": target_counts,
}, indent=2, sort_keys=True))
PY
BASH
```

This command is read-only. It must not be changed into a copy, execute, truncate, delete, reset, seed, smoke, deploy, Railway env-var wiring, or resource-modification command without separate owner approval.

## Gate 4: Production FastAPI Deploy And Env-Var Wiring Checklist

Purpose: deploy FastAPI to Railway production and wire it to the approved migrated production Postgres database.

Approval required before this gate:

- Production Postgres exists.
- Production schema is at `20260523_0001`.
- PG-8E production migration is complete and validated, or owner explicitly approves deploy against an empty/schema-only production database.
- Exact production FastAPI service name is approved: `rep-api-production`.
- Required production env vars are approved for Railway runtime delivery.

Preflight:

- Confirm Railway environment is `production`.
- Confirm service is `rep-api-production`, not `rep-api-staging`.
- Confirm app root/config matches the existing Railway API deploy configuration.
- Confirm `DATABASE_CREATE_ALL_ON_STARTUP=false`.
- Confirm `DATABASE_SEED_DEMO_DATA_ON_STARTUP=false`.
- Confirm `DEBUG=false`.
- Confirm no code push is bundled unless separately approved.

Allowed actions after approval:

- Create or configure the production FastAPI service.
- Wire approved production env vars through Railway without printing values.
- Deploy FastAPI to production.
- Verify deployment health path `/` only enough to confirm startup if included in approval.

Forbidden during this gate:

- No new Alembic migration.
- No PG-8E rerun.
- No seed.
- No protected public smoke unless separately approved.
- No staging changes.
- No secret printing.

Stop point:

- Stop after deploy health is known and runtime reports production posture through non-secret diagnostics.

Rollback posture:

- If deploy fails, stop and inspect non-secret logs/status only. Reverting env vars, redeploying a prior service version, pausing/removing the service, or changing the production database target requires separate approval.

## Gate 5: Public Production Smoke Checklist

Purpose: verify the public production API against the production Postgres backend after deploy.

Approval required before this gate:

- Exact public production URL is known.
- Expected production row counts are known from Gate 3 or approved empty/schema-only target.
- Expected audit write behavior is approved.

Default unprotected smoke:

```text
/                    200, backend postgresql
/api/accounts        200, expected count from production migration
/api/product-library 200, expected count from production migration
```

Protected GET smoke requires separate explicit approval because it writes audit rows:

```text
/api/homes/all 200, expected count from production migration
/api/designs   200, expected count from production migration
/api/scenarios 200, expected count from production migration
```

Expected protected-smoke write behavior:

```text
audit_events_delta=3
core_migrated_table_counts unchanged
```

Post-smoke readiness checks:

- `alembic_version=20260523_0001`.
- Core migrated row counts match expected production counts.
- `data_provenance_orphan_count=0`.
- `rule_provenance_orphan_count=0`.
- Public FK constraints are validated.
- Startup create-all remains disabled.
- Startup seed remains disabled.
- No secrets printed.

Stop point:

- Stop after smoke and readiness results are recorded.

Rollback posture:

- If public smoke fails, stop and do not retry write-producing smoke automatically. Any env-var change, redeploy, database repair, migration rerun, or rollback requires separate approval.

## Production DB Identity Correction

Matt confirmed the production 1Password item now matches the correct Railway production Postgres card/service. The prior wrong-card ambiguity is resolved for secret identity. Earlier Production Gate 2 and PG-8E evidence was superseded until re-verified against this now-proven identity; corrected Gate 2 and PG-8E execute have now passed from owner-run signed-in terminal output.

Non-secret owner verification result:

```text
post_update_internal_exact_match=True
post_update_public_exact_match=True
internal_same_password=True
public_same_password=True
public_same_host=True
public_same_port=True
pgpassword_matches_internal=True
```

Interpretation:

- Production 1Password `DATABASE_URL` now exactly matches the correct Railway production internal URL.
- Production 1Password `DATABASE_PUBLIC_URL` now exactly matches the correct Railway production public/proxy URL.
- `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, and `PGDATABASE` now match the corrected internal URL.
- The internal/public production URLs share the same username, password, and database and use different hosts as expected.
- Staging does not need redo based on the read-only staging classification: staging remains a separate staging-only target, and the issue was the production 1Password item pointing at the wrong Railway production DB card/service.

Corrected production database checks:

- Corrected Production Gate 2 verification: PASS against the now-proven production DB identity.
- PG-8E production execute: PASS against the now-proven production DB identity.
- Post-cutover integrity verification: PASS.

Credential exposure:

- Live production DB credentials were exposed during troubleshooting outside this runbook.
- Production DB credential rotation: PASS.
- Matt rotated the Railway production Postgres credentials after the exposure and updated the production 1Password DB fields.
- Rotated production 1Password fields are internally consistent: `DATABASE_URL`, `DATABASE_PUBLIC_URL`, and `PGHOST`/`PGPORT`/`PGUSER`/`PGPASSWORD`/`PGDATABASE` all describe the same production database identity through the expected internal and public Railway endpoints.
- Rotated `scripts/templates/production-op.env.tpl` delivery path works; `scripts/check_production_op_secrets.sh` passed without printing secret values.
- Template-based post-rotation production DB verification passed: connection PASS, `alembic_version=20260523_0001`, `count_mismatches={}`, public FK constraints validated, and provenance orphan counts are zero.
- Do not paste, print, commit, or store the old or rotated values in docs, chat, scripts, tests, local env files, or shell history.

## Gate 3 Corrected PG-8E Execute Result

Owner manually ran PG-8E execute from a signed-in terminal using Docker + `op run` against the corrected Railway production DB identity. No secrets are recorded here.

Execute result:

```text
mode=execute
count_mismatches={}
target_provenance_issues=[]
sqlite_foreign_key_issue_count=0
source_validation.provenance_issues=[]
audit_events_copied_count=0
copied_counts_matched_target_counts=true
```

Postcheck result:

```text
alembic_version=20260523_0001
postgres_unvalidated_fk_constraint_count=0
data_provenance_orphan_count=0
rule_provenance_orphan_count=0
```

Production target counts after corrected PG-8E execute:

```text
accounts=1
audit_events=0
buildings=2
compatibility_issues=2
consent_records=0
data_provenance=7
design_equipment=5
design_goal_presets=2
electrical_panels=1
energy_system_designs=2
equipment_locations=3
equipment_products=8
estimated_pathways=2
facts=0
geometry_obstructions=0
homes=1
load_templates=6
loads=3
roof_planes=0
rule_provenance=25
scenario_revisions=2
scenarios=2
source_documents=5
takeoff_line_items=2
takeoff_requests=1
```

## Current Status

- Production Postgres Gate 1: PASS.
- Production workspace: `0xsk8babylon's Projects`.
- Production project: `rep-postgres-production`.
- Production project ID: `c71285ee-5be0-451c-ab39-c023cf4a9a98`.
- Production environment: `production`.
- Production environment ID: `f47e9ce9-e868-4089-9865-bb5b54ae59e1`.
- Production Postgres service: `Postgres`.
- Production Postgres service ID: `13a5b2f6-3983-4ff5-92a7-69d4b09e0372`.
- Logical DB / app target label: `rep_pg8e_production`.
- Production Postgres deployment status: `SUCCESS`.
- Production Postgres instance status: `RUNNING`.
- Production Postgres volume state: `READY`.
- Production DB vars exist: yes, values redacted.
- Production DB identity correction: PASS by owner non-secret exact-match checks against the correct Railway production Postgres card/service.
- Prior wrong-card ambiguity: RESOLVED for production 1Password identity; corrected Gate 2 and PG-8E execute have now been re-verified against the corrected identity.
- Production credential rotation: PASS after credential exposure; rotated production 1Password DB fields are internally consistent.
- Rotated 1Password/template path: PASS; `scripts/check_production_op_secrets.sh` passed and template-based post-rotation DB verification reached production without printing secrets.
- Production Alembic Gate 2 status against corrected DB identity: PASS.
- 1Password `op run` delivery path with disposable Docker API dependency install and in-memory `postgresql+psycopg://` URL rewrite: reached Alembic invocation without printing secrets.
- Production Alembic upgrade command result against corrected DB identity: PASS.
- Production DB connection verification against corrected DB identity: PASS.
- Production Alembic version against corrected DB identity: `20260523_0001`.
- Production schema/tables against corrected DB identity: PASS.
- PG-8E production execute against corrected DB identity: PASS.
- Post-rotation production schema/data integrity verification: PASS with `alembic_version=20260523_0001`, `count_mismatches={}`, public FK constraints validated, and provenance orphan counts zero.
- PG-8E production `count_mismatches`: `{}`.
- PG-8E production provenance orphan checks: PASS.
- PG-8E production public FK validation: PASS.
- Production FastAPI deployed: no.
- Production FastAPI env vars set: no.
- Public production smoke run: no.
- Production secrets touched or printed by this runbook: no.
- Staging resources changed by this runbook: no.
- Push approved or performed by this runbook: no.

## Next Required Approval

Next gate is either OAuth/auth foundation or Production FastAPI runtime env-var wiring, each only by separate owner approval. Public production smoke also remains separate approval after runtime wiring.
