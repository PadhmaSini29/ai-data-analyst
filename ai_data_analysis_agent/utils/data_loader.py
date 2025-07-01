# data_loader.py
import pandas as pd

def load_csv_and_get_info(df: pd.DataFrame) -> str:
    """
    Summarizes the structure of the uploaded DataFrame.
    Returns a string with column names, data types, and number of missing values.
    """
    info = "Columns Summary:\n"
    for col in df.columns:
        dtype = df[col].dtype
        missing = df[col].isnull().sum()
        info += f"- {col} ({dtype}) — Missing: {missing}\n"
    return info.strip()
