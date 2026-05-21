import { useState, useEffect } from 'react';
import { generateInsights, getStats } from '../../api/client';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorBanner } from '../shared/ErrorBanner';
import { SummaryStatsTable } from './SummaryStatsTable';
import type { InsightResult, StatsResponse } from '../../types/api';

interface InsightsPanelProps {
  sessionId: string;
}

export function InsightsPanel({ sessionId }: InsightsPanelProps) {
  const [insights, setInsights] = useState<InsightResult | null>(null);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loadingInsights, setLoadingInsights] = useState(false);
  const [loadingStats, setLoadingStats] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getStats(sessionId).then(setStats).catch(() => {}).finally(() => setLoadingStats(false));
  }, [sessionId]);

  const handleGenerate = async () => {
    setError(null);
    setLoadingInsights(true);
    try {
      setInsights(await generateInsights(sessionId));
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to generate insights.');
    } finally {
      setLoadingInsights(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white mb-1">💡 AI Insights</h2>
        <p className="text-gray-400 text-sm">Human-readable analysis of your dataset</p>
      </div>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />

      {/* Summary Statistics */}
      <div className="rounded-2xl bg-white/5 border border-white/10 p-6">
        <h3 className="text-base font-semibold text-white mb-4">📈 Summary Statistics</h3>
        {loadingStats ? <LoadingSpinner loading size="md" /> : stats ? <SummaryStatsTable stats={stats} /> : <p className="text-gray-500 text-sm">Statistics unavailable.</p>}
      </div>

      {/* AI Insights */}
      <div className="rounded-2xl bg-white/5 border border-white/10 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-semibold text-white">🤖 AI Analysis</h3>
          {!insights && !loadingInsights && (
            <button type="button" onClick={handleGenerate} aria-label="Generate AI insights"
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white text-sm font-medium transition-all duration-200">
              Generate Insights ✨
            </button>
          )}
        </div>

        {loadingInsights && (
          <div className="flex flex-col items-center gap-3 py-8">
            <LoadingSpinner loading size="md" />
            <p className="text-gray-400 text-sm">DataDoctor AI is analyzing your data...</p>
          </div>
        )}

        {insights && (
          <div className="space-y-5">
            {/* Summary */}
            <div className="rounded-xl bg-blue-500/10 border border-blue-500/20 p-4">
              <p className="text-sm text-blue-200 leading-relaxed">{insights.summary}</p>
            </div>

            {/* Temporal trends */}
            {insights.temporal_trends && (
              <div>
                <h4 className="text-sm font-semibold text-gray-300 mb-2">📅 Temporal Trends</h4>
                <p className="text-sm text-gray-400">{insights.temporal_trends}</p>
              </div>
            )}

            {/* Top correlations */}
            {insights.top_correlations.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-gray-300 mb-3">🔗 Top Correlations</h4>
                <div className="space-y-2">
                  {insights.top_correlations.map((c, i) => (
                    <div key={i} className="flex items-center justify-between rounded-xl bg-white/3 border border-white/10 px-4 py-3">
                      <span className="text-sm text-gray-300">
                        <span className="text-white font-medium">{c.col_a}</span>
                        <span className="text-gray-500 mx-2">↔</span>
                        <span className="text-white font-medium">{c.col_b}</span>
                      </span>
                      <span className={`text-sm font-bold ${c.correlation > 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {c.correlation > 0 ? '+' : ''}{c.correlation.toFixed(3)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Quality suggestions */}
            {insights.quality_suggestions.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-gray-300 mb-3">💊 Recommendations</h4>
                <div className="space-y-2">
                  {insights.quality_suggestions.map((s, i) => (
                    <div key={i} className="flex items-start gap-3 rounded-xl bg-purple-500/10 border border-purple-500/20 px-4 py-3">
                      <span className="text-purple-400 mt-0.5 flex-shrink-0">💡</span>
                      <p className="text-sm text-gray-300">{s}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {!insights && !loadingInsights && (
          <div className="text-center py-8">
            <div className="text-4xl mb-3">🔍</div>
            <p className="text-gray-500 text-sm">Click "Generate Insights" to get AI-powered analysis</p>
          </div>
        )}
      </div>
    </div>
  );
}
