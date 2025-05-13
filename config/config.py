from pydantic import BaseModel, FilePath, Path as PPath
from pathlib import Path
import yaml

class LoggingConfig(BaseModel):
    level: str         # e.g., INFO, DEBUG
    file: PPath        # Path to log file

class DBConfig(BaseModel):
    schema_file: FilePath  # SQL DDL file
    db_path: PPath          # SQLite DB path

class Settings(BaseModel):
    database: DBConfig
    logging: LoggingConfig

    @classmethod
    def from_yaml(cls) -> "Settings":
        config_path = Path(f"config/settings.yaml")
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found")
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)
