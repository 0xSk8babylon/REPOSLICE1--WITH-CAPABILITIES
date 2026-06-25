# Address Onboarding Plan

## Status

Docs-only planning approved by Matt on 2026-06-25.

This plan records the approved address onboarding direction on top of the completed provider-neutral auth foundation, account-membership ownership enforcement, and audit/trust foundation. It does not implement code, create migrations, alter production DB, wire external geocoding APIs, add secrets, deploy, run smoke, wire Railway runtime variables, add provider SDKs, or push.

Backend implementation requires separate explicit approval.

## Current Findings

The existing backend already has the core persistence and authorization surfaces needed for a minimal address onboarding slice:

- `accounts` owns `homes`.
- `users`, `oauth_identities`, and `account_memberships` provide the provider-neutral internal principal and account-membership boundary.
- `homes.account_id` is currently nullable for compatibility, but ownership enforcement hides or denies null-account homes by default.
- `POST /api/homes` exists, but it accepts caller-provided `id` and `account_id`; it is not the approved first-time onboarding path.
- `HomeCreate` currently requires a caller-provided `id`.
- Permission helpers already define `owner`, `admin`, and `member` as write-capable roles; `viewer` is read-only.
- Audit events now support actor, account, object, route, decision, minimized event context, and provenance references.
- `data_provenance` can record user-entered address fields with `entity_type=home`, `entity_id=<home_id>`, and field-level source/trust metadata.
- Demo seed assumes `account_demo` and `home_001` with placeholder address data; first implementation must preserve this behavior.
- The frontend currently defaults local/test scaffold headers to `home_001` and generally assumes `GET /api/homes` succeeds. Frontend onboarding is deferred.

## Approved Route Decision

Use a dedicated first-time onboarding route:

```text
POST /api/onboarding/address
```

Do not use raw `POST /api/homes` as the first-time address onboarding path.

Reason:

- onboarding must derive or verify `account_id` from app-owned membership, not trust caller-controlled home payloads
- onboarding must generate or safely assign `home_id`
- onboarding must prevent orphan/null-account homes
- onboarding must audit the onboarding decision and record provenance for address fields
- onboarding should return workflow state and next steps, not just a raw `Home`

The existing `POST /api/homes` can remain for normal planner editing compatibility, still protected by existing write checks.

## Request Shape

Proposed first implementation request:

```json
{
  "account_id": "optional when the principal has exactly one writable account",
  "name": "Cedar Ridge Residence",
  "address_line_1": "123 Main St",
  "address_line_2": null,
  "city": "Placerville",
  "state": "CA",
  "postal_code": "95667",
  "country": "US"
}
```

Address fields should be required except `address_line_2`. `country` may default to `US`.

Do not accept caller-provided `home_id` in the onboarding request.

## Response Shape

Proposed response:

```json
{
  "home_id": "home_...",
  "account_id": "account_...",
  "status": "created",
  "readiness_state": "address_recorded",
  "next_route": "/",
  "next_steps": [
    "Review service panel",
    "Add major loads",
    "Confirm utility provider"
  ],
  "limitations": [
    "Address is user-entered and not externally verified.",
    "No geocoding, property enrichment, utility inference, climate inference, AHJ inference, or program inference was performed."
  ]
}
```

Allowed `status` values for the first slice:

- `created`
- `existing_home_found`

Allowed `readiness_state` value for the first slice:

- `address_recorded`

## Ownership And Permission Rules

- `owner`, `admin`, and `member` may create homes through onboarding.
- `viewer` may not create homes.
- Principal with no writable account gets `403`.
- If the principal has exactly one writable account, backend may derive `account_id`.
- If the principal has multiple writable accounts, request must include `account_id`.
- Explicit `account_id` must be a writable account for the current principal.
- Created homes must always have non-null `account_id`.
- Same address in another account must not be returned.
- Account-scoped exact normalized address match returns the existing `home_id`.
- Matching is scoped to the selected account only.
- Null-account homes remain hidden/denied and must not be produced by onboarding.
- Provider claims must not assign ownership, role, account, home access, provenance authority, or audit authority.

