# VentureTrack — Dataset Provenance & Data Hygiene Disclosure
**Academic Mini Project 13** | **Author:** Richa Sharma (`25BAI10049`)  
**Curriculum Topic:** Advanced Data Engineering & Analytics — Data Lineage & Provenance  

---

## 1. Source Origin & Lineage Disclosure

- **Primary Data Source**: Kaggle Indian Startup Funding Dataset
- **Original Curator**: Sudalai Rajkumar
- **Public Repository**: [https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding)
- **Time Window**: January 2015 through January 2020
- **Total Raw Records**: 3,044 funding transactions
- **Raw File Stored Locally**: `data/startup_funding_raw.csv` (425,801 bytes)
- **Canonical Cleaned Output**: `data/startup_funding_cleaned.csv` (406,435 bytes)

> [!IMPORTANT]
> **Academic Lineage Disclosure**: The pre-cleaned output file from Mini Project 12 was not present in this workspace environment. In accordance with academic reproducibility standards, rather than fabricating a previous pipeline, a transparent, fully reproducible, non-destructive cleaning engine was reconstructed in `src/cleaning.py`. The original source dataset is strictly preserved in `data/startup_funding_raw.csv` and is never overwritten or mutated.

---

## 2. Schema Evolution & Attribute Mapping

The Kaggle source dataset features variations in column naming across releases. VentureTrack standardizes these into a uniform internal canonical schema:

| Raw Kaggle Field Header | Kaggle Release Variant | VentureTrack Canonical Internal Attribute | Target Type | Description & Semantic Role |
| :--- | :--- | :--- | :--- | :--- |
| `Startup Name` | `StartupName` | `startup_name` | String / Object | Legal or operating brand name of the startup entity |
| `City  Location` | `CityLocation` | `city` | String / Object | Primary operating metropolitan headquarters |
| `Amount in USD` | `AmountInUSD` | `funding_amount` | Float64 (working) | Deal value in USD before Task 1 INR Crores conversion |
| `InvestmentnType` | `InvestmentType` | `funding_round` | String / Object | Investment instrument or stage (Seed, Angel, Series A-F, PE, Debt) |
| `Industry Vertical` | `IndustryVertical` | `sector` | String / Object | Primary market vertical or industry domain |
| `Date dd/mm/yyyy` | `Date` | `date` | Datetime64[ns] | Funding transaction announcement timestamp |
| `SubVertical` | `SubVertical` | `sub_sector` | String / Object | Granular sub-category or niche focus |
| `Investors Name` | `InvestorsName` | `investors_name` | String / Object | Participating angel investors or institutional venture funds |
| `Remarks` | `Remarks` | `remarks` | String / Object | Contextual annotations or secondary notes |

---

## 3. Data Sanitization & Cleaning Rules

The data cleaning pipeline (`src/cleaning.py`) applies the following deterministic operations:

### 1. Unicode & Artifact Removal (`remove_unicode_escapes`)
- Strips non-breaking whitespace escapes (`\xc2\xa0`, `\\xc2\\xa0`, `\xa0`) and Windows carriage returns (`\r\n`).
- Strips excessive whitespace and normalizes empty text strings to `np.nan`.

### 2. Monetary Amount Parsing (`parse_numeric_amount`)
- Strips currency symbols (`$`, `₹`), formatting commas (`,`), plus signs (`+`), and trailing non-breaking spaces.
- Identifies unverified string sentinels (`"undisclosed"`, `"unknown"`, `"N/A"`, `"nan"`, `"none"`) and maps them strictly to `np.nan`.
- Parses valid amounts to standard `float64` USD values.
- **Strict Anti-Imputation Rule**: Undisclosed funding rounds are never populated with fabricated or synthetic averages, preserving true empirical skewness.

### 3. Date Sanitization (`parse_date_safely`)
- Resolves known typographical errors in the Kaggle dataset:
  - `"05/072018"` $\to$ `"05/07/2018"`
  - `"01/07/015"` $\to$ `"01/07/2015"`
  - `"10/7/2015"` $\to$ `"10/07/2015"`
- Normalizes irregular delimiters (`//`, `.`, `/`).
- Parses dates using the standard Indian calendar format (`%d/%m/%Y`). Irrecoverable dates resolve to `pd.NaT` without dropping the startup row.

### 4. Categorical Normalization
- Removes newline formatting artifacts (e.g. `"Seed\\nFunding"` $\to$ `"Seed Funding"`).
- Normalizes city spellings (`"Bangalore"` $\to$ `"Bengaluru"` for grouping while preserving historical labels).

---

## 4. Currency Conversion Methodology

In accordance with assignment requirements:
- **Exchange Rate Assumption**: Fixed rate of **₹83.00 INR per USD**.
- **Conversion Equation**:
  $$\text{funding\_crores} = \text{round}\left( \frac{\text{funding\_amount} \times 83.0}{10,000,000}, 2 \right)$$
- **Working Column Removal**: Following computation of `funding_crores`, the intermediate `funding_amount` (USD) column is dropped from the active DataFrame in Task 1.

---

## 5. Dataset Limitations

1. **Voluntary Reporting Bias**:
   - Only publicly announced or media-covered venture transactions are captured. Early-stage stealth rounds and undisclosed venture deals are underrepresented or contain missing financial amounts (971 of 3,044 deals have undisclosed funding).
2. **Temporal Coverage**:
   - The dataset concludes in January 2020. Consequently, it reflects the 2015–2019 hyper-growth and initial consolidation cycle, but does not capture post-2021 liquidity expansions or the 2022–2023 tech funding correction.
3. **Static Currency Conversion**:
   - A uniform exchange rate of ₹83/USD is applied across the entire timeline (2015–2020) for academic consistency. Real historical exchange rates varied between ₹62/USD (2015) and ₹71/USD (2019).
4. **Self-Reported Sectors**:
   - Industry verticals are self-reported by startups or news outlets, leading to high cardinal fragmentation (over 800 granular sector strings before dictionary aggregation).

