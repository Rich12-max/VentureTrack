"""
VentureTrack Analytics Core Engine
Performs purely dynamic, data-driven mathematical, statistical, and aggregative calculations.
Strictly adheres to the No Hardcoding Policy.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np


def calculate_market_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes high-level market metrics dynamically from the active dataset."""
    total_records = len(df)
    if total_records == 0:
        return {
            "total_records": 0,
            "unique_startups": 0,
            "total_funding_crores": 0.0,
            "avg_funding_crores": 0.0,
            "median_funding_crores": 0.0,
            "unique_cities": 0,
            "unique_sectors": 0,
            "unique_rounds": 0,
            "above_sector_avg_pct": 0.0,
            "bengaluru_pct": 0.0,
            "top_funded_startup": "N/A",
            "top_funded_amount": 0.0,
        }
        
    valid_funding = df["funding_crores"].dropna()
    total_funding = valid_funding.sum()
    avg_funding = valid_funding.mean() if len(valid_funding) > 0 else 0.0
    median_funding = valid_funding.median() if len(valid_funding) > 0 else 0.0
    
    unique_startups = df["startup_name"].nunique()
    unique_cities = df["city"].nunique()
    unique_sectors = df["sector"].nunique()
    unique_rounds = df["funding_round"].nunique()
    
    above_sector_cnt = df["above_sector_avg"].sum() if "above_sector_avg" in df.columns else 0
    above_sector_pct = (above_sector_cnt / total_records * 100) if total_records > 0 else 0.0
    
    bengaluru_cnt = df["is_bengaluru"].sum() if "is_bengaluru" in df.columns else 0
    bengaluru_pct = (bengaluru_cnt / total_records * 100) if total_records > 0 else 0.0
    
    # Top funded startup
    top_record = df.sort_values(by="funding_crores", ascending=False).iloc[0] if len(valid_funding) > 0 else None
    top_startup = str(top_record["startup_name"]) if top_record is not None else "N/A"
    top_amount = float(top_record["funding_crores"]) if top_record is not None else 0.0
    
    return {
        "total_records": int(total_records),
        "unique_startups": int(unique_startups),
        "total_funding_crores": float(round(total_funding, 2)),
        "avg_funding_crores": float(round(avg_funding, 2)),
        "median_funding_crores": float(round(median_funding, 2)),
        "unique_cities": int(unique_cities),
        "unique_sectors": int(unique_sectors),
        "unique_rounds": int(unique_rounds),
        "above_sector_avg_pct": float(round(above_sector_pct, 2)),
        "above_sector_avg_count": int(above_sector_cnt),
        "bengaluru_count": int(bengaluru_cnt),
        "bengaluru_pct": float(round(bengaluru_pct, 2)),
        "top_funded_startup": top_startup,
        "top_funded_amount": round(top_amount, 2),
    }


def get_sector_summary(df: pd.DataFrame, min_deals: int = 1) -> pd.DataFrame:
    """Computes sector intelligence metrics, sorted descending by average funding."""
    if len(df) == 0:
        return pd.DataFrame()
        
    grouped = df.groupby("sector").agg(
        deal_count=("startup_name", "count"),
        total_funding_crores=("funding_crores", "sum"),
        avg_funding_crores=("funding_crores", "mean"),
        median_funding_crores=("funding_crores", "median"),
        above_avg_count=("above_sector_avg", "sum"),
    ).reset_index()
    
    grouped = grouped[grouped["deal_count"] >= min_deals]
    grouped["above_avg_pct"] = (
        (grouped["above_avg_count"] / grouped["deal_count"]) * 100
    ).round(2)
    grouped["avg_funding_crores"] = grouped["avg_funding_crores"].round(2)
    grouped["total_funding_crores"] = grouped["total_funding_crores"].round(2)
    grouped["median_funding_crores"] = grouped["median_funding_crores"].round(2)
    
    return grouped.sort_values(by="avg_funding_crores", ascending=False)


