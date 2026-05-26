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
  - `GET /api/design-advisor/summary/{design_id}` now includes additive `recommendation_profiles` guidance
  - `recommendation_profiles.profiles[*]` now include additive planning-only battery sizing estimate ranges
  - `recommendation_profiles.profiles[*]` now include additive planning-only solar sizing and recovery estimate ranges
  - `recommendation_profiles.profiles[*]` now include additive `architecture_fit` tradeoff summaries, warnings, and status tied to recorded equipment mix and backup-path posture
  - `recommendation_profiles.inverter_system_architecture` now includes additive AC-coupled vs hybrid posture, pathway suitability, coexistence assumptions, planning-only consistency output, confidence framing, and inspectability metadata
  - `recommendation_profiles.reasoning_graph` now includes additive recommended-profile dependency nodes and provenance-linked reasoning edges connecting loads, backup scope, panel/service posture, inverter/system architecture, battery posture, and solar posture
  - `recommendation_profiles.profiles[*]`, `battery_sizing_estimate`, and `solar_sizing_estimate` now include additive inspectability metadata for basis signals, estimated inputs, incomplete inputs, and planning-only warnings
  - `recommendation_profiles.backup_load_selection` now includes additive selected-scope reasoning, recorded-load coverage, outage posture, confidence posture, planning-gap warning, and inspectability metadata for deterministic backup/load selection
  - `solar_sizing_estimate` now also includes additive site-aware planning fields such as the base solar range, site capacity posture, shading caution, seasonal production caution, and install realism caution
  - `solar_sizing_estimate.roof_geometry_readiness` now includes additive roof-data completeness, roof-measurement confidence, measured-vs-estimated status, future geometry source placeholders, and missing-geometry warnings
  - `recommendation_profiles.panel_service_architecture` now includes additive panel/service posture, backup-architecture recommendation, architecture-consistency output, upgrade cautions, readiness notes, and planning-only inspectability metadata
- scenario and takeoff endpoints
  - current UI treats placeholder score/cost content as planning-level outputs only
- `GET /api/scenarios/compare`
  - now returns additive comparison metadata, rankings, warnings, completeness, and lineage summaries on top of scenario records
- `GET /api/loads`
  - now returns additive `provenance_summary` metadata on each load record
- `GET /api/estimated-pathways`
  - now returns additive `provenance_summary` metadata on each pathway record
