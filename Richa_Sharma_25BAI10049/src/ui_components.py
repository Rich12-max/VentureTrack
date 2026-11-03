"""
VentureTrack UI Components & Design System Engine
Modern Editorial Fintech Intelligence aesthetic (inspired by Linear, Stripe, Mercury, Ramp).
Light theme, robust multi-column layouts, DM Serif Display typography, zero raw HTML leakage.
"""
from typing import Optional, Dict, Any, List
import streamlit as st
from src.config import (
    THEME_COLORS,
    APP_NAME,
    APP_SUBTITLE,
    APP_TAGLINE,
    USD_TO_INR_RATE,
    APP_VERSION
)


def inject_custom_css():
    """Injects high-performance, compact light editorial CSS defining the VentureTrack SaaS design system."""
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* Root Tokens & Design System Variables */
        :root {{
            --vt-bg-main: {THEME_COLORS["main_bg"]};
            --vt-bg-secondary: {THEME_COLORS["secondary_bg"]};
            --vt-surface: {THEME_COLORS["secondary_surface"]};
            --vt-surface-elevated: {THEME_COLORS["elevated_card"]};
            --vt-text-primary: {THEME_COLORS["primary_text"]};
            --vt-text-secondary: {THEME_COLORS["secondary_text"]};
            --vt-text-muted: {THEME_COLORS["muted_text"]};
            --vt-accent-primary: {THEME_COLORS["primary_accent"]};
            --vt-accent-secondary: {THEME_COLORS["secondary_accent"]};
            --vt-accent-growth: {THEME_COLORS["growth_green"]};
            --vt-accent-warning: {THEME_COLORS["warning_amber"]};
            --vt-highlight: {THEME_COLORS["highlight"]};
            --vt-border: {THEME_COLORS["borders"]};
            --vt-border-solid: {THEME_COLORS["border_solid"]};
            --vt-font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --vt-font-serif: 'DM Serif Display', Georgia, serif;
            --vt-font-mono: 'JetBrains Mono', 'Fira Code', monospace;
        }}

        /* Force light theme across every single top-level container */
        html,
        body,
        #root,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewBlockContainer"],
        .main,
        section.main {{
            background-color: var(--vt-bg-main) !important;
            background: var(--vt-bg-main) !important;
            color: var(--vt-text-primary) !important;
            font-family: var(--vt-font-sans);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* Completely eliminate the top header, toolbar, and decoration */
        header,
        header[data-testid="stHeader"],
        .stAppHeader,
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        div[data-testid="stDecoration"] {{
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
            min-height: 0px !important;
            max-height: 0px !important;
            padding: 0 !important;
            margin: 0 !important;
            opacity: 0 !important;
            background: var(--vt-bg-main) !important;
            background-color: var(--vt-bg-main) !important;
            border: none !important;
            box-shadow: none !important;
            pointer-events: none !important;
        }}

        /* Zero out top margin/padding on the main view container */
        [data-testid="stAppViewContainer"] {{
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}

        /* Main Workspace Container — Zero wasted vertical space */
        .main .block-container {{
            max-width: 1420px !important;
            padding-top: 1rem !important;
            padding-bottom: 2.8rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }}

        /* Headings & Text Color Overrides */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--vt-text-primary) !important;
            font-feature-settings: "cv02" 1, "cv03" 1;
        }}

        p, span, label, div {{
            color: var(--vt-text-primary);
        }}

        /* Sidebar Styling — Modern Futuristic 295px Desktop Rail */
        section[data-testid="stSidebar"] {{
            width: 295px !important;
            min-width: 295px !important;
            max-width: 295px !important;
            background: #F8FAF8 !important;
            border-right: 1px solid #E5E9E5 !important;
            padding-top: 0.85rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
        }}

        section[data-testid="stSidebar"] > div:first-child {{
            width: 295px !important;
            padding: 0 0.25rem !important;
        }}

        section[data-testid="stSidebar"] .stMarkdown {{
            color: var(--vt-text-secondary);
        }}

        /* Clean up clutter: hide repetitive question mark icons in sidebar */
        section[data-testid="stSidebar"] div[data-testid="stTooltipIcon"] {{
            display: none !important;
        }}

        /* Sidebar Navigation Radio Styling */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {{
            gap: 2px !important;
        }}

        /* Remove default circular radio bullet entirely for sleek SaaS rail */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child {{
            display: none !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label input[type="radio"] {{
            display: none !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
            background: transparent !important;
            border-radius: 7px !important;
            padding: 6px 11px !important;
            margin: 1px 0 !important;
            transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
            border: 1px solid transparent !important;
            cursor: pointer !important;
            color: #526058 !important;
            font-size: 0.83rem !important;
            font-weight: 500 !important;
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
            position: relative !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
            background: #FFFFFF !important;
            border-color: #E2E6E2 !important;
            color: var(--vt-accent-primary) !important;
            transform: translateX(3px) !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"],
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
            background: #FFFFFF !important;
            border: 1px solid rgba(49, 95, 206, 0.22) !important;
            border-left: 3.5px solid var(--vt-accent-primary) !important;
            box-shadow: 0 3px 10px rgba(49, 95, 206, 0.09) !important;
            color: #17211F !important;
            font-weight: 600 !important;
            transform: translateX(3px) !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {{
            margin: 0 !important;
            font-size: 0.83rem !important;
            font-weight: inherit !important;
            color: inherit !important;
            letter-spacing: -0.01em !important;
        }}

        /* Editorial Typography & Body Formatting */
        body, p, li, span {{
            -webkit-font-smoothing: antialiased !important;
            -moz-osx-font-smoothing: grayscale !important;
            text-rendering: optimizeLegibility !important;
        }}

        .vt-editorial-heading {{
            font-family: var(--vt-font-serif);
            font-size: 1.75rem;
            font-weight: 400;
            color: var(--vt-text-primary);
            line-height: 1.25;
            letter-spacing: -0.015em;
            margin: 0 0 4px 0;
        }}

        .vt-editorial-lead {{
            font-size: 0.88rem;
            color: var(--vt-text-secondary);
            line-height: 1.55;
            font-weight: 400;
            margin-bottom: 16px;
        }}

        .vt-editorial-kicker {{
            font-size: 0.69rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--vt-accent-primary);
            margin-bottom: 4px;
        }}

        /* Unified Stat Strip Cell with Smooth Hover Lift */
        .vt-stat-cell {{
            background: #FFFFFF !important;
            border: 1px solid var(--vt-border) !important;
            border-radius: 8px !important;
            padding: 13px 16px !important;
            margin-bottom: 10px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            min-height: 94px !important;
            box-sizing: border-box !important;
            width: 100% !important;
            transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s ease, border-color 0.22s ease !important;
        }}

        .vt-stat-cell:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05) !important;
            border-color: rgba(49, 95, 206, 0.35) !important;
        }}

        .vt-stat-label {{
            font-size: 0.69rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            color: var(--vt-text-secondary) !important;
            margin-bottom: 3px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }}

        .vt-stat-value {{
            font-size: 1.44rem !important;
            font-weight: 700 !important;
            color: var(--vt-text-primary) !important;
            line-height: 1.15 !important;
            letter-spacing: -0.02em !important;
            font-variant-numeric: tabular-nums !important;
            font-feature-settings: "tnum" 1 !important;
        }}

        .vt-stat-sub {{
            font-size: 0.74rem !important;
            color: var(--vt-text-secondary) !important;
            margin-top: 3px !important;
            font-weight: 400 !important;
            line-height: 1.35 !important;
        }}

        /* Modern Editorial Financial Metric Card */
        .vt-metric-card {{
            background: var(--vt-surface) !important;
            border: 1px solid var(--vt-border) !important;
            border-radius: 8px !important;
            padding: 14px 16px !important;
            margin-bottom: 12px !important;
            position: relative !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
            box-sizing: border-box !important;
            width: 100% !important;
            transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s ease, border-color 0.22s ease !important;
        }}

        .vt-metric-card:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05) !important;
            border-color: rgba(49, 95, 206, 0.35) !important;
        }}

        .vt-metric-label {{
            font-size: 0.70rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            color: var(--vt-text-secondary) !important;
            margin-bottom: 4px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }}

        .vt-metric-value {{
            font-size: 1.45rem !important;
            font-weight: 700 !important;
            color: var(--vt-text-primary) !important;
            line-height: 1.15 !important;
            letter-spacing: -0.02em !important;
            font-variant-numeric: tabular-nums !important;
            font-feature-settings: "tnum" 1 !important;
        }}

        .vt-metric-sub {{
            font-size: 0.75rem !important;
            color: var(--vt-text-secondary) !important;
            margin-top: 4px !important;
            font-weight: 400 !important;
        }}

        /* Top Operational Workspace Ribbon — Ultra Slim */
        .vt-topbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #FFFFFF;
            border: 1px solid var(--vt-border);
            border-radius: 6px;
            padding: 6px 14px;
            margin-bottom: 16px;
            font-size: 0.78rem;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
        }}

        /* Futuristic Pulse Dot with Glowing Keyframe Animation */
        @keyframes vtPulseAnim {{
            0% {{
                transform: scale(0.92);
                box-shadow: 0 0 0 0 rgba(22, 134, 106, 0.7);
            }}
            70% {{
                transform: scale(1.15);
                box-shadow: 0 0 0 6px rgba(22, 134, 106, 0);
            }}
            100% {{
                transform: scale(0.92);
                box-shadow: 0 0 0 0 rgba(22, 134, 106, 0);
            }}
        }}

        .vt-pulse-dot {{
            width: 7px;
            height: 7px;
            background-color: var(--vt-accent-growth);
            border-radius: 50%;
            display: inline-block;
            animation: vtPulseAnim 2s infinite ease-in-out;
        }}

        /* Clean Editorial Status Badges */
        .vt-badge {{
            display: inline-flex;
            align-items: center;
            gap: 3px;
            padding: 1px 6px;
            border-radius: 4px;
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }}

        .vt-badge-green {{
            background: #E8F5E9;
            color: #16866A;
            border: 1px solid #C8E6C9;
        }}

        .vt-badge-blue {{
            background: var(--vt-highlight);
            color: var(--vt-accent-primary);
            border: 1px solid rgba(49, 95, 206, 0.22);
        }}

        .vt-badge-amber {{
            background: #FEF3C7;
            color: #B45309;
            border: 1px solid #FDE68A;
        }}

        /* Section Break Headers */
        .vt-section-header {{
            border-bottom: 1px solid var(--vt-border);
            padding-bottom: 6px;
            margin-top: 18px;
            margin-bottom: 14px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}

        .vt-section-title {{
            font-size: 1.10rem;
            font-weight: 600;
            color: var(--vt-text-primary);
            letter-spacing: -0.01em;
        }}

        .vt-section-desc {{
            font-size: 0.79rem;
            color: var(--vt-text-secondary);
            margin-top: 2px;
        }}

        /* Editorial Container Cards */
        .vt-editorial-card {{
            background: var(--vt-surface);
            border: 1px solid var(--vt-border);
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 16px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        }}

        /* Streamlit DataFrames & Tables */
        div[data-testid="stDataFrame"], div[data-testid="stTable"] {{
            border: 1px solid var(--vt-border) !important;
            border-radius: 6px !important;
            overflow: hidden !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
            background: var(--vt-surface) !important;
        }}

        /* Streamlit Tabs */
        div[data-testid="stTabs"] button[role="tab"] {{
            color: var(--vt-text-secondary) !important;
            font-weight: 500 !important;
            font-size: 0.84rem !important;
            padding: 7px 14px !important;
            border-radius: 6px 6px 0 0 !important;
            transition: all 0.12s ease !important;
            border-bottom: 2px solid transparent !important;
        }}

        div[data-testid="stTabs"] button[role="tab"]:hover {{
            color: var(--vt-text-primary) !important;
            background: rgba(0, 0, 0, 0.02) !important;
        }}

        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
            color: var(--vt-accent-primary) !important;
            font-weight: 600 !important;
            border-bottom: 2px solid var(--vt-accent-primary) !important;
            background: transparent !important;
        }}

        /* Buttons & Download Triggers */
        div.stButton > button, div.stDownloadButton > button {{
            background: #FFFFFF !important;
            color: var(--vt-text-primary) !important;
            border: 1px solid var(--vt-border) !important;
            border-radius: 6px !important;
            padding: 0.42rem 0.95rem !important;
            font-weight: 500 !important;
            font-size: 0.82rem !important;
            transition: all 0.12s ease !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        }}

        div.stButton > button:hover, div.stDownloadButton > button:hover {{
            background: #FAFAFA !important;
            border-color: var(--vt-accent-primary) !important;
            color: var(--vt-accent-primary) !important;
        }}

        /* Form Inputs & Selects — Forced Clean Light Theme Overrides */
        div[data-testid="stTextInput"] input,
        div[data-baseweb="input"] input,
        div[data-baseweb="base-input"] input,
        input.st-bc,
        input.st-bd {{
            background-color: #FFFFFF !important;
            color: var(--vt-text-primary) !important;
            font-size: 0.84rem !important;
            padding: 7px 10px !important;
            border: none !important;
        }}

        div[data-baseweb="input"],
        div[data-baseweb="base-input"],
        div[data-testid="stTextInput"] > div > div {{
            background-color: #FFFFFF !important;
            border: 1px solid var(--vt-border) !important;
            border-radius: 6px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        }}

        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="base-input"]:focus-within,
        div[data-testid="stTextInput"] > div > div:focus-within {{
            border-color: var(--vt-accent-primary) !important;
            box-shadow: 0 0 0 2px rgba(49, 95, 206, 0.12) !important;
        }}

        input::placeholder {{
            color: var(--vt-text-muted) !important;
            opacity: 1 !important;
        }}

        /* Select & Multiselect Controls */
        div[data-baseweb="select"] > div {{
            background-color: #FFFFFF !important;
            border: 1px solid var(--vt-border) !important;
            border-radius: 6px !important;
            color: var(--vt-text-primary) !important;
            min-height: 34px !important;
        }}

        div[data-baseweb="select"] span {{
            color: var(--vt-text-primary) !important;
            font-size: 0.82rem !important;
        }}

        /* Multiselect Tags / Badges */
        div[data-baseweb="tag"] {{
            background-color: var(--vt-highlight) !important;
            border: 1px solid rgba(49, 95, 206, 0.20) !important;
            border-radius: 4px !important;
            padding: 1px 5px !important;
        }}

        div[data-baseweb="tag"] span {{
            color: var(--vt-accent-primary) !important;
            font-weight: 500 !important;
            font-size: 0.75rem !important;
        }}

        div[data-baseweb="tag"] svg {{
            fill: var(--vt-accent-primary) !important;
        }}

        /* Dropdown Menu Popover */
        div[data-baseweb="popover"],
        div[data-baseweb="menu"] {{
            background-color: #FFFFFF !important;
            border: 1px solid var(--vt-border) !important;
            border-radius: 6px !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08) !important;
        }}

        ul[role="listbox"] {{
            background-color: #FFFFFF !important;
        }}

        li[role="option"] {{
            background-color: #FFFFFF !important;
            color: var(--vt-text-primary) !important;
            font-size: 0.83rem !important;
        }}

        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {{
            background-color: var(--vt-highlight) !important;
            color: var(--vt-accent-primary) !important;
        }}

        /* Sidebar Specific Form Elements & Controls */
        section[data-testid="stSidebar"] label {{
            color: #4B5651 !important;
            font-size: 0.73rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            margin-bottom: 2px !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stRadio"] > label {{
            font-size: 0.68rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.09em !important;
            color: #8C9690 !important;
            text-transform: uppercase !important;
            margin-bottom: 6px !important;
            padding-left: 4px !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stTextInput"] > div > div,
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
            background-color: #FFFFFF !important;
            border: 1px solid #DCE3DC !important;
            border-radius: 7px !important;
            min-height: 33px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
            transition: all 0.15s ease !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stTextInput"] > div > div:focus-within,
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {{
            border-color: #315FCE !important;
            box-shadow: 0 0 0 2px rgba(49, 95, 206, 0.14) !important;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="select"] span {{
            font-size: 0.81rem !important;
            color: #55625B !important;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="tag"] {{
            background-color: #EEF3FD !important;
            border: 1px solid #D2E0FB !important;
            border-radius: 4px !important;
            padding: 1px 6px !important;
            margin: 2px !important;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="tag"] span {{
            color: #244AA6 !important;
            font-weight: 600 !important;
            font-size: 0.72rem !important;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="tag"] svg {{
            fill: #244AA6 !important;
        }}

        /* Checkboxes — Modern Interactive Cards */
        section[data-testid="stSidebar"] div[data-testid="stCheckbox"] {{
            background: #FFFFFF !important;
            border: 1px solid #DCE3DC !important;
            border-radius: 7px !important;
            padding: 7px 10px !important;
            margin-bottom: 7px !important;
            transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stCheckbox"]:hover {{
            border-color: rgba(49, 95, 206, 0.38) !important;
            background: #FDFEFF !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 2px 7px rgba(49, 95, 206, 0.07) !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stCheckbox"]:has(input:checked) {{
            border-color: rgba(49, 95, 206, 0.48) !important;
            background: #F6F9FF !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label {{
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            cursor: pointer !important;
            width: 100% !important;
            margin: 0 !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label div[data-testid="stMarkdownContainer"] {{
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label div[data-testid="stMarkdownContainer"] p {{
            white-space: nowrap !important;
            font-size: 0.79rem !important;
            font-weight: 500 !important;
            color: #17211F !important;
            margin: 0 !important;
            padding: 0 !important;
        }}

        /* Reset Button */
        section[data-testid="stSidebar"] div.stButton > button {{
            background: #FFFFFF !important;
            border: 1px solid #DCE3DC !important;
            color: #4A5750 !important;
            border-radius: 7px !important;
            font-weight: 600 !important;
            font-size: 0.78rem !important;
            letter-spacing: 0.02em !important;
            padding: 0.46rem 0.85rem !important;
            margin-top: 5px !important;
            margin-bottom: 4px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
            transition: all 0.18s ease !important;
            width: 100% !important;
        }}

        section[data-testid="stSidebar"] div.stButton > button:hover {{
            background: #F4F7FC !important;
            border-color: #315FCE !important;
            color: #315FCE !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 3px 8px rgba(49, 95, 206, 0.12) !important;
        }}

        /* Slider */
        div[data-testid="stSlider"] {{
            padding-left: 2px !important;
            padding-right: 2px !important;
            margin-bottom: 8px !important;
        }}

        div[data-testid="stSlider"] label {{
            color: var(--vt-text-primary) !important;
            font-size: 0.80rem !important;
            font-weight: 600 !important;
            margin-bottom: 2px !important;
        }}

        div[data-testid="stSlider"] div[role="slider"] {{
            background-color: var(--vt-accent-primary) !important;
            border-color: var(--vt-accent-primary) !important;
        }}

        /* Academic Callout */
        .vt-academic-callout {{
            background: #F4F7FC !important;
            border: 1px solid #DCE5F5 !important;
            border-left: 3px solid var(--vt-accent-primary) !important;
            border-radius: 6px !important;
            padding: 10px 14px !important;
            margin: 12px 0 16px 0 !important;
            color: var(--vt-text-primary) !important;
            font-size: 0.84rem !important;
            line-height: 1.45 !important;
        }}

        /* Code Box */
        .vt-code-card {{
            background: #F0F2EF !important;
            border: 1px solid var(--vt-border) !important;
            border-left: 3px solid var(--vt-accent-primary) !important;
            border-radius: 6px !important;
            padding: 10px 14px !important;
            margin: 10px 0 !important;
            font-family: var(--vt-font-mono) !important;
            font-size: 0.80rem !important;
            color: var(--vt-text-primary) !important;
        }}

        /* Streamlit Code Blocks */
        div[data-testid="stCodeBlock"] {{
            border: 1px solid var(--vt-border) !important;
            border-radius: 6px !important;
            margin-bottom: 12px !important;
        }}

        div[data-testid="stCodeBlock"] pre,
        div[data-testid="stCodeBlock"] code {{
            white-space: pre-wrap !important;
            word-break: break-word !important;
            font-size: 0.80rem !important;
            font-family: var(--vt-font-mono) !important;
            line-height: 1.45 !important;
        }}

        /* Responsive Breakpoints */
        @media (max-width: 900px) {{
            section[data-testid="stSidebar"] {{
                width: 100% !important;
                max-width: 100% !important;
            }}
            .main .block-container {{
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
            .vt-editorial-heading {{
                font-size: 1.45rem;
            }}
            .vt-topbar {{
                flex-direction: column;
                align-items: flex-start;
                gap: 5px;
            }}
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_brand_sidebar():
    """Renders the sleek, futuristic editorial fintech brand identity badge in the sidebar rail."""
    html = (
        f'<div style="padding: 2px 2px 12px 2px; border-bottom: 1px solid #E5E9E5; margin-bottom: 12px;">'
        f'<div style="display: flex; align-items: center; gap: 10px;">'
        f'<div style="width: 30px; height: 30px; background: linear-gradient(135deg, #315FCE 0%, #2045A8 100%); border-radius: 7px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.82rem; color: #FFFFFF; letter-spacing: 0.02em; box-shadow: 0 3px 10px rgba(49, 95, 206, 0.28);">VT</div>'
        f'<div>'
        f'<div style="font-size: 1.02rem; font-weight: 800; letter-spacing: -0.02em; color: {THEME_COLORS["primary_text"]}; line-height: 1.1; font-family: Inter, sans-serif;">{APP_NAME}</div>'
        f'<div style="font-size: 0.60rem; font-weight: 700; color: #315FCE; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px; display: flex; align-items: center; gap: 5px;">'
        f'<span class="vt-pulse-dot" style="width: 5px; height: 5px;"></span>FINANCIAL INTELLIGENCE'
        f'</div>'
        f'</div>'
        f'</div>'
        f'<div style="font-size: 0.72rem; color: #727D77; margin-top: 7px; line-height: 1.35; padding-left: 2px;">{APP_TAGLINE}</div>'
        f'</div>'
    )
    st.sidebar.markdown(html, unsafe_allow_html=True)


def render_top_workspace_bar(total_records: int, filtered_records: int, loaded_at: Optional[str] = None):
    """Renders a sleek, ultra-compact single-line top workspace status bar."""
    is_filtered = filtered_records != total_records
    status_text = (
        f"Filtered Scope: {filtered_records:,} of {total_records:,} Deals"
        if is_filtered
        else f"Full Cohort: {total_records:,} Deals"
    )
    timestamp_str = loaded_at or "Cached Pipeline"
    
    html = (
        f'<div class="vt-topbar">'
        f'<div style="display: flex; align-items: center; gap: 8px;">'
        f'<span class="vt-pulse-dot"></span>'
        f'<span style="color: {THEME_COLORS["growth_green"]}; font-weight: 600; font-size: 0.70rem; letter-spacing: 0.05em; text-transform: uppercase;">LIVE PIPELINE</span>'
        f'<span style="color: {THEME_COLORS["secondary_text"]}; font-weight: 500;">• &nbsp; {status_text}</span>'
        f'</div>'
        f'<div style="display: flex; align-items: center; gap: 10px;">'
        f'<span class="vt-badge vt-badge-blue">FX: ₹{USD_TO_INR_RATE} / USD</span>'
        f'<span style="color: {THEME_COLORS["muted_text"]}; font-size: 0.73rem; font-family: var(--vt-font-mono);">Synced: {timestamp_str}</span>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, badge: Optional[str] = None):
    """Renders a modern compact page header without wasting vertical space."""
    badge_html = f'<span class="vt-badge vt-badge-blue" style="margin-left: 8px; vertical-align: middle;">{badge}</span>' if badge else ""
    html = (
        f'<div style="margin-bottom: 14px;">'
        f'<div style="display: flex; align-items: baseline;">'
        f'<h1 style="font-size: 1.60rem; font-weight: 700; color: {THEME_COLORS["primary_text"]}; margin: 0; display: inline; letter-spacing: -0.015em;">{title}</h1>'
        f'{badge_html}'
        f'</div>'
        f'<div style="font-size: 0.82rem; color: {THEME_COLORS["secondary_text"]}; margin-top: 3px; margin-bottom: 0;">{subtitle}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_editorial_hero(headline: str, kicker: str = "EXECUTIVE BRIEFING", summary: Optional[str] = None):
    """Renders a refined editorial headline block in DM Serif Display."""
    summary_html = f'<div style="font-size: 0.88rem; color: {THEME_COLORS["secondary_text"]}; line-height: 1.45; margin-top: 5px;">{summary}</div>' if summary else ""
    html = (
        f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-left: 4px solid {THEME_COLORS["primary_accent"]}; border-radius: 8px; padding: 14px 18px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">'
        f'<div class="vt-editorial-kicker">{kicker}</div>'
        f'<div class="vt-editorial-heading" style="font-size: 1.48rem; margin-bottom: 2px;">{headline}</div>'
        f'{summary_html}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_stat_strip(stats: List[Dict[str, Any]]):
    """
    Renders a unified horizontal statistic strip across responsive Streamlit columns.
    Uses unindented single-line HTML per column, completely immune to Markdown parsing bugs.
    """
    cols = st.columns(len(stats))
    for i, s in enumerate(stats):
        badge_html = f'<span class="vt-badge vt-badge-blue">{s["badge"]}</span>' if s.get("badge") else ""
        sub_html = f'<div class="vt-stat-sub">{s["sub"]}</div>' if s.get("sub") else ""
        card_html = (
            f'<div class="vt-stat-cell">'
            f'<div class="vt-stat-label"><span>{s["label"]}</span>{badge_html}</div>'
            f'<div class="vt-stat-value">{s["value"]}</div>'
            f'{sub_html}'
            f'</div>'
        )
        with cols[i]:
            st.markdown(card_html, unsafe_allow_html=True)


def render_kpi_card(
    label: str,
    value: str,
    subtext: str,
    badge: Optional[str] = None,
    badge_type: str = "blue"
):
    """Renders a clean editorial numerical KPI card with tabular numerals."""
    badge_markup = f'<span class="vt-badge vt-badge-{badge_type}">{badge}</span>' if badge else ""
    card_html = (
        f'<div class="vt-metric-card">'
        f'<div class="vt-metric-label"><span>{label}</span>{badge_markup}</div>'
        f'<div class="vt-metric-value">{value}</div>'
        f'<div class="vt-metric-sub">{subtext}</div>'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)


def render_section_header(title: str, description: Optional[str] = None):
    """Renders a refined, compact section break header."""
    desc_html = f'<div class="vt-section-desc">{description}</div>' if description else ""
    html = (
        f'<div class="vt-section-header">'
        f'<div><div class="vt-section-title">{title}</div>{desc_html}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_editorial_card(title: str, items: List[str], kicker: Optional[str] = None):
    """Renders an editorial list or insight card on clean white surface."""
    kicker_html = f'<div class="vt-editorial-kicker">{kicker}</div>' if kicker else ""
    items_html = "".join([
        f'<div style="display: flex; align-items: flex-start; gap: 8px; padding: 6px 0; border-bottom: 1px solid #F0F2EF;">'
        f'<div style="color: {THEME_COLORS["primary_accent"]}; font-size: 0.90rem; line-height: 1.4;">•</div>'
        f'<div style="font-size: 0.84rem; color: {THEME_COLORS["primary_text"]}; line-height: 1.45;">{it}</div>'
        f'</div>'
        for it in items
    ])
    html = (
        f'<div class="vt-editorial-card">'
        f'{kicker_html}'
        f'<div style="font-size: 0.98rem; font-weight: 700; color: {THEME_COLORS["primary_text"]}; margin-bottom: 6px;">{title}</div>'
        f'{items_html}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_academic_callout(text: str, title: str = "METHODOLOGICAL NOTE"):
    """Renders an institutional academic callout box."""
    html = (
        f'<div class="vt-academic-callout">'
        f'<div style="font-size: 0.68rem; font-weight: 700; color: {THEME_COLORS["primary_accent"]}; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 3px;">{title}</div>'
        f'<div>{text}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
