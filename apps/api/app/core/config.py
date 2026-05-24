from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Residential Energy Planner API"
    api_version: str = "0.1.0"
    debug: bool = True
    data_dir: Path = Path(__file__).resolve().parents[2] / "data"
    database_file: str = "residential_energy_planner.sqlite3"
    database_url: str = ""

    @property
    def sqlite_path(self) -> Path:
        return self.data_dir / self.database_file

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"sqlite:///{self.sqlite_path}"


settings = Settings()
