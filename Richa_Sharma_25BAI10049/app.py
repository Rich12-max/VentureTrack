"""
VentureTrack — Indian Startup Funding Intelligence Platform
Main Streamlit Application Entrypoint
Academic Mini Project 13 | Author: Richa Sharma (25BAI10049)
"""
import streamlit as st

# 1. Page Configuration (Fintech Institutional Research Terminal)
st.set_page_config(
    page_title="VentureTrack — Indian Startup Funding Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Design System & CSS Injection
from src.ui_components import (
    inject_custom_css,
    render_brand_sidebar,
    render_top_workspace_bar,
)
inject_custom_css()

# 3. Data Loading
from src.data_loader import get_engineered_dataset, get_dataset_metadata
from src.filters import render_sidebar_filters

# Load cached engineered dataset
try:
    master_df = get_engineered_dataset()
    meta = get_dataset_metadata()
except Exception as e:
    st.error(f"Critical Data Pipeline Failure: {e}")
    st.stop()

# 4. Brand & Sidebar Navigation Rail
render_brand_sidebar()

NAV_PAGES = [
    "Market Overview",
    "Startup Explorer",
    "Sector Intelligence",
    "City Intelligence",
    "Funding Rounds",
    "Funding Distribution",
    "Time & Era Analysis",
    "Feature Engineering Lab",
    "Data Laboratory",
    "Insights & Reports"
]

selected_page = st.sidebar.radio(
    "NAVIGATION RAIL",
    options=NAV_PAGES,
    index=0,
    help="Select an analytical intelligence workspace"
)

# 5. Global Filter Controls in Sidebar
filtered_df, filter_state = render_sidebar_filters(master_df)

# Sidebar Academic Footer
sidebar_footer_html = (
    '<div style="background: #FFFFFF; border: 1px solid #DCE3DC; border-radius: 7px; padding: 9px 11px; margin-top: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">'
    '<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 2px;">'
    '<span style="font-weight: 700; color: #17211F; letter-spacing: 0.05em; text-transform: uppercase; font-size: 0.68rem;">VENTURETRACK</span>'
    '<span style="background: #E8F5E9; color: #16866A; font-weight: 700; font-size: 0.60rem; padding: 1px 5px; border-radius: 4px; border: 1px solid #C8E6C9;">v2.4</span>'
    '</div>'
    '<div style="color: #16866A; font-weight: 600; font-size: 0.67rem;">Academic Edition — Mini Project 13</div>'
    '<div style="margin-top: 5px; padding-top: 5px; border-top: 1px solid #F0F2EF; color: #727D77; font-size: 0.69rem; line-height: 1.4;">'
    'Author: <b style="color: #17211F;">Richa Sharma</b> &nbsp;·&nbsp; Reg: <span style="font-family: var(--vt-font-mono); color: #315FCE; font-weight: 700;">25BAI10049</span>'
    '</div>'
    '</div>'
)
st.sidebar.markdown(sidebar_footer_html, unsafe_allow_html=True)

# 6. Top Operational Status Bar
render_top_workspace_bar(
    total_records=len(master_df),
    filtered_records=len(filtered_df),
    loaded_at=meta.get("loaded_at")
)

# 7. Page Router
from views import (
    overview,
    startup_explorer,
    sector_intelligence,
    city_intelligence,
    funding_rounds,
    funding_distribution,
    time_analysis,
    feature_lab,
    data_laboratory,
    reports,
)

if selected_page == "Market Overview":
    overview.render(filtered_df)
elif selected_page == "Startup Explorer":
    startup_explorer.render(filtered_df)
elif selected_page == "Sector Intelligence":
    sector_intelligence.render(filtered_df)
elif selected_page == "City Intelligence":
    city_intelligence.render(filtered_df)
elif selected_page == "Funding Rounds":
    funding_rounds.render(filtered_df)
elif selected_page == "Funding Distribution":
    funding_distribution.render(filtered_df)
elif selected_page == "Time & Era Analysis":
    time_analysis.render(filtered_df)
elif selected_page == "Feature Engineering Lab":
    feature_lab.render(filtered_df)
elif selected_page == "Data Laboratory":
    data_laboratory.render(filtered_df)
elif selected_page == "Insights & Reports":
    reports.render(filtered_df, master_df)

