# Secrets Management Runbook

## Purpose

This runbook defines the current secrets boundary for local development, local smoke tests, Railway staging, Railway production, CI, and future providers. It is documentation-only and does not approve Railway provisioning, production deployment, migrations, auth providers, storage providers, or new secrets.

## Current Loader Behavior

- Backend settings are loaded by `apps/api/app/core/config.py` through `pydantic-settings`.
- The backend reads standard environment variables only. It does not import or depend on 1Password, Infisical, Railway, or provider-specific secrets SDKs.
- `APP_ENV` is an environment selector for runtime intent. Current expected values are `local`, `test`, `staging`, and `production`; it does not select a secrets provider.
- `DATABASE_URL` is optional. When it is empty or unset, the API uses local SQLite at `DATA_DIR` plus `DATABASE_FILE`.
- Postgres URLs are supported when `DATABASE_URL` is explicitly set. `postgres://` URLs are normalized to `postgresql://`.
- For SQLite, startup table creation and demo seeding default to enabled.
- For non-SQLite databases, startup table creation and demo seeding default to disabled unless explicitly enabled. Managed staging and production must keep both disabled.
- The root API diagnostic response uses the redaction helper in `apps/api/app/core/database.py` for the database URL.
- Alembic reads the same settings in `apps/api/migrations/env.py`. Any migration command therefore targets whatever `DATABASE_URL` is present in that process.

## Secret Classes

- `APP_ENV`: non-secret environment selector. Keep it aligned with the runtime target so logs and diagnostics can distinguish local, test, staging, and production runs.
- `DATABASE_URL`: secret when it contains managed database credentials. Local placeholder Compose values are development-only and must not be reused outside local Docker.
- `VITE_API_BASE_URL`, `VITE_API_USER_ID`, and `VITE_API_HOME_ACCESS`: frontend development variables. The current `VITE_API_USER_ID` and `VITE_API_HOME_ACCESS` values are local scaffold headers, not production auth.
- `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`: local Docker service variables in `compose.postgres.yml`. They are placeholders for local development only.
- Auth local/test toggles: `AUTH_ALLOW_SCAFFOLD_HEADERS` and `AUTH_ALLOW_FAKE_OIDC_TOKENS` are non-secret booleans for explicit local/test-only behavior. Keep both false for staging and production.
- Future auth/session secrets: `JWT_SECRET`, `SESSION_SECRET`, provider issuer/client credentials, and signing keys are not currently implemented and must not be introduced without owner-approved auth/security scope.
- `SECRET_KEY`: not currently implemented. Reserve only for a future framework or session mechanism that explicitly requires it; do not add it to runtime without an owner-approved auth/security scope.
- Future storage/provider secrets: bucket names, access keys, provider API keys, CRM keys, utility/provider keys, and webhook signing secrets are not currently implemented and must remain absent until approved.
- Railway platform variables: `RAILWAY_*` values are managed by Railway and should not be committed, copied into chat, or mirrored into `.env`.

## Local Development

Use SQLite by default.

Required:

```text
APP_ENV=local
DATABASE_URL=
```

Optional:

```text
DATA_DIR=apps/api/data
DATABASE_FILE=residential_energy_planner.sqlite3
DEBUG=true
VITE_API_BASE_URL=http://localhost:8000
VITE_API_USER_ID=demo_user
VITE_API_HOME_ACCESS=home_001
```

Rules:

- Keep real local secret source material outside the repo. Preferred local convention: `~/.secrets/residential-energy-planner/`.
- Repo-local `.env`, `apps/api/.env`, or `apps/web/.env.local` files are gitignored runtime delivery files only, not the source of truth.
- Do not commit real local env files, credentials, or private config directories.
- Do not use local scaffold auth headers as production authentication.
- Do not enable fake OIDC bearer tokens outside explicit local/test behavior.
- Do not place Railway, production Postgres, provider, or API-key material in repo docs.

## Local Smoke And Test Databases

Use one-shot shell variables for explicit, approved Postgres checks. Do not make Postgres the default by writing it into committed files.

Required for Postgres smoke:

```text
APP_ENV=test
DATABASE_URL=<local disposable Postgres URL>
DATABASE_CREATE_ALL_ON_STARTUP=false
DATABASE_SEED_DEMO_DATA_ON_STARTUP=false
```

