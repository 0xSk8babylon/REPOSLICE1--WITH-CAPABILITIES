# OAuth / Auth Foundation Plan

## Status

Docs-only planning approved by Matt on 2026-06-25.

Implementation slice 1 was separately approved by Matt on 2026-06-25 for provider-neutral schema and backend boundary only.

Implemented slice 1 adds app-owned auth foundation tables/models, a provider-neutral principal boundary, a test-only fake verified-claims adapter, explicit local/test-only scaffold-header config, and `GET /api/auth/me`. It does not add provider SDKs, provider secrets, app sessions, home ownership/grant tables, production DB changes, Railway runtime wiring, deploys, production smoke tests, or pushes.

## Approved Direction

The first auth foundation should use a provider-neutral OIDC/JWT backend boundary.

OAuth is identity proof only. App-owned tables remain responsible for ownership, permissions, audit actor identity, provenance continuity, and future permissioned-view enforcement.

Approved trust path:

```text
OIDC provider identity
-> app-owned user
-> app-owned account membership
-> account/home authorization decision
-> app-owned audit actor record
```

Provider tokens must not become the source of planner ownership, home access, permission grants, provenance authority, contractor authorization, utility authority, or operational-control authority.

## Current Findings

- Current A2 auth is local scaffold enforcement only. `HomeAccessMiddleware` trusts `x-user-id` and `x-home-access`, applies path/query `home_id` checks for home-data API paths, and writes `audit_events`.
- The current scaffold is useful as an adapter seam, but it is not production-safe authentication.
- Existing `accounts` are business/workspace scaffolding. Account `role`, `subscription_status`, and `plan_type` are documented as non-RBAC fields.
- `homes.account_id` is nullable and is the closest current ownership-adjacent link.
- `audit_events.user_id` and `consent_records.user_id` are plain strings, not FK-backed app users.
- No app-owned `users`, `oauth_identities`, `account_memberships`, app sessions, or home grant tables exist yet.
- Current frontend local development sends scaffold headers from `VITE_API_USER_ID` and `VITE_API_HOME_ACCESS`.
- Collection routes such as `/api/homes/all` currently authenticate but are not yet filtered by app-owned account/home access.
- Production DB state is at Alembic `20260523_0001`; auth schema work must use a new explicit Alembic revision and must not rely on metadata drift or startup `create_all`.

## First Implementation Slice

Matt approved and slice 1 implemented:

- `users`
- `oauth_identities`
- `account_memberships`
- provider-neutral principal interface
- `/api/auth/me` contract
- bearer JWT request boundary with a fake verified-claims adapter for tests only
- local/test-only scaffold header path behind explicit development configuration

No app session table should be added in the first slice. The initial model is bearer JWT validation on backend requests.

No Clerk, Auth0, Supabase, WorkOS, or other provider SDK should be added until Matt approves a provider choice and integration boundary.

## Proposed Tables

### `users`

App-owned actor identity.

Implemented fields:

- `id`
- `primary_email`
- `display_name`
- `status`
- `created_at`
- `updated_at`

This table is the app identity anchor for audit and ownership decisions. It does not prove OAuth identity by itself.

### `oauth_identities`

Provider identity link.

Implemented fields:

- `id`
- `user_id`
- `provider`
- `issuer`
- `subject`
- `email`
- `email_verified`
- `last_seen_at`
- `created_at`
- `updated_at`
- optional minimal profile/claims snapshot for diagnostics

Required uniqueness:

- unique `(issuer, subject)`

Do not store provider access tokens or refresh tokens in the first slice.

### `account_memberships`

App-owned business/workspace membership.

Implemented fields:

- `id`
- `account_id`
- `user_id`
- `role`
- `status`
- `created_at`
- `updated_at`

This table controls account-level app access. Provider organization, role, permission, or metadata claims may be recorded for diagnostics later, but must not replace app-owned membership checks.

## Principal Boundary

The backend should build an internal principal after token validation and app lookup.

Planned principal shape:

- `user_id`
- `identity_id`
- `provider`
- `issuer`
- `subject`
- `account_ids`
- `authorized_home_ids` derived from app-owned account/home relationships
- `auth_source` such as `oidc_bearer_jwt` or `local_test_headers`

