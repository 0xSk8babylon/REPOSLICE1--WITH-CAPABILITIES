# Railway Staging Postgres Runbook

## Current Railway State

- Repo Railway config: none found.
- Railway CLI: not installed on PATH.
- Visible Railway environment variables: no `RAILWAY_*` variable names visible in the local shell.
- Repo status at preflight: clean on `fix/github-workflow`, ahead of origin by 29.

## Proposed Staging Resource

- Railway environment: `staging`
- Railway Postgres service: `rep-postgres-staging`
- Logical DB / app target label: `rep_pg8e_staging`

This is a staging-only managed Postgres target. It is not a production database and should not be treated as a production cutover.

## Future FastAPI Environment Variables

When a staging FastAPI service is later approved, it should use Railway-managed Postgres connection settings with these app-level variables:

```text
DATABASE_URL
DATABASE_CREATE_ALL_ON_STARTUP=false
DATABASE_SEED_DEMO_DATA_ON_STARTUP=false
```

Do not print or commit resolved connection strings. Do not copy Railway secrets into the repo.

## Approval Gate

Owner approval is required before provisioning any Railway resource because provisioning happens outside the repo and may create managed infrastructure or cost.

Before provisioning, confirm:

- target environment is `staging`
- target service name is `rep-postgres-staging`
- target is PostgreSQL only
- no production environment, service, or database is selected
- no app deploy, migration, or data copy is being bundled into the provisioning step

## Guardrails

- Staging only.
- Do not create production Railway resources.
- Do not deploy FastAPI.
- Do not run PG-8E migration against Railway yet.
- Do not touch production SQLite.
- Do not touch production Postgres.
- Do not edit secrets or vault material.
- Do not introduce frontend Supabase SDKs.
- Do not push without explicit approval.

## Next Step

After owner approval, install or authenticate Railway tooling only as needed, link or select the intended Railway project/environment, and create exactly one staging PostgreSQL service named `rep-postgres-staging`. Stop after provisioning/preflight unless Matt explicitly approves the next step.
