# Database Schema

## Current Persistence Model

SQLite + SQLAlchemy is the active local development persistence stack.

DB file:

- `apps/api/data/residential_energy_planner.sqlite3`

Migration scaffold:

- `apps/api/alembic.ini`
- `apps/api/migrations/`

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
- Migration discipline is still early-stage and should become normal practice before larger schema changes.
