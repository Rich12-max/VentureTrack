"""
Tests for Data Cleaning Pipeline (Phase 1 & Phase 7)
"""
import pytest
import pandas as pd
import numpy as np

from src.cleaning import (
    remove_unicode_escapes,
    parse_numeric_amount,
    parse_date_safely,
    clean_raw_dataset,
)


def test_remove_unicode_escapes():
    assert remove_unicode_escapes("\\xc2\\xa0Bangalore") == "Bangalore"
    assert remove_unicode_escapes("Noida\\xc2\\xa0") == "Noida"
    assert remove_unicode_escapes("Seed\\nFunding") == "Seed Funding"
    assert pd.isna(remove_unicode_escapes(np.nan))
    assert pd.isna(remove_unicode_escapes("nan"))
    assert pd.isna(remove_unicode_escapes("   "))


def test_parse_numeric_amount():
    # Standard commas
    assert parse_numeric_amount("1,00,000") == 100000.0
    assert parse_numeric_amount("20,00,00,000") == 200000000.0
    # Plus sign & spaces
    assert parse_numeric_amount("50,000+") == 50000.0
    # Unicode escape with amount
    assert parse_numeric_amount("\\xc2\\xa020,000,000") == 20000000.0
    # Non-numeric indicators
    assert np.isnan(parse_numeric_amount("undisclosed"))
    assert np.isnan(parse_numeric_amount("unknown"))
    assert np.isnan(parse_numeric_amount("N/A"))
    assert np.isnan(parse_numeric_amount(np.nan))


def test_parse_date_safely():
    # Valid date
    d1 = parse_date_safely("09/01/2020")
    assert d1.year == 2020
    assert d1.month == 1
    assert d1.day == 9
    
    # Documented typos
    d2 = parse_date_safely("05/072018")
    assert d2.year == 2018
    assert d2.month == 7
    assert d2.day == 5
    
    # Dot separators
    d3 = parse_date_safely("12/05.2015")
    assert d3.year == 2015
    assert d3.month == 5
    assert d3.day == 12
    
    # Missing / invalid
    assert pd.isna(parse_date_safely("invalid-date-string"))
    assert pd.isna(parse_date_safely(np.nan))


def test_clean_raw_dataset_schema():
    raw_mock = pd.DataFrame({
        "Sr No": [1, 2],
        "Date dd/mm/yyyy": ["01/08/2017", "02/08/2017"],
        "Startup Name": ["TouchKin", "Ethinos"],
        "Industry Vertical": ["Technology", "eCommerce"],
        "City  Location": ["Bangalore", "Mumbai / USA"],
        "InvestmentnType": ["Private Equity", "Series A"],
        "Amount in USD": ["1,300,000", "undisclosed"],
    })
    
    cleaned = clean_raw_dataset(raw_mock)
    
    # Required canonical columns
    assert "startup_name" in cleaned.columns
    assert "city" in cleaned.columns
    assert "funding_amount" in cleaned.columns
    assert "funding_round" in cleaned.columns
    assert "sector" in cleaned.columns
    assert "date" in cleaned.columns
    
    # Check cleaning transformations
    assert cleaned.loc[0, "funding_amount"] == 1300000.0
    assert pd.isna(cleaned.loc[1, "funding_amount"])
    assert cleaned.loc[1, "city"] == "Mumbai"

