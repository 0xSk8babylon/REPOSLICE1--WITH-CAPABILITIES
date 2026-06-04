---
name: codex-automation-governance
description: Use when Matt asks Codex to automate repeatable engineering workflow blocks in residential-energy-planner while preserving assessment, implementation, verification, commit, closeout, and Matt approval gates.
---

# Codex Automation Governance

## Purpose

Route repeatable Codex engineering workflows without expanding authority. This skill defines how Codex works; repo docs define what Codex is working on; prompts define the currently approved slice.

Do not hardcode phase schedules, roadmap order, or current implementation targets here. Phase-specific state belongs in `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, phase charters, and handoffs.

## Permanent Matt Approval Gates

Never do these without explicit Matt approval:

- `git push`
- migrations
- auth, security, or permission enforcement changes
- deleting files
- rewriting architecture doctrine
- changing phase scope
- touching unrelated repos
- adding external services or secrets
- broad refactors
- billing or payment logic
- production deployment
- destructive commands

If a requested automation block needs one of these actions, stop and report the blocked boundary, completed work, and decision needed from Matt.

## Assessment-Only Slice Workflow

Use when Matt asks for assessment, inventory, planning, or smallest-boundary identification.

1. Inspect only the relevant code, docs, contracts, and tests.
2. Identify the smallest additive boundary.
3. List files likely to change.
4. List files not to touch.
5. Propose schema, service, router, and test plan when relevant.
6. Report risks, blockers, deferred capabilities, and approval gates.
7. Do not edit files.
8. Wait for Matt approval before implementation.

## Approved Implementation Slice Workflow

Use only after Matt approves a concrete implementation slice.

1. Restate the approved boundary.
2. Touch only approved files.
3. Preserve additive API evolution unless Matt approved a breaking change.
4. Preserve deterministic runtime behavior.
5. Preserve provenance, trust, assumption, limitation, and deferred-boundary visibility.
6. Avoid unrelated refactors and formatting churn.
7. Run appropriate verification.
8. Report changed files, verification, risks, and final status.
9. Wait for commit approval.

## Verification + Boundary Audit Workflow

Use after implementation or when Matt requests verification.

1. Run `git diff --check`.
2. Run appropriate compile, type, lint, or import checks.
3. Run focused tests for the touched surface.
4. Run full tests when practical.
5. Confirm final `git status --short`.
6. Audit that no forbidden boundaries were touched:
   - migrations
   - persistence
   - frontend
   - auth, security, or permission enforcement
   - exports
   - pricing
   - proposal generation
   - product selection
   - compatibility engines
   - economic reasoning
   - scenario simulation or comparison
   - graph engine
   - `twin_id`
   - marketplace behavior
   - operational behavior
   - unrelated repos or files
7. Audit that no prohibited capability claims were introduced:
   - scoring
   - ranking
   - pass/fail verdicts
   - approval claims
   - verification claims
   - AHJ or manual approval claims
   - contractor readiness claims unless explicitly approved
   - pricing, proposal, compatibility, export, simulation, or operational claims

## Commit Checkpoint Workflow

Use only after Matt separately approves committing.

1. Stage approved files only.
2. Run `git diff --cached --check`.
3. Use a clean, scoped commit message.
4. Commit locally.
5. Report commit hash.
6. Report final `git status --short`.
7. Do not push unless separately approved.

## Closeout Continuity Workflow

Use only when Matt chooses to stabilize or close out.

1. Update `PROJECT_STATE.md`.
2. Update `SESSION_HANDOFF.md`.
3. Update `discovery-index.md`.
4. Add a dated handoff under `docs/handoffs/`.
5. Record scope, changed files, verification, commit hash, risks, and next action.
6. Keep closeout docs-only unless Matt separately approves runtime or architecture changes.
