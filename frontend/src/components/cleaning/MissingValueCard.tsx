import { useState } from 'react';
import { applyMissingValueStrategies, suggestFillStrategy } from '../../api/client';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorBanner } from '../shared/ErrorBanner';
import type { MissingValueInfo, MissingValueMethod, MissingValueResponse } from '../../types/api';

interface MissingValueCardProps {
  sessionId: string;
  missingSummary: Record<string, MissingValueInfo>;
  onApplied: (result: MissingValueResponse) => void;
}

const METHODS: MissingValueMethod[] = ['mean', 'median', 'mode', 'forward_fill', 'drop_rows', 'fill'];

export function MissingValueCard({ sessionId, missingSummary, onApplied }: MissingValueCardProps) {
  const columnsWithMissing = Object.entries(missingSummary).filter(([, info]) => info.count > 0);
  const [strategies, setStrategies] = useState<Record<string, MissingValueMethod>>(
    Object.fromEntries(columnsWithMissing.map(([col]) => [col, 'mode']))
  );
  const [fillValues, setFillValues] = useState<Record<string, string>>({});
  const [suggesting, setSuggesting] = useState<Record<string, boolean>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [applied, setApplied] = useState(false);

  const handleSuggest = async (col: string) => {
    setSuggesting((p) => ({ ...p, [col]: true }));
    try {
      const res = await suggestFillStrategy(sessionId, col);
      setStrategies((p) => ({ ...p, [col]: res.suggested_method }));
    } catch { /* ignore */ }
    finally { setSuggesting((p) => ({ ...p, [col]: false })); }
  };

  const handleApply = async () => {
    setError(null); setLoading(true);
    try {
      const res = await applyMissingValueStrategies(sessionId, {
        strategies: columnsWithMissing.map(([col]) => ({
          column: col, method: strategies[col] || 'mode',
          fill_value: strategies[col] === 'fill' ? (fillValues[col] || '') : undefined,
        })),
      });
      setApplied(true); onApplied(res);
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to apply strategies.');
    } finally { setLoading(false); }
  };

  if (columnsWithMissing.length === 0) {
    return (
      <div className="rounded-2xl bg-white/5 border border-white/10 p-5">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-green-500/20 flex items-center justify-center text-xl">✅</div>
          <h3 className="font-semibold text-white">Missing Values</h3>
        </div>
        <p className="text-sm text-green-400">No missing values found — your data is complete!</p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-white/5 border border-white/10 p-5">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-xl bg-yellow-500/20 flex items-center justify-center text-xl">❓</div>
        <div>
          <h3 className="font-semibold text-white">Missing Values</h3>
          <p className="text-xs text-gray-500">{columnsWithMissing.length} column(s) affected</p>
        </div>
      </div>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />

      <div className="mb-4 max-h-56 overflow-y-auto space-y-2 scrollbar-thin">
        {columnsWithMissing.map(([col, info]) => (
          <div key={col} className="rounded-xl bg-white/3 border border-white/10 p-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-300">{col}</span>
              <span className="text-xs text-yellow-400">{info.count} missing ({info.percentage.toFixed(1)}%)</span>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <select
                value={strategies[col] || 'mode'}
                onChange={(e) => setStrategies((p) => ({ ...p, [col]: e.target.value as MissingValueMethod }))}
                aria-label={`Fill strategy for ${col}`}
                className="rounded-lg border border-white/10 bg-white/5 px-2 py-1 text-xs text-gray-300 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                {METHODS.map((m) => <option key={m} value={m} className="bg-gray-900">{m.replace('_', ' ')}</option>)}
              </select>
              {strategies[col] === 'fill' && (
                <input type="text" placeholder="Fill value" value={fillValues[col] || ''}
                  onChange={(e) => setFillValues((p) => ({ ...p, [col]: e.target.value }))}
                  aria-label={`Fill value for ${col}`}
                  className="rounded-lg border border-white/10 bg-white/5 px-2 py-1 text-xs text-gray-300 focus:outline-none focus:ring-1 focus:ring-blue-500 w-24" />
              )}
              <button type="button" onClick={() => handleSuggest(col)} disabled={suggesting[col]}
                aria-label={`Suggest fill strategy for ${col}`}
                className="px-2 py-1 rounded-lg bg-blue-500/20 border border-blue-500/30 text-xs text-blue-300 hover:bg-blue-500/30 transition-all disabled:opacity-50">
                {suggesting[col] ? '...' : '✨ AI'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {loading ? <LoadingSpinner loading size="sm" /> : (
        <button type="button" onClick={handleApply} disabled={applied}
          aria-label="Apply missing value strategies"
          className="w-full py-2.5 rounded-xl bg-yellow-500/20 hover:bg-yellow-500/30 border border-yellow-500/30 text-yellow-300 text-sm font-medium transition-all duration-200 disabled:opacity-40">
          {applied ? '✅ Strategies Applied' : 'Apply Strategies'}
        </button>
      )}
    </div>
  );
}
