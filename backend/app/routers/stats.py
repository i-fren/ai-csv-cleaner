from fastapi import APIRouter
from app.models.schemas import StatsResponse
from app.services.session_store import session_store
from app.services.stats_engine import compute_stats

router = APIRouter()


@router.get("/sessions/{session_id}/stats", response_model=StatsResponse)
async def get_stats(session_id: str):
    session = session_store.get(session_id)
    raw_stats = compute_stats(session.raw_df, session.inferred_types)
    cleaned_stats = compute_stats(session.cleaned_df, session.inferred_types)
    return StatsResponse(raw=raw_stats, cleaned=cleaned_stats)
