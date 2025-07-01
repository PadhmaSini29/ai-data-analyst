import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Make sure NLTK resources are available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

def clean_and_preprocess(df: pd.DataFrame):
    original_shape = df.shape

    # 1. Drop columns that are entirely null
    df = df.dropna(axis=1, how="all")

    # 2. Drop rows that contain any missing values
    df = df.dropna(axis=0, how="any")

    # 3. Remove duplicate rows
    df = df.drop_duplicates()

    # 4. Convert string columns that look numeric into numbers
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except Exception:
            continue

    # 5. Outlier detection and removal using Z-score method
    for col in df.select_dtypes(include=["number"]).columns:
        z = (df[col] - df[col].mean()) / df[col].std()
        df = df[(z > -3) & (z < 3)]

    # 6. Normalize numerical values using Min-Max scaling
    numeric_cols = df.select_dtypes(include=["number"]).columns
    if not df.empty and not numeric_cols.empty:
        scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # 7. Text preprocessing for object/string columns
    stop_words = set(stopwords.words("english"))
    for col in df.select_dtypes(include=["object"]).columns:
        try:
            df[col] = df[col].astype(str).apply(lambda text: " ".join(
                [word for word in word_tokenize(text.lower())
                 if word.isalnum() and word not in stop_words]
            ))
        except Exception:
            continue

    cleaned_shape = df.shape
    return df, original_shape, cleaned_shape
