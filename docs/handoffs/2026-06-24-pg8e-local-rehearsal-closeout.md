# PG-8E Local Rehearsal Closeout

## Summary

PG-8E local SQLite-to-Postgres rehearsal passed against owned Docker Postgres only.

## Scope

- Local Docker Postgres target only
- Disposable rehearsal database: `rep_pg8e_rehearsal`
- Existing PG-8E SQLite backup as source
- Alembic upgrade head against the disposable rehearsal DB
- Migration dry-run and execute with committed PG-8E tooling
- Independent row-count, provenance orphan, sample ID, and FastAPI smoke validation

## Inputs

- Backup path: `apps/api/data/backups/residential_energy_planner.pg8e.20260623T070201Z.sqlite3`
- Backup checksum: `b9cf2b94c3a13b4a66352688a8a19338ef2a6aba86b184d9d218a1e4a4056c9d`
- Migration tooling commit: `ea76986080b364c76333ba346d44586d366dd4ee` (`Add PG-8E SQLite to Postgres migration tooling`)
- Execution environment: ephemeral `python:3.11-slim` containers on local Docker network `residential-energy-planner-postgres-dev`

## Results

- Alembic upgrade: PASS
- Alembic revision: `20260523_0001`
- Migration dry-run: PASS
- Migration execute: PASS
- `count_mismatches`: `{}`
- SQLite foreign-key issue count: `0`
- Provenance orphan checks: PASS
- `data_provenance` source-document orphans: `0`
- `rule_provenance` source-document orphans: `0`

## Row Counts

```text
accounts=1
source_documents=5
design_goal_presets=2
load_templates=6
homes=1
audit_events=0 before smoke, 3 after smoke
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

## Sample IDs

```text
accounts=account_demo
homes=home_001
energy_system_designs=design_001,design_002
scenarios=scenario_001,scenario_002
equipment_products=product_ecoflow_system,product_eg4_hybrid,product_enphase_micro
source_documents=source_doc_demo_seed_catalog,source_doc_internal_rulebook,source_doc_pathway_walkthrough_note
```

## FastAPI Smoke

FastAPI TestClient ran against `rep_pg8e_rehearsal` with `DATABASE_CREATE_ALL_ON_STARTUP=false` and `DATABASE_SEED_DEMO_DATA_ON_STARTUP=false`.

```text
/                       200
/api/accounts           200
/api/homes/all          200
/api/designs            200
/api/scenarios          200
/api/product-library    200
```

## Boundaries Preserved

- Railway touched: no
- Supabase touched: no
- Production SQLite touched: no
- Production Postgres touched: no
- Vault/secrets touched: no
- Frontend Supabase SDK introduced: no
- Repo code changed during rehearsal: no
- Push: no
- `rep_pg8_seed_smoke` touched: no
- `residential_energy_planner` touched: no writes, schema changes, or data operations

## Repo State

- Branch: `fix/github-workflow`
- Status after rehearsal: clean
- Ahead of origin by: 28

## Next Safe Step

Keep `rep_pg8e_rehearsal` available for inspection until Matt explicitly approves disposable rehearsal DB cleanup. After documentation is committed, the next deployment step should remain local-first unless Matt separately approves a managed Postgres or Railway deployment action.
