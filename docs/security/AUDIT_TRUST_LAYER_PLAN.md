# Audit / Trust Layer Plan

## Status

Docs-only planning approved by Matt on 2026-06-25.

This plan records the approved audit/trust direction on top of the completed provider-neutral auth foundation and account-membership ownership enforcement slices. It does not implement code, create migrations, alter production DB, wire provider SDKs, deploy, run smoke, wire Railway runtime variables, or push.

First implementation later should use a new explicit Alembic revision. Audit schema evolution must be additive and must preserve existing `audit_events` fields for compatibility.

## Approved Direction

Audit authority is app-owned.

OAuth/OIDC provider identity remains identity proof only. Provider claims must not assign audit authority, planner permissions, ownership, provenance authority, contractor authority, utility authority, privacy rights, or operational authority.

Approved trust path:

```text
OIDC provider identity
-> app-owned user
-> active app-owned account_membership
-> route/object authorization decision
-> audit event with app-owned actor and object scope
-> source/provenance references where relevant
```

Audit records should explain who attempted or performed an action, what object/scope was involved, what authorization decision occurred, and what source/provenance context was relevant. They should not claim source truth, field verification, engineering approval, legal authority, privacy compliance completion, or provider-side authorization.

## Current Findings

### Audit Events

Current `audit_events` fields:

- `id`
- `user_id`
- `home_id`
- `action`
- `method`
- `path`
- `status_code`
- `authorized`
- `reason`
- timestamps from `TimestampMixin`

Current weaknesses:

- `user_id` is a nullable string and is not a durable FK-style actor reference.
- There is no `actor_user_id` or `actor_identity_id`.
- There is no explicit `account_id`.
- There is no `object_type` / `object_id` pair for object-level decisions.
- There is no route template distinct from raw path.
- There is no request id or sanitized request context field.
- There is no structured auth source or role snapshot.
- There is no link to relevant data/rule/source provenance.
- `authorized` is string-based, not structured as a boolean/decision enum.
- Middleware writes audit events directly, so route-level permission decisions are not centrally described.
- Existing tests prove basic middleware writes, but not app-owned actor semantics or object/action consistency.

### Auth Principal

The provider-neutral `AuthPrincipal` now carries:

- app-owned `user_id`
- optional `identity_id`
- `provider`, `issuer`, and `subject` for identity provenance
- `auth_source`
- app-owned `account_ids`
- app-owned `account_roles`
- derived `allowed_home_ids`

This is the correct source for audit actor identity. Provider claims can explain how identity was proven, but must not define audit authority.

### Ownership Checks

The current first ownership boundary is active `account_memberships`. Implemented route filtering now covers high-risk homes, designs, scenarios, buildings, panels, loads, equipment locations, estimated pathways, compatibility routes, takeoffs, design advisor, AI design context, and owner-only privacy export/delete.

The audit layer should record decisions made from this app-owned authorization boundary. It should not duplicate business policy inside provider metadata.

### Provenance Tables

Current provenance tables:

- `data_provenance`: field/entity lineage through polymorphic `entity_type` / `entity_id`.
- `rule_provenance`: source/rule basis for deterministic rules and derived outputs.
- `source_documents`: source artifacts and verification status metadata.

Current provenance weaknesses:

- `/api/provenance` returns broad polymorphic records today and is not entity-aware filtered.
- `data_provenance` cannot be safely filtered by simple `home_id` because it may point to home-scoped, design-scoped, scenario-scoped, product/reference, or unknown entities.
- Rule/source provenance is reference-style today and should remain separate from authorization.

## Audit / Provenance Relationship

These tables have different jobs:

| Surface | Purpose | Authority Boundary |
| --- | --- | --- |
| `audit_events` | Actor/action/request/object decision ledger | App principal + app-owned authorization |
| `data_provenance` | Field/entity source lineage and trust state | Source lineage only, not permission authority |
| `rule_provenance` | Rule basis for derived outputs | Rule/source basis only, not permission authority |
| `source_documents` | Source artifact metadata | Reference/source metadata only |
| `auth principal` | Request-scoped app actor and memberships | Built from verified identity + app-owned tables |
| `permissions.py` | Authorization decision helpers | App-owned account/home/object relationships |

Audit records may reference provenance records when a read/write/reasoning event depends on source or rule lineage. Provenance records should not grant access, ownership, or privacy rights.

## Recommended Architecture

Add a central audit writer/service later, likely under `app/security/audit.py`.

Recommended service responsibilities:

