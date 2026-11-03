# VentureTrack — Requirement-to-Implementation Mapping
**Academic Mini Project 13** | **Author:** Richa Sharma (`25BAI10049`)  
**Curriculum Topic:** Advanced Data Engineering & Analytics — Feature Engineering Primitives  

This document provides a verified, auditable traceability matrix mapping every academic assignment requirement (Tasks 1 through 5) directly to its implementing Python source code, function signatures, generated schema attributes, visual application views, and corresponding Jupyter notebook sections.

---

## Traceability Matrix

| Assignment Task | Implementing Source File | Core Function Name | Output DataFrame Attributes | Web Application Surface | Jupyter Notebook Section |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Task 1: Column Addition & Removal** | `src/feature_engineering.py` | `task_1_add_and_remove_columns()` | `funding_crores`<br>`is_bengaluru`<br>`investor_count`<br>*(Dropped: `funding_amount`)* | • **Market Overview** (`views/overview.py`)<br>• **City Intelligence** (`views/city_intelligence.py`)<br>• **Data Laboratory** (`views/data_laboratory.py`) | **Section 6** (Cells 9–10) |
| **Task 2: apply() & map() Operations** | `src/feature_engineering.py` | `task_2_apply_and_map_transformations()` | `round_number`<br>`sector_category`<br>`headline` | • **Startup Explorer** (`views/startup_explorer.py`)<br>• **Sector Intelligence** (`views/sector_intelligence.py`)<br>• **Funding Rounds** (`views/funding_rounds.py`)<br>• **Feature Lab** (`views/feature_lab.py`) | **Section 7** (Cells 11–12) |
| **Task 3: Binning with cut() & qcut()** | `src/feature_engineering.py` | `task_3_binning_cut_and_qcut()`<br>`compare_tier_vs_quartile()` | `funding_tier`<br>`funding_quartile` | • **Funding Distribution** (`views/funding_distribution.py`)<br>• **Market Overview** (`views/overview.py`)<br>• **Feature Lab** (`views/feature_lab.py`) | **Section 8** (Cells 13–14) |
| **Task 4: Temporal Feature Engineering** | `src/feature_engineering.py` | `task_4_date_and_time_extraction()` | `year`, `month`, `quarter`<br>`day_of_week`, `month_name`<br>`days_since_funding`<br>`funding_era` | • **Time & Era Analysis** (`views/time_analysis.py`)<br>• **Reports & Insights** (`views/reports.py`) | **Section 9** (Cells 15–16) |
| **Task 5: Groupby, Transform & Synthesis** | `src/feature_engineering.py`<br>`src/insights.py` | `task_5_summary_metrics_and_transform()`<br>`generate_task5_interpretation()` | `sector_avg`<br>`above_sector_avg`<br>*(Dynamic Markdown synthesis)* | • **Market Overview** (`views/overview.py`)<br>• **Sector Intelligence** (`views/sector_intelligence.py`)<br>• **Reports & Insights** (`views/reports.py`)<br>• **Feature Lab** (`views/feature_lab.py`) | **Section 10 & 13** (Cells 17–18, 23) |

---

## Detailed Task Verification & Scientific Explanations

### Task 1 — Adding and Removing Columns
- **Source File**: `src/feature_engineering.py` (Lines 23–60)
- **Mathematical Specification**:
  $$\text{funding\_crores} = \left( \frac{\text{funding\_amount} \times 83.0}{10^7} \right) \quad [\text{rounded to 2 decimal places}]$$
- **Feature Definitions**:
  1. `funding_crores` (Float64): Primary financial reporting unit.
  2. `is_bengaluru` (Boolean): Evaluates to `True` if city string matches `'Bengaluru'` or `'Bangalore'` variants. Missing/unrecorded locations resolve strictly to `False`.
  3. `investor_count` (Float64): Initialized explicitly with `np.nan`. Enforces scientific integrity by preventing synthetic counts when investor arrays are uncurated.
  4. `funding_amount` (DROPPED): Standardized USD working column is purged from the DataFrame.
- **Academic Justification for Dropping vs Retaining**:
  - *When to Drop*: When a feature is an exact, deterministic, one-to-one linear scalar transformation, retaining both introduces exact multicollinearity ($R^2 = 1.0$) and doubles memory overhead. In Indian financial analytics, INR Crores is the statutory standard. Dropping the USD column creates a single source of truth.
  - *When to Retain*: When transformations are non-invertible/lossy (e.g., binning continuous variables into tiers) or parameter-variant (e.g., floating foreign exchange rates requiring historical auditability).
- **Application Audit**:
  - `views/data_laboratory.py` features a live automated test block verifying `"funding_amount" not in df.columns` and displays the full `df.columns` array.

