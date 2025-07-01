# agent.py
from utils.gorq_client import call_gorq
from utils.code_executor import execute_code
from utils.prompt_templates import build_insight_prompt, build_chart_prompt
import pandas as pd
from difflib import get_close_matches

# === Fuzzy match query terms to column names ===
def map_query_columns_to_actual(query: str, columns: list[str]) -> str:
    replacements = {}
    for word in query.split():
        close = get_close_matches(word, columns, n=1, cutoff=0.7)
        if close:
            replacements[word] = close[0]
    for orig, match in replacements.items():
        query = query.replace(orig, match)
    return query

# === Natural language answer only ===
def generate_answer_from_query(query: str, df: pd.DataFrame) -> str:
    lowered = query.lower()
    # Shortcut for known patterns
    if "coldest day" in lowered and "temp_min" in df.columns and "date" in df.columns:
        coldest_row = df.loc[df['temp_min'].idxmin()]
        date = coldest_row['date']
        temp = coldest_row['temp_min']
        return f"The coldest day was {temp}°C on {date}."

    # Fuzzy correct the query based on known column names
    query = map_query_columns_to_actual(query, list(df.columns))

    # Fallback: generate + execute code with grounded column names
    prompt = f"""
You are a data analyst.

You are working with the following DataFrame called `df`. These are its columns:
{list(df.columns)}

Based on the question below, generate Python code using only the above column names.
Assign your final English answer to a variable called `result`.

User question:
"{query}"

Instructions:
- Do NOT guess column names — use only the ones listed above.
- Only return valid Python code.
- `result` must contain a clear, final English sentence answering the question.
- Do not include comments or markdown.
"""
    code = call_gorq(prompt)
    result, error = execute_code(code, df)
    if error:
        return f"⚠️ Failed to execute generated code: {error}"
    return result

# === Natural language + chart code ===
def generate_insight_with_chart_instruction(query: str, df: pd.DataFrame) -> str:
    prompt = build_chart_prompt(query, df)
    return call_gorq(prompt)
