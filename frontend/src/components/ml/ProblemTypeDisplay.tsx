import type { DetectProblemTypeResponse } from '../../types/api';

interface ProblemTypeDisplayProps {
  response: DetectProblemTypeResponse;
  onTrain: () => void;
  training: boolean;
}

export function ProblemTypeDisplay({ response, onTrain, training }: ProblemTypeDisplayProps) {
  const isClassification = response.problem_type === 'classification';
  return (
    <div className="rounded-xl border border-blue-500/20 bg-blue-500/10 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xl">{isClassification ? '🏷️' : '📈'}</span>
            <p className="text-sm font-semibold text-white">
              Detected: <span className="text-blue-300 capitalize">{response.problem_type}</span>
            </p>
          </div>
          <p className="text-xs text-gray-400 mb-1">{response.reasoning}</p>
          <p className="text-xs text-gray-500">Unique values in target: {response.unique_value_count}</p>
        </div>
        <button
          type="button"
          onClick={onTrain}
          disabled={training}
          aria-label="Train ML models"
          className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white text-sm font-medium transition-all duration-200 disabled:opacity-50 shadow-lg shadow-blue-500/20"
        >
          {training ? '⏳ Training...' : '🚀 Train Models'}
        </button>
      </div>
    </div>
  );
}