---

### Task 2 — apply() and map() Transformations
- **Source File**: `src/feature_engineering.py` (Lines 62–95)
- **Implementation Rules**:
  1. `round_number` via `Series.apply()` & Lambda:
     - Strict mapping: Series A $\to 1$, Series B $\to 2$, Series C $\to 3$, Series D $\to 4$, Series E $\to 5$, Series F $\to 6$.
     - Real unlettered venture rounds (Seed, Debt, Private Equity) are mapped to `0` without fabricating series letters.
  2. `sector_category` via `Series.map()`:
     - Evaluated against assignment mapping dictionary (`Mobility` $\to$ Consumer, `FinTech` $\to$ Financial, `EdTech` $\to$ Social, etc.).
     - Unmapped entries resolve to `'Other / Unmapped'` via `.fillna()`, guaranteeing zero data loss.
  3. `headline` via `DataFrame.apply(axis=1)`:
     - Formats natural language press synthesis: `"Startup raised ₹X Cr in Round Y"`.
     - Gracefully handles undisclosed funding rounds (`"Startup raised an undisclosed amount in Round Y"`).
- **Core Concept: `apply()` vs `map()`**:
  - `map()` is a specialized, highly optimized C-level hash substitution method operating strictly element-wise on a pandas `Series`.
  - `apply()` is a general-purpose functional iteration primitive capable of traversing values or computing across axes (`axis=1` for horizontal multi-column evaluation).

---

### Task 3 — Binning with cut() and qcut()
- **Source File**: `src/feature_engineering.py` (Lines 97–144)
- **Interval Specifications**:
  1. `funding_tier` via `pd.cut()`:
     - **Small**: $(-\infty, 99.999999\text{ Cr}]$
     - **Mid**: $(99.999999\text{ Cr}, 300.0\text{ Cr}]$
     - **Large**: $(300.0\text{ Cr}, \infty)$
  2. `funding_quartile` via `pd.qcut()`:
     - Discretizes active deals into 4 equal population cohorts: `Q1` (0–25%), `Q2` (25–50%), `Q3` (50–75%), `Q4` (75–100%).
     - Configured with `duplicates="drop"` and fallback rank indexing to ensure zero crashes on tied values.
- **Empirical Divergence Audit**:
  - In `views/funding_distribution.py`, an automated cross-tabulation demonstrates that 120 deals (~5.8% of disclosed transactions) classified as **Small Tier (<₹100 Cr)** simultaneously fall into **Q4 (Top 25% relative quartile)**.
  - **Academic Explanation**: Startup capital follows an extreme Pareto (power-law) distribution. Over 80% of transactions fall below ₹100 Cr; therefore, the 75th percentile cutoff occurs at approximately ₹66 Cr. Deals between ₹66 Cr and ₹100 Cr are objectively "Small" by venture capital institutional standards, yet rank within the "Top 25%" relative to the sheer volume of seed and angel micro-deals.

---

### Task 4 — Date and Time Feature Extraction
- **Source File**: `src/feature_engineering.py` (Lines 146–183)
- **Extracted Attributes**:
  1. `year`, `month`, `quarter`, `day_of_week` (Monday = 0), `month_name`.
  2. `days_since_funding`: Dynamic integer feature computed on-the-fly relative to current system runtime (`pd.Timestamp.now().normalize() - df['date']`).
  3. `funding_era` via `pd.cut()`:
     - **Early**: Pre-2020 ($\le 2019$)
     - **Pandemic**: 2020–2021
     - **Recovery**: 2022 onwards
- **Methodological Disclaimer**: The historical deal peak in 2015–2016 reflects early-stage media disclosure cadence and consumer internet proliferation, not macroeconomic contraction.

---

### Task 5 — Groupby, Transform and Academic Synthesis
- **Source File**: `src/feature_engineering.py` (Lines 185–205) & `src/insights.py`
- **Peer-Group Normalization**:
  $$\text{sector\_avg} = \text{df.groupby}('sector')['funding\_crores'].\text{transform}('mean').\text{round}(2)$$
  $$\text{above\_sector\_avg} = \text{df}['funding\_crores'] > \text{df}['sector\_avg']$$
- **Engineering Advantage of `transform()` over `.agg()` / `.merge()`**:
  - `.agg()` reduces grouping rows into an aggregate table with a collapsed index.
  - `.transform()` broadcasts computed aggregate scalars directly back across the original row index without reshaping, preserving the shape $(N, D)$ and eliminating join overhead.
- **Empirical Finding**: Only **10.32%** of all deals exceed their industry vertical average, demonstrating that startup funding distributions are heavily right-skewed by mega-rounds.

