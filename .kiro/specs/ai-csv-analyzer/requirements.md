# Requirements Document

## Introduction

The AI CSV Analyzer is a full-stack web application that enables users to upload CSV files and receive automated data cleaning, statistical analysis, AI-generated insights, and machine learning model comparisons through a browser-based dashboard. The system consists of a React + TypeScript frontend SPA and a Python FastAPI backend. Sessions are stored in-memory on the server, keyed by a UUID session identifier returned at upload time.

This document derives requirements from the approved design document and covers all thirteen functional areas: CSV upload, duplicate removal, missing value handling, format standardization, outlier detection, AI insights, summary statistics, before/after comparison, ML problem type detection, ML training and comparison, feature importance, download/export, and responsive/accessible UI.

## Glossary

- **System**: The AI CSV Analyzer application (frontend + backend together)
- **Backend**: The Python FastAPI server
- **Frontend**: The React + TypeScript single-page application
- **Session**: A server-side record keyed by a UUID that holds the raw dataset, the evolving cleaned dataset, and all derived results
- **Raw_Dataset**: The immutable original DataFrame stored at upload time
- **Cleaned_Dataset**: The mutable copy of the raw dataset that accumulates cleaning operations
- **Upload_Handler**: The backend component that processes file uploads and creates sessions
- **Session_Store**: The in-memory dictionary that holds all active sessions
- **Data_Cleaner**: The backend service responsible for duplicate removal, missing value handling, format standardization, and outlier detection
- **Stats_Engine**: The backend service that computes summary statistics
- **AI_Engine**: The backend service that calls the OpenAI API to generate insights and fill-strategy suggestions
- **ML_Pipeline**: The backend service that detects problem type and trains Random Forest models
- **PDF_Generator**: The backend service that assembles the insights report PDF
- **IQR**: Interquartile Range — the difference between the 75th percentile (Q3) and 25th percentile (Q1) of a numeric column
- **EARS**: Easy Approach to Requirements Syntax — the pattern language used for all acceptance criteria in this document

---

## Requirements

### Requirement 1: CSV File Upload

**User Story:** As a data analyst, I want to upload a CSV file through the browser, so that I can begin analyzing and cleaning my data without installing any software.

#### Acceptance Criteria

1. WHEN a user drops a file onto the upload zone or selects a file via the file picker, THE Frontend SHALL accept only files with a `.csv` extension and SHALL reject all other file types with an error message before initiating any network request.
2. WHEN a user attempts to upload a file larger than 50 MB, THE Backend SHALL return HTTP 413 and SHALL NOT create a session.
3. WHEN a user uploads a valid CSV file at or below 50 MB, THE Upload_Handler SHALL create a session and return HTTP 200.
4. WHEN a user uploads a file that is not a valid CSV (malformed structure, mismatched column counts, or invalid encoding), THE Backend SHALL return HTTP 400 and SHALL NOT create a session.
5. WHEN a valid CSV file with N rows and M columns is uploaded, THE Upload_Handler SHALL return a response containing: `session_id`, `filename`, `row_count` equal to N, `column_count` equal to M, `columns`, `preview`, `duplicate_count`, `missing_value_summary`, and `inferred_types`.
6. WHEN a valid CSV file with N rows is uploaded, THE Upload_Handler SHALL return a `preview` array containing exactly `min(N, 10)` rows, and those rows SHALL be the first `min(N, 10)` rows of the dataset.
7. WHEN a CSV file is uploaded, THE Upload_Handler SHALL infer each column's type as one of `numeric`, `date`, or `text` and include the mapping in `inferred_types`.

---

### Requirement 2: Duplicate Record Removal

**User Story:** As a data analyst, I want to detect and remove duplicate rows from my dataset, so that my analysis is not skewed by repeated records.

#### Acceptance Criteria

1. WHEN a session exists with a dataset containing D duplicate rows, THE Data_Cleaner SHALL report exactly D duplicates in the upload response `duplicate_count` field.
2. WHEN a user requests duplicate removal, THE Data_Cleaner SHALL remove all duplicate rows from the Cleaned_Dataset, retaining the first occurrence of each unique row.
3. WHEN duplicate removal completes, THE Backend SHALL return `rows_removed` equal to D and `updated_row_count` equal to the original row count minus D.
4. WHEN duplicate removal completes, THE Cleaned_Dataset SHALL contain zero duplicate rows and SHALL contain every unique row that was present in the dataset before removal.

