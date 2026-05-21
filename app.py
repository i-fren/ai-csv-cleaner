"""
DataForge AI - AI-Powered Smart CSV Cleaning & Analytics
Built by Farheen with Kiro
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import json
import zipfile

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataForge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── THEME CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
:root {
    --bg: #0F172A;
    --card: #1E293B;
    --cyan: #22D3EE;
    --blue: #60A5FA;
    --text: #F8FAFC;
    --muted: #94a3b8;
    --border: rgba(34,211,238,0.12);
    --glow-cyan: 0 0 20px rgba(34,211,238,0.15);
}
* { font-family: 'Inter', sans-serif; }
.stApp {
    background: var(--bg);
    background-image:
        linear-gradient(rgba(34,211,238,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(34,211,238,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
}
.main .block-container { padding-top: 1rem; max-width: 1350px; }
h1,h2,h3,h4 { color: var(--text) !important; }
p, label, span, li { color: var(--muted); }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A, #1E293B);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h3 { color: var(--cyan) !important; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 700; }
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.5px; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid rgba(34,211,238,0.08); }
.stTabs [data-baseweb="tab"] {
    background: transparent; color: var(--muted); border-radius: 8px 8px 0 0;
    padding: 10px 18px; font-weight: 500; transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--cyan); }
.stTabs [aria-selected="true"] {
    background: rgba(34,211,238,0.08) !important; color: var(--cyan) !important;
    border-bottom: 2px solid var(--cyan) !important; box-shadow: var(--glow-cyan);
}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, rgba(34,211,238,0.12), rgba(96,165,250,0.12)) !important;
    color: var(--cyan) !important; border: 1px solid rgba(34,211,238,0.25) !important;
    border-radius: 10px !important; font-weight: 600 !important; transition: all 0.3s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(135deg, rgba(34,211,238,0.2), rgba(96,165,250,0.2)) !important;
    box-shadow: var(--glow-cyan) !important; border-color: var(--cyan) !important;
}
[data-testid="stFileUploader"] { border: 1px dashed rgba(34,211,238,0.25) !important; border-radius: 12px; }
[data-testid="stDataFrame"] { border: 1px solid rgba(34,211,238,0.1); border-radius: 12px; overflow: hidden; }
.glass-card {
    background: var(--card); border: 1px solid var(--border); border-radius: 16px;
    padding: 24px; backdrop-filter: blur(8px);
}
.insight-card {
    background: rgba(34,211,238,0.04); border: 1px solid rgba(34,211,238,0.1);
    border-radius: 12px; padding: 16px; margin-bottom: 10px; color: #cbd5e1;
}
.insight-card strong { color: var(--text); }
.hero-box {
    background: linear-gradient(135deg, rgba(34,211,238,0.06), rgba(96,165,250,0.08));
    border: 1px solid rgba(34,211,238,0.15); border-radius: 24px; padding: 56px 32px; text-align: center;
}
.hero-title {
    font-size: 3rem; font-weight: 900;
    background: linear-gradient(135deg, #22D3EE, #60A5FA, #22D3EE);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-badge {
    display: inline-block; background: rgba(34,211,238,0.1); border: 1px solid rgba(34,211,238,0.3);
    border-radius: 20px; padding: 6px 16px; font-size: 0.75rem; color: var(--cyan); font-weight: 600;
}
.stat-glow {
    background: linear-gradient(145deg, var(--card), rgba(34,211,238,0.03));
    border: 1px solid var(--border); border-radius: 18px; padding: 24px 16px; text-align: center;
}
.stat-glow .icon { font-size: 1.8rem; margin-bottom: 4px; }
.stat-glow .num { font-size: 2.2rem; font-weight: 800; color: var(--cyan); margin: 4px 0; }
.stat-glow .lbl { font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.feat-card {
    background: var(--card); border: 1px solid var(--border); border-radius: 16px;
    padding: 24px; text-align: center; transition: all 0.3s ease;
}
.feat-card:hover { border-color: rgba(34,211,238,0.3); box-shadow: var(--glow-cyan); }
.feat-card h4 { color: var(--cyan) !important; margin: 8px 0 4px; }
.divider { border: none; border-top: 1px solid rgba(34,211,238,0.08); margin: 1.5rem 0; }
.footer-bar {
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 999;
    background: rgba(15,23,42,0.9); backdrop-filter: blur(12px);
    border-top: 1px solid rgba(34,211,238,0.12); padding: 10px 0; text-align: center;
}
.footer-bar p { margin: 0; font-size: 0.78rem; color: #64748b; }
.footer-bar .cy { color: var(--cyan); }
.footer-bar .bl { color: var(--blue); }
@media (max-width: 768px) {
    .main .block-container { padding: 0.5rem 0.8rem !important; }
    .hero-box { padding: 28px 16px !important; }
    .hero-title { font-size: 1.8rem !important; }
    .stat-glow { padding: 14px 8px !important; }
    .stat-glow .num { font-size: 1.4rem !important; }
    .feat-card { padding: 16px !important; }
    .stTabs [data-baseweb="tab"] { padding: 8px 10px !important; font-size: 0.75rem !important; }
}
@media (pointer: coarse) {
    .stButton > button, .stDownloadButton > button { min-height: 48px !important; }
}
</style>
""", unsafe_allow_html=True)


