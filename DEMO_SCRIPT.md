# 🎬 Demo Script — DataDoctor AI

**Duration:** 3–4 minutes  
**Audience:** Judges / Technical reviewers  
**Goal:** Show the full data cleaning → AI insights → ML pipeline in action

---

## Setup Before Demo

1. Start backend: `cd backend && uvicorn app.main:app --reload --port 8000`
2. Start frontend: `cd frontend && npm run dev`
3. Have a sample CSV ready (e.g., a dataset with ~500-1000 rows, some duplicates, missing values, and numeric columns)
4. Open browser to http://localhost:5173

---

## Demo Flow (3–4 minutes)

### 1. Landing Page (15 seconds)

**Show:** The animated landing page with feature cards.

**Say:** "DataDoctor AI is a full-stack application that turns messy CSV files into clean, AI-ready data. It was built entirely with Kiro using spec-driven development — from requirements to design to implementation."

**Action:** Click "Start Cleaning Now"

---

### 2. Upload (30 seconds)

**Show:** Drag-and-drop upload zone.

**Say:** "Upload any CSV file — the system instantly analyzes it, infers column types, counts duplicates and missing values, and shows a preview."

**Action:** Drop a CSV file. Point out:
- Row/column count badges
- Duplicate count
- Missing value count
- Data preview table
- Inferred column types

---

### 3. Cleaning (60 seconds)

**Show:** The cleaning panel with all 4 cards.

**Say:** "The cleaning panel gives you one-click tools for common data quality issues."

**Action — Duplicates:**
- "Here we have X duplicates. One click to remove them."
- Click "Remove Duplicates" → show updated count

**Action — Missing Values:**
- "For missing values, we can ask AI to suggest the best strategy."
- Click "Suggest" on a column → show AI recommendation with rationale
- Apply the strategy → show resolved count

**Action — Outliers:**
- "Outlier detection uses the IQR method on numeric columns."
- Click "Detect Outliers" → show summary with bounds
- Click "Remove Outliers" → show rows removed

---

### 4. AI Insights (30 seconds)

**Show:** Insights panel.

**Say:** "Now let's ask AI to analyze our cleaned data."

**Action:** Click "Generate Insights" → show:
- Natural language summary
- Top correlations table
- Quality suggestions list

**Say:** "The AI identifies patterns, correlations, and remaining quality issues — all in plain English."

---

### 5. Before vs After Comparison (20 seconds)

**Show:** Comparison panel.

**Say:** "The comparison dashboard shows exactly what changed."

**Action:** Point out:
- Metrics summary (rows removed, duplicates, missing resolved, outliers)
- Bar chart comparing raw vs cleaned
- Pie chart showing data retention

---

### 6. ML Model Training (45 seconds)

**Show:** ML panel.

**Say:** "Here's where it gets interesting. We can train ML models on BOTH the raw and cleaned data to prove that cleaning actually improves predictions."

**Action:**
- Select a target column
- Show auto-detected problem type (classification/regression) with reasoning
- Click "Train Models" → show:
  - Side-by-side metrics table (raw vs cleaned)
  - Better model highlighted in green
  - Feature importance chart
  - AI explanation of results

**Say:** "The cleaned model outperforms the raw model — data cleaning directly translates to better ML performance."

---

### 7. Chat with Data (20 seconds)

**Show:** Chat panel.

**Say:** "You can also chat with your data in natural language."

**Action:** Click a suggested question like "What are the main issues with my data?" → show AI response.

---

### 8. Export (15 seconds)

**Show:** Export panel.

**Say:** "Finally, export your cleaned CSV and a comprehensive PDF report with all statistics, insights, and ML results."

**Action:** Click download buttons to show they work.

---

## Key Talking Points

1. **Built with Kiro** — Spec-driven development: requirements → design → tasks → code
2. **Full-stack AI** — Not just a wrapper around GPT; real data processing with Pandas + Scikit-learn
3. **Proves cleaning value** — ML comparison quantifies the impact of data quality
4. **Production-ready** — Proper error handling, type safety, accessibility, responsive design
5. **Works without API key** — Fallback heuristics ensure the app is always functional
6. **Comprehensive** — 14 API endpoints, 20+ React components, PDF report generation

---

## Best Feature Showcase Order

1. 🏠 Landing page (visual impact)
2. 📁 Upload with instant analysis (speed)
3. 🧹 AI-suggested cleaning (intelligence)
4. 🤖 ML raw vs cleaned comparison (unique value prop)
5. 💬 Chat with data (wow factor)
6. ⬇️ PDF report export (completeness)

---

## Backup Plan

If OpenAI API is slow or unavailable:
- The app still works — all cleaning, stats, and ML features use local computation
- AI features fall back to heuristic-based suggestions
- Mention this as a design decision: "graceful degradation"

If the demo CSV is too small for ML:
- Use a dataset with at least 20+ rows and 3+ numeric columns
- The system requires minimum 5 rows for ML training
