"""
VentureTrack View 2: Startup Explorer
Allows deep entity search, derived feature auditing, funding headline inspection, and CSV export.
High-density editorial fintech layout with compact controls and refined table styling.
"""
import streamlit as st
import pandas as pd
from src.exports import export_dataframe_to_csv
from src.ui_components import (
    render_page_header,
    render_section_header,
    render_academic_callout,
)
from src.config import THEME_COLORS


def render(df: pd.DataFrame):
    """Renders the Startup Explorer interactive terminal with compact information density."""
    render_page_header(
        title="Startup Explorer",
        subtitle="Individual Deal Inspector, Headline Synthesis & Granular Data Table",
        badge="Entity Intelligence"
    )
    
    if len(df) == 0:
        st.warning("No startups match the active filter criteria. Adjust filters to inspect entities.")
        return

    # 1. Compact Single-Line Search & Sort Toolbar
    col_s1, col_s2, col_s3, col_s4 = st.columns([3, 2, 1.5, 1.5])
    with col_s1:
        local_search = st.text_input(
            "Search Startups",
            value="",
            placeholder="Search by startup name (e.g., Paytm, Swiggy, Ola)...",
            label_visibility="collapsed",
            help="Filter current table instantly"
        ).strip()
    with col_s2:
        sort_by = st.selectbox(
            "Sort Metric",
            options=["funding_crores", "date", "startup_name", "sector_avg"],
            index=0,
            label_visibility="collapsed",
            format_func=lambda x: {
                "funding_crores": "Sort: Capital (₹ Cr)",
                "date": "Sort: Date",
                "startup_name": "Sort: Name",
                "sector_avg": "Sort: Sector Avg"
            }.get(x, x)
        )
    with col_s3:
        ascending = st.selectbox(
            "Sort Direction",
            options=["Descending", "Ascending"],
            index=0,
            label_visibility="collapsed"
        ) == "Ascending"
    with col_s4:
        st.markdown(
            f'<div style="height: 36px; display: flex; align-items: center; justify-content: center; background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-radius: 6px; font-size: 0.78rem; font-weight: 600; color: {THEME_COLORS["primary_accent"]}; font-variant-numeric: tabular-nums;">{len(df):,} Deals</div>',
            unsafe_allow_html=True
        )

    view_df = df.copy()
    if local_search:
        view_df = view_df[view_df["startup_name"].str.contains(local_search, case=False, na=False)]

    view_df = view_df.sort_values(by=sort_by, ascending=ascending, na_position="last")

    # 2. Compact Headline Ticker Strip (Task 2 Requirement)
    sample_headlines = view_df["headline"].dropna().head(4).tolist()
    if sample_headlines:
        headline_items_html = "".join([
            f'<div style="flex: 1; min-width: 240px; background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-left: 3px solid {THEME_COLORS["primary_accent"]}; padding: 7px 11px; border-radius: 5px; font-size: 0.81rem;"><span style="color: {THEME_COLORS["primary_accent"]}; font-weight: 700; font-family: monospace; font-size: 0.74rem; margin-right: 4px;">#{idx:02d}</span><span style="color: {THEME_COLORS["primary_text"]}; font-weight: 500;">{h}</span></div>'
            for idx, h in enumerate(sample_headlines, 1)
        ])
        ticker_html = (
            f'<div style="margin-top: 10px; margin-bottom: 14px;">'
            f'<div style="font-size: 0.68rem; font-weight: 700; color: {THEME_COLORS["secondary_text"]}; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 5px;">Synthesized Funding Headlines (Task 2 — apply() axis=1)</div>'
            f'<div style="display: flex; gap: 8px; flex-wrap: wrap;">{headline_items_html}</div>'
            f'</div>'
        )
        st.markdown(ticker_html, unsafe_allow_html=True)

    # 3. High-Density Data Table
    display_cols = [
        "startup_name",
        "city",
        "sector",
        "sector_category",
        "funding_round",
        "round_number",
        "funding_crores",
        "sector_avg",
        "above_sector_avg",
        "funding_tier",
        "funding_quartile",
        "date",
        "funding_era",
        "is_bengaluru",
        "headline"
    ]
    display_cols = [c for c in display_cols if c in view_df.columns]
    
    st.dataframe(
        view_df[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "startup_name": st.column_config.TextColumn("Startup Name", width="medium"),
            "city": st.column_config.TextColumn("City", width="small"),
            "sector": st.column_config.TextColumn("Sector", width="medium"),
            "funding_crores": st.column_config.NumberColumn("Funding (₹ Cr)", format="₹%.2f Cr"),
            "sector_avg": st.column_config.NumberColumn("Sector Avg (₹ Cr)", format="₹%.2f Cr"),
            "above_sector_avg": st.column_config.CheckboxColumn("> Sector Avg"),
            "is_bengaluru": st.column_config.CheckboxColumn("Bengaluru"),
            "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "funding_tier": st.column_config.TextColumn("Tier"),
            "funding_quartile": st.column_config.TextColumn("Quartile"),
            "round_number": st.column_config.NumberColumn("Round #"),
        }
    )

    # 4. Compact Export Button
    col_d1, col_d2 = st.columns([1, 3])
    with col_d1:
        csv_bytes = export_dataframe_to_csv(view_df[display_cols])
        st.download_button(
            label=f"Export Filtered Results ({len(view_df):,} Rows)",
            data=csv_bytes,
            file_name="venturetrack_startups_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )

    # 5. Methodological Note
    render_academic_callout(
        "By applying df.apply(axis=1), multiple heterogenous dimensions (startup name, domestic INR Crores value, and round stage) "
        "are consolidated horizontally into a journalistic narrative string without slow row-by-row Python iteration.",
        title="APPLY(AXIS=1) HORIZONTAL VECTORIZATION"
    )
