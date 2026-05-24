# Trust And Provenance Philosophy

## Core Position

Stronger claims require stronger lineage. If provenance is partial, the product should be explicit about that limit rather than compensating with confidence language.

## Data Origin Meanings

- `demo_seed`: seeded continuity data for first-run planning, not factual authority
- `user_created`: entered by a user, still requiring normal skepticism and verification
- `imported`: brought in from an outside source, not automatically verified
- `verified`: explicitly verified according to the system's verification posture
- `derived_estimate`: generated from rules or calculations, not direct observed fact
- `placeholder`: illustrative or provisional content that must remain visibly labeled

## Doctrine

- Source lineage should become stronger before stronger claims are made.
- Derived estimates must expose both basis and uncertainty.
- Manufacturer data must not be treated as verified until explicitly verified.
- Provenance should support AI grounding, advisor trust, future auditability, and user education.
- Verification status and visible trust posture are related but not interchangeable concepts.

## Architectural Implications

- Provenance belongs in structured persistence, not only in prose.
- Derived views should carry basis metadata where possible.
- Trust visibility should appear where decisions are made, not only in backend internals.
