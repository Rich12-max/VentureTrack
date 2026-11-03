"""
VentureTrack View 5: Funding Rounds
Analyzes investment instruments, Series A-F ladder progression, and unmapped round semantics.
Investment-stage progression layout with dual-axis capital escalation ladder.
"""
import streamlit as st
import pandas as pd
import plotly.express as px

from src.analytics import get_funding_round_summary
from src.visualizations import plot_round_number_analysis
from src.ui_components import (
    render_page_header,
    render_stat_strip,
    render_section_header,
    render_academic_callout,
)
from src.config import THEME_COLORS


def render(df: pd.DataFrame):
    """Renders the Funding Rounds intelligence workspace with a stage progression layout."""
    render_page_header(
        title="Funding Rounds",
        subtitle="Investment Stage Decomposition, Series Progression & Capital Velocity",
        badge="Stage Analytics"
    )
    
    if len(df) == 0:
        st.warning("No funding round data under active filters.")
        return

    round_summary = get_funding_round_summary(df)
    
    if len(round_summary) == 0:
        st.warning("No round metrics available.")
        return

    # 1. Investment Stage Decomposition Strip
    series_deals = df[df["round_number"] > 0]
    non_series_deals = df[df["round_number"] == 0]
    series_cap = series_deals["funding_crores"].sum()
    non_series_cap = non_series_deals["funding_crores"].sum()

    round_stats = [
        {
            "label": "Series A-F Deals",
            "value": f"{len(series_deals):,}",
            "sub": f"{round(len(series_deals)/len(df)*100, 1)}% of Tracked Deals",
            "badge": "Series"
        },
        {
            "label": "Non-Series Deals",
            "value": f"{len(non_series_deals):,}",
            "sub": "Seed, Angel, Private Equity, Debt",
            "badge": "Other"
        },
        {
            "label": "Series Capital",
            "value": f"₹{series_cap:,.1f} Cr",
            "sub": f"Mean: ₹{series_deals['funding_crores'].mean():,.2f} Cr",
            "badge": "Institutional"
        },
        {
            "label": "Non-Series Capital",
            "value": f"₹{non_series_cap:,.1f} Cr",
            "sub": f"Mean: ₹{non_series_deals['funding_crores'].mean():,.2f} Cr",
        },
    ]
    render_stat_strip(round_stats)

    # 2. Main Focal Chart: Series A → F Escalation Ladder (Task 2 round_number)
    render_section_header("Institutional Series Progression (Task 2 — round_number)", "Visualizing check size expansion and deal filtering from Series A (1) through Series F (6)")
    fig_series = plot_round_number_analysis(round_summary)
    st.plotly_chart(fig_series, use_container_width=True)

    # 3. Top Instruments Distribution Bar Chart
    render_section_header("Investment Structure Breakdown", "Deals announced by legal investment classification")
    top_rounds = round_summary.head(8)
    fig_rounds = px.bar(
        top_rounds,
        x="funding_round",
        y="deal_count",
        color="round_number",
        color_continuous_scale=[[0, "#E8EEF9"], [0.2, "#7B9CE8"], [1.0, THEME_COLORS["primary_accent"]]],
        title="Top Disclosed Round Types by Volume",
    )
    fig_rounds.update_traces(marker=dict(cornerradius=4))
    fig_rounds.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=300,
        margin=dict(l=30, r=20, t=30, b=25),
        xaxis_title="",
        yaxis_title="Deals",
        font=dict(family="Inter, sans-serif", color=THEME_COLORS["primary_text"], size=10),
        xaxis=dict(gridcolor="#F0F2EF", linecolor="#E5E9E5"),
        yaxis=dict(gridcolor="#F0F2EF", linecolor="#E5E9E5"),
    )
    st.plotly_chart(fig_rounds, use_container_width=True)

    # 4. Full Funding Stage Matrix
    render_section_header("Funding Stage Matrix", "Disclosed rounds with mapped round_number index")
    st.dataframe(
        round_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "funding_round": st.column_config.TextColumn("Investment Type / Round", width="medium"),
            "round_number": st.column_config.NumberColumn("Round Number (1-6, Other 0)", format="%d"),
            "deal_count": st.column_config.NumberColumn("Deals", format="%d"),
            "total_funding_crores": st.column_config.NumberColumn("Total Capital (₹ Cr)", format="₹%.2f Cr"),
            "avg_funding_crores": st.column_config.NumberColumn("Mean Ticket (₹ Cr)", format="₹%.2f Cr"),
            "median_funding_crores": st.column_config.NumberColumn("Median Ticket (₹ Cr)", format="₹%.2f Cr"),
        }
    )

    # 5. Methodological Note
    render_academic_callout(
        "Task 2 requires mapping Series A=1, B=2, C=3, D=4, E=5, F=6, and other structures=0. "
        "The empirical data shows severe attrition at each progressive round (a steep deal funnel), "
        "accompanied by exponential ticket size escalation.",
        title="SERIES PROGRESSION & ATTRITION DYNAMICS"
    )
