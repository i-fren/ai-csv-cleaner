import { MetricsSummary } from './MetricsSummary';
import { ComparisonCharts } from './ComparisonCharts';

interface ComparisonPanelProps {
  rawRowCount: number;
  cleanedRowCount: number;
  duplicatesRemoved: number;
  missingResolved: number;
  outliersRemoved: number;
  columnsStandardized: number;
}

export function ComparisonPanel(props: ComparisonPanelProps) {
  const totalFixed = props.duplicatesRemoved + props.missingResolved + props.outliersRemoved;
  const qualityScore = props.rawRowCount > 0
    ? Math.max(60, Math.round(100 - (totalFixed / props.rawRowCount) * 100 * 0.5))
    : 100;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white mb-1">📊 Before vs. After</h2>
        <p className="text-gray-400 text-sm">See exactly what DataDoctor AI improved</p>
      </div>

      {/* Quality score banner */}
      <div className="rounded-2xl bg-gradient-to-r from-green-500/10 to-cyan-500/10 border border-green-500/20 p-6 flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-400 mb-1">Data Quality Score</p>
          <p className="text-4xl font-black text-white">{qualityScore}<span className="text-xl text-gray-400">/100</span></p>
          <p className="text-sm text-green-400 mt-1">↑ {totalFixed} issues resolved by DataDoctor AI</p>
        </div>
        <div className="text-6xl">🏆</div>
      </div>

      <div className="rounded-2xl bg-white/5 border border-white/10 p-6">
        <h3 className="text-base font-semibold text-white mb-4">Cleaning Metrics</h3>
        <MetricsSummary {...props} />
      </div>

      <div className="rounded-2xl bg-white/5 border border-white/10 p-6">
        <h3 className="text-base font-semibold text-white mb-4">Visual Comparison</h3>
        <ComparisonCharts
          rawRowCount={props.rawRowCount}
          cleanedRowCount={props.cleanedRowCount}
          duplicatesRemoved={props.duplicatesRemoved}
          missingResolved={props.missingResolved}
          outliersRemoved={props.outliersRemoved}
        />
      </div>
    </div>
  );
}