- normalize actor context from `AuthPrincipal`
- normalize object scope from route/object resolvers
- record authorization decisions consistently
- preserve legacy audit field compatibility
- attach sanitized request context
- attach optional provenance references for derived/read/reasoning actions
- avoid secrets, raw bearer tokens, raw claims, request bodies with sensitive data, and provider tokens

Recommended event categories:

- `read`
- `write`
- `delete`
- `export`
- `consent`
- `auth`
- `authorization_denied`
- `derived_view_read`
- `reasoning_context_read`
- `privacy_action`

Recommended first implementation should keep middleware-level auditing but route sensitive/object-level decisions through the central audit writer.

## Additive Audit Schema Recommendations

First implementation should create a new explicit Alembic revision, likely after `20260625_0002_auth_foundation.py`.

Do not remove or rename existing `audit_events` columns.

Add nullable fields:

- `actor_user_id`: FK-style reference to app-owned `users.id` where compatible
- `actor_identity_id`: FK-style reference to `oauth_identities.id` where compatible
- `auth_source`
- `account_id`
- `object_type`
- `object_id`
- `route_template`
- `source_surface`
- `decision`
- `request_id`
- `event_context` JSON
- `provenance_refs` JSON

Compatibility notes:

- Existing rows can remain valid with null new fields.
- Keep legacy `user_id` until compatibility and reporting migration are explicitly planned.
- Prefer nullable FK-style references, but avoid blocking local/test scaffold audit records that have no durable app user/identity.
- If strict FK constraints conflict with legacy/scaffold behavior, use nullable indexed string columns first and document the tradeoff before implementation.
- `event_context` must be sanitized and should not store secrets, raw authorization headers, provider tokens, raw provider claims, full addresses unless deliberately approved, or full privacy export payloads.

## Entity-Aware Provenance Filtering Plan

When implemented, `/api/provenance` broad list should filter by accessible entities for the current principal.

Unknown entity types should deny or omit by default.

Recommended resolver shape:

```text
resolve_entity_scope(entity_type, entity_id)
-> scope_type: home | account | design | scenario | global_reference | unknown
-> account_id
-> home_id
-> allowed
```

Initial resolver map:

- Direct home scoped:
  - `home`
  - `building`
  - `electrical_panel`
  - `load`
  - `equipment_location`
  - `estimated_pathway`
  - `fact`
  - `roof_plane`
  - `geometry_obstruction`
- Design scoped:
  - `energy_system_design`
  - `design_equipment`
  - `compatibility_issue`
  - `takeoff_request`
  - `takeoff_line_item`
- Scenario scoped:
  - `scenario`
  - `scenario_revision`
- Reference/global:
  - `equipment_product`
  - `source_document`
  - `rule_provenance`
  - `design_goal_preset`
- Account-aware reference:
  - `load_template`, because `load_templates.account_id` exists and may need account filtering

Route behavior:

- If `entity_type` and `entity_id` are supplied, resolve the entity and require access.
- If only `entity_type` is supplied, return only records for accessible entities of that type.
- If no filter is supplied, return only records whose entity scopes resolve to accessible entities or approved global/reference scopes.
- Unknown or unresolved entity scopes should be omitted or denied by default, not returned broadly.

Performance note: broad `/api/provenance` filtering may need batching by entity type to avoid per-row resolver queries.

## Audit Behavior Plan

### Reads

Record reads for protected home/account/object routes at middleware or route boundary.

High-signal read events:

- home/object reads
- collection reads with scoped result counts
- privacy export
- design advisor / AI context reads
- provenance reads

Avoid logging full response payloads.

### Writes

Record attempted and successful writes for normal planner data:

- action
- actor
- account/home/object scope
- route template
- status code
- authorization decision
- sanitized change context such as affected fields, not raw full body by default

Viewer/member/owner role decisions should be derived from app-owned roles and may be recorded as sanitized role snapshots.

### Denials

Record:

- unauthenticated requests as `not_authenticated`
- authenticated but unauthorized requests as `denied`
- unknown object or null-account object decisions carefully, without leaking object data beyond route/object identifiers already in the request

Route-level permission denials should eventually call the same audit writer as middleware denials.

### Privacy Export / Delete

Privacy export and delete are owner-only in the current route layer.

Future audit behavior:

- record actor user and identity when available
- record home/account scope
- record `privacy.export` and `privacy.delete`
- preserve audit records after privacy delete
- sanitize/minimize `event_context`
- do not store exported payload, deleted data, raw address, or full consent body in audit context unless explicitly approved

Privacy delete posture: local app records may be deleted, but audit events should be retained as minimal compliance/security records. Retained audit records should minimize sensitive context and preserve only what is needed to prove action, actor, scope, and outcome.

### Consent Capture

