# Migrations

This is a lightweight Alembic setup for local SQLite development.

## Current Policy

- Existing local databases may need an explicit reset/reseed when schema-hardening changes land.
- Current migration support is intended to stabilize development flow before editable user workflows begin.
- Future revisions should move toward explicit per-change migrations instead of metadata-wide bootstrapping.

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

