from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.config import GOLD_DIR, WAREHOUSE_DB, WAREHOUSE_DIR


def load_gold_to_sqlite(gold_dir: Path = GOLD_DIR, db_path: Path = WAREHOUSE_DB) -> list[str]:
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    loaded_tables: list[str] = []

    with sqlite3.connect(db_path) as conn:
        for path in sorted(gold_dir.glob("*.parquet")):
            table_name = path.stem
            df = pd.read_parquet(path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            loaded_tables.append(table_name)

    return loaded_tables
