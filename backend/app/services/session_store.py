from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import pandas as pd


@dataclass
class Session:
    session_id: str
    filename: str
    raw_df: pd.DataFrame
    cleaned_df: pd.DataFrame
    inferred_types: dict[str, str]

    # Cleaning audit trail
    duplicates_removed: int = 0
    missing_resolved: int = 0
    outliers_removed: int = 0
    columns_standardized: list[str] = field(default_factory=list)

    # Derived results (populated lazily)
    insights: Any | None = None
    ml_result: Any | None = None

    created_at: datetime = field(default_factory=datetime.utcnow)


class SessionStore:
    def __init__(self):
        self._store: dict[str, Session] = {}

    def create(self, session: Session) -> None:
        self._store[session.session_id] = session

    def get(self, session_id: str) -> Session:
        session = self._store.get(session_id)
        if session is None:
            from app.errors import AppError
            raise AppError(
                status_code=404,
                message=f"Session '{session_id}' not found or has expired."
            )
        return session

    def update(self, session: Session) -> None:
        self._store[session.session_id] = session

    def delete(self, session_id: str) -> None:
        self._store.pop(session_id, None)


# Module-level singleton
session_store = SessionStore()
