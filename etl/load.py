import sqlite3
from pathlib import Path

from etl.extract import extract_csv_data


def run_sql_script(conn: sqlite3.Connection, sql_file: Path) -> None:
    with open(sql_file, "r") as file:
        sql_script = file.read()
    conn.executescript(sql_script)
    print("[INFO] Executed schema SQL.")


def create_fund_positions_table(conn: sqlite3.Connection) -> None:
    create_sql = """
    CREATE TABLE IF NOT EXISTS fund_positions (
        fund_name TEXT,
        position_date TEXT,
        price REAL,
        market_value REAL,
        quantity REAL,
        financial_type TEXT,
        symbol TEXT,
        security_name TEXT,
        sedol TEXT,
        realised_pl TEXT,
        isin TEXT 
    );
    """
    conn.execute(create_sql)
    print("[INFO] Created table fund_positions.")


def load_csvs_into_db(conn: sqlite3.Connection, csv_folder: Path) -> None:
    for csv_file in csv_folder.glob("*.csv"):
        df = extract_csv_data(csv_file)
        df.to_sql("fund_positions", conn, if_exists="append", index=False)
        print(f"[INFO] Loaded {csv_file.name}")
