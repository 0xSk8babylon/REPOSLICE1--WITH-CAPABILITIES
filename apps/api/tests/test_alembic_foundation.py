import pathlib
import unittest

import tests.fast_db  # noqa: F401, E402  must precede app imports (binds in-memory DB)

from sqlalchemy.pool import NullPool, StaticPool

from app.core.database import engine_kwargs_for_url


MIGRATIONS_DIR = pathlib.Path(__file__).resolve().parents[1] / "migrations"
ENV_PATH = MIGRATIONS_DIR / "env.py"


class AlembicFoundationTests(unittest.TestCase):
    def test_env_uses_application_settings_url_and_metadata(self):
        source = ENV_PATH.read_text()

        self.assertIn("settings.resolved_database_url", source)
        self.assertIn("target_metadata = Base.metadata", source)

    def test_env_reuses_dialect_aware_runtime_engine_kwargs(self):
        source = ENV_PATH.read_text()

        self.assertIn("engine_kwargs_for_url", source)
        self.assertIn("migration_engine_kwargs", source)
        self.assertIn("create_engine(", source)
        self.assertNotIn("engine_from_config", source)

    def test_migration_engine_defaults_preserve_sqlite_memory_pooling(self):
        namespace = {"pool": __import__("sqlalchemy.pool").pool}
        exec(
            "from app.core.database import engine_kwargs_for_url\n"
            "def migration_engine_kwargs(url):\n"
            "    kwargs = engine_kwargs_for_url(url)\n"
            "    kwargs.setdefault('poolclass', pool.NullPool)\n"
            "    return kwargs\n",
            namespace,
        )

        kwargs = namespace["migration_engine_kwargs"]("sqlite://")

        self.assertEqual({"check_same_thread": False}, kwargs["connect_args"])
        self.assertEqual(StaticPool, kwargs["poolclass"])

    def test_migration_engine_defaults_use_nullpool_for_postgres(self):
        namespace = {"pool": __import__("sqlalchemy.pool").pool}
        exec(
            "from app.core.database import engine_kwargs_for_url\n"
            "def migration_engine_kwargs(url):\n"
            "    kwargs = engine_kwargs_for_url(url)\n"
            "    kwargs.setdefault('poolclass', pool.NullPool)\n"
            "    return kwargs\n",
            namespace,
        )

        kwargs = namespace["migration_engine_kwargs"](
            "postgresql+psycopg://planner:secret@localhost:5432/energy"
        )

        self.assertEqual({"future": True, "poolclass": NullPool}, kwargs)

    def test_runtime_helper_keeps_postgres_free_of_sqlite_connect_args(self):
        kwargs = engine_kwargs_for_url("postgresql+psycopg://planner:secret@localhost:5432/energy")

        self.assertEqual({"future": True}, kwargs)


if __name__ == "__main__":
    unittest.main()
