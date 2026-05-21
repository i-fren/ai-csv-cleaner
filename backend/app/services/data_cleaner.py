"""
data_cleaner.py
---------------
Pandas-based data cleaning utilities for the AI CSV Analyzer.

Sections:
  1. Imports
  2. Type Inference & CSV Parsing Utilities  (task 3.1)
  3. Duplicate Handling                       (task 4.x)
  4. Missing Value Handling                   (task 4.x)
  5. Format Standardization                   (task 4.x)
  6. Outlier Detection & Removal              (task 4.x)
"""

# ---------------------------------------------------------------------------
# 1. Imports
# ---------------------------------------------------------------------------
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# 2. Type Inference & CSV Parsing Utilities
# ---------------------------------------------------------------------------

def infer_column_types(df: pd.DataFrame) -> dict[str, str]:
    """
    Infer a high-level type label for each column in *df*.

    Returns a dict mapping column name -> one of:
      "numeric"  – column has a numeric dtype
      "date"     – >50 % of non-null values parse as dates
      "text"     – everything else
    """
    result: dict[str, str] = {}

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            result[col] = "numeric"
        else:
            # Attempt date parsing on non-null values
            non_null = df[col].dropna()
            if len(non_null) == 0:
                result[col] = "text"
                continue

            parsed = pd.to_datetime(non_null, errors="coerce")
            success_rate = parsed.notna().sum() / len(non_null)

            if success_rate > 0.5:
                result[col] = "date"
            else:
                result[col] = "text"

    return result


def count_duplicates(df: pd.DataFrame) -> int:
    """Return the number of fully-duplicate rows in *df*."""
    return int(df.duplicated().sum())


def missing_value_summary(df: pd.DataFrame) -> dict[str, dict]:
    """
    Return a per-column summary of missing values.

    Each entry has the shape expected by ``MissingValueInfo``:
      {"count": int, "percentage": float}

    ``percentage`` is computed as ``count / len(df) * 100`` when the
    DataFrame is non-empty, and ``0.0`` otherwise.
    """
    summary: dict[str, dict] = {}
    total_rows = len(df)

    for col in df.columns:
        missing_count = int(df[col].isna().sum())
        percentage = (missing_count / total_rows * 100) if total_rows > 0 else 0.0
        summary[col] = {"count": missing_count, "percentage": percentage}

    return summary


# ---------------------------------------------------------------------------
# 3. Duplicate Handling
# ---------------------------------------------------------------------------

def remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove duplicate rows, keeping first occurrence. Returns (new_df, rows_removed)."""
    original_len = len(df)
    new_df = df.drop_duplicates(keep="first").reset_index(drop=True)
    rows_removed = original_len - len(new_df)
    return new_df, rows_removed


# ---------------------------------------------------------------------------
# 4. Missing Value Handling
# ---------------------------------------------------------------------------

def apply_missing_value_strategies(
    df: pd.DataFrame,
    strategies: list,
) -> tuple[pd.DataFrame, int, dict]:
    """
    Apply per-column missing value strategies.
    strategies: list of MissingValueStrategy-like objects with .column, .method, .fill_value
    Returns (new_df, resolved_count, updated_missing_summary_dict)
    """
    new_df = df.copy()
    resolved_count = 0

    for strategy in strategies:
        col = strategy.column
        if col not in new_df.columns:
            continue

        before = int(new_df[col].isna().sum())
        method = strategy.method

        if method == "mean":
            if pd.api.types.is_numeric_dtype(new_df[col]):
                new_df[col] = new_df[col].fillna(new_df[col].mean())
        elif method == "median":
            if pd.api.types.is_numeric_dtype(new_df[col]):
                new_df[col] = new_df[col].fillna(new_df[col].median())
        elif method == "mode":
            mode_val = new_df[col].mode()
            if not mode_val.empty:
                new_df[col] = new_df[col].fillna(mode_val.iloc[0])
        elif method == "forward_fill":
            new_df[col] = new_df[col].ffill()
        elif method == "drop_rows":
            new_df = new_df.dropna(subset=[col]).reset_index(drop=True)
        elif method == "fill":
            fill_val = strategy.fill_value if strategy.fill_value is not None else ""
            new_df[col] = new_df[col].fillna(fill_val)

        after = int(new_df[col].isna().sum()) if col in new_df.columns else 0
        resolved_count += max(0, before - after)

    updated_summary = missing_value_summary(new_df)
    return new_df, resolved_count, updated_summary


# ---------------------------------------------------------------------------
# 5. Format Standardization
# ---------------------------------------------------------------------------

def standardize_formats(
    df: pd.DataFrame,
    columns: list,
) -> tuple[pd.DataFrame, list[str], int, int]:
    """
    Standardize column formats.
    columns: list of FormatColumnRequest-like objects with .column, .type, .casing
    Returns (new_df, modified_columns, converted_value_count, new_missing_count)
    """
    import re
    new_df = df.copy()
    modified_columns = []
    converted_value_count = 0
    new_missing_count = 0

    for req in columns:
        col = req.column
        if col not in new_df.columns:
            continue

        before_missing = int(new_df[col].isna().sum())

        if req.type == "date":
            converted = pd.to_datetime(new_df[col], errors="coerce")
            valid_mask = converted.notna() & new_df[col].notna()
            converted_value_count += int(valid_mask.sum())
            new_df[col] = converted.dt.strftime("%Y-%m-%d").where(converted.notna(), other=np.nan)

        elif req.type == "text":
            mask = new_df[col].notna()
            new_df.loc[mask, col] = new_df.loc[mask, col].astype(str).str.strip()
            casing = getattr(req, "casing", None)
            if casing == "lower":
                new_df.loc[mask, col] = new_df.loc[mask, col].str.lower()
            elif casing == "upper":
                new_df.loc[mask, col] = new_df.loc[mask, col].str.upper()
            elif casing == "title":
                new_df.loc[mask, col] = new_df.loc[mask, col].str.title()
            converted_value_count += int(mask.sum())

        elif req.type == "numeric":
            def clean_numeric(val):
                if pd.isna(val):
                    return np.nan
                s = re.sub(r"[^\d.\-]", "", str(val).replace(",", ""))
                try:
                    return float(s)
                except ValueError:
                    return np.nan

            new_df[col] = new_df[col].apply(clean_numeric)
            after_non_null = new_df[col].notna().sum()
            converted_value_count += int(after_non_null)

        after_missing = int(new_df[col].isna().sum())
        new_missing_count += max(0, after_missing - before_missing)
        modified_columns.append(col)

    return new_df, modified_columns, converted_value_count, new_missing_count


# ---------------------------------------------------------------------------
# 6. Outlier Detection & Removal
# ---------------------------------------------------------------------------

def detect_outliers(df: pd.DataFrame) -> tuple[dict, list[int]]:
    """
    Detect outliers using IQR method on numeric columns.
    Returns (outlier_summary, outlier_row_indices)
    outlier_summary: {col: {"count": int, "lower_bound": float, "upper_bound": float}}
    """
    outlier_summary = {}
    outlier_mask = pd.Series([False] * len(df), index=df.index)

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue
        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        col_outlier_mask = (df[col] < lower) | (df[col] > upper)
        count = int(col_outlier_mask.sum())

        if count > 0:
            outlier_summary[col] = {
                "count": count,
                "lower_bound": lower,
                "upper_bound": upper,
            }
            outlier_mask = outlier_mask | col_outlier_mask

    outlier_row_indices = [int(i) for i in df.index[outlier_mask].tolist()]
    return outlier_summary, outlier_row_indices


def remove_outliers(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Remove all rows containing at least one outlier value.
    Returns (new_df, rows_removed)
    """
    _, outlier_row_indices = detect_outliers(df)
    original_len = len(df)
    new_df = df.drop(index=outlier_row_indices).reset_index(drop=True)
    rows_removed = original_len - len(new_df)
    return new_df, rows_removed
