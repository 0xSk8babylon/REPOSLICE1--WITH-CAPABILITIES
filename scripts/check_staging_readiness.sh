#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${STAGING_ENV_FILE:-$HOME/.secrets/residential-energy-planner/staging.env}"
EXPECTED_ALEMBIC_HEAD="${EXPECTED_ALEMBIC_HEAD:-20260523_0001}"
EXPECTED_PUBLIC_TABLE_COUNT="${EXPECTED_PUBLIC_TABLE_COUNT:-26}"
ALLOW_DIRTY_REPO="${ALLOW_DIRTY_REPO:-false}"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

pass() {
  printf 'PASS: %s\n' "$1"
}

mode_has_no_group_or_other_bits() {
  local path="$1"
  local label="$2"
  local mode

  mode="$(stat -c '%a' "$path")"
  if (( (8#$mode & 8#077) != 0 )); then
    fail "$label permissions are too open: mode $mode"
  fi
  pass "$label permissions OK: mode $mode"
}

require_key_name() {
  local key="$1"

  if ! grep -Eq "^[[:space:]]*(export[[:space:]]+)?${key}=" "$ENV_FILE"; then
    fail "missing required key name: $key"
  fi
}

require_value() {
  local key="$1"
  local value="${!key:-}"

  if [[ -z "$value" ]]; then
    fail "$key is empty or unset"
  fi
}

assert_value() {
  local key="$1"
  local expected="$2"
  local value="${!key:-}"

  if [[ "$value" != "$expected" ]]; then
    fail "$key must be $expected"
  fi
  pass "$key=$expected"
}

if [[ -n "$(git -C "$REPO_ROOT" status --short)" ]]; then
  if [[ "$ALLOW_DIRTY_REPO" == "true" ]]; then
    pass "repo cleanliness check observed uncommitted changes; allowed by ALLOW_DIRTY_REPO=true"
  else
    fail "repo has uncommitted changes; commit or stash before staging readiness verification"
  fi
else
  pass "repo clean"
fi

[[ -f "$ENV_FILE" ]] || fail "staging env file does not exist"
pass "staging env file exists"

mode_has_no_group_or_other_bits "$ENV_FILE" "staging env file"
mode_has_no_group_or_other_bits "$(dirname "$ENV_FILE")" "staging env parent directory"
mode_has_no_group_or_other_bits "$(dirname "$(dirname "$ENV_FILE")")" "staging env grandparent directory"

for key in \
  APP_ENV \
  DEBUG \
  DATABASE_URL \
  DATABASE_CREATE_ALL_ON_STARTUP \
  DATABASE_SEED_DEMO_DATA_ON_STARTUP; do
  require_key_name "$key"
done
pass "required key names present"

set -a
# shellcheck source=/dev/null
if ! source "$ENV_FILE" >/dev/null 2>&1; then
  set +a
  fail "could not load staging env file"
fi
set +a

require_value "DATABASE_URL"
pass "DATABASE_URL present: yes (redacted)"

case "$DATABASE_URL" in
  postgres://*|postgresql://*|postgresql+psycopg://*|postgresql+psycopg2://*)
    pass "DATABASE_URL postgres-like: yes (redacted)"
    ;;
  *)
    fail "DATABASE_URL is not Postgres-like"
    ;;
esac

assert_value "APP_ENV" "staging"
assert_value "DEBUG" "false"
assert_value "DATABASE_CREATE_ALL_ON_STARTUP" "false"
assert_value "DATABASE_SEED_DEMO_DATA_ON_STARTUP" "false"

export EXPECTED_ALEMBIC_HEAD
export EXPECTED_PUBLIC_TABLE_COUNT
export PYTHONPATH="$REPO_ROOT/apps/api:${PYTHONPATH:-}"

python3 - <<'PY'
from __future__ import annotations

import os
import sys
from typing import Any

EXPECTED_COUNTS = {
    "accounts": 1,
    "homes": 1,
    "source_documents": 5,
    "data_provenance": 7,
    "rule_provenance": 25,
    "equipment_products": 8,
    "energy_system_designs": 2,
    "scenarios": 2,
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def passed(message: str) -> None:
    print(f"PASS: {message}")


try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import SQLAlchemyError
    from scripts.sqlite_to_postgres import TABLE_ORDER
except ImportError as exc:
    fail(f"required Python dependency unavailable: {exc.__class__.__name__}")


database_url = os.environ.get("DATABASE_URL", "")
expected_head = os.environ["EXPECTED_ALEMBIC_HEAD"]
expected_public_table_count = int(os.environ["EXPECTED_PUBLIC_TABLE_COUNT"])


def sqlalchemy_psycopg_url(url: str) -> str:
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://") :]
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://") :]
    return url


def scalar(connection: Any, statement: str, parameters: dict[str, Any] | None = None) -> Any:
    return connection.execute(text(statement), parameters or {}).scalar_one()


def count_table(connection: Any, table_name: str) -> int:
    return int(scalar(connection, f'select count(*) from "{table_name}"'))


try:
    engine = create_engine(sqlalchemy_psycopg_url(database_url), future=True)
    with engine.connect() as connection:
        scalar(connection, "select current_database()")
        scalar(connection, "select current_user")
        scalar(connection, "select version()")
        passed("database connectivity/read identity: yes (values redacted)")

        public_table_count = int(
            scalar(
                connection,
                """
                select count(*)
                from information_schema.tables
                where table_schema = 'public'
                  and table_type = 'BASE TABLE'
                """,
            )
        )
        print(f"INFO: public_schema_table_count={public_table_count}")
        if public_table_count != expected_public_table_count:
            fail(
                "public schema table count mismatch: "
                f"expected {expected_public_table_count}, observed {public_table_count}"
            )
        passed("public schema table count matches expected")

        table_names = {
            row[0]
            for row in connection.execute(
                text(
                    """
                    select table_name
                    from information_schema.tables
                    where table_schema = 'public'
                      and table_type = 'BASE TABLE'
                    """
                )
            )
        }
        expected_tables = set(TABLE_ORDER) | {"alembic_version"}
        missing_tables = sorted(expected_tables - table_names)
        if missing_tables:
            fail(f"missing expected public tables: {', '.join(missing_tables)}")
        passed("expected public tables present")

        alembic_version = scalar(connection, "select version_num from alembic_version")
        print(f"INFO: alembic_version={alembic_version}")
        if alembic_version != expected_head:
            fail(f"alembic version mismatch: expected {expected_head}, observed {alembic_version}")
        passed("alembic revision matches expected head")

        observed_counts = {table: count_table(connection, table) for table in EXPECTED_COUNTS}
        for table, expected_count in EXPECTED_COUNTS.items():
            observed_count = observed_counts[table]
            print(f"INFO: {table}={observed_count}")
            if observed_count != expected_count:
                fail(f"{table} count mismatch: expected {expected_count}, observed {observed_count}")
        passed("expected core row counts match")

        audit_events = count_table(connection, "audit_events")
        print(f"INFO: audit_events={audit_events}")

        data_orphans = int(
            scalar(
                connection,
                """
                select count(*)
                from data_provenance provenance
                left join source_documents source
                  on provenance.source_document_id = source.id
                where provenance.source_document_id is not null
                  and source.id is null
                """,
            )
        )
        rule_orphans = int(
            scalar(
                connection,
                """
                select count(*)
                from rule_provenance provenance
                left join source_documents source
                  on provenance.source_document_id = source.id
                where provenance.source_document_id is not null
                  and source.id is null
                """,
            )
        )
        print(f"INFO: data_provenance_orphan_count={data_orphans}")
        print(f"INFO: rule_provenance_orphan_count={rule_orphans}")
        if data_orphans or rule_orphans:
            fail("provenance orphan check failed")
        passed("provenance orphan checks passed")

        unvalidated_fk_count = int(
            scalar(
                connection,
                """
                select count(*)
                from pg_constraint constraint_record
                join pg_namespace namespace_record
                  on namespace_record.oid = constraint_record.connamespace
                where namespace_record.nspname = 'public'
                  and constraint_record.contype = 'f'
                  and not constraint_record.convalidated
                """,
            )
        )
        print(f"INFO: postgres_unvalidated_fk_constraint_count={unvalidated_fk_count}")
        if unvalidated_fk_count != 0:
            fail("Postgres has unvalidated public foreign key constraints")
        passed("Postgres FK validation check passed")
except SQLAlchemyError as exc:
    fail(f"database readiness check failed: {exc.__class__.__name__}")
finally:
    try:
        engine.dispose()
    except NameError:
        pass

passed("staging readiness checks completed without secret output")
PY
