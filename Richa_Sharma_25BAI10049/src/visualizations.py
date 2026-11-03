"""
VentureTrack Visualization Engine
Constructs custom Plotly visual assets adhering strictly to the Modern Editorial Fintech Design System.
Clean white surfaces, crisp slate typography, refined palette, minimal grid lines.
"""
from typing import Optional
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from src.config import THEME_COLORS, CHART_PALETTE


def _apply_fintech_layout(
    fig: go.Figure,
    title: Optional[str] = None,
    xaxis_title: Optional[str] = None,
    yaxis_title: Optional[str] = None,
    height: int = 400,
    show_legend: bool = False,
) -> go.Figure:
    """Applies modern editorial fintech styling to Plotly figures with light theme and crisp typography."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color=THEME_COLORS["primary_text"], size=12),
        margin=dict(l=45, r=35, t=55 if title else 25, b=45),
        height=height,
        showlegend=show_legend,
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=THEME_COLORS["borders"],
            font=dict(family="Inter, sans-serif", size=12, color=THEME_COLORS["primary_text"]),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=THEME_COLORS["secondary_text"], size=11),
            bgcolor="rgba(255,255,255,0)",
        ),
        xaxis=dict(
            title=dict(text=xaxis_title or "", font=dict(color=THEME_COLORS["secondary_text"], size=11)),
            tickfont=dict(color=THEME_COLORS["secondary_text"], size=11),
            gridcolor="#F0F2EF",
            zerolinecolor="#E5E9E5",
            showline=True,
            linecolor="#E5E9E5",
        ),
        yaxis=dict(
            title=dict(text=yaxis_title or "", font=dict(color=THEME_COLORS["secondary_text"], size=11)),
            tickfont=dict(color=THEME_COLORS["secondary_text"], size=11),
            gridcolor="#F0F2EF",
            zerolinecolor="#E5E9E5",
            showline=True,
            linecolor="#E5E9E5",
        ),
    )
    if title:
        fig.update_layout(
            title=dict(
                text=f"<b>{title}</b>",
                font=dict(color=THEME_COLORS["primary_text"], size=13.5, family="Inter, sans-serif"),
                x=0.02,
                y=0.96,
            )
        )
    return fig


def plot_funding_over_time(yearly_df: pd.DataFrame) -> go.Figure:
    """Renders dual-axis timeline: Deal Volume bars + Total Funding line."""
    fig = go.Figure()
    
    # Deal Count (Bars)
    fig.add_trace(
        go.Bar(
            x=yearly_df["year"],
            y=yearly_df["deal_count"],
            name="Deals Announced",
            marker=dict(
                color=THEME_COLORS["primary_accent"],
                opacity=0.88,
                cornerradius=4
            ),
            yaxis="y1",
            hovertemplate="<b>%{x}</b><br>Deals: %{y:,}<extra></extra>",
        )
    )
    
    # Capital Deployed (Line)
    fig.add_trace(
        go.Scatter(
            x=yearly_df["year"],
            y=yearly_df["total_funding_crores"],
            name="Total Capital (₹ Cr)",
            mode="lines+markers",
            line=dict(color=THEME_COLORS["secondary_accent"], width=3),
            marker=dict(size=7, color=THEME_COLORS["secondary_accent"], line=dict(color="#FFFFFF", width=1.5)),
            yaxis="y2",
            hovertemplate="<b>%{x}</b><br>Capital: ₹%{y:,.2f} Cr<extra></extra>",
        )
    )
    
    fig = _apply_fintech_layout(
        fig,
        title="Historical Funding Trajectory & Deal Velocity",
        xaxis_title="Calendar Year",
        yaxis_title="Deal Volume (Announcements)",
        show_legend=True,
    )
    
    # Secondary Y-Axis for capital deployed
    fig.update_layout(
        yaxis2=dict(
            title=dict(text="Total Capital (₹ Cr)", font=dict(color=THEME_COLORS["secondary_text"], size=11)),
            tickfont=dict(color=THEME_COLORS["secondary_text"], size=11),
            overlaying="y",
            side="right",
            gridcolor="rgba(0,0,0,0)",
            showgrid=False,
            zeroline=False,
        )
    )
    return fig


def plot_sector_breakdown(sector_df: pd.DataFrame, top_n: int = 10, metric: str = "total_funding_crores") -> go.Figure:
    """Renders horizontal bar chart for top market sectors."""
    df_sorted = sector_df.sort_values(by=metric, ascending=True).tail(top_n)
    
    metric_label = "Total Capital (₹ Cr)" if metric == "total_funding_crores" else (
        "Average Capital (₹ Cr)" if metric == "avg_funding_crores" else "Deal Volume"
    )
    
    fig = go.Figure(
        go.Bar(
            x=df_sorted[metric],
            y=df_sorted["sector"],
            orientation="h",
            marker=dict(
                color=df_sorted[metric],
                colorscale=[
                    [0, "#E8EEF9"],
                    [0.5, "#7B9CE8"],
                    [1.0, THEME_COLORS["primary_accent"]]
                ],
                cornerradius=4
            ),
            hovertemplate="<b>%{y}</b><br>" + metric_label + ": %{x:,.2f}<extra></extra>",
        )
    )
    
    fig = _apply_fintech_layout(
        fig,
        title=f"Top {top_n} Sectors by {metric_label}",
        xaxis_title=metric_label,
        yaxis_title="Market Sector",
        height=420,
    )
    return fig


def plot_city_breakdown(city_df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Renders city rankings highlighting Bengaluru with primary brand identity."""
    df_sorted = city_df.sort_values(by="deal_count", ascending=True).tail(top_n).copy()
    
    # Dynamic coloring: Highlight Bengaluru
    colors = [
        THEME_COLORS["primary_accent"] if is_b else "#A3B8CC"
        for is_b in df_sorted["is_bengaluru"]
    ]
    
    fig = go.Figure(
        go.Bar(
            x=df_sorted["deal_count"],
            y=df_sorted["city"],
            orientation="h",
            marker=dict(color=colors, cornerradius=4),
            hovertemplate="<b>%{y}</b><br>Deals: %{x:,}<extra></extra>",
        )
    )
    
    fig = _apply_fintech_layout(
        fig,
        title=f"Top {top_n} Startup Hubs (Deals Announced)",
        xaxis_title="Deal Volume",
        yaxis_title="City / Ecosystem",
        height=420,
    )
    return fig


