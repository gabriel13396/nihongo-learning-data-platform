from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

from src.config import BRONZE_DIR, GOLD_DIR, RAW_DIR, SILVER_DIR
from src.data_quality import (
    QualityCheckResult,
    assert_quality,
    require_columns,
    require_non_null,
    require_positive,
    require_unique_key,
    require_values_in_set,
)

ALLOWED_SKILLS = {"vocab", "reading", "listening", "grammar", "speaking"}
ALLOWED_JLPT = {"N5", "N4", "N3", "N2", "N1"}
ALLOWED_STAGES = {"new", "learning", "young", "mature"}


def reset_output_dirs() -> None:
    for directory in [BRONZE_DIR, SILVER_DIR, GOLD_DIR]:
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)


def read_csv(name: str) -> pd.DataFrame:
    path = RAW_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing raw file: {path}. Run python -m src.generate_sample_data first.")
    return pd.read_csv(path)


def write_bronze(df: pd.DataFrame, table_name: str) -> None:
    df.to_parquet(BRONZE_DIR / f"{table_name}.parquet", index=False)


def write_silver(df: pd.DataFrame, table_name: str) -> None:
    df.to_parquet(SILVER_DIR / f"{table_name}.parquet", index=False)


def write_gold(df: pd.DataFrame, table_name: str) -> None:
    df.to_parquet(GOLD_DIR / f"{table_name}.parquet", index=False)
    df.to_csv(GOLD_DIR / f"{table_name}.csv", index=False)


def clean_study_sessions() -> pd.DataFrame:
    df = read_csv("study_sessions.csv")
    write_bronze(df, "study_sessions")

    required = ["session_id", "session_date", "skill", "resource", "minutes", "focus_score"]
    results: list[QualityCheckResult] = [
        require_columns(df, "study_sessions", required),
        require_non_null(df, "study_sessions", required),
        require_unique_key(df, "study_sessions", "session_id"),
        require_positive(df, "study_sessions", "minutes"),
        require_values_in_set(df, "study_sessions", "skill", ALLOWED_SKILLS),
    ]
    assert_quality(results)

    df = df.copy()
    df["session_date"] = pd.to_datetime(df["session_date"])
    df["week_start"] = df["session_date"].dt.to_period("W-MON").dt.start_time
    df["month"] = df["session_date"].dt.to_period("M").astype(str)
    df["hours"] = (df["minutes"] / 60).round(2)
    write_silver(df, "study_sessions_clean")
    return df


def clean_vocab_reviews() -> pd.DataFrame:
    df = read_csv("vocab_reviews.csv")
    write_bronze(df, "vocab_reviews")

    required = [
        "review_id",
        "review_date",
        "card_id",
        "jlpt_level",
        "review_stage",
        "response_seconds",
        "is_correct",
    ]
    results: list[QualityCheckResult] = [
        require_columns(df, "vocab_reviews", required),
        require_non_null(df, "vocab_reviews", required),
        require_unique_key(df, "vocab_reviews", "review_id"),
        require_positive(df, "vocab_reviews", "response_seconds"),
        require_values_in_set(df, "vocab_reviews", "jlpt_level", ALLOWED_JLPT),
        require_values_in_set(df, "vocab_reviews", "review_stage", ALLOWED_STAGES),
    ]
    assert_quality(results)

    df = df.copy()
    df["review_date"] = pd.to_datetime(df["review_date"])
    df["week_start"] = df["review_date"].dt.to_period("W-MON").dt.start_time
    df["is_correct"] = df["is_correct"].astype(int)
    write_silver(df, "vocab_reviews_clean")
    return df


def clean_reading_logs() -> pd.DataFrame:
    df = read_csv("reading_logs.csv")
    write_bronze(df, "reading_logs")

    required = [
        "reading_id",
        "reading_date",
        "title",
        "pages_read",
        "unknown_words_logged",
        "perceived_difficulty",
    ]
    results: list[QualityCheckResult] = [
        require_columns(df, "reading_logs", required),
        require_non_null(df, "reading_logs", required),
        require_unique_key(df, "reading_logs", "reading_id"),
        require_positive(df, "reading_logs", "pages_read"),
    ]
    assert_quality(results)

    df = df.copy()
    df["reading_date"] = pd.to_datetime(df["reading_date"])
    df["unknown_words_per_page"] = (df["unknown_words_logged"] / df["pages_read"]).round(2)
    write_silver(df, "reading_logs_clean")
    return df


def clean_grammar_drills() -> pd.DataFrame:
    df = read_csv("grammar_drills.csv")
    write_bronze(df, "grammar_drills")

    required = [
        "drill_id",
        "drill_date",
        "grammar_point",
        "jlpt_level",
        "sentences_attempted",
        "sentences_correct",
    ]
    results: list[QualityCheckResult] = [
        require_columns(df, "grammar_drills", required),
        require_non_null(df, "grammar_drills", required),
        require_unique_key(df, "grammar_drills", "drill_id"),
        require_positive(df, "grammar_drills", "sentences_attempted"),
        require_values_in_set(df, "grammar_drills", "jlpt_level", ALLOWED_JLPT),
    ]
    assert_quality(results)

    df = df.copy()
    df["drill_date"] = pd.to_datetime(df["drill_date"])
    df["grammar_accuracy"] = (df["sentences_correct"] / df["sentences_attempted"]).round(3)
    write_silver(df, "grammar_drills_clean")
    return df


