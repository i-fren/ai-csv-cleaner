import io
import uuid
import pandas as pd
from fastapi import APIRouter, UploadFile, File
from app.errors import AppError
from app.config import MAX_FILE_SIZE_MB
from app.models.schemas import UploadResponse, MissingValueInfo
from app.services.session_store import Session, session_store
from app.services.data_cleaner import infer_column_types, count_duplicates, missing_value_summary

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    # Validate extension
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise AppError(400, "Only .csv files are accepted.")

    # Read and validate size
    content = await file.read()
    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise AppError(413, "File size exceeds the 50 MB limit.")

    # Parse CSV
    try:
        df = pd.read_csv(io.BytesIO(content))
    except pd.errors.ParserError as e:
        raise AppError(400, f"CSV parsing failed: {e}")
    except Exception as e:
        raise AppError(400, f"CSV parsing failed: {e}")

    if len(df) == 0:
        raise AppError(400, "CSV file contains no data rows.")

    # Compute metadata
    inferred_types = infer_column_types(df)
    dup_count = count_duplicates(df)
    mv_summary_raw = missing_value_summary(df)
    mv_summary = {col: MissingValueInfo(**info) for col, info in mv_summary_raw.items()}

    # Create session
    session_id = str(uuid.uuid4())
    session = Session(
        session_id=session_id,
        filename=file.filename,
        raw_df=df.copy(),
        cleaned_df=df.copy(),
        inferred_types=inferred_types,
    )
    session_store.create(session)

    # Build preview (first min(N, 10) rows)
    preview = df.head(10).fillna("").to_dict(orient="records")

    return UploadResponse(
        session_id=session_id,
        filename=file.filename,
        row_count=len(df),
        column_count=len(df.columns),
        columns=list(df.columns),
        preview=preview,
        duplicate_count=dup_count,
        missing_value_summary=mv_summary,
        inferred_types=inferred_types,
    )
