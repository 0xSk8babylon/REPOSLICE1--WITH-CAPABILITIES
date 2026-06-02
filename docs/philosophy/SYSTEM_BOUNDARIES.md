# System Boundaries

## Frontend

- Presents and edits structured state.
- Surfaces trust posture, planning guidance, and relationship context.
- Must not become the owner of domain truth.
- Must present the planner as an application over the Residential Energy Twin, not as the durable asset itself.

## Backend

- Owns persistence, rules, advisor logic, provenance summaries, and AI grounding context.
- Should preserve inspectable deterministic behavior for planning calculations and explanation inputs.
- Should keep GET contracts stable unless coordinated changes are intentional.
- Should strengthen the Residential Energy Twin as the trusted record without implying that current planner records are a canonical runtime Twin implementation.

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

- The Residential Energy Twin is the core asset.
- The Residential Energy Planner is the first application.
- Structured facts decide.
- Deterministic rules interpret.
- AI explains.
- UI reveals state and tradeoffs.
- Safety, permissions, provenance, interoperability, and lifecycle continuity remain first-class boundaries.
- Registry and network concepts are long-term doctrine, not current runtime capability.