def get_city_summary(df: pd.DataFrame, min_deals: int = 1) -> pd.DataFrame:
    """Computes city intelligence metrics, sorted descending by average funding."""
    if len(df) == 0:
        return pd.DataFrame()
        
    grouped = df.groupby("city").agg(
        deal_count=("startup_name", "count"),
        total_funding_crores=("funding_crores", "sum"),
        avg_funding_crores=("funding_crores", "mean"),
        median_funding_crores=("funding_crores", "median"),
        is_bengaluru=("is_bengaluru", "max"),
    ).reset_index()
    
    grouped = grouped[grouped["deal_count"] >= min_deals]
    grouped["avg_funding_crores"] = grouped["avg_funding_crores"].round(2)
    grouped["total_funding_crores"] = grouped["total_funding_crores"].round(2)
    grouped["median_funding_crores"] = grouped["median_funding_crores"].round(2)
    
    return grouped.sort_values(by="avg_funding_crores", ascending=False)


def get_bengaluru_comparison(df: pd.DataFrame) -> Dict[str, Any]:
    """Generates comparative analytical metrics for Bengaluru vs all other cities."""
    if len(df) == 0:
        return {}
        
    bengaluru_df = df[df["is_bengaluru"] == True]
    others_df = df[df["is_bengaluru"] == False]
    
    b_kpis = calculate_market_kpis(bengaluru_df)
    o_kpis = calculate_market_kpis(others_df)
    
    return {
        "bengaluru": b_kpis,
        "others": o_kpis,
        "deal_ratio": round(b_kpis["total_records"] / max(o_kpis["total_records"], 1), 3),
        "funding_share_pct": round(
            (b_kpis["total_funding_crores"] / max(b_kpis["total_funding_crores"] + o_kpis["total_funding_crores"], 1e-9)) * 100,
            2
        )
    }


def get_funding_round_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates funding metrics by investment type and round number."""
    if len(df) == 0:
        return pd.DataFrame()
        
    grouped = df.groupby(["funding_round", "round_number"]).agg(
        deal_count=("startup_name", "count"),
        total_funding_crores=("funding_crores", "sum"),
        avg_funding_crores=("funding_crores", "mean"),
        median_funding_crores=("funding_crores", "median"),
    ).reset_index()
    
    grouped["avg_funding_crores"] = grouped["avg_funding_crores"].round(2)
    grouped["total_funding_crores"] = grouped["total_funding_crores"].round(2)
    grouped["median_funding_crores"] = grouped["median_funding_crores"].round(2)
    
    return grouped.sort_values(by="deal_count", ascending=False)


def get_time_series_aggregations(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Generates time activity aggregations across year, quarter, month, and day of week."""
    valid_dates = df.dropna(subset=["date"]).copy()
    
    # 1. Yearly
    yearly = valid_dates.groupby("year").agg(
        deal_count=("startup_name", "count"),
        total_funding_crores=("funding_crores", "sum"),
        avg_funding_crores=("funding_crores", "mean")
    ).reset_index()
    yearly["avg_funding_crores"] = yearly["avg_funding_crores"].round(2)
    yearly["total_funding_crores"] = yearly["total_funding_crores"].round(2)
    yearly["year"] = yearly["year"].astype(int)
    yearly = yearly.sort_values(by="year")
    
    # 2. Quarterly
    quarterly = valid_dates.groupby("quarter").agg(
        deal_count=("startup_name", "count"),
        total_funding_crores=("funding_crores", "sum"),
        avg_funding_crores=("funding_crores", "mean")
    ).reset_index()
    quarterly["avg_funding_crores"] = quarterly["avg_funding_crores"].round(2)
    quarterly["quarter_label"] = quarterly["quarter"].apply(lambda q: f"Q{int(q)}")
    quarterly = quarterly.sort_values(by="quarter")
    
    # 3. Year & Quarter Matrix
    year_quarter = valid_dates.groupby(["year", "quarter"]).agg(
        deal_count=("startup_name", "count"),
        total_funding_crores=("funding_crores", "sum")
    ).reset_index()
    year_quarter["period"] = year_quarter.apply(lambda r: f"{int(r['year'])} Q{int(r['quarter'])}", axis=1)
    year_quarter = year_quarter.sort_values(by=["year", "quarter"])
    
    # 4. Monthly
    monthly = valid_dates.groupby("month").agg(
        deal_count=("startup_name", "count"),
        total_funding_crores=("funding_crores", "sum")
    ).reset_index()
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly["month_name"] = monthly["month"].apply(lambda m: month_names[int(m)-1] if 1 <= int(m) <= 12 else str(m))
    monthly = monthly.sort_values(by="month")
    
    # 5. Day of week (0=Monday, 6=Sunday)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekday = valid_dates.groupby("day_of_week").agg(
        deal_count=("startup_name", "count"),
        total_funding_crores=("funding_crores", "sum")
    ).reset_index()
    weekday["day_name"] = weekday["day_of_week"].apply(lambda d: day_names[int(d)] if 0 <= int(d) <= 6 else str(d))
    weekday = weekday.sort_values(by="day_of_week")
    
    # 6. Era
    era = valid_dates.groupby("funding_era", observed=False).agg(
        deal_count=("startup_name", "count"),
        total_funding_crores=("funding_crores", "sum"),
        avg_funding_crores=("funding_crores", "mean")
    ).reset_index()
    era["avg_funding_crores"] = era["avg_funding_crores"].round(2)
    era["total_funding_crores"] = era["total_funding_crores"].round(2)
    
    return {
        "yearly": yearly,
        "quarterly": quarterly,
        "year_quarter": year_quarter,
        "monthly": monthly,
        "weekday": weekday,
        "era": era,
    }


