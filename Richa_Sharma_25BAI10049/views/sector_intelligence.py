"""
VentureTrack View 3: Sector Intelligence
Provides deep sector benchmarks, capital concentration analysis, and above-average distribution.
Distinct focal-visualization layout with compact summary and macro category panels.
"""
import streamlit as st
import pandas as pd
import plotly.express as px

from src.analytics import get_sector_summary
from src.visualizations import plot_sector_breakdown
from src.insights import generate_sector_insights
from src.ui_components import (
    render_page_header,
    render_stat_strip,
    render_section_header,
    render_editorial_card,
    render_academic_callout,
)
from src.config import THEME_COLORS


def render(df: pd.DataFrame):
    """Renders Sector Intelligence workspace with a distinct focal-visualization layout."""
    render_page_header(
        title="Sector Intelligence",
        subtitle="Vertical Capital Allocation, Transform Groupings & Outlier Intensity",
        badge="Sector Analytics"
    )
    
    if len(df) == 0:
        st.warning("No data available for Sector Intelligence under active filters.")
        return

    sector_summary = get_sector_summary(df, min_deals=1)
    
    if len(sector_summary) == 0:
        st.warning("Insufficient sector data.")
        return

    # 1. Compact Sector Performance Summary Strip
    top_cap_sec = sector_summary.sort_values(by="total_funding_crores", ascending=False).iloc[0]
    top_avg_sec = sector_summary.sort_values(by="avg_funding_crores", ascending=False).iloc[0]
    top_vol_sec = sector_summary.sort_values(by="deal_count", ascending=False).iloc[0]

    sector_stats = [
        {
            "label": "Most Active Sector",
            "value": str(top_vol_sec["sector"]),
            "sub": f"{int(top_vol_sec['deal_count']):,} Announced Deals",
            "badge": "Volume"
        },
        {
            "label": "Largest Capital Pool",
            "value": str(top_cap_sec["sector"]),
            "sub": f"₹{top_cap_sec['total_funding_crores']:,.2f} Cr Total",
            "badge": "Capital"
        },
        {
            "label": "Highest Average Ticket",
            "value": str(top_avg_sec["sector"]),
            "sub": f"₹{top_avg_sec['avg_funding_crores']:,.2f} Cr Per Deal",
            "badge": "Intensity"
        },
    ]
    render_stat_strip(sector_stats)

    # 2. Main Focal Point: Ranked Sector Visualizer with Metric Selector
    render_section_header("Sector Capital Allocation (Top Verticals)", "Comparative analysis across deal volume, total capital, and average check sizes")
    
    metric_choice = st.radio(
        "Sort Chart By",
        options=["total_funding_crores", "avg_funding_crores", "deal_count"],
        index=0,
        horizontal=True,
        label_visibility="collapsed",
        format_func=lambda x: {
            "total_funding_crores": "Sort: Total Capital (₹ Cr)",
            "avg_funding_crores": "Sort: Average Ticket (₹ Cr)",
            "deal_count": "Sort: Deal Volume"
        }.get(x, x)
    )
    
    fig_sec = plot_sector_breakdown(sector_summary, top_n=10, metric=metric_choice)
    st.plotly_chart(fig_sec, use_container_width=True)

    # 3. Macro Sector Categories Split Panel (Task 2 Mapping)
    render_section_header("Macro Sector Categories (Task 2 — map())", "Distribution across Consumer, Financial, Social, and Other / Unmapped groupings")
    
    cat_summary = df.groupby("sector_category", observed=False).agg(
        deal_count=("startup_name", "count"),
        total_funding_crores=("funding_crores", "sum"),
        avg_funding_crores=("funding_crores", "mean")
    ).reset_index()
    cat_summary["avg_funding_crores"] = cat_summary["avg_funding_crores"].round(2)
    cat_summary["total_funding_crores"] = cat_summary["total_funding_crores"].round(2)
    
    cat_col1, cat_col2 = st.columns([1, 1])
    with cat_col1:
        st.dataframe(
            cat_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "sector_category": "Macro Category",
                "deal_count": st.column_config.NumberColumn("Deals", format="%d"),
                "total_funding_crores": st.column_config.NumberColumn("Total Capital (₹ Cr)", format="₹%.2f Cr"),
                "avg_funding_crores": st.column_config.NumberColumn("Average (₹ Cr)", format="₹%.2f Cr"),
            }
        )
    with cat_col2:
        fig_cat = px.bar(
            cat_summary,
            x="sector_category",
            y="total_funding_crores",
            color="sector_category",
            color_discrete_sequence=[THEME_COLORS["primary_accent"], THEME_COLORS["secondary_accent"], THEME_COLORS["warning_amber"], THEME_COLORS["muted_text"]],
            title="Capital by Category",
        )
        fig_cat.update_traces(marker=dict(cornerradius=4))
        fig_cat.update_layout(
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            showlegend=False,
            height=260,
            margin=dict(l=30, r=20, t=30, b=25),
            xaxis_title="",
            yaxis_title="Total (₹ Cr)",
            font=dict(family="Inter, sans-serif", color=THEME_COLORS["primary_text"], size=10),
            xaxis=dict(gridcolor="#F0F2EF", linecolor="#E5E9E5"),
            yaxis=dict(gridcolor="#F0F2EF", linecolor="#E5E9E5"),
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    # 4. Sector Benchmark Matrix (Task 5 transform())
    render_section_header("Full Sector Benchmark Matrix (Task 5 — transform)", "Outperformer proportions calculated dynamically per industry vertical")
    st.dataframe(
        sector_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "sector": "Sector",
            "deal_count": st.column_config.NumberColumn("Deals", format="%d"),
            "total_funding_crores": st.column_config.NumberColumn("Total Capital (₹ Cr)", format="₹%.2f Cr"),
            "avg_funding_crores": st.column_config.NumberColumn("Mean Deal (₹ Cr)", format="₹%.2f Cr"),
            "median_funding_crores": st.column_config.NumberColumn("Median Deal (₹ Cr)", format="₹%.2f Cr"),
            "above_sector_avg_count": st.column_config.NumberColumn("Outperforming Deals", format="%d"),
            "above_sector_avg_pct": st.column_config.NumberColumn("Outperformer %", format="%.1f%%"),
        }
    )

    # 5. Methodological Note
    render_academic_callout(
        "By broadcasting group-level means with df.groupby('sector')['funding_crores'].transform('mean'), every row "
        "maintains its individual record identity while acquiring a dynamic benchmark for comparative outlier indexing.",
        title="TASK 5 TRANSFORM BENCHMARKING"
    )
