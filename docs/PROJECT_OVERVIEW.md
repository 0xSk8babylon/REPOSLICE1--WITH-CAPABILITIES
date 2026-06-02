# Project Overview

## Product Definition

`residential-energy-planner` is a living home energy system planning platform. It is not just a solar proposal tool. The platform is intended to persist home context over time so homeowners and contractors can model a house, compare architectures, understand expansion pathways, and eventually generate takeoffs and estimates from structured state.

The Residential Energy Planner is the first application built on top of the Residential Energy Twin. The Twin is the core asset. The planner's strategic role is to create, maintain, and enrich trusted Twin records through useful planning workflows.

Current positioning is the Trusted Residential Energy Record. The long-term end state is a Residential Infrastructure Registry, and the long-term vision is a Residential Infrastructure Network. These are doctrine and positioning concepts only; they do not imply current utility authority, operational control, registry runtime, network runtime, or safety approval capability.

## Current Technical Shape

- Monorepo
- FastAPI backend in `apps/api`
- React/Vite frontend in `apps/web`
- SQLite local persistence via SQLAlchemy
- Seed-backed demo mode for first-run continuity

## Product Principles

- The Residential Energy Twin is the durable core asset.
- The Residential Energy Planner is the first application and adoption path.
- The house model persists and grows over time.
- Structured facts are the authority layer.
- Rules, calculations, and explanations are separate concerns.
- AI must be grounded in structured persisted context.
- Placeholder logic is acceptable for planning prototypes, but it must be labeled as such.
- Persistence, provenance, permissions, safety, interoperability, and lifecycle continuity take precedence over one-off project-workflow optimization.
- The long-term moat is Twin adoption, trusted records, permissioned provenance, continuity, interoperability, ecosystem participation, and network effects rather than planner workflow ownership or protocol ownership alone.

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
