import { useState, useRef, DragEvent, ChangeEvent, useCallback } from 'react';
import { uploadCsv } from '../../api/client';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorBanner } from '../shared/ErrorBanner';
import type { UploadResponse } from '../../types/api';

interface UploadZoneProps {
  onUploadSuccess: (response: UploadResponse) => void;
}

export function UploadZone({ onUploadSuccess }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateAndUpload = useCallback(async (file: File) => {
    setError(null);
    if (!file.name.toLowerCase().endsWith('.csv')) {
      setError('Only CSV files are accepted. Please select a .csv file.');
      return;
    }
    if (file.size > 50 * 1024 * 1024) {
      setError('File size exceeds 50 MB limit. Please use a smaller file.');
      return;
    }
    setLoading(true);
    try {
      const response = await uploadCsv(file);
      onUploadSuccess(response);
    } catch (err: unknown) {
      let message = 'Upload failed. Please try again.';
      if (err && typeof err === 'object' && 'response' in err) {
        message = (err as { response: { data: { detail: string } } }).response?.data?.detail || message;
      } else if (err instanceof Error) {
        message = err.message;
      }
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [onUploadSuccess]);

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) validateAndUpload(file);
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) validateAndUpload(file);
    if (inputRef.current) inputRef.current.value = '';
  };

  return (
    <div className="w-full">
      <ErrorBanner message={error} onDismiss={() => setError(null)} />
      <div
        role="region"
        aria-label="CSV file upload area"
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={(e) => { e.preventDefault(); setIsDragging(false); }}
        onDrop={handleDrop}
        className={`flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-16 transition-all duration-300 cursor-pointer ${
          isDragging
            ? 'border-blue-500 bg-blue-500/10 scale-[1.02]'
            : 'border-white/20 bg-white/3 hover:border-blue-500/50 hover:bg-blue-500/5'
        }`}
        onClick={() => inputRef.current?.click()}
      >
        {loading ? (
          <div className="flex flex-col items-center gap-4">
            <LoadingSpinner loading size="lg" />
            <p className="text-gray-400 text-sm">Analyzing your data...</p>
          </div>
        ) : (
          <>
            <div className="text-6xl mb-4 animate-float">📂</div>
            <p className="text-xl font-semibold text-white mb-2">Drop your CSV file here</p>
            <p className="text-gray-500 text-sm mb-6">or click to browse</p>
            <label
              htmlFor="csv-file-input"
              aria-label="Browse to select a CSV file"
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-medium text-sm cursor-pointer transition-all duration-200 shadow-lg shadow-blue-500/25"
              onClick={(e) => e.stopPropagation()}
            >
              Browse Files
              <input
                id="csv-file-input"
                ref={inputRef}
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                aria-label="Select CSV file"
                className="sr-only"
              />
            </label>
            <p className="mt-4 text-xs text-gray-600">Supports CSV files up to 50 MB</p>
          </>
        )}
      </div>
    </div>
  );
}
