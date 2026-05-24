# System Boundaries

## Frontend

- Presents and edits structured state.
- Surfaces trust posture, planning guidance, and relationship context.
- Must not become the owner of domain truth.

## Backend

- Owns persistence, rules, advisor logic, provenance summaries, and AI grounding context.
- Should preserve inspectable deterministic behavior for planning calculations and explanation inputs.
- Should keep GET contracts stable unless coordinated changes are intentional.

## AI Context

- Must be generated from structured current state.
- Must not rely on freeform guesses or undocumented assumptions.
- Must preserve uncertainty markers and source posture.

## Takeoffs

- Remain transient until versioned snapshot rules are intentionally designed.
- Represent derived planning views, not procurement-grade records.

## Advisor Issues

- Represent planning guidance and surfaced tradeoffs.
- Do not represent engineering approval, code sign-off, or permit readiness.

## Boundary Discipline

- Structured facts decide.
- Deterministic rules interpret.
- AI explains.
- UI reveals state and tradeoffs.
