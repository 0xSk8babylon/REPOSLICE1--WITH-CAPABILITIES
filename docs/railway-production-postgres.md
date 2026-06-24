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

Recommended production-only labels, not yet created or verified:

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

## Current Status

- Production Postgres created: no.
- Production Alembic upgrade run: no.
- PG-8E production data migration run: no.
- Production FastAPI deployed: no.
- Production FastAPI env vars set: no.
- Public production smoke run: no.
- Production secrets touched or printed by this runbook: no.
- Staging resources changed by this runbook: no.
- Push approved or performed by this runbook: no.

## Next Required Approval

Next approval should be for Gate 1 only: production Postgres creation planning/execution, with exact Railway target names confirmed before any managed resource is created.
