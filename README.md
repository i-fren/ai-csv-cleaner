# 🩺 DataDoctor AI — AI-Powered CSV Cleaning & Analytics

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/React-18-61DAFB?logo=react" alt="React" />
  <img src="https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/TypeScript-5.4-3178C6?logo=typescript" alt="TypeScript" />
  <img src="https://img.shields.io/badge/TailwindCSS-3.4-06B6D4?logo=tailwindcss" alt="Tailwind" />
  <img src="https://img.shields.io/badge/OpenAI-gpt--4o--mini-412991?logo=openai" alt="OpenAI" />
  <img src="https://img.shields.io/badge/Built_with-Kiro-purple" alt="Kiro" />
</p>

---

## Overview

**DataDoctor AI** is a full-stack web application that transforms messy CSV files into clean, analysis-ready datasets using AI. Upload any CSV, and the system automatically detects data quality issues, applies intelligent cleaning strategies, generates AI-powered insights, trains ML models to prove the value of cleaning, and exports production-ready results.

Built entirely with **Kiro** — an AI-powered development environment — this project demonstrates spec-driven development from requirements through design to implementation.

---

## Features

| Feature | Description |
|---------|-------------|
| 📁 **Smart Upload** | Drag-and-drop CSV upload with instant 10-row preview, type inference, and data quality summary |
| 🧹 **Automated Cleaning** | One-click duplicate removal, AI-suggested missing value strategies, format standardization, IQR outlier detection |
| 💡 **AI Insights** | GPT-4o-mini powered natural language analysis with correlations, trends, and quality suggestions |
| 📊 **Before vs After** | Interactive Plotly charts comparing raw vs cleaned data metrics side-by-side |
| 🤖 **ML Model Training** | Auto-detect classification/regression, train Random Forest on raw vs cleaned, compare performance |
| 💬 **Chat with Data** | Ask questions about your dataset in plain English and get AI-powered answers |
| ⬇️ **Export** | Download cleaned CSV and comprehensive PDF report with stats, insights, and ML results |
| 📱 **Responsive UI** | Dark-themed, mobile-friendly interface with smooth animations and full accessibility |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + TypeScript | Component-based SPA |
| **Styling** | Tailwind CSS 3.4 | Utility-first responsive design |
| **Charts** | Plotly.js + react-plotly.js | Interactive data visualizations |
| **HTTP Client** | Axios | Typed API communication |
| **Build Tool** | Vite 5 | Fast HMR development server |
| **Backend** | Python FastAPI | Async REST API with auto-docs |
| **Data Processing** | Pandas 2.2 + NumPy | Tabular data manipulation |
| **Machine Learning** | Scikit-learn 1.4 | Random Forest training & metrics |
| **AI/LLM** | OpenAI API (gpt-4o-mini) | Insights, suggestions, chat |
| **PDF Generation** | ReportLab | Professional PDF reports |
| **Testing** | Pytest + Hypothesis + Vitest | Property-based & unit testing |
| **Alternative UI** | Streamlit | Standalone analytics dashboard |

---

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- OpenAI API key (optional — app works without it using fallback heuristics)

### Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file (optional for AI features):
```env
OPENAI_API_KEY=your_openai_api_key_here
MAX_FILE_SIZE_MB=50
```

Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API is available at http://localhost:8000  
Interactive API docs: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The app is available at http://localhost:5173

### Streamlit Alternative (Optional)

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

---

## Usage

1. **Upload** — Drag a CSV file onto the upload zone (max 50 MB)
2. **Review** — See instant data preview, column types, duplicate count, and missing values
3. **Clean** — Remove duplicates, handle missing values (with AI suggestions), standardize formats, detect outliers
4. **Analyze** — Generate AI insights, view correlations, get quality suggestions
5. **Compare** — See before/after metrics with interactive charts
6. **Train ML** — Select a target column, auto-detect problem type, train and compare models
7. **Chat** — Ask questions about your data in natural language
8. **Export** — Download cleaned CSV and PDF insights report

---

## Screenshots

> Screenshots can be added to a `/docs/screenshots/` folder

| Screen | Description |
|--------|-------------|
| Home Page | Landing page with feature overview and CTA |
| Upload Panel | Drag-and-drop zone with data preview table |
| Cleaning Panel | Duplicate, missing value, format, and outlier cards |
| Insights Panel | AI-generated summary, correlations, and suggestions |
| Comparison Panel | Before/after metrics with Plotly charts |
| ML Panel | Target selection, problem type, metrics table, feature importance |
| Chat Panel | Conversational AI interface for data questions |
| Export Panel | CSV and PDF download options |

---

## Folder Structure

