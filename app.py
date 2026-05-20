"""
DataForge AI — AI-Powered Smart CSV Cleaning & Analytics
Built by Farheen with Kiro
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO, StringIO
import json
import zipfile

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="DataForge AI", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# ─── MIDNIGHT BLUE + CYAN THEME ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
:root {
    --bg: #0F172A;
    --bg2: #111827;
    --card: #1E293B;
    --cyan: #22D3EE;
    --blue: #60A5FA;
    --text: #F8FAFC;
    --muted: #94a3b8;
    --border: rgba(34,211,238,0.12);
    --glow-cyan: 0 0 20px rgba(34,211,238,0.15);
    --glow-blue: 0 0 20px rgba(96,165,250,0.15);
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

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A, #1E293B);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h3 { color: var(--cyan) !important; }

/* Metrics */
[data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 700; }
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.5px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid rgba(34,211,238,0.08); }
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--muted);
    border-radius: 8px 8px 0 0;
    padding: 10px 18px;
    font-weight: 500;
    transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--cyan); }
.stTabs [aria-selected="true"] {
    background: rgba(34,211,238,0.08) !important;
    color: var(--cyan) !important;
    border-bottom: 2px solid var(--cyan) !important;
    box-shadow: var(--glow-cyan);
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, rgba(34,211,238,0.12), rgba(96,165,250,0.12)) !important;
    color: var(--cyan) !important;
    border: 1px solid rgba(34,211,238,0.25) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: none !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(135deg, rgba(34,211,238,0.2), rgba(96,165,250,0.2)) !important;
    box-shadow: var(--glow-cyan) !important;
    transform: translateY(-1px) !important;
    border-color: var(--cyan) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 1px dashed rgba(34,211,238,0.25) !important;
    border-radius: 12px;
    transition: all 0.3s ease;
}
[data-testid="stFileUploader"]:hover { border-color: var(--cyan) !important; box-shadow: var(--glow-cyan); }

/* ─── MOBILE RESPONSIVENESS ─── */
@media (max-width: 768px) {
    .main .block-container { padding: 0.5rem 0.8rem !important; }
    .hero-box { padding: 28px 16px !important; border-radius: 16px !important; }
    .hero-title { font-size: 1.8rem !important; letter-spacing: -1px !important; }
    .hero-sub { font-size: 0.9rem !important; }
    .hero-badge { font-size: 0.65rem !important; padding: 4px 10px !important; }
    .feat-card { padding: 16px !important; border-radius: 12px !important; }
    .feat-card h4 { font-size: 0.9rem !important; }
    .stat-glow { padding: 14px 8px !important; border-radius: 12px !important; }
    .stat-glow .num { font-size: 1.4rem !important; }
    .stat-glow .icon { font-size: 1.3rem !important; }
    .stat-glow .lbl { font-size: 0.6rem !important; }
    .glass-card { padding: 16px !important; border-radius: 12px !important; }
    .insight-card { padding: 12px !important; font-size: 0.85rem !important; }
    .ai-orb-container { display: none !important; }
    .stTabs [data-baseweb="tab"] { padding: 8px 10px !important; font-size: 0.75rem !important; }
    .stTabs [data-baseweb="tab-list"] { overflow-x: auto; flex-wrap: nowrap; }
    .footer-bar { padding: 8px 0; }
    .footer-bar p { font-size: 0.7rem; }
}
@media (max-width: 480px) {
    .hero-title { font-size: 1.5rem !important; }
    .hero-box { padding: 20px 12px !important; }
    .stat-glow .num { font-size: 1.2rem !important; }
    .feat-card { padding: 12px !important; }
}
/* Touch-friendly targets */
@media (pointer: coarse) {
    .stButton > button, .stDownloadButton > button { min-height: 48px !important; font-size: 0.9rem !important; }
    .stTabs [data-baseweb="tab"] { min-height: 44px !important; }
    [data-testid="stFileUploader"] { min-height: 60px; }
}

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid rgba(34,211,238,0.1); border-radius: 12px; overflow: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(15,23,42,0.5); }
::-webkit-scrollbar-thumb { background: rgba(34,211,238,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--cyan); }

/* Custom classes */
.glass-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}
.glass-card:hover { border-color: rgba(34,211,238,0.25); box-shadow: var(--glow-cyan); }
.hero-box {
    background: linear-gradient(135deg, rgba(34,211,238,0.06), rgba(96,165,250,0.08), rgba(34,211,238,0.04));
    border: 1px solid rgba(34,211,238,0.15);
    border-radius: 24px;
    padding: 56px 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 80px rgba(34,211,238,0.06), 0 0 40px rgba(96,165,250,0.04), inset 0 1px 0 rgba(255,255,255,0.05);
}
.hero-box::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(34,211,238,0.03), transparent, rgba(96,165,250,0.03), transparent);
    animation: rotate-bg 20s linear infinite;
}
@keyframes rotate-bg { to { transform: rotate(360deg); } }
.hero-title {
    position: relative;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #22D3EE 0%, #60A5FA 50%, #22D3EE 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer-text 4s linear infinite;
    margin-bottom: 8px;
    letter-spacing: -2px;
}
@keyframes shimmer-text { to { background-position: 200% center; } }
.hero-sub { position: relative; color: #94a3b8; font-size: 1.2rem; font-weight: 400; }
.hero-badge {
    display: inline-block;
    position: relative;
    background: rgba(34,211,238,0.1);
    border: 1px solid rgba(34,211,238,0.3);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.75rem;
    color: var(--cyan);
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 16px;
    box-shadow: 0 0 15px rgba(34,211,238,0.1);
}
.insight-card {
    background: rgba(34,211,238,0.04);
    border: 1px solid rgba(34,211,238,0.1);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    color: #cbd5e1;
    transition: all 0.3s ease;
}
.insight-card:hover { border-color: rgba(34,211,238,0.25); box-shadow: var(--glow-cyan); }
.insight-card strong { color: var(--text); }
.feat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s ease;
}
.feat-card:hover { border-color: rgba(34,211,238,0.3); box-shadow: var(--glow-cyan); transform: translateY(-2px); }
.feat-card h4 { color: var(--cyan) !important; margin: 8px 0 4px; }

/* Animated stat counter */
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 10px rgba(34,211,238,0.08), inset 0 0 20px rgba(34,211,238,0.02); }
    50% { box-shadow: 0 0 30px rgba(34,211,238,0.15), inset 0 0 30px rgba(34,211,238,0.04); }
}
@keyframes float-up {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
}
.stat-glow {
    animation: pulse-glow 4s ease-in-out infinite;
    background: linear-gradient(145deg, var(--card), rgba(34,211,238,0.03));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 24px 16px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.stat-glow::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0.5;
}
.stat-glow:hover { transform: translateY(-4px) scale(1.02); border-color: var(--cyan); }
.stat-glow .icon { font-size: 1.8rem; margin-bottom: 4px; animation: float-up 3s ease-in-out infinite; }
.stat-glow .num { font-size: 2.2rem; font-weight: 800; color: var(--cyan); margin: 4px 0; text-shadow: 0 0 20px rgba(34,211,238,0.3); }
.stat-glow .lbl { font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.divider { border: none; border-top: 1px solid rgba(34,211,238,0.08); margin: 1.5rem 0; }
.footer-bar {
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 999;
    background: rgba(15,23,42,0.9); backdrop-filter: blur(12px);
    border-top: 1px solid rgba(34,211,238,0.12);
    padding: 10px 0; text-align: center;
}
.footer-bar p { margin: 0; font-size: 0.78rem; color: #64748b; }
.footer-bar .cy { color: var(--cyan); }
.footer-bar .bl { color: var(--blue); }

/* AI Illustration Animations */
.ai-orb-container {
    position: relative;
    filter: drop-shadow(0 0 30px rgba(34,211,238,0.15));
}
.ai-illustration { overflow: visible; }
@keyframes ring-spin { to { transform: rotate(360deg); transform-origin: 100px 100px; } }
@keyframes ring-spin-rev { to { transform: rotate(-360deg); transform-origin: 100px 100px; } }
@keyframes node-blink {
    0%, 100% { opacity: 0.4; r: 3; }
    50% { opacity: 1; r: 5; }
}
@keyframes line-pulse-anim {
    0%, 100% { opacity: 0.2; }
    50% { opacity: 0.8; }
}
@keyframes core-breathe {
    0%, 100% { opacity: 0.6; transform: scale(1); transform-origin: 100px 100px; }
    50% { opacity: 1; transform: scale(1.08); transform-origin: 100px 100px; }
}
.ring-rotate { animation: ring-spin 30s linear infinite; }
.ring-rotate-reverse { animation: ring-spin-rev 25s linear infinite; }
.node-blink { animation: node-blink 2.5s ease-in-out infinite; }
.line-pulse { animation: line-pulse-anim 2s ease-in-out infinite; }
.core-pulse { animation: core-breathe 4s ease-in-out infinite; }

/* Chat styling */
[data-testid="stChatMessage"] { border-radius: 12px !important; }

/* ─── PROFESSIONAL ANIMATIONS ─── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInRight {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes slideDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes borderGlow {
    0%, 100% { border-color: rgba(34,211,238,0.12); }
    50% { border-color: rgba(34,211,238,0.35); }
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Apply fade-in to main content */
.main .block-container { animation: fadeInUp 0.6s ease-out; }

/* Tabs animate in */
.stTabs { animation: fadeInUp 0.5s ease-out 0.1s both; }

/* Metrics animate */
[data-testid="stMetric"] { animation: scaleIn 0.4s ease-out both; }
[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.1s; }
[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.2s; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.3s; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 0.4s; }

/* Dataframes slide in */
[data-testid="stDataFrame"] { animation: fadeInUp 0.5s ease-out 0.2s both; }

/* Download buttons pulse on idle */
.stDownloadButton > button {
    animation: borderGlow 3s ease-in-out infinite;
}

/* Sidebar items animate */
section[data-testid="stSidebar"] .stMarkdown { animation: fadeInLeft 0.4s ease-out both; }

/* Chat messages animate in */
[data-testid="stChatMessage"] { animation: fadeInUp 0.3s ease-out; }

/* Plotly charts fade in */
.js-plotly-plot { animation: scaleIn 0.6s ease-out 0.3s both; }

/* Loading shimmer effect for cards */
.shimmer-loading {
    background: linear-gradient(90deg, var(--card) 25%, rgba(34,211,238,0.08) 50%, var(--card) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
    border-radius: 16px;
    height: 120px;
}

/* Smooth hover on all interactive elements */
button, a, [role="tab"], .stSelectbox > div {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* Animated gradient on hero badge */
.hero-badge {
    background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(96,165,250,0.1), rgba(34,211,238,0.15));
    background-size: 200% 200%;
    animation: gradientShift 4s ease infinite;
}

/* Feature cards stagger animation */
.feat-card { animation: fadeInUp 0.5s ease-out both; }
.feat-card:nth-child(1) { animation-delay: 0.1s; }
.feat-card:nth-child(2) { animation-delay: 0.2s; }
.feat-card:nth-child(3) { animation-delay: 0.3s; }

/* Stat cards stagger */
.stat-glow:nth-child(1) { animation-delay: 0s; }
.stat-glow:nth-child(2) { animation-delay: 0.5s; }
.stat-glow:nth-child(3) { animation-delay: 1s; }
.stat-glow:nth-child(4) { animation-delay: 1.5s; }

/* Insight cards cascade */
.insight-card { animation: fadeInLeft 0.4s ease-out both; }
.insight-card:nth-child(1) { animation-delay: 0.05s; }
.insight-card:nth-child(2) { animation-delay: 0.1s; }
.insight-card:nth-child(3) { animation-delay: 0.15s; }
.insight-card:nth-child(4) { animation-delay: 0.2s; }
.insight-card:nth-child(5) { animation-delay: 0.25s; }

/* Glass card hover lift with shadow expansion */
.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(34,211,238,0.1), 0 0 20px rgba(34,211,238,0.05);
}

/* Smooth expand on selectbox open */
.stSelectbox [data-baseweb="select"] { transition: all 0.2s ease !important; }
.stSelectbox [data-baseweb="select"]:focus-within { box-shadow: 0 0 0 2px rgba(34,211,238,0.3) !important; }

/* Warning/success/info boxes animate */
.stAlert { animation: slideDown 0.4s ease-out; }

/* File uploader pulse when empty */
[data-testid="stFileUploader"] { animation: borderGlow 4s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def infer_column_types(df):
    types = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            types[col] = "numeric"
        else:
            nn = df[col].dropna()
            if len(nn) > 0 and pd.to_datetime(nn, errors="coerce").notna().sum() / len(nn) > 0.5:
                types[col] = "date"
            else:
                types[col] = "text"
    return types

def detect_outliers_iqr(df):
    info = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        s = df[col].dropna()
        if len(s) < 4: continue
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
        c = int(((s < lo) | (s > hi)).sum())
        if c > 0: info[col] = {"count": c, "lower_bound": round(float(lo),2), "upper_bound": round(float(hi),2)}
    return info

def quality_score(df, raw_df):
    tc = raw_df.shape[0] * raw_df.shape[1]
    if tc == 0: return 100
    iss = int(raw_df.duplicated().sum())*raw_df.shape[1] + int(raw_df.isna().sum().sum())
    iss += sum(v["count"] for v in detect_outliers_iqr(raw_df).values())
    return max(0, min(100, int(100 - (iss/tc)*100)))

def to_excel(df):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Data")
    return buf.getvalue()

def make_pdf(raw_df, cleaned_df, log, fname):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    sty = getSampleStyleSheet()
    story = [Paragraph("DataForge AI — Analytics Report", sty["Title"]), Spacer(1,12)]
    story.append(Paragraph(f"File: {fname}", sty["Normal"]))
    story.append(Spacer(1,16))
    data = [["Metric","Value"],["Original Rows",str(len(raw_df))],["Cleaned Rows",str(len(cleaned_df))],
            ["Removed",str(len(raw_df)-len(cleaned_df))],["Duplicates Fixed",str(log.get("duplicates_removed",0))],
            ["Missing Fixed",str(log.get("missing_resolved",0))],["Outliers Removed",str(log.get("outliers_removed",0))],
            ["Quality Score",f"{quality_score(cleaned_df,raw_df)}/100"]]
    t = Table(data, colWidths=[8*cm,5*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0ea5e9")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),10),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f0f9ff")]),
        ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#e2e8f0")),("PADDING",(0,0),(-1,-1),8)]))
    story.append(t)
    story.append(Spacer(1,16))
    story.append(Paragraph("Built by Farheen with Kiro", sty["Normal"]))
    doc.build(story)
    return buf.getvalue()

def make_zip(raw_df, cleaned_df, log, fname):
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("cleaned_data.csv", cleaned_df.to_csv(index=False))
        zf.writestr("cleaned_data.xlsx", to_excel(cleaned_df))
        zf.writestr("report.json", json.dumps({"file":fname,"rows_before":len(raw_df),"rows_after":len(cleaned_df),
            "duplicates_removed":log.get("duplicates_removed",0),"missing_fixed":log.get("missing_resolved",0),
            "outliers_removed":log.get("outliers_removed",0),"quality":quality_score(cleaned_df,raw_df)}, indent=2))
        zf.writestr("analytics_report.pdf", make_pdf(raw_df, cleaned_df, log, fname))
    return buf.getvalue()

def ai_insights(df, raw_df, log):
    ins = []
    rr = len(raw_df)-len(df)
    ins.append(("📊 Summary", f"**{len(df):,} rows** × **{len(df.columns)} cols** after cleaning." + (f" Removed **{rr:,}** rows." if rr>0 else "")))
    d = int(raw_df.duplicated().sum())
    if d>0: ins.append(("🔁 Duplicates", f"**{d:,}** found. {'✅ Fixed.' if log.get('duplicates_removed',0)>0 else '⚠️ Pending.'}"))
    tm = int(raw_df.isna().sum().sum())
    if tm>0:
        w = raw_df.isna().sum().idxmax()
        ins.append(("❓ Missing", f"**{tm:,}** total. Worst: `{w}` ({int(raw_df[w].isna().sum())})"))
    ol = detect_outliers_iqr(raw_df)
    if ol: ins.append(("📉 Outliers", f"**{sum(v['count'] for v in ol.values())}** across {len(ol)} cols."))
    nc = df.select_dtypes(include=[np.number]).columns
    if len(nc)>=2:
        c = df[nc].corr().abs()
        a = c.to_numpy(copy=True)
        np.fill_diagonal(a,0)
        mx = float(a.max())
        if mx>0.5:
            idx = np.unravel_index(a.argmax(), a.shape)
            ins.append(("🔗 Correlation", f"`{nc[idx[0]]}` ↔ `{nc[idx[1]]}` (r={mx:.3f})"))
    ins.append(("⭐ Quality", f"**{quality_score(df,raw_df)}/100**"))
    return ins

DL = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#94a3b8", font_size=11, margin=dict(t=40,b=40,l=40,r=20))

# ─── STATE ───────────────────────────────────────────────────────────────────
for k,v in [("raw_df",None),("cleaned_df",None),("cleaning_log",{}),("chat_history",[])]:
    if k not in st.session_state: st.session_state[k] = v


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ DataForge AI")
    st.caption("Smart CSV Cleaning & Analytics")
    st.markdown("---")
    uf = st.file_uploader("📂 Upload CSV", type=["csv"], help="Max 50 MB")
    if uf:
        if st.session_state.raw_df is None or uf.name != st.session_state.get("fn"):
            try:
                d = pd.read_csv(uf)
                if len(d)==0: st.error("Empty file.")
                else:
                    st.session_state.raw_df = d.copy(deep=True)
                    st.session_state.cleaned_df = d.copy(deep=True)
                    st.session_state.fn = uf.name
                    st.session_state.cleaning_log = {}
                    st.session_state.chat_history = []
                    st.success(f"✅ {uf.name}")
            except Exception as e: st.error(str(e))
        if st.session_state.raw_df is not None:
            st.markdown("---")
            r = st.session_state.raw_df
            st.markdown(f"📋 **{len(r):,}** rows • **{len(r.columns)}** cols")
            st.markdown(f"🔁 **{int(r.duplicated().sum())}** duplicates")
            st.markdown(f"❓ **{int(r.isna().sum().sum())}** missing")
    st.markdown("---")
    st.caption("Built by Farheen with Kiro")

# ─── MAIN ────────────────────────────────────────────────────────────────────
if st.session_state.raw_df is None:
    st.markdown("""
    <div class="hero-box" style="text-align:left; display:flex; align-items:center; justify-content:space-between; gap:40px; flex-wrap:wrap;">
        <div style="flex:1; min-width:280px;">
            <div class="hero-badge">⚡ AI POWERED</div>
            <div class="hero-title" style="text-align:left;">DataForge AI</div>
            <p class="hero-sub" style="text-align:left; margin-bottom:20px;">Next-Gen Smart CSV Cleaning & Analytics Platform</p>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <span class="hero-badge" style="margin:0">🧹 Clean Data</span>
                <span class="hero-badge" style="margin:0">💡 AI Insights</span>
                <span class="hero-badge" style="margin:0">📊 Analytics</span>
                <span class="hero-badge" style="margin:0">💬 Chat</span>
            </div>
        </div>
        <div style="flex:0 0 280px; display:flex; align-items:center; justify-content:center;">
            <div class="ai-orb-container">
                <svg viewBox="0 0 200 200" width="260" height="260" xmlns="http://www.w3.org/2000/svg" class="ai-illustration">
                    <!-- Outer ring -->
                    <circle cx="100" cy="100" r="90" fill="none" stroke="rgba(34,211,238,0.15)" stroke-width="1" stroke-dasharray="4 6" class="ring-rotate"/>
                    <circle cx="100" cy="100" r="75" fill="none" stroke="rgba(96,165,250,0.12)" stroke-width="1" stroke-dasharray="3 8" class="ring-rotate-reverse"/>
                    <!-- Core glow -->
                    <circle cx="100" cy="100" r="45" fill="url(#coreGrad)" class="core-pulse"/>
                    <circle cx="100" cy="100" r="30" fill="rgba(34,211,238,0.08)" class="core-pulse" style="animation-delay:0.5s"/>
                    <!-- Data nodes -->
                    <circle cx="100" cy="30" r="4" fill="#22D3EE" class="node-blink"/>
                    <circle cx="160" cy="70" r="3.5" fill="#60A5FA" class="node-blink" style="animation-delay:0.3s"/>
                    <circle cx="160" cy="130" r="3" fill="#22D3EE" class="node-blink" style="animation-delay:0.6s"/>
                    <circle cx="100" cy="170" r="4" fill="#60A5FA" class="node-blink" style="animation-delay:0.9s"/>
                    <circle cx="40" cy="130" r="3.5" fill="#22D3EE" class="node-blink" style="animation-delay:1.2s"/>
                    <circle cx="40" cy="70" r="3" fill="#60A5FA" class="node-blink" style="animation-delay:1.5s"/>
                    <!-- Connection lines -->
                    <line x1="100" y1="30" x2="100" y2="55" stroke="rgba(34,211,238,0.3)" stroke-width="0.8" class="line-pulse"/>
                    <line x1="160" y1="70" x2="135" y2="85" stroke="rgba(96,165,250,0.3)" stroke-width="0.8" class="line-pulse" style="animation-delay:0.4s"/>
                    <line x1="160" y1="130" x2="135" y2="115" stroke="rgba(34,211,238,0.3)" stroke-width="0.8" class="line-pulse" style="animation-delay:0.8s"/>
                    <line x1="100" y1="170" x2="100" y2="145" stroke="rgba(96,165,250,0.3)" stroke-width="0.8" class="line-pulse" style="animation-delay:1.2s"/>
                    <line x1="40" y1="130" x2="65" y2="115" stroke="rgba(34,211,238,0.3)" stroke-width="0.8" class="line-pulse" style="animation-delay:1.6s"/>
                    <line x1="40" y1="70" x2="65" y2="85" stroke="rgba(96,165,250,0.3)" stroke-width="0.8" class="line-pulse" style="animation-delay:2s"/>
                    <!-- Center icon -->
                    <text x="100" y="106" text-anchor="middle" font-size="24" fill="#22D3EE" class="core-pulse">⚡</text>
                    <!-- Gradient defs -->
                    <defs>
                        <radialGradient id="coreGrad" cx="50%" cy="50%" r="50%">
                            <stop offset="0%" stop-color="rgba(34,211,238,0.2)"/>
                            <stop offset="100%" stop-color="rgba(34,211,238,0)"/>
                        </radialGradient>
                    </defs>
                </svg>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    # Animated stats
    s1,s2,s3,s4 = st.columns(4)
    with s1: st.markdown('<div class="stat-glow"><div class="icon">📁</div><div class="num">0</div><div class="lbl">Files Processed</div></div>', unsafe_allow_html=True)
    with s2: st.markdown('<div class="stat-glow"><div class="icon">⭐</div><div class="num">—</div><div class="lbl">Quality Score</div></div>', unsafe_allow_html=True)
    with s3: st.markdown('<div class="stat-glow"><div class="icon">📊</div><div class="num">0</div><div class="lbl">Rows Analyzed</div></div>', unsafe_allow_html=True)
    with s4: st.markdown('<div class="stat-glow"><div class="icon">💡</div><div class="num">0</div><div class="lbl">AI Insights</div></div>', unsafe_allow_html=True)
    st.markdown("")
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown('<div class="feat-card"><div style="font-size:2.5rem;margin-bottom:8px">🧹</div><h4>Smart Cleaning</h4><p style="font-size:0.85rem;margin-bottom:12px">Duplicates • Nulls • Outliers • Formats</p><div class="hero-badge" style="margin:0">One-Click Fix</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="feat-card"><div style="font-size:2.5rem;margin-bottom:8px">💡</div><h4>AI Insights</h4><p style="font-size:0.85rem;margin-bottom:12px">Patterns • Correlations • Quality Score</p><div class="hero-badge" style="margin:0">Auto-Generated</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="feat-card"><div style="font-size:2.5rem;margin-bottom:8px">💬</div><h4>Chat With Data</h4><p style="font-size:0.85rem;margin-bottom:12px">Ask questions in plain English</p><div class="hero-badge" style="margin:0">AI Assistant</div></div>', unsafe_allow_html=True)
    st.markdown("")
    st.info("👈 Upload a CSV to get started!")
