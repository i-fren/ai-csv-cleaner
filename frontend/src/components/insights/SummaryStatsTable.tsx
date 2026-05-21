import { useState } from 'react';
import type { StatsResponse, NumericColumnStats, TextColumnStats } from '../../types/api';

interface SummaryStatsTableProps { stats: StatsResponse; }

export function SummaryStatsTable({ stats }: SummaryStatsTableProps) {
  const [activeTab, setActiveTab] = useState<'raw' | 'cleaned'>('cleaned');
  const data = activeTab === 'raw' ? stats.raw : stats.cleaned;
  const numericCols = Object.entries(data).filter(([, s]) => s.type === 'numeric');
  const textCols = Object.entries(data).filter(([, s]) => s.type === 'text');

  return (
    <div>
      <div className="flex gap-2 mb-4" role="tablist">
        {(['cleaned', 'raw'] as const).map((tab) => (
          <button key={tab} role="tab" aria-selected={activeTab === tab} onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
              activeTab === tab ? 'bg-blue-600/30 text-blue-300 border border-blue-500/30' : 'bg-white/5 text-gray-400 hover:text-white border border-white/10'
            }`}>
            {tab === 'cleaned' ? '✅ Cleaned' : '📋 Raw'}
          </button>
        ))}
      </div>

      {numericCols.length > 0 && (
        <div className="overflow-x-auto rounded-xl border border-white/10 mb-4 scrollbar-thin">
          <table className="min-w-full text-xs" aria-label="Summary statistics">
            <thead><tr className="bg-white/5">
              {['Column', 'Count', 'Mean', 'Median', 'Std', 'Min', 'Max'].map(h => (
                <th key={h} scope="col" className="px-3 py-2.5 text-left font-semibold text-gray-400 border-b border-white/10">{h}</th>
              ))}
            </tr></thead>
            <tbody>
              {numericCols.map(([col, s]) => {
                const ns = s as NumericColumnStats;
                return (
                  <tr key={col} className="border-b border-white/5 hover:bg-white/3 transition-colors">
                    <td className="px-3 py-2.5 font-medium text-blue-300">{col}</td>
                    <td className="px-3 py-2.5 text-gray-400">{ns.count}</td>
                    <td className="px-3 py-2.5 text-gray-300">{ns.mean.toFixed(2)}</td>
                    <td className="px-3 py-2.5 text-gray-300">{ns.median.toFixed(2)}</td>
                    <td className="px-3 py-2.5 text-gray-400">{ns.std.toFixed(2)}</td>
                    <td className="px-3 py-2.5 text-gray-400">{ns.min.toFixed(2)}</td>
                    <td className="px-3 py-2.5 text-gray-400">{ns.max.toFixed(2)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {textCols.length > 0 && (
        <div className="overflow-x-auto rounded-xl border border-white/10 scrollbar-thin">
          <table className="min-w-full text-xs" aria-label="Text column statistics">
            <thead><tr className="bg-white/5">
              {['Column', 'Count', 'Unique', 'Top Value', 'Frequency'].map(h => (
                <th key={h} scope="col" className="px-3 py-2.5 text-left font-semibold text-gray-400 border-b border-white/10">{h}</th>
              ))}
            </tr></thead>
            <tbody>
              {textCols.map(([col, s]) => {
                const ts = s as TextColumnStats;
                return (
                  <tr key={col} className="border-b border-white/5 hover:bg-white/3 transition-colors">
                    <td className="px-3 py-2.5 font-medium text-purple-300">{col}</td>
                    <td className="px-3 py-2.5 text-gray-400">{ts.count}</td>
                    <td className="px-3 py-2.5 text-gray-300">{ts.unique}</td>
                    <td className="px-3 py-2.5 text-gray-300">{ts.top}</td>
                    <td className="px-3 py-2.5 text-gray-400">{ts.top_freq}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
