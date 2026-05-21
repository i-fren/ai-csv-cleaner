# Implementation Plan: AI CSV Analyzer

## Overview

Full-stack implementation of the AI CSV Analyzer using a Python FastAPI backend and a React + TypeScript frontend. Tasks are ordered to build incrementally: project scaffolding → backend data layer → API endpoints (upload, cleaning, stats, insights, ML, export) → frontend infrastructure → UI panels → property-based and unit tests.

All backend code lives in `f:\csv-cleaner-app\backend\`, all frontend code in `f:\csv-cleaner-app\frontend\`.

---

## Tasks

- [x] 1. Project scaffolding
  - [x] 1.1 Scaffold the backend Python project structure
    - Create `backend/` directory with `app/main.py`, `app/config.py`, `app/models/schemas.py`, `app/routers/__init__.py`, `app/services/__init__.py`
    - Create `backend/requirements.txt` pinning: `fastapi`, `uvicorn[standard]`, `pandas`, `scikit-learn`, `openai`, `reportlab`, `python-multipart`, `hypothesis`, `pytest`, `pytest-asyncio`, `httpx`, `pytest-mock`
    - Create `backend/pyproject.toml` (or `setup.cfg`) configuring pytest with `asyncio_mode = auto`
    - Implement `app/main.py`: instantiate `FastAPI`, configure CORS to allow `http://localhost:5173`, register all routers (stubs for now), add `AppError` exception handler returning `{"detail": message}`
    - Implement `app/config.py`: load `OPENAI_API_KEY` and `MAX_FILE_SIZE_MB` (default 50) from environment variables using `os.getenv`
    - _Requirements: 1.1, 1.2, 1.3_

  - [x] 1.2 Scaffold the frontend Vite + React + TypeScript project
    - Run `npm create vite@latest frontend -- --template react-ts` (or create equivalent `package.json`, `vite.config.ts`, `tsconfig.json` manually)
    - Install and pin dependencies: `react`, `react-dom`, `react-plotly.js`, `plotly.js`, `axios`, `tailwindcss`, `postcss`, `autoprefixer`
    - Install and pin dev dependencies: `vitest`, `@vitest/coverage-v8`, `@testing-library/react`, `@testing-library/user-event`, `@testing-library/jest-dom`, `axe-core`, `jest-axe`, `@types/react`, `@types/react-dom`, `@types/plotly.js`
    - Configure Tailwind CSS: create `tailwind.config.js` and `postcss.config.js`, add Tailwind directives to `src/index.css`
    - Configure Vitest in `vite.config.ts`: set `test.environment = 'jsdom'`, `test.setupFiles = ['./src/setupTests.ts']`, `test.globals = true`
    - Create `src/setupTests.ts` importing `@testing-library/jest-dom`
    - Create the full directory skeleton: `src/components/upload/`, `src/components/cleaning/`, `src/components/insights/`, `src/components/comparison/`, `src/components/ml/`, `src/components/shared/`, `src/hooks/`, `src/types/`, `src/api/`
    - _Requirements: 13.1, 13.2, 13.3_


- [x] 2. Backend data models and session store
  - [x] 2.1 Implement Pydantic schemas in `app/models/schemas.py`
    - Define `MissingValueInfo`, `UploadResponse`, `MissingValueStrategy`, `ApplyMissingValueRequest`, `FormatColumnRequest`, `ApplyFormatRequest`
    - Define `NumericColumnStats`, `TextColumnStats`, `CorrelationEntry`, `InsightResult`
    - Define `ClassificationMetrics`, `RegressionMetrics`, `FeatureImportanceEntry`, `MLResult`
    - Define `DetectProblemTypeRequest`, `DetectProblemTypeResponse`, `TrainRequest`
    - Define `DuplicateRemovalResponse`, `MissingValueResponse`, `FormatResponse`, `OutlierDetectResponse`, `OutlierRemoveResponse`
    - Use `Literal` types for `method`, `type`, `casing`, `problem_type`, `better_model` fields
    - _Requirements: 1.5, 2.3, 3.6, 4.5, 5.2, 6.1, 7.2, 9.4, 10.5_

  - [x] 2.2 Implement `Session` dataclass and `SessionStore` in `app/services/session_store.py`
    - Define `Session` dataclass with fields: `session_id: str`, `filename: str`, `raw_df: pd.DataFrame`, `cleaned_df: pd.DataFrame`, `inferred_types: dict[str, str]`, `duplicates_removed: int = 0`, `missing_resolved: int = 0`, `outliers_removed: int = 0`, `columns_standardized: list[str]`, `insights: InsightResult | None = None`, `ml_result: MLResult | None = None`, `created_at: datetime`
    - Implement `SessionStore` class with `create(session) -> None`, `get(session_id) -> Session`, `update(session) -> None` methods using an in-memory `dict`
    - `get()` SHALL raise a 404 `AppError` with message `"Session '{id}' not found or has expired."` when the session does not exist
    - Export a module-level singleton `session_store = SessionStore()`
    - _Requirements: 1.5, 13.7_

  - [ ]* 2.3 Write unit tests for `SessionStore`
    - Test `create` + `get` round-trip returns the same session object
    - Test `get` with unknown ID raises the correct 404 error
    - Test `update` mutates the stored session
    - _Requirements: 13.7_

