import { useState } from 'react';
import { DuplicateCard } from './DuplicateCard';
import { MissingValueCard } from './MissingValueCard';
import { FormatCard } from './FormatCard';
import { OutlierCard } from './OutlierCard';
import type {
  UploadResponse,
  DuplicateRemovalResponse,
  MissingValueResponse,
  FormatResponse,
  OutlierRemoveResponse,
} from '../../types/api';

interface CleaningState {
  duplicatesRemoved: number;
  missingResolved: number;
  outliersRemoved: number;
  columnsStandardized: number;
  currentRowCount: number;
}

interface CleaningPanelProps {
  sessionId: string;
  uploadResponse: UploadResponse;
  onCleaningUpdate: (state: CleaningState) => void;
}

export function CleaningPanel({ sessionId, uploadResponse, onCleaningUpdate }: CleaningPanelProps) {
  const [state, setState] = useState<CleaningState>({
    duplicatesRemoved: 0,
    missingResolved: 0,
    outliersRemoved: 0,
    columnsStandardized: 0,
    currentRowCount: uploadResponse.row_count,
  });

  const update = (patch: Partial<CleaningState>) => {
    setState((prev) => {
      const next = { ...prev, ...patch };
      onCleaningUpdate(next);
      return next;
    });
  };

  const totalMissing = Object.values(uploadResponse.missing_value_summary).reduce((s, v) => s + v.count, 0);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white mb-1">🧹 Smart Data Cleaning</h2>
        <p className="text-gray-400 text-sm">AI-powered detection and fixing of data quality issues</p>
      </div>

      {/* Quick stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: 'Duplicates', value: uploadResponse.duplicate_count, icon: '🔁', color: uploadResponse.duplicate_count > 0 ? 'text-orange-400' : 'text-green-400' },
          { label: 'Missing Values', value: totalMissing, icon: '❓', color: totalMissing > 0 ? 'text-yellow-400' : 'text-green-400' },
          { label: 'Columns', value: uploadResponse.column_count, icon: '📐', color: 'text-blue-400' },
          { label: 'Total Rows', value: uploadResponse.row_count.toLocaleString(), icon: '📋', color: 'text-purple-400' },
        ].map((s) => (
          <div key={s.label} className="rounded-xl bg-white/5 border border-white/10 p-4">
            <div className="text-xl mb-1">{s.icon}</div>
            <div className={`text-xl font-bold ${s.color}`}>{s.value}</div>
            <div className="text-xs text-gray-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Cleaning cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <DuplicateCard
          sessionId={sessionId}
          duplicateCount={uploadResponse.duplicate_count}
          onRemoved={(res: DuplicateRemovalResponse) => update({ duplicatesRemoved: res.rows_removed, currentRowCount: res.updated_row_count })}
        />
        <MissingValueCard
          sessionId={sessionId}
          missingSummary={uploadResponse.missing_value_summary}
          onApplied={(res: MissingValueResponse) => update({ missingResolved: res.resolved_count })}
        />
        <FormatCard
          sessionId={sessionId}
          columns={uploadResponse.columns}
          inferredTypes={uploadResponse.inferred_types}
          onApplied={(res: FormatResponse) => update({ columnsStandardized: res.modified_columns.length })}
        />
        <OutlierCard
          sessionId={sessionId}
          onRemoved={(res: OutlierRemoveResponse) => update({ outliersRemoved: res.rows_removed, currentRowCount: res.updated_row_count })}
        />
      </div>
    </div>
  );
}
