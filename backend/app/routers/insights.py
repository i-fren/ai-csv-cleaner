from fastapi import APIRouter
from app.errors import AppError
from app.models.schemas import InsightResult, CorrelationEntry
from app.services.session_store import session_store
from app.services.stats_engine import compute_top_correlations
from app.services.ai_engine import generate_insights
from app.config import OPENAI_API_KEY

router = APIRouter()


@router.post("/sessions/{session_id}/insights", response_model=InsightResult)
async def get_insights(session_id: str):
    session = session_store.get(session_id)

    # Compute correlations (pure Python, no AI needed)
    top_correlations = compute_top_correlations(session.cleaned_df, top_n=5)

    # Get OpenAI client
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
    except Exception:
        client = None

    # Generate insights (falls back gracefully if no API key)
    insight_data = generate_insights(session, client, top_correlations)

    # Build CorrelationEntry objects
    correlation_entries = [
        CorrelationEntry(**entry) for entry in top_correlations
    ]

    result = InsightResult(
        summary=insight_data["summary"],
        top_correlations=correlation_entries,
        temporal_trends=insight_data.get("temporal_trends"),
        quality_suggestions=insight_data["quality_suggestions"],
    )

    # Cache in session
    session.insights = result
    session_store.update(session)

    return result
