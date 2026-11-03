"""
VentureTrack View 1: Market Overview
Displays dynamic macro KPIs, primary ecosystem visualizations, and automated executive takeaways.
Modern Editorial Fintech styling with asymmetric layout and unified stat strips.
"""
import streamlit as st
import pandas as pd

from src.analytics import (
    calculate_market_kpis,
    get_sector_summary,
    get_city_summary,
    get_time_series_aggregations,
    get_distribution_metrics,
)
from src.visualizations import (
    plot_funding_over_time,
    plot_sector_breakdown,
    plot_city_breakdown,
    plot_tier_distribution,
)
from src.insights import generate_market_overview_insights
from src.ui_components import (
    render_page_header,
    render_editorial_hero,
    render_stat_strip,
    render_section_header,
    render_editorial_card,
    render_academic_callout,
)


def render(df: pd.DataFrame):
    """Renders the Market Overview intelligence workspace with an asymmetric editorial layout."""
    render_page_header(
        title="Market Overview",
        subtitle="Macro Liquidity Aggregations, Capital Distribution & Velocity Metrics",
        badge="Ecosystem Intelligence"
    )
    
    if len(df) == 0:
        st.warning("No records match the active filter criteria. Please broaden your filter parameters in the sidebar.")
        return

    # Calculate Market KPIs dynamically
    kpis = calculate_market_kpis(df)
    
    # 1. Refined Editorial Hero with Data-Driven Headline
    render_editorial_hero(
        headline=f"₹{kpis['total_funding_crores']:,.0f} Crore Deployed Across {kpis['total_records']:,} Institutional Deals",
        kicker="MACRO MARKET INTELLIGENCE",
        summary=f"Ecosystem analytics show an average deal size of ₹{kpis['avg_funding_crores']:,.2f} Cr against a median of ₹{kpis['median_funding_crores']:,.2f} Cr, reflecting strong power-law concentration. Bengaluru leads all hubs capturing {kpis['bengaluru_pct']}% of deals across {kpis['unique_sectors']} market sectors."
    )
    
    # 2. Unified Primary Statistic Strip (Horizontal Metrics Bar)
    primary_stats = [
        {
            "label": "Total Capital Deployed",
            "value": f"₹{kpis['total_funding_crores']:,.2f} Cr",
            "sub": "Disclosed Equity & Debt",
            "badge": "Liquidity"
        },
        {
            "label": "Total Deals Tracked",
            "value": f"{kpis['total_records']:,}",
            "sub": f"{kpis['unique_startups']:,} Unique Startups",
            "badge": "Volume"
        },
        {
            "label": "Mean Deal Size",
            "value": f"₹{kpis['avg_funding_crores']:,.2f} Cr",
            "sub": f"Median: ₹{kpis['median_funding_crores']:,.2f} Cr",
            "badge": "Average"
        },
        {
            "label": "Bengaluru Share",
            "value": f"{kpis['bengaluru_pct']}%",
            "sub": f"{kpis['bengaluru_count']:,} Tech Hub Deals",
            "badge": "Innovation"
        },
    ]
    render_stat_strip(primary_stats)

    # 3. Secondary Asymmetric Supporting Metrics
    sec_stats = [
        {
            "label": "Outperforming Deals",
            "value": f"{kpis['above_sector_avg_pct']}%",
            "sub": f"{kpis['above_sector_avg_count']:,} Deals > Sector Average",
        },
        {
            "label": "Geographic Hubs",
            "value": f"{kpis['unique_cities']:,}",
            "sub": "Metros & Regional Ecosystems",
        },
        {
            "label": "Industry Verticals",
            "value": f"{kpis['unique_sectors']:,}",
            "sub": "Disclosed Target Verticals",
        },
        {
            "label": "Investment Stages",
            "value": f"{kpis['unique_rounds']:,}",
            "sub": "Seed to Late Stage Series",
        },
    ]
    render_stat_strip(sec_stats)

    # 4. Dominant Funding Trend Visualization
    render_section_header("Capital Trajectory & Deal Velocity", "Longitudinal capital deployment and deal count volume")
    time_aggs = get_time_series_aggregations(df)
    yearly_df = time_aggs["yearly"]
    
    if len(yearly_df) > 0:
        fig_time = plot_funding_over_time(yearly_df)
        st.plotly_chart(fig_time, use_container_width=True)

    # 5. Two Supporting Analytical Visualizations (Sector & City)
    render_section_header("Capital Allocation Across Sectors & Hubs", "Comparative volume and capital concentration")
    sec_col, city_col = st.columns(2)
    with sec_col:
        sec_df = get_sector_summary(df)
        if len(sec_df) > 0:
            fig_sec = plot_sector_breakdown(sec_df, top_n=8, metric="total_funding_crores")
            st.plotly_chart(fig_sec, use_container_width=True)
    with city_col:
        city_df = get_city_summary(df)
        if len(city_df) > 0:
            fig_city = plot_city_breakdown(city_df, top_n=8)
            st.plotly_chart(fig_city, use_container_width=True)

    # 6. Refined Market Insights Section
    render_section_header("Executive Takeaways", "Real-time empirical observations synthesized from the active portfolio")
    insights = generate_market_overview_insights(kpis)
    render_editorial_card(
        title="Empirical Portfolio Synthesis",
        items=insights,
        kicker="PORTFOLIO SIGNALS"
    )

    # 7. Methodological Note
    render_academic_callout(
        f"Venture capital distributions are power-law distributed: arithmetic mean (₹{kpis['avg_funding_crores']:,.2f} Cr) "
        f"exceeds the median (₹{kpis['median_funding_crores']:,.2f} Cr) by {(kpis['avg_funding_crores']/max(kpis['median_funding_crores'], 0.01)):.1f}x. "
        "This divergence demonstrates that high-magnitude outlier rounds exert an outsized influence on macroeconomic liquidity totals.",
        title="STATISTICAL SKEWNESS & OUTLIER ASYMMETRY"
    )