- [x] 3. Upload endpoint
  - [x] 3.1 Implement type inference and CSV parsing utilities in `app/services/data_cleaner.py`
    - Implement `infer_column_types(df: pd.DataFrame) -> dict[str, str]`: for each column, return `"numeric"` if `pd.api.types.is_numeric_dtype`, `"date"` if parseable as dates via `pd.to_datetime(errors='coerce')` with >50% success rate, else `"text"`
    - Implement `count_duplicates(df: pd.DataFrame) -> int` returning `df.duplicated().sum()`
    - Implement `missing_value_summary(df: pd.DataFrame) -> dict[str, MissingValueInfo]` returning count and `count / len(df) * 100` percentage per column
    - _Requirements: 1.7, 2.1, 3.1_

  - [x] 3.2 Implement `POST /api/v1/upload` in `app/routers/upload.py`
    - Accept `file: UploadFile`; reject non-`.csv` extensions with HTTP 400 `"Only .csv files are accepted."`
    - Read file bytes; reject if size > `config.MAX_FILE_SIZE_MB * 1024 * 1024` with HTTP 413 `"File size exceeds the 50 MB limit."`
    - Parse with `pd.read_csv(io.BytesIO(content))`; catch `pd.errors.ParserError` and return HTTP 400 `"CSV parsing failed: {error}"`
    - Call `infer_column_types`, `count_duplicates`, `missing_value_summary`
    - Create a `Session`, store via `session_store.create()`, return `UploadResponse` with `preview` = first `min(N, 10)` rows as `list[dict]`
    - Register router with prefix `/api/v1` in `main.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

  - [ ]* 3.3 Write property test for upload session correctness (Property 2)
    - **Property 2: Upload creates a session with correct data**
    - **Validates: Requirements 1.5**
    - Use `hypothesis` `data_frames` strategy; POST to `/api/v1/upload` via `httpx.AsyncClient`; assert `row_count == len(df)` and `column_count == len(df.columns)`

  - [ ]* 3.4 Write property test for preview row count (Property 3)
    - **Property 3: Preview shows at most 10 rows**
    - **Validates: Requirements 1.6**
    - For any DataFrame with N rows, assert `len(response["preview"]) == min(N, 10)` and preview rows match the first `min(N, 10)` rows

  - [ ]* 3.5 Write property test for file size limit (Property 4)
    - **Property 4: File size limit is enforced**
    - **Validates: Requirements 1.2**
    - Generate byte sequences > 50 MB; assert HTTP 413 and no session created; generate valid CSVs ≤ 50 MB; assert HTTP 200

  - [ ]* 3.6 Write property test for malformed CSV rejection (Property 5)
    - **Property 5: Malformed CSV produces an error**
    - **Validates: Requirements 1.3**
    - Generate random byte sequences that are not valid CSVs; assert HTTP 400 and no session created

  - [ ]* 3.7 Write property test for non-CSV file rejection (Property 1)
    - **Property 1: Non-CSV files are rejected**
    - **Validates: Requirements 1.1**
    - Generate filenames with extensions other than `.csv`; assert the upload is rejected before any network request (frontend validation) or returns HTTP 400 (backend validation)


- [ ] 4. Data cleaning endpoints
  - [x] 4.1 Implement duplicate removal logic and endpoint
    - In `app/services/data_cleaner.py`, implement `remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]`: call `df.drop_duplicates(keep='first')`, return `(new_df, rows_removed)`
    - In `app/routers/cleaning.py`, implement `POST /api/v1/sessions/{session_id}/clean/duplicates`: fetch session, call `remove_duplicates`, update `session.cleaned_df` and `session.duplicates_removed`, return `DuplicateRemovalResponse`
    - _Requirements: 2.2, 2.3, 2.4_

  - [ ]* 4.2 Write property test for duplicate detection accuracy (Property 6)
    - **Property 6: Duplicate detection is accurate**
    - **Validates: Requirements 2.1, 2.2**
    - Use `hypothesis` `data_frames`; inject known duplicates; assert `count_duplicates(df) == expected_duplicates`

  - [ ]* 4.3 Write property test for duplicate removal correctness (Property 7)
    - **Property 7: Duplicate removal preserves first occurrences and updates row count**
    - **Validates: Requirements 2.3, 2.4**
    - For any DataFrame with R rows and D duplicates: assert cleaned has 0 duplicates, all unique rows present, `rows_removed == D`

  - [-] 4.4 Implement missing value strategies and endpoint
    - In `app/services/data_cleaner.py`, implement `apply_missing_value_strategies(df: pd.DataFrame, strategies: list[MissingValueStrategy]) -> tuple[pd.DataFrame, int, dict]`:
      - `mean`/`median`/`mode`: fill with column statistic
      - `forward_fill`: `df[col].ffill()`
      - `drop_rows`: `df.dropna(subset=[col])`
      - `fill`: `df[col].fillna(fill_value)`
      - Return `(new_df, resolved_count, updated_missing_summary)`
    - In `app/routers/cleaning.py`, implement `POST /api/v1/sessions/{session_id}/clean/missing-values`: validate columns exist (HTTP 400 if not), apply strategies, update session, return `MissingValueResponse`
    - _Requirements: 3.3, 3.4, 3.5, 3.6, 3.7_

  - [ ]* 4.5 Write property test for missing value strategy correctness (Property 9)
    - **Property 9: Missing value strategies reduce missing counts**
    - **Validates: Requirements 3.4, 3.5**
    - For any column with M missing values and any valid fill strategy, assert missing count is 0 after applying; for `drop_rows`, also assert row count decreased correctly

  - [ ]* 4.6 Write property test for missing value count accuracy (Property 8)
    - **Property 8: Missing value counts are accurate**
    - **Validates: Requirements 3.1**
    - For any DataFrame with a known missing value pattern, assert `missing_value_summary` returns exact counts and correct percentages

  - [ ] 4.7 Implement AI fill-strategy suggestion endpoint
    - In `app/services/ai_engine.py`, implement `suggest_fill_strategy(column: str, df: pd.DataFrame, openai_client) -> dict`: build a prompt describing the column's dtype, sample values, and missing count; call `openai_client.chat.completions.create` with `model="gpt-4o-mini"`; parse response to extract `suggested_method` (one of `mean`, `median`, `mode`, `forward_fill`, `drop_rows`) and `rationale`; raise HTTP 502 on API failure
    - In `app/routers/cleaning.py`, implement `POST /api/v1/sessions/{session_id}/clean/missing-values/suggest`: validate column exists, call `suggest_fill_strategy`, return response
    - _Requirements: 3.2, 3.3_

  - [ ]* 4.8 Write property test for AI suggestion validity (Property 10)
    - **Property 10: AI-suggested fill strategy is always a valid strategy**
    - **Validates: Requirements 3.3**
    - Mock the OpenAI client; for any column, assert `suggested_method` is one of the five valid strategies

  - [ ] 4.9 Implement format standardization logic and endpoint
    - In `app/services/data_cleaner.py`, implement `standardize_formats(df: pd.DataFrame, columns: list[FormatColumnRequest]) -> tuple[pd.DataFrame, list[str], int, int]`:
      - `date`: `pd.to_datetime(col, errors='coerce').dt.strftime('%Y-%m-%d')`
      - `text`: strip whitespace + apply `.str.lower()` / `.str.upper()` / `.str.title()` per `casing`
      - `numeric`: strip currency symbols and thousand separators with regex, then `pd.to_numeric(errors='coerce')`
      - Unconvertible values become NaN; count new NaN cells as `new_missing_count`
      - Return `(new_df, modified_columns, converted_value_count, new_missing_count)`
    - In `app/routers/cleaning.py`, implement `POST /api/v1/sessions/{session_id}/clean/format`: validate columns, apply standardization, update session, return `FormatResponse`
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [ ]* 4.10 Write property test for format standardization correctness (Property 11)
    - **Property 11: Format standardization transforms values correctly**
    - **Validates: Requirements 4.3, 4.4, 4.5**
    - For any recognized date string, assert output matches `YYYY-MM-DD`; for text, assert no leading/trailing whitespace and correct casing; for numeric strings with symbols, assert correct numeric value

  - [ ]* 4.11 Write property test for unconvertible values becoming NaN (Property 12)
    - **Property 12: Unconvertible values become missing values**
    - **Validates: Requirements 4.6**
    - For any value that cannot be converted to the requested type, assert the cell is NaN and `new_missing_count` increases by 1

  - [ ] 4.12 Implement outlier detection and removal logic and endpoints
    - In `app/services/data_cleaner.py`, implement `detect_outliers(df: pd.DataFrame) -> dict`: for each numeric column, compute Q1, Q3, IQR; identify values outside `[Q1 − 1.5×IQR, Q3 + 1.5×IQR]`; return `outlier_summary` dict and `outlier_row_indices` list
    - Implement `remove_outliers(df: pd.DataFrame) -> tuple[pd.DataFrame, int]`: drop all rows with at least one outlier value; return `(new_df, rows_removed)`
    - In `app/routers/cleaning.py`, implement `POST /api/v1/sessions/{session_id}/clean/outliers/detect` and `POST /api/v1/sessions/{session_id}/clean/outliers/remove`; update session on removal
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ]* 4.13 Write property test for IQR outlier detection accuracy (Property 13)
    - **Property 13: IQR outlier detection identifies correct values**
    - **Validates: Requirements 5.1, 5.2**
    - For any numeric column, assert detected outliers are exactly the values outside `[Q1 − 1.5×IQR, Q3 + 1.5×IQR]` and bounds match

  - [ ]* 4.14 Write property test for outlier removal completeness (Property 14)
    - **Property 14: Outlier removal eliminates all outlier rows**
    - **Validates: Requirements 5.5**
    - For any DataFrame with known outlier rows, assert no outlier values remain after removal and `rows_removed` equals the count of removed rows

- [ ] 5. Checkpoint — cleaning layer complete
  - Ensure all tests pass, ask the user if questions arise.


- [ ] 6. Stats endpoint
  - [ ] 6.1 Implement summary statistics computation in `app/services/stats_engine.py`
    - Implement `compute_stats(df: pd.DataFrame, inferred_types: dict[str, str]) -> dict`:
      - For numeric columns: compute `count`, `mean`, `median`, `std`, `min`, `max`, `p25`, `p75` using `df[col].describe()` and `df[col].median()`; return as `NumericColumnStats`
      - For text columns: compute `count`, `unique`, `top` (most frequent value), `top_freq`; return as `TextColumnStats`
      - Label each column with its `type`
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ] 6.2 Implement `GET /api/v1/sessions/{session_id}/stats` in `app/routers/stats.py`
    - Fetch session; call `compute_stats` on both `session.raw_df` and `session.cleaned_df`
    - Return `{"raw": {...}, "cleaned": {...}}`
    - Register router in `main.py`
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ]* 6.3 Write property test for numeric statistics correctness (Property 17)
    - **Property 17: Numeric summary statistics are correct**
    - **Validates: Requirements 7.2**
    - For any numeric column, assert `min ≤ p25 ≤ median ≤ p75 ≤ max`, `mean` equals arithmetic mean of non-null values, `std` equals standard deviation of non-null values

- [ ] 7. AI insights endpoint
  - [ ] 7.1 Implement correlation computation in `app/services/stats_engine.py`
    - Implement `compute_top_correlations(df: pd.DataFrame, top_n: int = 5) -> list[dict]`: compute Pearson correlation matrix for numeric columns; extract upper triangle pairs; sort by absolute value descending; return top `top_n` as `list[CorrelationEntry]`
    - _Requirements: 6.2_

  - [ ]* 7.2 Write property test for top correlations ranking (Property 15)
    - **Property 15: Top correlations are correctly ranked**
    - **Validates: Requirements 6.2**
    - For any DataFrame with numeric columns, assert returned top-5 pairs are the 5 highest absolute Pearson correlations in descending order

  - [ ] 7.3 Implement AI insights generation in `app/services/ai_engine.py`
    - Implement `generate_insights(session: Session, openai_client) -> InsightResult`:
      - Build a prompt including dataset shape, column names, inferred types, top correlations, and cleaning audit trail
      - Call `openai_client.chat.completions.create` with `model="gpt-4o-mini"`, requesting structured JSON output with `summary`, `temporal_trends`, and `quality_suggestions` (≥ 3 entries)
      - Merge computed `top_correlations` from `compute_top_correlations` into the result
      - Raise HTTP 502 with `"AI service is temporarily unavailable. Please try again."` on API failure
    - _Requirements: 6.1, 6.3, 6.4, 6.5_

  - [ ] 7.4 Implement `POST /api/v1/sessions/{session_id}/insights` in `app/routers/insights.py`
    - Fetch session; call `generate_insights`; store result in `session.insights`; return `InsightResult`
    - Register router in `main.py`
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ]* 7.5 Write property test for quality suggestions count (Property 16)
    - **Property 16: At least 3 quality suggestions are always returned**
    - **Validates: Requirements 6.4**
    - Mock the OpenAI client to return varied responses; assert `len(quality_suggestions) >= 3` for any dataset

- [ ] 8. ML pipeline endpoints
  - [ ] 8.1 Implement problem type detection in `app/services/ml_pipeline.py`
    - Implement `detect_problem_type(df: pd.DataFrame, target_column: str, inferred_types: dict[str, str]) -> dict`:
      - Raise HTTP 400 if `target_column` not in `df.columns`
      - Count unique values; return `"classification"` if `unique_count <= 10` or `inferred_types[target_column] == "text"`, else `"regression"`
      - Return `DetectProblemTypeResponse` with `target_column`, `problem_type`, `unique_value_count`, `reasoning`
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [ ] 8.2 Implement `POST /api/v1/sessions/{session_id}/ml/detect-problem-type` in `app/routers/ml.py`
    - Fetch session; call `detect_problem_type` on `session.cleaned_df`; return response
    - Register router in `main.py`
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [ ]* 8.3 Write property test for problem type detection rules (Property 18)
    - **Property 18: Problem type detection follows the specified rules**
    - **Validates: Requirements 9.2, 9.3, 9.4**
    - For any target column: assert `classification` when `unique_count <= 10` or type is text; assert `regression` when `unique_count > 10` and type is numeric

  - [ ] 8.4 Implement Random Forest training in `app/services/ml_pipeline.py`
    - Implement `train_models(raw_df: pd.DataFrame, cleaned_df: pd.DataFrame, target_column: str, problem_type: str, openai_client) -> MLResult`:
      - For each DataFrame: encode categoricals with `pd.get_dummies`, impute remaining NaN with column mean/mode, split 80/20 with `train_test_split(test_size=0.2, random_state=42)`
      - Train `RandomForestClassifier` or `RandomForestRegressor` (100 estimators, `random_state=42`)
      - Compute classification metrics: `accuracy_score`, `precision_score(average='weighted')`, `recall_score(average='weighted')`, `f1_score(average='weighted')`
      - Compute regression metrics: `mean_squared_error(squared=False)` (RMSE), `mean_absolute_error`, `r2_score`
      - Extract `feature_importances_` from the cleaned model; sort descending; return as `list[FeatureImportanceEntry]`
      - Determine `better_model` per the comparison rules (higher is better for accuracy/precision/recall/f1/r2; lower for rmse/mae)
      - Call OpenAI to generate `explanation` and `top_features_description`
    - _Requirements: 10.1, 10.2, 10.3, 10.5, 10.6, 11.1, 11.2, 11.4_

  - [ ] 8.5 Implement `POST /api/v1/sessions/{session_id}/ml/train` in `app/routers/ml.py`
    - Fetch session; call `train_models`; store result in `session.ml_result`; return `MLResult`
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8_

  - [ ]* 8.6 Write property test for train/test split correctness (Property 19)
    - **Property 19: Train/test split is 80/20**
    - **Validates: Requirements 10.1**
    - For any dataset with N rows, assert training set has `floor(0.8 × N)` rows, test set has remaining rows, no overlap

  - [ ]* 8.7 Write property test for classification metrics validity (Property 20)
    - **Property 20: Classification metrics are valid probabilities**
    - **Validates: Requirements 10.2**
    - For any classification training run, assert all four metrics (accuracy, precision, recall, F1) are in `[0.0, 1.0]`

  - [ ]* 8.8 Write property test for regression metrics validity (Property 21)
    - **Property 21: Regression metrics satisfy validity constraints**
    - **Validates: Requirements 10.3**
    - For any regression training run, assert `rmse >= 0`, `mae >= 0`, `r2 <= 1.0`

  - [ ]* 8.9 Write property test for better model highlighting consistency (Property 22)
    - **Property 22: Better model highlighting is consistent**
    - **Validates: Requirements 10.6**
    - For any pair of metric results, assert `better_model` selects higher value for accuracy/precision/recall/f1/r2 and lower value for rmse/mae

  - [ ]* 8.10 Write property test for feature importance sum (Property 23)
    - **Property 23: Feature importance scores sum to approximately 1**
    - **Validates: Requirements 11.1**
    - For any trained Random Forest model, assert `abs(sum(scores) - 1.0) < 0.001`

  - [ ]* 8.11 Write property test for feature importance sort order (Property 24)
    - **Property 24: Feature importance scores are sorted descending**
    - **Validates: Requirements 11.2**
    - For any feature importance result, assert each score is ≤ the previous score

- [ ] 9. Export endpoints
  - [ ] 9.1 Implement CSV export in `app/routers/export.py`
    - Implement `GET /api/v1/sessions/{session_id}/export/csv`: fetch session; serialize `session.cleaned_df` to CSV bytes via `df.to_csv(index=False)`; return `StreamingResponse` with `media_type="text/csv"` and `Content-Disposition: attachment; filename="cleaned_{session.filename}"`
    - Register router in `main.py`
    - _Requirements: 12.1, 12.2, 12.5_

  - [ ]* 9.2 Write property test for CSV export round-trip (Property 26)
    - **Property 26: CSV export is a round-trip**
    - **Validates: Requirements 12.2**
    - For any cleaned DataFrame, serialize to CSV and re-parse; assert same shape, column names, and values within floating-point tolerance

  - [ ]* 9.3 Write property test for export filename patterns (Property 27)
    - **Property 27: Export filenames follow the specified patterns**
    - **Validates: Requirements 12.2, 12.5**
    - For any original filename F, assert CSV download filename is `cleaned_F` and PDF filename is `insights_report_F`

  - [ ] 9.4 Implement PDF report generation in `app/services/pdf_generator.py`
    - Implement `generate_pdf(session: Session) -> bytes` using ReportLab:
      - Include title, generation timestamp, and original filename
      - Section 1: Summary statistics table (column name, type, key stats)
      - Section 2: AI insights (summary text, top correlations table, quality suggestions list)
      - Section 3: Data quality metrics (rows removed, duplicates, missing values, outliers)
      - Section 4: ML model comparison table (raw vs cleaned metrics side by side) — skip if `session.ml_result` is None
      - Return PDF as `bytes`; raise HTTP 500 with `"Failed to generate the insights report."` on failure
    - _Requirements: 12.3, 12.4, 12.6_

  - [ ] 9.5 Implement `GET /api/v1/sessions/{session_id}/export/report` in `app/routers/export.py`
    - Fetch session; call `generate_pdf`; return `StreamingResponse` with `media_type="application/pdf"` and `Content-Disposition: attachment; filename="insights_report_{session.filename}"`
    - Return HTTP 404 if session not found; HTTP 500 on PDF generation failure
    - _Requirements: 12.3, 12.4, 12.5, 12.6_

- [ ] 10. Checkpoint — backend API complete
  - Ensure all backend tests pass, ask the user if questions arise.


- [x] 11. Frontend shared infrastructure
  - [x] 11.1 Define TypeScript API types in `src/types/api.ts`
    - Define interfaces mirroring all Pydantic schemas: `UploadResponse`, `MissingValueInfo`, `MissingValueStrategy`, `ApplyMissingValueRequest`, `FormatColumnRequest`, `ApplyFormatRequest`
    - Define `NumericColumnStats`, `TextColumnStats`, `ColumnStats` (union), `StatsResponse`
    - Define `CorrelationEntry`, `InsightResult`, `ClassificationMetrics`, `RegressionMetrics`, `FeatureImportanceEntry`, `MLResult`
    - Define `DetectProblemTypeResponse`, `DuplicateRemovalResponse`, `MissingValueResponse`, `FormatResponse`, `OutlierDetectResponse`, `OutlierRemoveResponse`
    - Define `ApiError` interface `{ detail: string }`
    - _Requirements: 1.5, 2.3, 3.6, 4.5, 5.2, 6.1, 7.2, 9.4, 10.5_

  - [x] 11.2 Implement `src/api/client.ts` with all API call functions
    - Create `axios` instance with `baseURL = 'http://localhost:8000/api/v1'` and `timeout = 35000`
    - Implement typed functions for every endpoint:
      - `uploadCsv(file: File): Promise<UploadResponse>`
      - `removeDuplicates(sessionId: string): Promise<DuplicateRemovalResponse>`
      - `applyMissingValueStrategies(sessionId: string, req: ApplyMissingValueRequest): Promise<MissingValueResponse>`
      - `suggestFillStrategy(sessionId: string, column: string): Promise<{column: string; suggested_method: string; rationale: string}>`
      - `applyFormat(sessionId: string, req: ApplyFormatRequest): Promise<FormatResponse>`
      - `detectOutliers(sessionId: string): Promise<OutlierDetectResponse>`
      - `removeOutliers(sessionId: string): Promise<OutlierRemoveResponse>`
      - `getStats(sessionId: string): Promise<StatsResponse>`
      - `generateInsights(sessionId: string): Promise<InsightResult>`
      - `detectProblemType(sessionId: string, targetColumn: string): Promise<DetectProblemTypeResponse>`
      - `trainModels(sessionId: string, targetColumn: string, problemType: string): Promise<MLResult>`
      - `exportCsvUrl(sessionId: string): string`
      - `exportReportUrl(sessionId: string): string`
    - _Requirements: 1.1, 2.2, 3.3, 4.1, 5.1, 6.1, 7.1, 9.1, 10.2_

  - [x] 11.3 Implement `src/hooks/useApi.ts` and `src/hooks/useSession.ts`
    - `useApi<T>`: generic hook wrapping an async API call; manages `data: T | null`, `loading: boolean`, `error: string | null` state; sets `loading = true` before call, `false` after; extracts `error.response.data.detail` on failure
    - `useSession`: manages `sessionId: string | null` in React state; exposes `setSessionId`, `clearSession`
    - _Requirements: 13.2, 13.3_

  - [x] 11.4 Implement shared UI components
    - `src/components/shared/LoadingSpinner.tsx`: animated spinner with `aria-label="Loading"` and `role="status"`; visible when `loading` prop is `true`
    - `src/components/shared/ErrorBanner.tsx`: dismissible banner with `role="alert"` and `aria-label="Error message"`; renders `message` prop; calls `onDismiss` callback on close button click
    - `src/components/shared/DownloadButton.tsx`: anchor tag styled as button; accepts `href`, `filename`, `label`, `aria-label` props; renders only when `href` is non-null
    - _Requirements: 13.2, 13.3, 13.6_

  - [ ]* 11.5 Write unit tests for shared hooks and components
    - Test `useApi` sets `loading = true` during call and `false` after; sets `error` on failure
    - Test `ErrorBanner` renders message and calls `onDismiss` on button click
    - Test `LoadingSpinner` renders with correct `aria-label`
    - Test `DownloadButton` renders only when `href` is non-null
    - _Requirements: 13.2, 13.3, 13.6_

- [ ] 12. Upload UI
  - [-] 12.1 Implement `src/components/upload/UploadZone.tsx`
    - Render a drag-and-drop zone using HTML5 drag events (`onDragOver`, `onDrop`) and a hidden `<input type="file" accept=".csv">`
    - Validate `.csv` extension client-side before calling `uploadCsv`; display `ErrorBanner` for non-CSV files without making a network request
    - Show `LoadingSpinner` while upload is in progress
    - On success, call `onUploadSuccess(response: UploadResponse)` callback prop
    - All interactive elements (drop zone div, file input label, submit button) MUST have `aria-label` attributes
    - _Requirements: 1.1, 1.2, 13.2, 13.3, 13.6_

  - [ ] 12.2 Implement `src/components/upload/DataPreviewTable.tsx`
    - Accept `preview: Record<string, unknown>[]` and `columns: string[]` props
    - Render an HTML `<table>` with `<thead>` column headers and `<tbody>` data rows
    - Apply Tailwind CSS for responsive horizontal scroll on small viewports
    - Table MUST have `aria-label="Data preview"` and column headers MUST use `<th scope="col">`
    - _Requirements: 1.6, 13.1, 13.6_

  - [ ]* 12.3 Write unit tests for upload components
    - Test `UploadZone` rejects non-CSV files without calling `uploadCsv`
    - Test `UploadZone` shows `LoadingSpinner` during upload
    - Test `DataPreviewTable` renders correct number of rows and columns
    - Run axe-core accessibility check on both components
    - _Requirements: 1.1, 1.6, 13.6_

- [ ] 13. Cleaning UI
  - [ ] 13.1 Implement `src/components/cleaning/DuplicateCard.tsx`
    - Display `duplicate_count` from upload response
    - Render a "Remove Duplicates" button with `aria-label="Remove duplicate rows"`
    - On click, call `removeDuplicates` via `useApi`; show `LoadingSpinner` during call; show updated row count on success
    - _Requirements: 2.1, 2.2, 13.2, 13.6_

  - [ ] 13.2 Implement `src/components/cleaning/MissingValueCard.tsx`
    - Display per-column missing value counts and percentages from `missing_value_summary`
    - For each column, render a strategy selector (`<select>`) with options: `mean`, `median`, `mode`, `forward_fill`, `drop_rows`, `fill`; selector MUST have `aria-label="Fill strategy for {column}"`
    - Render a "Suggest" button per column with `aria-label="Suggest fill strategy for {column}"`; on click, call `suggestFillStrategy` and pre-select the returned strategy
    - Render an "Apply" button with `aria-label="Apply missing value strategies"`; on click, call `applyMissingValueStrategies`
    - Show `LoadingSpinner` during API calls; show `ErrorBanner` on failure
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 13.2, 13.3, 13.6_

  - [ ] 13.3 Implement `src/components/cleaning/FormatCard.tsx`
    - For each column, display inferred type and render a type selector (`date`, `numeric`, `text`) with `aria-label="Format type for {column}"`
    - For text columns, render a casing selector (`lower`, `upper`, `title`) with `aria-label="Text casing for {column}"`
    - Render an "Apply Format" button with `aria-label="Apply format standardization"`; on click, call `applyFormat`
    - Show `LoadingSpinner` during call; show `ErrorBanner` on failure
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 13.2, 13.3, 13.6_

  - [ ] 13.4 Implement `src/components/cleaning/OutlierCard.tsx`
    - Render a "Detect Outliers" button with `aria-label="Detect outliers"`; on click, call `detectOutliers`; display `outlier_summary` table showing count, lower bound, upper bound per column
    - Render a "Remove Outliers" button with `aria-label="Remove outlier rows"`; on click, call `removeOutliers`; display updated row count
    - Show `LoadingSpinner` during calls; show `ErrorBanner` on failure
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 13.2, 13.3, 13.6_

  - [ ] 13.5 Implement `src/components/cleaning/CleaningPanel.tsx`
    - Orchestrate `DuplicateCard`, `MissingValueCard`, `FormatCard`, `OutlierCard` in a vertical layout
    - Accept `sessionId`, `uploadResponse`, and `onCleaningUpdate` callback props
    - Pass appropriate props and callbacks to each card
    - Apply Tailwind CSS responsive layout (single column on mobile, two columns on ≥ 1024px)
    - _Requirements: 2.1, 3.1, 4.1, 5.1, 13.1_

  - [ ]* 13.6 Write unit tests for cleaning components
    - Test `DuplicateCard` calls `removeDuplicates` on button click and shows updated count
    - Test `MissingValueCard` pre-selects suggested strategy after "Suggest" click
    - Test `OutlierCard` shows outlier summary after detection
    - Run axe-core accessibility check on `CleaningPanel`
    - _Requirements: 2.2, 3.2, 5.1, 13.6_

- [ ] 14. Insights UI
  - [ ] 14.1 Implement `src/components/insights/SummaryStatsTable.tsx`
    - Accept `stats: StatsResponse` prop
    - Render two tabs ("Raw" / "Cleaned") with `role="tab"` and `aria-selected`; each tab shows a table of column statistics
    - For numeric columns: display count, mean, median, std, min, max, p25, p75
    - For text columns: display count, unique, top, top_freq
    - Table MUST have `aria-label="Summary statistics"` and `<th scope="col">` headers
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 13.6_

  - [ ] 14.2 Implement `src/components/insights/InsightsPanel.tsx`
    - Render a "Generate Insights" button with `aria-label="Generate AI insights"`; on click, call `generateInsights` via `useApi`
    - Show `LoadingSpinner` during the call (may take up to 30 seconds)
    - On success, display: `summary` text, `top_correlations` table (col_a, col_b, correlation, description), `temporal_trends` text (if non-null), `quality_suggestions` as a bulleted list
    - Show `ErrorBanner` on failure
    - Fetch and display `SummaryStatsTable` by calling `getStats` when the panel mounts
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 13.2, 13.3, 13.6_

  - [ ]* 14.3 Write unit tests for insights components
    - Test `InsightsPanel` shows `LoadingSpinner` while `generateInsights` is pending
    - Test `InsightsPanel` renders correlations table and suggestions list on success
    - Test `SummaryStatsTable` renders numeric and text column stats correctly
    - Run axe-core accessibility check on `InsightsPanel`
    - _Requirements: 6.1, 7.2, 13.6_

- [ ] 15. Comparison UI
  - [ ] 15.1 Implement `src/components/comparison/MetricsSummary.tsx`
    - Accept `rawRowCount`, `cleanedRowCount`, `duplicatesRemoved`, `missingResolved`, `outliersRemoved`, `columnsStandardized` props
    - Render a summary card grid showing each metric with a label and value
    - Each metric card MUST have `aria-label` describing the metric
    - _Requirements: 8.1, 8.2, 8.4, 13.6_

  - [ ] 15.2 Implement `src/components/comparison/ComparisonCharts.tsx`
    - Render a Plotly bar chart comparing raw vs cleaned row counts, duplicate counts, and missing value counts
    - Render a Plotly pie chart showing the proportion of rows removed vs retained
    - Each `<Plot>` component MUST have `aria-label` describing the chart content
    - Use `react-plotly.js` `Plot` component with `config={{ responsive: true }}`
    - _Requirements: 8.3, 13.1, 13.6_

  - [ ] 15.3 Implement `src/components/comparison/ComparisonPanel.tsx`
    - Orchestrate `MetricsSummary` and `ComparisonCharts` in a responsive layout
    - Source raw metrics from the original `UploadResponse` and cleaned metrics from cumulative cleaning operation results
    - Apply Tailwind CSS responsive layout
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 13.1_

  - [ ]* 15.4 Write unit tests for comparison components
    - Test `MetricsSummary` renders all six metric values correctly
    - Test `ComparisonCharts` renders without errors given valid data
    - Run axe-core accessibility check on `ComparisonPanel`
    - _Requirements: 8.2, 8.3, 13.6_

- [ ] 16. ML UI
  - [ ] 16.1 Implement `src/components/ml/TargetColumnSelector.tsx`
    - Accept `columns: string[]` and `onSelect: (column: string) => void` props
    - Render a `<select>` dropdown with `aria-label="Select target column for ML"`
    - On change, call `detectProblemType` via `useApi` and pass result to `onSelect`
    - Show `LoadingSpinner` during detection; show `ErrorBanner` on failure
    - _Requirements: 9.1, 9.4, 13.2, 13.6_

  - [ ] 16.2 Implement `src/components/ml/ProblemTypeDisplay.tsx`
    - Accept `response: DetectProblemTypeResponse` prop
    - Display `problem_type` (Classification / Regression), `unique_value_count`, and `reasoning`
    - Render a "Train Models" button with `aria-label="Train ML models"`
    - _Requirements: 9.2, 9.3, 9.4, 13.6_

  - [ ] 16.3 Implement `src/components/ml/ModelMetricsTable.tsx`
    - Accept `result: MLResult` prop
    - Render a side-by-side table of raw vs cleaned model metrics
    - Highlight the better value in each row using a Tailwind CSS green background; the highlighted cell MUST have `aria-label="Better performing model"`
    - For classification: show accuracy, precision, recall, F1; for regression: show RMSE, MAE, R²
    - _Requirements: 10.2, 10.3, 10.6, 13.6_

  - [ ] 16.4 Implement `src/components/ml/FeatureImportanceChart.tsx`
    - Accept `featureImportance: FeatureImportanceEntry[]` prop
    - Display exactly `min(featureImportance.length, 10)` features (highest scores)
    - Render a horizontal Plotly bar chart with features on Y-axis and importance scores on X-axis
    - Chart MUST have `aria-label="Feature importance chart"` and `config={{ responsive: true }}`
    - _Requirements: 11.1, 11.2, 11.3, 13.1, 13.6_

  - [ ] 16.5 Implement `src/components/ml/MLPanel.tsx`
    - Orchestrate `TargetColumnSelector`, `ProblemTypeDisplay`, `ModelMetricsTable`, `FeatureImportanceChart`
    - Manage local state: `targetColumn`, `problemTypeResponse`, `mlResult`
    - On "Train Models" click, call `trainModels` via `useApi`; show `LoadingSpinner` during training
    - Display `top_features_description` and `explanation` text below the metrics table
    - Show `ErrorBanner` on failure
    - _Requirements: 9.1, 10.1, 10.5, 11.1, 11.3, 13.2, 13.3_

  - [ ]* 16.6 Write unit tests for ML components
    - Test `TargetColumnSelector` calls `detectProblemType` on column change
    - Test `ModelMetricsTable` highlights the correct better-performing metric cells
    - Test `FeatureImportanceChart` renders exactly `min(F, 10)` features
    - Run axe-core accessibility check on `MLPanel`
    - _Requirements: 9.4, 10.6, 11.3, 13.6_

  - [ ]* 16.7 Write property test for feature importance chart display (Property 25)
    - **Property 25: Feature importance chart shows top features**
    - **Validates: Requirements 11.3**
    - For any feature importance list with F features, assert the chart renders exactly `min(F, 10)` features with the highest scores

- [ ] 17. Export UI
  - [ ] 17.1 Implement export download buttons in `src/components/shared/DownloadButton.tsx` and wire into `App.tsx`
    - Render a "Download Cleaned CSV" `DownloadButton` with `href={exportCsvUrl(sessionId)}`, `filename="cleaned_data.csv"`, `aria-label="Download cleaned CSV file"`
    - Render a "Download PDF Report" `DownloadButton` with `href={exportReportUrl(sessionId)}`, `filename="insights_report.pdf"`, `aria-label="Download PDF insights report"`
    - Both buttons MUST only render when `sessionId` is non-null
    - _Requirements: 12.1, 12.3, 13.6_

  - [ ]* 17.2 Write unit tests for export buttons
    - Test CSV download button renders with correct `href` and `aria-label`
    - Test PDF download button renders with correct `href` and `aria-label`
    - Test both buttons do not render when `sessionId` is null
    - Run axe-core accessibility check
    - _Requirements: 12.1, 12.3, 13.6_

- [ ] 18. Wire up `App.tsx` and responsive layout
  - [ ] 18.1 Implement `src/App.tsx` as the root component
    - Manage top-level state: `sessionId`, `uploadResponse`, `cleaningState` (cumulative cleaning results), `activePanel: 'upload' | 'cleaning' | 'insights' | 'comparison' | 'ml' | 'export'`
    - Render a top navigation bar with panel tabs; each tab MUST have `aria-label` and `role="tab"`
    - Conditionally render the active panel component; pass `sessionId` and relevant state as props
    - Apply Tailwind CSS responsive layout: full-width single column on mobile, sidebar + content on ≥ 1024px
    - Apply CSS transitions (200ms–400ms) on panel switches using Tailwind `transition` and `duration-300`
    - _Requirements: 13.1, 13.4_

  - [ ]* 18.2 Write unit tests for `App.tsx`
    - Test navigation tabs switch the active panel
    - Test `UploadZone` is shown initially and `CleaningPanel` appears after successful upload
    - Run axe-core accessibility check on the full app layout
    - _Requirements: 13.1, 13.4, 13.6_

- [ ] 19. Backend property-based tests (Hypothesis)
  - [ ] 19.1 Create `backend/tests/test_properties.py` and write all 29 property tests
    - Import `hypothesis`, `hypothesis.strategies`, `hypothesis.extra.pandas`; configure `@settings(max_examples=100)`
    - Tag each test with `# Feature: ai-csv-analyzer, Property {N}: {property_text}`
    - Implement property tests for Properties 1–29 as sub-tasks below (each test is a separate `@given`-decorated function)
    - Properties already covered as sub-tasks in earlier groups (3.3–3.7, 4.2–4.3, 4.5–4.6, 4.8, 4.10–4.11, 4.13–4.14, 6.3, 7.2, 7.5, 8.3, 8.6–8.11, 9.2) should be consolidated here
    - _Requirements: all_

  - [ ]* 19.2 Write property test for loading indicator timing (Property 28)
    - **Property 28: Loading indicator appears for slow operations**
    - **Validates: Requirements 13.2**
    - Mock API calls with a 600ms delay; assert `loading` state is `true` before response and `false` after

  - [ ]* 19.3 Write property test for aria-labels on interactive elements (Property 29)
    - **Property 29: All interactive elements have aria-labels**
    - **Validates: Requirements 13.6**
    - Use axe-core to scan each rendered component; assert no violations for `aria-label` rules on buttons, inputs, selects, and charts

