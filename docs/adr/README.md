# ADRs

## Purpose

Architecture Decision Records capture durable decisions that future sessions should preserve unless explicitly superseded.

## How To Use

- Read relevant ADRs before making architecture-shaping changes.
- Prefer adding a new ADR over silently changing doctrine.
- Treat ADRs as implementation constraints, not product-marketing language.

## Current ADR Index

- `0001-structured-data-decides-ai-explains.md`
- `0002-transient-takeoffs-before-versioned-snapshots.md`
- `0003-planning-completeness-not-engineering-compliance.md`
- `0004-trust-visibility-before-strong-estimate-claims.md`
- `0005-living-house-model-as-core-domain.md`
- `0006-pathways-and-products-both-matter.md`
- `0007-repository-cognition-as-memory-substrate.md`

## ADR Discipline

New or revised ADRs should state:

- intent
- tradeoffs
- rejected alternatives
- future implications
- migration implications
- continuity implications
- orchestration compatibility when relevant

ADRs should preserve architectural history. Do not silently rewrite accepted decisions to match current implementation convenience.
