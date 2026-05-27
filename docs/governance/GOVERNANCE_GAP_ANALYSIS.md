# Governance Gap Analysis

## Mature Doctrine

- Structured data decides; AI explains.
- Planning completeness is not engineering compliance.
- Takeoffs remain transient before versioned snapshot semantics.
- Trust visibility precedes stronger estimate claims.
- The living house model is the core domain.
- Products and pathways are distinct but interdependent concerns.

## Duplicated Concepts

- Architecture boundaries appear in `docs/ARCHITECTURE.md`, `docs/architecture.md`, and `docs/session-continuity/architecture-principles.md`.
- Roadmap status appears in root state docs, `docs/NEXT_STEPS.md`, `docs/ACTIVE_TASKS.md`, and `docs/session-continuity/current-roadmap.md`.
- Restore procedure appears in `AGENTS.md`, `discovery-index.md`, `SESSION_HANDOFF.md`, and `docs/session-continuity/continuity-workflow.md`.

Recommended posture: keep root files as discovery surfaces, use subdirectories for canonical definitions, and avoid moving legacy files until references are updated deliberately.

## Missing Canonical Definitions

- canonical object
- derived estimate
- advisory output
- operational state
- revision graph
- continuity lineage
- deployment lineage
- orchestration-safe abstraction
- scoped intelligence exposure

Initial definitions now live in `docs/architecture/CANONICAL_TERMINOLOGY.md`.

## Authority Boundary Gaps

- Field-level provenance is still partial.
- Verification status can be mistaken for engineering validity.
- Scenario revisions do not yet store full advisor payloads or replayable reasoning.
- Deployment lineage is not yet formalized.
- Model-agnostic restore relies on human agents honoring the discovery layer.

## Orchestration-Readiness Gaps

- No DER dispatch, utility integration, or operational-control contract exists.
- No contractor-safe packet boundary exists.
- No utility-safe abstraction exists.
- No deployment manifest links code revision, schema revision, seed revision, and trust posture.
- No explicit AI visibility matrix defines which facts future agents may see, summarize, or act on.

## Preservation Rules

- Do not introduce fake completeness to close documentation gaps.
- Do not add RBAC, orchestration behavior, or utility workflows before contracts exist.
- Prefer explicit boundary documents over runtime abstractions until implementation pressure justifies code changes.
