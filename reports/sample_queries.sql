-- Weekly study workload
SELECT
    week_start,
    total_minutes,
    ROUND(total_minutes / 60.0, 2) AS total_hours,
    speaking_pct,
    reading_listening_pct
FROM gold_weekly_skill_balance
ORDER BY week_start DESC;

-- Skill mix by week
SELECT
    week_start,
    vocab,
    reading,
    listening,
    grammar,
    speaking
FROM gold_weekly_skill_balance
ORDER BY week_start DESC;

-- Vocabulary retention by JLPT level and review stage
SELECT
    jlpt_level,
    review_stage,
    total_reviews,
    retention_rate,
    avg_response_seconds
FROM gold_vocab_retention_by_level
ORDER BY jlpt_level, review_stage;

-- Overall learning readiness score
SELECT *
FROM gold_learning_readiness_score;
