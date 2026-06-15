from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

Base = declarative_base()


def database_backend_for_url(database_url: str) -> str:
    return make_url(database_url).get_backend_name()


def engine_kwargs_for_url(database_url: str):
    kwargs = {"future": True}
    if database_backend_for_url(database_url) == "sqlite":
        kwargs["connect_args"] = {"check_same_thread": False}
        if make_url(database_url).database in (None, "", ":memory:"):
            kwargs["poolclass"] = StaticPool
    return kwargs


def redact_database_url(database_url: str) -> str:
    return make_url(database_url).render_as_string(hide_password=True)


def database_backend() -> str:
    return database_backend_for_url(settings.resolved_database_url)


def is_sqlite_database() -> bool:
    return database_backend() == "sqlite"


if is_sqlite_database():
    settings.data_dir.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    settings.resolved_database_url,
    **engine_kwargs_for_url(settings.resolved_database_url),
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def database_path() -> Path:
    if not is_sqlite_database():
        raise RuntimeError("database_path is only available for SQLite-backed local development")
    return settings.sqlite_path


def database_connection_summary():
    return {
        "backend": database_backend(),
        "url": redact_database_url(settings.resolved_database_url),
        "create_all_on_startup": settings.should_create_all_on_startup,
        "seed_demo_data_on_startup": settings.should_seed_demo_data_on_startup,
    }
