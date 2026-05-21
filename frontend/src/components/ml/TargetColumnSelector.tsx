import { useState } from 'react';
import { detectProblemType } from '../../api/client';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorBanner } from '../shared/ErrorBanner';
import type { DetectProblemTypeResponse } from '../../types/api';

interface TargetColumnSelectorProps {
  sessionId: string;
  columns: string[];
  onDetected: (response: DetectProblemTypeResponse) => void;
}

export function TargetColumnSelector({ sessionId, columns, onDetected }: TargetColumnSelectorProps) {
  const [selected, setSelected] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = async (col: string) => {
    setSelected(col);
    if (!col) return;
    setError(null);
    setLoading(true);
    try {
      onDetected(await detectProblemType(sessionId, col));
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to detect problem type.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />
      <div className="flex items-center gap-3">
        <label htmlFor="target-col" className="text-sm font-medium text-gray-300">Target Column</label>
        <select
          id="target-col"
          value={selected}
          onChange={(e) => handleChange(e.target.value)}
          aria-label="Select target column for ML"
          className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50"
        >
          <option value="" className="bg-gray-900">-- Select a column --</option>
          {columns.map((col) => (
            <option key={col} value={col} className="bg-gray-900">{col}</option>
          ))}
        </select>
        {loading && <LoadingSpinner loading size="sm" />}
      </div>
    </div>
  );
}
