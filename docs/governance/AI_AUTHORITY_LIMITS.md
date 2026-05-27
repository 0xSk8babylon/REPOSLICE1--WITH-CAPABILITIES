# AI Authority Limits

## Core Rule

AI can explain, summarize, compare, and suggest next questions. AI cannot create canonical facts, override deterministic rules, assert verification, or authorize operational action.

## Allowed AI Outputs

- explain current structured state
- summarize deterministic outputs
- surface missing inputs and uncertainty
- suggest planning questions
- translate technical posture into user-appropriate language
- help navigate tradeoffs already represented in structured state

## Prohibited AI Outputs

- engineering approval
- permit or code compliance claims
- utility interconnection readiness
- dispatch or control authorization
- manufacturer fact verification without provenance
- hidden product selection as canonical state
- inferred site truth without recorded source

## Grounding Requirements

Every AI-facing context should preserve:

- source object identity
- authority layer
- trust zone
- data classification
- data origin
- confidence posture
- missing inputs
- rule outputs used
- planning-only limitations

## Future Agent Boundary

Future orchestration agents must consume structured context envelopes. They should not scrape prose summaries as their source of truth.

Future AI-facing, contractor-facing, utility-facing, or orchestration-facing API views must remain scoped representations, not evidence of current RBAC or operational authorization. Role or audience labels may describe intended consumers, but they do not grant authority until an enforcement layer, audit model, and compatibility plan exist.
