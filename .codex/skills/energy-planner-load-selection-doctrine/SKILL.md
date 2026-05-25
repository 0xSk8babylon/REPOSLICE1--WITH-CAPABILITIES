---
name: energy-planner-load-selection-doctrine
description: Govern backup and load-selection refinement in residential-energy-planner. Use when changing how essential loads, backup loads, profile-aware prioritization, or backup-scope reasoning feed recommendation, battery, solar, or panel/service planning.
---

# Energy Planner Load Selection Doctrine

## Purpose

Keep backup-load refinement deterministic, inspectable, and tightly scoped.

## Required Doctrine

- load selection must be deterministic
- backup-scope reasoning must be explicit
- the selection basis must be inspectable
- profile-aware load prioritization is allowed only when the rule is explicit
- hidden heuristics are not acceptable
- battery and solar sizing compatibility must be preserved
- existing resilience behavior stays intact unless the refinement explicitly requires a bounded change
- inverter and generator scope must not expand during load-selection work

## Enforcement Workflow

1. Define the exact load-selection rule path before changing code.
2. Distinguish raw recorded load groups from the selected planning scope derived from them.
3. Make profile-aware prioritization explicit in rule logic and inspectability output.
4. Check how the new selected scope flows into battery, solar, and panel/service layers.
5. Reject opportunistic changes to inverter, generator, or unrelated resilience heuristics.

## Required Checks

- selected loads are explainable from recorded groups and explicit rules
- backup-scope reasoning is visible in the result or inspectability layer
- battery and solar estimates still consume a compatible deterministic scope
- panel/service posture does not silently inherit broader or narrower scope than intended
- no unrelated resilience logic changes piggyback on the refinement

## Escalate If

- selection behavior depends on undocumented tie-breakers
- the refinement requires inverter or generator logic to change
- compatibility with current battery or solar sizing cannot be preserved additively
