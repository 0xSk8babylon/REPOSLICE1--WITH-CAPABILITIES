# A4 Privacy / CCPA Closeout

## Summary

A4 Privacy / CCPA is implemented as local homeowner record export, deletion, and consent-record foundation.

## Runtime Endpoints

- `GET /api/privacy/homes/{home_id}/export`
- `POST /api/privacy/homes/{home_id}/consent`
- `DELETE /api/privacy/homes/{home_id}`

## Runtime Files

- `apps/api/app/privacy/__init__.py`
- `apps/api/app/privacy/schemas.py`
- `apps/api/app/privacy/router.py`
- `apps/api/app/services/privacy.py`
- `apps/api/app/core/models.py`
- `apps/api/app/main.py`
- `apps/api/app/security/auth.py`
- `apps/api/tests/test_privacy.py`

## Verification

- `python3 -m py_compile app/privacy/schemas.py app/privacy/router.py app/services/privacy.py app/core/models.py app/security/auth.py app/main.py tests/test_privacy.py` passed.
- `python3 -m unittest tests/test_privacy.py` passed with `3 tests OK`.
- `python3 -m unittest tests/test_auth_audit.py tests/test_privacy.py` passed with `7 tests OK`.
- `git diff --check` passed.

## Boundary

A4 applies only to local SQLite application records. It does not add external provider deletion, external CRM/utility/contractor deletion, legal advice, production privacy workflow, frontend UI, dependency installs, lockfile rewrites, secrets, push, deployment, billing, or operational control.

## Next Action

Run A4 verification, commit the completed loop if verification passes, then continue to C1 / Phases 18-19.
