---
name: energy-planner-runtime-invariants
description: Protect deterministic runtime behavior and architectural invariants in residential-energy-planner. Use when changing recommendation logic, resilience calculations, sizing behavior, advisor outputs, API contracts, or adjacent planning heuristics that could drift core system behavior.
---

# Energy Planner Runtime Invariants

## Purpose

Protect the deterministic planning architecture while recommendation and sizing logic are refined.

## Required Invariants

- structured data stays authoritative
- deterministic recommendation outputs remain deterministic for the same inputs
- AI explains results and boundaries but does not decide calculations
- API evolution stays additive unless a breaking change is explicitly approved
- sizing systems do not gain hidden coupling through convenience logic
- resilience calculations remain inspectable deterministic rules
- panel/service posture remains deterministic and separately grounded
- unrelated heuristic drift is not acceptable collateral damage

## Enforcement Workflow

1. Identify which deterministic service outputs the change touches.
2. Map the exact structured inputs and rule paths that drive those outputs.
3. Keep refinement local to that path instead of rebalancing adjacent heuristics.
4. Check that battery, solar, panel/service, and resilience layers remain intentionally separated unless the change explicitly requires a bounded interface between them.
5. If an additive API field is needed, keep existing contracts stable and document the addition.

## Required Checks

- same inputs still resolve to the same outputs
- no new AI-dependent calculation path appears
- no hidden heuristic changes leak into unrelated sizing layers
- resilience and panel/service logic remain deterministic and inspectable
- existing GET contracts remain compatible

## Escalate If

- the refinement requires breaking an existing contract
- deterministic outputs would depend on hidden mutable state
- a nearby sizing system must be reworked to make the change function
