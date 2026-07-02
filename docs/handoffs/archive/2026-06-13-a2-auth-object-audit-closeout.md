# A2 Auth + Object Authorization + Audit Closeout

## Summary

A2 is implemented as a local provider-free header-based authentication, home-level authorization, and audit logging foundation for home-data API paths.

## Runtime Files

- `apps/api/app/security/__init__.py`
- `apps/api/app/security/auth.py`
- `apps/api/app/core/models.py`
- `apps/api/app/main.py`
- `apps/api/tests/test_auth_audit.py`

## Completed Scope

- Added `AuditEvent` SQLAlchemy model.
- Added `HomeAccessMiddleware`.
- Requires `x-user-id` for home-data API paths.
- Enforces object-level `home_id` access where path or query home ID is present through `x-home-access`.
- Writes audit events for allowed and denied home-data access.
- Added focused tests for authentication, cross-home authorization blocking, allowed access, home-list authentication, and audit writes.

## Verification

- `python3 -m py_compile app/security/auth.py app/core/models.py app/main.py tests/test_auth_audit.py` passed.
- `python3 -m unittest tests/test_auth_audit.py` passed with `4 tests OK`.
- `python3 -m unittest tests/test_facts.py tests/test_geometry.py tests/test_auth_audit.py` passed with `15 tests OK`.
- `git diff --check` passed.
- `fastapi.testclient.TestClient` was avoided because `httpx` is not installed and dependency installation/lockfile changes remain out of scope.

## Boundary

A2 does not add an external auth provider, secrets, sessions, cookies, OAuth, password flow, RBAC/ABAC, tenant isolation beyond header-scoped home access, frontend login UI, dependency installs, lockfile rewrites, production deployment, push, billing, or operational control.

## Next Action

Run A2 verification, commit the completed loop if verification passes, then continue to A4 Privacy / CCPA.