def plot_tier_distribution(tier_counts: dict) -> go.Figure:
    """Renders funding tier distribution as a refined fintech donut chart."""
    labels = list(tier_counts.keys())
    values = list(tier_counts.values())
    
    color_map = {
        "Small": THEME_COLORS["primary_accent"],
        "Mid": THEME_COLORS["secondary_accent"],
        "Large": THEME_COLORS["warning_amber"],
    }
    colors = [color_map.get(str(k), THEME_COLORS["muted_text"]) for k in labels]
    
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.64,
            marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2.5)),
            textinfo="label+percent",
            textfont=dict(color=THEME_COLORS["primary_text"], size=12),
            hovertemplate="<b>Tier: %{label}</b><br>Deals: %{value:,} (%{percent})<extra></extra>",
        )
    )
    
    fig = _apply_fintech_layout(
        fig,
        title="Funding Tier Composition (pd.cut)",
        show_legend=True,
        height=360,
    )
    return fig


def plot_quartile_distribution(quartile_counts: dict) -> go.Figure:
    """Renders relative quartile cohorts with styled bar indicators."""
    labels = list(quartile_counts.keys())
    values = list(quartile_counts.values())
    
    colors = [THEME_COLORS["primary_accent"], THEME_COLORS["secondary_accent"], THEME_COLORS["warning_amber"], "#6366F1"]
    
    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            marker=dict(color=colors[:len(labels)], cornerradius=4),
            hovertemplate="<b>Cohort: %{x}</b><br>Deals: %{y:,}<extra></extra>",
        )
    )
    
    fig = _apply_fintech_layout(
        fig,
        title="Relative Funding Cohorts (pd.qcut)",
        xaxis_title="Quartile Cohort",
        yaxis_title="Deals Count",
        height=360,
    )
    return fig


def plot_funding_distribution_box(df: pd.DataFrame, use_log: bool = True) -> go.Figure:
    """Renders box plot for funding distribution with optional log scaling."""
    valid = df.dropna(subset=["funding_crores"]).copy()
    
    fig = go.Figure(
        go.Box(
            y=valid["funding_crores"],
            name="Funding (₹ Cr)",
            marker=dict(color=THEME_COLORS["primary_accent"], size=4),
            boxpoints="outliers",
            jitter=0.25,
            pointpos=-1.6,
            line=dict(color=THEME_COLORS["primary_accent"], width=1.8),
            fillcolor="rgba(49, 95, 206, 0.08)",
        )
    )
    
    fig = _apply_fintech_layout(
        fig,
        title="Funding Amount Dispersion & Outlier Analysis",
        yaxis_title="Capital in INR Crores (₹ Cr)",
        height=380,
    )
    if use_log:
        fig.update_layout(yaxis=dict(type="log", title=dict(text="Capital in ₹ Cr (Log Scale)")))
    return fig


