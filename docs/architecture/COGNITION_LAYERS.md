# Project Cognition Layers

## Purpose

This document defines how repository knowledge is separated so future agents can restore project understanding without depending on prior chat context.

## Layer Model

### Canonical Knowledge

Authoritative project facts and decisions.

- persisted domain models and schema contracts
- accepted ADRs
- root discovery files
- current API and persistence contracts
- explicit doctrine under `docs/philosophy/`

Canonical knowledge may be changed only through deliberate edits that update the affected contracts, continuity files, and ADRs when the change alters architectural intent.

### Derived Intelligence

Deterministic outputs computed from canonical or recorded state.

- advisor recommendation profiles
- planning completeness and maturity signals
- scenario comparison summaries
- transient takeoff views
- provenance summaries
- structured reasoning graphs

Derived intelligence must expose inputs, assumptions, confidence posture, and missing-data conditions where users or downstream agents make decisions.

### Advisory Knowledge

Guidance generated from canonical and derived layers.

- AI explanations
- recommendation copy
- UX warnings
- planning notes
- next-step suggestions

Advisory knowledge is not source of truth. It can explain or prioritize, but it cannot create product facts, engineering authority, site truth, or operational authorization.

### Operational Knowledge

Instructions for safely working on the repository.

- `AGENTS.md`
- `.codex/skills/*`
- `.codex/project-skills/*`
- `docs/continuity/*`
- handoff files
- migration and closeout workflows

Operational knowledge controls restore and implementation discipline. It must stay compact enough for model-agnostic onboarding.

### Historical Knowledge

Records that explain prior work but are not the primary restore surface.

- dated handoffs
- session logs
- older continuity notes
- superseded planning docs

Historical knowledge should clarify lineage and tradeoffs. It should not override current canonical state unless explicitly promoted.

## Authority Order

1. Persisted structured state and schema contracts
2. Accepted ADRs and doctrine
3. Current API contracts
4. Deterministic service outputs with inspectability metadata
5. Continuity and roadmap docs
6. Handoffs and session logs
7. Advisory text and AI-generated explanations

When layers conflict, preserve the higher-authority layer and record the mismatch before changing behavior.

## Portability Rule

Every future agent should be able to start with:

```text
Load project skills before implementation.
```

The repository must then route that agent toward the smallest sufficient doctrine, state, and contract set.