def get_distribution_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes descriptive and quartile statistics for the funding distribution."""
    valid = df["funding_crores"].dropna()
    if len(valid) == 0:
        return {}
        
    q1 = float(np.percentile(valid, 25))
    q2 = float(np.percentile(valid, 50))
    q3 = float(np.percentile(valid, 75))
    iqr = q3 - q1
    lower_whisker = max(float(valid.min()), q1 - 1.5 * iqr)
    upper_whisker = min(float(valid.max()), q3 + 1.5 * iqr)
    outliers = valid[(valid < lower_whisker) | (valid > upper_whisker)]
    
    tier_counts = df["funding_tier"].value_counts().to_dict()
    quartile_counts = df["funding_quartile"].value_counts().to_dict()
    
    return {
        "count": int(len(valid)),
        "mean": round(float(valid.mean()), 2),
        "std": round(float(valid.std()), 2),
        "min": round(float(valid.min()), 2),
        "q1": round(q1, 2),
        "median": round(q2, 2),
        "q3": round(q3, 2),
        "max": round(float(valid.max()), 2),
        "iqr": round(iqr, 2),
        "outlier_count": int(len(outliers)),
        "outlier_pct": round(len(outliers) / len(valid) * 100, 2),
        "tier_counts": tier_counts,
        "quartile_counts": quartile_counts,
    }


def get_data_quality_report(df: pd.DataFrame) -> Dict[str, Any]:
    """Performs deep data quality and nullity auditing across the dataset."""
    total_rows = len(df)
    missing_summary = []
    
    for col in df.columns:
        null_cnt = df[col].isnull().sum()
        null_pct = (null_cnt / total_rows * 100) if total_rows > 0 else 0.0
        missing_summary.append({
            "Column": col,
            "Data Type": str(df[col].dtype),
            "Missing Count": int(null_cnt),
            "Missing Pct (%)": round(null_pct, 2),
            "Unique Values": int(df[col].nunique()),
        })
        
    missing_df = pd.DataFrame(missing_summary)
    duplicates_count = int(df.duplicated(subset=["startup_name", "date", "funding_round"]).sum())
    
    # Quality metrics
    unmapped_sectors_cnt = int((df["sector_category"] == "Other / Unmapped").sum()) if "sector_category" in df.columns else 0
    unmapped_rounds_cnt = int((df["round_number"] == 0).sum()) if "round_number" in df.columns else 0
    invalid_dates_cnt = int(df["date"].isnull().sum()) if "date" in df.columns else 0
    
    return {
        "total_records": total_rows,
        "total_columns": len(df.columns),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        "duplicates_count": duplicates_count,
        "unmapped_sectors_count": unmapped_sectors_cnt,
        "unmapped_rounds_count": unmapped_rounds_cnt,
        "invalid_dates_count": invalid_dates_cnt,
        "missing_table": missing_df,
    }