## Address Normalization

First implementation should use minimal local normalization only:

- trim leading/trailing whitespace
- collapse internal repeated whitespace where straightforward
- normalize `state` and `country` to uppercase
- trim postal code
- treat empty `address_line_2` as null

The normalized address is for account-scoped exact matching and persistence consistency only. It is not a verified postal address, canonical address, parcel identity, geocode, utility territory, AHJ, climate zone, or program jurisdiction.

No external geocoding, address validation API, property enrichment, utility inference, climate inference, AHJ inference, program inference, or external secret is approved.

## Trust Boundaries

Address onboarding must preserve these boundaries:

| Surface | Trust posture |
| --- | --- |
| Raw address input | Request-time user input only; do not store raw request body in audit context |
| Stored address fields | User-entered planning record |
| Normalized address | Local formatting normalization only |
| Account/home ownership | App-owned `account_memberships` and `homes.account_id` |
| Geocoded/enriched data | Deferred; not implemented in first slice |
| Utility/climate/AHJ/program data | Deferred; not inferred |
| User-entered facts | Source-marked user input |
| Derived planner facts | Must remain explicitly derived and provenance-backed when later introduced |
| Audit actor | Current app principal and app-owned membership decision |

## Audit Requirements

Use the central audit writer for onboarding events.

Recommended actions:

- `onboarding.address.submit`
- `onboarding.home.created`
- `onboarding.home.resolved`
- `onboarding.address.denied`

Audit records should include:

- `actor_user_id` where available
- `actor_identity_id` where available
- `auth_source`
- `account_id`
- `home_id` when known
- `object_type=home`
- `object_id=<home_id>` when known
- `route_template=/api/onboarding/address`
- `source_surface=address_onboarding`
- `decision=allowed`, `denied`, or `not_authenticated`

Audit `event_context` must be minimized. It may include safe metadata such as:

- fields present
- normalization mode, such as `local_minimal`
- account resolution mode, such as `single_writable_account` or `explicit_account_id`
- duplicate resolution result, such as `created` or `existing_home_found`

Audit `event_context` must not include:

- raw full request body
- full raw address
- provider tokens or claims
- secrets
- external enrichment results

## Provenance Requirements

Create user-entered provenance rows for address fields if feasible in the first implementation.

Recommended rows:

- `entity_type=home`
- `entity_id=<home_id>`
- `field_name=address_line_1`
- `field_name=address_line_2` when present
- `field_name=city`
- `field_name=state`
- `field_name=postal_code`
- `field_name=country`
- `source_type=user_entry`
- `trust_state=user_created`
- `confidence_level=medium`
- `notes` should state that the value is user-entered and not externally verified

Do not create provenance that implies geocoding, validation, property ownership, utility territory, climate, AHJ, or program verification.

If provenance creation cannot be cleanly included in the first backend slice, the implementation must explicitly document the deferral and keep audit context minimized.

## Backend Implementation Plan

First backend slice should add:

- `apps/api/app/onboarding/__init__.py`
- `apps/api/app/onboarding/schemas.py`
- `apps/api/app/onboarding/router.py`
- route registration in `apps/api/app/main.py`
- repository helpers for account-scoped normalized address lookup and home creation if existing helpers are insufficient
- permission helper use through existing `writable_account_ids` / `can_write_account`
- audit writer calls through `app/security/audit.py`
- provenance row creation through existing `repository.create_data_provenance` or equivalent
- tests in `apps/api/tests/test_address_onboarding.py`

Implementation should be additive and should not create a migration.

`POST /api/onboarding/address` should be covered by auth middleware if the middleware prefix list is used for route-level audit or authentication expectations. The route itself should also depend on `current_principal`.

## Frontend Deferred Plan

