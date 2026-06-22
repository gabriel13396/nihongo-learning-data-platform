from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
WAREHOUSE_DIR = PROJECT_ROOT / "warehouse"
WAREHOUSE_DB = WAREHOUSE_DIR / "nihongo_analytics.db"

EXPECTED_RAW_FILES = [
    "study_sessions.csv",
    "vocab_reviews.csv",
    "reading_logs.csv",
    "grammar_drills.csv",
    "tutoring_sessions.csv",
]

for directory in [RAW_DIR, BRONZE_DIR, SILVER_DIR, GOLD_DIR, WAREHOUSE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
