from fastapi import APIRouter
from app.errors import AppError
from app.models.schemas import (
    DuplicateRemovalResponse,
    ApplyMissingValueRequest,
    MissingValueResponse,
    MissingValueInfo,
    SuggestFillStrategyRequest,
    SuggestFillStrategyResponse,
    ApplyFormatRequest,
    FormatResponse,
    OutlierDetectResponse,
    OutlierColumnInfo,
    OutlierRemoveResponse,
)
from app.services.session_store import session_store
from app.services.data_cleaner import (
    remove_duplicates,
    missing_value_summary,
    apply_missing_value_strategies,
    standardize_formats,
    detect_outliers,
    remove_outliers,
)

router = APIRouter()


@router.post("/sessions/{session_id}/clean/duplicates", response_model=DuplicateRemovalResponse)
async def clean_duplicates(session_id: str):
    session = session_store.get(session_id)
    new_df, rows_removed = remove_duplicates(session.cleaned_df)
    session.cleaned_df = new_df
    session.duplicates_removed += rows_removed
    session_store.update(session)
    return DuplicateRemovalResponse(
        rows_removed=rows_removed,
        updated_row_count=len(new_df),
    )


@router.post("/sessions/{session_id}/clean/missing-values", response_model=MissingValueResponse)
async def clean_missing_values(session_id: str, body: ApplyMissingValueRequest):
    session = session_store.get(session_id)
    for strategy in body.strategies:
        if strategy.column not in session.cleaned_df.columns:
            raise AppError(400, f"Column '{strategy.column}' does not exist in the dataset.")
    new_df, resolved_count, updated_summary_raw = apply_missing_value_strategies(
        session.cleaned_df, body.strategies
    )
    session.cleaned_df = new_df
    session.missing_resolved += resolved_count
    session_store.update(session)
    updated_summary = {col: MissingValueInfo(**info) for col, info in updated_summary_raw.items()}
    return MissingValueResponse(
        resolved_count=resolved_count,
        updated_missing_summary=updated_summary,
    )


@router.post(
    "/sessions/{session_id}/clean/missing-values/suggest",
    response_model=SuggestFillStrategyResponse,
)
async def suggest_missing_value_strategy(session_id: str, body: SuggestFillStrategyRequest):
    session = session_store.get(session_id)
    if body.column not in session.cleaned_df.columns:
        raise AppError(400, f"Column '{body.column}' does not exist in the dataset.")
    from app.services.ai_engine import suggest_fill_strategy
    from app.config import OPENAI_API_KEY

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        client = None

    result = suggest_fill_strategy(body.column, session.cleaned_df, client)
    return SuggestFillStrategyResponse(**result)


@router.post("/sessions/{session_id}/clean/format", response_model=FormatResponse)
async def clean_format(session_id: str, body: ApplyFormatRequest):
    session = session_store.get(session_id)
    for req in body.columns:
        if req.column not in session.cleaned_df.columns:
            raise AppError(400, f"Column '{req.column}' does not exist in the dataset.")
    new_df, modified_columns, converted_count, new_missing = standardize_formats(
        session.cleaned_df, body.columns
    )
    session.cleaned_df = new_df
    for col in modified_columns:
        if col not in session.columns_standardized:
            session.columns_standardized.append(col)
    session_store.update(session)
    return FormatResponse(
        modified_columns=modified_columns,
        converted_value_count=converted_count,
        new_missing_count=new_missing,
    )


@router.post(
    "/sessions/{session_id}/clean/outliers/detect",
    response_model=OutlierDetectResponse,
)
async def detect_outliers_endpoint(session_id: str):
    session = session_store.get(session_id)
    outlier_summary_raw, outlier_row_indices = detect_outliers(session.cleaned_df)
    outlier_summary = {
        col: OutlierColumnInfo(**info) for col, info in outlier_summary_raw.items()
    }
    return OutlierDetectResponse(
        outlier_summary=outlier_summary,
        outlier_row_indices=outlier_row_indices,
    )


@router.post(
    "/sessions/{session_id}/clean/outliers/remove",
    response_model=OutlierRemoveResponse,
)
async def remove_outliers_endpoint(session_id: str):
    session = session_store.get(session_id)
    new_df, rows_removed = remove_outliers(session.cleaned_df)
    session.cleaned_df = new_df
    session.outliers_removed += rows_removed
    session_store.update(session)
    return OutlierRemoveResponse(
        rows_removed=rows_removed,
        updated_row_count=len(new_df),
    )
