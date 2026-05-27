# Canonical Terminology

## Canonical Object

A persisted or explicitly documented object that the system treats as authoritative for planning state.

Examples: home, building, panel, load, design, product record, scenario, scenario revision, equipment location, estimated pathway, ADR.

## Derived Estimate

A deterministic calculation or classification produced from canonical objects and explicit rules.

Examples: backup capability score, expansion readiness score, recommendation profile, battery sizing range, solar sizing range, roof-readiness posture, scenario comparison ranking.

Required posture: planning-only, inspectable, reproducible from structured inputs.

## Transient Recommendation

An advisory view generated for the current live state without snapshot authority.

Examples: current advisor summary, transient takeoff output, current profile comparison view.

Required posture: useful for planning, not a stored engineering conclusion.

## Operational State

The runtime or workflow state needed to operate the application or restore the project.

Examples: current branch, migration status, seed state, local SQLite state, active task, latest handoff.

Required posture: concrete and current; do not infer from stale session memory.

## Revision Graph

The lineage of saved planning states over time.

Current status: lightweight immutable scenario revisions exist. They preserve compact planning-state framing, not full advisor payload replay.

Future status: revision graphs may link canonical state changes, derived output snapshots, provenance deltas, and decision rationale.

## Continuity Lineage

The chain of documentation that allows future agents to reconstruct project state.

Current entry points: `AGENTS.md`, `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, repo skills, project skills, selected continuity docs.

## Deployment Lineage

The record of what code, schema, seed state, and configuration produced a running environment.

Current status: not formalized beyond local SQLite, seed runtime, and git history.

Future status: environment manifests, migration revisions, seed versions, and deployment notes should be linked without adding premature production infrastructure.

## Orchestration-Safe Abstraction

A structured representation that can be consumed by future DER, utility, contractor, or agent workflows without exposing unsupported authority.

Required traits:

- stable identity
- explicit source and trust posture
- clear advisory vs authoritative status
- no hidden AI-derived facts
- no permit, interconnection, dispatch, or compliance claim unless a future authority layer supports it

## Data Classification

The visibility and sensitivity category attached to a field, object, derived output, or advisory explanation.

Current status: classification is a documentation and design boundary only. Runtime RBAC, tenant isolation, export scoping, and policy enforcement are not implemented.

Initial categories:

- `public_reference`: low-risk reference material that can be shown broadly when provenance is visible.
- `planning_private`: homeowner, site, design, load, scenario, or estimate data that should be treated as private planning context.
- `contractor_scoped`: recorded facts, assumptions, and planning-only derived estimates prepared for a future contractor-facing view.
- `utility_scoped`: minimized, source-linked site or interconnection context reserved for a future utility-facing abstraction.
- `operational_control`: device, dispatch, credential, audit, or failure-handling data required before operational behavior can exist.
- `internal_governance`: project, rule, provenance, doctrine, migration, and continuity material used to operate the repository safely.

Required posture: classification must not be confused with trust. A private field can be unverified, a public reference can have weak provenance, and a contractor-scoped output can still be planning-only.

## API View Boundary

A future contract shape that exposes a scoped subset of canonical objects, derived estimates, provenance, and advisory text for a specific audience or workflow.

Current status: existing API responses are functional product contracts, not authorization boundaries. They should not be treated as RBAC, tenant isolation, utility submission packets, or contractor approval packages.

Required posture:

- expose only the minimum fields needed for the view
- include authority layer, data classification, provenance summary, and trust-zone posture
- keep advisory text separate from canonical facts and derived estimates
- avoid operational, permit, utility, or engineering claims unless a future authority layer explicitly supports them

## RBAC Boundary

A future enforcement model that may control who can read, edit, export, or operationalize classified data and scoped API views.

Current status: deferred. Account, role, and subscription fields exist as scaffolding only and do not enforce access decisions.

Required posture: documentation may prepare RBAC concepts, but product behavior must not imply multi-user security, contractor authorization, utility submission authority, or operational-control permission until enforcement exists.
