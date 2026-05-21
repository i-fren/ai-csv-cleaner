---
inclusion: auto
---

# Coding Standards — DataDoctor AI

## Python (Backend)

### Style
- Follow PEP 8 with 100-character line limit
- Use type hints on all function signatures
- Use docstrings (Google style) on all public functions
- Use `snake_case` for functions and variables, `PascalCase` for classes

### Structure
- Each service module has a clear section header with comments
- Imports grouped: stdlib → third-party → local
- One router per domain (upload, cleaning, stats, insights, ml, export, chat)
- Business logic lives in `services/`, not in routers

### Error Handling
- Use `AppError(status_code, message)` for all business errors
- Never expose stack traces to the client
- Always validate input before processing
- Use try/except around external API calls (OpenAI) with fallback behavior

### Patterns
```python
# Router pattern
@router.post("/sessions/{session_id}/action", response_model=ResponseModel)
async def action_endpoint(session_id: str, body: RequestModel):
    session = session_store.get(session_id)  # Raises 404 if not found
    # Validate inputs
    # Call service function
    # Update session
    # Return response model
```

### Dependencies
- Pin exact versions in requirements.txt
- No unused imports
- Prefer stdlib over third-party when equivalent

---

## TypeScript (Frontend)

### Style
- Use TypeScript strict mode
- Define interfaces for all API responses in `types/api.ts`
- Use functional components with hooks
- Use `camelCase` for variables/functions, `PascalCase` for components/interfaces

### Structure
- One component per file
- Components organized by feature domain (upload/, cleaning/, insights/, etc.)
- Shared components in `shared/`
- API calls centralized in `api/client.ts`
- Custom hooks in `hooks/`

### Patterns
```typescript
// Component pattern
interface Props {
  sessionId: string;
  onSuccess: (result: ResultType) => void;
}

export function ComponentName({ sessionId, onSuccess }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // ...
}
```

### State Management
- Lift state to the nearest common ancestor
- Use props for parent-child communication
- Use `useApi` hook for API call state (loading, error, data)
- Session ID managed at App.tsx level

### Error Handling
- All API calls wrapped in try/catch
- Display errors via `ErrorBanner` component
- Never show raw error objects to users
- Extract `error.response.data.detail` for user-friendly messages

---

## General Rules

- No `console.log` in production code (use proper error handling)
- No hardcoded URLs — use environment variables
- No secrets in source code — use `.env` files
- Comments explain "why", not "what"
- Keep functions under 50 lines where possible
- Prefer early returns over deep nesting
- DRY: Extract repeated logic into utility functions
