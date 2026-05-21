"""
pdf_generator.py
----------------
ReportLab-based PDF report generation for the AI CSV Analyzer.
"""
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER


def generate_pdf(session) -> bytes:
    """
    Generate a PDF insights report for the given session.
    Returns PDF as bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title", parent=styles["Title"], fontSize=20, spaceAfter=6, alignment=TA_CENTER
    )
    h1_style = ParagraphStyle(
        "H1", parent=styles["Heading1"], fontSize=14, spaceBefore=12, spaceAfter=6
    )
    h2_style = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=9, spaceAfter=4, leading=14
    )
    bullet_style = ParagraphStyle(
        "Bullet", parent=styles["Normal"], fontSize=9, leftIndent=12, spaceAfter=3
    )

    story = []

    # --- Title ---
    story.append(Paragraph("AI CSV Analyzer — Insights Report", title_style))
    story.append(Paragraph(f"File: {session.filename}", body_style))
    story.append(
        Paragraph(
            f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            body_style,
        )
    )
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    story.append(Spacer(1, 0.3 * cm))

    # --- Section 1: Data Quality Metrics ---
    story.append(Paragraph("1. Data Quality Metrics", h1_style))
    metrics_data = [
        ["Metric", "Value"],
        ["Original rows", str(len(session.raw_df))],
        ["Cleaned rows", str(len(session.cleaned_df))],
        ["Duplicates removed", str(session.duplicates_removed)],
        ["Missing values resolved", str(session.missing_resolved)],
        ["Outliers removed", str(session.outliers_removed)],
        ["Columns standardized", str(len(session.columns_standardized))],
    ]
    metrics_table = Table(metrics_data, colWidths=[9 * cm, 6 * cm])
    metrics_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F4F6")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(metrics_table)
    story.append(Spacer(1, 0.4 * cm))

    # --- Section 2: Summary Statistics ---
    story.append(Paragraph("2. Summary Statistics", h1_style))
    from app.services.stats_engine import compute_stats
    stats = compute_stats(session.cleaned_df, session.inferred_types)

    numeric_rows = [["Column", "Count", "Mean", "Median", "Std", "Min", "Max"]]
    text_rows = [["Column", "Count", "Unique", "Top Value", "Frequency"]]

    for col, s in stats.items():
        if s["type"] == "numeric":
            numeric_rows.append([
                col,
                str(s["count"]),
                f"{s['mean']:.2f}",
                f"{s['median']:.2f}",
                f"{s['std']:.2f}",
                f"{s['min']:.2f}",
                f"{s['max']:.2f}",
            ])
        else:
            text_rows.append([
                col,
                str(s["count"]),
                str(s["unique"]),
                str(s["top"])[:30],
                str(s["top_freq"]),
            ])

    if len(numeric_rows) > 1:
        story.append(Paragraph("Numeric Columns", h2_style))
        num_table = Table(numeric_rows, repeatRows=1)
        num_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E40AF")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EFF6FF")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFDBFE")),
                ("PADDING", (0, 0), (-1, -1), 5),
            ])
        )
        story.append(num_table)
        story.append(Spacer(1, 0.3 * cm))

    if len(text_rows) > 1:
        story.append(Paragraph("Text / Categorical Columns", h2_style))
        txt_table = Table(text_rows, repeatRows=1)
        txt_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E40AF")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EFF6FF")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFDBFE")),
                ("PADDING", (0, 0), (-1, -1), 5),
            ])
        )
        story.append(txt_table)
        story.append(Spacer(1, 0.4 * cm))

    # --- Section 3: AI Insights ---
    if session.insights:
        story.append(Paragraph("3. AI-Generated Insights", h1_style))
        story.append(Paragraph(session.insights.summary, body_style))
        story.append(Spacer(1, 0.2 * cm))

        if session.insights.temporal_trends:
            story.append(Paragraph("Temporal Trends", h2_style))
            story.append(Paragraph(session.insights.temporal_trends, body_style))

        if session.insights.top_correlations:
            story.append(Paragraph("Top Correlations", h2_style))
            corr_data = [["Column A", "Column B", "Correlation", "Description"]]
            for c in session.insights.top_correlations:
                corr_data.append([
                    c.col_a, c.col_b, f"{c.correlation:.3f}", c.description[:60]
                ])
            corr_table = Table(corr_data, repeatRows=1)
            corr_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#059669")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#ECFDF5")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#A7F3D0")),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(corr_table)
            story.append(Spacer(1, 0.2 * cm))

        if session.insights.quality_suggestions:
            story.append(Paragraph("Data Quality Suggestions", h2_style))
            for suggestion in session.insights.quality_suggestions:
                story.append(Paragraph(f"• {suggestion}", bullet_style))
        story.append(Spacer(1, 0.4 * cm))

    # --- Section 4: ML Model Comparison ---
    if session.ml_result:
        story.append(Paragraph("4. Machine Learning Model Comparison", h1_style))
        ml = session.ml_result
        story.append(
            Paragraph(
                f"Problem type: <b>{ml.problem_type.capitalize()}</b> | "
                f"Better model: <b>{ml.better_model.capitalize()}</b>",
                body_style,
            )
        )
        story.append(Paragraph(ml.explanation, body_style))
        story.append(Spacer(1, 0.2 * cm))

        raw_m = ml.raw_model_metrics
        clean_m = ml.cleaned_model_metrics

        if ml.problem_type == "classification":
            ml_data = [
                ["Metric", "Raw Dataset", "Cleaned Dataset"],
                ["Accuracy", f"{raw_m.accuracy:.4f}", f"{clean_m.accuracy:.4f}"],
                ["Precision", f"{raw_m.precision:.4f}", f"{clean_m.precision:.4f}"],
                ["Recall", f"{raw_m.recall:.4f}", f"{clean_m.recall:.4f}"],
                ["F1 Score", f"{raw_m.f1:.4f}", f"{clean_m.f1:.4f}"],
            ]
        else:
            ml_data = [
                ["Metric", "Raw Dataset", "Cleaned Dataset"],
                ["RMSE", f"{raw_m.rmse:.4f}", f"{clean_m.rmse:.4f}"],
                ["MAE", f"{raw_m.mae:.4f}", f"{clean_m.mae:.4f}"],
                ["R²", f"{raw_m.r2:.4f}", f"{clean_m.r2:.4f}"],
            ]

        ml_table = Table(ml_data, repeatRows=1)
        ml_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7C3AED")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F3FF")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDD6FE")),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(ml_table)
        story.append(Spacer(1, 0.3 * cm))

        if ml.feature_importance:
            story.append(Paragraph("Top Feature Importance", h2_style))
            story.append(Paragraph(ml.top_features_description, body_style))
            fi_data = [["Feature", "Importance Score"]]
            for fi in ml.feature_importance[:10]:
                fi_data.append([fi.feature, f"{fi.score:.4f}"])
            fi_table = Table(fi_data, colWidths=[10 * cm, 5 * cm], repeatRows=1)
            fi_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7C3AED")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F3FF")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDD6FE")),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(fi_table)

    doc.build(story)
    return buffer.getvalue()
