"""Fast in-memory database harness for the test suite.

Importing this module (before any ``app.*`` import) binds the application
engine to a single shared in-memory SQLite database instead of an on-disk
file. The demo dataset is seeded exactly once per process and captured as an
in-memory template via SQLite's backup API; ``reset_and_reseed()`` restores
that template in milliseconds instead of deleting the database file and
re-running the full seed + revision pipeline for every test.

This module must be the first project import in every test file so the
environment variables below are set before ``app.core.config`` is evaluated.
"""

import os

# Must run before any app.* import so the engine binds to in-memory SQLite.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ.setdefault("DATA_DIR", "/tmp/residential-energy-planner-tests")

import sqlite3  # noqa: E402

from sqlalchemy.orm import Session  # noqa: E402

from app.core.database import Base, engine  # noqa: E402
from app.seed.runtime import seed_database  # noqa: E402

_template = None


def _live_connection():
    """Check out the engine's single in-memory DBAPI connection."""
    raw = engine.raw_connection()
    raw.rollback()  # defensively clear any implicit transaction before backup
    return raw


def _build_template():
    """Seed the in-memory database once and snapshot it as a template."""
    global _template
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        seed_database(db, force=True)
    _template = sqlite3.connect(":memory:")
    raw = _live_connection()
    try:
        raw.driver_connection.backup(_template)
    finally:
        raw.close()


def reset_and_reseed():
    """Drop-in replacement for app.seed.runtime.reset_and_reseed in tests.

    Restores the seeded template snapshot into the live in-memory database.
    """
    raw = _live_connection()
    try:
        _template.backup(raw.driver_connection)
    finally:
        raw.close()


# Build eagerly at import so every test module (including ones that never
# call reset_and_reseed) starts from a fully seeded database, matching the
# old behavior where the first module's setUpClass seeded the shared DB.
_build_template()