---

### Requirement 3: Missing Value Handling

**User Story:** As a data analyst, I want to detect, review, and resolve missing values in my dataset using appropriate strategies, so that downstream analysis and ML models are not degraded by incomplete data.

#### Acceptance Criteria

1. WHEN a CSV file is uploaded, THE Upload_Handler SHALL report the exact missing value count and percentage for each column, where `percentage = count / total_rows * 100`.
2. WHEN a user requests a fill-strategy suggestion for a column, THE AI_Engine SHALL return a `suggested_method` that is one of: `mean`, `median`, `mode`, `forward_fill`, `drop_rows`.
3. WHEN a user applies a fill strategy of `mean`, `median`, `mode`, or `forward_fill` to a column, THE Data_Cleaner SHALL reduce the missing value count for that column to 0.
4. WHEN a user applies the `drop_rows` strategy to a column, THE Data_Cleaner SHALL remove all rows that have a missing value in that column, and the missing value count for that column SHALL be 0 after the operation.
5. WHEN a user applies the `fill` strategy with a `fill_value` to a column, THE Data_Cleaner SHALL replace all missing values in that column with the specified `fill_value`.
6. WHEN missing value strategies are applied, THE Backend SHALL return `resolved_count` and an `updated_missing_summary` reflecting the new state of each affected column.
7. IF a `column` specified in a missing value strategy request does not exist in the dataset, THEN THE Backend SHALL return HTTP 400 with a descriptive error message.

---

### Requirement 4: Format Standardization

**User Story:** As a data analyst, I want to standardize column formats (dates, text casing, numeric parsing), so that my data is consistent and ready for analysis.

#### Acceptance Criteria

1. WHEN a user requests date standardization for a column, THE Data_Cleaner SHALL convert all recognized date strings in that column to the `YYYY-MM-DD` format.
2. WHEN a user requests text standardization for a column with a `casing` option of `lower`, `upper`, or `title`, THE Data_Cleaner SHALL strip leading and trailing whitespace from each value and apply the specified casing transformation.
3. WHEN a user requests numeric standardization for a column, THE Data_Cleaner SHALL parse numeric strings (including those with currency symbols or thousand separators) into numeric values.
4. WHEN a value in a column cannot be converted to the requested type, THE Data_Cleaner SHALL mark that cell as a missing value (NaN), and the missing value count for that column SHALL increase by 1 for each unconvertible value.
5. WHEN format standardization completes, THE Backend SHALL return `modified_columns`, `converted_value_count`, and `new_missing_count`.
6. IF a `column` specified in a format request does not exist in the dataset, THEN THE Backend SHALL return HTTP 400 with a descriptive error message.

---

### Requirement 5: Outlier Detection and Removal

**User Story:** As a data analyst, I want to detect and optionally remove statistical outliers from numeric columns, so that my analysis and ML models are not distorted by extreme values.

#### Acceptance Criteria

1. WHEN a user requests outlier detection, THE Data_Cleaner SHALL apply the IQR method to each numeric column and identify all values outside the range `[Q1 − 1.5 × IQR, Q3 + 1.5 × IQR]`.
2. WHEN outlier detection completes, THE Backend SHALL return an `outlier_summary` containing, for each numeric column with outliers: the outlier `count`, the `lower_bound` equal to `Q1 − 1.5 × IQR`, and the `upper_bound` equal to `Q3 + 1.5 × IQR`.
3. WHEN outlier detection completes, THE Backend SHALL return `outlier_row_indices` listing the row indices of all rows that contain at least one outlier value.
4. WHEN a user requests outlier removal, THE Data_Cleaner SHALL remove all rows from the Cleaned_Dataset that contain at least one value outside the IQR bounds for any numeric column.
5. WHEN outlier removal completes, THE Cleaned_Dataset SHALL contain no values outside the IQR bounds for any numeric column, and THE Backend SHALL return `rows_removed` equal to the number of rows removed and `updated_row_count` reflecting the new row count.

---

### Requirement 6: AI-Generated Insights

**User Story:** As a data analyst, I want to receive AI-generated insights about my dataset, so that I can quickly understand patterns, correlations, and data quality issues without manual exploration.

