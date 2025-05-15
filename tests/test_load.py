import sqlite3
from pathlib import Path
from typing import Generator

import pytest

from etl.load import create_fund_positions_table, load_csvs_into_db, run_sql_script


@pytest.fixture
def db_connection(tmp_path: Path) -> Generator[sqlite3.Connection, None, None]:
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()


def test_run_sql_script(db_connection: sqlite3.Connection, tmp_path: Path) -> None:
    sql_file = tmp_path / "init.sql"
    sql_file.write_text("CREATE TABLE test_table (id INTEGER PRIMARY KEY);")
    run_sql_script(db_connection, sql_file)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='test_table';"
    )
    assert cursor.fetchone() is not None


def test_create_fund_positions_table(db_connection: sqlite3.Connection) -> None:
    create_fund_positions_table(db_connection)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='fund_positions';"
    )
    assert cursor.fetchone() is not None


def test_load_csvs_into_db(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    csv_path = tmp_path / "Applebead.30-04-2023.csv"
    csv_path.write_text("price,market value,quantity\n100.5,1000,10")

    conn = sqlite3.connect(db_path)
    create_fund_positions_table(conn)
    load_csvs_into_db(conn, tmp_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM fund_positions")
    assert cursor.fetchone()[0] == 1
    conn.close()
