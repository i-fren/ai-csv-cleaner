interface ErrorBannerProps {
  message: string | null;
  onDismiss: () => void;
}

export function ErrorBanner({ message, onDismiss }: ErrorBannerProps) {
  if (!message) return null;
  return (
    <div role="alert" aria-label="Error message" className="flex items-start justify-between rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-red-300 mb-4">
      <div className="flex items-start gap-2">
        <span className="text-red-400 mt-0.5">⚠️</span>
        <p className="text-sm">{message}</p>
      </div>
      <button type="button" onClick={onDismiss} aria-label="Dismiss error" className="ml-4 text-red-400 hover:text-red-300 transition-colors">✕</button>
    </div>
  );
}
