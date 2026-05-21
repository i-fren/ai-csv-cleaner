import { useState, useCallback } from 'react';

interface UseSessionReturn {
  sessionId: string | null;
  setSessionId: (id: string) => void;
  clearSession: () => void;
}

export function useSession(): UseSessionReturn {
  const [sessionId, setSessionIdState] = useState<string | null>(null);

  const setSessionId = useCallback((id: string) => {
    setSessionIdState(id);
  }, []);

  const clearSession = useCallback(() => {
    setSessionIdState(null);
  }, []);

  return { sessionId, setSessionId, clearSession };
}
