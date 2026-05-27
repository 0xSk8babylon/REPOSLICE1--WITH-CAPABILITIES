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
