import pandas as pd
import pytest

from src.data_quality import assert_quality, require_positive, require_unique_key, require_values_in_set


def test_require_unique_key_fails_for_duplicate_ids():
    df = pd.DataFrame({"id": [1, 1, 2], "minutes": [30, 40, 50]})
    result = require_unique_key(df, "sample", "id")
    assert result.passed is False
    assert result.failed_rows == 1


def test_require_positive_passes_for_valid_minutes():
    df = pd.DataFrame({"minutes": [1, 30, 90]})
    result = require_positive(df, "sample", "minutes")
    assert result.passed is True


def test_require_values_in_set_catches_invalid_skill():
    df = pd.DataFrame({"skill": ["vocab", "reading", "random"]})
    result = require_values_in_set(df, "study_sessions", "skill", {"vocab", "reading"})
    assert result.passed is False
    assert result.failed_rows == 1


def test_assert_quality_raises_on_failure():
    df = pd.DataFrame({"minutes": [30, -1]})
    result = require_positive(df, "sample", "minutes")
    with pytest.raises(ValueError):
        assert_quality([result])
