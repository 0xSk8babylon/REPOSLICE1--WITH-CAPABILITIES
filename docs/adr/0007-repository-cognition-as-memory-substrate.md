# ADR 0007: Repository Cognition As Memory Substrate

## Status

Accepted

## Context

The project has relied on long restore prompts and chat continuity to preserve architecture, doctrine, and implementation intent. That does not port cleanly across ChatGPT, Claude, Gemini, Codex, Cursor, or future orchestration agents.

## Decision

The repository should increasingly function as the project memory substrate. Canonical doctrine, cognition layers, continuity flow, governance boundaries, provenance posture, topology lifecycle, and orchestration readiness should live in repo documents and project skills rather than transient conversation history.

## Tradeoffs

- Adds documentation surface area.
- Requires discipline to avoid duplicating state summaries.
- Improves restore portability and reduces chat-context dependence.
- Makes architecture boundaries more inspectable before runtime systems exist.

## Rejected Alternatives

- Keep using large restore prompts as the primary memory mechanism.
- Collapse doctrine into one monolithic project brief.
- Encode future orchestration behavior before authority boundaries are defined.

## Migration Implications

No runtime migration is required. Documentation routing must be updated so future agents load compact project skills and task-specific references instead of sweeping all docs.

## Continuity Implications

Root discovery files remain the restore entry point. New canonical cognition docs and `.codex/project-skills/` provide portable route maps for future agents.

## Orchestration Compatibility

This decision prepares for future orchestration-safe context envelopes by separating canonical facts, derived estimates, advisory outputs, operational state, and historical records before runtime orchestration exists.
