"""
ai_engine.py
------------
OpenAI API integration for AI-powered suggestions and insights.
"""
import json
import pandas as pd


def suggest_fill_strategy(column: str, df, openai_client) -> dict:
    """
    Use OpenAI to suggest a fill strategy for a column with missing values.
    Returns {"column": str, "suggested_method": str, "rationale": str}
    """
    col_data = df[column] if column in df.columns else None
    if col_data is None:
        return {
            "column": column,
            "suggested_method": "mode",
            "rationale": "Column not found; defaulting to mode.",
        }

    dtype = str(col_data.dtype)
    missing_count = int(col_data.isna().sum())
    total = len(col_data)
    sample = col_data.dropna().head(5).tolist()

    prompt = (
        f"You are a data cleaning expert. A dataset column named '{column}' has:\n"
        f"- Data type: {dtype}\n"
        f"- Missing values: {missing_count} out of {total} ({missing_count / total * 100:.1f}%)\n"
        f"- Sample non-null values: {sample}\n\n"
        "Choose the best fill strategy from: mean, median, mode, forward_fill, drop_rows.\n"
        'Respond with JSON only: {"suggested_method": "<strategy>", "rationale": "<one sentence>"}'
    )

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=150,
        )
        content = response.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        result = json.loads(content)
        valid_methods = {"mean", "median", "mode", "forward_fill", "drop_rows"}
        if result.get("suggested_method") not in valid_methods:
            result["suggested_method"] = "mode"
        return {
            "column": column,
            "suggested_method": result["suggested_method"],
            "rationale": result.get("rationale", ""),
        }
    except Exception:
        # Fallback heuristic when OpenAI is unavailable
        if pd.api.types.is_numeric_dtype(col_data):
            return {
                "column": column,
                "suggested_method": "median",
                "rationale": "Numeric column; median is robust to outliers.",
            }
        return {
            "column": column,
            "suggested_method": "mode",
            "rationale": "Categorical column; mode fills with the most common value.",
        }


def generate_insights(session, openai_client, top_correlations: list) -> dict:
    """
    Generate AI insights for a dataset session.
    Returns InsightResult-compatible dict.
    """
    df = session.cleaned_df
    shape_info = f"{len(df)} rows x {len(df.columns)} columns"
    col_info = ", ".join([f"{c} ({t})" for c, t in session.inferred_types.items()])
    audit = (
        f"Duplicates removed: {session.duplicates_removed}, "
        f"Missing values resolved: {session.missing_resolved}, "
        f"Outliers removed: {session.outliers_removed}"
    )

    corr_text = ""
    if top_correlations:
        corr_text = "Top correlations: " + "; ".join(
            [
                f"{e['col_a']} & {e['col_b']} = {e['correlation']:.2f}"
                for e in top_correlations[:5]
            ]
        )

    prompt = (
        "You are a data analyst. Analyze this dataset:\n"
        f"- Shape: {shape_info}\n"
        f"- Columns: {col_info}\n"
        f"- Cleaning applied: {audit}\n"
        f"- {corr_text}\n\n"
        "Respond with a JSON object with these exact keys:\n"
        '{"summary": "<2-3 sentence overview>", '
        '"temporal_trends": "<trend description or null>", '
        '"quality_suggestions": ["<suggestion 1>", "<suggestion 2>", "<suggestion 3>"]}'
    )

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        result = json.loads(content)
        suggestions = result.get("quality_suggestions", [])
        if len(suggestions) < 3:
            suggestions += [
                "Review columns with high missing value rates.",
                "Check for data entry inconsistencies.",
                "Consider normalizing numeric columns before modeling.",
            ]
            suggestions = suggestions[:3]
        return {
            "summary": result.get("summary", f"Dataset has {shape_info}."),
            "temporal_trends": result.get("temporal_trends"),
            "quality_suggestions": suggestions,
        }
    except Exception:
        return {
            "summary": f"Dataset contains {shape_info} with {len(df.columns)} features.",
            "temporal_trends": None,
            "quality_suggestions": [
                "Review columns with high missing value rates.",
                "Check for data entry inconsistencies.",
                "Consider normalizing numeric columns before modeling.",
            ],
        }
