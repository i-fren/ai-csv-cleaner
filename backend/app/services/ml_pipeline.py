"""
ml_pipeline.py
--------------
Problem type detection and Random Forest model training for the AI CSV Analyzer.
"""
import math
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)
from sklearn.preprocessing import LabelEncoder


def detect_problem_type(
    df: pd.DataFrame,
    target_column: str,
    inferred_types: dict[str, str],
) -> dict:
    """
    Detect whether the target column requires classification or regression.
    Returns DetectProblemTypeResponse-compatible dict.
    """
    if target_column not in df.columns:
        from app.errors import AppError
        raise AppError(400, f"Column '{target_column}' does not exist in the dataset.")

    unique_count = int(df[target_column].nunique())
    col_type = inferred_types.get(target_column, "text")

    if unique_count <= 10 or col_type == "text":
        problem_type = "classification"
        reasoning = (
            f"Target column has {unique_count} unique value(s) "
            f"{'or is of text type ' if col_type == 'text' else ''}"
            "→ classification."
        )
    else:
        problem_type = "regression"
        reasoning = (
            f"Target column has {unique_count} unique numeric values → regression."
        )

    return {
        "target_column": target_column,
        "problem_type": problem_type,
        "unique_value_count": unique_count,
        "reasoning": reasoning,
    }


def _prepare_features(df: pd.DataFrame, target_column: str):
    """Encode categoricals, drop target, impute NaN. Returns (X, y)."""
    data = df.copy()
    y_raw = data[target_column]
    X = data.drop(columns=[target_column])

    # Encode categorical columns
    for col in X.select_dtypes(include=["object", "category"]).columns:
        X[col] = LabelEncoder().fit_transform(X[col].astype(str))

    # Impute remaining NaN with column mean (numeric) or 0
    for col in X.columns:
        if X[col].isna().any():
            if pd.api.types.is_numeric_dtype(X[col]):
                X[col] = X[col].fillna(X[col].mean())
            else:
                X[col] = X[col].fillna(0)

    # Encode target for classification
    if y_raw.dtype == object or str(y_raw.dtype) == "category":
        y = LabelEncoder().fit_transform(y_raw.astype(str))
    else:
        y = y_raw.fillna(y_raw.mean() if pd.api.types.is_numeric_dtype(y_raw) else 0).values

    return X.values, y


def _train_single(X, y, problem_type: str):
    """Train a Random Forest on X, y. Returns (model, X_test, y_test)."""
    n = len(X)
    if n < 5:
        from app.errors import AppError
        raise AppError(400, "Dataset too small for ML training. Need at least 5 rows.")
    test_size = max(1, n - math.floor(0.8 * n))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size / n, random_state=42
    )

    if problem_type == "classification":
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)

    model.fit(X_train, y_train)
    return model, X_test, y_test


def _classification_metrics(model, X_test, y_test) -> dict:
    y_pred = model.predict(X_test)
    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, average="weighted", zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, average="weighted", zero_division=0)),
        "f1": float(f1_score(y_test, y_pred, average="weighted", zero_division=0)),
    }


def _regression_metrics(model, X_test, y_test) -> dict:
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return {
        "rmse": float(np.sqrt(mse)),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "r2": float(r2_score(y_test, y_pred)),
    }


def _determine_better_model(raw_metrics: dict, cleaned_metrics: dict, problem_type: str) -> str:
    """Return 'raw', 'cleaned', or 'tie'."""
    if problem_type == "classification":
        raw_score = raw_metrics["f1"]
        cleaned_score = cleaned_metrics["f1"]
    else:
        # For regression, lower RMSE is better — invert for comparison
        raw_score = -raw_metrics["rmse"]
        cleaned_score = -cleaned_metrics["rmse"]

    if cleaned_score > raw_score:
        return "cleaned"
    elif raw_score > cleaned_score:
        return "raw"
    return "tie"


def train_models(
    raw_df: pd.DataFrame,
    cleaned_df: pd.DataFrame,
    target_column: str,
    problem_type: str,
    openai_client=None,
) -> dict:
    """
    Train Random Forest models on raw and cleaned datasets.
    Returns MLResult-compatible dict.
    """
    # Prepare features
    X_raw, y_raw = _prepare_features(raw_df, target_column)
    X_clean, y_clean = _prepare_features(cleaned_df, target_column)

    # Train models
    raw_model, X_raw_test, y_raw_test = _train_single(X_raw, y_raw, problem_type)
    clean_model, X_clean_test, y_clean_test = _train_single(X_clean, y_clean, problem_type)

    # Compute metrics
    if problem_type == "classification":
        raw_metrics = _classification_metrics(raw_model, X_raw_test, y_raw_test)
        cleaned_metrics = _classification_metrics(clean_model, X_clean_test, y_clean_test)
    else:
        raw_metrics = _regression_metrics(raw_model, X_raw_test, y_raw_test)
        cleaned_metrics = _regression_metrics(clean_model, X_clean_test, y_clean_test)

    better_model = _determine_better_model(raw_metrics, cleaned_metrics, problem_type)

    # Feature importance from cleaned model
    feature_names = [
        c for c in cleaned_df.columns if c != target_column
    ]
    importances = clean_model.feature_importances_
    feature_importance = sorted(
        [
            {"feature": name, "score": float(score)}
            for name, score in zip(feature_names, importances)
        ],
        key=lambda x: x["score"],
        reverse=True,
    )

    # Plain-language explanation
    top3 = feature_importance[:3]
    top3_desc = ", ".join(
        [f"{f['feature']} ({f['score']:.1%})" for f in top3]
    )

    if better_model == "cleaned":
        explanation = (
            "The model trained on the cleaned dataset outperforms the raw dataset model. "
            "Data cleaning reduced noise from duplicates, missing values, and outliers, "
            "leading to better generalization."
        )
    elif better_model == "raw":
        explanation = (
            "The model trained on the raw dataset performed slightly better. "
            "This can happen when cleaning removes rows that contained useful signal."
        )
    else:
        explanation = "Both models performed equally well."

    top_features_description = (
        f"The top predictive features are: {top3_desc}. "
        "These columns have the most influence on the model's predictions."
    )

    return {
        "problem_type": problem_type,
        "raw_model_metrics": raw_metrics,
        "cleaned_model_metrics": cleaned_metrics,
        "better_model": better_model,
        "explanation": explanation,
        "feature_importance": feature_importance,
        "top_features_description": top_features_description,
    }
