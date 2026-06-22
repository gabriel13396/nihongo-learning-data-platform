from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class QualityCheckResult:
    table_name: str
    check_name: str
    passed: bool
    failed_rows: int
    details: str


def require_columns(df: pd.DataFrame, table_name: str, required_columns: list[str]) -> QualityCheckResult:
    missing = [column for column in required_columns if column not in df.columns]
    return QualityCheckResult(
        table_name=table_name,
        check_name="required_columns",
        passed=len(missing) == 0,
        failed_rows=len(missing),
        details=f"Missing columns: {missing}" if missing else "All required columns are present.",
    )


def require_non_null(df: pd.DataFrame, table_name: str, columns: list[str]) -> QualityCheckResult:
    failed_rows = int(df[columns].isna().any(axis=1).sum())
    return QualityCheckResult(
        table_name=table_name,
        check_name="non_null_values",
        passed=failed_rows == 0,
        failed_rows=failed_rows,
        details=f"Rows with nulls in {columns}: {failed_rows}",
    )


def require_positive(df: pd.DataFrame, table_name: str, column: str) -> QualityCheckResult:
    failed_rows = int((df[column] <= 0).sum())
    return QualityCheckResult(
        table_name=table_name,
        check_name=f"positive_{column}",
        passed=failed_rows == 0,
        failed_rows=failed_rows,
        details=f"Rows with {column} <= 0: {failed_rows}",
    )


def require_values_in_set(df: pd.DataFrame, table_name: str, column: str, allowed_values: set[str]) -> QualityCheckResult:
    failed_rows = int((~df[column].isin(allowed_values)).sum())
    return QualityCheckResult(
        table_name=table_name,
        check_name=f"valid_{column}",
        passed=failed_rows == 0,
        failed_rows=failed_rows,
        details=f"Rows with invalid {column}: {failed_rows}",
    )


def require_unique_key(df: pd.DataFrame, table_name: str, key_column: str) -> QualityCheckResult:
    failed_rows = int(df.duplicated(subset=[key_column]).sum())
    return QualityCheckResult(
        table_name=table_name,
        check_name=f"unique_{key_column}",
        passed=failed_rows == 0,
        failed_rows=failed_rows,
        details=f"Duplicate keys in {key_column}: {failed_rows}",
    )


def assert_quality(results: list[QualityCheckResult]) -> None:
    failures = [result for result in results if not result.passed]
    if failures:
        formatted = "\n".join(
            f"{failure.table_name}.{failure.check_name}: {failure.details}" for failure in failures
        )
        raise ValueError(f"Data quality checks failed:\n{formatted}")