```
csv-cleaner-app/
├── .kiro/
│   ├── specs/ai-csv-analyzer/     # Kiro spec documents
│   │   ├── requirements.md        # 13 requirements with EARS criteria
│   │   ├── design.md              # Architecture, API design, data models
│   │   └── tasks.md               # Implementation plan with dependencies
│   ├── steering/                   # Development guidelines
│   │   ├── ui-guidelines.md       # UI/UX standards
│   │   ├── coding-standards.md    # Code quality rules
│   │   └── project-rules.md       # Project conventions
│   └── prompts/                    # Reusable AI prompts
│       ├── ui-design.txt           # UI component design prompts
│       ├── export-system.txt       # Export feature prompts
│       ├── analytics.txt           # Analytics/stats prompts
│       └── ai-insights.txt        # AI insights prompts
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI app, CORS, router registration
│   │   ├── config.py              # Environment variables
│   │   ├── errors.py              # Custom error classes
│   │   ├── models/
│   │   │   └── schemas.py         # Pydantic request/response models
│   │   ├── routers/
│   │   │   ├── upload.py          # POST /upload
│   │   │   ├── cleaning.py        # POST /sessions/{id}/clean/*
│   │   │   ├── stats.py           # GET /sessions/{id}/stats
│   │   │   ├── insights.py        # POST /sessions/{id}/insights
│   │   │   ├── ml.py              # POST /sessions/{id}/ml/*
│   │   │   ├── export.py          # GET /sessions/{id}/export/*
│   │   │   └── chat.py            # POST /sessions/{id}/chat
│   │   └── services/
│   │       ├── session_store.py   # In-memory session management
│   │       ├── data_cleaner.py    # Cleaning logic (duplicates, missing, format, outliers)
│   │       ├── stats_engine.py    # Summary statistics & correlations
│   │       ├── ai_engine.py       # OpenAI API integration
│   │       ├── ml_pipeline.py     # Problem detection & model training
│   │       └── pdf_generator.py   # ReportLab PDF assembly
│   ├── tests/
│   │   └── test_properties.py    # Hypothesis property-based tests
│   ├── requirements.txt           # Python dependencies
│   └── pyproject.toml             # Project configuration
├── frontend/
│   ├── src/
│   │   ├── App.tsx                # Root component with routing
│   │   ├── api/client.ts          # Typed API client (all endpoints)
│   │   ├── components/
│   │   │   ├── upload/            # UploadZone, DataPreviewTable
│   │   │   ├── cleaning/         # DuplicateCard, MissingValueCard, FormatCard, OutlierCard
│   │   │   ├── insights/         # InsightsPanel, SummaryStatsTable
│   │   │   ├── comparison/       # ComparisonPanel, MetricsSummary, ComparisonCharts
│   │   │   ├── ml/               # MLPanel, TargetColumnSelector, ModelMetricsTable, FeatureImportanceChart
│   │   │   └── shared/           # LoadingSpinner, ErrorBanner, DownloadButton
│   │   ├── hooks/                 # useApi, useSession
│   │   └── types/api.ts          # TypeScript interfaces
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
├── streamlit_app/                  # Alternative Streamlit UI
│   └── app.py
├── README.md
├── DEVLOG.md
└── AWS_DEPLOYMENT.md
```

---

## Kiro Workflow

This project was built using **Kiro's spec-driven development** workflow:

1. **Requirements** — Defined 13 functional requirements with EARS acceptance criteria covering upload, cleaning, insights, ML, export, and accessibility
2. **Design** — Created a comprehensive architecture document with component diagrams, API contracts, data models, sequence diagrams, and 29 correctness properties
3. **Tasks** — Generated an ordered implementation plan with dependency graph, enabling parallel development of independent components
4. **Implementation** — Kiro autonomously implemented each task, following the spec to produce consistent, well-structured code
5. **Steering** — Used steering files to maintain coding standards, UI guidelines, and project rules throughout development

### How Kiro Accelerated Development

- **Spec-to-code pipeline** — Requirements → Design → Tasks → Code with full traceability
- **Consistent architecture** — Design document ensured all components followed the same patterns
- **Parallel task execution** — Dependency graph enabled efficient implementation ordering
- **Quality guardrails** — Steering files enforced standards across all generated code
- **Rapid iteration** — Changes to specs automatically propagated to implementation

---

## API Documentation

The backend provides interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/upload` | Upload CSV file |
| POST | `/api/v1/sessions/{id}/clean/duplicates` | Remove duplicates |
| POST | `/api/v1/sessions/{id}/clean/missing-values` | Apply fill strategies |
| POST | `/api/v1/sessions/{id}/clean/missing-values/suggest` | AI fill suggestion |
| POST | `/api/v1/sessions/{id}/clean/format` | Standardize formats |
| POST | `/api/v1/sessions/{id}/clean/outliers/detect` | Detect outliers |
| POST | `/api/v1/sessions/{id}/clean/outliers/remove` | Remove outliers |
| GET | `/api/v1/sessions/{id}/stats` | Summary statistics |
| POST | `/api/v1/sessions/{id}/insights` | AI insights |
| POST | `/api/v1/sessions/{id}/ml/detect-problem-type` | Detect ML problem type |
| POST | `/api/v1/sessions/{id}/ml/train` | Train & compare models |
| POST | `/api/v1/sessions/{id}/chat` | Chat with data |
| GET | `/api/v1/sessions/{id}/export/csv` | Download cleaned CSV |
| GET | `/api/v1/sessions/{id}/export/report` | Download PDF report |

---

## Future Improvements

- [ ] Persistent session storage (Redis/PostgreSQL)
- [ ] User authentication and multi-user support
- [ ] Support for Excel, JSON, and Parquet file formats
- [ ] Advanced ML models (XGBoost, LightGBM, neural networks)
- [ ] Automated data profiling with Great Expectations
- [ ] Real-time collaborative editing
- [ ] Scheduled cleaning pipelines
- [ ] Custom cleaning rule builder
- [ ] Data versioning and audit trail
- [ ] Cloud deployment with auto-scaling (AWS/GCP)

---

## Contributors

| Name | Role |
|------|------|
| **Farheen** | Developer — Built with Kiro |

---

## License

This project was built for the Kiro hackathon / educational purposes.
