# Migration Discipline

## Current Posture

SQLite is the local development system of record. Alembic exists as a baseline scaffold, but migration discipline is still early.

Postgres foundation is configuration and DBAPI-driver only at this stage. Non-SQLite connections do not auto-create or auto-seed tables unless explicitly opted in, and no production Postgres service, secret, schema migration, or persistence switch is approved by that foundation.

## Required Practice

- Treat schema changes as compatibility-sensitive.
- Prefer additive migrations.
- Document irreversible changes before implementation.
- Keep existing GET contracts stable unless a breaking version boundary is explicit.
- Preserve seed continuity and local database recoverability.
- Update `docs/DATABASE_SCHEMA.md`, API contracts, and continuity docs when persistence shape changes.

## Compatibility Surfaces

- existing local SQLite databases
- first-run seed runtime
- frontend API client expectations
- scenario revision lineage
- provenance records
- historical handoffs and restore docs

## Non-Goals

- no production migration framework hardening yet
- no tenant migration automation yet
- no destructive cleanup unless explicitly approved
