import unittest

import tests.fast_db  # noqa: F401, E402  must precede app imports (binds in-memory DB)

from app.core.config import Settings  # noqa: E402
from app.core.database import (  # noqa: E402
    database_connection_summary,
    database_path,
    engine_kwargs_for_url,
    redact_database_url,
)
from app.main import root  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402


class DatabaseFoundationTests(unittest.TestCase):
    def test_sqlite_engine_keeps_thread_check_disabled_and_static_pool_for_memory(self):
        kwargs = engine_kwargs_for_url("sqlite://")

        self.assertEqual({"check_same_thread": False}, kwargs["connect_args"])
        self.assertEqual(StaticPool, kwargs["poolclass"])

    def test_postgres_engine_does_not_receive_sqlite_connect_args(self):
        kwargs = engine_kwargs_for_url("postgresql://planner:secret@localhost:5432/energy")

        self.assertEqual({"future": True}, kwargs)

    def test_postgres_url_alias_is_normalized_for_sqlalchemy(self):
        settings = Settings(database_url="postgres://planner:secret@localhost:5432/energy")

        self.assertEqual(
            "postgresql://planner:secret@localhost:5432/energy",
            settings.resolved_database_url,
        )
        self.assertEqual("postgresql", settings.database_backend)
        self.assertFalse(settings.should_create_all_on_startup)
        self.assertFalse(settings.should_seed_demo_data_on_startup)

    def test_explicit_startup_flags_override_non_sqlite_defaults(self):
        settings = Settings(
            database_url="postgresql://planner:secret@localhost:5432/energy",
            database_create_all_on_startup=True,
            database_seed_demo_data_on_startup=True,
        )

        self.assertTrue(settings.should_create_all_on_startup)
        self.assertTrue(settings.should_seed_demo_data_on_startup)

    def test_connection_summary_redacts_database_credentials(self):
        redacted = redact_database_url("postgresql://planner:secret@localhost:5432/energy")

        self.assertEqual("postgresql://planner:***@localhost:5432/energy", redacted)

    def test_current_test_database_remains_sqlite(self):
        summary = database_connection_summary()

        self.assertEqual("sqlite", summary["backend"])
        self.assertTrue(summary["url"].startswith("sqlite://"))
        self.assertTrue(summary["create_all_on_startup"])
        self.assertTrue(summary["seed_demo_data_on_startup"])
        self.assertIsNotNone(database_path())

    def test_root_response_preserves_redacted_database_url_field(self):
        response = root()

        self.assertIn("database_url", response)
        self.assertIn("database", response)
        self.assertEqual(response["database"]["url"], response["database_url"])


if __name__ == "__main__":
    unittest.main()
