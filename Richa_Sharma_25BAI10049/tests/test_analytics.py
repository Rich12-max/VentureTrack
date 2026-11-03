"""
Tests for Analytics Engine, Dynamic Non-Hardcoding Proof & Edge Cases
"""
import pytest
import pandas as pd
import numpy as np

from src.feature_engineering import engineer_features
from src.analytics import (
    calculate_market_kpis,
    get_sector_summary,
    get_city_summary,
    get_distribution_metrics,
)


def test_dynamic_calculations_on_two_different_mini_datasets():
    """
    CRITICAL PROOF OF NO HARDCODING:
    Executes analytical pipelines on two distinct miniature datasets and verifies
    that all output statistics change dynamically in direct response to input differences.
    """
    # Dataset A: Heavily Bengaluru and Consumer tech oriented
    mini_a = pd.DataFrame({
        "startup_name": ["Zepto", "Blinkit", "Dunzo", "Instamart"],
        "city": ["Bangalore", "Bangalore", "Bengaluru", "Mumbai"],
        "funding_amount": [10_000_000.0, 20_000_000.0, 15_000_000.0, 5_000_000.0],
        "funding_round": ["Series A", "Series B", "Series A", "Seed Funding"],
        "sector": ["eCommerce", "Grocery", "Mobility", "eCommerce"],
        "date": pd.to_datetime(["2017-02-01", "2018-03-01", "2019-04-01", "2016-05-01"]),
    })
    
    # Dataset B: Heavily Delhi / NCR and FinTech oriented with completely different amounts
    mini_b = pd.DataFrame({
        "startup_name": ["PolicyBazaar", "BharatPe", "MobiKwik"],
        "city": ["Gurgaon", "New Delhi", "Gurgaon"],
        "funding_amount": [50_000_000.0, 80_000_000.0, 100_000_000.0],
        "funding_round": ["Series C", "Series D", "Series E"],
        "sector": ["FinTech", "FinTech", "FinTech"],
        "date": pd.to_datetime(["2020-01-10", "2021-06-15", "2022-11-20"]),
    })
    
    enriched_a = engineer_features(mini_a)
    enriched_b = engineer_features(mini_b)
    
    kpis_a = calculate_market_kpis(enriched_a)
    kpis_b = calculate_market_kpis(enriched_b)
    
    # 1. Verification of Deal Counts
    assert kpis_a["total_records"] == 4
    assert kpis_b["total_records"] == 3
    assert kpis_a["total_records"] != kpis_b["total_records"]
    
    # 2. Verification of Capital Deployed
    assert kpis_a["total_funding_crores"] != kpis_b["total_funding_crores"]
    
    # 3. Verification of Average Ticket Size
    assert kpis_a["avg_funding_crores"] != kpis_b["avg_funding_crores"]
    
    # 4. Verification of Bengaluru Share
    assert kpis_a["bengaluru_pct"] == 75.0  # 3 of 4 in Bangalore/Bengaluru
    assert kpis_b["bengaluru_pct"] == 0.0   # 0 of 3 in Gurgaon/Delhi
    
    # 5. Verification of Top Sector Aggregations
    sec_a = get_sector_summary(enriched_a)
    sec_b = get_sector_summary(enriched_b)
    assert set(sec_a["sector"]) != set(sec_b["sector"])
    assert sec_b.iloc[0]["sector"] == "FinTech"


def test_edge_case_empty_dataset():
    """Verifies that an empty DataFrame does not crash calculations."""
    empty_df = pd.DataFrame(columns=[
        "startup_name", "city", "funding_crores", "sector", "funding_round",
        "above_sector_avg", "is_bengaluru", "funding_tier", "funding_quartile"
    ])
    
    kpis = calculate_market_kpis(empty_df)
    assert kpis["total_records"] == 0
    assert kpis["total_funding_crores"] == 0.0
    
    sec_summary = get_sector_summary(empty_df)
    assert len(sec_summary) == 0
    
    city_summary = get_city_summary(empty_df)
    assert len(city_summary) == 0


def test_edge_case_missing_funding_amounts():
    """Verifies that NaN funding values are handled gracefully without zero-division or crash."""
    nan_amt_df = pd.DataFrame({
        "startup_name": ["GhostStartup1", "GhostStartup2"],
        "city": ["Unknown", "Bangalore"],
        "funding_amount": [np.nan, np.nan],
        "funding_round": ["Seed Funding", "Unknown"],
        "sector": ["Artificial Intelligence", "Blockchain"],
        "date": [pd.NaT, pd.NaT],
    })
    
    enriched = engineer_features(nan_amt_df)
    assert enriched["funding_crores"].isna().all()
    assert enriched["funding_tier"].isna().all()
    
    kpis = calculate_market_kpis(enriched)
    assert kpis["total_records"] == 2
    assert kpis["total_funding_crores"] == 0.0


def test_edge_case_identical_values_qcut():
    """Verifies that qcut duplicate boundaries do not raise ValueError."""
    dup_df = pd.DataFrame({
        "startup_name": [f"Startup_{i}" for i in range(10)],
        "city": ["Mumbai"] * 10,
        "funding_amount": [1_000_000.0] * 10,  # Exactly identical amounts
        "funding_round": ["Seed Funding"] * 10,
        "sector": ["eCommerce"] * 10,
        "date": [pd.to_datetime("2018-01-01")] * 10,
    })
    
    # Must not raise ValueError: Bin edges must be unique
    enriched = engineer_features(dup_df)
    assert "funding_quartile" in enriched.columns
    assert len(enriched) == 10

