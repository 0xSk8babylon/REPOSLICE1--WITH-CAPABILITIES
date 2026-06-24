#!/usr/bin/env python3
"""Local FastAPI smoke checks against Railway staging Postgres.

The default run uses only GET endpoints that do not trigger the home-data audit
middleware. Use --include-protected-audit-smoke when the expected audit_events
writes for protected GET routes are explicitly approved.
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path
from typing import Any

EXPECTED_CORE_COUNTS = {
    "accounts": 1,
    "homes": 1,
    "source_documents": 5,
    "data_provenance": 7,
    "rule_provenance": 25,
    "equipment_products": 8,
    "energy_system_designs": 2,
    "scenarios": 2,
}
EXPECTED_ALEMBIC_HEAD = "20260523_0001"
DEFAULT_ENV_FILE = Path.home() / ".secrets" / "residential-energy-planner" / "staging.env"
REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"
API_VENV_PYTHON = API_ROOT / ".venv" / "bin" / "python"
ALLOW_DIRTY_REPO_ENV = "ALLOW_DIRTY_REPO"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def passed(message: str) -> None:
    print(f"PASS: {message}")


def info(message: str) -> None:
    print(f"INFO: {message}")


def mode_has_no_group_or_other_bits(path: Path, label: str) -> None:
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        fail(f"{label} permissions are too open: mode {mode:o}")
    passed(f"{label} permissions OK: mode {mode:o}")


def parse_env_value(raw_value: str) -> str:
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def validate_repo_cleanliness() -> None:
    import subprocess

    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--short"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        if os.environ.get(ALLOW_DIRTY_REPO_ENV) == "true":
            passed("repo cleanliness check could not run; allowed by ALLOW_DIRTY_REPO=true")
            return
        fail("repo cleanliness check failed; verify git status before staging FastAPI smoke")
    if result.stdout.strip():
        if os.environ.get(ALLOW_DIRTY_REPO_ENV) == "true":
            passed("repo cleanliness check observed uncommitted changes; allowed by ALLOW_DIRTY_REPO=true")
            return
        fail("repo has uncommitted changes; commit or stash before staging FastAPI smoke")
    passed("repo clean")


def load_env_file(env_file: Path) -> None:
    if not env_file.is_file():
        fail("staging env file does not exist")
    passed("staging env file exists")

    mode_has_no_group_or_other_bits(env_file, "staging env file")
    mode_has_no_group_or_other_bits(env_file.parent, "staging env parent directory")
    mode_has_no_group_or_other_bits(env_file.parent.parent, "staging env grandparent directory")

    loaded_keys: set[str] = set()
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        key, separator, raw_value = line.partition("=")
        if not separator:
            continue
        key = key.strip()
        if not key:
            continue
        os.environ[key] = parse_env_value(raw_value)
        loaded_keys.add(key)

    required_keys = {
        "APP_ENV",
        "DEBUG",
        "DATABASE_URL",
        "DATABASE_CREATE_ALL_ON_STARTUP",
        "DATABASE_SEED_DEMO_DATA_ON_STARTUP",
    }
    missing = sorted(required_keys - loaded_keys)
    if missing:
        fail(f"missing required key names: {', '.join(missing)}")
    passed("required key names present")


def validate_env() -> None:
    database_url = os.environ.get("DATABASE_URL", "")
    if not database_url:
        fail("DATABASE_URL is empty or unset")
    passed("DATABASE_URL present: yes (redacted)")

    if not database_url.startswith(
        ("postgres://", "postgresql://", "postgresql+psycopg://", "postgresql+psycopg2://")
    ):
        fail("DATABASE_URL is not Postgres-like")
    passed("DATABASE_URL postgres-like: yes (redacted)")

    expected_values = {
        "APP_ENV": "staging",
        "DEBUG": "false",
        "DATABASE_CREATE_ALL_ON_STARTUP": "false",
        "DATABASE_SEED_DEMO_DATA_ON_STARTUP": "false",
    }
    for key, expected in expected_values.items():
        if os.environ.get(key) != expected:
            fail(f"{key} must be {expected}")
        passed(f"{key}={expected}")


def maybe_reexec_with_api_venv() -> None:
    if os.environ.get("REP_STAGING_SMOKE_NO_REEXEC") == "1":
        return
    if not API_VENV_PYTHON.exists():
        return
    if Path(sys.executable).resolve() == API_VENV_PYTHON.resolve():
        return
    try:
        import fastapi  # noqa: F401
        import pydantic_settings  # noqa: F401
    except ImportError:
        os.environ["REP_STAGING_SMOKE_NO_REEXEC"] = "1"
        os.execv(str(API_VENV_PYTHON), [str(API_VENV_PYTHON), *sys.argv])


def sqlalchemy_psycopg_url(url: str) -> str:
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://") :]
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://") :]
    return url


def import_runtime_dependencies() -> tuple[Any, Any, Any, Any]:
    sys.path.insert(0, str(API_ROOT))
    try:
        import pydantic_settings  # noqa: F401
        from fastapi.testclient import TestClient
        from sqlalchemy import create_engine, text
        from sqlalchemy.exc import SQLAlchemyError
    except ImportError as exc:
        missing_dependency = getattr(exc, "name", None) or exc.__class__.__name__
        fail(f"required API runtime dependency unavailable: {missing_dependency}")
    return TestClient, create_engine, text, SQLAlchemyError


def count_table(connection: Any, text: Any, table_name: str) -> int:
    return int(connection.execute(text(f'select count(*) from "{table_name}"')).scalar_one())


def database_counts(create_engine: Any, text: Any) -> dict[str, int]:
    engine = create_engine(os.environ["DATABASE_URL"], future=True)
    try:
        with engine.connect() as connection:
            alembic_version = connection.execute(text("select version_num from alembic_version")).scalar_one()
            if alembic_version != EXPECTED_ALEMBIC_HEAD:
                fail(
                    "alembic version mismatch: "
                    f"expected {EXPECTED_ALEMBIC_HEAD}, observed {alembic_version}"
                )
            counts = {table: count_table(connection, text, table) for table in EXPECTED_CORE_COUNTS}
            counts["audit_events"] = count_table(connection, text, "audit_events")
            return counts
    finally:
        engine.dispose()


def assert_core_counts(counts: dict[str, int]) -> None:
    for table, expected_count in EXPECTED_CORE_COUNTS.items():
        observed_count = counts[table]
        info(f"{table}={observed_count}")
        if observed_count != expected_count:
            fail(f"{table} count mismatch: expected {expected_count}, observed {observed_count}")
    passed("core migrated table counts match expected")


def require_json_list_count(response: Any, path: str, expected_count: int) -> None:
    try:
        payload = response.json()
    except ValueError:
        fail(f"{path} did not return JSON")
    if not isinstance(payload, list):
        fail(f"{path} did not return a JSON list")
    observed_count = len(payload)
    info(f"{path} count={observed_count}")
    if observed_count != expected_count:
        fail(f"{path} count mismatch: expected {expected_count}, observed {observed_count}")


def smoke_get(client: Any, path: str, expected_status: int = 200, headers: dict[str, str] | None = None) -> Any:
    response = client.get(path, headers=headers or {})
    info(f"{path} status={response.status_code}")
    if response.status_code != expected_status:
        fail(f"{path} returned {response.status_code}; expected {expected_status}")
    return response


def run_smoke(include_protected_audit_smoke: bool) -> None:
    TestClient, create_engine, text, SQLAlchemyError = import_runtime_dependencies()
    try:
        pre_counts = database_counts(create_engine, text)
        passed("database reachable before FastAPI smoke")
        assert_core_counts(pre_counts)
        info(f"audit_events_before={pre_counts['audit_events']}")

        from app.main import app

        with TestClient(app) as client:
            smoke_get(client, "/")
            require_json_list_count(smoke_get(client, "/api/accounts"), "/api/accounts", 1)
            require_json_list_count(smoke_get(client, "/api/product-library"), "/api/product-library", 8)

            if include_protected_audit_smoke:
                headers = {"x-user-id": "staging_smoke", "x-home-access": "*"}
                require_json_list_count(smoke_get(client, "/api/homes/all", headers=headers), "/api/homes/all", 1)
                require_json_list_count(smoke_get(client, "/api/designs", headers=headers), "/api/designs", 2)
                require_json_list_count(smoke_get(client, "/api/scenarios", headers=headers), "/api/scenarios", 2)

        post_counts = database_counts(create_engine, text)
        assert_core_counts(post_counts)
        info(f"audit_events_after={post_counts['audit_events']}")

        expected_audit_delta = 3 if include_protected_audit_smoke else 0
        observed_audit_delta = post_counts["audit_events"] - pre_counts["audit_events"]
        info(f"audit_events_delta={observed_audit_delta}")
        if observed_audit_delta != expected_audit_delta:
            fail(
                "audit_events delta mismatch: "
                f"expected {expected_audit_delta}, observed {observed_audit_delta}"
            )
        if include_protected_audit_smoke:
            passed("protected GET smoke produced expected audit-only writes")
        else:
            passed("read-only smoke completed without DB writes")
    except SQLAlchemyError as exc:
        fail(f"database smoke check failed: {exc.__class__.__name__}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smoke local FastAPI against Railway staging Postgres")
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument(
        "--include-protected-audit-smoke",
        action="store_true",
        help="Also call protected GET routes and require exactly three audit_events writes.",
    )
    return parser


def main() -> int:
    maybe_reexec_with_api_venv()
    args = build_parser().parse_args()
    validate_repo_cleanliness()
    load_env_file(args.env_file)
    validate_env()
    os.environ["DATABASE_URL"] = sqlalchemy_psycopg_url(os.environ["DATABASE_URL"])
    run_smoke(args.include_protected_audit_smoke)
    passed("FastAPI staging smoke completed without secret output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
