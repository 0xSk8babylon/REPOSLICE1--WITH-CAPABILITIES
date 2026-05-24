# Persistence Agent Plan

## Status

This document defines a future continuity agent. It is not implemented yet.

## Purpose

The persistence agent should maintain portable project memory across:

- ChatGPT/Codex session resets
- account switches
- subscription interruptions
- long implementation gaps
- multi-session engineering handoffs

## Responsibilities

- Update continuity docs when architecture, contracts, persistence, or roadmap status materially change.
- Record what is implemented versus what is still placeholder.
- Detect and summarize compatibility-sensitive changes.
- Preserve current next-step recommendations based on real repo state.
- Keep continuity memory concise, factual, and architecture-aligned.
- Track hardening changes such as migrations, API prefixes, and data-origin governance.

## Boundaries

- It may summarize and document the codebase.
- It may not redesign product architecture on its own.
- It may not create product policy that contradicts existing repo docs without explicit instruction.
- It may not infer implementation state from intention alone.
- It must treat the repository as source of truth, not prior chat memory.

## Safety Rules

- Never write code changes outside continuity/documentation scope unless explicitly instructed.
- Never delete continuity history simply to make docs shorter.
- Never claim features are implemented unless verified in the repo.
- Never rewrite roadmap status to make the project appear further along than it is.
- Never convert placeholder logic into “supported behavior” in documentation.

## When It Should Run

- After any meaningful backend architecture change
- After any API contract change
- After persistence/model changes
- After roadmap-shifting frontend work
- At the end of major implementation sessions
- Before a handoff when context-window loss is likely

## Files It Should Update

- `docs/session-continuity/project-state.md`
- `docs/session-continuity/architecture-principles.md`
- `docs/session-continuity/domain-map.md`
- `docs/session-continuity/current-roadmap.md`
- `docs/session-continuity/active-pressure-points.md`
- `docs/session-continuity/persistence-agent-plan.md`
- `docs/session-continuity/session-restore-template.md`

It may also update top-level `README.md` only when continuity-critical operating instructions materially change.

## What It Must Never Do

- Never mutate database records
- Never run destructive reseeds automatically
- Never add or remove migrations automatically
- Never change API contracts silently
- Never overwrite human-authored architecture decisions without preserving them
- Never present itself as a substitute for code review or engineering judgment

## Future Implementation Approach

- Read continuity docs first
- Read high-authority repo files second
- Compare documented state against actual repo state
- Produce targeted documentation deltas
- Require explicit invocation or post-session hooks rather than background autonomy

## Minimal Future Inputs

- repo tree
- current key backend/frontend entrypoints
- verification results
- known roadmap target
- any explicit user/developer decisions from the current session