def plot_tier_vs_quartile_heatmap(crosstab_df: pd.DataFrame) -> go.Figure:
    """Renders heatmap comparing fixed monetary tiers vs relative quartiles."""
    matrix = crosstab_df.drop(index=["Total"], columns=["Total"], errors="ignore")
    
    fig = go.Figure(
        go.Heatmap(
            z=matrix.values,
            x=matrix.columns.tolist(),
            y=matrix.index.tolist(),
            colorscale=[
                [0, "#F7F8F6"],
                [0.4, "#E8EEF9"],
                [1.0, THEME_COLORS["primary_accent"]]
            ],
            text=matrix.values,
            texttemplate="<b>%{text}</b>",
            textfont=dict(color=THEME_COLORS["primary_text"], size=12),
            hovertemplate="Tier: %{y}<br>Quartile: %{x}<br>Deals: %{z}<extra></extra>",
        )
    )
    
    fig = _apply_fintech_layout(
        fig,
        title="Funding Tier (Cut) vs Funding Quartile (QCut) Crosstab Matrix",
        xaxis_title="Relative Empirical Cohort (funding_quartile)",
        yaxis_title="Fixed Venture Capital Tier (funding_tier)",
        height=380,
    )
    return fig


def plot_round_number_analysis(round_df: pd.DataFrame) -> go.Figure:
    """Plots Series A through F progression against average funding."""
    series_only = round_df[round_df["round_number"] > 0].sort_values(by="round_number")
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=[f"Round {r} ({name})" for r, name in zip(series_only["round_number"], series_only["funding_round"])],
            y=series_only["deal_count"],
            name="Deal Count",
            marker=dict(color=THEME_COLORS["primary_accent"], cornerradius=4),
            yaxis="y1",
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=[f"Round {r} ({name})" for r, name in zip(series_only["round_number"], series_only["funding_round"])],
            y=series_only["avg_funding_crores"],
            name="Average Funding (₹ Cr)",
            mode="lines+markers",
            line=dict(color=THEME_COLORS["secondary_accent"], width=3),
            marker=dict(size=7.5, color=THEME_COLORS["warning_amber"], line=dict(color="#FFFFFF", width=1.5)),
            yaxis="y2",
        )
    )
    
    fig = _apply_fintech_layout(
        fig,
        title="Institutional Series Progression (Series A → F)",
        xaxis_title="Investment Series",
        yaxis_title="Deal Volume",
        show_legend=True,
        height=400,
    )
    
    fig.update_layout(
        yaxis2=dict(
            title=dict(text="Average Funding (₹ Cr)", font=dict(color=THEME_COLORS["secondary_text"], size=11)),
            tickfont=dict(color=THEME_COLORS["secondary_text"], size=11),
            overlaying="y",
            side="right",
            showgrid=False,
            zeroline=False,
        )
    )
    return fig


def plot_era_comparison(era_df: pd.DataFrame) -> go.Figure:
    """Compares Early, Pandemic, and Recovery funding eras."""
    fig = go.Figure(
        go.Bar(
            x=era_df["funding_era"],
            y=era_df["deal_count"],
            marker=dict(
                color=[THEME_COLORS["primary_accent"], THEME_COLORS["warning_amber"], THEME_COLORS["secondary_accent"]][:len(era_df)],
                cornerradius=4
            ),
            text=era_df["deal_count"],
            textposition="auto",
            hovertemplate="<b>Era: %{x}</b><br>Deals: %{y:,}<extra></extra>",
        )
    )
    
    fig = _apply_fintech_layout(
        fig,
        title="Deal Activity by Macro Funding Era",
        xaxis_title="Funding Era (pd.cut)",
        yaxis_title="Deals Announced",
        height=360,
    )
    return fig


def plot_weekday_seasonality(weekday_df: pd.DataFrame) -> go.Figure:
    """Plots funding announcement activity across days of the week (Mon=0)."""
    fig = go.Figure(
        go.Bar(
            x=weekday_df["day_name"],
            y=weekday_df["deal_count"],
            marker=dict(
                color=weekday_df["deal_count"],
                colorscale=[
                    [0, "#E8EEF9"],
                    [1.0, THEME_COLORS["primary_accent"]]
                ],
                cornerradius=4
            ),
            hovertemplate="<b>Day: %{x}</b><br>Announcements: %{y:,}<extra></extra>",
        )
    )
    
    fig = _apply_fintech_layout(
        fig,
        title="Announcement Seasonality by Day of Week (Monday = 0)",
        xaxis_title="Day of Week",
        yaxis_title="Deal Announcements",
        height=360,
    )
    return fig
