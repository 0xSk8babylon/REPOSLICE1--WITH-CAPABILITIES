# S0 Security Sprint Signoff Evidence

Date: 2026-06-23
Branch: `fix/github-workflow`
Scope: S0 remediation and signoff evidence only.

## Status

S0 status: PASS

S0 is signed off for the Security Sprint remediation scope. Secret scanning, session-handoff tracking remediation, CI security scanning, Dependabot coverage, npm high-threshold audit remediation, Python dependency audit remediation, FastAPI/Pydantic v2 compatibility verification, PG-8D smoke rerun, and owner two-factor authentication attestations have evidence. This signoff does not enter PG-8E, production cutover, migrations, production database work, or Supabase implementation.

## Evidence

### Gitleaks

- Local scan method: ephemeral Docker run using `ghcr.io/gitleaks/gitleaks:latest`.
- Initial result: 1 redacted `generic-api-key` finding in `docs/handoffs/2026-06-04-phase-5a-contractor-participant-charter.md`.
- Remediation: added a narrow `.gitleaksignore` entry for the exact reviewed false-positive fingerprint.
- Follow-up result: PASS, exit code 0, 0 findings.
- Secret values or finding contents were not printed.

### SESSION_HANDOFF Tracking

- `SESSION_HANDOFF.md` was removed from git tracking with `git rm --cached SESSION_HANDOFF.md`.
- The local `SESSION_HANDOFF.md` file remains on disk.
- `.gitignore` now includes `/SESSION_HANDOFF.md`.
- Verification showed `SESSION_HANDOFF.md` is not tracked and is ignored.

### CI Security Scanning

- `.github/workflows/ci.yml` now includes a security job.
- Coverage added:
  - gitleaks full-history secret scan through `gitleaks/gitleaks-action@v3`
  - `npm audit --audit-level=high`
  - `pip-audit` against `apps/api/requirements.txt`
- CI workflow YAML parsed successfully in local syntax sanity check.

### Dependabot

- `.github/dependabot.yml` now exists.
- Coverage added:
  - npm updates at repo root
  - pip updates for `apps/api`
  - GitHub Actions updates
- Dependabot YAML parsed successfully in local syntax sanity check.

### Dependency Audit Findings

- Local npm audit result: PASS at `--audit-level=high`.
- npm remediation updated `react-router-dom` from `6.30.3` to `6.30.4` and `vite` from `5.4.21` to `6.4.3`.
- Follow-up npm audit reports 1 low severity vulnerability below the configured S0 high threshold.
- Frontend lockfile consistency passed with `npm ci --ignore-scripts`.
- Frontend build passed with Vite `6.4.3`.
- Local Python audit method: ephemeral Docker `python:3.11-slim` container with `pip-audit`.
- Python audit result: PASS.
- Strategy A FastAPI-only/Pydantic-v1 probe remained blocked because `starlette 0.46.2` still reported vulnerabilities.
- Strategy B remediation updated FastAPI to `>=0.138,<0.139`, Pydantic to `>=2.13,<2.14`, and added `pydantic-settings>=2,<3`.
- Resolved Strategy B versions: `fastapi==0.138.0`, `starlette==1.3.1`, `pydantic==2.13.4`, `pydantic-settings==2.14.2`.
- Follow-up `pip-audit -r apps/api/requirements.txt` reported no known vulnerabilities.
- Backend compatibility checks passed for changed source compile, app import, and focused backend tests.

### PG-8D Smoke Rerun

- Smoke target: repo-owned Postgres compose service with database `rep_pg8_seed_smoke`.
- Smoke DB state checked read-only:
  - public tables: 26
  - `alembic_version`: `20260523_0001`
  - sample counts: accounts 1, homes 1, designs 2, scenarios 2, equipment_products 8
- Temporary FastAPI server was started against `rep_pg8_seed_smoke` only and stopped after smoke verification.
- Endpoint results:
  - `/`: 200
  - `/api/accounts`: 200
  - `/api/homes/all`: 200
  - `/api/designs`: 200
  - `/api/scenarios`: 200
  - `/api/product-library`: 200
- Product library returned 8 products, with provenance summary and source document fields present.
- Production database `residential_energy_planner` was not touched.
- PG-8E was not entered.
- No migrations, seed operation, database create/drop/recreate, Docker volume removal, commit, or push was performed during smoke verification.

### Owner Attestation

- GitHub 2FA: owner attests enabled.
- npm 2FA: owner attests npm publishing is not applicable for this repo at this time.
- npm audit remains applicable to repository dependencies.
- If npm publishing becomes relevant later, npm 2FA must be enabled before publishing.
- No account settings were inspected or automated.

## Verification Commands

- `git status --short`
- `git diff --check`
- `git ls-files --error-unmatch SESSION_HANDOFF.md`
- `git check-ignore -q SESSION_HANDOFF.md`
- `rg -n "gitleaks|npm audit|pip_audit|pip-audit|package-ecosystem" .github/workflows/ci.yml .github/dependabot.yml`
- `python3` YAML parse for `.github/workflows/ci.yml` and `.github/dependabot.yml`
- Docker gitleaks scan with redacted JSON report
- `npm audit --audit-level=high`
- `npm ci --ignore-scripts`
- `npm run web:build`
- Docker `pip-audit -r apps/api/requirements.txt`
- Docker dependency resolution for `apps/api/requirements.txt`
- `python3 -m py_compile` on changed backend source files
- Docker backend import check: `from app.main import app`
- Docker focused backend tests: `tests.test_database_foundation`, `tests.test_facts`, `tests.test_resilience_recommendation`, `tests.test_scenario_revisions`, `tests.test_estimate_readiness`
- PG-8D smoke rerun against `rep_pg8_seed_smoke`

## Remaining Manual Actions

- None for S0 Security Sprint signoff.
- Next step after this signoff is PG-8E cutover planning only, with Supabase managed-Postgres boundary documented before execution.

## PG-8E Readiness

PG-8E readiness: READY FOR PLANNING ONLY.

PG-8E was not entered. Production cutover remains a separate owner-approved planning and execution boundary.
