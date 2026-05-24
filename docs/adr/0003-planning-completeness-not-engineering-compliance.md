# ADR 0003: Planning Completeness Is Not Engineering Compliance

## Status

Accepted

## Context

The platform now exposes design completeness and maturity signals to support planning workflows and scenario comparison.

## Decision

Completeness scoring and design maturity represent planning readiness only. They do not indicate NEC compliance, permit readiness, engineering approval, or installation sign-off.

## Consequences

- UI and AI language must preserve the planning-only boundary.
- Future sessions must not reinterpret completeness metrics as code or engineering authority.
- Additional readiness models should stay explicitly scoped.
