import Plot from 'react-plotly.js';

interface ComparisonChartsProps {
  rawRowCount: number;
  cleanedRowCount: number;
  duplicatesRemoved: number;
  missingResolved: number;
  outliersRemoved: number;
}

const darkLayout = {
  paper_bgcolor: 'transparent',
  plot_bgcolor: 'transparent',
  font: { color: '#9ca3af', size: 11 },
  margin: { t: 40, b: 50, l: 50, r: 20 },
};

export function ComparisonCharts({ rawRowCount, cleanedRowCount, duplicatesRemoved, missingResolved, outliersRemoved }: ComparisonChartsProps) {
  const rowsRemoved = rawRowCount - cleanedRowCount;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div className="rounded-2xl bg-white/5 border border-white/10 p-4" aria-label="Bar chart showing cleaning impact">
        <Plot
          data={[{
            type: 'bar',
            x: ['Duplicates', 'Missing Values', 'Outliers', 'Total Removed'],
            y: [duplicatesRemoved, missingResolved, outliersRemoved, rowsRemoved],
            marker: { color: ['#f97316', '#eab308', '#a855f7', '#ef4444'], opacity: 0.85 },
          }]}
          layout={{
            ...darkLayout,
            title: { text: 'Issues Fixed', font: { color: '#e5e7eb', size: 14 } },
            xaxis: { gridcolor: 'rgba(255,255,255,0.05)', tickfont: { color: '#6b7280' } },
            yaxis: { gridcolor: 'rgba(255,255,255,0.05)', tickfont: { color: '#6b7280' } },
          }}
          config={{ responsive: true, displayModeBar: false }}
          style={{ width: '100%', height: '260px' }}
        />
      </div>

      <div className="rounded-2xl bg-white/5 border border-white/10 p-4" aria-label="Pie chart showing rows retained vs removed">
        <Plot
          data={[{
            type: 'pie',
            labels: ['Rows Retained', 'Rows Removed'],
            values: [cleanedRowCount, rowsRemoved],
            marker: { colors: ['#22c55e', '#ef4444'] },
            textinfo: 'label+percent',
            hole: 0.5,
            textfont: { color: '#e5e7eb' },
          }]}
          layout={{
            ...darkLayout,
            title: { text: 'Data Retention', font: { color: '#e5e7eb', size: 14 } },
            showlegend: false,
            margin: { t: 40, b: 20, l: 20, r: 20 },
          }}
          config={{ responsive: true, displayModeBar: false }}
          style={{ width: '100%', height: '260px' }}
        />
      </div>
    </div>
  );
}
