# Auto-Loop Roadmap Runner Packets

## Created

2026-06-13

## Source

Matt-provided Auto-Loop Roadmap Runner prompt for B1 through B7/Phase 21, A2, A4, C1/Phases 18-19, and deferred B3 evidence intake.

## Operating Boundary

- OwnerWorkflows controls generic automation, staging, commit, hard-stop, secret, dependency, and closeout rules.
- Residential Energy Planner controls product scope, Energy Twin doctrine, API/runtime boundaries, and continuity docs.
- No push is allowed.
- No migrations, auth or permission enforcement, lockfile rewrites, dependency installs, real `.env` changes, destructive deletion, production deploy, billing, real customer data, external paid services, GitHub Actions/CI changes, or work outside the active packet is allowed.

## Ordered Loop Packets

### B1 - Fact Lifecycle

Add the provenance-aware fact lifecycle layer for home-scoped facts: fact value, unit, source, confidence tier, verification time, optional expiry/decay policy, derived-from parent IDs, effective confidence on read, and calculation gap reporting. This packet may add backend API/schema/model/service/test/docs work, but must not add Alembic migrations, auth, permission enforcement, delete workflows, external services, or frontend behavior.

### B2 - NEC 220 Load Calculation

Implement NEC 220.82 and 220.83 calculation endpoints that consume B1 facts, return stage-by-stage VA/amp results, propagate confidence, substitute only documented defaults, and report gaps. This packet touches electrical logic and must preserve the non-authoritative engineer/AHJ boundary.

### B4 - Calculator Primitives

Add pure-function calculator primitives for backfeed, supply-side tap, coupling, critical-load identification, tier-1 shading derate, and solar production estimation with optional injected PVWatts behavior. This packet must keep primitives state-free and network-free unless the caller injects a mocked client.

### B5 - 8760 Hourly Simulation

Add the request-time hourly simulation engine for solar, battery, load profile, rate structures, imports/exports, outage coverage, and cycle counting. This packet must keep energy conservation test coverage and preserve confidence lineage.

### Phase 20 - Geometry

Add roof-plane and obstruction storage/query surfaces plus geometry export for future HomeDiagram consumption and per-plane shading input. This packet is additive and does not gate B6.

### B6 - Sizers

Add battery, generator, V2H, and transformer-headroom sizers that consume B4/B5/B1 inputs and return recommendation bands plus assumptions, corrections, and inherited confidence. This packet must not bake SGIP, 25D, 48E, quote, pricing, eligibility, or savings claims into sizing outputs.

### B7 / Phase 21 - Graph Comparator And Smart Panel Scoring

Add typed multigraph comparator foundations, candidate configuration scoring, and smart-panel planning score metadata. This packet must not create operational control, final design approval, product ranking as sales direction, or utility authority.

### A2 - Auth, Object-Level Authorization, Audit Logging

Hard stop under current automation rules. This packet requires explicit owner-controlled auth/security/permission-enforcement approval outside Auto-Loop Roadmap Runner.

### A4 - Privacy / CCPA

Hard stop under current automation rules if it requires deletion workflows, consent enforcement, privacy enforcement, or auth/security coupling. Requires separate owner decision.

### C1 / Phases 18-19 - UI On Heart-Quill Shell

Frontend work behind A2 auth. Hard stop until A2 is separately approved and implemented.

### B3 - Hardened Evidence Intake

Deferred until C1 capture UI and hardened untrusted-upload boundaries are approved. Hard stop if it requires upload security, external services, secrets, or auth/permission enforcement.

## Carry-Forward Practice

When a packet names a protected future capability, split the packet into the smallest safe additive slice and stop before migrations, auth/security/permission enforcement, destructive deletion, external services, dependency installs, lockfile rewrites, or production operations.
