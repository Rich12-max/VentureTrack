# VentureTrack — Final Quality Assurance & Academic Validation Report
**Academic Mini Project 13** | **Author:** Richa Sharma (`25BAI10049`)  
**Evaluation Scope:** Code Integrity, Unit Tests, Fresh Notebook Execution & Real Browser QA  
**Date & Time:** 2026-11-03 05:25 IST  

---

## 1. Quality Assurance Dashboard

```
========================================================================================
  VENTURETRACK — FINAL ACADEMIC VERIFICATION SUMMARY
========================================================================================
  [✓] Python Syntax & Compilation       : 100% Passed (py_compile across all files)
  [✓] Automated Pytest Test Suite      : 23 of 23 Passed (1.73s runtime)
  [✓] Fresh Kernel Notebook Execution  : 11 of 11 Code Cells Executed (Exit Code 0)
  [✓] Real Headless Browser QA (Chrome): All 10 Pages Inspected (0 HTML Leaks)
  [✓] Live Browser Interaction Tests   : Search, City Filter, CSV & PDF Verified
  [✓] Multi-Viewport Responsive Audit  : 1440px, 1280px, 1024px Verified
  [✓] Anti-Hardcoding Validation       : Verified on Dual Disjoint Mini-Datasets
========================================================================================
```

---

## 2. Automated Test Suite Results (`pytest tests/ -v`)

All 23 automated tests passed cleanly:

```
tests/test_analytics.py::test_dynamic_calculations_on_two_different_mini_datasets PASSED [  4%]
tests/test_analytics.py::test_edge_case_empty_dataset PASSED             [  8%]
tests/test_analytics.py::test_edge_case_missing_funding_amounts PASSED   [ 13%]
tests/test_analytics.py::test_edge_case_identical_values_qcut PASSED     [ 17%]
tests/test_cleaning.py::test_remove_unicode_escapes PASSED               [ 21%]
tests/test_cleaning.py::test_parse_numeric_amount PASSED                 [ 26%]
tests/test_cleaning.py::test_parse_date_safely PASSED                    [ 30%]
tests/test_cleaning.py::test_clean_raw_dataset_schema PASSED             [ 34%]
tests/test_features.py::test_task_1_inr_conversion_and_removal PASSED    [ 39%]
tests/test_features.py::test_task_2_apply_and_map PASSED                 [ 43%]
tests/test_features.py::test_task_3_cut_and_qcut PASSED                  [ 47%]
tests/test_features.py::test_task_4_date_and_time_extraction PASSED      [ 52%]
tests/test_features.py::test_task_5_transform_summary PASSED             [ 56%]
tests/test_views.py::test_all_pages_render_without_exception[Market Overview] PASSED [ 60%]
tests/test_views.py::test_all_pages_render_without_exception[Startup Explorer] PASSED [ 65%]
tests/test_views.py::test_all_pages_render_without_exception[Sector Intelligence] PASSED [ 69%]
tests/test_views.py::test_all_pages_render_without_exception[City Intelligence] PASSED [ 73%]
tests/test_views.py::test_all_pages_render_without_exception[Funding Rounds] PASSED [ 78%]
tests/test_views.py::test_all_pages_render_without_exception[Funding Distribution] PASSED [ 82%]
tests/test_views.py::test_all_pages_render_without_exception[Time & Era Analysis] PASSED [ 86%]
tests/test_views.py::test_all_pages_render_without_exception[Feature Engineering Lab] PASSED [ 91%]
tests/test_views.py::test_all_pages_render_without_exception[Data Laboratory] PASSED [ 95%]
tests/test_views.py::test_all_pages_render_without_exception[Insights & Reports] PASSED [100%]

======================== 23 passed, 2 warnings in 1.73s ========================
```

---

## 3. Jupyter Notebook Fresh-Kernel Verification

The academic notebook (`notebooks/VentureTrack_EDA.ipynb`) was compiled and executed from a clean Python 3.13 kernel via `nbconvert`:
- **Execution Command**: `jupyter nbconvert --to notebook --execute notebooks/VentureTrack_EDA.ipynb --output VentureTrack_EDA_executed.ipynb`
- **Total Code Cells**: 11 code cells executed in strict sequence (`execution_count=1` to `11`).
- **Uncaught Exceptions**: 0.
- **Visual Artifact Output**: Visualizations rendered cleanly to `notebooks/venturetrack_visualizations.png` using dynamic, agnostic path resolution.
- **Executed Notebook**: Persisted and verified at `notebooks/VentureTrack_EDA_executed.ipynb`.

---

## 4. Real Browser Inspection & Interaction Audit

Browser automation was performed using Google Chrome (`v156.0.8078.74`) and Selenium WebDriver connected to `http://localhost:8501`.

### A. All Ten Analytical Workspaces
1. **Market Overview**: Verified 4 macro KPI cards, dual timeline, and zero raw HTML strings.
2. **Startup Explorer**: Verified dynamic search input and Task 2 headline ticker.
3. **Sector Intelligence**: Verified capital concentration bar chart and category breakdowns.
4. **City Intelligence**: Verified Bengaluru vs Rest of India comparison module.
5. **Funding Rounds**: Verified Series A–F progression ladder and stage decomposition.
6. **Funding Distribution**: Verified contingency table and Small-tier-in-Q4 divergence proof.
7. **Time & Era Analysis**: Verified 5 Plotly charts (annual, quarterly, monthly, day-of-week, era).
8. **Feature Engineering Lab**: Verified 9 pandas primitive interactive execution demonstrations.
9. **Data Laboratory**: Verified schema report, nullity audit, and confirmed `funding_amount` drop.
10. **Insights & Reports**: Verified memo viewer, data preview tables, and download triggers.

### B. Live Browser Interaction Results
- **Startup Search Filter**: Searched `"Swiggy"`. Scoped active rows to matching records (**PASS**).
- **Metropolitan Hub Filter**: Scoped to `"Bengaluru"`. Updated live deal cohort to 851 deals (**PASS**).
- **Direct Jupyter Notebook Download**: Clicked `"Download .ipynb Notebook"`. Delivered `VentureTrack_EDA.ipynb` (**PASS**).
- **Cleaned & Raw CSV Downloads**: Direct one-click downloads for `startup_funding_cleaned.csv` and `startup_funding_raw.csv` (**PASS**).
- **Complete Academic Submission Bundle**: Clicked `"Download Complete Bundle (.zip)"`. Dynamically generated and delivered `VentureTrack_Submission_Bundle.zip` containing all notebooks, datasets, PDF reports, and documentation (**PASS**).
- **PDF Report Download**: Clicked `"Download PDF Briefing"`. Verified output file creation at `artifacts/browser_qa/downloads/VentureTrack_Executive_Briefing.pdf` (3,997 bytes) (**PASS**).
- **Filtered CSV Export**: Clicked `"Export Filtered CSV"`. Verified output file creation at `artifacts/browser_qa/downloads/venturetrack_dataset_filtered.csv` (37,051 bytes) (**PASS**).

### C. Responsive Viewport Status
- **1440px (Desktop)**: Optimal editorial layout with full sidebar and 4-column metric strip.
- **1280px (Laptop)**: Fluid layout with no horizontal container overflow.
- **1024px (Narrow Viewport)**: Cards and tables maintain layout stability without clipping.

