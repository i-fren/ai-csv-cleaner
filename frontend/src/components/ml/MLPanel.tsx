import { useState } from 'react';
import { trainModels } from '../../api/client';
import { TargetColumnSelector } from './TargetColumnSelector';
import { ProblemTypeDisplay } from './ProblemTypeDisplay';
import { ModelMetricsTable } from './ModelMetricsTable';
import { FeatureImportanceChart } from './FeatureImportanceChart';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorBanner } from '../shared/ErrorBanner';
import type { DetectProblemTypeResponse, MLResult } from '../../types/api';

interface MLPanelProps {
  sessionId: string;
  columns: string[];
}

export function MLPanel({ sessionId, columns }: MLPanelProps) {
  const [problemTypeResponse, setProblemTypeResponse] = useState<DetectProblemTypeResponse | null>(null);
  const [mlResult, setMlResult] = useState<MLResult | null>(null);
  const [training, setTraining] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTrain = async () => {
    if (!problemTypeResponse) return;
    setError(null);
    setTraining(true);
    try {
      setMlResult(await trainModels(sessionId, problemTypeResponse.target_column, problemTypeResponse.problem_type));
    } catch (err: unknown) {
      setError((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Model training failed.');
    } finally {
      setTraining(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white mb-1">🤖 ML Model Comparison</h2>
        <p className="text-gray-400 text-sm">Train models on raw vs cleaned data to prove the value of cleaning</p>
      </div>
      <ErrorBanner message={error} onDismiss={() => setError(null)} />

      <div className="rounded-2xl bg-white/5 border border-white/10 p-6">
        <h3 className="text-base font-semibold text-white mb-4">Configure Model</h3>
        <TargetColumnSelector sessionId={sessionId} columns={columns} onDetected={setProblemTypeResponse} />
        {problemTypeResponse && !mlResult && (
          <div className="mt-4">
            <ProblemTypeDisplay response={problemTypeResponse} onTrain={handleTrain} training={training} />
          </div>
        )}
        {training && (
          <div className="mt-4 flex items-center gap-3 rounded-xl bg-blue-500/10 border border-blue-500/20 p-4">
            <LoadingSpinner loading size="sm" />
            <p className="text-sm text-blue-300">Training Random Forest on raw and cleaned datasets…</p>
          </div>
        )}
      </div>

      {mlResult && (
        <>
          <div className="rounded-2xl bg-white/5 border border-white/10 p-6">
            <h3 className="text-base font-semibold text-white mb-4">📊 Performance Comparison</h3>
            <ModelMetricsTable result={mlResult} />
          </div>
          <div className="rounded-2xl bg-white/5 border border-white/10 p-6">
            <h3 className="text-base font-semibold text-white mb-4">🎯 Feature Importance</h3>
            <FeatureImportanceChart featureImportance={mlResult.feature_importance} topFeaturesDescription={mlResult.top_features_description} />
          </div>
        </>
      )}
    </div>
  );
}
