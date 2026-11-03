"""
VentureTrack Data Loader Module
Handles transparent data retrieval, schema validation, caching, and data freshness tracking.
"""
from typing import Tuple, Dict, Any, Optional, List
from datetime import datetime
import pandas as pd
import numpy as np
import streamlit as st

from src.config import RAW_DATA_PATH, CLEANED_DATA_PATH
from src.cleaning import generate_and_save_cleaned_dataset, clean_raw_dataset
from src.feature_engineering import engineer_features


# Global memory tracker for dataset metadata and freshness
_DATA_METADATA: Dict[str, Any] = {
    "loaded_at": None,
    "raw_rows": 0,
    "clean_rows": 0,
    "source_file": None,
    "is_cached": False,
}


def get_dataset_metadata() -> Dict[str, Any]:
    """Returns current dataset loading timestamps and diagnostic counts."""
    return _DATA_METADATA.copy()


def load_raw_dataset() -> pd.DataFrame:
    """Loads the raw Kaggle dataset directly without mutation."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Source raw dataset missing at: {RAW_DATA_PATH}")
    df = pd.read_csv(RAW_DATA_PATH)
    return df


def load_cleaned_dataset(force_refresh: bool = False) -> pd.DataFrame:
    """Loads cleaned dataset, generating it transparently if not already compiled."""
    df = generate_and_save_cleaned_dataset(
        raw_path=RAW_DATA_PATH,
        cleaned_path=CLEANED_DATA_PATH,
        force_refresh=force_refresh
    )
    return df


@st.cache_data(show_spinner="Loading VentureTrack Funding Intelligence Data...")
def get_engineered_dataset(refresh_nonce: int = 0) -> pd.DataFrame:
    """
    Cached loader returning the fully enriched, engineered DataFrame.
    Acts as the centralized application data provider.
    """
    cleaned_df = load_cleaned_dataset(force_refresh=(refresh_nonce > 0))
    enriched_df = engineer_features(cleaned_df)
    
    # Update runtime metadata
    _DATA_METADATA["loaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _DATA_METADATA["clean_rows"] = len(cleaned_df)
    _DATA_METADATA["source_file"] = str(CLEANED_DATA_PATH.name)
    _DATA_METADATA["is_cached"] = True
    
    return enriched_df


def load_and_enrich_custom(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and enriches an arbitrary raw DataFrame (useful for testing miniature
    synthetic datasets or user-uploaded updates).
    """
    cleaned = clean_raw_dataset(raw_df)
    enriched = engineer_features(cleaned)
    return enriched


def validate_schema(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Performs rigorous schema auditing to verify all required assignment features exist.
    """
    required_features = [
        "startup_name",
        "city",
        "funding_crores",
        "is_bengaluru",
        "investor_count",
        "round_number",
        "sector_category",
        "headline",
        "funding_tier",
        "funding_quartile",
        "year",
        "month",
        "quarter",
        "day_of_week",
        "month_name",
        "days_since_funding",
        "funding_era",
        "sector_avg",
        "above_sector_avg",
    ]
    
    missing = [feat for feat in required_features if feat not in df.columns]
    
    # Also verify raw working column 'funding_amount' was dropped
    forbidden_features = ["funding_amount"]
    forbidden_present = [feat for feat in forbidden_features if feat in df.columns]
    
    issues = []
    if missing:
        issues.append(f"Missing mandatory features: {', '.join(missing)}")
    if forbidden_present:
        issues.append(f"Standardized working column was not dropped: {', '.join(forbidden_present)}")
        
    return len(issues) == 0, issues
