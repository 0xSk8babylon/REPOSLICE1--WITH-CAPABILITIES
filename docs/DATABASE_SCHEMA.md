# Database Schema

## Current Persistence Model

SQLite + SQLAlchemy is the active local development persistence stack.

DB file:

- `apps/api/data/residential_energy_planner.sqlite3`

Migration scaffold:

- `apps/api/alembic.ini`
- `apps/api/migrations/`

Postgres foundation:

- `DATABASE_URL` may point at a SQLAlchemy-supported Postgres URL in a future approved environment.
- `postgres://` URLs are normalized to `postgresql://` before SQLAlchemy engine creation.
- SQLite-only engine arguments are applied only to SQLite connections.
- Alembic uses the same dialect-aware engine argument helper as runtime setup.
- For non-SQLite databases, startup `create_all` and demo seeding default to disabled unless explicitly opted in with `DATABASE_CREATE_ALL_ON_STARTUP=true` and `DATABASE_SEED_DEMO_DATA_ON_STARTUP=true`.
- A Python Postgres DBAPI dependency is present for future approved checks. No production service, secret, schema migration, data migration, or runtime persistence switch is introduced by this foundation.

## Core Tables

- `accounts`
- `homes`
- `buildings`
- `electrical_panels`
- `loads`
- `energy_system_designs`
- `equipment_products`
- `equipment_locations`
- `design_equipment`
- `compatibility_issues`
- `scenarios`
- `takeoff_requests`
- `takeoff_line_items`
- `estimated_pathways`
- `load_templates`
- `design_goal_presets`
- `source_documents`
- `data_provenance`
- `rule_provenance`

## Ownership Scaffolding

- `homes.account_id` is nullable for now.
- Account-level role, subscription status, and plan type are persisted but not enforced.

## Demo Versus Real Data

Many persisted planning records include `data_origin` with these intended values:

- `demo_seed`
- `user_created`
- `imported`
- `verified`

This is the minimum separation contract, not a complete governance system.

## Migration State

- Alembic exists as a lightweight baseline.
- Current baseline revision creates or drops tables from metadata.
- The current baseline is not the final durable Postgres initial schema strategy.
- Migration discipline is still early-stage and should become normal practice before larger schema changes.
