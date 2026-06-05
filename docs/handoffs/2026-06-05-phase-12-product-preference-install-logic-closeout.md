# Phase 12 Product Preference & Install Logic Closeout

## Summary

Phase 12 Block 1 runtime/tests are implemented in the working tree as an additive read-only backend/API slice.

Added `GET /api/product-preferences/homes/{home_id}` to expose product preference and install-logic guidance from existing planning context. The view is planning metadata only. It does not recommend final products, rank products, choose a best option, price work, procure equipment, generate a final BOM, or produce final electrical design.

## Scope

- Backend read-only product-preference response schemas.
- Backend read-only product-preference route.
- Request-time deterministic product preference/install-logic service.
- Router registration under `/api`.
- Composition from existing Phase 7 shared compatibility, Phase 8 topology takeoff, Phase 9 estimate readiness, and Phase 10 proposal option-set outputs.
- Source-limited unsupported categories with explicit missing inputs rather than inferred preferences.
- Homeowner-safe explanations and contractor-facing review prompts.
- Boundary flags for deferred and forbidden capabilities.
- Focused backend tests.
- Phase 12 continuity and API docs closeout.

## Endpoint Added

- `GET /api/product-preferences/homes/{home_id}`

## Product / Install Categories

- PV modules.
- Inverter topology.
- Microinverter / string / hybrid direction.
- AC-coupled vs DC-coupled battery direction.
- Partial-home vs whole-home backup direction.
- Gateway / transfer equipment implications.
- Backup loads panel implications.
- Monitoring / controls.
- EV charger readiness.
- Main service panel / subpanel implications.
- Aesthetic preference.
- Contractor-preferred product family.

Unsupported categories remain source-limited with explicit missing inputs.

## Runtime / Test Files Changed

- `apps/api/app/main.py`
- `apps/api/app/product_preferences/__init__.py`
- `apps/api/app/product_preferences/router.py`
- `apps/api/app/product_preferences/schemas.py`
- `apps/api/app/services/product_preferences.py`
- `apps/api/tests/test_product_preferences.py`

## Verification

- `python3 -m py_compile apps/api/app/product_preferences/schemas.py apps/api/app/product_preferences/router.py apps/api/app/services/product_preferences.py apps/api/tests/test_product_preferences.py` - passed.
- `cd apps/api && python3 -m unittest tests/test_product_preferences.py` - passed, 8 tests in `344.870s`.
- `git diff --check` - passed.

Broad backend discovery was not run because the focused Phase 12 suite took about 345s and prior adjacent full discovery timed out under the current cap.

## Boundary Preserved

Phase 12 remains read-only, additive, request-time derived, `home_id` anchored, deterministic, provenance-bearing, homeowner-safe, contractor-facing where appropriate, and non-authoritative.

Direct Phase 11 workflow rebuild is intentionally not used in runtime composition because it is expensive and unnecessary for Phase 12 category derivation. Phase 12 derives supported product/install categories from existing Phase 7, Phase 8, Phase 9, and Phase 10 outputs.

Phase 12 does not add final product recommendations, product ranking, best-option selection, pricing, live inventory, distributor quotes, procurement, purchase links, payments, final BOM, final electrical design, manufacturer certification, warranty claims, CRM handoff, runtime email automation, frontend work, persistence, migrations, writes, auth/security changes, permission enforcement, external services, secrets, push, graph behavior, `twin_id`, operational behavior, or source-of-truth mutation.

## Assumptions

- Existing Phase 7 through Phase 10 source views are authoritative over the Phase 12 derived layer.
- Product/install categories are fixed and sorted deterministically.
- Unsupported categories should be surfaced as source-limited rather than inferred.

## Risks / Open Questions

- Focused Phase 12 tests are slow because the endpoint composes expensive existing derived-view stacks.
- Broad backend discovery remains too slow under the current cap.
- Phase 12 is not staged or committed yet.

## Decisions Needed From Matt

- Whether to stage the Phase 11 continuity repair, Phase 12 runtime/tests, and Phase 12 docs closeout.
- Whether to run a longer full backend test window before commit.

## Next Safe Boundary

Do not proceed into staging, commit, push, final product recommendations, product ranking, best-option selection, pricing, live inventory, distributor quoting, procurement, purchase links, payments, final BOM, final electrical design, manufacturer certification, warranty claims, CRM handoff, runtime email automation, frontend work, persistence, migrations, writes, auth/security changes, permission enforcement, external services/secrets, graph behavior, `twin_id`, or operational behavior without Matt approval.
