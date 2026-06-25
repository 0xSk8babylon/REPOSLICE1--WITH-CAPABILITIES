# Ownership / Permissions Plan

## Status

Docs-only planning approved by Matt on 2026-06-25.

Implementation slice 1 was separately approved by Matt on 2026-06-25 for account-membership route filtering on the highest-risk collection/object routes.

Implemented slice 1 adds a provider-neutral permissions helper, account-role metadata on the internal principal, membership-filtered home/design/scenario collection routes, object authorization for design equipment and scenario revisions, and focused ownership tests. It does not add migrations, new tables, provider SDKs, secrets, production DB changes, Railway runtime wiring, deploys, smoke tests, pushes, `home_access_grants`, or `home_ownerships`.

Implementation slice 2 was separately approved by Matt on 2026-06-25 for remaining high-risk account-membership route filtering.

Implemented slice 2 extends the same account-membership boundary to buildings, electrical panels, loads, load summaries, equipment locations, estimated pathways, compatibility issue lists, current/generated takeoffs, design advisor summaries, AI design context, and owner-only privacy export/delete checks. It does not add migrations, new tables, provider SDKs, secrets, production DB changes, Railway runtime wiring, deploys, smoke tests, pushes, `home_access_grants`, or `home_ownerships`.

## Approved Direction

Use `account_memberships` as the first app-owned ownership and authorization boundary.

OAuth/OIDC provider identity remains identity proof only. Provider claims must not assign planner roles, account ownership, home access, privacy rights, audit authority, provenance authority, contractor authorization, utility authorization, or operational authority.

Approved first trust path:

```text
OIDC provider identity
-> app-owned user
-> active app-owned account_membership
-> homes where homes.account_id is in the principal account set
-> route/object authorization decision
-> app-owned audit actor record
```

Do not add `home_access_grants` or `home_ownerships` in the first ownership slice. Per-home sharing and ownership-transfer tables remain deferred.

## Current Relationship Findings

- `accounts` is the current business/workspace container.
- `users`, `oauth_identities`, and `account_memberships` exist from the provider-neutral auth foundation slice.
- `account_memberships.role` and `account_memberships.status` are the first app-owned role and activation fields.
- `homes.account_id` is the current ownership edge from account to home.
- `homes.account_id` is nullable. Nullable-account homes must be hidden or denied by default until explicitly assigned.
- Most planner records are home-scoped through `home_id`: buildings, panels, loads, equipment locations, designs, scenarios, facts, geometry, estimated pathways, and derived home views.
- Some records are design-scoped and need indirect authorization by resolving `design_id -> energy_system_designs.home_id`.
- Some records are scenario-scoped and need indirect authorization by resolving `scenario_id -> scenarios.home_id`.
- `source_documents`, `rule_provenance`, `equipment_products`, load templates, and design goal presets are global/reference-style data today.
- `data_provenance` is polymorphic through `entity_type` and `entity_id`; full entity-aware filtering can be deferred to the audit/trust phase unless an immediate route-safety need appears.
- `audit_events.user_id` and `consent_records.user_id` remain string-based and are planned for the audit/trust layer.

## Ownership Model

### Account Ownership

The account is the first durable app-owned workspace. A user has account access only through an active `account_memberships` row.

Rules:

- only active memberships count
- provider organization, role, metadata, or group claims do not grant app access
- account role semantics are based on `account_memberships.role`, not the legacy `accounts.role` field
- the legacy `accounts.role`, `subscription_status`, and `plan_type` fields remain business/scaffolding metadata, not authorization policy

### Home Access

Home access is derived from account membership:

```text
user -> active account_memberships.account_id -> homes.account_id
```

Rules:

- a principal may access a home when `home.account_id` is in the principal account set
- `homes.account_id = null` is denied/hidden by default
- home-scoped child records inherit the home authorization decision
- design/scenario records inherit the authorization decision from their parent home

### Future Home Grants

Per-home grants are deferred until the product needs exception sharing beyond account membership.

Deferred examples:

- contractor temporary access
- homeowner-to-contractor sharing
- utility/program read-only sharing
- real estate, insurance, finance, manufacturer, or aggregator access
- scoped exports or share links
- ownership transfer
- revocation and grant expiry workflows

## Role Policy Matrix

First-slice roles come only from `account_memberships.role`.