#### Acceptance Criteria

1. WHEN a user requests insights for a session, THE AI_Engine SHALL generate and return a response containing: `summary`, `top_correlations`, `temporal_trends`, and `quality_suggestions`.
2. WHEN insights are generated, THE AI_Engine SHALL return the 5 column pairs with the highest absolute Pearson correlation coefficients in the `top_correlations` list, ranked in descending order of absolute value, each entry containing `col_a`, `col_b`, `correlation`, and `description`.
3. WHEN insights are generated, THE AI_Engine SHALL return a `quality_suggestions` list containing at least 3 entries.
4. WHEN the insights request is processing, THE Backend SHALL complete the response within 30 seconds.
5. IF the OpenAI API call fails, THEN THE Backend SHALL return HTTP 502 with the message "AI service is temporarily unavailable. Please try again."

---

### Requirement 7: Summary Statistics

**User Story:** As a data analyst, I want to view summary statistics for each column in both the raw and cleaned datasets, so that I can understand the distribution of my data and measure the impact of cleaning.

#### Acceptance Criteria

1. WHEN a user requests statistics for a session, THE Stats_Engine SHALL return statistics for both the `raw` and `cleaned` datasets.
2. WHEN statistics are computed for a numeric column, THE Stats_Engine SHALL return: `count`, `mean`, `median`, `std`, `min`, `max`, `p25`, and `p75`, where `min ≤ p25 ≤ median ≤ p75 ≤ max`, `mean` equals the arithmetic mean of non-null values, and `std` equals the standard deviation of non-null values.
3. WHEN statistics are computed for a text column, THE Stats_Engine SHALL return: `count`, `unique`, `top` (most frequent value), and `top_freq` (frequency of the most frequent value).
4. WHEN statistics are computed, THE Stats_Engine SHALL label each column's stats with its inferred `type` (`numeric` or `text`).

---

### Requirement 8: Before/After Comparison

**User Story:** As a data analyst, I want to compare the raw and cleaned datasets side by side, so that I can understand the impact of each cleaning operation I applied.

#### Acceptance Criteria

1. WHEN a session has cleaning operations applied, THE Frontend SHALL display a comparison panel showing metrics for both the raw and cleaned datasets.
2. WHEN the comparison panel is displayed, THE Frontend SHALL show the total rows removed, duplicates removed, missing values resolved, outliers removed, and columns standardized.
3. WHEN the comparison panel is displayed, THE Frontend SHALL render bar and pie charts visualizing the before/after differences in dataset composition.
4. WHEN the comparison panel is displayed, THE Frontend SHALL source the raw metrics from the original upload response and the cleaned metrics from the cumulative results of all applied cleaning operations.

---

### Requirement 9: ML Problem Type Detection

**User Story:** As a data analyst, I want the system to automatically detect whether my target column requires classification or regression, so that the correct ML model type is selected without requiring ML expertise.

#### Acceptance Criteria

1. WHEN a user selects a target column for ML analysis, THE ML_Pipeline SHALL inspect the column's unique value count and inferred type to determine the problem type.
2. WHEN the target column has 10 or fewer unique values OR is of text type, THE ML_Pipeline SHALL return `problem_type` as `classification`.
3. WHEN the target column has more than 10 unique values AND is of numeric type, THE ML_Pipeline SHALL return `problem_type` as `regression`.
4. WHEN problem type detection completes, THE Backend SHALL return `target_column`, `problem_type`, `unique_value_count`, and `reasoning`.
5. IF the specified `target_column` does not exist in the dataset, THEN THE Backend SHALL return HTTP 400 with a descriptive error message.

---

### Requirement 10: ML Model Training and Comparison

**User Story:** As a data analyst, I want to train ML models on both the raw and cleaned datasets and compare their performance, so that I can quantify the value of data cleaning for predictive modeling.

#### Acceptance Criteria

