# Architecture

## Monorepo Shape

- `apps/api` contains the planning API, domain schemas, service placeholders, and seed data.
- `apps/web` contains the application shell and workflow pages.
- `docs` contains product, architecture, and roadmap documents.

## Boundary Rules

- Structured facts belong in domain models and product records.
- Compatibility logic belongs in rules and services.
- Calculations belong in deterministic service layers.
- Explanations are composed from facts, rule outputs, and calculations.
- AI context is assembled from authoritative structured state and explicit policies.

## Current Implementation Choice

FastAPI and React/Vite were chosen to keep the scaffold approachable, modular, and easy to evolve without committing early to heavy infrastructure.

