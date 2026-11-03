"""
VentureTrack View 6: Funding Distribution
Rigorous exploration of cut() fixed tiers vs qcut() empirical quartiles and outlier mechanics.
Statistical research layout with parametric vs non-parametric comparisons and contingency heatmaps.
"""
import streamlit as st
import pandas as pd

from src.analytics import get_distribution_metrics
from src.feature_engineering import compare_tier_vs_quartile
from src.visualizations import (
    plot_tier_distribution,
    plot_quartile_distribution,
    plot_funding_distribution_box,
    plot_tier_vs_quartile_heatmap,
)
from src.ui_components import (
    render_page_header,
    render_stat_strip,
    render_section_header,
    render_academic_callout,
)
from src.config import THEME_COLORS


def render(df: pd.DataFrame):
    """Renders the Funding Distribution intelligence workspace with a statistical research layout."""
    render_page_header(
        title="Funding Distribution",
        subtitle="Empirical Dispersion, Task 3 Binning Audit & Tier vs Quartile Divergence",
        badge="Statistical Distribution"
    )
    
    if len(df) == 0:
        st.warning("No distribution data available under active filters.")
        return

    dist_metrics = get_distribution_metrics(df)
    crosstab_df, div_stats = compare_tier_vs_quartile(df)

    if not dist_metrics:
        st.warning("Insufficient non-null funding amounts to calculate distribution.")
        return

    # 1. Parametric vs Non-Parametric Metric Strip
    dist_strip = [
        {
            "label": "Arithmetic Mean",
            "value": f"₹{dist_metrics['mean']:,.2f} Cr",
            "sub": f"Std Dev: ₹{dist_metrics['std']:,.2f} Cr",
            "badge": "Parametric"
        },
        {
            "label": "Median (Q2)",
            "value": f"₹{dist_metrics['median']:,.2f} Cr",
            "sub": f"IQR: ₹{dist_metrics['iqr']:,.2f} Cr",
            "badge": "Robust"
        },
        {
            "label": "Statistical Outliers",
            "value": f"{dist_metrics['outlier_count']:,}",
            "sub": f"{dist_metrics['outlier_pct']}% > 1.5x IQR Threshold",
            "badge": "Anomalies"
        },
        {
            "label": "Max Recorded Deal",
            "value": f"₹{dist_metrics['max']:,.2f} Cr",
            "sub": f"Min: ₹{dist_metrics['min']:,.2f} Cr",
        },
    ]
    render_stat_strip(dist_strip)

    # 2. Side-by-Side: Tiers (cut) vs Quartiles (qcut)
    render_section_header("Task 3 Binning: Fixed Tiers (pd.cut) vs Relative Quartiles (pd.qcut)", "Direct visual comparison between arbitrary financial thresholds and relative population quartiles")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig_tier = plot_tier_distribution(dist_metrics["tier_counts"])
        st.plotly_chart(fig_tier, use_container_width=True)
    with chart_col2:
        fig_q = plot_quartile_distribution(dist_metrics["quartile_counts"])
        st.plotly_chart(fig_q, use_container_width=True)

    # 3. Outlier Dispersion Box Plot
    render_section_header("Capital Dispersion & Logarithmic Geometry", "Non-parametric quantile distribution and mega-round outlier isolation")
    col_t1, col_t2 = st.columns([1, 4])
    with col_t1:
        use_log = st.checkbox("Log Scale (Y-Axis)", value=True, help="Suppresses visual compression from mega-deals")
    
    fig_box = plot_funding_distribution_box(df, use_log=use_log)
    st.plotly_chart(fig_box, use_container_width=True)

    # 4. Task 3 Crosstab Matrix & Divergence Analysis
    render_section_header("Contingency Matrix: Tier (cut) vs Quartile (qcut)", "Empirical proof of why fixed monetary tiers and relative quartiles measure different phenomena")
    
    col_mat1, col_mat2 = st.columns([1, 1])
    with col_mat1:
        st.markdown("<div style='font-size: 0.82rem; font-weight: 600; color: #17211F; margin-bottom: 6px;'>Empirical Joint Frequency Table</div>", unsafe_allow_html=True)
        st.dataframe(crosstab_df, use_container_width=True)
        
        divergence_html = (
            f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-left: 3px solid {THEME_COLORS["warning_amber"]}; padding: 10px 14px; border-radius: 6px; font-size: 0.82rem; margin-top: 8px;">'
            f'<div style="color: {THEME_COLORS["warning_amber"]}; font-weight: 700; font-size: 0.68rem; letter-spacing: 0.08em; text-transform: uppercase;">EMPIRICAL DIVERGENCE PROOF</div>'
            f'<div style="margin-top: 3px; color: {THEME_COLORS["primary_text"]};">Deals classified in <b>Small Tier (&lt;₹100 Cr)</b> yet falling into <b>Q4 (Top 25% Relative)</b>: <span style="color: {THEME_COLORS["primary_accent"]}; font-weight: 700; font-variant-numeric: tabular-nums;">{div_stats["small_tier_in_q4_count"]:,} deals ({div_stats["small_tier_in_q4_pct"]}%)</span>.</div>'
            f'</div>'
        )
        st.markdown(divergence_html, unsafe_allow_html=True)
    with col_mat2:
        fig_heat = plot_tier_vs_quartile_heatmap(crosstab_df)
        st.plotly_chart(fig_heat, use_container_width=True)

    # 5. Methodological Note
    render_academic_callout(
        div_stats["explanation"],
        title="TASK 3 INTERPRETATION: CUT() VS QCUT()"
    )

    # 6. Side-by-Side Sample Inspection Table
    render_section_header("Side-by-Side Verification (Task 3 Item 3)", "Sample transactions illustrating simultaneous fixed tier and quartile labels")
    valid_recs = df.dropna(subset=["funding_crores", "funding_tier", "funding_quartile"]).head(8)
    st.dataframe(
        valid_recs[["startup_name", "funding_crores", "funding_tier", "funding_quartile", "funding_round", "sector"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "startup_name": "Startup",
            "funding_crores": st.column_config.NumberColumn("Funding (₹ Cr)", format="₹%.2f Cr"),
            "funding_tier": "Fixed Tier (cut)",
            "funding_quartile": "Relative Quartile (qcut)",
            "funding_round": "Round",
            "sector": "Sector",
        }
    )
