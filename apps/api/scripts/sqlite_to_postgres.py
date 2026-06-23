"""PG-8E SQLite-to-Postgres migration helper.

This script is intentionally conservative:
- source inspection can run against the local SQLite file without a target
- copy/dry-run mode requires an explicit Postgres URL
- application target tables must be empty before copy
- target URLs are reported only in redacted form
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit, urlunsplit


EXPECTED_ALEMBIC_HEAD = "20260523_0001"
DEFAULT_SOURCE_FILE = Path(__file__).resolve().parents[1] / "data" / "residential_energy_planner.sqlite3"

TABLE_ORDER = [
    "accounts",
    "source_documents",
    "design_goal_presets",
    "load_templates",
    "homes",
    "audit_events",
    "consent_records",
    "buildings",
    "electrical_panels",
    "loads",
    "facts",
    "roof_planes",
    "geometry_obstructions",
    "equipment_locations",
    "equipment_products",
    "energy_system_designs",
    "design_equipment",
    "compatibility_issues",
    "scenarios",
    "scenario_revisions",
    "takeoff_requests",
    "takeoff_line_items",
    "estimated_pathways",
    "data_provenance",
    "rule_provenance",
]

JSON_COLUMNS = {
    "facts": {"value", "derived_from"},
    "roof_planes": {"horizon_trace"},
    "equipment_products": {"specs"},
    "compatibility_issues": {"possible_solutions", "related_equipment_ids"},
    "scenario_revisions": {"planning_state_snapshot"},
    "data_provenance": {"value_snapshot"},
}

DATETIME_COLUMNS = {
    "created_at",
    "updated_at",
    "verified_at",
    "expires_at",
    "published_date",
    "retrieved_at",
}

SAMPLE_KEY_TABLES = [
    "accounts",
    "homes",
    "energy_system_designs",
    "scenarios",
    "equipment_products",
    "source_documents",
    "audit_events",
]


class MigrationError(RuntimeError):
    """Raised when migration preconditions are not met."""


@dataclass(frozen=True)
class SourceReport:
    source_file: Path
    source_file_size: int
    table_counts: dict[str, int]
    sqlite_foreign_key_issues: list[dict[str, Any]]
    provenance_issues: list[str]
    audit_event_count: int
    sample_primary_keys: dict[str, list[Any]]


def redact_url(url: str) -> str:
    parsed = urlsplit(url)
    if not parsed.netloc:
        return url
    host = parsed.hostname or ""
    port = f":{parsed.port}" if parsed.port else ""
    if parsed.username:
        userinfo = f"{parsed.username}:***@"
    elif parsed.password:
        userinfo = "***@"
    else:
        userinfo = ""
    return urlunsplit((parsed.scheme, f"{userinfo}{host}{port}", parsed.path, parsed.query, parsed.fragment))


def validate_postgres_url(url: str) -> str:
    if not url:
        raise MigrationError("Target Postgres URL is required for copy or dry-run mode.")
    scheme = urlsplit(url).scheme
    if not scheme.startswith("postgres"):
        raise MigrationError("Target URL must use a Postgres SQLAlchemy scheme.")
    return url


def open_sqlite_readonly(source_file: Path) -> sqlite3.Connection:
    if not source_file.exists():
        raise MigrationError(f"Source SQLite file does not exist: {source_file}")
    connection = sqlite3.connect(f"file:{source_file}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def quote_identifier(name: str) -> str:
    escaped = name.replace('"', '""')
    return f'"{escaped}"'


def sqlite_user_tables(connection: sqlite3.Connection) -> set[str]:
    rows = connection.execute(
        "select name from sqlite_master where type = 'table' and name not like 'sqlite_%'"
    ).fetchall()
    return {row["name"] for row in rows}


def require_source_tables(connection: sqlite3.Connection) -> None:
    missing = sorted(set(TABLE_ORDER) - sqlite_user_tables(connection))
    if missing:
        raise MigrationError(f"Source SQLite database is missing expected tables: {', '.join(missing)}")


def table_primary_key_columns(connection: sqlite3.Connection, table_name: str) -> list[str]:
    rows = connection.execute(f"pragma table_info({quote_identifier(table_name)})").fetchall()
    return [row["name"] for row in rows if row["pk"]]


def count_table(connection: sqlite3.Connection, table_name: str) -> int:
    row = connection.execute(f"select count(*) as count from {quote_identifier(table_name)}").fetchone()
    return int(row["count"])


def source_table_counts(connection: sqlite3.Connection) -> dict[str, int]:
    return {table_name: count_table(connection, table_name) for table_name in TABLE_ORDER}


def source_foreign_key_issues(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = connection.execute("pragma foreign_key_check").fetchall()
    return [dict(row) for row in rows]


def orphan_count_sqlite(
    connection: sqlite3.Connection,
    provenance_table: str,
    source_document_column: str = "source_document_id",
) -> int:
    row = connection.execute(
        f"""
        select count(*) as count
        from {quote_identifier(provenance_table)} provenance
        left join source_documents source
          on provenance.{quote_identifier(source_document_column)} = source.id
        where provenance.{quote_identifier(source_document_column)} is not null
          and source.id is null
        """
    ).fetchone()
    return int(row["count"])


def provenance_issues_sqlite(connection: sqlite3.Connection) -> list[str]:
    issues = []
    data_orphans = orphan_count_sqlite(connection, "data_provenance")
    if data_orphans:
        issues.append(f"data_provenance has {data_orphans} rows with missing source_documents")
    rule_orphans = orphan_count_sqlite(connection, "rule_provenance")
    if rule_orphans:
        issues.append(f"rule_provenance has {rule_orphans} rows with missing source_documents")
    return issues


def sample_primary_keys(connection: sqlite3.Connection) -> dict[str, list[Any]]:
    samples: dict[str, list[Any]] = {}
    for table_name in SAMPLE_KEY_TABLES:
        pk_columns = table_primary_key_columns(connection, table_name)
        if not pk_columns:
            continue
        pk_column = pk_columns[0]
        rows = connection.execute(
            f"""
            select {quote_identifier(pk_column)} as id
            from {quote_identifier(table_name)}
            order by {quote_identifier(pk_column)}
            limit 3
            """
        ).fetchall()
        samples[table_name] = [row["id"] for row in rows]
    return samples


def build_source_report(source_file: Path) -> SourceReport:
    with open_sqlite_readonly(source_file) as connection:
        require_source_tables(connection)
        return SourceReport(
            source_file=source_file,
            source_file_size=source_file.stat().st_size,
            table_counts=source_table_counts(connection),
            sqlite_foreign_key_issues=source_foreign_key_issues(connection),
            provenance_issues=provenance_issues_sqlite(connection),
            audit_event_count=count_table(connection, "audit_events"),
            sample_primary_keys=sample_primary_keys(connection),
        )


def parse_datetime(value: Any) -> Any:
    if value is None or isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        return value
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return value


def parse_json_value(value: Any) -> Any:
    if value is None or isinstance(value, (dict, list, int, float, bool)):
        return value
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def convert_row_for_postgres(table_name: str, row: sqlite3.Row) -> dict[str, Any]:
    converted = dict(row)
    for column in JSON_COLUMNS.get(table_name, set()):
        if column in converted:
            converted[column] = parse_json_value(converted[column])
    for column in DATETIME_COLUMNS:
        if column in converted:
            converted[column] = parse_datetime(converted[column])
    return converted


def iter_source_rows(connection: sqlite3.Connection, table_name: str) -> Iterable[dict[str, Any]]:
    pk_columns = table_primary_key_columns(connection, table_name)
    order_clause = ""
    if table_name == "scenario_revisions":
        order_clause = " order by revision_number, id"
    elif pk_columns:
        quoted = ", ".join(quote_identifier(column) for column in pk_columns)
        order_clause = f" order by {quoted}"
    rows = connection.execute(f"select * from {quote_identifier(table_name)}{order_clause}")
    for row in rows:
        yield convert_row_for_postgres(table_name, row)


def import_sqlalchemy():
    try:
        from sqlalchemy import MetaData, Table, create_engine, text
        from sqlalchemy.exc import SQLAlchemyError
    except ImportError as exc:
        raise MigrationError("SQLAlchemy is required for target Postgres dry-run/copy mode.") from exc
    return MetaData, Table, create_engine, text, SQLAlchemyError


def target_count(connection: Any, text: Any, table_name: str) -> int:
    result = connection.execute(text(f"select count(*) from {quote_identifier(table_name)}"))
    return int(result.scalar_one())


def target_alembic_revision(connection: Any, text: Any) -> str | None:
    try:
        result = connection.execute(text("select version_num from alembic_version order by version_num"))
        versions = [row[0] for row in result]
    except Exception:
        return None
    if not versions:
        return None
    return ",".join(versions)


def target_table_counts(connection: Any, text: Any) -> dict[str, int]:
    return {table_name: target_count(connection, text, table_name) for table_name in TABLE_ORDER}


def require_empty_target_application_tables(connection: Any, text: Any) -> dict[str, int]:
    counts = target_table_counts(connection, text)
    non_empty = {table_name: count for table_name, count in counts.items() if count}
    if non_empty:
        formatted = ", ".join(f"{table}={count}" for table, count in sorted(non_empty.items()))
        raise MigrationError(
            "Target application tables are not empty; refusing to copy without a separately "
            f"approved safe mode. Non-empty tables: {formatted}"
        )
    return counts


def target_orphan_count(connection: Any, text: Any, provenance_table: str) -> int:
    result = connection.execute(
        text(
            f"""
            select count(*)
            from {quote_identifier(provenance_table)} provenance
            left join source_documents source
              on provenance.source_document_id = source.id
            where provenance.source_document_id is not null
              and source.id is null
            """
        )
    )
    return int(result.scalar_one())


def target_provenance_issues(connection: Any, text: Any) -> list[str]:
    issues = []
    data_orphans = target_orphan_count(connection, text, "data_provenance")
    if data_orphans:
        issues.append(f"data_provenance has {data_orphans} rows with missing source_documents")
    rule_orphans = target_orphan_count(connection, text, "rule_provenance")
    if rule_orphans:
        issues.append(f"rule_provenance has {rule_orphans} rows with missing source_documents")
    return issues


def batch_rows(rows: Iterable[dict[str, Any]], batch_size: int) -> Iterable[list[dict[str, Any]]]:
    batch: list[dict[str, Any]] = []
    for row in rows:
        batch.append(row)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def copy_source_to_target(source_file: Path, target_url: str, dry_run: bool, batch_size: int = 500) -> dict[str, Any]:
    validate_postgres_url(target_url)
    source_report = build_source_report(source_file)
    MetaData, Table, create_engine, text, SQLAlchemyError = import_sqlalchemy()
    redacted_target_url = redact_url(target_url)

    try:
        engine = create_engine(target_url, future=True)
        with engine.begin() as target_connection:
            target_revision = target_alembic_revision(target_connection, text)
            if target_revision != EXPECTED_ALEMBIC_HEAD:
                raise MigrationError(
                    "Target Alembic revision is not at expected head "
                    f"{EXPECTED_ALEMBIC_HEAD}; observed {target_revision or 'none'}."
                )
            initial_target_counts = require_empty_target_application_tables(target_connection, text)
            if dry_run:
                return {
                    "mode": "dry-run",
                    "target_url": redacted_target_url,
                    "source_counts": source_report.table_counts,
                    "target_counts": initial_target_counts,
                    "would_copy_tables": TABLE_ORDER,
                    "source_validation": validation_summary(source_report),
                }

            metadata = MetaData()
            reflected_tables = {
                table_name: Table(table_name, metadata, autoload_with=target_connection)
                for table_name in TABLE_ORDER
            }
            copied_counts: dict[str, int] = {}
            with open_sqlite_readonly(source_file) as source_connection:
                require_source_tables(source_connection)
                for table_name in TABLE_ORDER:
                    copied_counts[table_name] = 0
                    target_table = reflected_tables[table_name]
                    for batch in batch_rows(iter_source_rows(source_connection, table_name), batch_size):
                        target_connection.execute(target_table.insert(), batch)
                        copied_counts[table_name] += len(batch)

            final_target_counts = target_table_counts(target_connection, text)
            mismatches = {
                table_name: {
                    "source": source_report.table_counts[table_name],
                    "target": final_target_counts[table_name],
                }
                for table_name in TABLE_ORDER
                if source_report.table_counts[table_name] != final_target_counts[table_name]
            }
            provenance_issues = target_provenance_issues(target_connection, text)
            return {
                "mode": "execute",
                "target_url": redacted_target_url,
                "copied_counts": copied_counts,
                "target_counts": final_target_counts,
                "count_mismatches": mismatches,
                "target_provenance_issues": provenance_issues,
                "source_validation": validation_summary(source_report),
            }
    except MigrationError:
        raise
    except SQLAlchemyError as exc:
        raise MigrationError(
            f"Target Postgres operation failed for {redacted_target_url}: {exc.__class__.__name__}"
        ) from None


def validation_summary(source_report: SourceReport) -> dict[str, Any]:
    return {
        "sqlite_foreign_key_issue_count": len(source_report.sqlite_foreign_key_issues),
        "provenance_issues": source_report.provenance_issues,
        "audit_event_count": source_report.audit_event_count,
        "sample_primary_keys": source_report.sample_primary_keys,
    }


def print_source_report(source_report: SourceReport) -> None:
    payload = {
        "mode": "report",
        "source_file": str(source_report.source_file),
        "source_file_size": source_report.source_file_size,
        "table_order": TABLE_ORDER,
        "table_counts": source_report.table_counts,
        "validation": validation_summary(source_report),
    }
    print(json.dumps(payload, indent=2, sort_keys=True, default=str))


def print_copy_report(report: dict[str, Any]) -> None:
    print(json.dumps(report, indent=2, sort_keys=True, default=str))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PG-8E SQLite-to-Postgres migration helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    report_parser = subparsers.add_parser("report", help="Inspect source SQLite only")
    report_parser.add_argument("--source-file", type=Path, default=DEFAULT_SOURCE_FILE)

    copy_parser = subparsers.add_parser("copy", help="Dry-run or execute a source-to-target copy")
    copy_parser.add_argument("--source-file", type=Path, default=DEFAULT_SOURCE_FILE)
    copy_parser.add_argument("--target-url", required=True, help="Explicit Postgres SQLAlchemy URL")
    copy_parser.add_argument("--execute", action="store_true", help="Perform the copy. Omit for dry-run.")
    copy_parser.add_argument("--batch-size", type=int, default=500)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "report":
            print_source_report(build_source_report(args.source_file))
            return 0
        if args.command == "copy":
            report = copy_source_to_target(
                source_file=args.source_file,
                target_url=args.target_url,
                dry_run=not args.execute,
                batch_size=args.batch_size,
            )
            print_copy_report(report)
            return 0
    except MigrationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
