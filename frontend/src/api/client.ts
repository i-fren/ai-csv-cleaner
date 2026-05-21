import axios from 'axios';
import type {
  UploadResponse,
  DuplicateRemovalResponse,
  ApplyMissingValueRequest,
  MissingValueResponse,
  SuggestFillStrategyResponse,
  ApplyFormatRequest,
  FormatResponse,
  OutlierDetectResponse,
  OutlierRemoveResponse,
  StatsResponse,
  InsightResult,
  DetectProblemTypeResponse,
  MLResult,
} from '../types/api';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 35000,
});

export async function uploadCsv(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post<UploadResponse>('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
}

export async function removeDuplicates(sessionId: string): Promise<DuplicateRemovalResponse> {
  const response = await api.post<DuplicateRemovalResponse>(
    `/sessions/${sessionId}/clean/duplicates`
  );
  return response.data;
}

export async function applyMissingValueStrategies(
  sessionId: string,
  req: ApplyMissingValueRequest
): Promise<MissingValueResponse> {
  const response = await api.post<MissingValueResponse>(
    `/sessions/${sessionId}/clean/missing-values`,
    req
  );
  return response.data;
}

export async function suggestFillStrategy(
  sessionId: string,
  column: string
): Promise<SuggestFillStrategyResponse> {
  const response = await api.post<SuggestFillStrategyResponse>(
    `/sessions/${sessionId}/clean/missing-values/suggest`,
    { column }
  );
  return response.data;
}

export async function applyFormat(
  sessionId: string,
  req: ApplyFormatRequest
): Promise<FormatResponse> {
  const response = await api.post<FormatResponse>(
    `/sessions/${sessionId}/clean/format`,
    req
  );
  return response.data;
}

export async function detectOutliers(sessionId: string): Promise<OutlierDetectResponse> {
  const response = await api.post<OutlierDetectResponse>(
    `/sessions/${sessionId}/clean/outliers/detect`
  );
  return response.data;
}

export async function removeOutliers(sessionId: string): Promise<OutlierRemoveResponse> {
  const response = await api.post<OutlierRemoveResponse>(
    `/sessions/${sessionId}/clean/outliers/remove`
  );
  return response.data;
}

export async function getStats(sessionId: string): Promise<StatsResponse> {
  const response = await api.get<StatsResponse>(`/sessions/${sessionId}/stats`);
  return response.data;
}

export async function generateInsights(sessionId: string): Promise<InsightResult> {
  const response = await api.post<InsightResult>(`/sessions/${sessionId}/insights`);
  return response.data;
}

export async function detectProblemType(
  sessionId: string,
  targetColumn: string
): Promise<DetectProblemTypeResponse> {
  const response = await api.post<DetectProblemTypeResponse>(
    `/sessions/${sessionId}/ml/detect-problem-type`,
    { target_column: targetColumn }
  );
  return response.data;
}

export async function trainModels(
  sessionId: string,
  targetColumn: string,
  problemType: string
): Promise<MLResult> {
  const response = await api.post<MLResult>(`/sessions/${sessionId}/ml/train`, {
    target_column: targetColumn,
    problem_type: problemType,
  });
  return response.data;
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export function exportCsvUrl(sessionId: string): string {
  return `${BASE_URL}/sessions/${sessionId}/export/csv`;
}

export function exportReportUrl(sessionId: string): string {
  return `${BASE_URL}/sessions/${sessionId}/export/report`;
}

export async function chatWithData(sessionId: string, message: string): Promise<{ reply: string }> {
  const response = await api.post<{ reply: string }>(`/sessions/${sessionId}/chat`, { message });
  return response.data;
}
