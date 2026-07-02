# ADR 0008: Twin Test And Capability Formula As Core Doctrine

## Status

Accepted

## Context

The root `ARCHITECTURE.md`, removed in the 2026-07 documentation collapse and preserved in git history and the owner's strategy vault, contained two foundational doctrine items that existed nowhere else in the repository.

This ADR rescues them into the surviving canon so they remain binding on design decisions.

## Decision

### The Canonical Twin Test

Every design decision affecting the twin must pass this test:

> **"If this application disappeared tomorrow, would the twin still exist?"**

The twin, the structured record of a home's energy identity including capacity, headroom, installed equipment, capabilities, and provenance, must remain a portable, meaningful object independent of this application's UI, API, or runtime.

The application renders and edits the twin; it does not own it. Any change that couples the twin's meaning to application-specific logic, routes, or display code fails the test and must be reworked.

### The Capability Formula

Usable grid capacity is defined as:

> **Technical Capability + Customer Permission + Availability = Usable Grid Capacity**

All three terms are required:

- **Technical Capability** - the home can physically perform the action, based on factors such as panel headroom, battery discharge rating, and inverter capacity.
- **Customer Permission** - the homeowner has consented to that capability being used, such as through program enrollment or authorization grants.
- **Availability** - the capability is operable right now, based on factors such as state of charge, equipment online state, and curtailment state.

Capacity lacking any one term is not usable capacity and must not be represented, aggregated, or sold as such.

Features that model, report, or broker capacity must track all three terms with provenance.

## Consequences

- The Twin Test constrains schema and API design: twin data structures must be exportable and self-describing, aligned with the portable capacity object and energy passport work.
- The Capability Formula constrains VPP enrollment, capacity intelligence, and any future data products: three-term verification is a correctness requirement, not a reporting nicety.
- Consumers of this doctrine include the permissions/grant model, provenance layer, and any Stage 4 aggregate reporting.