Rules:

- Use disposable local database names for smoke and rehearsal targets.
- Run migrations only when the specific target and command are approved.
- Do not run migrations against production.
- Do not commit local Postgres URLs to `.env`, docs, tests, or scripts.
- Stop local Docker services without deleting volumes unless cleanup is explicitly approved.

## Railway Staging

Railway staging is the next intended managed Postgres target only after owner approval. Current approved documentation names the staging Postgres service `rep-postgres-staging` in Railway environment `staging`, with logical app target label `rep_pg8e_staging`.

Required app variables for a future approved staging FastAPI service:

```text
APP_ENV=staging
DATABASE_URL=<Railway-managed staging Postgres connection string>
DATABASE_CREATE_ALL_ON_STARTUP=false
DATABASE_SEED_DEMO_DATA_ON_STARTUP=false
DEBUG=false
```

Rules:

- Do not create Railway resources without explicit approval.
- Do not deploy FastAPI to Railway without explicit approval.
- Do not run PG-8E migration against Railway without explicit approval.
- Do not print or copy the resolved Railway connection string into chat, docs, logs, or commits.
- Prefer Railway-managed variable references inside Railway over copying resolved credentials into local files.
- Keep staging variables separate from production variables.

## Railway Production

Production provisioning, migration, deployment, env-var wiring, and smoke remain separated by approval gate. The current planning boundary is documented in `docs/railway-production-postgres.md`; it does not approve production resource creation, migrations, data copy, FastAPI deployment, env-var wiring, smoke, push, or new secrets.

Required production variables when production is later approved:

```text
APP_ENV=production
DATABASE_URL=<Railway-managed production Postgres connection string>
DATABASE_CREATE_ALL_ON_STARTUP=false
DATABASE_SEED_DEMO_DATA_ON_STARTUP=false
DEBUG=false
```

Production rules:

- Use a distinct Railway production environment and distinct production Postgres service.
- Owner must manually capture production `DATABASE_URL`, `DATABASE_PUBLIC_URL`, and `PG*` values into 1Password through the Railway dashboard; do not print or copy them through chat, docs, commits, logs, or repo-local env files.
- Never reuse staging database credentials in production.
- Never point production at local Docker, Supabase staging, or disposable rehearsal databases.
- Do not run migrations or data copy until a production migration plan is approved.
- Do not expose database diagnostics beyond redacted connection summaries.
- Do not bundle production Postgres creation, Alembic upgrade, PG-8E data migration, FastAPI deploy/env-var wiring, and public smoke into one approval.

## CI Secrets

Current GitHub Actions CI does not require application secrets.

Current CI assumptions:

- Backend tests run with default SQLite behavior.
- Security scan uses GitHub-provided `secrets.GITHUB_TOKEN`.
- Frontend build uses default Vite values unless the workflow is changed later.

Rules:

- Do not add `DATABASE_URL` or provider secrets to CI unless a test or deploy plan explicitly requires them.
- If future CI database tests are approved, use CI-scoped disposable credentials only.
- Keep deployment secrets out of pull-request workflows from untrusted forks.

## Source Of Truth And Delivery Layers

Current intended ownership:

- 1Password is the owner-controlled source of truth for real secrets.
- `~/.secrets/residential-energy-planner/` is the preferred external local working path for any owner-managed local export or notes that should not live in the repo.
- Railway environment variables are deployed runtime delivery for Railway-hosted services.
- Local `.env` files are gitignored local/runtime delivery.
- `.env.example` is the non-secret contract.
- Future Infisical adoption should sync or deliver the same variable names rather than changing backend code.

Rules:

- Do not import 1Password or Infisical SDKs into FastAPI.
- Do not require FastAPI to know where a secret came from.
- Do not copy real 1Password, Railway, or future Infisical values into committed files or chat.
- Do not create repo-local `secrets/`, `.secrets/`, `env/`, `credentials/`, or private config directories for real values.
- Treat env var names as the stable contract and provider tooling as replaceable delivery infrastructure.

## 1Password Gate 2 Runtime Delivery

