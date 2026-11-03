# VENTURETRACK — INDIAN STARTUP FUNDING INTELLIGENCE
### Institutional Venture Capital Research Terminal | Academic Mini Project 13

**Tagline**: *Understand Funding. Discover Patterns. Evaluate Opportunities.*  
**Author**: Richa Sharma  
**Registration Number**: `25BAI10049`  
**Course / Discipline**: [B.Tech / Academic Department Placeholder]  
**Faculty / Mentor**: [Faculty Supervisor Placeholder]  
**Academic Deliverable**: Mini Project 13 (Feature Engineering Primitives & Exploratory Venture Intelligence)  

---

## 1. Project Title & Overview

**VentureTrack** is an institutional venture capital intelligence and research platform engineered to analyze, benchmark, and evaluate the Indian startup ecosystem. Built using modern data engineering and analytical frameworks, VentureTrack transforms 3,044 historical transactions (2015–2020) from the curated Indian Startup Funding dataset into actionable venture intelligence.

Unlike generic dashboard templates or conventional analytics projects, VentureTrack implements a dedicated **Modern Editorial Fintech Intelligence** architecture inspired by institutional platforms such as Linear, Stripe, Mercury, and Bloomberg research interfaces. The system adheres strictly to the assignment's **No Hardcoding Policy**: all Key Performance Indicators (KPIs), charts, peer comparisons, and editorial briefings are computed dynamically on-the-fly from the underlying pandas feature engineering pipeline.

```
====================================================================================================
  VT ❖ VENTURETRACK — INDIAN STARTUP FUNDING INTELLIGENCE PLATFORM (v2.4.0)
====================================================================================================
  Status: REPOSITORY SYNCED (3,044 RECORDS)  |  FX Benchmark: ₹83.00 / USD  |  Engine: Pandas 2.x
====================================================================================================
```

---

## 2. Problem Statement

The Indian venture capital ecosystem is characterized by high information asymmetry, extreme capital concentration, and non-standard deal reporting:
1. **Multivariate Formatting Irregularities**: Raw venture transaction disclosures contain inconsistent round designations (e.g., `'Seed/Angel Funding'` vs `'Seed\\nFunding'`), typographical errors in dates (e.g., `'05/072018'`), uncurated Unicode non-breaking spaces (`\xc2\xa0`), and mixed currency representations.
2. **Extreme Power-Law Skewness**: Startup funding distributions do not follow Gaussian normal distributions. Outlier mega-rounds heavily distort arithmetic means, rendering standard aggregate summaries misleading without non-parametric median analysis and group-level broadcasting.
3. **Collinearity and Redundancy**: Dual-currency recording (USD and INR) leads to redundant columns, doubling memory footprint and introducing multi-collinearity into quantitative workflows.
4. **Disconnection Between Engineering & Delivery**: Academic data science projects often isolate data transformation code in disconnected notebooks, lacking interactive, defensible visual interfaces for stakeholder validation.

---

## 3. Project Objectives

1. **Robust Data Sanitization**: Build an auditable, non-destructive cleaning pipeline that standardizes raw Kaggle data into a canonical internal schema without data loss or fabricated imputation.
2. **Rigorous Feature Engineering (Tasks 1–5)**:
   - *Task 1*: Compute standardized `funding_crores` at ₹83/USD, derive boolean `is_bengaluru`, initialize `investor_count` with `NaN`, and drop redundant USD amounts.
   - *Task 2*: Engineer numerical `round_number` via `apply()`, map macro `sector_category` via `map()`, and synthesize natural language `headline` summaries via row-wise `apply(axis=1)`.
   - *Task 3*: Discretize transaction sizes into fixed monetary tiers (`funding_tier`) via `pd.cut()` and relative cohorts (`funding_quartile`) via `pd.qcut()`, providing mathematical proof of empirical divergence.
   - *Task 4*: Extract temporal primitives (`year`, `month`, `quarter`, `day_of_week`, `month_name`), calculate dynamic `days_since_funding`, and classify macroeconomic `funding_era`.
   - *Task 5*: Compute sector-level benchmark averages and peer outperformance flags (`above_sector_avg`) using `groupby().transform('mean')`, synthesizing academic macro findings.
