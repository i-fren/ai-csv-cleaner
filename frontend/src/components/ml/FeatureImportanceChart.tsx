import Plot from 'react-plotly.js';
import type { FeatureImportanceEntry } from '../../types/api';

interface FeatureImportanceChartProps {
  featureImportance: FeatureImportanceEntry[];
  topFeaturesDescription: string;
}

export function FeatureImportanceChart({ featureImportance, topFeaturesDescription }: FeatureImportanceChartProps) {
  const top10 = featureImportance.slice(0, 10);
  const features = top10.map((f) => f.feature).reverse();
  const scores = top10.map((f) => f.score).reverse();

  return (
    <div>
      <div aria-label="Feature importance chart">
        <Plot
          data={[{
            type: 'bar',
            orientation: 'h',
            x: scores,
            y: features,
            marker: { color: scores.map((_, i) => `rgba(99, 102, 241, ${1 - i * 0.07})`), },
          }]}
          layout={{
            autosize: true,
            margin: { t: 20, b: 40, l: 120, r: 20 },
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            xaxis: { title: 'Importance Score', tickformat: '.3f', gridcolor: 'rgba(255,255,255,0.05)', tickfont: { color: '#6b7280' }, titlefont: { color: '#9ca3af' } },
            yaxis: { tickfont: { color: '#d1d5db' } },
            font: { size: 11, color: '#9ca3af' },
          }}
          config={{ responsive: true, displayModeBar: false }}
          style={{ width: '100%', height: '300px' }}
        />
      </div>
      <div className="mt-3 rounded-xl bg-purple-500/10 border border-purple-500/20 p-4">
        <p className="text-sm text-purple-200">{topFeaturesDescription}</p>
      </div>
    </div>
  );
}
