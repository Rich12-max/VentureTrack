# VentureTrack Data Architecture & Source Provenance

## Source Dataset
- **Origin**: Kaggle Indian Startup Funding Dataset
- **Curated By**: Sudalai Rajkumar ([Kaggle Dataset Page](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding))
- **File**: `startup_funding_raw.csv` (3,044 raw records spanning 2015 to 2020)
- **Status**: Raw source data preserved without modification. Never overwritten or destructively mutated.

## Schema Evolution & Column Mapping

The raw Kaggle dataset exhibits inconsistent column naming conventions across different releases. VentureTrack standardizes these variations into a canonical internal schema.

| Raw Kaggle Field Name | Kaggle Variant | VentureTrack Canonical Internal Schema | Data Type | Description |
|---|---|---|---|---|
| `Startup Name` | `StartupName` | `startup_name` | String / Object | Legal or operating brand name of the startup |
| `City  Location` | `CityLocation` | `city` | String / Object | Primary headquarters city in India or globally |
| `Amount in USD` | `AmountInUSD` | `funding_amount` | Float64 (working) | Deal value in USD before INR conversion (dropped in Task 1) |
| `InvestmentnType` | `InvestmentType`| `funding_round` | String / Object | Funding instrument or stage (Seed, Series A-F, PE, Debt) |
| `Industry Vertical`| `IndustryVertical`| `sector` | String / Object | Primary market vertical or industry domain |
| `Date dd/mm/yyyy` | `Date` | `date` | Datetime64[ns] | Funding transaction announcement date |
| `SubVertical` | `SubVertical` | `sub_sector` | String / Object | Granular sub-category or niche focus |
| `Investors Name` | `InvestorsName` | `investors_name` | String / Object | Participating angel investors or institutional venture funds |
| `Remarks` | `Remarks` | `remarks` | String / Object | Contextual annotations or secondary notes |

## Cleaning Assumptions & Business Rules
1. **Currency Cleaning**:
   - Strips non-breaking whitespace escapes (`\\xc2\\xa0`, `\xa0`), formatting commas, and symbols (`+`).
   - Non-numeric strings (e.g., `'undisclosed'`, `'unknown'`, `'N/A'`) are set to `np.nan`.
   - Values are parsed to `float64` in USD.
2. **Date Sanitization**:
   - Fixes irregular typos and non-breaking space artifacts (e.g. `'05/072018'`, `'01/07/015'`, `'\\xc2\\xa010/7/2015'`).
   - Normalizes date delimiters (`//`, `.`, `/`).
   - Parses dates with `%d/%m/%Y`. Invalid/unparseable dates remain `NaT` without silent distortion.
3. **City Normalization**:
   - Resolves multi-city strings (e.g., `'Bangalore / USA'`) by identifying the primary operating hub.
   - Preserves raw names for granular research while mapping common variants (`'Bangalore'` and `'Bengaluru'`) to support the `is_bengaluru` feature.
4. **Sector Normalization**:
   - Removes trailing spaces and escape sequences.
   - Preserves original sector names while applying assignment mapping dictionaries transparently.
5. **Funding Round Normalization**:
   - Eliminates formatting newlines (`Seed\\nFunding`) and irregular slashes.