def clean_tutoring_sessions() -> pd.DataFrame:
    df = read_csv("tutoring_sessions.csv")
    write_bronze(df, "tutoring_sessions")

    required = [
        "tutor_session_id",
        "session_date",
        "minutes",
        "conversation_topic",
        "self_rating",
        "new_phrases_learned",
    ]
    results: list[QualityCheckResult] = [
        require_columns(df, "tutoring_sessions", required),
        require_non_null(df, "tutoring_sessions", required),
        require_unique_key(df, "tutoring_sessions", "tutor_session_id"),
        require_positive(df, "tutoring_sessions", "minutes"),
    ]
    assert_quality(results)

    df = df.copy()
    df["session_date"] = pd.to_datetime(df["session_date"])
    df["phrases_per_hour"] = (df["new_phrases_learned"] / (df["minutes"] / 60)).round(2)
    write_silver(df, "tutoring_sessions_clean")
    return df


def build_gold_marts(
    sessions: pd.DataFrame,
    vocab: pd.DataFrame,
    reading: pd.DataFrame,
    grammar: pd.DataFrame,
    tutoring: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    daily = (
        sessions.groupby("session_date", as_index=False)
        .agg(total_minutes=("minutes", "sum"), study_activities=("session_id", "count"), avg_focus_score=("focus_score", "mean"))
        .sort_values("session_date")
    )
    daily["total_hours"] = (daily["total_minutes"] / 60).round(2)
    daily["avg_focus_score"] = daily["avg_focus_score"].round(2)

    weekly_skill = (
        sessions.pivot_table(index="week_start", columns="skill", values="minutes", aggfunc="sum", fill_value=0)
        .reset_index()
        .rename_axis(None, axis=1)
    )
    for skill in ALLOWED_SKILLS:
        if skill not in weekly_skill.columns:
            weekly_skill[skill] = 0
    weekly_skill["total_minutes"] = weekly_skill[list(ALLOWED_SKILLS)].sum(axis=1)
    weekly_skill["speaking_pct"] = (weekly_skill["speaking"] / weekly_skill["total_minutes"]).round(3)
    weekly_skill["reading_listening_pct"] = ((weekly_skill["reading"] + weekly_skill["listening"]) / weekly_skill["total_minutes"]).round(3)
    weekly_skill = weekly_skill.sort_values("week_start")

    vocab_retention = (
        vocab.groupby(["jlpt_level", "review_stage"], as_index=False)
        .agg(total_reviews=("review_id", "count"), correct_reviews=("is_correct", "sum"), avg_response_seconds=("response_seconds", "mean"))
    )
    vocab_retention["retention_rate"] = (vocab_retention["correct_reviews"] / vocab_retention["total_reviews"]).round(3)
    vocab_retention["avg_response_seconds"] = vocab_retention["avg_response_seconds"].round(2)

    latest_week = weekly_skill["week_start"].max()
    latest_week_skill = weekly_skill[weekly_skill["week_start"] == latest_week].copy()
    latest_total_minutes = int(latest_week_skill["total_minutes"].iloc[0])
    latest_balance = float(latest_week_skill["reading_listening_pct"].iloc[0])
    n2_retention = float(
        vocab_retention[vocab_retention["jlpt_level"] == "N2"]["retention_rate"].mean().round(3)
    )
    grammar_accuracy = float(grammar["grammar_accuracy"].mean().round(3))
    tutoring_hours = float((tutoring["minutes"].sum() / 60).round(2))
    pages_read = int(reading["pages_read"].sum())

    consistency_score = min(100, round((latest_total_minutes / 900) * 100, 1))
    input_balance_score = min(100, round(latest_balance / 0.45 * 100, 1))
    retention_score = round(n2_retention * 100, 1)
    grammar_score = round(grammar_accuracy * 100, 1)
    readiness_score = round(
        consistency_score * 0.3 + input_balance_score * 0.25 + retention_score * 0.3 + grammar_score * 0.15,
        1,
    )

    readiness = pd.DataFrame(
        [
            {
                "as_of_week_start": latest_week,
                "weekly_minutes": latest_total_minutes,
                "total_tutoring_hours": tutoring_hours,
                "total_pages_read": pages_read,
                "n2_vocab_retention": n2_retention,
                "grammar_accuracy": grammar_accuracy,
                "consistency_score": consistency_score,
                "input_balance_score": input_balance_score,
                "retention_score": retention_score,
                "grammar_score": grammar_score,
                "learning_readiness_score": readiness_score,
            }
        ]
    )

    marts = {
        "gold_daily_study_summary": daily,
        "gold_weekly_skill_balance": weekly_skill,
        "gold_vocab_retention_by_level": vocab_retention,
        "gold_learning_readiness_score": readiness,
    }

    for table_name, df in marts.items():
        write_gold(df, table_name)

    return marts


def run_transforms() -> dict[str, pd.DataFrame]:
    reset_output_dirs()
    sessions = clean_study_sessions()
    vocab = clean_vocab_reviews()
    reading = clean_reading_logs()
    grammar = clean_grammar_drills()
    tutoring = clean_tutoring_sessions()
    return build_gold_marts(sessions, vocab, reading, grammar, tutoring)
