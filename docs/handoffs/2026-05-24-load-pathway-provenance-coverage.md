# 2026-05-24 Load And Pathway Provenance Coverage

## What Changed

- Added additive `provenance_summary` metadata to `GET /api/loads` and `GET /api/estimated-pathways`.
- Extended provenance summaries to aggregate confidence levels in addition to source types, trust states, verification posture, and unverified fields.
- Seeded first-pass pathway provenance records plus a routing-note source document for demo continuity.
- Surfaced load and pathway provenance details in the Home Model UI so trust badges are backed by inspectable lineage where records exist.

## Architecture Impact

- Runtime architecture did not change.
- No schema migration was required because the existing provenance tables and repository queries already supported the new summaries.

## Compatibility Impact

- API changes are additive only.
- Existing clients should continue to work because the entity shape only gained optional `provenance_summary` fields.
- Existing local databases will not automatically gain the new seeded pathway provenance unless reseeded or updated manually.

## Next Recommended Step

Extend the same provenance-summary pattern into more design, scenario-input, and broader home-model facts so comparison, advisor, and AI layers rely on stronger field-level lineage.

## Risks And Gaps

- Most design and scenario inputs still lack equivalent field-level provenance coverage.
- Current local demo DBs may show empty pathway lineage until reseeded.
- Trust visibility is stronger, but verification depth remains partial and must not be overstated.
