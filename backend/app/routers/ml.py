from fastapi import APIRouter
from app.errors import AppError
from app.models.schemas import (
    DetectProblemTypeRequest,
    DetectProblemTypeResponse,
    TrainRequest,
    MLResult,
    ClassificationMetrics,
    RegressionMetrics,
    FeatureImportanceEntry,
)
from app.services.session_store import session_store
from app.services.ml_pipeline import detect_problem_type, train_models
from app.config import OPENAI_API_KEY

router = APIRouter()


@router.post(
    "/sessions/{session_id}/ml/detect-problem-type",
    response_model=DetectProblemTypeResponse,
)
async def detect_problem_type_endpoint(session_id: str, body: DetectProblemTypeRequest):
    session = session_store.get(session_id)
    result = detect_problem_type(
        session.cleaned_df, body.target_column, session.inferred_types
    )
    return DetectProblemTypeResponse(**result)


@router.post("/sessions/{session_id}/ml/train", response_model=MLResult)
async def train_models_endpoint(session_id: str, body: TrainRequest):
    session = session_store.get(session_id)

    if body.target_column not in session.cleaned_df.columns:
        raise AppError(400, f"Column '{body.target_column}' does not exist in the dataset.")

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
    except Exception:
        client = None

    result_data = train_models(
        raw_df=session.raw_df,
        cleaned_df=session.cleaned_df,
        target_column=body.target_column,
        problem_type=body.problem_type,
        openai_client=client,
    )

    # Build typed metrics
    if body.problem_type == "classification":
        raw_metrics = ClassificationMetrics(**result_data["raw_model_metrics"])
        cleaned_metrics = ClassificationMetrics(**result_data["cleaned_model_metrics"])
    else:
        raw_metrics = RegressionMetrics(**result_data["raw_model_metrics"])
        cleaned_metrics = RegressionMetrics(**result_data["cleaned_model_metrics"])

    feature_importance = [
        FeatureImportanceEntry(**fi) for fi in result_data["feature_importance"]
    ]

    ml_result = MLResult(
        problem_type=body.problem_type,
        raw_model_metrics=raw_metrics,
        cleaned_model_metrics=cleaned_metrics,
        better_model=result_data["better_model"],
        explanation=result_data["explanation"],
        feature_importance=feature_importance,
        top_features_description=result_data["top_features_description"],
    )

    session.ml_result = ml_result
    session_store.update(session)

    return ml_result
