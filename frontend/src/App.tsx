import { useState, useRef, useEffect } from 'react';
import { UploadZone } from './components/upload/UploadZone';
import { DataPreviewTable } from './components/upload/DataPreviewTable';
import { CleaningPanel } from './components/cleaning/CleaningPanel';
import { InsightsPanel } from './components/insights/InsightsPanel';
import { ComparisonPanel } from './components/comparison/ComparisonPanel';
import { MLPanel } from './components/ml/MLPanel';
import { exportCsvUrl, exportReportUrl, chatWithData } from './api/client';
import type { UploadResponse } from './types/api';

type Panel = 'home' | 'upload' | 'cleaning' | 'insights' | 'comparison' | 'ml' | 'export' | 'chat';

interface CleaningState {
  duplicatesRemoved: number;
  missingResolved: number;
  outliersRemoved: number;
  columnsStandardized: number;
  currentRowCount: number;
}

interface ChatMessage {
  role: 'user' | 'ai';
  text: string;
  timestamp: Date;
}

const NAV_TABS: { id: Panel; label: string; icon: string }[] = [
  { id: 'upload', label: 'Upload', icon: '📁' },
  { id: 'cleaning', label: 'Clean', icon: '🧹' },
  { id: 'insights', label: 'Insights', icon: '💡' },
  { id: 'comparison', label: 'Compare', icon: '📊' },
  { id: 'ml', label: 'ML Model', icon: '🤖' },
  { id: 'chat', label: 'Chat', icon: '💬' },
  { id: 'export', label: 'Export', icon: '⬇️' },
];

const SUGGESTED_QUESTIONS = [
  'What are the main issues with my data?',
  'Which column has the most missing values?',
  'Summarize this dataset',
  'What trends do you see?',
  'What is my data quality score?',
];

