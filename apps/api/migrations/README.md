# Migrations

This is a lightweight Alembic setup for local SQLite development.

## Current Policy

- Existing local databases may need an explicit reset/reseed when schema-hardening changes land.
- Current migration support is intended to stabilize development flow before editable user workflows begin.
- Future revisions should move toward explicit per-change migrations instead of metadata-wide bootstrapping.
- Postgres is foundation-ready at the SQLAlchemy URL/configuration layer only. Do not treat a Postgres URL as approved production persistence until the driver dependency, target environment, migration plan, rollback posture, and secret handling are explicitly reviewed.

## Common Commands

```bash
cd apps/api
alembic upgrade head
alembic current
alembic history
```

If using the local `.vendor` dependency folder:

```bash
cd apps/api
PYTHONPATH=.vendor alembic upgrade head
```
