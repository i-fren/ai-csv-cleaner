import { useState } from 'react';
import { detectOutliers, removeOutliers } from '../../api/client';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorBanner } from '../shared/ErrorBanner';
import type { OutlierDetectResponse, OutlierRemoveResponse } from '../../types/api';

interface OutlierCardProps {
  sessionId: string;
  onRemoved: (result: OutlierRemoveResponse) => void;
}

export function OutlierCard({ sessionId, onRemoved }: OutlierCardProps) {
  const [detecting, setDetecting] = useState(false);
  const [removing, setRemoving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [detected, setDetected] = useState<OutlierDetectResponse | null>(null);
  const [removeResult, setRemoveResult] = useState<OutlierRemoveResponse | null>(null);

  const totalOutliers = detected ? Object.values(detected.outlier_summary).reduce((s, c) => s + c.count, 0) : 0;

  return (
    <div className="rounded-2xl bg-white/5 border border-white/10 p-5">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-xl bg-red-500/20 flex items-center justify-center text-xl">📉</div>
        <div>
          <h3 className="font-semibold text-white">Outlier Detection</h3>
          <p className="text-xs text-gray-500">IQR method on numeric columns</p>
        </div>
      </div>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />

      {detected && (
        <div className="mb-4 rounded-xl bg-white/3 border border-white/10 p-3">
          <p className="text-sm text-gray-300 mb-2">
            Found <strong className="text-red-400">{totalOutliers}</strong> outlier(s) across{' '}
            <strong className="text-white">{Object.keys(detected.outlier_summary).length}</strong> column(s)
          </p>
          {Object.entries(detected.outlier_summary).slice(0, 3).map(([col, info]) => (
            <div key={col} className="flex justify-between text-xs text-gray-500 py-1 border-t border-white/5">
              <span className="text-gray-400">{col}</span>
              <span className="text-red-400">{info.count} outliers</span>
            </div>
          ))}
          {removeResult && <p className="text-xs text-green-400 mt-2">✅ {removeResult.rows_removed} rows removed</p>}
        </div>
      )}

      <div className="flex gap-2">
        {detecting ? <LoadingSpinner loading size="sm" /> : (
          <button type="button" onClick={async () => {
            setError(null); setDetecting(true);
            try { setDetected(await detectOutliers(sessionId)); }
            catch (e: unknown) { setError((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Detection failed.'); }
            finally { setDetecting(false); }
          }} disabled={!!detected} aria-label="Detect outliers"
            className="flex-1 py-2.5 rounded-xl bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 text-red-300 text-sm font-medium transition-all duration-200 disabled:opacity-40">
            {detected ? '✅ Detected' : '🔍 Detect Outliers'}
          </button>
        )}
        {detected && totalOutliers > 0 && !removeResult && (
          removing ? <LoadingSpinner loading size="sm" /> : (
            <button type="button" onClick={async () => {
              setError(null); setRemoving(true);
              try { const r = await removeOutliers(sessionId); setRemoveResult(r); onRemoved(r); }
              catch (e: unknown) { setError((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Removal failed.'); }
              finally { setRemoving(false); }
            }} aria-label="Remove outlier rows"
              className="flex-1 py-2.5 rounded-xl bg-red-600/30 hover:bg-red-600/40 border border-red-500/40 text-red-200 text-sm font-medium transition-all duration-200">
              Remove Outliers
            </button>
          )
        )}
      </div>
    </div>
  );
}
