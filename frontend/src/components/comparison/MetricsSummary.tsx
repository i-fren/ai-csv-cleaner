interface MetricsSummaryProps {
  rawRowCount: number;
  cleanedRowCount: number;
  duplicatesRemoved: number;
  missingResolved: number;
  outliersRemoved: number;
  columnsStandardized: number;
}

export function MetricsSummary({ rawRowCount, cleanedRowCount, duplicatesRemoved, missingResolved, outliersRemoved, columnsStandardized }: MetricsSummaryProps) {
  const rowsRemoved = rawRowCount - cleanedRowCount;
  const qualityImprovement = rawRowCount > 0
    ? Math.round(((duplicatesRemoved + missingResolved + outliersRemoved) / rawRowCount) * 100)
    : 0;

  const metrics = [
    { label: 'Rows Removed', value: rowsRemoved, icon: '🗑️', color: 'stat-card-red', textColor: 'text-red-400' },
    { label: 'Duplicates Fixed', value: duplicatesRemoved, icon: '🔁', color: 'stat-card-orange', textColor: 'text-orange-400' },
    { label: 'Missing Fixed', value: missingResolved, icon: '✅', color: 'stat-card-green', textColor: 'text-green-400' },
    { label: 'Outliers Removed', value: outliersRemoved, icon: '📉', color: 'stat-card-purple', textColor: 'text-purple-400' },
    { label: 'Cols Standardized', value: columnsStandardized, icon: '📐', color: 'stat-card-blue', textColor: 'text-blue-400' },
    { label: 'Quality Boost', value: `+${qualityImprovement}%`, icon: '⬆️', color: 'stat-card-cyan', textColor: 'text-cyan-400' },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      {metrics.map((m) => (
        <div key={m.label} className={`rounded-2xl bg-white/5 border border-white/10 p-4 ${m.color}`} aria-label={`${m.label}: ${m.value}`}>
          <div className="text-2xl mb-2">{m.icon}</div>
          <div className={`text-2xl font-bold ${m.textColor}`}>{m.value}</div>
          <div className="text-xs text-gray-500 mt-1">{m.label}</div>
        </div>
      ))}
    </div>
  );
}
