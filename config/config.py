from pathlib import Path

import yaml
from pydantic import BaseModel, FilePath


class LoggingConfig(BaseModel):
    level: str  # e.g., INFO, DEBUG
    file: Path  # Path to log file


class DBConfig(BaseModel):
    schema_file: FilePath  # SQL DDL file
    db_path: Path  # SQLite DB path


class Settings(BaseModel):
    database: DBConfig
    logging: LoggingConfig

    @classmethod
    def from_yaml(cls, path: Path = Path("config/settings.yaml")) -> "Settings":
        if not path.exists():
            raise FileNotFoundError(f"Settings file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)