else:
    raw_df = st.session_state.raw_df
    cleaned_df = st.session_state.cleaned_df
    tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs(["📋 Preview","🧹 Clean","💡 Insights","📊 Compare","📈 Visuals","💬 Chat","⬇️ Export"])

    with tab1:
        st.subheader("Data Preview")
        st.dataframe(cleaned_df.head(20), use_container_width=True, height=400)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Rows", f"{len(cleaned_df):,}")
        c2.metric("Columns", len(cleaned_df.columns))
        c3.metric("Duplicates", int(cleaned_df.duplicated().sum()))
        c4.metric("Missing", int(cleaned_df.isna().sum().sum()))

    with tab2:
        st.subheader("🧹 Smart Cleaning")
        st.markdown("#### 🔁 Duplicates")
        dc = int(cleaned_df.duplicated().sum())
        if dc>0:
            st.warning(f"**{dc}** duplicates.")
            if st.button("Remove Duplicates", key="rd"):
                b=len(st.session_state.cleaned_df)
                st.session_state.cleaned_df = st.session_state.cleaned_df.drop_duplicates(keep="first").reset_index(drop=True)
                rm=b-len(st.session_state.cleaned_df)
                st.session_state.cleaning_log["duplicates_removed"] = st.session_state.cleaning_log.get("duplicates_removed",0)+rm
                st.success(f"✅ Removed {rm}!")
                st.rerun()
        else: st.success("✅ No duplicates.")
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### ❓ Missing Values")
        ms = cleaned_df.isna().sum()
        cm = ms[ms>0]
        if len(cm)>0:
            st.warning(f"**{int(cm.sum())}** missing in **{len(cm)}** cols.")
            strat = st.selectbox("Strategy:", ["median","mean","mode","forward_fill","drop_rows"], key="ms")
            if st.button("Apply Fix", key="fm"):
                d = st.session_state.cleaned_df.copy(deep=True)
                res=0
                for col in cm.index:
                    bf=int(d[col].isna().sum())
                    if strat=="mean" and pd.api.types.is_numeric_dtype(d[col]): d[col]=d[col].fillna(d[col].mean())
                    elif strat=="median" and pd.api.types.is_numeric_dtype(d[col]): d[col]=d[col].fillna(d[col].median())
                    elif strat=="mode":
                        mv=d[col].mode()
                        if not mv.empty: d[col]=d[col].fillna(mv.iloc[0])
                    elif strat=="forward_fill": d[col]=d[col].ffill()
                    elif strat=="drop_rows": d=d.dropna(subset=[col])
                    res+=bf-int(d[col].isna().sum() if col in d.columns else 0)
                st.session_state.cleaned_df=d.reset_index(drop=True)
                st.session_state.cleaning_log["missing_resolved"]=st.session_state.cleaning_log.get("missing_resolved",0)+res
                st.success(f"✅ Fixed {res}!")
                st.rerun()
        else: st.success("✅ No missing values.")
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### 📉 Outliers")
        ol = detect_outliers_iqr(cleaned_df)
        if ol:
            st.warning(f"**{sum(v['count'] for v in ol.values())}** outliers.")
            st.dataframe(pd.DataFrame([{"Col":c,"Count":v["count"],"Lo":v["lower_bound"],"Hi":v["upper_bound"]} for c,v in ol.items()]), use_container_width=True, hide_index=True)
            if st.button("Remove Outliers", key="ro"):
                d=st.session_state.cleaned_df.copy(deep=True)
                mask=pd.Series([False]*len(d),index=d.index)
                for c,v in ol.items(): mask=mask|(d[c]<v["lower_bound"])|(d[c]>v["upper_bound"])
                rm=int(mask.sum())
                st.session_state.cleaned_df=d[~mask].reset_index(drop=True)
                st.session_state.cleaning_log["outliers_removed"]=st.session_state.cleaning_log.get("outliers_removed",0)+rm
                st.success(f"✅ Removed {rm}!")
                st.rerun()
        else: st.success("✅ No outliers.")

    with tab3:
        st.subheader("💡 AI Insights")
        for t,x in ai_insights(cleaned_df, raw_df, st.session_state.cleaning_log):
            st.markdown(f'<div class="insight-card"><strong>{t}</strong><br>{x}</div>', unsafe_allow_html=True)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### 📈 Statistics")
        st.dataframe(cleaned_df.describe().round(2), use_container_width=True)
        nc = cleaned_df.select_dtypes(include=[np.number]).columns
        if len(nc)>=2:
            fig = px.imshow(cleaned_df[nc].corr(), text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto")
            fig.update_layout(**DL, title="Correlations")
            st.plotly_chart(fig, use_container_width=True)


    with tab4:
        st.subheader("📊 Before vs After")
        dr=st.session_state.cleaning_log.get("duplicates_removed",0)
        mf=st.session_state.cleaning_log.get("missing_resolved",0)
        orr=st.session_state.cleaning_log.get("outliers_removed",0)
        rr=len(raw_df)-len(cleaned_df)
        qs=quality_score(cleaned_df,raw_df)
        st.markdown(f'<div class="glass-card" style="text-align:center"><p style="color:var(--muted);margin:0;font-size:0.85rem">Quality Score</p><p style="font-size:3rem;font-weight:900;color:var(--cyan);margin:4px 0">{qs}/100</p><p style="color:var(--cyan);margin:0;font-size:0.85rem">↑ {dr+mf+orr} issues fixed</p></div>', unsafe_allow_html=True)
        st.markdown("")
        m1,m2,m3,m4,m5=st.columns(5)
        m1.metric("Before",f"{len(raw_df):,}")
        m2.metric("After",f"{len(cleaned_df):,}",delta=f"-{rr}" if rr>0 else "0")
        m3.metric("Dups",dr)
        m4.metric("Missing",mf)
        m5.metric("Outliers",orr)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### 📋 Side-by-Side")
        cl,cr=st.columns(2)
        with cl:
            st.markdown("**🔴 Raw**")
            st.dataframe(raw_df.head(15), use_container_width=True, height=300)
        with cr:
            st.markdown("**🟢 Cleaned**")
            st.dataframe(cleaned_df.head(15), use_container_width=True, height=300)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        rm_s=raw_df.isna().sum()
        cm_s=cleaned_df.isna().sum()
        cols_m=rm_s[rm_s>0].index.tolist()
        if cols_m:
            fig=go.Figure()
            fig.add_trace(go.Bar(name="Raw",x=cols_m,y=[int(rm_s[c]) for c in cols_m],marker_color="#60A5FA",opacity=0.8))
            fig.add_trace(go.Bar(name="Cleaned",x=cols_m,y=[int(cm_s.get(c,0)) for c in cols_m],marker_color="#22D3EE",opacity=0.8))
            fig.update_layout(**DL,barmode="group",title="Missing: Before vs After")
            st.plotly_chart(fig, use_container_width=True)
        ch1,ch2=st.columns(2)
        with ch1:
            fig=go.Figure(data=[go.Bar(x=["Dups","Missing","Outliers","Total"],y=[dr,mf,orr,rr],marker_color=["#f97316","#eab308","#a855f7","#ef4444"])])
            fig.update_layout(**DL,title="Issues Fixed")
            st.plotly_chart(fig, use_container_width=True)
        with ch2:
            fig=go.Figure(data=[go.Pie(labels=["Retained","Removed"],values=[len(cleaned_df),max(rr,0)],marker_colors=["#22D3EE","#ef4444"],hole=0.5,textinfo="label+percent")])
            fig.update_layout(**DL,title="Retention")
            st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.subheader("📈 Advanced Visuals")
        ncl=cleaned_df.select_dtypes(include=[np.number]).columns.tolist()
        if not ncl: st.info("No numeric columns.")
        else:
            st.markdown("#### 📊 Distribution")
            hc=st.selectbox("Column:",ncl,key="vh")
            if hc:
                fig=go.Figure()
                rv=raw_df[hc].dropna() if hc in raw_df.columns else pd.Series(dtype=float)
                cv=cleaned_df[hc].dropna()
                if len(rv)>0: fig.add_trace(go.Histogram(x=rv,name="Raw",marker_color="rgba(96,165,250,0.5)",nbinsx=30))
                if len(cv)>0: fig.add_trace(go.Histogram(x=cv,name="Cleaned",marker_color="rgba(34,211,238,0.5)",nbinsx=30))
                fig.update_layout(**DL,barmode="overlay",title=f"{hc}")
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("#### 📦 Boxplot")
            bc=st.selectbox("Column:",ncl,key="vb")
            if bc:
                fig=go.Figure()
                if bc in raw_df.columns: fig.add_trace(go.Box(y=raw_df[bc].dropna(),name="Raw",marker_color="#60A5FA",boxmean=True))
                fig.add_trace(go.Box(y=cleaned_df[bc].dropna(),name="Cleaned",marker_color="#22D3EE",boxmean=True))
                fig.update_layout(**DL,title=f"Boxplot: {bc}")
                st.plotly_chart(fig, use_container_width=True)
            if len(ncl)>=2:
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("#### 🔥 Heatmap")
                fig=px.imshow(cleaned_df[ncl].corr(),text_auto=".2f",color_continuous_scale="Viridis",aspect="auto")
                fig.update_layout(**DL)
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("#### 🗺️ Null Pattern")
            nd=raw_df.isna().astype(int)
            if nd.sum().sum()>0:
                fig=px.imshow(nd.head(50).T,color_continuous_scale=["#0F172A","#22D3EE"],aspect="auto")
                fig.update_layout(**DL,title="Missing Pattern (first 50 rows)",coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            else: st.success("✅ No missing data.")

    with tab6:
        st.subheader("💬 Chat With Your Data")
        for msg in st.session_state.chat_history:
            st.chat_message("user" if msg["role"]=="user" else "assistant", avatar=None if msg["role"]=="user" else "⚡").write(msg["text"])
        if not st.session_state.chat_history:
            st.markdown("**Ask me anything about your dataset:**")
            for i,q in enumerate(["What issues does my data have?","Which column has most missing?","Summarize dataset","Quality score?"]):
                if st.button(q, key=f"sq_{i}"):
                    st.session_state.chat_history.append({"role":"user","text":q})
                    st.rerun()
        ui=st.chat_input("Ask about your data...")
        if ui:
            st.session_state.chat_history.append({"role":"user","text":ui})
            m=ui.lower()
            ms=cleaned_df.isna().sum()
            cm=ms[ms>0]
            if "missing" in m or "null" in m:
                reply=f"`{cm.idxmax()}` has {int(cm.max())} missing." if len(cm)>0 else "No missing values!"
            elif "duplicate" in m: reply=f"{int(cleaned_df.duplicated().sum())} duplicates."
            elif "outlier" in m: reply=f"{sum(v['count'] for v in detect_outliers_iqr(cleaned_df).values())} outliers."
            elif "summar" in m or "overview" in m: reply=f"{len(cleaned_df):,} rows × {len(cleaned_df.columns)} cols."
            elif "quality" in m or "score" in m: reply=f"Quality: **{quality_score(cleaned_df,raw_df)}/100**"
            else: reply=f"{len(cleaned_df):,} rows × {len(cleaned_df.columns)} cols. Ask about missing, duplicates, outliers, or quality!"
            st.session_state.chat_history.append({"role":"assistant","text":reply})
            st.rerun()

    with tab7:
        st.subheader("⬇️ Export Center")
        st.markdown("Download in multiple formats.")
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### 📊 Excel")
        e1,e2=st.columns(2)
        with e1: st.download_button("⬇️ original_data.xlsx",to_excel(raw_df),"original_data.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
        with e2: st.download_button("⬇️ cleaned_data.xlsx",to_excel(cleaned_df),"cleaned_data.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("#### 📝 More Formats")
        f1,f2,f3,f4=st.columns(4)
        fn=st.session_state.get("fn","data.csv")
        with f1: st.download_button("⬇️ CSV",cleaned_df.to_csv(index=False).encode("utf-8"),"cleaned_data.csv","text/csv",use_container_width=True)
        with f2: st.download_button("⬇️ JSON",cleaned_df.to_json(orient="records",indent=2),"cleaned_data.json","application/json",use_container_width=True)
        with f3: st.download_button("⬇️ PDF Report",make_pdf(raw_df,cleaned_df,st.session_state.cleaning_log,fn),"analytics_report.pdf","application/pdf",use_container_width=True)
        with f4: st.download_button("⬇️ ZIP (All)",make_zip(raw_df,cleaned_df,st.session_state.cleaning_log,fn),"dataforge_report.zip","application/zip",use_container_width=True)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.info("💡 ZIP includes: cleaned_data.csv, cleaned_data.xlsx, report.json, analytics_report.pdf")

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown('<div class="footer-bar"><p>Built by <span class="cy">Farheen</span> with <span class="bl">Kiro</span></p></div>', unsafe_allow_html=True)
