from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    app_name: str = "Residential Energy Planner API"
    api_version: str = "0.1.0"
    debug: bool = True
    data_dir: Path = Path(__file__).resolve().parents[2] / "data"
    database_file: str = "residential_energy_planner.sqlite3"
    database_url: str = ""
    database_create_all_on_startup: Optional[bool] = None
    database_seed_demo_data_on_startup: Optional[bool] = None

    @property
    def sqlite_path(self) -> Path:
        return self.data_dir / self.database_file

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self._normalize_database_url(self.database_url)
        return f"sqlite:///{self.sqlite_path}"

    @staticmethod
    def _normalize_database_url(url: str) -> str:
        if url.startswith("postgres://"):
            return "postgresql://" + url[len("postgres://") :]
        return url

    @property
    def database_backend(self) -> str:
        return make_url(self.resolved_database_url).get_backend_name()

    @property
    def is_sqlite_database(self) -> bool:
        return self.database_backend == "sqlite"

    @property
    def should_create_all_on_startup(self) -> bool:
        if self.database_create_all_on_startup is not None:
            return self.database_create_all_on_startup
        return self.is_sqlite_database

    @property
    def should_seed_demo_data_on_startup(self) -> bool:
        if self.database_seed_demo_data_on_startup is not None:
            return self.database_seed_demo_data_on_startup
        return self.is_sqlite_database


settings = Settings()