# ─── HELPER FUNCTIONS ────────────────────────────────────────────────────────

def detect_outliers_iqr(df):
    """Detect outliers using IQR method on numeric columns."""
    info = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        s = df[col].dropna()
        if len(s) < 4:
            continue
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        count = int(((s < lo) | (s > hi)).sum())
        if count > 0:
            info[col] = {"count": count, "lower_bound": round(float(lo), 2), "upper_bound": round(float(hi), 2)}
    return info


def quality_score(cleaned_df, raw_df):
    """Calculate data quality score (0-100)."""
    total_cells = raw_df.shape[0] * raw_df.shape[1]
    if total_cells == 0:
        return 100
    issues = (
        int(raw_df.duplicated().sum()) * raw_df.shape[1]
        + int(raw_df.isna().sum().sum())
        + sum(v["count"] for v in detect_outliers_iqr(raw_df).values())
    )
    return max(0, min(100, int(100 - (issues / total_cells) * 100)))


def to_excel_multi(raw_df, cleaned_df, insights_text):
    """Create Excel with 3 sheets: Original, Cleaned, AI Insights."""
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        raw_df.to_excel(writer, index=False, sheet_name="Original Data")
        cleaned_df.to_excel(writer, index=False, sheet_name="Cleaned Data")
        # Insights sheet
        insights_df = pd.DataFrame({"Insight": insights_text})
        insights_df.to_excel(writer, index=False, sheet_name="AI Insights")
    return buf.getvalue()


def to_excel_single(df, sheet_name="Data"):
    """Create single-sheet Excel file."""
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return buf.getvalue()


