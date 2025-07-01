# prompt_templates.py
import pandas as pd

def generate_dataset_summary(df: pd.DataFrame, max_rows: int = 3) -> str:
    summary = f"\n📄 Dataset Overview:\n"
    summary += f"- Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
    summary += "- Columns:\n"
    for col in df.columns:
        dtype = df[col].dtype
        example = df[col].dropna().iloc[0] if not df[col].dropna().empty else "N/A"
        hint = " (likely a date column)" if 'date' in col.lower() else ""
        summary += f"  • {col} ({dtype}) — example: {example}{hint}\n"
    summary += f"\n📌 Sample Rows:\n"
    try:
        summary += df.head(max_rows).to_string(index=False)
    except:
        summary += "(Unable to display sample rows)"
    return summary

def generate_profiling_summary(df: pd.DataFrame) -> str:
    summary = "\n\n📊 Data Profiling Summary:\n"
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if not missing_cols.empty:
        summary += "🟠 Missing Values:\n"
        for col, count in missing_cols.items():
            summary += f"  • {col}: {count} missing\n"
    else:
        summary += "✅ No missing values detected.\n"
    numeric_cols = df.select_dtypes(include="number")
    if not numeric_cols.empty:
        summary += "\n🔢 Numeric Stats:\n"
        for col in numeric_cols.columns:
            summary += f"  • {col}: min={df[col].min()}, max={df[col].max()}, mean={df[col].mean():.2f}\n"
    return summary

def build_insight_prompt(query: str, df: pd.DataFrame) -> str:
    return f"""
You are an expert data analyst.

{generate_dataset_summary(df)}
{generate_profiling_summary(df)}

The user asked:
"{query}"

Instructions:
- Base your answer strictly on the data provided.
- Answer clearly and concisely in natural language.
- If the question involves identifying a specific value from a column (e.g., min temp or max wind), return the exact value AND the corresponding date from the 'date' column.
- Always respond in this format: "The [description] was [value] on [date]."
- Do NOT include explanation steps, assumptions, or Python code.
"""

def build_chart_prompt(query: str, df: pd.DataFrame) -> str:
    return f"""
You are a data analyst and visualization expert.

{generate_dataset_summary(df)}
{generate_profiling_summary(df)}

The user asked:
"{query}"

Please provide:
1. A plain-English insight answering the query directly.
2. If relevant, include Python code to generate a chart using `df`, inside [plot]...[/plot] tags.

Instructions:
- Only include code inside [plot] tags.
- Do NOT include markdown or explanation in or outside the plot block.
- Your final output should be accurate and executable.
"""
