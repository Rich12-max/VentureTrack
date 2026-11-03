"""
VentureTrack View 9: Data Laboratory
Performs complete dataset diagnostic auditing, schema verification, nullity analysis, and quality health checks.
Technical inspection workspace with data hygiene metrics and schema compliance verification.
"""
import streamlit as st
import pandas as pd

from src.analytics import get_data_quality_report
from src.data_loader import validate_schema, get_dataset_metadata
from src.feature_engineering import get_column_removal_explanation
from src.ui_components import (
    render_page_header,
    render_stat_strip,
    render_section_header,
    render_academic_callout,
)
from src.config import THEME_COLORS


def render(df: pd.DataFrame):
    """Renders the Data Laboratory auditing workspace with a technical inspection layout."""
    render_page_header(
        title="Data Laboratory",
        subtitle="Data Hygiene Diagnostics, Schema Verification & Nullity Audit",
        badge="Quality Assurance"
    )
    
    dq = get_data_quality_report(df)
    is_valid_schema, schema_issues = validate_schema(df)
    meta = get_dataset_metadata()

    # 1. Technical Health Diagnostics Strip
    schema_status = "Compliant" if is_valid_schema else "Non-Compliant"
    health_strip = [
        {
            "label": "Total Matrix Dimensions",
            "value": f"{dq['total_records']:,} × {dq['total_columns']}",
            "sub": f"{dq['memory_usage_mb']} MB In-Memory",
            "badge": "Shape"
        },
        {
            "label": "Schema Verification",
            "value": schema_status,
            "sub": "Tasks 1-5 Schema Enforced",
            "badge": "Pass" if is_valid_schema else "Alert"
        },
        {
            "label": "Duplicate Rows",
            "value": f"{dq['duplicates_count']:,}",
            "sub": "Entity + Date + Round Key",
            "badge": "Clean"
        },
        {
            "label": "Missing Dates (NaT)",
            "value": f"{dq['invalid_dates_count']:,}",
            "sub": "Preserved as Missing",
        },
    ]
    render_stat_strip(health_strip)

    # 2. Task 1 Column Removal Verification (Crucial Assignment Requirement)
    render_section_header("Task 1 Column Audit: Standardized funding_amount Removal", "Explicit verification that the raw working column has been dropped from the final enriched DataFrame")
    
    col_rem1, col_rem2 = st.columns([1, 1])
    with col_rem1:
        funding_amt_dropped = "funding_amount" not in df.columns
        status_color = THEME_COLORS["growth_green"] if funding_amt_dropped else THEME_COLORS["danger_red"]
        status_text = "PASSED: 'funding_amount' is successfully dropped from final DataFrame" if funding_amt_dropped else "FAILED: 'funding_amount' still present"
        
        status_card = (
            f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-left: 4px solid {status_color}; padding: 12px 16px; border-radius: 6px; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">'
            f'<div style="font-weight: 700; color: {status_color}; font-size: 0.90rem; margin-bottom: 3px;">{status_text}</div>'
            f'<div style="font-size: 0.78rem; color: {THEME_COLORS["secondary_text"]};">Verified columns in active engineered DataFrame: <code>{len(df.columns)} columns present</code></div>'
            f'</div>'
        )
        st.markdown(status_card, unsafe_allow_html=True)
        
        # Display formatted multi-line Python list with line-breaks so it wraps cleanly without horizontal overflow
        formatted_cols = "[\n" + ",\n".join([f"    '{col}'" for col in df.columns]) + "\n]"
        st.caption("Active Schema Columns (`df.columns` — 26 Features):")
        st.code(formatted_cols, language="python")
    with col_rem2:
        explanations = get_column_removal_explanation()
        justification_card = (
            f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-radius: 8px; padding: 14px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">'
            f'<div style="font-size: 0.70rem; font-weight: 700; color: {THEME_COLORS["primary_accent"]}; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;">METHODOLOGICAL GOVERNANCE</div>'
            f'<div style="font-size: 1.02rem; font-weight: 700; color: {THEME_COLORS["primary_text"]}; margin-bottom: 10px;">When to Drop vs Retain a Raw Feature</div>'
            f'<div style="margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #F0F2EF;">'
            f'<div style="font-size: 0.76rem; font-weight: 700; color: {THEME_COLORS["danger_red"]}; text-transform: uppercase; margin-bottom: 2px;">• Rationale for Dropping (Standardized funding_amount):</div>'
            f'<div style="font-size: 0.81rem; color: {THEME_COLORS["secondary_text"]}; line-height: 1.45;">{explanations["rationale_for_dropping"]}</div>'
            f'</div>'
            f'<div>'
            f'<div style="font-size: 0.76rem; font-weight: 700; color: {THEME_COLORS["growth_green"]}; text-transform: uppercase; margin-bottom: 2px;">• Rationale for Retaining Derived Features:</div>'
            f'<div style="font-size: 0.82rem; color: {THEME_COLORS["secondary_text"]}; line-height: 1.45;">{explanations["rationale_for_retaining"]}</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(justification_card, unsafe_allow_html=True)

    # 3. Project Deliverables & Submission Downloads Section
    from src.exports import (
        get_jupyter_notebook_bytes,
        get_cleaned_dataset_bytes,
        get_raw_dataset_bytes,
        create_submission_bundle_zip,
        generate_executive_pdf_report,
        export_dataframe_to_csv,
    )
    from src.analytics import calculate_market_kpis

    render_section_header("Academic Deliverables & Artifact Downloads", "Direct one-click downloads for Jupyter Notebook, Cleaned Dataset, Raw Data, and Submission Bundle")
    d_col1, d_col2, d_col3, d_col4 = st.columns(4)

    with d_col1:
        st.markdown(
            f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-top: 3px solid {THEME_COLORS["primary_accent"]}; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px;">'
            f'<div style="font-weight: 700; color: {THEME_COLORS["primary_text"]}; font-size: 0.86rem; margin-bottom: 2px;">Jupyter Notebook (.ipynb)</div>'
            f'<div style="font-size: 0.73rem; color: {THEME_COLORS["secondary_text"]}; line-height: 1.35;">Fully executed EDA notebook covering Tasks 1 through 5 with rendered charts.</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        nb_data = get_jupyter_notebook_bytes()
        st.download_button(
            label="Download .ipynb Notebook",
            data=nb_data,
            file_name="VentureTrack_EDA.ipynb",
            mime="application/x-ipynb+json",
            use_container_width=True
        )

    with d_col2:
        st.markdown(
            f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-top: 3px solid {THEME_COLORS["secondary_accent"]}; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px;">'
            f'<div style="font-weight: 700; color: {THEME_COLORS["primary_text"]}; font-size: 0.86rem; margin-bottom: 2px;">Cleaned Dataset (.csv)</div>'
            f'<div style="font-size: 0.73rem; color: {THEME_COLORS["secondary_text"]}; line-height: 1.35;">Sanitized canonical dataset (3,044 deals) without missing value distortion.</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        clean_data = get_cleaned_dataset_bytes()
        st.download_button(
            label="Download Cleaned CSV",
            data=clean_data,
            file_name="startup_funding_cleaned.csv",
            mime="text/csv",
            use_container_width=True
        )

    with d_col3:
        st.markdown(
            f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-top: 3px solid {THEME_COLORS["warning_amber"]}; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px;">'
            f'<div style="font-weight: 700; color: {THEME_COLORS["primary_text"]}; font-size: 0.86rem; margin-bottom: 2px;">Raw Kaggle Data (.csv)</div>'
            f'<div style="font-size: 0.73rem; color: {THEME_COLORS["secondary_text"]}; line-height: 1.35;">Preserved source dataset from Kaggle curator Sudalai Rajkumar (3,044 deals).</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        raw_data = get_raw_dataset_bytes()
        st.download_button(
            label="Download Raw Kaggle CSV",
            data=raw_data,
            file_name="startup_funding_raw.csv",
            mime="text/csv",
            use_container_width=True
        )

    with d_col4:
        st.markdown(
            f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-top: 3px solid #6366F1; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px;">'
            f'<div style="font-weight: 700; color: {THEME_COLORS["primary_text"]}; font-size: 0.86rem; margin-bottom: 2px;">Submission Bundle (.zip)</div>'
            f'<div style="font-size: 0.73rem; color: {THEME_COLORS["secondary_text"]}; line-height: 1.35;">All-in-one package: Notebook, Datasets, PDF Briefing, and README.md.</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        kpis_lab = calculate_market_kpis(df)
        zip_bundle = create_submission_bundle_zip(df, kpis_lab)
        st.download_button(
            label="Download Bundle (.zip)",
            data=zip_bundle,
            file_name="VentureTrack_Academic_Submission_Bundle.zip",
            mime="application/zip",
            use_container_width=True
        )

    # 3. Missing Value & Nullity Report
    render_section_header("Field Nullity & Data Type Analysis", "Granular column breakdown with missing value counts and percentages")
    st.dataframe(
        dq["missing_table"],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Column": st.column_config.TextColumn("Column Name", width="medium"),
            "Data Type": st.column_config.TextColumn("Dtype", width="small"),
            "Missing Count": st.column_config.NumberColumn("Missing Values", format="%d"),
            "Missing Pct (%)": st.column_config.NumberColumn("Missing Rate", format="%.2f%%"),
            "Unique Values": st.column_config.NumberColumn("Cardinality", format="%d"),
        }
    )

    # 4. Numeric Summary Statistics
    render_section_header("Parametric Descriptive Statistics", "Empirical summary metrics for numerical and engineered features")
    st.dataframe(df.describe(include=[float, int]).round(2), use_container_width=True)

    # 5. Methodological Note
    render_academic_callout(
        "Notice that missing values in funding amounts (~31% of raw Kaggle dataset) are deliberately preserved as NaN "
        "rather than imputed with artificial medians or synthetic zeroes. In financial intelligence, fabricating undisclosed "
        "funding figures introduces catastrophic survivorship bias and distorts actual deal benchmarks.",
        title="DATA PRESERVATION INTEGRITY"
    )
