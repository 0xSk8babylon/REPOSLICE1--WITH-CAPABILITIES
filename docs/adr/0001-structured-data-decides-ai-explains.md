# ADR 0001: Structured Data Decides, AI Explains

## Status

Accepted

## Context

The product includes AI-facing explanation layers, but the repository architecture is built around persisted structured planning state and deterministic services.

## Decision

Structured state, persisted facts, and deterministic rule outputs are authoritative. AI may explain, summarize, and guide, but it must not become the source of domain truth.

## Consequences

- AI grounding must use current persisted state.
- Backend services should keep rules and calculations inspectable.
- Future sessions should resist shortcuts that replace domain structure with prompt-only behavior.
