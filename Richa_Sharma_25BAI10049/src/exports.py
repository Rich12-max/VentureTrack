"""
VentureTrack Export & Intelligence Distribution Module
Handles CSV dataset serialization and institutional PDF executive report generation.
"""
from typing import Dict, Any, Optional
import io
import pandas as pd
import numpy as np

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from src.insights import generate_task5_interpretation


def export_dataframe_to_csv(df: pd.DataFrame) -> bytes:
    """Serializes a DataFrame to CSV bytes for client-side download."""
    return df.to_csv(index=False).encode("utf-8")


def generate_executive_pdf_report(df: pd.DataFrame, kpis: Dict[str, Any]) -> bytes:
    """
    Constructs an institutional PDF Executive Investment Intelligence Report
    using ReportLab Flowables and styling.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom ReportLab Styles
    header_style = ParagraphStyle(
        "FintechHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#17211F"),
    )
    
    subtitle_style = ParagraphStyle(
        "FintechSub",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#315FCE"),
    )
    
    meta_style = ParagraphStyle(
        "FintechMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748B"),
    )
    
    section_title = ParagraphStyle(
        "FintechSec",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=12,
        spaceAfter=6,
    )
    
    body_style = ParagraphStyle(
        "FintechBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
    )

    story = []
    
    # Header Banner
    story.append(Paragraph("VENTURETRACK — EXECUTIVE INTELLIGENCE MEMO", header_style))
    story.append(Paragraph("INDIAN STARTUP FUNDING INTELLIGENCE PLATFORM | MINI PROJECT 13", subtitle_style))
    story.append(Paragraph(f"Generated at: {pd.Timestamp.now().strftime('%d %B %Y, %H:%M:%S')} UTC | Exchange Baseline: ₹83 / USD", meta_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#315FCE"), spaceAfter=12))
    
    # 1. Executive Summary Table
    story.append(Paragraph("1. Macro Ecosystem Metrics", section_title))
    
    kpi_data = [
        ["Metric", "Value", "Metric", "Value"],
        ["Total Tracked Deals", f"{kpis['total_records']:,}", "Active Startups", f"{kpis['unique_startups']:,}"],
        ["Total Capital Deployed", f"₹{kpis['total_funding_crores']:,.2f} Cr", "Average Deal Size", f"₹{kpis['avg_funding_crores']:,.2f} Cr"],
        ["Median Deal Size", f"₹{kpis['median_funding_crores']:,.2f} Cr", "Bengaluru Share (%)", f"{kpis['bengaluru_pct']}%"],
        ["Above Sector Avg (%)", f"{kpis['above_sector_avg_pct']}%", "Top Funded Entity", f"{kpis['top_funded_startup']} (₹{kpis['top_funded_amount']:,.2f} Cr)"],
    ]
    
    kpi_table = Table(kpi_data, colWidths=[140, 130, 140, 130])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17211F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
        ("FONTNAME", (1, 1), (1, -1), "Helvetica-Bold"),
        ("FONTNAME", (3, 1), (3, -1), "Helvetica-Bold"),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 10))
    
    # 2. Academic Synthesis
    story.append(Paragraph("2. Research Findings & Analytical Interpretation (Task 5)", section_title))
    interp_text = generate_task5_interpretation(df)
    story.append(Paragraph(interp_text, body_style))
    story.append(Spacer(1, 12))
    
    # 3. Top Sector Rankings
    story.append(Paragraph("3. Sector Concentration (Top 5 by Capital)", section_title))
    valid = df.dropna(subset=["funding_crores"]).copy()
    if len(valid) > 0:
        sec_agg = valid.groupby("sector").agg(
            deals=("startup_name", "count"),
            total=("funding_crores", "sum"),
            avg=("funding_crores", "mean")
        ).reset_index().sort_values(by="total", ascending=False).head(5)
        
        sec_data = [["Sector", "Deals", "Total Capital (₹ Cr)", "Avg Deal (₹ Cr)"]]
        for _, row in sec_agg.iterrows():
            sec_data.append([
                str(row["sector"])[:25],
                f"{int(row['deals']):,}",
                f"₹{row['total']:,.2f}",
                f"₹{row['avg']:,.2f}",
            ])
            
        sec_table = Table(sec_data, colWidths=[200, 80, 130, 130])
        sec_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#315FCE")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
        ]))
        story.append(sec_table)
        
    story.append(Spacer(1, 14))
    
    # Signoff footer
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#94A3B8"), spaceAfter=6))
    story.append(Paragraph("VentureTrack Academic Research Platform — Built for Mini Project 13 | Author: Richa Sharma (25BAI10049)", meta_style))
    
    doc.build(story)
    return buffer.getvalue()


def get_jupyter_notebook_bytes() -> bytes:
    """Reads the verified Jupyter Notebook bytes for direct user download."""
    import os
    from src.config import BASE_DIR
    candidate_paths = [
        BASE_DIR / "notebooks" / "VentureTrack_EDA.ipynb",
        BASE_DIR / "notebooks" / "VentureTrack_EDA_executed.ipynb",
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            with open(p, "rb") as f:
                return f.read()
    return b"{}"


def get_cleaned_dataset_bytes() -> bytes:
    """Reads the canonical cleaned dataset bytes."""
    import os
    from src.config import CLEANED_DATA_PATH
    if os.path.exists(CLEANED_DATA_PATH):
        with open(CLEANED_DATA_PATH, "rb") as f:
            return f.read()
    return b""


def get_raw_dataset_bytes() -> bytes:
    """Reads the preserved raw Kaggle dataset bytes."""
    import os
    from src.config import RAW_DATA_PATH
    if os.path.exists(RAW_DATA_PATH):
        with open(RAW_DATA_PATH, "rb") as f:
            return f.read()
    return b""


def create_submission_bundle_zip(df: pd.DataFrame, kpis: Dict[str, Any]) -> bytes:
    """
    Constructs a complete academic submission ZIP package containing:
    - Jupyter Notebook (.ipynb)
    - Cleaned Dataset (.csv)
    - Raw Dataset (.csv)
    - Filtered Dataset (.csv)
    - Executive PDF Memorandum (.pdf)
    - Master Documentation (README.md)
    """
    import zipfile
    import os
    from src.config import BASE_DIR
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Notebook
        nb_bytes = get_jupyter_notebook_bytes()
        if nb_bytes:
            zf.writestr("notebooks/VentureTrack_EDA.ipynb", nb_bytes)
            
        # 2. Cleaned Dataset
        clean_bytes = get_cleaned_dataset_bytes()
        if clean_bytes:
            zf.writestr("data/startup_funding_cleaned.csv", clean_bytes)
            
        # 3. Raw Dataset
        raw_bytes = get_raw_dataset_bytes()
        if raw_bytes:
            zf.writestr("data/startup_funding_raw.csv", raw_bytes)
            
        # 4. Filtered active CSV
        zf.writestr("exports/venturetrack_active_dataset.csv", export_dataframe_to_csv(df))
        
        # 5. Generated PDF Memo
        try:
            pdf_bytes = generate_executive_pdf_report(df, kpis)
            zf.writestr("reports/VentureTrack_Executive_Briefing.pdf", pdf_bytes)
        except Exception:
            pass
            
        # 6. README.md & Requirements
        for fname in ["README.md", "requirements.txt"]:
            fpath = BASE_DIR / fname
            if os.path.exists(fpath):
                with open(fpath, "rb") as f:
                    zf.writestr(fname, f.read())
                    
    return zip_buffer.getvalue()


