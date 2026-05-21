import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.errors import AppError
from app.services.session_store import session_store
from app.services.pdf_generator import generate_pdf

router = APIRouter()


@router.get("/sessions/{session_id}/export/csv")
async def export_csv(session_id: str):
    session = session_store.get(session_id)
    csv_bytes = session.cleaned_df.to_csv(index=False).encode("utf-8")
    filename = f"cleaned_{session.filename}"
    return StreamingResponse(
        io.BytesIO(csv_bytes),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/sessions/{session_id}/export/report")
async def export_report(session_id: str):
    session = session_store.get(session_id)
    try:
        pdf_bytes = generate_pdf(session)
    except Exception as e:
        raise AppError(500, "Failed to generate the insights report.")
    filename = f"insights_report_{session.filename.replace('.csv', '.pdf')}"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
