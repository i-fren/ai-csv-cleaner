interface LoadingSpinnerProps {
  loading?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export function LoadingSpinner({ loading = true, size = 'md' }: LoadingSpinnerProps) {
  if (!loading) return null;
  const sizeClasses = { sm: 'h-4 w-4 border-2', md: 'h-8 w-8 border-2', lg: 'h-12 w-12 border-4' };
  return (
    <div role="status" aria-label="Loading" className="flex items-center justify-center">
      <div className={`${sizeClasses[size]} animate-spin rounded-full border-blue-500 border-t-transparent`} />
      <span className="sr-only">Loading...</span>
    </div>
  );
}