Production Gate 2 should use 1Password secret references as the local runtime delivery layer, not a maintained `production.env` file. The checked-in template `scripts/templates/production-op.env.tpl` contains only `op://` references and non-secret flags.

For local Alembic access to Railway production Postgres, the template maps:

```text
DATABASE_URL="op://TwinEnergy/j3qbtqgq3ywnrem3hxxcx2ngle/DATABASE_PUBLIC_URL"
```

This intentionally exposes the Railway public connection string to Alembic as `DATABASE_URL` only inside the `op run` subprocess. Backend and Alembic code remain provider-neutral because they continue to read standard environment variables.

Before any approved Gate 2 execution, run the redacted preflight:

```bash
scripts/check_production_op_secrets.sh
```

The preflight verifies `op` auth, item existence by item ID, and required field-title presence without printing secret values. A later approved Gate 2 command should use this shape:

```bash
op run --env-file scripts/templates/production-op.env.tpl -- bash -lc 'cd apps/api && python3 -m alembic upgrade head'
```

Do not run that command until Production Alembic Gate 2 execution is explicitly approved.

## Files Intentionally Ignored By Git

The current `.gitignore` intentionally excludes:

```text
.env
.env.local
.env.*
apps/api/.env
apps/api/.env.local
apps/web/.env.local
apps/api/data/
SESSION_HANDOFF.md
```

Notes:

- `apps/api/data/` includes local SQLite databases, local backups, and other runtime data.
- `SESSION_HANDOFF.md` is local continuity state and is intentionally untracked.
- `.env.example` is safe to track because it contains placeholders only.

## Known Risks And Blockers

- Session-report email delivery and its Resend secret were removed. Do not add provider email keys back to repo-local env files without a new owner-approved setup.
- The root API response includes a redacted database URL. Redaction is present, but production exposure of diagnostics should be reviewed before public deployment.
- Auth foundation slice 1 is provider-neutral and app-owned. It adds local/test-only scaffold and fake-OIDC toggles, but no provider SDKs, provider secrets, app sessions, or production auth runtime wiring. Future production auth will require provider choice, secret inventory, rotation policy, storage location, and deployment-specific documentation.
- Railway CLI/config is not present in the repo state captured by `docs/railway-staging-postgres.md`; Railway resource discovery and provisioning remain blocked on owner approval.

## Rotation And Incident Rules

- If a secret is printed, committed, pasted into chat, or sent to the wrong service, treat it as compromised and rotate it at the source.
- Remove leaked material from current files immediately, but do not rely on git history edits as the only remediation.
- Prefer replacing credentials over trying to prove a leaked credential was unused.
- Update this runbook when a new provider, deploy target, or auth/session mechanism is approved.

Production DB credential rotation record:

- Live production DB credentials were exposed during production DB identity troubleshooting.
- Production DB credential rotation: PASS.
- Matt rotated the Railway production Postgres credentials and updated the production 1Password DB fields from the correct Railway production Postgres card/service.
- Post-rotation non-secret verification passed: `DATABASE_URL` is a valid internal Railway URL, `DATABASE_PUBLIC_URL` is a valid public Railway proxy URL, internal/public URLs share username/password/database, and `PGHOST`/`PGPORT`/`PGUSER`/`PGPASSWORD`/`PGDATABASE` match the internal URL.
- Rotated template delivery path works: `scripts/check_production_op_secrets.sh` passed, and `scripts/templates/production-op.env.tpl` resolved the rotated production DB connection for verification without printing secret values.
- Template-based post-rotation DB verification passed with `production_db_connection=PASS`, `alembic_version=20260523_0001`, `count_mismatches={}`, validated public FK constraints, and zero data/rule provenance orphans.
- Do not paste, print, commit, or store old or rotated credential values in docs, chat, scripts, tests, local env files, or shell history.
- Production FastAPI deploy, Railway runtime env-var wiring, and public production smoke still require separate owner approval.

## Related Files

- `.env.example`
- `.gitignore`
- `compose.postgres.yml`
- `apps/api/app/core/config.py`
- `apps/api/app/core/database.py`
- `apps/api/migrations/env.py`
- `.github/workflows/ci.yml`
- `docs/postgres-local-dev.md`
- `docs/railway-staging-postgres.md`
- `docs/railway-production-postgres.md`
