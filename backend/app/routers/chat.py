from fastapi import APIRouter
from pydantic import BaseModel
from app.errors import AppError
from app.services.session_store import session_store
from app.config import OPENAI_API_KEY

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/sessions/{session_id}/chat", response_model=ChatResponse)
async def chat_with_data(session_id: str, body: ChatRequest):
    session = session_store.get(session_id)
    df = session.cleaned_df

    # Build context about the dataset
    shape = f"{len(df)} rows x {len(df.columns)} columns"
    cols = list(df.columns)
    dtypes = {col: str(df[col].dtype) for col in cols}
    missing = {col: int(df[col].isna().sum()) for col in cols if df[col].isna().sum() > 0}
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    stats_summary = ""
    if numeric_cols:
        desc = df[numeric_cols].describe().to_string()
        stats_summary = f"\nNumeric statistics:\n{desc}"

    context = (
        f"Dataset: {session.filename}\n"
        f"Shape: {shape}\n"
        f"Columns: {', '.join(cols)}\n"
        f"Data types: {dtypes}\n"
        f"Missing values: {missing if missing else 'None'}\n"
        f"Duplicates removed: {session.duplicates_removed}\n"
        f"Missing values resolved: {session.missing_resolved}\n"
        f"Outliers removed: {session.outliers_removed}\n"
        f"{stats_summary}"
    )

    prompt = (
        f"You are DataDoctor AI, an expert data analyst assistant. "
        f"Answer the user's question about their dataset concisely and helpfully.\n\n"
        f"Dataset context:\n{context}\n\n"
        f"User question: {body.message}\n\n"
        f"Provide a clear, actionable answer in 2-4 sentences. "
        f"Use plain language suitable for non-technical users."
    )

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=300,
        )
        reply = response.choices[0].message.content.strip()
    except Exception:
        # Fallback: rule-based responses when OpenAI is unavailable
        msg = body.message.lower()
        if "missing" in msg or "null" in msg or "empty" in msg:
            if missing:
                top = max(missing, key=missing.get)
                reply = (
                    f"The column with the most missing values is '{top}' "
                    f"with {missing[top]} missing entries. "
                    f"Total columns with missing data: {len(missing)}."
                )
            else:
                reply = "Great news — your dataset has no missing values after cleaning!"
        elif "duplicate" in msg:
            reply = (
                f"DataDoctor removed {session.duplicates_removed} duplicate rows from your dataset. "
                f"The cleaned dataset now has {len(df)} unique rows."
            )
        elif "outlier" in msg:
            reply = (
                f"{session.outliers_removed} outlier rows were removed during cleaning. "
                f"Outliers were detected using the IQR method on numeric columns."
            )
        elif "summar" in msg or "overview" in msg or "about" in msg:
            reply = (
                f"Your dataset '{session.filename}' contains {shape}. "
                f"After cleaning: {session.duplicates_removed} duplicates removed, "
                f"{session.missing_resolved} missing values resolved, "
                f"{session.outliers_removed} outliers removed."
            )
        elif "trend" in msg or "pattern" in msg:
            if numeric_cols:
                reply = (
                    f"Your dataset has {len(numeric_cols)} numeric columns: {', '.join(numeric_cols[:5])}. "
                    f"Run the Insights panel for AI-generated trend analysis and correlations."
                )
            else:
                reply = "No numeric columns found for trend analysis. Your dataset appears to be primarily categorical."
        elif "column" in msg or "feature" in msg:
            reply = (
                f"Your dataset has {len(cols)} columns: {', '.join(cols[:8])}{'...' if len(cols) > 8 else ''}. "
                f"Use the Insights panel to see which columns are most important for modeling."
            )
        elif "quality" in msg or "score" in msg or "good" in msg:
            total_issues = session.duplicates_removed + session.missing_resolved + session.outliers_removed
            score = max(60, 100 - total_issues // max(len(df) // 10, 1))
            reply = (
                f"Your data quality score is approximately {score}/100. "
                f"DataDoctor fixed {total_issues} total issues including duplicates, missing values, and outliers."
            )
        else:
            reply = (
                f"Your dataset has {shape} with {len(cols)} columns. "
                f"DataDoctor has cleaned it by removing {session.duplicates_removed} duplicates, "
                f"resolving {session.missing_resolved} missing values, and removing {session.outliers_removed} outliers. "
                f"Try asking about specific columns, trends, or data quality!"
            )

    return ChatResponse(reply=reply)