function App() {
  const [activePanel, setActivePanel] = useState<Panel>('home');
  const [uploadResponse, setUploadResponse] = useState<UploadResponse | null>(null);
  const [cleaningState, setCleaningState] = useState<CleaningState>({
    duplicatesRemoved: 0,
    missingResolved: 0,
    outliersRemoved: 0,
    columnsStandardized: 0,
    currentRowCount: 0,
  });
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const sessionId = uploadResponse?.session_id ?? null;

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const handleUploadSuccess = (res: UploadResponse) => {
    setUploadResponse(res);
    setCleaningState((prev) => ({ ...prev, currentRowCount: res.row_count }));
    setActivePanel('cleaning');
  };

  const handleSendChat = async (message?: string) => {
    const msg = message || chatInput.trim();
    if (!msg || !sessionId) return;
    setChatInput('');
    setChatMessages((prev) => [...prev, { role: 'user', text: msg, timestamp: new Date() }]);
    setChatLoading(true);
    try {
      const res = await chatWithData(sessionId, msg);
      setChatMessages((prev) => [...prev, { role: 'ai', text: res.reply, timestamp: new Date() }]);
    } catch {
      setChatMessages((prev) => [...prev, {
        role: 'ai',
        text: 'Sorry, I could not process that request. Please try again.',
        timestamp: new Date(),
      }]);
    } finally {
      setChatLoading(false);
    }
  };

  const dataQualityScore = uploadResponse ? Math.max(60, Math.round(
    100 - (
      (cleaningState.duplicatesRemoved + cleaningState.missingResolved + cleaningState.outliersRemoved) /
      Math.max(uploadResponse.row_count, 1) * 100
    )
  )) : null;

  // ── HOME PAGE ──────────────────────────────────────────────────────────────
  if (activePanel === 'home') {
    return (
      <div className="min-h-screen bg-[#0a0a1a] text-white overflow-hidden">
        {/* Animated background */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl animate-pulse-slow" />
          <div className="absolute top-1/2 -left-40 w-80 h-80 bg-purple-600/20 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
          <div className="absolute bottom-0 right-1/3 w-72 h-72 bg-indigo-600/15 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '2s' }} />
        </div>

        {/* Nav */}
        <nav className="relative z-10 flex items-center justify-between px-8 py-5 border-b border-white/5">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-lg">🩺</div>
            <span className="text-xl font-bold gradient-text">DataDoctor AI</span>
          </div>
          <button
            onClick={() => setActivePanel('upload')}
            className="px-5 py-2 rounded-full bg-white/10 hover:bg-white/20 text-sm font-medium transition-all duration-200 border border-white/10"
          >
            Launch App →
          </button>
        </nav>

        {/* Hero */}
        <div className="relative z-10 max-w-5xl mx-auto px-8 pt-24 pb-16 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-8">
            <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
            AI-Powered Data Cleaning
          </div>

          <h1 className="text-5xl md:text-7xl font-black leading-tight mb-6">
            Turn Messy CSV Files Into{' '}
            <span className="gradient-text">Clean, AI-Ready</span>{' '}
            Data in Seconds
          </h1>

          <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Upload your CSV, let AI detect problems, clean data, generate insights,
            and export a production-ready dataset.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => setActivePanel('upload')}
              className="px-8 py-4 rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold text-lg transition-all duration-200 shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 hover:scale-105"
            >
              🚀 Start Cleaning Now
            </button>
            <button
              onClick={() => setActivePanel('upload')}
              className="px-8 py-4 rounded-2xl bg-white/5 hover:bg-white/10 border border-white/10 text-white font-semibold text-lg transition-all duration-200"
            >
              📂 Upload CSV
            </button>
          </div>
        </div>

        {/* Feature cards */}
        <div className="relative z-10 max-w-6xl mx-auto px-8 pb-24">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { icon: '🧹', title: 'Smart Cleaning', desc: 'Auto-detect duplicates, missing values, outliers, and format inconsistencies with one click.', color: 'from-blue-500/10 to-blue-600/5', border: 'border-blue-500/20' },
              { icon: '💡', title: 'AI Insights', desc: 'Get human-readable analysis of your data quality, trends, correlations, and improvement suggestions.', color: 'from-purple-500/10 to-purple-600/5', border: 'border-purple-500/20' },
              { icon: '💬', title: 'Chat With Data', desc: 'Ask questions in plain English — "What\'s wrong with my data?" or "Which column has issues?"', color: 'from-pink-500/10 to-pink-600/5', border: 'border-pink-500/20' },
              { icon: '📊', title: 'Before vs After', desc: 'Visual comparison dashboard showing exactly what was cleaned and how much quality improved.', color: 'from-cyan-500/10 to-cyan-600/5', border: 'border-cyan-500/20' },
              { icon: '🤖', title: 'ML Ready', desc: 'Train and compare Random Forest models on raw vs cleaned data to prove the value of cleaning.', color: 'from-green-500/10 to-green-600/5', border: 'border-green-500/20' },
              { icon: '⬇️', title: 'Export Everything', desc: 'Download cleaned CSV and a full PDF report with statistics, insights, and model results.', color: 'from-orange-500/10 to-orange-600/5', border: 'border-orange-500/20' },
            ].map((f) => (
              <div key={f.title} className={`rounded-2xl bg-gradient-to-br ${f.color} border ${f.border} p-6 hover:scale-105 transition-transform duration-200`}>
                <div className="text-3xl mb-3">{f.icon}</div>
                <h3 className="text-lg font-bold text-white mb-2">{f.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // ── APP SHELL ──────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-[#0a0a1a] text-white">
      {/* Subtle background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -left-40 w-80 h-80 bg-purple-600/10 rounded-full blur-3xl" />
      </div>

      {/* Header */}
      <header className="relative z-20 border-b border-white/5 bg-[#0a0a1a]/80 backdrop-blur-xl sticky top-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <button onClick={() => setActivePanel('home')} className="flex items-center gap-3 hover:opacity-80 transition-opacity">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-base">🩺</div>
              <span className="text-lg font-bold gradient-text">DataDoctor AI</span>
            </button>

            {uploadResponse && (
              <div className="hidden sm:flex items-center gap-3">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs text-gray-400">
                  <span className="w-2 h-2 rounded-full bg-green-400" />
                  {uploadResponse.filename}
                </div>
                <div className="px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs text-gray-400">
                  {uploadResponse.row_count.toLocaleString()} rows
                </div>
                {dataQualityScore && (
                  <div className={`px-3 py-1.5 rounded-full text-xs font-semibold border ${
                    dataQualityScore >= 80 ? 'bg-green-500/10 border-green-500/30 text-green-400' :
                    dataQualityScore >= 60 ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400' :
                    'bg-red-500/10 border-red-500/30 text-red-400'
                  }`}>
                    Quality: {dataQualityScore}/100
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="relative z-10 border-b border-white/5 bg-[#0a0a1a]/60 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex overflow-x-auto scrollbar-thin gap-1 py-1">
            {NAV_TABS.map((tab) => {
              const isDisabled = tab.id !== 'upload' && !uploadResponse;
              const isActive = activePanel === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => !isDisabled && setActivePanel(tab.id)}
                  disabled={isDisabled}
                  aria-label={`Navigate to ${tab.label}`}
                  className={`flex items-center gap-2 whitespace-nowrap px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-600/30 to-purple-600/30 text-white border border-blue-500/30'
                      : isDisabled
                      ? 'text-gray-600 cursor-not-allowed'
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  <span>{tab.icon}</span>
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">

        {/* ── UPLOAD ── */}
        {activePanel === 'upload' && (
          <div className="space-y-6">
            {/* Stats bar if already uploaded */}
            {uploadResponse && (
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                {[
                  { label: 'Total Rows', value: uploadResponse.row_count.toLocaleString(), icon: '📋', color: 'stat-card-blue' },
                  { label: 'Columns', value: uploadResponse.column_count, icon: '📐', color: 'stat-card-purple' },
                  { label: 'Duplicates', value: uploadResponse.duplicate_count, icon: '🔁', color: 'stat-card-orange' },
                  { label: 'Missing Values', value: Object.values(uploadResponse.missing_value_summary).reduce((s, v) => s + v.count, 0), icon: '❓', color: 'stat-card-red' },
                ].map((s) => (
                  <div key={s.label} className={`rounded-2xl bg-white/5 border border-white/10 p-4 ${s.color}`}>
                    <div className="text-2xl mb-1">{s.icon}</div>
                    <div className="text-2xl font-bold text-white">{s.value}</div>
                    <div className="text-xs text-gray-400 mt-1">{s.label}</div>
                  </div>
                ))}
              </div>
            )}

            <div className="rounded-2xl bg-white/5 border border-white/10 p-6">
              <h2 className="text-xl font-bold text-white mb-2">Upload Your CSV</h2>
              <p className="text-gray-400 text-sm mb-6">Drag & drop or browse — up to 50 MB</p>
              <UploadZone onUploadSuccess={handleUploadSuccess} />
            </div>

            {uploadResponse && (
              <div className="rounded-2xl bg-white/5 border border-white/10 p-6">
                <h3 className="text-base font-semibold text-white mb-4">
                  Data Preview <span className="text-gray-500 font-normal text-sm">(first {Math.min(uploadResponse.row_count, 10)} rows)</span>
                </h3>
                <DataPreviewTable preview={uploadResponse.preview} columns={uploadResponse.columns} />
              </div>
            )}
          </div>
        )}

        {/* ── CLEANING ── */}
        {activePanel === 'cleaning' && uploadResponse && sessionId && (
          <CleaningPanel
            sessionId={sessionId}
            uploadResponse={uploadResponse}
            onCleaningUpdate={setCleaningState}
          />
        )}

        {/* ── INSIGHTS ── */}
        {activePanel === 'insights' && sessionId && (
          <InsightsPanel sessionId={sessionId} />
        )}

        {/* ── COMPARISON ── */}
        {activePanel === 'comparison' && uploadResponse && (
          <ComparisonPanel
            rawRowCount={uploadResponse.row_count}
            cleanedRowCount={cleaningState.currentRowCount || uploadResponse.row_count}
            duplicatesRemoved={cleaningState.duplicatesRemoved}
            missingResolved={cleaningState.missingResolved}
            outliersRemoved={cleaningState.outliersRemoved}
            columnsStandardized={cleaningState.columnsStandardized}
          />
        )}

        {/* ── ML ── */}
        {activePanel === 'ml' && sessionId && uploadResponse && (
          <MLPanel sessionId={sessionId} columns={uploadResponse.columns} />
        )}

        {/* ── CHAT ── */}
        {activePanel === 'chat' && (
          <div className="max-w-3xl mx-auto">
            <div className="rounded-2xl bg-white/5 border border-white/10 overflow-hidden flex flex-col" style={{ height: '70vh' }}>
              {/* Chat header */}
              <div className="px-6 py-4 border-b border-white/10 bg-gradient-to-r from-blue-600/10 to-purple-600/10">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xl">🩺</div>
                  <div>
                    <p className="font-semibold text-white">DataDoctor AI</p>
                    <p className="text-xs text-gray-400">Ask anything about your dataset</p>
                  </div>
                  <div className="ml-auto flex items-center gap-2 text-xs text-green-400">
                    <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                    Online
                  </div>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-thin">
                {chatMessages.length === 0 && (
                  <div className="text-center py-8">
                    <div className="text-5xl mb-4">💬</div>
                    <p className="text-gray-400 mb-6">
                      {sessionId ? 'Ask me anything about your dataset!' : 'Upload a CSV file first to start chatting.'}
                    </p>
                    {sessionId && (
                      <div className="flex flex-wrap gap-2 justify-center">
                        {SUGGESTED_QUESTIONS.map((q) => (
                          <button
                            key={q}
                            onClick={() => handleSendChat(q)}
                            className="px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-sm text-gray-300 hover:bg-white/10 hover:text-white transition-all duration-200"
                          >
                            {q}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {chatMessages.map((msg, i) => (
                  <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    {msg.role === 'ai' && (
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-sm mr-3 flex-shrink-0 mt-1">🩺</div>
                    )}
                    <div className={`max-w-[80%] px-4 py-3 text-sm leading-relaxed ${
                      msg.role === 'user' ? 'chat-bubble-user text-white' : 'chat-bubble-ai text-gray-200'
                    }`}>
                      {msg.text}
                    </div>
                  </div>
                ))}

                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-sm mr-3 flex-shrink-0">🩺</div>
                    <div className="chat-bubble-ai px-4 py-3">
                      <div className="flex gap-1">
                        <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                        <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                        <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                      </div>
                    </div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>

              {/* Input */}
              <div className="px-4 py-4 border-t border-white/10">
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSendChat()}
                    placeholder={sessionId ? 'Ask about your data...' : 'Upload a CSV first...'}
                    disabled={!sessionId || chatLoading}
                    aria-label="Chat message input"
                    className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 disabled:opacity-50 transition-all"
                  />
                  <button
                    onClick={() => handleSendChat()}
                    disabled={!sessionId || !chatInput.trim() || chatLoading}
                    aria-label="Send message"
                    className="px-5 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-medium text-sm transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Send →
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ── EXPORT ── */}
        {activePanel === 'export' && (
          <div className="max-w-2xl mx-auto space-y-6">
            <div className="rounded-2xl bg-white/5 border border-white/10 p-8 text-center">
              <div className="text-5xl mb-4">📦</div>
              <h2 className="text-2xl font-bold text-white mb-2">Export Your Results</h2>
              <p className="text-gray-400 mb-8">Download your cleaned data and full analysis report</p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <a
                  href={sessionId ? exportCsvUrl(sessionId) : '#'}
                  download={`cleaned_${uploadResponse?.filename ?? 'data.csv'}`}
                  aria-label="Download cleaned CSV file"
                  className={`flex flex-col items-center gap-3 p-6 rounded-2xl border transition-all duration-200 ${
                    sessionId
                      ? 'bg-blue-600/10 border-blue-500/30 hover:bg-blue-600/20 hover:scale-105 cursor-pointer'
                      : 'bg-white/5 border-white/10 opacity-40 cursor-not-allowed'
                  }`}
                >
                  <span className="text-4xl">📄</span>
                  <span className="font-semibold text-white">Cleaned CSV</span>
                  <span className="text-xs text-gray-400">Production-ready dataset</span>
                </a>

                <a
                  href={sessionId ? exportReportUrl(sessionId) : '#'}
                  download={`insights_report_${uploadResponse?.filename?.replace('.csv', '.pdf') ?? 'report.pdf'}`}
                  aria-label="Download PDF insights report"
                  className={`flex flex-col items-center gap-3 p-6 rounded-2xl border transition-all duration-200 ${
                    sessionId
                      ? 'bg-purple-600/10 border-purple-500/30 hover:bg-purple-600/20 hover:scale-105 cursor-pointer'
                      : 'bg-white/5 border-white/10 opacity-40 cursor-not-allowed'
                  }`}
                >
                  <span className="text-4xl">📊</span>
                  <span className="font-semibold text-white">PDF Report</span>
                  <span className="text-xs text-gray-400">Stats, insights & ML results</span>
                </a>
              </div>

              {!sessionId && (
                <p className="mt-6 text-sm text-gray-500">Upload a CSV file to enable exports</p>
              )}
            </div>
          </div>
        )}

      </main>
    </div>
  );
}

export default App;
