---
inclusion: auto
---

# Project Rules — DataDoctor AI

## Architecture

- Backend and frontend are separate applications communicating via REST API
- All API endpoints are prefixed with `/api/v1`
- Sessions are stored in-memory, keyed by UUID
- The backend owns all data processing — the frontend never manipulates data directly
- OpenAI integration has fallback heuristics for when the API is unavailable

## API Contract

- All error responses follow: `{"detail": "<message>"}`
- File uploads use `multipart/form-data`
- All other requests/responses use JSON
- File downloads use `StreamingResponse` with `Content-Disposition` headers
- Response models are defined in `app/models/schemas.py` (Pydantic)
- Frontend types mirror backend schemas in `src/types/api.ts`

## Session Lifecycle

- Created on CSV upload → returns `session_id`
- All subsequent operations reference `session_id`
- `raw_df` is immutable after upload
- `cleaned_df` accumulates all cleaning operations
- Sessions are lost on server restart (acceptable for demo)

## Data Flow

1. Upload → creates session with raw_df and cleaned_df (copy)
2. Cleaning operations mutate cleaned_df
3. Stats computed on both raw_df and cleaned_df
4. ML trains on both raw_df and cleaned_df for comparison
5. Export serializes cleaned_df

## Testing Strategy

- Backend: pytest + Hypothesis for property-based tests
- Frontend: Vitest + React Testing Library + axe-core
- Property tests validate correctness invariants (29 properties defined)
- Unit tests cover specific edge cases and error conditions

## Development Workflow

- Backend dev server: `uvicorn app.main:app --reload --port 8000`
- Frontend dev server: `npm run dev` (port 5173)
- Backend tests: `pytest` from `backend/` directory
- Frontend tests: `npm test` from `frontend/` directory
- Frontend build: `npm run build` from `frontend/` directory

## File Naming

- Python: `snake_case.py`
- TypeScript components: `PascalCase.tsx`
- TypeScript utilities: `camelCase.ts`
- Config files: lowercase with dots (e.g., `vite.config.ts`)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | None | OpenAI API key for AI features |
| `MAX_FILE_SIZE_MB` | 50 | Maximum upload file size |
| `VITE_API_BASE_URL` | `http://localhost:8000/api/v1` | Backend API URL for frontend |

## Deployment

- Backend: Any ASGI server (uvicorn, gunicorn+uvicorn)
- Frontend: Static files served by any web server (nginx, S3+CloudFront)
- See `AWS_DEPLOYMENT.md` for cloud deployment guide
