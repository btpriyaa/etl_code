import sqlite3
from pathlib import Path

from config.config import Settings
from etl.load import create_fund_positions_table, load_csvs_into_db, run_sql_script


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    settings = Settings.from_yaml(base_dir / "config" / "settings.yaml")

    print(f"[INFO] Connecting to database at {settings.database.db_path}...")
    conn = sqlite3.connect(settings.database.db_path)

    run_sql_script(conn, settings.database.schema_file)
    create_fund_positions_table(conn)
    load_csvs_into_db(conn, base_dir / "data" / "raw" / "external-funds")

    conn.commit()
    conn.close()
    print("[INFO] Database setup completed.")


if __name__ == "__main__":
    main()
