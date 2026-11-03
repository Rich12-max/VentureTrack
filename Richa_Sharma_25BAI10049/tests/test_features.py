"""
Tests for Feature Engineering Engine (Tasks 1 through 5)
"""
import pytest
import pandas as pd
import numpy as np

from src.feature_engineering import (
    task_1_add_and_remove_columns,
    task_2_apply_and_map_transformations,
    task_3_binning_cut_and_qcut,
    task_4_date_and_time_extraction,
    task_5_summary_metrics_and_transform,
    engineer_features,
)


@pytest.fixture
def sample_cleaned_df():
    return pd.DataFrame({
        "startup_name": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta"],
        "city": ["Bangalore", "Bengaluru", "Mumbai", "New Delhi", "Pune", np.nan],
        "funding_amount": [1_000_000.0, 10_000_000.0, 50_000_000.0, 500_000.0, np.nan, 2_000_000.0],
        "funding_round": ["Series A", "Series B", "Private Equity", "Series C", "Seed Funding", "Series D"],
        "sector": ["eCommerce", "FinTech", "EdTech", "Mobility", "Healthcare", "FoodTech"],
        "date": pd.to_datetime(["2016-01-15", "2018-05-20", "2020-04-10", "2021-08-12", "2023-02-01", "2015-11-05"]),
    })


def test_task_1_inr_conversion_and_removal(sample_cleaned_df):
    df1 = task_1_add_and_remove_columns(sample_cleaned_df)
    
    # 1. funding_crores = funding_amount * 83 / 10,000,000 (rounded to 2 decimals)
    # 1,000,000 * 83 / 10,000,000 = 8.30
    assert df1.loc[0, "funding_crores"] == 8.30
    # 10,000,000 * 83 / 10,000,000 = 83.00
    assert df1.loc[1, "funding_crores"] == 83.00
    # NaN check
    assert np.isnan(df1.loc[4, "funding_crores"])
    
    # 2. is_bengaluru boolean
    assert bool(df1.loc[0, "is_bengaluru"]) is True   # Bangalore
    assert bool(df1.loc[1, "is_bengaluru"]) is True   # Bengaluru
    assert bool(df1.loc[2, "is_bengaluru"]) is False  # Mumbai
    assert bool(df1.loc[5, "is_bengaluru"]) is False  # NaN city
    
    # 3. investor_count initialized with NaN
    assert "investor_count" in df1.columns
    assert df1["investor_count"].isna().all()
    
    # 4. Standardized funding_amount working column is dropped
    assert "funding_amount" not in df1.columns


def test_task_2_apply_and_map(sample_cleaned_df):
    df1 = task_1_add_and_remove_columns(sample_cleaned_df)
    df2 = task_2_apply_and_map_transformations(df1)
    
    # 1. round_number mapping via apply lambda
    # Series A -> 1, Series B -> 2, Private Equity -> 0, Series C -> 3, Seed -> 0, Series D -> 4
    assert df2.loc[0, "round_number"] == 1
    assert df2.loc[1, "round_number"] == 2
    assert df2.loc[2, "round_number"] == 0
    assert df2.loc[3, "round_number"] == 3
    assert df2.loc[4, "round_number"] == 0
    assert df2.loc[5, "round_number"] == 4
    
    # 2. sector_category mapping via map()
    # eCommerce -> Consumer, FinTech -> Financial, EdTech -> Social, Healthcare -> Other / Unmapped
    assert df2.loc[0, "sector_category"] == "Consumer"
    assert df2.loc[1, "sector_category"] == "Financial"
    assert df2.loc[2, "sector_category"] == "Social"
    assert df2.loc[4, "sector_category"] == "Other / Unmapped"
    
    # 3. headline via apply(axis=1)
    # Expected format: "Startup raised ₹X Cr in Round Y"
    h0 = df2.loc[0, "headline"]
    assert "Alpha raised ₹8.30 Cr in Round Series A" in h0
    h4 = df2.loc[4, "headline"]
    assert "Epsilon raised an undisclosed amount in Round Seed Funding" in h4


def test_task_3_cut_and_qcut(sample_cleaned_df):
    df1 = task_1_add_and_remove_columns(sample_cleaned_df)
    df2 = task_2_apply_and_map_transformations(df1)
    df3 = task_3_binning_cut_and_qcut(df2)
    
    # Exact tier boundaries:
    # Small: below ₹100 Cr
    # Mid: ₹100 Cr through ₹300 Cr
    # Large: above ₹300 Cr
    # 50,000,000 * 83 / 10,000,000 = 415.00 -> Large
    # 10,000,000 * 83 / 10,000,000 = 83.00 -> Small
    assert df3.loc[0, "funding_tier"] == "Small"
    assert df3.loc[1, "funding_tier"] == "Small"
    assert df3.loc[2, "funding_tier"] == "Large"
    
    # Quartile check
    assert "funding_quartile" in df3.columns
    # Non-null values should have Q1-Q4
    valid_q = df3["funding_quartile"].dropna()
    assert set(valid_q.unique()).issubset({"Q1", "Q2", "Q3", "Q4"})


def test_task_4_date_and_time_extraction(sample_cleaned_df):
    df1 = task_1_add_and_remove_columns(sample_cleaned_df)
    df2 = task_2_apply_and_map_transformations(df1)
    df3 = task_3_binning_cut_and_qcut(df2)
    df4 = task_4_date_and_time_extraction(df3)
    
    # 2016-01-15 -> year 2016, month 1, quarter 1, month_name January
    assert df4.loc[0, "year"] == 2016
    assert df4.loc[0, "month"] == 1
    assert df4.loc[0, "quarter"] == 1
    assert df4.loc[0, "month_name"] == "January"
    
    # days_since_funding dynamic check
    assert (df4["days_since_funding"].dropna() > 0).all()
    
    # funding_era via pd.cut():
    # Pre-2020: Early
    # 2020-2021: Pandemic
    # 2022 onwards: Recovery
    assert df4.loc[0, "funding_era"] == "Early"     # 2016
    assert df4.loc[2, "funding_era"] == "Pandemic"  # 2020
    assert df4.loc[3, "funding_era"] == "Pandemic"  # 2021
    assert df4.loc[4, "funding_era"] == "Recovery"  # 2023


def test_task_5_transform_summary(sample_cleaned_df):
    df1 = task_1_add_and_remove_columns(sample_cleaned_df)
    df2 = task_2_apply_and_map_transformations(df1)
    df3 = task_3_binning_cut_and_qcut(df2)
    df4 = task_4_date_and_time_extraction(df3)
    df5 = task_5_summary_metrics_and_transform(df4)
    
    # sector_avg calculated via transform
    assert "sector_avg" in df5.columns
    assert "above_sector_avg" in df5.columns
    assert isinstance(df5.loc[0, "above_sector_avg"], (bool, np.bool_))
