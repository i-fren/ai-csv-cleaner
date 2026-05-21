import { useState } from 'react';
import { removeDuplicates } from '../../api/client';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorBanner } from '../shared/ErrorBanner';
import type { DuplicateRemovalResponse } from '../../types/api';

interface DuplicateCardProps {
  sessionId: string;
  duplicateCount: number;
  onRemoved: (result: DuplicateRemovalResponse) => void;
}

export function DuplicateCard({ sessionId, duplicateCount, onRemoved }: DuplicateCardProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DuplicateRemovalResponse | null>(null);

  const handleRemove = async () => {
    setError(null);
    setLoading(true);
    try {
      const res = await removeDuplicates(sessionId);
      setResult(res);
      onRemoved(res);
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to remove duplicates.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-2xl bg-white/5 border border-white/10 p-5">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-xl bg-orange-500/20 flex items-center justify-center text-xl">🔁</div>
        <div>
          <h3 className="font-semibold text-white">Duplicate Records</h3>
          <p className="text-xs text-gray-500">Identical rows in your dataset</p>
        </div>
      </div>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />
      <div className="flex items-center justify-between mb-4">
        <span className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium ${
          duplicateCount > 0 ? 'bg-orange-500/15 text-orange-400 border border-orange-500/20' : 'bg-green-500/15 text-green-400 border border-green-500/20'
        }`}>
          {duplicateCount > 0 ? '⚠️' : '✅'} {duplicateCount} duplicate{duplicateCount !== 1 ? 's' : ''} found
        </span>
        {result && <span className="text-xs text-gray-500">{result.rows_removed} removed · {result.updated_row_count} remain</span>}
      </div>
      {loading ? <LoadingSpinner loading size="sm" /> : (
        <button
          type="button"
          onClick={handleRemove}
          disabled={duplicateCount === 0 || !!result}
          aria-label="Remove duplicate rows"
          className="w-full py-2.5 rounded-xl bg-orange-500/20 hover:bg-orange-500/30 border border-orange-500/30 text-orange-300 text-sm font-medium transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {result ? '✅ Duplicates Removed' : 'Remove Duplicates'}
        </button>
      )}
    </div>
  );
}
