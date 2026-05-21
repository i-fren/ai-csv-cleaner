"""
stats_engine.py
---------------
Summary statistics and correlation computation for the AI CSV Analyzer.
"""
import pandas as pd
import numpy as np
from itertools import combinations


def compute_stats(df: pd.DataFrame, inferred_types: dict[str, str]) -> dict:
    """
    Compute per-column summary statistics.
    Returns a dict mapping column name -> NumericColumnStats or TextColumnStats dict.
    """
    result = {}

    for col in df.columns:
        col_type = inferred_types.get(col, "text")
        series = df[col]

        if col_type == "numeric" and pd.api.types.is_numeric_dtype(series):
            non_null = series.dropna()
            result[col] = {
                "type": "numeric",
                "count": int(series.count()),
                "mean": float(non_null.mean()) if len(non_null) > 0 else 0.0,
                "median": float(non_null.median()) if len(non_null) > 0 else 0.0,
                "std": float(non_null.std()) if len(non_null) > 1 else 0.0,
                "min": float(non_null.min()) if len(non_null) > 0 else 0.0,
                "max": float(non_null.max()) if len(non_null) > 0 else 0.0,
                "p25": float(non_null.quantile(0.25)) if len(non_null) > 0 else 0.0,
                "p75": float(non_null.quantile(0.75)) if len(non_null) > 0 else 0.0,
            }
        else:
            # Text / date column
            value_counts = series.value_counts()
            top_val = str(value_counts.index[0]) if len(value_counts) > 0 else ""
            top_freq = int(value_counts.iloc[0]) if len(value_counts) > 0 else 0
            result[col] = {
                "type": "text",
                "count": int(series.count()),
                "unique": int(series.nunique()),
                "top": top_val,
                "top_freq": top_freq,
            }

    return result


def compute_top_correlations(df: pd.DataFrame, top_n: int = 5) -> list[dict]:
    """
    Compute top N column pairs by absolute Pearson correlation.
    Returns list of CorrelationEntry dicts sorted descending by |correlation|.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) < 2:
        return []

    corr_matrix = df[numeric_cols].corr(method="pearson")
    pairs = []

    for col_a, col_b in combinations(numeric_cols, 2):
        val = corr_matrix.loc[col_a, col_b]
        if pd.isna(val):
            continue
        abs_val = abs(float(val))
        direction = "positively" if float(val) > 0 else "negatively"
        strength = (
            "strongly" if abs_val >= 0.7
            else "moderately" if abs_val >= 0.4
            else "weakly"
        )
        pairs.append({
            "col_a": col_a,
            "col_b": col_b,
            "correlation": round(float(val), 4),
            "description": (
                f"{col_a} and {col_b} are {strength} {direction} correlated "
                f"(r = {float(val):.2f})."
            ),
        })

    pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)
    return pairs[:top_n]
