from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from src.config import RAW_DIR

random.seed(42)

SKILLS = ["vocab", "reading", "listening", "grammar", "speaking"]
JLPT_LEVELS = ["N5", "N4", "N3", "N2"]


def date_range(start: date, days: int) -> list[date]:
    return [start + timedelta(days=offset) for offset in range(days)]


def generate_study_sessions(output_dir: Path) -> None:
    rows: list[dict] = []
    start = date(2026, 1, 1)
    session_id = 1

    for current_day in date_range(start, 120):
        # Most days have two or three activities. Some days are lighter.
        planned_skills = random.sample(SKILLS, k=random.choice([2, 2, 3, 4]))
        for skill in planned_skills:
            minutes = {
                "vocab": random.randint(35, 90),
                "reading": random.randint(25, 75),
                "listening": random.randint(30, 120),
                "grammar": random.randint(20, 55),
                "speaking": random.randint(30, 90),
            }[skill]
            rows.append(
                {
                    "session_id": session_id,
                    "session_date": current_day.isoformat(),
                    "skill": skill,
                    "resource": random.choice(
                        [
                            "Anki",
                            "Bunpro",
                            "Tutor Conversation",
                            "Native Book",
                            "Anime Listening",
                            "NHK Easy",
                            "Grammar Drill Notebook",
                        ]
                    ),
                    "minutes": minutes,
                    "focus_score": round(random.uniform(0.65, 0.98), 2),
                }
            )
            session_id += 1

    pd.DataFrame(rows).to_csv(output_dir / "study_sessions.csv", index=False)


def generate_vocab_reviews(output_dir: Path) -> None:
    rows: list[dict] = []
    start = date(2026, 1, 1)
    review_id = 1

    for current_day in date_range(start, 120):
        daily_reviews = random.randint(35, 100)
        for _ in range(daily_reviews):
            jlpt = random.choices(JLPT_LEVELS, weights=[0.1, 0.25, 0.4, 0.25], k=1)[0]
            stage = random.choices(["new", "learning", "young", "mature"], weights=[0.08, 0.22, 0.35, 0.35], k=1)[0]
            base_accuracy = {"N5": 0.94, "N4": 0.9, "N3": 0.84, "N2": 0.75}[jlpt]
            stage_adjustment = {"new": -0.18, "learning": -0.08, "young": 0.0, "mature": 0.07}[stage]
            probability_correct = max(0.45, min(0.98, base_accuracy + stage_adjustment))
            rows.append(
                {
                    "review_id": review_id,
                    "review_date": current_day.isoformat(),
                    "card_id": random.randint(10000, 99999),
                    "jlpt_level": jlpt,
                    "review_stage": stage,
                    "response_seconds": random.randint(2, 28),
                    "is_correct": int(random.random() < probability_correct),
                }
            )
            review_id += 1

    pd.DataFrame(rows).to_csv(output_dir / "vocab_reviews.csv", index=False)


def generate_reading_logs(output_dir: Path) -> None:
    books = [
        "Convenience Store Woman",
        "Your Name",
        "Bookworm Light Novel",
        "NHK Easy Articles",
        "Japanese Short Stories",
    ]
    rows: list[dict] = []
    start = date(2026, 1, 1)
    log_id = 1

    for current_day in date_range(start, 120):
        if random.random() < 0.62:
            pages = random.randint(3, 28)
            rows.append(
                {
                    "reading_id": log_id,
                    "reading_date": current_day.isoformat(),
                    "title": random.choice(books),
                    "pages_read": pages,
                    "unknown_words_logged": random.randint(3, max(4, pages * 4)),
                    "perceived_difficulty": random.choice(["easy", "medium", "hard"]),
                }
            )
            log_id += 1

    pd.DataFrame(rows).to_csv(output_dir / "reading_logs.csv", index=False)


def generate_grammar_drills(output_dir: Path) -> None:
    grammar_points = [
        "ないことには",
        "末に",
        "によって",
        "場合じゃない",
        "せず",
        "ことになっている",
        "ようにする",
        "に違いない",
    ]
    rows: list[dict] = []
    start = date(2026, 1, 1)
    drill_id = 1

    for current_day in date_range(start, 120):
        if random.random() < 0.7:
            for point in random.sample(grammar_points, k=random.choice([1, 2, 3])):
                attempts = random.randint(2, 8)
                correct = random.randint(max(1, attempts - 3), attempts)
                rows.append(
                    {
                        "drill_id": drill_id,
                        "drill_date": current_day.isoformat(),
                        "grammar_point": point,
                        "jlpt_level": random.choice(["N3", "N2"]),
                        "sentences_attempted": attempts,
                        "sentences_correct": correct,
                    }
                )
                drill_id += 1

    pd.DataFrame(rows).to_csv(output_dir / "grammar_drills.csv", index=False)


def generate_tutoring_sessions(output_dir: Path) -> None:
    rows: list[dict] = []
    start = date(2026, 1, 1)
    session_id = 1

    for current_day in date_range(start, 120):
        if current_day.weekday() in [1, 5] and random.random() < 0.78:
            minutes = random.choice([60, 75, 90])
            rows.append(
                {
                    "tutor_session_id": session_id,
                    "session_date": current_day.isoformat(),
                    "minutes": minutes,
                    "conversation_topic": random.choice(
                        [
                            "travel stories",
                            "daily routine",
                            "work and career",
                            "anime and media",
                            "Japanese grammar",
                            "future Japan plans",
                        ]
                    ),
                    "self_rating": random.randint(3, 5),
                    "new_phrases_learned": random.randint(4, 18),
                }
            )
            session_id += 1

    pd.DataFrame(rows).to_csv(output_dir / "tutoring_sessions.csv", index=False)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    generate_study_sessions(RAW_DIR)
    generate_vocab_reviews(RAW_DIR)
    generate_reading_logs(RAW_DIR)
    generate_grammar_drills(RAW_DIR)
    generate_tutoring_sessions(RAW_DIR)
    print(f"Synthetic raw data written to: {RAW_DIR}")


if __name__ == "__main__":
    main()
