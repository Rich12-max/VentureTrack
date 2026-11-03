"""
VentureTrack View 8: Feature Engineering Lab
Interactive academic workbench demonstrating pandas transformation primitives:
apply, map, cut, qcut, melt, pivot, crosstab, groupby, and transform.
Data science workbench layout with interactive input/output comparator.
"""
from typing import Dict, Any
import streamlit as st
import pandas as pd
import numpy as np

from src.ui_components import (
    render_page_header,
    render_section_header,
    render_academic_callout,
)
from src.config import (
    SECTOR_CATEGORY_MAP,
    SERIES_ROUND_MAP,
    FUNDING_TIER_BINS,
    FUNDING_TIER_LABELS,
    THEME_COLORS,
)


def render(df: pd.DataFrame):
    """Renders the Feature Engineering Lab interactive demonstration workbench."""
    render_page_header(
        title="Feature Engineering Lab",
        subtitle="Interactive Academic Workbench for Core Pandas Transformation Primitives",
        badge="Academic Benchmark"
    )
    
    st.markdown(
        f'<div style="background: #FFFFFF; border: 1px solid {THEME_COLORS["borders"]}; border-left: 3px solid {THEME_COLORS["primary_accent"]}; border-radius: 6px; padding: 11px 16px; margin-bottom: 16px; font-size: 0.84rem; color: {THEME_COLORS["primary_text"]}; line-height: 1.45;">Investigate the theoretical concept, vectorized Python syntax, and live row-level execution of the nine core pandas transformation primitives required across Tasks 1 through 5.</div>',
        unsafe_allow_html=True
    )

    operations = [
        "1. apply() — Custom Function Vectorization",
        "2. map() — Dictionary Substitution & Alignment",
        "3. cut() — Uniform & Arbitrary Fixed Binning",
        "4. qcut() — Quantile & Frequency Binning",
        "5. melt() — Wide-to-Long Reshaping",
        "6. pivot() — Long-to-Wide Reshaping",
        "7. crosstab() — Multi-Way Frequency Aggregation",
        "8. groupby() — Split-Apply-Combine Aggregation",
        "9. transform() — Broadcasted Group Calculations",
    ]
    
    selected_op = st.selectbox("Select Transformation Primitive to Investigate", options=operations, index=0)

    # 1. apply()
    if selected_op.startswith("1."):
        st.subheader("Primitive 1: `pd.Series.apply()` and `pd.DataFrame.apply()`")
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            st.markdown(
                """
                **Concept**:  
                `apply()` invokes an arbitrary Python callable (such as a lambda or custom function) along an axis of a DataFrame or across values of a Series.
                
                **Utility in Pipelines**:
                - Enables complex conditional logic that cannot be expressed via standard vectorized operators.
                - Essential for natural language headline generation (`DataFrame.apply(axis=1)`) combining multiple columns.
                - Facilitates categorical regex extraction and normalization.
                """
            )
        with col_c2:
            st.markdown(
                """
                **Production Syntax (Task 2)**:
                ```python
                # Series apply with lambda
                df['round_number'] = df['funding_round'].apply(
                    lambda r: series_map.get(str(r).strip(), 0)
                )

                # Row-wise apply across multiple columns
                df['headline'] = df.apply(
                    lambda row: f"{row['startup_name']} raised ₹{row['funding_crores']:.2f} Cr in Round {row['funding_round']}",
                    axis=1
                )
                ```
                """
            )
            
        st.markdown("##### Live Execution: Input vs Output")
        sample_input = df[["startup_name", "funding_round", "funding_crores"]].dropna().head(6)
        
        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown("**Input DataFrame (df)**")
            st.dataframe(sample_input, use_container_width=True)
        with col_out:
            st.markdown("**Transformed Features (round_number & headline)**")
            res_df = sample_input.copy()
            res_df["round_number"] = res_df["funding_round"].apply(lambda r: SERIES_ROUND_MAP.get(str(r).strip(), 0))
            res_df["headline"] = res_df.apply(
                lambda row: f"{row['startup_name']} raised ₹{row['funding_crores']:.2f} Cr in Round {row['funding_round']}", axis=1
            )
            st.dataframe(res_df[["round_number", "headline"]], use_container_width=True)

    # 2. map()
    elif selected_op.startswith("2."):
        st.subheader("Primitive 2: `pd.Series.map()`")
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            st.markdown(
                """
                **Concept**:  
                `map()` substitutes each value in a Series with another value using a mapping dictionary, Series, or function. Values not found in the dictionary result in `NaN` (unless chained with `.fillna()`).
                
                **Utility in Pipelines**:
                - Highly optimized C-level hash table lookup for categorical re-encoding.
                - Strictly preserves one-to-one or many-to-one category mapping.
                - Faster than `apply()` for dictionary lookups.
                """
            )
        with col_c2:
            st.markdown(
                """
                **Production Syntax (Task 2)**:
                ```python
                sector_dict = {
                    "Mobility": "Consumer",
                    "FoodTech": "Consumer",
                    "Grocery": "Consumer",
                    "eCommerce": "Consumer",
                    "FinTech": "Financial",
                    "EdTech": "Social",
                    "Beauty": "Consumer"
                }
                
                df['sector_category'] = (
                    df['sector'].map(sector_dict).fillna("Other / Unmapped")
                )
                ```
                """
            )
            
        st.markdown("##### Live Execution: Input vs Output")
        test_sectors = pd.DataFrame({"sector": ["Mobility", "FinTech", "EdTech", "eCommerce", "Artificial Intelligence", "Healthcare"]})
        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown("**Input Sectors**")
            st.dataframe(test_sectors, use_container_width=True)
        with col_out:
            st.markdown("**Mapped Categories via map()**")
            test_mapped = test_sectors.copy()
            test_mapped["sector_category"] = test_mapped["sector"].map(SECTOR_CATEGORY_MAP).fillna("Other / Unmapped")
            st.dataframe(test_mapped, use_container_width=True)

    # 3. cut()
    elif selected_op.startswith("3."):
        st.subheader("Primitive 3: `pd.cut()` — Fixed Monetary Tiers")
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            st.markdown(
                """
                **Concept**:  
                `cut()` bins continuous numerical data into discrete intervals based on explicit user-defined boundary edges.
                
                **Utility in Pipelines**:
                - Translates continuous figures into domain-specific institutional tiers (e.g., Small, Mid, Large).
                - Enforces business policy thresholds regardless of underlying sample distribution.
                """
            )
        with col_c2:
            st.markdown(
                """
                **Production Syntax (Task 3)**:
                ```python
                # Fixed tier boundaries specified in assignment:
                # Small: below ₹100 Cr
                # Mid: ₹100 Cr through ₹300 Cr
                # Large: above ₹300 Cr
                bins = [-np.inf, 99.999999, 300.0, np.inf]
                labels = ["Small", "Mid", "Large"]
                
                df['funding_tier'] = pd.cut(
                    df['funding_crores'], 
                    bins=bins, 
                    labels=labels, 
                    right=True
                )
                ```
                """
            )
            
        st.markdown("##### Live Execution: Input vs Output")
        sample_amts = pd.DataFrame({
            "startup_name": ["Seed Co", "Growth Co A", "Growth Co B", "Mega Unicorn"],
            "funding_crores": [15.50, 99.99, 250.00, 1660.00]
        })
        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown("**Input Numerical Values**")
            st.dataframe(sample_amts, use_container_width=True)
        with col_out:
            st.markdown("**Discretized Tiers via pd.cut()**")
            sample_cut = sample_amts.copy()
            sample_cut["funding_tier"] = pd.cut(sample_cut["funding_crores"], bins=FUNDING_TIER_BINS, labels=FUNDING_TIER_LABELS, right=True)
            st.dataframe(sample_cut[["funding_crores", "funding_tier"]], use_container_width=True)

    # 4. qcut()
    elif selected_op.startswith("4."):
        st.subheader("Primitive 4: `pd.qcut()` — Relative Quantile Cohorts")
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            st.markdown(
                """
                **Concept**:  
                `qcut()` partitions data into equal-frequency bins based on empirical sample percentiles (e.g. quartiles Q1, Q2, Q3, Q4).
                
                **Utility in Pipelines**:
                - Mitigates extreme skewness by guaranteeing approximately equal record volume per bin.
                - Compares relative standing within the active population rather than absolute monetary amounts.
                """
            )
        with col_c2:
            st.markdown(
                """
                **Production Syntax (Task 3)**:
                ```python
                # Quartile binning with duplicate handling
                valid_mask = df['funding_crores'].notna()
                df.loc[valid_mask, 'funding_quartile'] = pd.qcut(
                    df.loc[valid_mask, 'funding_crores'],
                    q=4,
                    labels=['Q1', 'Q2', 'Q3', 'Q4'],
                    duplicates='drop'
                )
                ```
                """
            )
            
        st.markdown("##### Live Execution: Input vs Output")
        valid_sample = df.dropna(subset=["funding_crores"])[["startup_name", "funding_crores"]].sample(6, random_state=42)
        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown("**Sample Input**")
            st.dataframe(valid_sample, use_container_width=True)
        with col_out:
            st.markdown("**Quantile Assignment via pd.qcut()**")
            res_q = valid_sample.copy()
            res_q["funding_quartile"] = pd.qcut(res_q["funding_crores"], q=4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop")
            st.dataframe(res_q, use_container_width=True)

    # 5. melt()
    elif selected_op.startswith("5."):
        st.subheader("Primitive 5: `pd.melt()` — Wide-to-Long Reshaping")
        st.markdown(
            """
            **Concept**:  
            Unpivots a DataFrame from wide format to long format, gathering identifier columns and unpivoting measurement columns into variable-value pairs.
            
            **Utility in Pipelines**:
            - Essential for relational tidy data formatting where multiple metric columns are gathered into a single categorical axis for visualization.
            """
        )
        sample_wide = pd.DataFrame({
            "startup_name": ["Paytm", "Swiggy", "Zomato"],
            "seed_funding": [5.0, 10.0, 8.0],
            "series_a": [50.0, 80.0, 60.0],
            "series_b": [200.0, 300.0, 250.0]
        })
        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown("**Wide Format Input**")
            st.dataframe(sample_wide, use_container_width=True)
        with col_out:
            st.markdown("**Long Format Output via pd.melt()**")
            melted = pd.melt(sample_wide, id_vars=["startup_name"], var_name="round_stage", value_name="capital_crores")
            st.dataframe(melted, use_container_width=True)

    # 6. pivot()
    elif selected_op.startswith("6."):
        st.subheader("Primitive 6: `pd.pivot()` / `pd.pivot_table()` — Long-to-Wide Reshaping")
        st.markdown(
            """
            **Concept**:  
            Reshapes data by setting unique index, column, and values, pivoting row labels into column headers with optional mathematical aggregation.
            
            **Utility in Pipelines**:
            - Constructs two-dimensional cross-sectional tables (e.g. Year vs Sector capital matrices) for heatmaps and reporting.
            """
        )
        valid = df.dropna(subset=["year", "funding_era", "funding_crores"]).copy()
        pivot_sample = valid.head(50)
        pivoted = pd.pivot_table(
            pivot_sample,
            index="year",
            columns="funding_tier",
            values="funding_crores",
            aggfunc="count",
            fill_value=0,
            observed=False
        )
        st.markdown("**Pivoted Cross-Section Table (Year vs Tier Deal Count)**")
        st.dataframe(pivoted, use_container_width=True)

    # 7. crosstab()
    elif selected_op.startswith("7."):
        st.subheader("Primitive 7: `pd.crosstab()` — Multi-Way Contingency Analysis")
        st.markdown(
            """
            **Concept**:  
            Computes a simple frequency cross-tabulation of two or more factors. Defaults to count frequencies unless a values array and aggfunc are passed.
            
            **Utility in Pipelines**:
            - Audits interaction between categorical features (e.g. Funding Tier vs Relative Quartile in Task 3).
            """
        )
        valid = df.dropna(subset=["funding_tier", "funding_quartile"]).copy()
        ct = pd.crosstab(valid["funding_tier"], valid["funding_quartile"], margins=True)
        st.dataframe(ct, use_container_width=True)

    # 8. groupby()
    elif selected_op.startswith("8."):
        st.subheader("Primitive 8: `pd.DataFrame.groupby()` — Split-Apply-Combine")
        st.markdown(
            """
            **Concept**:  
            Splits data into groups based on key columns, applies an aggregation function, and combines results into a summary DataFrame with reduced dimensions.
            
            **Utility in Pipelines**:
            - Generates macro summary metrics (e.g. total and average capital by sector or city in Task 5).
            """
        )
        grp = df.groupby("city").agg(
            deals=("startup_name", "count"),
            avg_crores=("funding_crores", "mean")
        ).reset_index().sort_values(by="deals", ascending=False).head(8)
        grp["avg_crores"] = grp["avg_crores"].round(2)
        st.dataframe(grp, use_container_width=True)

    # 9. transform()
    elif selected_op.startswith("9."):
        st.subheader("Primitive 9: `pd.core.groupby.GroupBy.transform()` — Broadcast Group Aggregations")
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            st.markdown(
                """
                **Concept**:  
                Executes a group-wise function but returns an object with the **exact same index and size** as the original DataFrame by broadcasting group values.
                
                **Utility in Pipelines (Task 5 Requirement)**:
                - Computes within-group deviations (e.g., `df['funding_crores'] > df.groupby('sector')['funding_crores'].transform('mean')`).
                - Generates group-relative features without performing an explicit merge or join.
                """
            )
        with col_c2:
            st.markdown(
                """
                **Production Syntax (Task 5)**:
                ```python
                # Broadcast sector mean back to row index
                df['sector_avg'] = (
                    df.groupby('sector')['funding_crores']
                    .transform('mean')
                    .round(2)
                )

                # Row-wise comparison against group benchmark
                df['above_sector_avg'] = df['funding_crores'] > df['sector_avg']
                ```
                """
            )
            
        st.markdown("##### Live Execution: Input vs Output")
        sample_tf = df.dropna(subset=["funding_crores"])[["startup_name", "sector", "funding_crores"]].head(8)
        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown("**Original Entity Rows**")
            st.dataframe(sample_tf, use_container_width=True)
        with col_out:
            st.markdown("**Broadcasted `sector_avg` & `above_sector_avg`**")
            res_tf = sample_tf.copy()
            res_tf["sector_avg"] = res_tf.groupby("sector")["funding_crores"].transform("mean").round(2)
            res_tf["above_sector_avg"] = res_tf["funding_crores"] > res_tf["sector_avg"]
            st.dataframe(res_tf[["sector_avg", "above_sector_avg"]], use_container_width=True)

    # Academic Callout
    render_academic_callout(
        "Notice the structural distinction between apply() and map(): map() is strictly optimized for element-wise dictionary "
        "lookups across a single Series; apply() is a general-purpose functional applicator capable of row-wise axis iteration. "
        "Similarly, contrast groupby().agg() (which collapses row count) with groupby().transform() (which preserves original record dimensions).",
        title="ACADEMIC SUMMARY: TRANSFORMATION PARADIGMS"
    )