| Role | Read account homes | Read derived advisory views | Create/update planner data | Manage account users | Privacy export/delete | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `owner` | yes | yes | yes | yes | yes | first durable account owner role |
| `admin` | yes | yes | yes | yes | no | operational account manager, no first-slice privacy delete/export |
| `member` | yes | yes | yes | no | no | normal write-capable planner collaborator |
| `viewer` | yes | yes | no | no | no | read-only, may read derived advisory views |
| `contractor` | deferred | deferred | deferred | no | no | future sharing/grant model |
| `utility` / `program` | deferred | deferred narrow views only | no | no | no | future scoped views, not first slice |

Unknown roles should deny by default.

Inactive memberships should deny by default.

## Route Filtering Plan

Implementation slice 1 status:

- implemented: `GET /api/homes`, `GET /api/homes/all`, `POST /api/homes`, `PATCH /api/homes/{home_id}`
- implemented: `GET /api/designs`, `POST /api/designs`, `PATCH /api/designs/{design_id}`
- implemented: `GET/POST/PATCH/DELETE /api/designs/{design_id}/equipment...`
- implemented: `GET /api/scenarios`, `GET /api/scenarios/compare`, `GET /api/scenarios/{scenario_id}/revisions`, `POST /api/scenarios`, `PATCH /api/scenarios/{scenario_id}`

Implementation slice 2 status:

- implemented: `GET/POST/PATCH /api/buildings`
- implemented: `GET/POST/PATCH /api/panels`
- implemented: `GET /api/loads`, `GET /api/loads/summary`, `POST/PATCH /api/loads`
- implemented: `GET/POST/PATCH /api/equipment/locations`
- implemented: `GET/POST/PATCH /api/estimated-pathways`
- implemented: `GET /api/compatibility-rules/issues`, `GET /api/compatibility-rules/evaluate/{design_id}`
- implemented: `GET /api/takeoffs/current`, `GET /api/takeoffs/generate/{design_id}`
- implemented: `GET /api/design-advisor/summary/{design_id}`, `GET /api/ai-context/design/{design_id}`
- implemented: owner-only checks for `GET /api/privacy/homes/{home_id}/export` and `DELETE /api/privacy/homes/{home_id}`

Still planned: broader home-path derived surfaces and entity-aware `data_provenance` filtering in later audit/trust or route-coverage phases.

### First Priority Collection Routes

These routes need account/home filtering before production runtime use:

- `GET /api/homes`
- `GET /api/homes/all`
- `GET /api/buildings`
- `GET /api/panels`
- `GET /api/loads`
- `GET /api/loads/summary`
- `GET /api/designs`
- `GET /api/scenarios`
- `GET /api/scenarios/compare`
- `GET /api/equipment/locations`
- `GET /api/estimated-pathways`
- `GET /api/compatibility-rules/issues`
- `GET /api/takeoffs/current`

Filtering should use the internal principal, not provider claims.

### First Priority Object Routes

These routes need object-level authorization by resolving the object to a home:

- `GET /api/scenarios/{scenario_id}/revisions`
- `GET /api/designs/{design_id}/equipment`
- `POST /api/designs/{design_id}/equipment`
- `PATCH /api/designs/{design_id}/equipment/{equipment_id}`
- `DELETE /api/designs/{design_id}/equipment/{equipment_id}`
- `GET /api/compatibility-rules/evaluate/{design_id}`
- `GET /api/takeoffs/generate/{design_id}`
- `GET /api/design-advisor/summary/{design_id}`
- `GET /api/ai-context/design/{design_id}`

### Home-Path Routes

Home-path routes are already shaped for direct `home_id` checks, but they should use the same policy helper as collection/object routes:

- `/api/homes/{home_id}/facts`
- `/api/homes/{home_id}/load-calculations/*`
- `/api/homes/{home_id}/geometry/*`
- `/api/privacy/homes/{home_id}/*`
- `/api/evidence/homes/{home_id}/*`
- `/api/planning-exchange/homes/{home_id}`
- `/api/twin-planning-context/homes/{home_id}/*`
- `/api/estimate-readiness/homes/{home_id}`
- `/api/proposal-option-sets/homes/{home_id}`
- `/api/contractor-workflow/homes/{home_id}/readiness`
- `/api/product-preferences/homes/{home_id}`
- `/api/post-install/homes/{home_id}`
- `/api/crm-handoff/homes/{home_id}`
- `/api/energy-passport/homes/{home_id}`
- `/api/program-intelligence/homes/{home_id}`

