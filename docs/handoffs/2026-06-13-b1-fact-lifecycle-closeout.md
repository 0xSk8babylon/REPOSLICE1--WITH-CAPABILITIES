# B1 Fact Lifecycle Closeout

## Summary

B1 Fact Lifecycle is implemented as the first Auto-Loop Roadmap Runner packet. It adds a provenance-aware, home-scoped fact lifecycle backend layer with persisted facts, read-time effective confidence decay, derived-from parent fact IDs, and named calculation gap reporting.

## Runtime Endpoints

- `GET /api/homes/{home_id}/facts`
- `POST /api/homes/{home_id}/facts`
- `PATCH /api/homes/{home_id}/facts/{fact_id}`
- `GET /api/homes/{home_id}/facts/gaps/{calculation_name}`

## Runtime Files

- `apps/api/app/facts/__init__.py`
- `apps/api/app/facts/schemas.py`
- `apps/api/app/facts/router.py`
- `apps/api/app/services/facts.py`
- `apps/api/app/core/models.py`
- `apps/api/app/core/repository.py`
- `apps/api/app/core/types.py`
- `apps/api/app/main.py`
- `apps/api/tests/test_facts.py`

## Completed Scope

- Added `FactSource`, `FactConfidenceTier`, and `FactDecayPolicy` enums.
- Added a SQLAlchemy `Fact` model tied to `home_id`.
- Added fact create/update/read APIs under `/api/homes/{home_id}/facts`.
- Server-side create/update resets `verified_at`.
- Added derived fact parent IDs through `derived_from`.
- Added read-time effective confidence scoring and tiering.
- Added no/slow/standard/fast decay policies and key-based default policy selection.
- Added expiry handling that degrades effective confidence to missing.
- Added named calculation gap reporting for `nec_220_82` and `battery_backup_sizing`.
- Added focused tests and API/continuity docs.

## Verification

- `python3 -m py_compile app/facts/schemas.py app/facts/router.py app/services/facts.py app/core/models.py app/core/repository.py app/core/types.py app/main.py tests/test_facts.py` passed.
- `python3 -m unittest tests/test_facts.py` passed with `8 tests OK`.
- `python3 -m unittest tests/test_facts.py tests/test_system_visibility.py` passed with `17 tests OK`.
- `git diff --check` passed.

## Boundary

B1 does not add Alembic migrations, auth/security changes, permission enforcement, delete endpoints, frontend behavior, external source lookups, external services, dependency installs, lockfile rewrites, GitHub Actions changes, billing, production deployment, push behavior, NEC calculation execution, pricing, proposal generation, field verification, engineering approval, AHJ approval, utility approval, `twin_id`, graph engine behavior, or operational control.

The fact gap endpoint reports fact availability and effective-confidence gaps only. It does not approve engineering inputs, perform NEC calculations, validate field measurements, or certify readiness.

## Remaining Risks

- No Alembic migration file exists for the new `facts` table because migrations are a hard stop in the active Auto-Loop Roadmap Runner. Existing startup and tests use `Base.metadata.create_all` for missing tables.
- Existing local SQLite databases may require normal app startup table creation before the fact endpoints can persist records.
- Fact values are accepted as structured JSON values; truth verification remains dependent on source/provenance and future evidence intake.
- Auth, permission enforcement, and audit logging remain deferred and are not part of B1.

## Next Action

Run B1 verification, commit the completed loop if verification passes, then stop before B2 if NEC calculation implementation requires a protected electrical/compliance decision beyond the approved packet boundary.
