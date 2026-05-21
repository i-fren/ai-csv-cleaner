from pydantic import BaseModel
from typing import Literal, Any


# --- Upload ---
class MissingValueInfo(BaseModel):
    count: int
    percentage: float


class UploadResponse(BaseModel):
    session_id: str
    filename: str
    row_count: int
    column_count: int
    columns: list[str]
    preview: list[dict[str, Any]]
    duplicate_count: int
    missing_value_summary: dict[str, MissingValueInfo]
    inferred_types: dict[str, str]


# --- Cleaning: Duplicates ---
class DuplicateRemovalResponse(BaseModel):
    rows_removed: int
    updated_row_count: int


# --- Cleaning: Missing Values ---
class MissingValueStrategy(BaseModel):
    column: str
    method: Literal["mean", "median", "mode", "forward_fill", "drop_rows", "fill"]
    fill_value: str | None = None


class ApplyMissingValueRequest(BaseModel):
    strategies: list[MissingValueStrategy]


class MissingValueResponse(BaseModel):
    resolved_count: int
    updated_missing_summary: dict[str, MissingValueInfo]


class SuggestFillStrategyRequest(BaseModel):
    column: str


class SuggestFillStrategyResponse(BaseModel):
    column: str
    suggested_method: Literal["mean", "median", "mode", "forward_fill", "drop_rows"]
    rationale: str


# --- Cleaning: Format ---
class FormatColumnRequest(BaseModel):
    column: str
    type: Literal["date", "numeric", "text"]
    casing: Literal["lower", "upper", "title"] | None = None


class ApplyFormatRequest(BaseModel):
    columns: list[FormatColumnRequest]


class FormatResponse(BaseModel):
    modified_columns: list[str]
    converted_value_count: int
    new_missing_count: int


# --- Cleaning: Outliers ---
class OutlierColumnInfo(BaseModel):
    count: int
    lower_bound: float
    upper_bound: float


class OutlierDetectResponse(BaseModel):
    outlier_summary: dict[str, OutlierColumnInfo]
    outlier_row_indices: list[int]


class OutlierRemoveResponse(BaseModel):
    rows_removed: int
    updated_row_count: int


# --- Statistics ---
class NumericColumnStats(BaseModel):
    type: Literal["numeric"]
    count: int
    mean: float
    median: float
    std: float
    min: float
    max: float
    p25: float
    p75: float


class TextColumnStats(BaseModel):
    type: Literal["text"]
    count: int
    unique: int
    top: str
    top_freq: int


class StatsResponse(BaseModel):
    raw: dict[str, Any]
    cleaned: dict[str, Any]


# --- Insights ---
class CorrelationEntry(BaseModel):
    col_a: str
    col_b: str
    correlation: float
    description: str


class InsightResult(BaseModel):
    summary: str
    top_correlations: list[CorrelationEntry]
    temporal_trends: str | None = None
    quality_suggestions: list[str]


# --- ML ---
class DetectProblemTypeRequest(BaseModel):
    target_column: str


class DetectProblemTypeResponse(BaseModel):
    target_column: str
    problem_type: Literal["classification", "regression"]
    unique_value_count: int
    reasoning: str


class TrainRequest(BaseModel):
    target_column: str
    problem_type: Literal["classification", "regression"]


class ClassificationMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1: float


class RegressionMetrics(BaseModel):
    rmse: float
    mae: float
    r2: float


class FeatureImportanceEntry(BaseModel):
    feature: str
    score: float


class MLResult(BaseModel):
    problem_type: Literal["classification", "regression"]
    raw_model_metrics: ClassificationMetrics | RegressionMetrics
    cleaned_model_metrics: ClassificationMetrics | RegressionMetrics
    better_model: Literal["raw", "cleaned", "tie"]
    explanation: str
    feature_importance: list[FeatureImportanceEntry]
    top_features_description: str