### Global / Reference Routes

These may remain readable to authenticated users for the first slice:

- `GET /api/product-library`
- `GET /api/source-documents`
- `GET /api/rule-provenance`
- `GET /api/load-templates`
- `GET /api/design-goal-presets`

Write operations for global/reference data should not be broadly available in production without a separate admin policy decision.

### Deferred Provenance Filtering

`GET /api/provenance` can remain deferred to the audit/trust phase unless immediate route safety requires earlier filtering.

Reason: provenance uses polymorphic `entity_type` / `entity_id`, so safe filtering requires entity-aware ownership resolution rather than simple `home_id` filtering.

## Authorization Helper Shape

First implementation should add a small provider-neutral authorization helper/service, likely under `app/security/permissions.py`.

Recommended helper concepts:

- role constants for `owner`, `admin`, `member`, `viewer`
- status constants for active/inactive membership handling
- `can_read_account(principal, account_id)`
- `can_manage_account(principal, account_id)`
- `can_read_home(principal, home_id)`
- `can_write_home(principal, home_id)`
- `can_privacy_admin_home(principal, home_id)`
- object resolvers for design and scenario home ownership
- collection filters for allowed account IDs and allowed home IDs

The helper should deny unknown roles, inactive memberships, unknown homes, and nullable-account homes by default.

## Migration Impact

No new migration is recommended for the first ownership implementation slice.

Use existing schema:

- `users`
- `oauth_identities`
- `account_memberships`
- `homes.account_id`

Possible future migrations:

- make `homes.account_id` non-null after all existing data has an approved backfill path
- add `home_access_grants`
- add `home_ownerships`
- add ownership transfer records
- add permissioned export/share-link tables
- add stronger audit actor references

Any production backfill for existing `account_demo` / `home_001` remains a separate approval gate.

## Test Strategy

Required first implementation tests:

- active `owner`, `admin`, `member`, and `viewer` membership role behavior
- inactive membership denied
- unknown role denied
- `member` can create/update normal planner data
- `viewer` can read but cannot write
- `viewer` can read derived advisory views
- privacy export/delete is owner-only
- `homes.account_id = null` is hidden/denied
- collection routes return only authorized home/account data
- object routes deny cross-account design/scenario access
- global/reference read routes remain readable to authenticated users
- provider claims cannot grant app roles or permissions
- scaffold headers remain local/test-only behind explicit config

## Risks And Blockers

- Collection routes currently return broad records and must be filtered before production runtime use.
- `homes.account_id` is nullable; denial/hiding must be explicit.
- Design and scenario routes need indirect object-to-home resolution.
- `data_provenance` cannot be safely filtered without entity-aware ownership resolution.
- `audit_events.user_id` and `consent_records.user_id` remain string-based until the audit/trust layer.
- The production DB has not had the auth foundation migration applied under an approved production runtime plan.
- Provider choice and production OIDC runtime wiring remain unapproved.
- No provider-side role or group claim may be treated as an app permission.

## Deferred Items

- `home_access_grants`
- `home_ownerships`
- ownership transfer
- contractor accounts and contractor sharing
- utility/program/finance/insurance/manufacturer/aggregator sharing
- permissioned exports and share links
- app-owned sessions
- provider SDK integration
- production runtime env-var wiring
- production deploy/smoke
- `data_provenance` entity-aware filtering, unless required earlier for route safety

## Decisions Needed Before Implementation

- Confirm exact route list for first filtering PR.
- Confirm whether account management endpoints are included in the first implementation or staged after home/planner filtering.
- Confirm whether global/reference writes are blocked, admin-only, or left unchanged until deployment hardening.
- Confirm whether `/api/auth/me` should expose role summaries in the first implementation.
- Confirm production backfill owner/user for `account_demo` / `home_001` before any production runtime auth use.

## Non-Goals

- No provider SDKs.
- No provider-owned roles or permissions.
- No secrets in repo.
- No app sessions.
- No home grants or ownership-transfer tables in the first slice.
- No production DB change.
- No Railway runtime wiring.
- No deploy or smoke.
- No push.
