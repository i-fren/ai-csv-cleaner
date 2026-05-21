// TypeScript interfaces mirroring backend Pydantic schemas (app/models/schemas.py)

// --- Upload ---

export interface MissingValueInfo {
  count: number;
  percentage: number;
}

export interface UploadResponse {
  session_id: string;
  filename: string;
  row_count: number;
  column_count: number;
  columns: string[];
  preview: Record<string, unknown>[];
  duplicate_count: number;
  missing_value_summary: Record<string, MissingValueInfo>;
  inferred_types: Record<string, string>;
}

// --- Cleaning: Duplicates ---

export interface DuplicateRemovalResponse {
  rows_removed: number;
  updated_row_count: number;
}

// --- Cleaning: Missing Values ---

export type MissingValueMethod =
  | 'mean'
  | 'median'
  | 'mode'
  | 'forward_fill'
  | 'drop_rows'
  | 'fill';

export interface MissingValueStrategy {
  column: string;
  method: MissingValueMethod;
  fill_value?: string;
}

export interface ApplyMissingValueRequest {
  strategies: MissingValueStrategy[];
}

export interface MissingValueResponse {
  resolved_count: number;
  updated_missing_summary: Record<string, MissingValueInfo>;
}

export interface SuggestFillStrategyResponse {
  column: string;
  suggested_method: MissingValueMethod;
  rationale: string;
}

// --- Cleaning: Format ---

export type FormatType = 'date' | 'numeric' | 'text';
export type TextCasing = 'lower' | 'upper' | 'title';

export interface FormatColumnRequest {
  column: string;
  type: FormatType;
  casing?: TextCasing;
}

export interface ApplyFormatRequest {
  columns: FormatColumnRequest[];
}

export interface FormatResponse {
  modified_columns: string[];
  converted_value_count: number;
  new_missing_count: number;
}

// --- Cleaning: Outliers ---

export interface OutlierColumnInfo {
  count: number;
  lower_bound: number;
  upper_bound: number;
}

export interface OutlierDetectResponse {
  outlier_summary: Record<string, OutlierColumnInfo>;
  outlier_row_indices: number[];
}

export interface OutlierRemoveResponse {
  rows_removed: number;
  updated_row_count: number;
}

// --- Statistics ---

export interface NumericColumnStats {
  type: 'numeric';
  count: number;
  mean: number;
  median: number;
  std: number;
  min: number;
  max: number;
  p25: number;
  p75: number;
}

export interface TextColumnStats {
  type: 'text';
  count: number;
  unique: number;
  top: string;
  top_freq: number;
}

export type ColumnStats = NumericColumnStats | TextColumnStats;

export interface StatsResponse {
  raw: Record<string, ColumnStats>;
  cleaned: Record<string, ColumnStats>;
}

// --- Insights ---

export interface CorrelationEntry {
  col_a: string;
  col_b: string;
  correlation: number;
  description: string;
}

export interface InsightResult {
  summary: string;
  top_correlations: CorrelationEntry[];
  temporal_trends: string | null;
  quality_suggestions: string[];
}

// --- ML ---

export type ProblemType = 'classification' | 'regression';

export interface DetectProblemTypeResponse {
  target_column: string;
  problem_type: ProblemType;
  unique_value_count: number;
  reasoning: string;
}

export interface ClassificationMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
}

export interface RegressionMetrics {
  rmse: number;
  mae: number;
  r2: number;
}

export interface FeatureImportanceEntry {
  feature: string;
  score: number;
}

export interface MLResult {
  problem_type: ProblemType;
  raw_model_metrics: ClassificationMetrics | RegressionMetrics;
  cleaned_model_metrics: ClassificationMetrics | RegressionMetrics;
  better_model: 'raw' | 'cleaned' | 'tie';
  explanation: string;
  feature_importance: FeatureImportanceEntry[];
  top_features_description: string;
}

// --- Error ---

export interface ApiError {
  detail: string;
}
