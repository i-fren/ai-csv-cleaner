import type { MLResult, ClassificationMetrics, RegressionMetrics } from '../../types/api';

interface ModelMetricsTableProps { result: MLResult; }

export function ModelMetricsTable({ result }: ModelMetricsTableProps) {
  const { problem_type, raw_model_metrics, cleaned_model_metrics, better_model } = result;
  const higherIsBetter = ['accuracy', 'precision', 'recall', 'f1', 'r2'];

  const isCleanedBetter = (metric: string) => {
    const raw = (raw_model_metrics as Record<string, number>)[metric];
    const cleaned = (cleaned_model_metrics as Record<string, number>)[metric];
    return higherIsBetter.includes(metric) ? cleaned > raw : cleaned < raw;
  };

  const metrics = problem_type === 'classification'
    ? ['accuracy', 'precision', 'recall', 'f1'] as (keyof ClassificationMetrics)[]
    : ['rmse', 'mae', 'r2'] as (keyof RegressionMetrics)[];

  return (
    <div>
      <div className="flex items-center gap-3 mb-4">
        <span className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-semibold border ${
          better_model === 'cleaned' ? 'bg-green-500/15 border-green-500/30 text-green-400' :
          better_model === 'raw' ? 'bg-orange-500/15 border-orange-500/30 text-orange-400' :
          'bg-gray-500/15 border-gray-500/30 text-gray-400'
        }`}>
          🏆 Better model: {better_model === 'tie' ? 'Tie' : `${better_model.charAt(0).toUpperCase() + better_model.slice(1)} Dataset`}
        </span>
      </div>

      <div className="overflow-x-auto rounded-xl border border-white/10 mb-4">
        <table className="min-w-full text-sm" aria-label="Model performance comparison">
          <thead><tr className="bg-white/5">
            <th scope="col" className="px-4 py-3 text-left font-semibold text-gray-400 border-b border-white/10">Metric</th>
            <th scope="col" className="px-4 py-3 text-left font-semibold text-gray-400 border-b border-white/10">Raw Dataset</th>
            <th scope="col" className="px-4 py-3 text-left font-semibold text-gray-400 border-b border-white/10">Cleaned Dataset</th>
          </tr></thead>
          <tbody>
            {metrics.map((metric) => {
              const rawVal = (raw_model_metrics as Record<string, number>)[metric as string];
              const cleanedVal = (cleaned_model_metrics as Record<string, number>)[metric as string];
              const cleanedWins = isCleanedBetter(metric as string);
              return (
                <tr key={metric} className="border-b border-white/5 hover:bg-white/3 transition-colors">
                  <td className="px-4 py-3 font-medium text-gray-300 uppercase text-xs tracking-wider">{metric}</td>
                  <td className={`px-4 py-3 font-mono text-sm ${!cleanedWins ? 'text-green-400 font-bold' : 'text-gray-500'}`}
                    aria-label={!cleanedWins ? 'Better performing model' : undefined}>
                    {rawVal.toFixed(4)} {!cleanedWins && '🏆'}
                  </td>
                  <td className={`px-4 py-3 font-mono text-sm ${cleanedWins ? 'text-green-400 font-bold' : 'text-gray-500'}`}
                    aria-label={cleanedWins ? 'Better performing model' : undefined}>
                    {cleanedVal.toFixed(4)} {cleanedWins && '🏆'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="rounded-xl bg-blue-500/10 border border-blue-500/20 p-4">
        <p className="text-sm text-blue-200 leading-relaxed">{result.explanation}</p>
      </div>
    </div>
  );
}