No frontend implementation is approved in this planning gate.

Later frontend slice should:

- call `GET /api/homes`
- show address onboarding when `GET /api/homes` returns `404 No home profile found`
- submit to `POST /api/onboarding/address`
- redirect to `/` or `/home` after success
- preserve demo `home_001` behavior when the demo home exists
- avoid claiming address verification, geocoding, utility inference, or property enrichment

Likely frontend files later:

- `apps/web/src/lib/api.js`
- `apps/web/src/app/App.jsx`
- new address onboarding page/component or an empty-state component in the Home shell
- relevant CSS

## Migration Impact

No migration is recommended for the first implementation slice.

Use existing:

- `homes`
- `account_memberships`
- `audit_events`
- `data_provenance`

Deferred schema work may be considered later for normalized address fingerprints, geocoding metadata, address verification state, parcel references, or source-enrichment records, but none of that is approved now.

## Test Strategy

Focused backend tests should cover:

- owner can create home through onboarding
- admin can create home through onboarding
- member can create home through onboarding
- viewer cannot create home
- principal with no writable account gets `403`
- multiple writable accounts require explicit `account_id`
- explicit cross-account `account_id` is denied
- created home always has non-null `account_id`
- account-scoped exact normalized address match returns existing `home_id`
- same address in another account is not returned
- created home appears in `GET /api/homes` and `GET /api/homes/all` for that account
- created home is hidden/denied for another account
- audit event has actor/account/home/object fields
- audit `event_context` does not include raw full address body
- provenance rows are created for address fields when feasible
- demo `account_demo` / `home_001` behavior remains unchanged

Verification should include:

- focused onboarding tests
- relevant auth/permissions/audit/provenance/privacy tests
- Alembic check only if safe and local, even though no migration is expected
- compileall
- `git diff --check`
- secret-safe review

## Risks And Blockers

- Existing raw `POST /api/homes` is not a safe first-time onboarding contract because the caller controls `id` and `account_id`.
- Address matching without a DB uniqueness constraint is best-effort only and should be account-scoped exact normalized matching.
- Address is sensitive; audit context minimization is mandatory.
- Local/test scaffold frontend defaults still point to `home_001`; production onboarding must use real bearer auth plus app-owned membership.
- Existing frontend assumes a home exists; frontend onboarding needs a deliberate empty-state branch later.
- Multi-account UX is deferred to explicit account selection; automatic choice is only safe for exactly one writable account.
- No external enrichment means onboarding cannot claim address validation, geocoding, service territory, property identity, climate zone, AHJ, or program readiness.

## Deferred Items

- frontend implementation
- external geocoding
- postal address validation APIs
- address verification state
- property/parcel enrichment
- utility territory inference
- climate zone inference
- AHJ/program jurisdiction inference
- external secrets
- provider SDKs
- normalized address fingerprint schema
- ownership transfer
- contractor/utility sharing
- address-change history
- production runtime deploy or smoke

## Decisions Locked For First Backend Slice

- Use dedicated `POST /api/onboarding/address`.
- Do not use raw `POST /api/homes` as first-time onboarding path.
- `owner`, `admin`, and `member` may create homes.
- `viewer` may not create homes.
- No writable account returns `403`.
- Multiple writable accounts require explicit `account_id`.
- Account-scoped exact normalized address match returns existing `home_id`.
- Same address in another account must not be returned.
- Created homes must have non-null `account_id`.
- Address normalization is local/minimal only.
- No external enrichment or secrets.
- Audit context must be minimized.
- Address field provenance should be created if feasible.
- Preserve demo `account_demo` / `home_001` behavior.
- Backend first; frontend deferred.

## Suggested Commit Plan

1. Docs-only plan commit: `docs: plan address onboarding`
2. Backend implementation commit after explicit approval: `feat: add address onboarding foundation`
3. Frontend implementation commit after separate approval: `feat: add address onboarding flow`
