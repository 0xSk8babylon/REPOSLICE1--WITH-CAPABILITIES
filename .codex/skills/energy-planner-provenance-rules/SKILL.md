---
name: energy-planner-provenance-rules
description: Protect provenance and trust signaling in residential-energy-planner. Use when changing recommendation outputs, inspectability metadata, trust badges, UI/API explanation layers, or any deterministic planning logic whose basis, limits, or traceability could become less explicit.
---

# Energy Planner Provenance Rules

## Purpose

Preserve traceability and honest planning-only framing while recommendation logic expands.

## Required Rules

- provenance visibility must remain explicit
- rule and source traceability must remain inspectable
- deterministic calculation stays separate from AI explanation
- planning-only limitations stay visible near the affected output
- no wording or API shape may imply engineering certification
- provenance expansion should be additive rather than replacing existing fields
- trust-boundary clarity must stay consistent across UI and API

## Enforcement Workflow

1. List the user-visible outputs affected by the change.
2. For each output, confirm the deterministic basis, trust state, assumptions, and missing-data posture remain visible.
3. If the change alters reasoning or selection behavior, expose the basis through inspectability rather than hidden heuristics.
4. Narrow any wording that could imply approval, certification, or final engineering readiness.
5. Prefer additive provenance fields or notes over rewrites that erase current lineage surfaces.

## Required Checks

- users can trace the result back to structured inputs or rule keys
- planning estimates are still labeled as planning estimates
- confidence does not exceed available evidence
- UI and API both preserve trust-boundary clarity where the output is consumed

## Escalate If

- a changed result can no longer explain why it was chosen
- engineering certainty is implied without new evidence
- provenance would have to be hidden to keep the implementation simple
