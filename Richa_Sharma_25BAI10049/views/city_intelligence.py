"""
VentureTrack View 4: City Intelligence
Explores geographic concentration, metropolitan rankings, and Bengaluru vs Rest of India benchmarks.
Geographic comparative layout with asymmetric regional split panels.
"""
import streamlit as st
import pandas as pd

from src.analytics import get_city_summary, get_bengaluru_comparison
from src.visualizations import plot_city_breakdown
from src.insights import generate_city_insights
from src.ui_components import (
    render_page_header,
    render_stat_strip,
    render_section_header,
    render_academic_callout,
)
from src.config import THEME_COLORS


def render(df: pd.DataFrame):
    """Renders the City Intelligence workspace with a geographic comparison layout."""
    render_page_header(
        title="City Intelligence",
        subtitle="Metropolitan Tech Hub Rankings, Bengaluru Dominance & Regional Dispersal",
        badge="Geographic Analytics"
    )
    
    if len(df) == 0:
        st.warning("No city data available under active filters.")
        return

    city_summary = get_city_summary(df, min_deals=1)
    bengaluru_stats = get_bengaluru_comparison(df)
    
    if len(city_summary) == 0:
        st.warning("Insufficient city records.")
        return

    # 1. Geographic Hub Topline Strip
    top_vol_city = city_summary.sort_values(by="deal_count", ascending=False).iloc[0]
    top_cap_city = city_summary.sort_values(by="total_funding_crores", ascending=False).iloc[0]
    top_avg_city = city_summary.sort_values(by="avg_funding_crores", ascending=False).iloc[0]

    city_strip = [
        {
            "label": "Premier Volume Hub",
            "value": str(top_vol_city["city"]),
            "sub": f"{int(top_vol_city['deal_count']):,} Transactions",
            "badge": "Volume"
        },
        {
            "label": "Premier Capital Hub",
            "value": str(top_cap_city["city"]),
            "sub": f"₹{top_cap_city['total_funding_crores']:,.2f} Cr Aggregate",
            "badge": "Capital"
        },
        {
            "label": "Highest Average Ticket",
            "value": str(top_avg_city["city"]),
            "sub": f"₹{top_avg_city['avg_funding_crores']:,.2f} Cr Per Deal",
            "badge": "Intensity"
        },
    ]
    render_stat_strip(city_strip)

    # 2. Asymmetric Regional Comparison Panel: Bengaluru vs Rest of India (Task 1 is_bengaluru)
    render_section_header("Ecosystem Core vs Periphery (Task 1 — is_bengaluru)", "Comparative capital concentration between Bengaluru and remaining metropolitan hubs")
    
    b_kpis = bengaluru_stats.get("bengaluru", {})
    o_kpis = bengaluru_stats.get("others", {})
    
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        blr_card = (
            f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-left: 4px solid {THEME_COLORS["primary_accent"]}; border-radius: 8px; padding: 14px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">'
            f'<div style="font-size: 0.68rem; font-weight: 700; color: {THEME_COLORS["primary_accent"]}; letter-spacing: 0.08em; text-transform: uppercase;">INNOVATION HUB CORE</div>'
            f'<div style="font-size: 1.25rem; font-weight: 700; color: {THEME_COLORS["primary_text"]}; margin: 2px 0 8px 0;">Bengaluru Ecosystem</div>'
            f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-variant-numeric: tabular-nums;">'
            f'<div><div style="font-size: 0.70rem; color: {THEME_COLORS["secondary_text"]}; text-transform: uppercase;">Tracked Deals</div><div style="font-size: 1.25rem; font-weight: 700; color: {THEME_COLORS["primary_text"]};">{b_kpis.get("total_records", 0):,}</div></div>'
            f'<div><div style="font-size: 0.70rem; color: {THEME_COLORS["secondary_text"]}; text-transform: uppercase;">National Share</div><div style="font-size: 1.25rem; font-weight: 700; color: {THEME_COLORS["primary_accent"]};">{bengaluru_stats.get("funding_share_pct", 0)}%</div></div>'
            f'<div><div style="font-size: 0.70rem; color: {THEME_COLORS["secondary_text"]}; text-transform: uppercase;">Total Capital</div><div style="font-size: 1.05rem; font-weight: 600; color: {THEME_COLORS["primary_text"]};">₹{b_kpis.get("total_funding_crores", 0):,.1f} Cr</div></div>'
            f'<div><div style="font-size: 0.70rem; color: {THEME_COLORS["secondary_text"]}; text-transform: uppercase;">Mean Deal Size</div><div style="font-size: 1.05rem; font-weight: 600; color: {THEME_COLORS["primary_text"]};">₹{b_kpis.get("avg_funding_crores", 0):,.2f} Cr</div></div>'
            f'</div></div>'
        )
        st.markdown(blr_card, unsafe_allow_html=True)
    with comp_col2:
        others_card = (
            f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-left: 4px solid {THEME_COLORS["secondary_accent"]}; border-radius: 8px; padding: 14px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">'
            f'<div style="font-size: 0.68rem; font-weight: 700; color: {THEME_COLORS["secondary_accent"]}; letter-spacing: 0.08em; text-transform: uppercase;">NON-BENGALURU AGGREGATE</div>'
            f'<div style="font-size: 1.25rem; font-weight: 700; color: {THEME_COLORS["primary_text"]}; margin: 2px 0 8px 0;">Rest of India Hubs</div>'
            f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-variant-numeric: tabular-nums;">'
            f'<div><div style="font-size: 0.70rem; color: {THEME_COLORS["secondary_text"]}; text-transform: uppercase;">Tracked Deals</div><div style="font-size: 1.25rem; font-weight: 700; color: {THEME_COLORS["primary_text"]};">{o_kpis.get("total_records", 0):,}</div></div>'
            f'<div><div style="font-size: 0.70rem; color: {THEME_COLORS["secondary_text"]}; text-transform: uppercase;">Deal Ratio (BLR vs Non)</div><div style="font-size: 1.25rem; font-weight: 700; color: {THEME_COLORS["secondary_accent"]};">{bengaluru_stats.get("deal_ratio", 0)}x</div></div>'
            f'<div><div style="font-size: 0.70rem; color: {THEME_COLORS["secondary_text"]}; text-transform: uppercase;">Total Capital</div><div style="font-size: 1.05rem; font-weight: 600; color: {THEME_COLORS["primary_text"]};">₹{o_kpis.get("total_funding_crores", 0):,.1f} Cr</div></div>'
            f'<div><div style="font-size: 0.70rem; color: {THEME_COLORS["secondary_text"]}; text-transform: uppercase;">Mean Deal Size</div><div style="font-size: 1.05rem; font-weight: 600; color: {THEME_COLORS["primary_text"]};">₹{o_kpis.get("avg_funding_crores", 0):,.2f} Cr</div></div>'
            f'</div></div>'
        )
        st.markdown(others_card, unsafe_allow_html=True)

    # 3. Metropolitan Rankings Chart
    render_section_header("Top Metropolitan Tech Hubs", "Announced deal volume across primary startup ecosystems")
    fig_city = plot_city_breakdown(city_summary, top_n=10)
    st.plotly_chart(fig_city, use_container_width=True)

    # 4. Comprehensive City Table
    render_section_header("Metropolitan Benchmark Matrix", "All geographic entities sorted by average deal ticket size")
    st.dataframe(
        city_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "city": st.column_config.TextColumn("Metropolitan Hub", width="medium"),
            "deal_count": st.column_config.NumberColumn("Deals", format="%d"),
            "total_funding_crores": st.column_config.NumberColumn("Total Funding (₹ Cr)", format="₹%.2f Cr"),
            "avg_funding_crores": st.column_config.NumberColumn("Average Ticket (₹ Cr)", format="₹%.2f Cr"),
            "median_funding_crores": st.column_config.NumberColumn("Median Ticket (₹ Cr)", format="₹%.2f Cr"),
            "is_bengaluru": st.column_config.CheckboxColumn("Bengaluru Entity"),
        }
    )

    # 5. Methodological Note
    render_academic_callout(
        "By normalizing raw city strings ('Bangalore', 'Bengaluru / USA', etc.) into a canonical is_bengaluru boolean flag, "
        "the pipeline avoids geographic fragmentation and captures the disproportionate gravitational pull of India's Silicon Valley.",
        title="GEOGRAPHIC NORMALIZATION INTEGRITY"
    )
