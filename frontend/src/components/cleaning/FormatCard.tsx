import { useState } from 'react';
import { applyFormat } from '../../api/client';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorBanner } from '../shared/ErrorBanner';
import type { FormatType, TextCasing, FormatResponse } from '../../types/api';

interface FormatCardProps {
  sessionId: string;
  columns: string[];
  inferredTypes: Record<string, string>;
  onApplied: (result: FormatResponse) => void;
}

export function FormatCard({ sessionId, columns, inferredTypes, onApplied }: FormatCardProps) {
  const [selectedCols, setSelectedCols] = useState<Record<string, boolean>>({});
  const [types, setTypes] = useState<Record<string, FormatType>>(
    Object.fromEntries(columns.map((c) => [c, (inferredTypes[c] as FormatType) || 'text']))
  );
  const [casings, setCasings] = useState<Record<string, TextCasing>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [applied, setApplied] = useState(false);

  const handleApply = async () => {
    const selected = columns.filter((c) => selectedCols[c]);
    if (!selected.length) { setError('Select at least one column to standardize.'); return; }
    setError(null); setLoading(true);
    try {
      const res = await applyFormat(sessionId, {
        columns: selected.map((col) => ({
          column: col, type: types[col] || 'text',
          casing: types[col] === 'text' ? casings[col] : undefined,
        })),
      });
      setApplied(true); onApplied(res);
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to apply format.');
    } finally { setLoading(false); }
  };

  return (
    <div className="rounded-2xl bg-white/5 border border-white/10 p-5">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-xl bg-blue-500/20 flex items-center justify-center text-xl">📐</div>
        <div>
          <h3 className="font-semibold text-white">Format Standardization</h3>
          <p className="text-xs text-gray-500">Dates, numbers, text casing</p>
        </div>
      </div>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />

      <div className="mb-4 max-h-56 overflow-y-auto space-y-1.5 scrollbar-thin">
        {columns.map((col) => (
          <div key={col} className="flex flex-wrap items-center gap-2 rounded-xl bg-white/3 border border-white/10 p-2.5">
            <input type="checkbox" id={`fmt-${col}`} checked={!!selectedCols[col]}
              onChange={(e) => setSelectedCols((p) => ({ ...p, [col]: e.target.checked }))}
              aria-label={`Select column ${col} for formatting`}
              className="h-3.5 w-3.5 rounded border-white/20 bg-white/10 text-blue-500 focus:ring-blue-500" />
            <label htmlFor={`fmt-${col}`} className="min-w-[80px] text-xs font-medium text-gray-300">{col}</label>
            <select value={types[col] || 'text'} onChange={(e) => setTypes((p) => ({ ...p, [col]: e.target.value as FormatType }))}
              aria-label={`Format type for ${col}`}
              className="rounded-lg border border-white/10 bg-white/5 px-2 py-1 text-xs text-gray-300 focus:outline-none focus:ring-1 focus:ring-blue-500">
              <option value="text" className="bg-gray-900">Text</option>
              <option value="numeric" className="bg-gray-900">Numeric</option>
              <option value="date" className="bg-gray-900">Date</option>
            </select>
            {types[col] === 'text' && (
              <select value={casings[col] || ''} onChange={(e) => setCasings((p) => ({ ...p, [col]: e.target.value as TextCasing }))}
                aria-label={`Text casing for ${col}`}
                className="rounded-lg border border-white/10 bg-white/5 px-2 py-1 text-xs text-gray-300 focus:outline-none focus:ring-1 focus:ring-blue-500">
                <option value="" className="bg-gray-900">No casing</option>
                <option value="lower" className="bg-gray-900">lowercase</option>
                <option value="upper" className="bg-gray-900">UPPERCASE</option>
                <option value="title" className="bg-gray-900">Title Case</option>
              </select>
            )}
          </div>
        ))}
      </div>

      {loading ? <LoadingSpinner loading size="sm" /> : (
        <button type="button" onClick={handleApply} disabled={applied}
          aria-label="Apply format standardization"
          className="w-full py-2.5 rounded-xl bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 text-blue-300 text-sm font-medium transition-all duration-200 disabled:opacity-40">
          {applied ? '✅ Format Applied' : 'Apply Format'}
        </button>
      )}
    </div>
  );
}