def make_txt_report(raw_df, cleaned_df, log, fname):
    """Generate plain text report."""
    lines = [
        "=" * 60,
        "  DataForge AI - Analytics Report",
        "=" * 60,
        f"\nFile: {fname}",
        f"Generated by DataForge AI (Built by Farheen with Kiro)\n",
        "-" * 40,
        "DATA QUALITY SUMMARY",
        "-" * 40,
        f"  Original Rows:      {len(raw_df):,}",
        f"  Cleaned Rows:       {len(cleaned_df):,}",
        f"  Rows Removed:       {len(raw_df) - len(cleaned_df):,}",
        f"  Duplicates Fixed:   {log.get('duplicates_removed', 0)}",
        f"  Missing Fixed:      {log.get('missing_resolved', 0)}",
        f"  Outliers Removed:   {log.get('outliers_removed', 0)}",
        f"  Quality Score:      {quality_score(cleaned_df, raw_df)}/100",
        "",
        "-" * 40,
        "COLUMN INFORMATION",
        "-" * 40,
    ]
    for col in cleaned_df.columns:
        dtype = str(cleaned_df[col].dtype)
        missing = int(cleaned_df[col].isna().sum())
        lines.append(f"  {col}: {dtype} (missing: {missing})")
    lines.append("")
    lines.append("-" * 40)
    lines.append("NUMERIC STATISTICS")
    lines.append("-" * 40)
    num_cols = cleaned_df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        s = cleaned_df[col].dropna()
        if len(s) > 0:
            lines.append(f"  {col}: mean={s.mean():.2f}, median={s.median():.2f}, std={s.std():.2f}")
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def make_pdf(raw_df, cleaned_df, log, fname):
    """Generate PDF report using ReportLab."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("DataForge AI - Analytics Report", styles["Title"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"File: {fname}", styles["Normal"]))
        story.append(Paragraph("Built by Farheen with Kiro", styles["Normal"]))
        story.append(Spacer(1, 20))

        data = [
            ["Metric", "Value"],
            ["Original Rows", f"{len(raw_df):,}"],
            ["Cleaned Rows", f"{len(cleaned_df):,}"],
            ["Rows Removed", f"{len(raw_df) - len(cleaned_df):,}"],
            ["Duplicates Fixed", str(log.get("duplicates_removed", 0))],
            ["Missing Fixed", str(log.get("missing_resolved", 0))],
            ["Outliers Removed", str(log.get("outliers_removed", 0))],
            ["Quality Score", f"{quality_score(cleaned_df, raw_df)}/100"],
        ]
        t = Table(data, colWidths=[8*cm, 5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0ea5e9")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f9ff")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))

        # Column stats
        story.append(Paragraph("Column Statistics", styles["Heading2"]))
        story.append(Spacer(1, 8))
        col_data = [["Column", "Type", "Non-Null", "Missing"]]
        for col in cleaned_df.columns:
            col_data.append([
                col,
                str(cleaned_df[col].dtype),
                str(int(cleaned_df[col].count())),
                str(int(cleaned_df[col].isna().sum())),
            ])
        t2 = Table(col_data)
        t2.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7c3aed")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#faf5ff")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t2)

        doc.build(story)
        return buf.getvalue()
    except Exception as e:
        # Fallback: return text report as bytes if reportlab fails
        return make_txt_report(raw_df, cleaned_df, log, fname).encode("utf-8")


def make_zip(raw_df, cleaned_df, log, fname, insights_text):
    """Create ZIP with all export formats."""
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("original_data.csv", raw_df.to_csv(index=False))
        zf.writestr("cleaned_data.csv", cleaned_df.to_csv(index=False))
        zf.writestr("cleaned_data.xlsx", to_excel_single(cleaned_df, "Cleaned Data"))
        zf.writestr("full_report.xlsx", to_excel_multi(raw_df, cleaned_df, insights_text))
        zf.writestr("report.json", json.dumps({
            "file": fname,
            "rows_before": len(raw_df),
            "rows_after": len(cleaned_df),
            "rows_removed": len(raw_df) - len(cleaned_df),
            "duplicates_removed": log.get("duplicates_removed", 0),
            "missing_fixed": log.get("missing_resolved", 0),
            "outliers_removed": log.get("outliers_removed", 0),
            "quality_score": quality_score(cleaned_df, raw_df),
            "columns": list(cleaned_df.columns),
        }, indent=2))
        zf.writestr("report.txt", make_txt_report(raw_df, cleaned_df, log, fname))
        zf.writestr("report.pdf", make_pdf(raw_df, cleaned_df, log, fname))
    return buf.getvalue()


def generate_insights(df, raw_df, log):
    """Generate AI insights about the dataset."""
    insights = []
    rows_removed = len(raw_df) - len(df)

    # Summary
    insights.append(("📊 Dataset Summary",
        f"**{len(df):,} rows** x **{len(df.columns)} columns** after cleaning. "
        + (f"Removed **{rows_removed:,}** problematic rows." if rows_removed > 0 else "No rows removed.")))

    # Duplicates
    dup_count = int(raw_df.duplicated().sum())
    if dup_count > 0:
        fixed = log.get("duplicates_removed", 0)
        insights.append(("🔁 Duplicate Analysis",
            f"Found **{dup_count:,}** duplicate rows in original data. "
            + (f"✅ All removed." if fixed >= dup_count else f"⚠️ {dup_count - fixed} still pending.")))
    else:
        insights.append(("🔁 Duplicate Analysis", "✅ No duplicate rows detected."))

    # Missing values
    total_missing = int(raw_df.isna().sum().sum())
    if total_missing > 0:
        worst_col = raw_df.isna().sum().idxmax()
        worst_count = int(raw_df[worst_col].isna().sum())
        worst_pct = round(worst_count / len(raw_df) * 100, 1)
        cols_with_missing = int((raw_df.isna().sum() > 0).sum())
        insights.append(("❓ Missing Data Analysis",
            f"**{total_missing:,}** missing values across **{cols_with_missing}** columns. "
            f"Worst: `{worst_col}` with {worst_count} missing ({worst_pct}%)."))
    else:
        insights.append(("❓ Missing Data Analysis", "✅ No missing values detected."))

    # Outliers
    outliers = detect_outliers_iqr(raw_df)
    if outliers:
        total_outliers = sum(v["count"] for v in outliers.values())
        worst_outlier_col = max(outliers, key=lambda k: outliers[k]["count"])
        insights.append(("📉 Outlier Detection",
            f"**{total_outliers}** outliers across **{len(outliers)}** columns (IQR method). "
            f"Most affected: `{worst_outlier_col}` ({outliers[worst_outlier_col]['count']} outliers)."))
    else:
        insights.append(("📉 Outlier Detection", "✅ No significant outliers detected."))

    # Correlations
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) >= 2:
        corr = df[num_cols].corr().abs()
        arr = corr.to_numpy(copy=True)
        np.fill_diagonal(arr, 0)
        max_corr = float(arr.max())
        if max_corr > 0.5:
            idx = np.unravel_index(arr.argmax(), arr.shape)
            col_a, col_b = num_cols[idx[0]], num_cols[idx[1]]
            strength = "strongly" if max_corr > 0.7 else "moderately"
            insights.append(("🔗 Key Correlation",
                f"`{col_a}` and `{col_b}` are **{strength} correlated** (r={max_corr:.3f}). "
                "Consider if one can be derived from the other."))

    # Data types
    num_count = len(df.select_dtypes(include=[np.number]).columns)
    text_count = len(df.select_dtypes(include=["object"]).columns)
    insights.append(("🏷️ Data Types",
        f"**{num_count}** numeric columns, **{text_count}** text/categorical columns."))

    # Recommendations
    recs = []
    if total_missing > 0 and log.get("missing_resolved", 0) == 0:
        recs.append("Handle missing values using median (numeric) or mode (categorical)")
    if dup_count > 0 and log.get("duplicates_removed", 0) == 0:
        recs.append("Remove duplicate rows to avoid bias")
    if outliers and log.get("outliers_removed", 0) == 0:
        recs.append("Review outliers - they may be data entry errors")
    if len(recs) > 0:
        insights.append(("💡 Recommendations", " | ".join([f"• {r}" for r in recs])))

    # Quality score
    qs = quality_score(df, raw_df)
    emoji = "🟢" if qs >= 80 else "🟡" if qs >= 60 else "🔴"
    insights.append(("⭐ Quality Score", f"{emoji} **{qs}/100** — "
        + ("Excellent!" if qs >= 80 else "Good, some issues remain." if qs >= 60 else "Needs more cleaning.")))

    return insights


# Plotly layout defaults
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#94a3b8",
    font_size=11,
    margin=dict(t=40, b=40, l=40, r=20),
)


# ─── SESSION STATE ───────────────────────────────────────────────────────────
if "raw_df" not in st.session_state:
    st.session_state.raw_df = None
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None
if "cleaning_log" not in st.session_state:
    st.session_state.cleaning_log = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "fn" not in st.session_state:
    st.session_state.fn = ""


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ DataForge AI")
    st.caption("Smart CSV Cleaning & Analytics")
    st.markdown("---")

    uploaded_file = st.file_uploader("📂 Upload CSV", type=["csv"], help="Max 50 MB")

    if uploaded_file:
        # Only re-read if new file
        if st.session_state.raw_df is None or uploaded_file.name != st.session_state.fn:
            try:
                df = pd.read_csv(uploaded_file)
                if len(df) == 0:
                    st.error("Empty file.")
                else:
                    st.session_state.raw_df = df.copy(deep=True)
                    st.session_state.cleaned_df = df.copy(deep=True)
                    st.session_state.fn = uploaded_file.name
                    st.session_state.cleaning_log = {}
                    st.session_state.chat_history = []
                    st.success(f"✅ Loaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error reading file: {e}")

        if st.session_state.raw_df is not None:
            st.markdown("---")
            raw = st.session_state.raw_df
            st.markdown(f"📋 **{len(raw):,}** rows • **{len(raw.columns)}** cols")
            st.markdown(f"🔁 **{int(raw.duplicated().sum())}** duplicates")
            st.markdown(f"❓ **{int(raw.isna().sum().sum())}** missing values")

    st.markdown("---")
    st.caption("Built by Farheen with Kiro")


# ─── MAIN CONTENT ────────────────────────────────────────────────────────────

if st.session_state.raw_df is None:
    # ── LANDING PAGE ──
    st.markdown("""
    <div class="hero-box">
        <div class="hero-badge">⚡ AI POWERED</div>
        <div class="hero-title">DataForge AI</div>
        <p style="color: #94a3b8; font-size: 1.2rem; margin-top: 8px;">
            Next-Gen Smart CSV Cleaning & Analytics Platform
        </p>
        <div style="display:flex; gap:8px; flex-wrap:wrap; justify-content:center; margin-top:20px;">
            <span class="hero-badge">🧹 Clean Data</span>
            <span class="hero-badge">💡 AI Insights</span>
            <span class="hero-badge">📊 Analytics</span>
            <span class="hero-badge">💬 Chat</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown('<div class="stat-glow"><div class="icon">📁</div><div class="num">0</div><div class="lbl">Files</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-glow"><div class="icon">⭐</div><div class="num">—</div><div class="lbl">Quality</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-glow"><div class="icon">📊</div><div class="num">0</div><div class="lbl">Rows</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown('<div class="stat-glow"><div class="icon">💡</div><div class="num">0</div><div class="lbl">Insights</div></div>', unsafe_allow_html=True)

    st.markdown("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feat-card"><div style="font-size:2.5rem">🧹</div><h4>Smart Cleaning</h4><p style="font-size:0.85rem">Duplicates • Nulls • Outliers</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feat-card"><div style="font-size:2.5rem">💡</div><h4>AI Insights</h4><p style="font-size:0.85rem">Patterns • Correlations • Score</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feat-card"><div style="font-size:2.5rem">⬇️</div><h4>Multi-Export</h4><p style="font-size:0.85rem">CSV • Excel • PDF • JSON • TXT</p></div>', unsafe_allow_html=True)

    st.markdown("")
    st.info("👈 Upload a CSV file in the sidebar to get started!")

else:
    # ── APP TABS ──
    raw_df = st.session_state.raw_df
    cleaned_df = st.session_state.cleaned_df

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 Preview", "🧹 Clean", "💡 Insights", "📊 Compare", "📈 Visuals", "💬 Chat", "⬇️ Export"
    ])


    # ── TAB 1: PREVIEW ──
    with tab1:
        st.subheader("Data Preview")
        st.dataframe(cleaned_df.head(20), use_container_width=True, height=400)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", f"{len(cleaned_df):,}")
        c2.metric("Columns", len(cleaned_df.columns))
        c3.metric("Duplicates", int(cleaned_df.duplicated().sum()))
        c4.metric("Missing", int(cleaned_df.isna().sum().sum()))

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### Column Info")
        col_info = pd.DataFrame({
            "Column": cleaned_df.columns,
            "Type": [str(cleaned_df[c].dtype) for c in cleaned_df.columns],
            "Non-Null": [int(cleaned_df[c].count()) for c in cleaned_df.columns],
            "Missing": [int(cleaned_df[c].isna().sum()) for c in cleaned_df.columns],
            "Unique": [int(cleaned_df[c].nunique()) for c in cleaned_df.columns],
        })
        st.dataframe(col_info, use_container_width=True, hide_index=True)

    # ── TAB 2: CLEAN ──
    with tab2:
        st.subheader("🧹 Smart Cleaning")

        # Duplicates
        st.markdown("#### 🔁 Duplicates")
        dup_count = int(cleaned_df.duplicated().sum())
        if dup_count > 0:
            st.warning(f"**{dup_count}** duplicate rows found.")
            if st.button("Remove Duplicates", key="btn_remove_dups"):
                before = len(st.session_state.cleaned_df)
                st.session_state.cleaned_df = st.session_state.cleaned_df.drop_duplicates(keep="first").reset_index(drop=True)
                removed = before - len(st.session_state.cleaned_df)
                st.session_state.cleaning_log["duplicates_removed"] = (
                    st.session_state.cleaning_log.get("duplicates_removed", 0) + removed
                )
                st.success(f"✅ Removed {removed} duplicate rows!")
                st.rerun()
        else:
            st.success("✅ No duplicates found.")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Missing Values
        st.markdown("#### ❓ Missing Values")
        missing_series = cleaned_df.isna().sum()
        cols_with_missing = missing_series[missing_series > 0]

        if len(cols_with_missing) > 0:
            total_missing = int(cols_with_missing.sum())
            st.warning(f"**{total_missing}** missing values in **{len(cols_with_missing)}** columns.")

            # Show which columns have missing
            missing_info = pd.DataFrame({
                "Column": cols_with_missing.index,
                "Missing": cols_with_missing.values,
                "% Missing": [round(v / len(cleaned_df) * 100, 1) for v in cols_with_missing.values],
            })
            st.dataframe(missing_info, use_container_width=True, hide_index=True)

            strategy = st.selectbox(
                "Fill Strategy:",
                ["median (numeric) / mode (text)", "mean (numeric) / mode (text)", "forward fill", "drop rows with missing"],
                key="missing_strategy",
            )

            if st.button("Apply Fix", key="btn_fix_missing"):
                df_fixed = st.session_state.cleaned_df.copy(deep=True)
                resolved = 0

                for col in cols_with_missing.index:
                    before_missing = int(df_fixed[col].isna().sum())

                    if "median" in strategy:
                        if pd.api.types.is_numeric_dtype(df_fixed[col]):
                            df_fixed[col] = df_fixed[col].fillna(df_fixed[col].median())
                        else:
                            mode_val = df_fixed[col].mode()
                            if not mode_val.empty:
                                df_fixed[col] = df_fixed[col].fillna(mode_val.iloc[0])
                    elif "mean" in strategy:
                        if pd.api.types.is_numeric_dtype(df_fixed[col]):
                            df_fixed[col] = df_fixed[col].fillna(df_fixed[col].mean())
                        else:
                            mode_val = df_fixed[col].mode()
                            if not mode_val.empty:
                                df_fixed[col] = df_fixed[col].fillna(mode_val.iloc[0])
                    elif "forward" in strategy:
                        df_fixed[col] = df_fixed[col].ffill()
                    elif "drop" in strategy:
                        df_fixed = df_fixed.dropna(subset=[col])

                    after_missing = int(df_fixed[col].isna().sum()) if col in df_fixed.columns else 0
                    resolved += before_missing - after_missing

                st.session_state.cleaned_df = df_fixed.reset_index(drop=True)
                st.session_state.cleaning_log["missing_resolved"] = (
                    st.session_state.cleaning_log.get("missing_resolved", 0) + resolved
                )
                st.success(f"✅ Fixed {resolved} missing values!")
                st.rerun()
        else:
            st.success("✅ No missing values.")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Outliers
        st.markdown("#### 📉 Outliers")
        outliers = detect_outliers_iqr(cleaned_df)
        if outliers:
            total_outliers = sum(v["count"] for v in outliers.values())
            st.warning(f"**{total_outliers}** outliers detected in **{len(outliers)}** columns.")
            outlier_df = pd.DataFrame([
                {"Column": c, "Count": v["count"], "Lower Bound": v["lower_bound"], "Upper Bound": v["upper_bound"]}
                for c, v in outliers.items()
            ])
            st.dataframe(outlier_df, use_container_width=True, hide_index=True)

            if st.button("Remove Outliers", key="btn_remove_outliers"):
                df_clean = st.session_state.cleaned_df.copy(deep=True)
                mask = pd.Series([False] * len(df_clean), index=df_clean.index)
                for col, vals in outliers.items():
                    mask = mask | (df_clean[col] < vals["lower_bound"]) | (df_clean[col] > vals["upper_bound"])
                removed = int(mask.sum())
                st.session_state.cleaned_df = df_clean[~mask].reset_index(drop=True)
                st.session_state.cleaning_log["outliers_removed"] = (
                    st.session_state.cleaning_log.get("outliers_removed", 0) + removed
                )
                st.success(f"✅ Removed {removed} outlier rows!")
                st.rerun()
        else:
            st.success("✅ No significant outliers detected.")

        # Cleaning Summary
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### 📋 Cleaning Summary")
        log = st.session_state.cleaning_log
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Rows Before", f"{len(raw_df):,}")
        s2.metric("Rows After", f"{len(cleaned_df):,}")
        s3.metric("Total Removed", f"{len(raw_df) - len(cleaned_df):,}")
        s4.metric("Quality", f"{quality_score(cleaned_df, raw_df)}/100")


    # ── TAB 3: INSIGHTS ──
    with tab3:
        st.subheader("💡 AI Insights")
        insights = generate_insights(cleaned_df, raw_df, st.session_state.cleaning_log)
        for title, text in insights:
            st.markdown(f'<div class="insight-card"><strong>{title}</strong><br>{text}</div>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### 📈 Descriptive Statistics")
        st.dataframe(cleaned_df.describe().round(2), use_container_width=True)

        # Correlation heatmap
        num_cols = cleaned_df.select_dtypes(include=[np.number]).columns
        if len(num_cols) >= 2:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("#### 🔗 Correlation Matrix")
            fig = px.imshow(
                cleaned_df[num_cols].corr(),
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                aspect="auto",
            )
            fig.update_layout(**PLOT_LAYOUT, title="Pearson Correlations")
            st.plotly_chart(fig, use_container_width=True)

    # ── TAB 4: COMPARE ──
    with tab4:
        st.subheader("📊 Before vs After Comparison")

        dr = st.session_state.cleaning_log.get("duplicates_removed", 0)
        mf = st.session_state.cleaning_log.get("missing_resolved", 0)
        orr = st.session_state.cleaning_log.get("outliers_removed", 0)
        rows_removed = len(raw_df) - len(cleaned_df)
        qs = quality_score(cleaned_df, raw_df)

        # Quality score card
        emoji = "🟢" if qs >= 80 else "🟡" if qs >= 60 else "🔴"
        st.markdown(f'''
        <div class="glass-card" style="text-align:center">
            <p style="color:var(--muted);margin:0;font-size:0.85rem">Data Quality Score</p>
            <p style="font-size:3rem;font-weight:900;color:var(--cyan);margin:4px 0">{emoji} {qs}/100</p>
            <p style="color:var(--cyan);margin:0;font-size:0.85rem">↑ {dr + mf + orr} issues fixed</p>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown("")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Rows Before", f"{len(raw_df):,}")
        m2.metric("Rows After", f"{len(cleaned_df):,}", delta=f"-{rows_removed}" if rows_removed > 0 else "0")
        m3.metric("Dups Fixed", dr)
        m4.metric("Missing Fixed", mf)
        m5.metric("Outliers Fixed", orr)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Side-by-side data preview
        st.markdown("#### 📋 Side-by-Side Preview")
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("**🔴 Original Data**")
            st.dataframe(raw_df.head(10), use_container_width=True, height=300)
        with col_right:
            st.markdown("**🟢 Cleaned Data**")
            st.dataframe(cleaned_df.head(10), use_container_width=True, height=300)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Charts
        # Missing values comparison
        raw_missing = raw_df.isna().sum()
        clean_missing = cleaned_df.isna().sum()
        cols_had_missing = raw_missing[raw_missing > 0].index.tolist()

        if cols_had_missing:
            st.markdown("#### ❓ Missing Values: Before vs After")
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Original", x=cols_had_missing,
                y=[int(raw_missing[c]) for c in cols_had_missing],
                marker_color="#60A5FA", opacity=0.8,
            ))
            fig.add_trace(go.Bar(
                name="Cleaned", x=cols_had_missing,
                y=[int(clean_missing.get(c, 0)) for c in cols_had_missing],
                marker_color="#22D3EE", opacity=0.8,
            ))
            fig.update_layout(**PLOT_LAYOUT, barmode="group", title="Missing Values Comparison")
            st.plotly_chart(fig, use_container_width=True)

        # Issues fixed bar chart + retention pie
        ch1, ch2 = st.columns(2)
        with ch1:
            st.markdown("#### 🔧 Issues Fixed")
            fig = go.Figure(data=[go.Bar(
                x=["Duplicates", "Missing", "Outliers", "Total Rows"],
                y=[dr, mf, orr, rows_removed],
                marker_color=["#f97316", "#eab308", "#a855f7", "#ef4444"],
            )])
            fig.update_layout(**PLOT_LAYOUT, title="Issues Resolved")
            st.plotly_chart(fig, use_container_width=True)

        with ch2:
            st.markdown("#### 📊 Data Retention")
            retained = len(cleaned_df)
            removed = max(rows_removed, 0)
            fig = go.Figure(data=[go.Pie(
                labels=["Retained", "Removed"],
                values=[retained, removed] if removed > 0 else [retained, 0],
                marker_colors=["#22D3EE", "#ef4444"],
                hole=0.5,
                textinfo="label+percent",
            )])
            fig.update_layout(**PLOT_LAYOUT, title="Row Retention")
            st.plotly_chart(fig, use_container_width=True)

        # Row count comparison
        st.markdown("#### 📏 Row Count Comparison")
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Original", x=["Dataset"], y=[len(raw_df)], marker_color="#60A5FA", width=0.3))
        fig.add_trace(go.Bar(name="Cleaned", x=["Dataset"], y=[len(cleaned_df)], marker_color="#22D3EE", width=0.3))
        fig.update_layout(**PLOT_LAYOUT, barmode="group", title="Row Count: Before vs After")
        st.plotly_chart(fig, use_container_width=True)


    # ── TAB 5: VISUALS ──
    with tab5:
        st.subheader("📈 Advanced Visualizations")
        num_cols_list = cleaned_df.select_dtypes(include=[np.number]).columns.tolist()

        if not num_cols_list:
            st.info("No numeric columns available for visualization.")
        else:
            # Distribution comparison
            st.markdown("#### 📊 Distribution Comparison")
            hist_col = st.selectbox("Select column:", num_cols_list, key="viz_hist_col")
            if hist_col:
                fig = go.Figure()
                raw_vals = raw_df[hist_col].dropna() if hist_col in raw_df.columns else pd.Series(dtype=float)
                clean_vals = cleaned_df[hist_col].dropna()
                if len(raw_vals) > 0:
                    fig.add_trace(go.Histogram(x=raw_vals, name="Original", marker_color="rgba(96,165,250,0.5)", nbinsx=30))
                if len(clean_vals) > 0:
                    fig.add_trace(go.Histogram(x=clean_vals, name="Cleaned", marker_color="rgba(34,211,238,0.5)", nbinsx=30))
                fig.update_layout(**PLOT_LAYOUT, barmode="overlay", title=f"Distribution: {hist_col}")
                st.plotly_chart(fig, use_container_width=True)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            # Boxplot comparison
            st.markdown("#### 📦 Boxplot Comparison")
            box_col = st.selectbox("Select column:", num_cols_list, key="viz_box_col")
            if box_col:
                fig = go.Figure()
                if box_col in raw_df.columns:
                    fig.add_trace(go.Box(y=raw_df[box_col].dropna(), name="Original", marker_color="#60A5FA", boxmean=True))
                fig.add_trace(go.Box(y=cleaned_df[box_col].dropna(), name="Cleaned", marker_color="#22D3EE", boxmean=True))
                fig.update_layout(**PLOT_LAYOUT, title=f"Boxplot: {box_col}")
                st.plotly_chart(fig, use_container_width=True)

            # Correlation heatmap
            if len(num_cols_list) >= 2:
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("#### 🔥 Correlation Heatmap")
                fig = px.imshow(
                    cleaned_df[num_cols_list].corr(),
                    text_auto=".2f",
                    color_continuous_scale="Viridis",
                    aspect="auto",
                )
                fig.update_layout(**PLOT_LAYOUT, title="Feature Correlations")
                st.plotly_chart(fig, use_container_width=True)

            # Missing data pattern
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("#### 🗺️ Missing Data Pattern")
            null_data = raw_df.isna().astype(int)
            if null_data.sum().sum() > 0:
                fig = px.imshow(
                    null_data.head(50).T,
                    color_continuous_scale=["#0F172A", "#22D3EE"],
                    aspect="auto",
                )
                fig.update_layout(**PLOT_LAYOUT, title="Missing Pattern (first 50 rows)", coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ No missing data to visualize.")

    # ── TAB 6: CHAT ──
    with tab6:
        st.subheader("💬 Chat With Your Data")

        # Display chat history
        for msg in st.session_state.chat_history:
            role = "user" if msg["role"] == "user" else "assistant"
            avatar = None if msg["role"] == "user" else "⚡"
            st.chat_message(role, avatar=avatar).write(msg["text"])

        # Suggested questions if no history
        if not st.session_state.chat_history:
            st.markdown("**Ask me anything about your dataset:**")
            suggestions = [
                "What issues does my data have?",
                "Which column has most missing values?",
                "Summarize the dataset",
                "What is the quality score?",
                "How many outliers are there?",
            ]
            cols = st.columns(len(suggestions))
            for i, q in enumerate(suggestions):
                with cols[i % len(cols)]:
                    if st.button(q, key=f"suggest_{i}"):
                        st.session_state.chat_history.append({"role": "user", "text": q})
                        st.rerun()

        # Chat input
        user_input = st.chat_input("Ask about your data...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "text": user_input})

            # Generate response
            msg = user_input.lower()
            missing_s = cleaned_df.isna().sum()
            cols_missing = missing_s[missing_s > 0]

            if "missing" in msg or "null" in msg:
                if len(cols_missing) > 0:
                    worst = cols_missing.idxmax()
                    reply = f"Column `{worst}` has the most missing values: **{int(cols_missing.max())}**. Total missing: {int(cols_missing.sum())} across {len(cols_missing)} columns."
                else:
                    reply = "✅ No missing values in the current dataset!"
            elif "duplicate" in msg:
                d = int(cleaned_df.duplicated().sum())
                reply = f"**{d}** duplicate rows found." if d > 0 else "✅ No duplicates!"
            elif "outlier" in msg:
                ol = detect_outliers_iqr(cleaned_df)
                if ol:
                    total = sum(v["count"] for v in ol.values())
                    reply = f"**{total}** outliers detected across **{len(ol)}** columns using IQR method."
                else:
                    reply = "✅ No significant outliers detected."
            elif "summar" in msg or "overview" in msg or "describe" in msg:
                reply = (
                    f"📊 **Dataset:** {len(cleaned_df):,} rows × {len(cleaned_df.columns)} columns\n\n"
                    f"**Numeric columns:** {len(cleaned_df.select_dtypes(include=[np.number]).columns)}\n\n"
                    f"**Text columns:** {len(cleaned_df.select_dtypes(include=['object']).columns)}\n\n"
                    f"**Missing values:** {int(cleaned_df.isna().sum().sum())}\n\n"
                    f"**Duplicates:** {int(cleaned_df.duplicated().sum())}"
                )
            elif "quality" in msg or "score" in msg:
                qs = quality_score(cleaned_df, raw_df)
                reply = f"Data Quality Score: **{qs}/100** {'🟢' if qs >= 80 else '🟡' if qs >= 60 else '🔴'}"
            elif "column" in msg or "col" in msg:
                reply = f"**Columns ({len(cleaned_df.columns)}):** " + ", ".join([f"`{c}`" for c in cleaned_df.columns])
            elif "shape" in msg or "size" in msg or "row" in msg:
                reply = f"**{len(cleaned_df):,}** rows × **{len(cleaned_df.columns)}** columns"
            else:
                reply = (
                    f"📊 Your dataset has **{len(cleaned_df):,}** rows and **{len(cleaned_df.columns)}** columns. "
                    f"Try asking about: missing values, duplicates, outliers, quality score, or a summary!"
                )

            st.session_state.chat_history.append({"role": "assistant", "text": reply})
            st.rerun()


    # ── TAB 7: EXPORT ──
    with tab7:
        st.subheader("⬇️ Export Center")
        st.markdown("Download your data in multiple formats.")

        fname = st.session_state.get("fn", "data.csv")
        log = st.session_state.cleaning_log
        insights = generate_insights(cleaned_df, raw_df, log)
        insights_text = [f"{t}: {x}" for t, x in insights]

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### 📄 CSV Files")
        csv1, csv2 = st.columns(2)
        with csv1:
            st.download_button(
                "⬇️ Original Data (CSV)",
                raw_df.to_csv(index=False).encode("utf-8"),
                f"original_{fname}",
                "text/csv",
                use_container_width=True,
            )
        with csv2:
            st.download_button(
                "⬇️ Cleaned Data (CSV)",
                cleaned_df.to_csv(index=False).encode("utf-8"),
                f"cleaned_{fname}",
                "text/csv",
                use_container_width=True,
            )

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### 📊 Excel Files")
        xl1, xl2 = st.columns(2)
        with xl1:
            st.download_button(
                "⬇️ Original Data (Excel)",
                to_excel_single(raw_df, "Original Data"),
                f"original_{fname.replace('.csv', '.xlsx')}",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        with xl2:
            st.download_button(
                "⬇️ Full Report (Excel - 3 Sheets)",
                to_excel_multi(raw_df, cleaned_df, insights_text),
                f"report_{fname.replace('.csv', '.xlsx')}",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        st.caption("Excel report includes: Sheet 1 = Original Data, Sheet 2 = Cleaned Data, Sheet 3 = AI Insights")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### 📝 Other Formats")
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            st.download_button(
                "⬇️ JSON",
                cleaned_df.to_json(orient="records", indent=2),
                "cleaned_data.json",
                "application/json",
                use_container_width=True,
            )
        with f2:
            st.download_button(
                "⬇️ TXT Report",
                make_txt_report(raw_df, cleaned_df, log, fname).encode("utf-8"),
                "analytics_report.txt",
                "text/plain",
                use_container_width=True,
            )
        with f3:
            st.download_button(
                "⬇️ PDF Report",
                make_pdf(raw_df, cleaned_df, log, fname),
                "analytics_report.pdf",
                "application/pdf",
                use_container_width=True,
            )
        with f4:
            st.download_button(
                "⬇️ ZIP (All Formats)",
                make_zip(raw_df, cleaned_df, log, fname, insights_text),
                "dataforge_complete.zip",
                "application/zip",
                use_container_width=True,
            )

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.info("💡 **ZIP includes:** original CSV, cleaned CSV, Excel (3 sheets), JSON, TXT report, PDF report")


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer-bar"><p>Built by <span class="cy">Farheen</span> with <span class="bl">Kiro</span></p></div>',
    unsafe_allow_html=True,
)