First audit implementation should require current app principal for consent capture if feasible.

Consent audit should record:

- principal user
- consent home scope
- consent type and status
- action outcome

Existing `consent_records.user_id` remains string-based until a separate compatibility decision changes it. A future additive `actor_user_id` may be considered.

### Reasoning / Advisor Actions

Reasoning and advisor routes should be audited as derived-view or reasoning-context reads, not as engineering, legal, financial, or operational decisions.

Audit context may include:

- design/home scope
- rule keys or provenance refs used by the response where available
- source surface such as `design_advisor` or `ai_context`
- limitations that derived outputs are planning-only

Do not audit derived outputs as approvals, recommendations authority, utility authority, permit readiness, or field verification.

### Future Contractor / Utility Access

Future participant access should add explicit app-owned grant/share references before those participants receive scoped access.

Planned future fields may include:

- `grant_id`
- `participant_type`
- `participant_account_id`
- `shared_view_id`

Do not use provider org/group/role claims as contractor, utility, program, finance, insurance, or manufacturer access authority.

## Immutable / Append-Only Expectations

Audit events should be append-only in application behavior.

Allowed maintenance should be explicit and approval-gated:

- retention pruning, if legally/product-approved later
- context minimization or redaction for privacy safety
- operational repair only with documented owner approval

Normal product flows should not update or delete audit events.

## API Contract Impact

First implementation should not expose new audit query APIs unless separately approved.

Expected API contract updates later:

- `/api/provenance` becomes authenticated and entity-aware filtered.
- Privacy consent route may require current app principal.
- Existing protected routes may produce richer audit side effects without changing response shape.
- If request ids are added to responses/headers later, document that separately.

Existing compatibility-sensitive response bodies should remain additive-first.

## Test Strategy

Required tests for first implementation:

- legacy audit rows with null new fields still load
- audit event writes include `actor_user_id` for fake OIDC/app principal
- audit event writes include `actor_identity_id` where available
- local/test scaffold audit events are marked with `auth_source=local_test_headers`
- provider claims do not become audit authority
- middleware 401 and 403 events produce structured decisions
- route-level permission denials write audit events where implemented
- privacy export/delete write owner-only audit events
- privacy delete preserves audit records and keeps event context minimal
- consent capture requires current principal if implemented
- `/api/provenance` entity filter allows same-account records
- `/api/provenance` omits or denies cross-account and null-account entities
- unknown provenance entity types are denied/omitted by default
- source documents and rule provenance remain intentional reference surfaces

## Migration Recommendation

First implementation needs a new explicit Alembic revision because audit actor/schema hardening changes persisted shape.

Migration posture:

- additive only
- no destructive changes
- preserve `audit_events.user_id`
- nullable new columns
- indexes for actor, identity, account, object, decision, and request id where useful
- JSON fields for context and provenance refs if supported by existing project DB compatibility
- no production DB change without separate approval

No migration should be created during this docs-only planning step.

## Deferred Items

- new audit query APIs
- audit event admin UI
- normalized audit reference table
- consent record actor FK migration
- audit retention/deletion automation
- provider SDK wiring
- app sessions
- contractor/utility/program grants
- permissioned exports/share links
- production runtime env-var wiring
- production deploy/smoke
- address onboarding
- reasoning/planner intelligence expansion

## Risks And Blockers

- Existing audit rows have only legacy string fields.
- Local/test scaffold principals may not map to durable users.
- Entity-aware provenance filtering can be expensive if implemented as per-row lookups.
- Unknown provenance entity types are risky and must deny/omit by default.
- Privacy delete and audit retention need careful context minimization.
- Consent capture currently accepts a string `user_id`; requiring principal may be a behavior change for direct route calls/tests.
- Production DB has not been approved for the auth foundation migration or later audit migration.
- Provider choice and production OIDC runtime wiring remain unapproved.

## Decisions Needed Before Implementation

- Confirm exact additive audit columns and whether strict FK constraints are safe or whether indexed nullable strings are the first compatibility step.
- Confirm whether `/api/provenance` broad list remains allowed with filtering or should require at least `entity_type`.
- Confirm context minimization rules for privacy export/delete audit records.
- Confirm whether consent capture must require principal in the first implementation slice.
- Confirm which route-level denials should call the new audit service in the first implementation slice.
- Confirm whether request id should be generated by middleware if missing.

## Non-Goals

- No provider SDKs.
- No provider-owned audit authority.
- No provider-side planner permissions.
- No new audit query API without separate approval.
- No production DB change.
- No Railway runtime wiring.
- No deploy or smoke.
- No push.
- No address onboarding.
- No reasoning tools or planner intelligence expansion.
