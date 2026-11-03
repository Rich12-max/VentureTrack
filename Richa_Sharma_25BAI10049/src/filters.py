"""
VentureTrack Interactive Filter Management Engine
Maintains global filter state, dynamic scoping, and multi-criteria querying.
"""
from typing import Tuple, Dict, Any, List
import streamlit as st
import pandas as pd
import numpy as np


def render_sidebar_filters(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Renders the modern fintech filter rail in the Streamlit sidebar.
    Returns (filtered_df, active_filters_dict).
    """
    st.sidebar.markdown(
        """
        <div style="padding: 12px 2px 6px 2px; border-top: 1px solid #E5E9E5; margin-top: 12px; margin-bottom: 8px;">
            <div style="font-size: 0.68rem; letter-spacing: 0.08em; color: #8C9690; font-weight: 700; text-transform: uppercase;">
                PORTFOLIO FILTERS
            </div>
            <div style="font-size: 0.72rem; color: #727D77; margin-top: 1px;">
                Multi-criteria pipeline scoping
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 1. Global text search
    search_query = st.sidebar.text_input(
        "Search Startup",
        value="",
        placeholder="e.g. Swiggy, Paytm, Zomato..."
    ).strip()
    
    # 2. City Filter
    all_cities = sorted([c for c in df["city"].dropna().unique() if c != "Unknown"])
    selected_cities = st.sidebar.multiselect(
        "Metropolitan Hubs",
        options=all_cities,
        default=[],
        placeholder="All Cities"
    )
    
    # 3. Sector Filter
    all_sectors = sorted([s for s in df["sector"].dropna().unique() if s != "Unspecified"])
    selected_sectors = st.sidebar.multiselect(
        "Industry Sectors",
        options=all_sectors,
        default=[],
        placeholder="All Sectors"
    )
    
    # 4. Investment Type / Round
    all_rounds = sorted([r for r in df["funding_round"].dropna().unique() if r != "Unknown"])
    selected_rounds = st.sidebar.multiselect(
        "Funding Rounds",
        options=all_rounds,
        default=[],
        placeholder="All Rounds"
    )
    
    # 5. Funding Tier (Small, Mid, Large)
    tier_options = ["Small", "Mid", "Large"]
    selected_tiers = st.sidebar.multiselect(
        "Deal Value Tiers",
        options=tier_options,
        default=[],
        placeholder="All Deal Tiers"
    )
    
    # 6. Macro Funding Era
    era_options = ["Early", "Pandemic", "Recovery"]
    available_eras = [e for e in era_options if e in df["funding_era"].dropna().unique()]
    selected_eras = st.sidebar.multiselect(
        "Macro Funding Eras",
        options=available_eras,
        default=[],
        placeholder="All Funding Eras"
    )
    
    # 7. Year Range Slider
    valid_years = df["year"].dropna().astype(int)
    min_year = int(valid_years.min()) if len(valid_years) > 0 else 2015
    max_year = int(valid_years.max()) if len(valid_years) > 0 else 2020
    
    if min_year < max_year:
        year_range = st.sidebar.slider(
            "Transaction Year Horizon",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
    else:
        year_range = (min_year, max_year)
        
    # 8. Special Toggles (Modern Interactive Cards)
    bengaluru_only = st.sidebar.checkbox(
        "Bengaluru Ecosystem Only",
        value=False
    )
    above_avg_only = st.sidebar.checkbox(
        "Sector Outperformers (> Sector Avg)",
        value=False
    )
        
    # Reset Filters Button
    if st.sidebar.button("↺ Reset All Filters", use_container_width=True):
        st.rerun()

    # Apply Filter Logic
    filtered = df.copy()
    
    if search_query:
        filtered = filtered[
            filtered["startup_name"].str.contains(search_query, case=False, na=False) |
            filtered["sector"].str.contains(search_query, case=False, na=False)
        ]
        
    if selected_cities:
        filtered = filtered[filtered["city"].isin(selected_cities)]
        
    if selected_sectors:
        filtered = filtered[filtered["sector"].isin(selected_sectors)]
        
    if selected_rounds:
        filtered = filtered[filtered["funding_round"].isin(selected_rounds)]
        
    if selected_tiers:
        filtered = filtered[filtered["funding_tier"].isin(selected_tiers)]
        
    if selected_eras:
        filtered = filtered[filtered["funding_era"].isin(selected_eras)]
        
    if year_range:
        filtered = filtered[
            (filtered["year"].isna()) | 
            ((filtered["year"] >= year_range[0]) & (filtered["year"] <= year_range[1]))
        ]
        
    if bengaluru_only:
        filtered = filtered[filtered["is_bengaluru"] == True]
        
    if above_avg_only:
        filtered = filtered[filtered["above_sector_avg"] == True]
        
    active_filters = {
        "search_query": search_query,
        "selected_cities": selected_cities,
        "selected_sectors": selected_sectors,
        "selected_rounds": selected_rounds,
        "selected_tiers": selected_tiers,
        "selected_eras": selected_eras,
        "year_range": year_range,
        "bengaluru_only": bengaluru_only,
        "above_avg_only": above_avg_only,
        "active_count": sum([
            bool(search_query),
            bool(selected_cities),
            bool(selected_sectors),
            bool(selected_rounds),
            bool(selected_tiers),
            bool(selected_eras),
            year_range != (min_year, max_year),
            bengaluru_only,
            above_avg_only,
        ]),
        "total_initial": len(df),
        "total_filtered": len(filtered),
    }
    
    return filtered, active_filters