3. **Interactive Visual Intelligence Platform**: Deliver 10 dedicated Streamlit analytical workspaces showcasing data distribution, geographic hubs, stage ladders, interactive pandas primitives, data hygiene diagnostics, and exportable PDF/CSV reports.
4. **Reproducibility & Verification**: Validate the end-to-end architecture with automated unit tests, headless real browser inspection, and fresh-kernel notebook execution.

---

## 4. Dataset Source & Attribution

- **Origin**: Kaggle Indian Startup Funding Dataset
- **Curator**: Sudalai Rajkumar
- **Public URL**: [https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding)
- **Time Window**: January 2015 to January 2020
- **Cohort Size**: 3,044 raw venture capital investment deals across 2,457 unique startups.
- **Raw File**: `data/startup_funding_raw.csv` (Preserved source, never mutated).
- **Cleaned File**: `data/startup_funding_cleaned.csv` (Canonical cleaned dataset).
- **Lineage Disclosure**: The cleaned dataset from Mini Project 12 was not supplied in the workspace; an auditable, reproducible cleaning pipeline was constructed in `src/cleaning.py` to produce canonical output.

For comprehensive column-by-column provenance and schema mappings, refer to [docs/DATASET_PROVENANCE.md](file:///Users/laxyagaba/Richa_Sharma_25BAI10049/docs/DATASET_PROVENANCE.md).

---

## 5. Technology Stack

- **Core Programming Language**: Python 3.10–3.13
- **Data Engineering & Manipulation**: Pandas 2.2+, NumPy 1.26+
- **Interactive Web Architecture**: Streamlit 1.35+
- **Data Visualization & Charting**: Plotly 5.20+ (Plotly Express & Graph Objects), Matplotlib 3.8+, Seaborn 0.13+
- **Document Generation & Reporting**: ReportLab 4.0+ (Institutional PDF Memo generation)
- **Automated Testing & QA**: Pytest 8.0+, Streamlit `AppTest` API, Selenium WebDriver 4.42+ with Google Chrome Headless Engine
- **Academic Notebooks**: Jupyter Lab, `nbformat` 5.9+, `nbconvert` 7.16+, `ipykernel` 6.29+

---

## 6. Project Architecture

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           RAW DATASET PROVENANCE                                  │
│             data/startup_funding_raw.csv (3,044 Kaggle Source Deals)              │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
                                         ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                      DATA SANITIZATION (src/cleaning.py)                         │
│   • Unicode & Escape Stripping (\xc2\xa0)  • Safe Date Parsing (dd/mm/yyyy)       │
│   • Currency Cleaning & Regex USD Parse   • Column Normalization (Canonical)      │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
                                         ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                 FEATURE ENGINEERING ENGINE (src/feature_engineering.py)           │
│   • Task 1: INR Crores Conversion (₹83/USD), is_bengaluru, Drop funding_amount    │
│   • Task 2: round_number via apply(), sector_category via map(), headline apply() │
│   • Task 3: funding_tier via pd.cut(), funding_quartile via pd.qcut()            │
│   • Task 4: Date Extraction (yr, mo, qtr, dow), days_since_funding, funding_era   │
│   • Task 5: sector_avg & above_sector_avg via groupby().transform('mean')         │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
                     ┌───────────────────┴───────────────────┐
                     ▼                                       ▼
┌────────────────────────────────────────┐ ┌────────────────────────────────────────┐
│     ACADEMIC JUPYTER NOTEBOOK          │ │      VENTURETRACK WEB APPLICATION       │
│    notebooks/VentureTrack_EDA.ipynb    │ │        Streamlit Multi-Page Engine      │
│  • Standalone execution from scratch   │ │   app.py | src/ui_components.py        │
│  • Tasks 1–5 step-by-step code cells   │ │   • Modern Editorial Fintech Design     │
│  • Matplotlib/Seaborn visualizations   │ │   • Global Multi-Attribute Filter Rail  │
│  • 100% Dynamic Outputs & Interpret.   │ │   • 10 Dedicated Intelligence Pages     │
└────────────────────────────────────────┘ └───────────────────┬────────────────────┘
                                                               │
                                         ┌─────────────────────┴────────────────────┐
                                         ▼                                          ▼
                         ┌──────────────────────────────┐ ┌─────────────────────────────────┐
                         │      EXPORTS & REPORTING     │ │       AUTOMATED QA SUITE        │
                         │   • Filtered & Master CSV    │ │   • pytest tests/ (23 Tests)    │
                         │   • ReportLab PDF Briefing   │ │   • Headless Chrome Selenium QA │
                         └──────────────────────────────┘ └─────────────────────────────────┘
```

---

## 7. Folder Structure

```
Richa_Sharma_25BAI10049/
├── app.py                          # Streamlit application entrypoint & routing engine
├── requirements.txt                # Verified dependency specifications
├── README.md                       # Master comprehensive project documentation
├── .gitignore                      # Git exclusion rules
│
├── .streamlit/
│   └── config.toml                 # Light theme design tokens & server configuration
│
├── artifacts/
│   └── browser_qa/                 # Headless browser verification outputs
│       ├── 01_market_overview_1440px.png
│       ├── 02_startup_explorer_1440px.png
│       ├── ... (Screenshots of all 10 pages)
│       ├── responsive_1280px_market_overview.png
│       ├── responsive_1024px_market_overview.png
│       ├── qa_results.json         # Automated browser test status metrics
│       └── downloads/              # Real browser-downloaded CSV and PDF files
│
├── data/
│   ├── startup_funding_raw.csv     # Preserved original Kaggle source dataset (3,044 records)
│   ├── startup_funding_cleaned.csv # Canonical cleaned dataset output
│   └── README.md                   # Source provenance, column mapping & cleaning assumptions
│
├── docs/
│   ├── REQUIREMENT_MAPPING.md      # Detailed Task 1–5 requirement-to-code traceability matrix
│   ├── DATASET_PROVENANCE.md       # Comprehensive provenance, data hygiene & lineage disclosure
│   ├── DEPLOYMENT_GUIDE.md         # Zero-cost Streamlit Cloud, local, and Docker hosting guide
│   └── FINAL_QA_REPORT.md          # Consolidated test suite, browser QA & notebook validation
│
├── notebooks/
│   ├── VentureTrack_EDA.ipynb      # Standalone academic EDA notebook (Executed from fresh kernel)
│   ├── VentureTrack_EDA_executed.ipynb # Verified executed notebook copy
│   └── venturetrack_visualizations.png # Rendered 4-panel exploratory visualization
│
├── scripts/
│   └── browser_qa_runner.py        # Automated headless Selenium browser QA test runner
│
├── src/
│   ├── __init__.py                 # Python package descriptor
│   ├── config.py                   # Design tokens, paths, FX rates, schema maps, bin intervals
│   ├── data_loader.py              # Cached dataset loading, metadata and freshness tracker
│   ├── cleaning.py                 # Non-destructive data sanitization & parsing pipeline
│   ├── feature_engineering.py      # Tasks 1–5 mathematical feature engine (Single Source of Truth)
│   ├── analytics.py                # Purely dynamic statistical aggregations, KPIs & crosstabs
│   ├── visualizations.py           # Fintech Plotly chart generators (bars, lines, heatmaps, ladders)
│   ├── insights.py                 # Statistically grounded automated natural language synthesis
│   ├── filters.py                  # Global multi-attribute sidebar query controller
│   ├── exports.py                  # CSV dataset serialization & ReportLab PDF memo generator
│   └── ui_components.py            # CSS design system, metric cards, status bars & callouts
│
├── tests/
│   ├── __init__.py                 # Tests package descriptor
│   ├── test_cleaning.py            # Unit tests for text, date, and currency sanitization
│   ├── test_features.py            # Unit tests for Tasks 1-5 feature transformations
│   ├── test_analytics.py           # Anti-hardcoding validation across dual disjoint mini-datasets
│   └── test_views.py               # Streamlit AppTest tests validating all 10 views without error
│
└── views/
    ├── __init__.py                 # Views package descriptor
    ├── overview.py                 # View 1: Market Overview & Macro Trajectory
    ├── startup_explorer.py         # View 2: Entity Search, Headlines & Granular Table
    ├── sector_intelligence.py      # View 3: Vertical Aggregations & Outlier Ratios
    ├── city_intelligence.py        # View 4: Metropolitan Hubs & Bengaluru Comparison
    ├── funding_rounds.py           # View 5: Series Progression (A-F) & Stage Semantics
    ├── funding_distribution.py     # View 6: Task 3 Tier vs Quartile Divergence Audit
    ├── time_analysis.py            # View 7: Temporal Cycles, Day-of-Week & Funding Eras
    ├── feature_lab.py              # View 8: Interactive Workbench for 9 Pandas Primitives
    ├── data_laboratory.py          # View 9: Data Hygiene, Schema Audit & Nullity Report
    └── reports.py                  # View 10: Executive Briefings, PDF Export & Data Downloads
```

---

## 8. Installation & Quick Start Guide

### Prerequisites
- Python 3.10 through 3.13
- Git & pip

### Step-by-Step Installation
```bash
# 1. Clone repository and navigate to root directory
git clone <repository-url>
cd Richa_Sharma_25BAI10049

# 2. Create and activate a clean virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install verified production dependencies
pip install -r requirements.txt

# 4. Verify system compilation
python3 -m py_compile app.py src/*.py views/*.py tests/*.py

# 5. Launch the VentureTrack Platform
streamlit run app.py
```
*The platform will open automatically in your browser at `http://localhost:8501`.*

---

## 9. Running the Academic Jupyter Notebook

The exploratory data analysis notebook is completely self-contained with relative paths that execute cleanly both from the project root and from within the `notebooks/` directory:
```bash
# Launch Jupyter Lab
jupyter lab notebooks/VentureTrack_EDA.ipynb

# Or execute headlessly to verify from a fresh kernel
jupyter nbconvert --to notebook --execute notebooks/VentureTrack_EDA.ipynb --output VentureTrack_EDA_executed.ipynb
```

---

## 10. Application Features

1. **Editorial Design Tokens**: Crisp `#F7F8F6` canvas, `#FFFFFF` metric surfaces, `#17211F` slate typography, `#315FCE` cobalt primary accent, and `#16866A` evergreen growth indicator.
2. **Global Real-Time Query Rail**: Dynamic sidebar controls allowing multi-select by Metropolitan Hub, Market Sector, Funding Round Stage, Minimum Capital, and Announcement Date Range.
3. **Synchronized Workspace Bar**: Displays live record counts (`Active Scoped Cohort vs Full Master Repository`), active foreign exchange benchmark (₹83.0 / USD), and pipeline freshness timestamp.
4. **Zero-Defect Multi-Column Metric Cards**: Individual columns rendering financial metrics in tabular numerals (`font-variant-numeric: tabular-nums`) with zero HTML leakage.
5. **ReportLab PDF Executive Briefing Generator**: Programmatic compilation of an executive investment memorandum with dynamically aggregated statistics, key findings, and academic disclaimers.
6. **Multi-Format Dataset Exporters**: Instant one-click downloads for both scoped filtered data and master canonical repositories in UTF-8 CSV format.

---

## 11. Explanation of All Ten Analytical Pages

1. **Market Overview (`views/overview.py`)**:
   - Executive briefing with 8 core KPIs: Total Tracked Deals (3,044), Aggregate Capital (₹316,594.92 Cr), Mean Ticket (₹152.72 Cr), Outperforming Deals (10.32%), Geographic Hubs (81), Market Verticals (822), Investment Stages (56), and Bengaluru Share (27.96%).
   - Dual-axis deal volume vs capital trendline, sector bar chart, city rankings, and funding tier donut chart.
2. **Startup Explorer (`views/startup_explorer.py`)**:
   - Real-time startup text search with sorting across all numerical and temporal columns.
   - Live Task 2 headline ticker strip (`"Startup raised ₹X Cr in Round Y"`).
   - Interactive data table with custom column formatting and instant filtered CSV download.
3. **Sector Intelligence (`views/sector_intelligence.py`)**:
   - Sector capital concentration rankings, average ticket size benchmarking, and outlier deal proportion.
   - Macro sector category breakdown (`Consumer`, `Financial`, `Social`, `Other`).
4. **City Intelligence (`views/city_intelligence.py`)**:
   - Metropolitan startup hub rankings.
   - Dedicated Bengaluru vs Rest of India comparison module analyzing deal counts, capital capture, and average ticket size differences.
5. **Funding Rounds (`views/funding_rounds.py`)**:
   - Investment stage decomposition across Seed, Angel, Series A–F, Private Equity, and Debt.
   - Series progression ladder tracing deal volume vs average funding from Series A to Series F.
6. **Funding Distribution (`views/funding_distribution.py`)**:
   - Statistical distribution metrics: arithmetic mean, standard deviation, non-parametric median, IQR, and 1.5x IQR outliers.
   - Side-by-side comparison matrix of fixed monetary tiers (`pd.cut`) vs relative quartiles (`pd.qcut`).
   - Log-scale box plots and contingency heatmap proving why Small tier deals appear in Q4.
7. **Time & Era Analysis (`views/time_analysis.py`)**:
   - Annual, quarterly, and monthly deal velocity.
   - Year-over-quarter heatmap matrix.
   - Day-of-week announcement seasonality (Monday = 0).
   - Macro funding era comparison (`Early` vs `Pandemic` vs `Recovery`).
8. **Feature Engineering Lab (`views/feature_lab.py`)**:
   - Key academic workbench interactively explaining and demonstrating nine pandas primitives:
     `apply()`, `map()`, `cut()`, `qcut()`, `melt()`, `pivot()`, `crosstab()`, `groupby()`, and `transform()`.
   - Live execution cards showing runnable code, actual input data, and resulting output.
9. **Data Laboratory (`views/data_laboratory.py`)**:
   - Dataset dimensions, memory footprint, duplicate records audit, and invalid date reports.
   - Explicit confirmation of Task 1 `funding_amount` drop with live `df.columns` display.
   - Missing-value diagnostic table and theoretical justification for dropping vs retaining raw columns.
10. **Insights & Reports (`views/reports.py`)**:
    - Automated executive briefings across ecosystem, sectors, cities, and time dimensions.
    - Full enriched master CSV export (3,044 rows × 26 columns).
    - Filtered dataset CSV export.
    - Professional, styled **Executive PDF Memo** generation powered by ReportLab.

---

## 12. Explanation of the Five Assignment Tasks

Detailed requirement-to-code traceability is documented in [docs/REQUIREMENT_MAPPING.md](file:///Users/laxyagaba/Richa_Sharma_25BAI10049/docs/REQUIREMENT_MAPPING.md). Summary of implementations:

### Task 1 — Adding and Removing Columns
- `funding_crores`: Derived via `(funding_amount * 83.0 / 10,000,000).round(2)`.
- `is_bengaluru`: Boolean flag indicating whether the entity's headquarters is in Bengaluru/Bangalore.
- `investor_count`: Explicitly initialized with `np.nan` (zero synthetic fabricated data).
- Standardized `funding_amount` (USD): Purged from the final DataFrame. Verified via `df.columns` audit.

### Task 2 — apply() and map() Transformations
- `round_number`: Evaluated via `df['funding_round'].apply(lambda r: mapping.get(str(r).strip(), 0))` (Series A $\to 1$ through Series F $\to 6$; unlettered rounds $\to 0$).
- `sector_category`: Evaluated via `df['sector'].map(SECTOR_CATEGORY_MAP).fillna('Other / Unmapped')`.
- `headline`: Formatted via `df.apply(..., axis=1)` adhering to `"Startup raised ₹X Cr in Round Y"`.

### Task 3 — Binning with cut() and qcut()
- `funding_tier`: Discretized via `pd.cut()` into **Small** (<₹100 Cr), **Mid** (₹100–300 Cr), and **Large** (>₹300 Cr).
- `funding_quartile`: Discretized via `pd.qcut()` into 4 equal population quartiles (`Q1`, `Q2`, `Q3`, `Q4`) with duplicate handling.
- **Divergence Proof**: 120 deals classified in the Small Tier (<₹100 Cr) fall into Q4 (Top 25% relative quartile) because startup funding follows an extreme power-law (Pareto) distribution where 80%+ of deals are below ₹100 Cr.

### Task 4 — Date and Time Feature Extraction
- Derived features: `year`, `month`, `quarter`, `day_of_week` (Monday = 0), `month_name`.
- `days_since_funding`: Dynamically calculated using `(pd.Timestamp.now().normalize() - df['date']).dt.days`.
- `funding_era`: Binned into **Early** (pre-2020), **Pandemic** (2020–2021), and **Recovery** (2022+).

### Task 5 — Groupby, Transform and Summary Metrics
- `sector_avg`: Calculated via `df.groupby('sector')['funding_crores'].transform('mean').round(2)`.
- `above_sector_avg`: Boolean comparison `df['funding_crores'] > df['sector_avg']`.
- **Finding**: Only 10.32% of deals exceed their respective sector's arithmetic mean funding, confirming that macroeconomic averages are heavily driven by mega-round outliers.

---

## 13. Key Analytical Findings

1. **Extreme Capital Skewness**:
   Across 2,073 disclosed funding rounds, the arithmetic mean deal size is **₹152.72 Cr**, whereas the non-parametric median deal size is only **₹14.52 Cr** (a 10.5× disparity). Macroeconomic averages are dominated by a handful of mega-rounds.
2. **Geographic Hegemony of Bengaluru**:
   Bengaluru-based startups captured **27.96%** of all transaction volume (851 deals) and **₹98,412.30 Cr** in venture capital, surpassing Delhi-NCR (New Delhi, Gurgaon, Noida combined) and Mumbai.
3. **Sector Capital Concentration**:
   E-Commerce, Technology, and FinTech captured over 65% of total institutional capital. Late-stage logistics and consumer platforms commanded the highest average ticket sizes.
4. **Deal Velocity Cycle**:
   Transaction velocity peaked in **2016** with **993 announced deals**, before consolidating into fewer, later-stage, higher-conviction equity financings between 2017 and 2019.
5. **Day-of-Week Announcement Preference**:
   Announcements are heavily skewed toward mid-week business days (Tuesday through Thursday), with weekend announcements (Saturday/Sunday) accounting for less than 8% of deal disclosures.

---

## 14. Testing Instructions

### Automated Pytest Suite
Run the 23-test unit and regression suite covering sanitization, feature engineering, dual-dataset non-hardcoding proof, and Streamlit view rendering:
```bash
pytest tests/ -v
```

### Automated Headless Browser QA (Selenium + Chrome)
Run the real browser inspection script that visits all 10 pages, tests interactions, verifies responsive viewports, and downloads exports:
```bash
python3 scripts/browser_qa_runner.py
```
*Screenshots and results are automatically saved to `artifacts/browser_qa/`.*

### Python Syntax Compilation Check
```bash
python3 -m py_compile app.py src/*.py views/*.py tests/*.py
```

---

## 15. Limitations

1. **Voluntary Reporting Bias**:
   Unfunded startups, self-funded lifestyle businesses, and undisclosed venture rounds are absent or represented with null values (971 deals have undisclosed funding amounts).
2. **Historical Time Boundary**:
   The dataset concludes in January 2020. It captures the 2015–2019 initial venture boom, but does not capture the 2021 hyper-liquidity bubble or the 2022–2023 tech funding correction.
3. **Static Currency Conversion**:
   A uniform rate of ₹83.0/USD is applied across the entire 2015–2020 timeline for academic consistency, abstracting historical foreign exchange volatility (historical rates were ₹62–₹71/USD).

---

## 16. Future Scope

1. **Live API Integration**: Connect real-time venture tracking feeds from Tracxn, Crunchbase, or MCA (Ministry of Corporate Affairs) filings to monitor active 2024–2026 funding rounds.
2. **Predictive Stage Modeling**: Train classification models (Random Forest, XGBoost) using the engineered features (`round_number`, `sector_category`, `is_bengaluru`, `funding_tier`) to forecast a startup's probability of securing follow-on Series B/C funding.
3. **Cap-Table & Dilution Analytics**: Extend the data model to estimate founder dilution and investor ownership percentages across progressive rounds.
4. **Investor Portfolio Co-Investment Graph**: Implement NetworkX graph analysis on `investors_name` to map syndicate relationships, institutional lead investors, and venture firm co-investment clusters.

---

## 17. Academic Evaluation Metadata & Identity

- **Project Title**: VENTURETRACK — INDIAN STARTUP FUNDING INTELLIGENCE
- **Academic Course**: Advanced Data Engineering & Analytics
- **Mini Project**: Project 13 (Feature Engineering Primitives)
- **Student Author**: Richa Sharma
- **Registration Number**: `25BAI10049`
- **Department**: [Department of Computer Science & Engineering / Data Science — Confirmed Placeholder]
- **Institution**: [Academic Institution / University Name — Confirmed Placeholder]
- **Faculty Supervisor**: [Faculty Advisor / Course Mentor — Confirmed Placeholder]
- **Evaluation Status**: Final Submission Ready
