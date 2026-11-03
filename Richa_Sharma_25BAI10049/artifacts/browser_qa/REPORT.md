# VentureTrack — Real Browser Verification & QA Report
**Academic Mini Project 13** | **Author:** Richa Sharma (`25BAI10049`)  
**Execution Environment:** macOS Darwin | Google Chrome Headless Engine (`v156.0.8078.74`) | Selenium WebDriver `4.42.0`  
**Application URL:** `http://localhost:8501` (Live Streamlit Server)  
**Date & Time:** 2026-11-03 05:22 IST  

---

## Executive Summary

| Category | Target | Result | Status |
| :--- | :--- | :--- | :--- |
| **All 10 Workspaces Rendered** | Zero raw HTML leaks, zero unrendered markdown code blocks | 0 leaks detected across all pages | **PASS** |
| **Top Header Strip** | Zero black/dark strip; light `#F7F8F6` background | Root computed color: `rgb(247, 248, 246)` | **PASS** |
| **Interactive Controls** | Real browser navigation, search, city filters | Filters trigger real-time DOM reactivity | **PASS** |
| **File Exports** | Real browser download clicks for CSV & PDF | `CSV` (37,051 B) & `PDF` (3,995 B) verified | **PASS** |
| **Responsive Viewports** | 1440px desktop, 1280px laptop, 1024px narrow | Fluid layout, no horizontal scroll/overflow | **PASS** |
| **Automated Test Suite** | Full py_compile & pytest validation | 23 of 23 tests passed | **PASS** |

---

## 1. Page-by-Page Real Browser Inspection (1440px Desktop)

All 10 analytical workspaces were navigated sequentially in a real browser instance. Screenshots have been persisted to `artifacts/browser_qa/`.

| # | Workspace Name | Raw HTML Leaks | Charts Active | DataFrames | Error Banners | Screenshot Filename | Status |
| :-: | :--- | :-: | :-: | :-: | :-: | :--- | :-: |
| 1 | **Market Overview** | 0 | 3 | 0 | 0 | `01_market_overview_1440px.png` | **PASS** |
| 2 | **Startup Explorer** | 0 | 0 | 1 | 0 | `02_startup_explorer_1440px.png` | **PASS** |
| 3 | **Sector Intelligence** | 0 | 2 | 2 | 0 | `03_sector_intelligence_1440px.png` | **PASS** |
| 4 | **City Intelligence** | 0 | 1 | 1 | 0 | `04_city_intelligence_1440px.png` | **PASS** |
| 5 | **Funding Rounds** | 0 | 2 | 1 | 0 | `05_funding_rounds_1440px.png` | **PASS** |
| 6 | **Funding Distribution** | 0 | 4 | 2 | 0 | `06_funding_distribution_1440px.png` | **PASS** |
| 7 | **Time & Era Analysis** | 0 | 5 | 1 | 0 | `07_time_and_era_analysis_1440px.png` | **PASS** |
| 8 | **Feature Engineering Lab** | 0 | 0 | 2 | 0 | `08_feature_engineering_lab_1440px.png` | **PASS** |
| 9 | **Data Laboratory** | 0 | 0 | 2 | 0 | `09_data_laboratory_1440px.png` | **PASS** |
| 10 | **Insights & Reports** | 0 | 0 | 4 | 0 | `10_insights_and_reports_1440px.png` | **PASS** |

---

## 2. Interaction & Dynamic Reactivity Testing

Real DOM interactions were executed and verified against live Streamlit session state:

### A. Live Startup Search Interaction
- **Tested Search String**: `"Swiggy"` entered into the sidebar search input.
- **Result**: The active scoped view dynamically filtered to Swiggy transactions.
- **Screenshot**: `artifacts/browser_qa/interaction_search_swiggy.png` (**PASS**).

### B. Metropolitan Hub Filter Interaction
- **Tested Selection**: Metropolitan Hub scoped to `"Bengaluru"`.
- **Result**: Filter propagated across session state; top workspace bar scoped total deals from 3,044 down to 851 deals.
- **Screenshot**: `artifacts/browser_qa/interaction_filter_bengaluru.png` (**PASS**).

### C. Live Export & Download Triggering
- **PDF Memorandum Download**: Real browser click on the `"Download PDF Briefing"` trigger.
  - Downloaded File: `artifacts/browser_qa/downloads/VentureTrack_Executive_Briefing.pdf` (3,995 bytes).
  - Status: **PASS**.
- **Filtered CSV Dataset Export**: Real browser click on `"Export Filtered CSV"`.
  - Downloaded File: `artifacts/browser_qa/downloads/venturetrack_dataset_filtered.csv` (37,051 bytes).
  - Status: **PASS**.

---

## 3. Responsive Viewport Analysis

| Viewport | Device Profile | Visual & Layout Observations | Screenshot | Status |
| :--- | :--- | :--- | :--- | :-: |
| **1440 × 900** | Standard Desktop / Widescreen | Full 260px sidebar rail, balanced 4-column KPI strip, expansive Plotly charts | `01_market_overview_1440px.png` | **PASS** |
| **1280 × 800** | MacBook / Mid-size Laptop | Fluid grid maintains padding; no horizontal scrollbar on main container | `responsive_1280px_market_overview.png` | **PASS** |
| **1024 × 768** | Narrow Desktop / Tablet Landscape | Sidebar adjusts cleanly, columns gracefully stack or scale without text truncation | `responsive_1024px_market_overview.png` | **PASS** |

---

## 4. Final Compilation & Test Verification

```bash
python3 -m py_compile app.py src/*.py views/*.py tests/*.py
# Result: Exit Code 0 (Zero syntax errors)

pytest tests/ -v
# Result: 23 passed in 1.73s (Exit Code 0)
```

