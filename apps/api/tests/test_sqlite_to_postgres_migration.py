import sqlite3
import tempfile
import unittest
from pathlib import Path

from scripts import sqlite_to_postgres


class SqliteToPostgresMigrationScriptTests(unittest.TestCase):
    def test_redact_url_hides_password(self):
        redacted = sqlite_to_postgres.redact_url(
            "postgresql+psycopg://planner:secret@example.test:5432/energy"
        )

        self.assertEqual("postgresql+psycopg://planner:***@example.test:5432/energy", redacted)

    def test_target_url_must_be_explicit_postgres(self):
        with self.assertRaises(sqlite_to_postgres.MigrationError):
            sqlite_to_postgres.validate_postgres_url("")
        with self.assertRaises(sqlite_to_postgres.MigrationError):
            sqlite_to_postgres.validate_postgres_url("sqlite:///local.sqlite3")

        self.assertEqual(
            "postgresql://example.test/db",
            sqlite_to_postgres.validate_postgres_url("postgresql://example.test/db"),
        )

    def test_copy_parser_defaults_to_dry_run(self):
        parser = sqlite_to_postgres.build_parser()
        args = parser.parse_args(["copy", "--target-url", "postgresql://example.test/db"])

        self.assertFalse(args.execute)

    def test_non_empty_target_tables_are_refused(self):
        class FakeConnection:
            def execute(self, statement):
                table_name = str(statement).split("from ", 1)[1].strip('"')
                count = 1 if table_name == "homes" else 0

                class Result:
                    def scalar_one(self):
                        return count

                return Result()

        with self.assertRaises(sqlite_to_postgres.MigrationError):
            sqlite_to_postgres.require_empty_target_application_tables(FakeConnection(), lambda sql: sql)

    def test_target_alembic_revision_is_read(self):
        class FakeConnection:
            def execute(self, statement):
                class Result:
                    def __iter__(self):
                        return iter([(sqlite_to_postgres.EXPECTED_ALEMBIC_HEAD,)])

                return Result()

        self.assertEqual(
            sqlite_to_postgres.EXPECTED_ALEMBIC_HEAD,
            sqlite_to_postgres.target_alembic_revision(FakeConnection(), lambda sql: sql),
        )

    def test_table_order_preserves_key_dependencies(self):
        order = sqlite_to_postgres.TABLE_ORDER

        self.assertLess(order.index("accounts"), order.index("homes"))
        self.assertLess(order.index("homes"), order.index("buildings"))
        self.assertLess(order.index("buildings"), order.index("electrical_panels"))
        self.assertLess(order.index("equipment_products"), order.index("design_equipment"))
        self.assertLess(order.index("energy_system_designs"), order.index("scenarios"))
        self.assertLess(order.index("source_documents"), order.index("data_provenance"))
        self.assertLess(order.index("source_documents"), order.index("rule_provenance"))

    def test_json_and_datetime_conversion(self):
        row = {
            "specs": '{"capacity_kw": 5}',
            "created_at": "2026-06-22T12:00:00",
        }

        class FakeRow(dict):
            pass

        converted = sqlite_to_postgres.convert_row_for_postgres("equipment_products", FakeRow(row))

        self.assertEqual({"capacity_kw": 5}, converted["specs"])
        self.assertEqual(2026, converted["created_at"].year)

    def test_report_requires_expected_tables(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source.sqlite3"
            connection = sqlite3.connect(source)
            connection.execute("create table accounts (id text primary key)")
            connection.commit()
            connection.close()

            with self.assertRaises(sqlite_to_postgres.MigrationError):
                sqlite_to_postgres.build_source_report(source)


if __name__ == "__main__":
    unittest.main()