1. WHEN ML training is requested, THE ML_Pipeline SHALL split each dataset using an 80/20 train-test split, where the training set contains `floor(0.8 × N)` rows and the test set contains the remaining rows, with no overlap between the two sets.
2. WHEN ML training is requested, THE ML_Pipeline SHALL train a Random Forest model on both the Raw_Dataset and the Cleaned_Dataset using the same target column and problem type.
3. WHEN a classification model is trained, THE ML_Pipeline SHALL compute and return `accuracy`, `precision`, `recall`, and `f1` metrics, each in the range `[0.0, 1.0]`.
4. WHEN a regression model is trained, THE ML_Pipeline SHALL compute and return `rmse`, `mae`, and `r2` metrics, where `rmse ≥ 0`, `mae ≥ 0`, and `r2 ≤ 1.0`.
5. WHEN ML training completes, THE Backend SHALL return `raw_model_metrics`, `cleaned_model_metrics`, `better_model`, `explanation`, `feature_importance`, and `top_features_description`.
6. WHEN determining the `better_model`, THE ML_Pipeline SHALL select the model with the higher value for `accuracy`, `precision`, `recall`, `f1`, and `r2`, and the lower value for `rmse` and `mae`.
7. WHEN ML training is requested for a dataset with at most 100,000 rows, THE ML_Pipeline SHALL complete training within 120 seconds.
8. IF ML training exceeds 120 seconds, THEN THE Backend SHALL return HTTP 504 with the message "Model training exceeded the 120-second time limit."

---

### Requirement 11: Feature Importance

**User Story:** As a data analyst, I want to see which features most influenced the ML model's predictions, so that I can understand the key drivers in my dataset.

#### Acceptance Criteria

1. WHEN ML training completes, THE ML_Pipeline SHALL return a `feature_importance` list where the sum of all scores is within 0.001 of 1.0.
2. WHEN ML training completes, THE ML_Pipeline SHALL return the `feature_importance` list sorted in non-increasing order of score (each score ≤ the previous score).
3. WHEN the feature importance chart is rendered for a model with F total features, THE Frontend SHALL display exactly `min(F, 10)` features, and those features SHALL be the ones with the highest importance scores.
4. WHEN ML training completes, THE Backend SHALL return a `top_features_description` providing a plain-language explanation of the most important features.

---

### Requirement 12: Download and Export

**User Story:** As a data analyst, I want to download the cleaned dataset as a CSV and an insights report as a PDF, so that I can share results and use the cleaned data in other tools.

#### Acceptance Criteria

1. WHEN a user requests the cleaned CSV export, THE Backend SHALL return a `text/csv` file stream with `Content-Disposition: attachment; filename="cleaned_<original_filename>.csv"`.
2. WHEN the cleaned CSV is downloaded and re-parsed, THE resulting DataFrame SHALL have the same shape, column names, and values as the Cleaned_Dataset (within floating-point tolerance for numeric columns).
3. WHEN a user requests the PDF report export, THE Backend SHALL return an `application/pdf` file stream with `Content-Disposition: attachment; filename="insights_report_<original_filename>.pdf"`.
4. WHEN the PDF report is generated, THE PDF_Generator SHALL include: summary statistics, AI insights, data-quality metrics, and ML model comparison results.
5. WHEN a user requests an export for a session that does not exist, THE Backend SHALL return HTTP 404.
6. IF PDF generation fails, THEN THE Backend SHALL return HTTP 500 with the message "Failed to generate the insights report."

---

### Requirement 13: Responsive and Accessible UI

**User Story:** As a data analyst, I want the dashboard to be usable on any screen size and accessible to assistive technologies, so that I can work effectively regardless of my device or accessibility needs.

#### Acceptance Criteria

1. THE Frontend SHALL render without horizontal scrolling at any viewport width between 768px and 2560px.
2. WHEN a backend operation takes longer than 500ms to respond, THE Frontend SHALL display a loading indicator before the response arrives and SHALL hide it after the response is received.
3. WHEN an API error occurs, THE Frontend SHALL display a dismissible error banner at the top of the relevant panel and SHALL NOT block the rest of the UI.
4. THE Frontend SHALL apply CSS transitions in the range of 200ms to 400ms for interactive state changes.
5. THE Frontend SHALL meet WCAG 2.1 AA color contrast requirements, with a minimum contrast ratio of 4.5:1 for all text elements.
6. THE Frontend SHALL provide a non-empty `aria-label` attribute on every interactive element, including buttons, inputs, charts, and dropdowns.
7. WHEN a session is not found (e.g., after a server restart), THE Backend SHALL return HTTP 404 with the message "Session '{id}' not found or has expired."