- [ ] 20. Final checkpoint — all tests pass
  - Ensure all backend pytest + Hypothesis tests pass, all frontend Vitest tests pass, ask the user if questions arise.


---

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- Checkpoints at tasks 5, 10, and 20 ensure incremental validation
- Property tests validate all 29 correctness properties from the design document
- Unit tests validate specific examples, edge cases, and UI rendering
- All backend code goes in `f:\csv-cleaner-app\backend\`, all frontend code in `f:\csv-cleaner-app\frontend\`
- The OpenAI API key must be set in the `OPENAI_API_KEY` environment variable before running the backend
- Use `uvicorn app.main:app --reload` to start the backend dev server (port 8000)
- Use `npm run dev` to start the frontend dev server (port 5173)

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1", "2.2"] },
    { "id": 2, "tasks": ["2.3", "3.1", "11.1"] },
    { "id": 3, "tasks": ["3.2", "11.2", "11.3", "11.4"] },
    { "id": 4, "tasks": ["3.3", "3.4", "3.5", "3.6", "3.7", "11.5", "4.1"] },
    { "id": 5, "tasks": ["4.2", "4.3", "4.4", "12.1"] },
    { "id": 6, "tasks": ["4.5", "4.6", "4.7", "12.2"] },
    { "id": 7, "tasks": ["4.8", "4.9", "12.3"] },
    { "id": 8, "tasks": ["4.10", "4.11", "4.12"] },
    { "id": 9, "tasks": ["4.13", "4.14", "6.1"] },
    { "id": 10, "tasks": ["6.2", "13.1", "13.2", "13.3", "13.4"] },
    { "id": 11, "tasks": ["6.3", "7.1", "13.5"] },
    { "id": 12, "tasks": ["7.2", "7.3", "13.6"] },
    { "id": 13, "tasks": ["7.4", "7.5", "8.1", "14.1"] },
    { "id": 14, "tasks": ["8.2", "14.2"] },
    { "id": 15, "tasks": ["8.3", "8.4", "14.3"] },
    { "id": 16, "tasks": ["8.5", "15.1", "15.2"] },
    { "id": 17, "tasks": ["8.6", "8.7", "8.8", "8.9", "8.10", "8.11", "15.3"] },
    { "id": 18, "tasks": ["9.1", "15.4", "16.1", "16.2", "16.3", "16.4"] },
    { "id": 19, "tasks": ["9.2", "9.3", "9.4", "16.5"] },
    { "id": 20, "tasks": ["9.5", "16.6", "16.7"] },
    { "id": 21, "tasks": ["17.1"] },
    { "id": 22, "tasks": ["17.2", "18.1"] },
    { "id": 23, "tasks": ["18.2", "19.1"] },
    { "id": 24, "tasks": ["19.2", "19.3"] }
  ]
}
```
