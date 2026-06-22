from pathlib import Path

import pandas as pd

from src.config import GOLD_DIR, WAREHOUSE_DB
from src.generate_sample_data import main as generate_sample_data
from src.pipeline import main as run_pipeline


def test_pipeline_creates_gold_outputs():
    generate_sample_data()
    run_pipeline()

    expected_tables = [
        "gold_daily_study_summary",
        "gold_weekly_skill_balance",
        "gold_vocab_retention_by_level",
        "gold_learning_readiness_score",
    ]

    for table in expected_tables:
        parquet_path = GOLD_DIR / f"{table}.parquet"
        csv_path = GOLD_DIR / f"{table}.csv"
        assert parquet_path.exists()
        assert csv_path.exists()
        assert len(pd.read_parquet(parquet_path)) > 0

    assert Path(WAREHOUSE_DB).exists()


def test_readiness_score_is_in_valid_range():
    generate_sample_data()
    run_pipeline()

    readiness = pd.read_parquet(GOLD_DIR / "gold_learning_readiness_score.parquet")
    score = readiness.loc[0, "learning_readiness_score"]

    assert 0 <= score <= 100
