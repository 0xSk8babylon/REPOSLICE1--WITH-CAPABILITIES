# API Contracts

## Versioning Policy

- Legacy unprefixed routes remain supported for compatibility.
- `/api/*` is the preferred route base for current and future frontend work.
- `/api/v1` is reserved for the first explicit breaking version if needed later.
- Current policy is additive-first.

## Core GET Contracts In Use

- `GET /api/homes`
- `GET /api/homes/all`
- `GET /api/buildings`
- `GET /api/panels`
- `GET /api/loads`
- `GET /api/loads/summary`
- `GET /api/load-templates`
- `GET /api/designs`
- `GET /api/product-library`
- `GET /api/compatibility-rules/issues`
- `GET /api/compatibility-rules/evaluate/{design_id}`
- `GET /api/scenarios`
- `GET /api/scenarios/compare`
- `GET /api/equipment/locations`
- `GET /api/estimated-pathways`
- `GET /api/takeoffs/current`
- `GET /api/takeoffs/generate/{design_id}`
- `GET /api/design-advisor/summary/{design_id}`
- `GET /api/ai-context/design/{design_id}`
- `GET /api/estimates/placeholder`

## Current Write Contracts

- `POST/PATCH /api/accounts`
- `POST/PATCH /api/homes`
- `POST/PATCH /api/buildings`
- `POST/PATCH /api/panels`
- `POST/PATCH /api/loads`
- `POST/PATCH /api/designs`
- `POST/PATCH /api/product-library`
- `POST/PATCH /api/scenarios`
- `POST/PATCH /api/equipment/locations`
- `POST/PATCH /api/estimated-pathways`

## Compatibility-Sensitive Contracts

- `GET /api/homes`
  - frontend depends on nested buildings and panels
- design/advisor/context endpoints
  - frontend assumes stable design IDs and current persisted demo data
- scenario and takeoff endpoints
  - current UI treats placeholder score/cost content as planning-level outputs only
- `GET /api/scenarios/compare`
  - now returns additive comparison metadata, rankings, warnings, completeness, and lineage summaries on top of scenario records
