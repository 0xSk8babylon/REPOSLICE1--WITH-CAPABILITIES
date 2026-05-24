# Project Overview

## Product Definition

`residential-energy-planner` is a living home energy system planning platform. It is not just a solar proposal tool. The platform is intended to persist home context over time so homeowners and contractors can model a house, compare architectures, understand expansion pathways, and eventually generate takeoffs and estimates from structured state.

## Current Technical Shape

- Monorepo
- FastAPI backend in `apps/api`
- React/Vite frontend in `apps/web`
- SQLite local persistence via SQLAlchemy
- Seed-backed demo mode for first-run continuity

## Product Principles

- The house model persists and grows over time.
- Structured facts are the authority layer.
- Rules, calculations, and explanations are separate concerns.
- AI must be grounded in structured persisted context.
- Placeholder logic is acceptable for planning prototypes, but it must be labeled as such.

## Current Delivery Phase

The repo has completed Phase 2A persistence hardening and moved beyond the Phase 2B editable-workflow milestone into the current Phase 2D/2E layer. Core editable workflows now exist for the home model, loads, panels, designs, scenarios, equipment locations, estimated pathways, design equipment, trust visibility, advisor intelligence, and first-pass provenance.

## Explicitly Deferred

- Authentication and authorization
- Billing and subscription enforcement
- NEC-compliance logic
- Permitting workflows
- Full provenance tracking
- Full audit/change history
- Production deployment hardening
