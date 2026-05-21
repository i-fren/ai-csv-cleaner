interface DataPreviewTableProps {
  preview: Record<string, unknown>[];
  columns: string[];
}

export function DataPreviewTable({ preview, columns }: DataPreviewTableProps) {
  if (!preview.length) return null;
  return (
    <div className="overflow-x-auto rounded-xl border border-white/10 scrollbar-thin">
      <table className="min-w-full text-sm" aria-label="Data preview">
        <thead>
          <tr className="bg-white/5">
            {columns.map((col) => (
              <th key={col} scope="col" className="whitespace-nowrap px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-400 border-b border-white/10">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {preview.map((row, rowIdx) => (
            <tr key={rowIdx} className="border-b border-white/5 hover:bg-white/3 transition-colors">
              {columns.map((col) => (
                <td key={col} className="whitespace-nowrap px-4 py-2.5 text-gray-300">
                  {row[col] === null || row[col] === undefined || row[col] === ''
                    ? <span className="italic text-gray-600 text-xs">null</span>
                    : String(row[col])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
