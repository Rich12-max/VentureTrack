"""
VentureTrack View 7: Time & Era Analysis
Decomposes temporal cycles, day-of-week seasonality, macro funding eras, and deal age.
Timeline-focused layout with longitudinal trajectories and seasonality matrices.
"""
import streamlit as st
import pandas as pd
import plotly.express as px

from src.analytics import get_time_series_aggregations
from src.visualizations import (
    plot_funding_over_time,
    plot_era_comparison,
    plot_weekday_seasonality,
)
from src.insights import generate_time_insights
from src.ui_components import (
    render_page_header,
    render_stat_strip,
    render_section_header,
    render_editorial_card,
    render_academic_callout,
)
from src.config import THEME_COLORS


def render(df: pd.DataFrame):
    """Renders the Time & Era Analysis workspace with a timeline-focused layout."""
    render_page_header(
        title="Time & Era Analysis",
        subtitle="Chronological Velocity, Weekday Seasonality, Task 4 Features & Macro Eras",
        badge="Temporal Dynamics"
    )
    
    if len(df) == 0:
        st.warning("No temporal records under active filters.")
        return

    time_aggs = get_time_series_aggregations(df)
    yearly = time_aggs["yearly"]
    quarterly = time_aggs["quarterly"]
    year_quarter = time_aggs["year_quarter"]
    monthly = time_aggs["monthly"]
    weekday = time_aggs["weekday"]
    era = time_aggs["era"]

    # 1. Temporal Pacing Strip
    peak_deal_year = yearly.sort_values(by="deal_count", ascending=False).iloc[0] if len(yearly) > 0 else None
    peak_cap_year = yearly.sort_values(by="total_funding_crores", ascending=False).iloc[0] if len(yearly) > 0 else None
    avg_deal_age = df["days_since_funding"].dropna().mean() if "days_since_funding" in df.columns else 0.0
    early_deals = (df["funding_era"] == "Early").sum() if "funding_era" in df.columns else 0

    pacing_strip = [
        {
            "label": "Peak Deal Volume Year",
            "value": str(int(peak_deal_year["year"])) if peak_deal_year is not None else "N/A",
            "sub": f"{int(peak_deal_year['deal_count']):,} Announcements" if peak_deal_year is not None else "",
            "badge": "Velocity"
        },
        {
            "label": "Peak Capital Year",
            "value": str(int(peak_cap_year["year"])) if peak_cap_year is not None else "N/A",
            "sub": f"₹{peak_cap_year['total_funding_crores']:,.1f} Cr Deployed" if peak_cap_year is not None else "",
            "badge": "Liquidity"
        },
        {
            "label": "Average Deal Age",
            "value": f"{int(avg_deal_age):,} Days",
            "sub": "Since Announcement Date",
            "badge": "Elapsed"
        },
        {
            "label": "Early Era Share",
            "value": f"{round(early_deals/len(df)*100, 1)}%",
            "sub": f"{early_deals:,} Pre-2020 Transactions",
        },
    ]
    render_stat_strip(pacing_strip)

    # 2. Dominant Longitudinal Funding Trajectory Chart
    render_section_header("Longitudinal Funding Trajectory (Task 4 — Year Aggregation)", "Annual deal count and total capital velocity across calendar years")
    if len(yearly) > 0:
        fig_time = plot_funding_over_time(yearly)
        st.plotly_chart(fig_time, use_container_width=True)

    # 3. Sub-Annual Cycles: Quarterly and Monthly Panels
    render_section_header("Sub-Annual Pacing & Intra-Year Seasonality", "Quarterly pacing and monthly deal announcement distributions")
    col_q, col_m = st.columns(2)
    with col_q:
        fig_q = px.bar(
            quarterly,
            x="quarter_label",
            y="deal_count",
            color="deal_count",
            color_continuous_scale=[[0, "#E8EEF9"], [1.0, THEME_COLORS["primary_accent"]]],
            title="Deal Volume by Quarter (Q1-Q4 Aggregate)",
        )
        fig_q.update_traces(marker=dict(cornerradius=4))
        fig_q.update_layout(
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=280,
            margin=dict(l=30, r=20, t=30, b=25),
            xaxis_title="",
            yaxis_title="Deals",
            font=dict(family="Inter, sans-serif", color=THEME_COLORS["primary_text"], size=10),
            xaxis=dict(gridcolor="#F0F2EF", linecolor="#E5E9E5"),
            yaxis=dict(gridcolor="#F0F2EF", linecolor="#E5E9E5"),
        )
        st.plotly_chart(fig_q, use_container_width=True)
    with col_m:
        fig_m = px.bar(
            monthly,
            x="month_name",
            y="deal_count",
            color="deal_count",
            color_continuous_scale=[[0, "#E8EEF9"], [1.0, THEME_COLORS["secondary_accent"]]],
            title="Monthly Announcement Distribution",
        )
        fig_m.update_traces(marker=dict(cornerradius=4))
        fig_m.update_layout(
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=280,
            margin=dict(l=30, r=20, t=30, b=25),
            xaxis_title="",
            yaxis_title="Deals",
            font=dict(family="Inter, sans-serif", color=THEME_COLORS["primary_text"], size=10),
            xaxis=dict(gridcolor="#F0F2EF", linecolor="#E5E9E5"),
            yaxis=dict(gridcolor="#F0F2EF", linecolor="#E5E9E5"),
        )
        st.plotly_chart(fig_m, use_container_width=True)

    # 4. Sequential Year & Quarter Activity Matrix
    render_section_header("Sequential Quarter Progression Matrix", "Complete chronology of deals and deployed capital")
    st.dataframe(
        year_quarter[["period", "year", "quarter", "deal_count", "total_funding_crores"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "period": "Period",
            "year": "Year",
            "quarter": "Quarter",
            "deal_count": st.column_config.NumberColumn("Deals", format="%d"),
            "total_funding_crores": st.column_config.NumberColumn("Capital (₹ Cr)", format="₹%.2f Cr"),
        }
    )

    # 5. Seasonality & Macro Eras
    render_section_header("PR Weekday Timing & Macro Funding Eras (Task 4 Features)", "Day-of-week press releases and Early vs Pandemic vs Recovery era grouping")
    col_w, col_e = st.columns(2)
    with col_w:
        fig_w = plot_weekday_seasonality(weekday)
        st.plotly_chart(fig_w, use_container_width=True)
    with col_e:
        fig_e = plot_era_comparison(era)
        st.plotly_chart(fig_e, use_container_width=True)

    # 6. Methodological Note
    render_academic_callout(
        "Notice that deal announcement spikes around 2015-2016 reflect the initial surge of consumer internet funding rounds "
        "and active press disclosure. Later periods reflect ticket consolidation (fewer, larger deals) and dataset collection boundaries.",
        title="CAUSATION VS SELECTION BIAS"
    )
