"""
config.py
---------
Application configuration loaded from environment variables.

Environment Variables:
    OPENAI_API_KEY   — OpenAI API key for AI features (optional; fallback heuristics used if absent)
    MAX_FILE_SIZE_MB — Maximum allowed CSV upload size in megabytes (default: 50)
"""

import os

# OpenAI API key for AI-powered insights, suggestions, and chat.
# The application gracefully degrades when this is not set.
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

# Maximum file upload size in megabytes. Files exceeding this limit
# are rejected with HTTP 413 before any processing occurs.
MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))

# Computed byte limit for convenience
MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
