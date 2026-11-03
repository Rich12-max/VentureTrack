"""
VentureTrack Data Cleaning Pipeline
Converts raw Kaggle dataset into a standardized, validated schema without destructive mutation.
"""
from typing import Optional
import re
import pandas as pd
import numpy as np

from src.config import RAW_TO_CLEAN_COLUMN_MAP, RAW_DATA_PATH, CLEANED_DATA_PATH


def remove_unicode_escapes(val: any) -> any:
    """Removes unicode escapes like \\xc2\\xa0, \\xa0 and irregular whitespace."""
    if pd.isna(val):
        return np.nan
    s = str(val)
    # Strip literal \xc2\xa0 or \\xc2\\xa0 and non-breaking spaces
    s = re.sub(r"\\+xc2\\+xa0|\\xc2\\xa0|\xa0", " ", s)
    s = re.sub(r"\\n|\\r", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if s.lower() in ["nan", "none", "null", ""]:
        return np.nan
    return s


def parse_numeric_amount(val: any) -> float:
    """
    Cleans raw monetary strings into float USD amounts.
    Discards currency symbols, commas, plus signs, and undisclosed markers.
    """
    if pd.isna(val):
        return np.nan
    s = str(val)
    s = re.sub(r"\\+xc2\\+xa0|\\xc2\\xa0|\xa0", "", s)
    s = re.sub(r"[,\+\$\s]", "", s).strip().lower()
    
    if s in ["undisclosed", "unknown", "n/a", "nan", "none", "", "\\xc2\\xa0n/a"]:
        return np.nan
    
    try:
        amt = float(s)
        return amt if amt >= 0 else np.nan
    except (ValueError, TypeError):
        return np.nan


def parse_date_safely(val: any) -> Optional[pd.Timestamp]:
    """
    Sanitizes and parses Indian date strings formatted primarily as dd/mm/yyyy.
    Fixes documented typos (e.g., missing slashes, extra slashes, dots).
    """
    if pd.isna(val):
        return pd.NaT
    s = str(val)
    s = re.sub(r"\\+xc2\\+xa0|\\xc2\\xa0|\xa0", "", s).strip()
    s = s.replace("//", "/").replace(".", "/")
    
    # Correct documented legacy Kaggle typos
    if s == "05/072018":
        s = "05/07/2018"
    elif s == "01/07/015":
        s = "01/07/2015"
    elif s == "10/7/2015":
        s = "10/07/2015"
    elif s == "12/05/2015":
        s = "12/05/2015"
        
    try:
        # Standard format in Kaggle dataset is Day/Month/Year
        return pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
    except Exception:
        # Fallback to flexible parser
        return pd.to_datetime(s, errors="coerce")


def clean_raw_dataset(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the raw Kaggle dataset into a clean DataFrame adhering to the
    canonical VentureTrack schema:
      - startup_name
      - city
      - funding_amount (USD float working column)
      - funding_round
      - sector
      - date
      - (optional auxiliary columns preserved for context)
    """
    df = raw_df.copy()
    
    # 1. Standardize column names via mapping
    mapped_cols = {}
    for col in df.columns:
        norm_col = col.strip()
        if norm_col in RAW_TO_CLEAN_COLUMN_MAP:
            mapped_cols[col] = RAW_TO_CLEAN_COLUMN_MAP[norm_col]
        elif col in RAW_TO_CLEAN_COLUMN_MAP:
            mapped_cols[col] = RAW_TO_CLEAN_COLUMN_MAP[col]
        else:
            mapped_cols[col] = col.lower().replace(" ", "_")
    
    df = df.rename(columns=mapped_cols)
    
    # Verify core columns exist
    required_cols = ["startup_name", "city", "funding_amount", "funding_round", "sector", "date"]
    for req in required_cols:
        if req not in df.columns:
            df[req] = np.nan
            
    # 2. Text cleaning across string columns
    text_cols = ["startup_name", "city", "funding_round", "sector"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].apply(remove_unicode_escapes)
            
    # Auxiliary text columns if present
    for aux in ["sub_sector", "investors_name", "remarks"]:
        if aux in df.columns:
            df[aux] = df[aux].apply(remove_unicode_escapes)

    # 3. Clean funding_amount (USD)
    df["funding_amount"] = df["funding_amount"].apply(parse_numeric_amount)

    # 4. Clean date
    df["date"] = df["date"].apply(parse_date_safely)

    # 5. Clean city values (remove trailing slashes, e.g., 'Bangalore / USA' -> 'Bangalore')
    def clean_city_val(v):
        if pd.isna(v):
            return "Unknown"
        s = str(v).strip()
        # Handle secondary international / dual listings gracefully
        if "/" in s:
            parts = [p.strip() for p in s.split("/")]
            return parts[0]
        return s

    df["city"] = df["city"].apply(clean_city_val)
    
    # 6. Fill missing sector and round with explicit unknown markers
    df["sector"] = df["sector"].fillna("Unspecified")
    df["funding_round"] = df["funding_round"].fillna("Unknown")
    df["startup_name"] = df["startup_name"].fillna("Unknown Startup")

    return df


def generate_and_save_cleaned_dataset(
    raw_path=RAW_DATA_PATH,
    cleaned_path=CLEANED_DATA_PATH,
    force_refresh: bool = False
) -> pd.DataFrame:
    """Reads raw data, cleans it, and persists the cleaned CSV without mutating the raw file."""
    if cleaned_path.exists() and not force_refresh:
        return pd.read_csv(cleaned_path)
    
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw dataset not found at {raw_path}")
        
    raw_df = pd.read_csv(raw_path)
    cleaned_df = clean_raw_dataset(raw_df)
    
    cleaned_df.to_csv(cleaned_path, index=False)
    return cleaned_df


if __name__ == "__main__":
    df_clean = generate_and_save_cleaned_dataset(force_refresh=True)
    print(f"Dataset cleaned and saved. Shape: {df_clean.shape}")
    print(f"Clean columns: {list(df_clean.columns)}")

