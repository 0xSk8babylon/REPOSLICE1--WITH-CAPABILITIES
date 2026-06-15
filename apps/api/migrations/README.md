# Migrations

This is a lightweight Alembic setup for local SQLite development and future approved Postgres migration checks.

## Current Policy

- Existing local databases may need an explicit reset/reseed when schema-hardening changes land.
- Current migration support is intended to stabilize development flow before editable user workflows begin.
- Future revisions should move toward explicit per-change migrations instead of metadata-wide bootstrapping.
- Postgres is foundation-ready at the SQLAlchemy URL/configuration and DBAPI-driver layer only. Do not treat a Postgres URL as approved production persistence until the target environment, migration plan, rollback posture, and secret handling are explicitly reviewed.
- Alembic uses the same dialect-aware engine argument helper as runtime setup. SQLite-only connection arguments stay limited to SQLite, and future Postgres migration checks avoid SQLite-only connection arguments.
- The existing baseline revision is metadata-wide and should not be treated as the final durable Postgres initial schema strategy.

## Common Commands

```bash
cd apps/api
python3 -m alembic upgrade head
python3 -m alembic current
python3 -m alembic history
```

If using the local `.vendor` dependency folder:

```bash
cd apps/api
PYTHONPATH=.vendor python3 -m alembic upgrade head
```
