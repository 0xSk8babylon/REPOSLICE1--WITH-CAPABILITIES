# B3 Hardened Evidence Intake Closeout

## Summary

B3 Hardened Evidence Intake is implemented as a local validated photo-evidence-to-fact endpoint. It validates evidence metadata and extracted values before creating B1 photo-verified facts.

## Runtime Endpoint

- `POST /api/evidence/homes/{home_id}/photo-facts`

## Runtime Files

- `apps/api/app/evidence/__init__.py`
- `apps/api/app/evidence/schemas.py`
- `apps/api/app/evidence/router.py`
- `apps/api/app/services/evidence.py`
- `apps/api/app/main.py`
- `apps/api/app/security/auth.py`
- `apps/api/tests/test_evidence.py`

## Verification

- `python3 -m py_compile app/evidence/schemas.py app/evidence/router.py app/services/evidence.py app/main.py app/security/auth.py tests/test_evidence.py`
- `python3 -m unittest tests/test_evidence.py`
- `python3 -m unittest tests/test_facts.py tests/test_evidence.py`
- `git diff --check`

## Boundary

B3 does not store raw files, perform OCR, call AI extraction, scan malware, add external providers, add dependencies, rewrite lockfiles, add frontend capture UI, add production storage, expose secrets, deploy, push, or perform field verification.

## Next Action

Run B3 verification, commit the completed loop if verification passes, then perform final roadmap closeout.