The principal should be request-scoped and should not persist provider authorization semantics into business logic.

## `/api/auth/me` Planning

Additive endpoint:

```text
GET /api/auth/me
```

Implemented response shape:

- internal app `user_id`
- `auth_source`
- linked identity summary with `identity_id`, `provider`, `issuer`, and `subject`
- app-owned `account_ids`
- derived `authorized_home_ids`
- limitations explaining that OAuth proves identity only and app tables control access

This endpoint should not expose raw tokens, secrets, provider refresh tokens, or provider-side authorization internals.

## Authorization Impact

Slice 1 preserves the existing home-data middleware concept and adds a provider-neutral principal source:

- production/staging future path: bearer JWT -> verified provider identity -> app user -> account membership -> authorized home access
- local/test: scaffold headers only when explicit dev/test config enables them
- test-only fake bearer path: fake verified claims -> app user -> account membership -> authorized home access

Collection/list routes must be filtered by app-owned access before production runtime use. This includes at least:

- `/api/homes`
- `/api/homes/all`
- list-style building, panel, load, design, scenario, equipment, pathway, and derived context endpoints where the route does not contain a path `home_id`

Existing compatibility-sensitive GET contracts should evolve additively and should not be narrowed without a deliberate contract plan.

## Audit Impact

Audit actor identity should move from string-only `user_id` toward app-owned actor references.

Planned direction:

- retain current audit event behavior while adding stronger actor semantics
- record internal app user ID as the durable actor
- optionally record provider/identity reference for authentication provenance
- keep audit policy app-owned

Audit entries must not rely on provider roles, provider organizations, or provider metadata as authority.

## Migration Impact

Implementation added explicit Alembic revision `20260625_0002_auth_foundation.py`.

Migration posture:

- additive tables first
- no destructive changes
- no production DB changes without separate approval
- no startup `create_all` reliance for managed Postgres
- explicit backfill plan for mapping existing `account_demo` / `home_001` to the first approved app user

The migration should be reviewed for SQLite local compatibility and managed Postgres compatibility.

## Frontend Impact

Planning only:

- replace local scaffold headers with bearer token attachment after provider choice
- centralize all API calls through one auth-aware request helper
- keep local scaffold variables for local/test only
- add login/logout/callback UI only after provider choice and frontend SDK approval

No provider SDK or login UI is approved by this document.

## Deferred Items

Deferred to the ownership/permissions phase unless Matt separately approves a minimal placeholder:

- `home_access_grants`
- `home_ownerships`
- ownership transfer
- contractor accounts
- utility, finance, insurance, manufacturer, or aggregator permission models
- RBAC/ABAC beyond minimal app-owned account membership
- permissioned exports/share links
- app-owned session table
- provider SDK integration
- production runtime env-var wiring
- production deploy/smoke
- collection/list route filtering rollout

## Risks And Blockers

- Current `x-user-id` / `x-home-access` scaffold is not production-safe.
- Collection routes need app-owned filtering before production runtime use.
- `audit_events.user_id` is currently string-based and not a durable app-user FK.
- `consent_records.user_id` is also string-based.
- Migration has an explicit auth revision; production application remains unrun until separately approved.
- Provider tokens must not become the authorization source.
- Provider choice remains unapproved.
- Current production FastAPI runtime wiring and smoke remain unapproved.

## Decisions Needed Next

- Provider choice, or explicit generic OIDC-only implementation target.
- First approved production app user/email for existing `account_demo` and `home_001`.
- Ownership/permissions model for home-level grants, ownership transfer, and collection filtering.
- Whether audit actor hardening should add FK-backed user references or stay staged behind string compatibility.
- Production runtime auth wiring plan and smoke scope.

## Non-Goals

- No provider SDKs.
- No secrets in repo.
- No app sessions.
- No home ownership/grant implementation.
- No production DB change.
- No Railway runtime wiring.
- No deploy or smoke.
- No push.
- No provider-side planner permissions, ownership, audit policy, or provenance.
