"""
errors.py
---------
Custom exception classes for the DataDoctor AI backend.

All business errors are raised as AppError instances and caught by the
global exception handler in main.py, which returns them as JSON responses.
"""


class AppError(Exception):
    """
    Application-level HTTP error raised by route handlers and services.

    Attributes:
        status_code: HTTP status code to return (e.g., 400, 404, 413, 500, 502)
        message: Human-readable error message included in the JSON response
    """

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)

    def __repr__(self) -> str:
        return f"AppError(status_code={self.status_code}, message={self.message!r})"
