"""
main.py
-------
FastAPI application entry point for DataDoctor AI.

Configures CORS, registers all API routers, and sets up
global error handling for consistent JSON error responses.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.errors import AppError
from app.routers import upload, cleaning, stats, insights, ml, export, chat

# ---------------------------------------------------------------------------
# Application Instance
# ---------------------------------------------------------------------------

app = FastAPI(
    title="DataDoctor AI — CSV Analyzer",
    version="1.0.0",
    description="AI-powered CSV data cleaning, analysis, and machine learning platform.",
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permissive for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Global Error Handler
# ---------------------------------------------------------------------------


@app.exception_handler(AppError)
async def app_error_handler(request, exc: AppError):
    """Return all business errors as JSON with appropriate HTTP status."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


# ---------------------------------------------------------------------------
# Router Registration
# ---------------------------------------------------------------------------

app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(cleaning.router, prefix="/api/v1", tags=["Cleaning"])
app.include_router(stats.router, prefix="/api/v1", tags=["Statistics"])
app.include_router(insights.router, prefix="/api/v1", tags=["Insights"])
app.include_router(ml.router, prefix="/api/v1", tags=["Machine Learning"])
app.include_router(export.router, prefix="/api/v1", tags=["Export"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------


@app.get("/health", tags=["System"])
async def health():
    """Health check endpoint for monitoring and load balancers."""
    return {"status": "ok", "service": "datadoctor-ai"}