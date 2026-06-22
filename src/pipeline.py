from __future__ import annotations

from src.config import RAW_DIR, WAREHOUSE_DB
from src.generate_sample_data import main as generate_sample_data
from src.load import load_gold_to_sqlite
from src.transform import run_transforms


def main() -> None:
    if not any(RAW_DIR.glob("*.csv")):
        print("No raw CSV files found. Generating synthetic study data first.")
        generate_sample_data()

    marts = run_transforms()
    loaded_tables = load_gold_to_sqlite()

    print("Pipeline completed successfully.")
    print(f"Gold marts created: {', '.join(marts.keys())}")
    print(f"SQLite tables loaded: {', '.join(loaded_tables)}")
    print(f"Local warehouse: {WAREHOUSE_DB}")


if __name__ == "__main__":
    main()
