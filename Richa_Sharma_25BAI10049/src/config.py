"""
VentureTrack Configuration Module
Defines design system palette, paths, business constants, and schema mappings.
"""
from pathlib import Path
import numpy as np

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
RAW_DATA_PATH = DATA_DIR / "startup_funding_raw.csv"
CLEANED_DATA_PATH = DATA_DIR / "startup_funding_cleaned.csv"

# Branding & App Metadata
APP_NAME = "VENTURETRACK"
APP_SUBTITLE = "INDIAN STARTUP FUNDING INTELLIGENCE"
APP_TAGLINE = "Understand Funding. Discover Patterns. Evaluate Opportunities."
APP_VERSION = "2.4.0 (Academic Edition — Mini Project 13)"

# Design System Palette (Modern Editorial Fintech Intelligence)
THEME_COLORS = {
    "main_bg": "#F7F8F6",              # Crisp Editorial Canvas
    "secondary_bg": "#F0F2EF",         # Architectural Sidebar & Muted Background
    "secondary_surface": "#FFFFFF",    # Clean White Surface Card
    "elevated_card": "#FFFFFF",        # Elevated Surface
    "primary_text": "#17211F",         # Deep Slate Charcoal Typography
    "secondary_text": "#727D77",       # Refined Editorial Secondary Text
    "muted_text": "#94A39D",           # Muted Text & Minimal Labeling
    "primary_accent": "#315FCE",       # High-Conviction Institutional Cobalt
    "investment_blue": "#315FCE",      # Backwards-compatible alias
    "secondary_accent": "#16866A",     # Editorial Evergreen
    "electric_violet": "#6366F1",      # Modern Indigo Accent alias
    "growth_green": "#16866A",         # Positive Capital / Momentum
    "warning_amber": "#D79A42",        # High Conviction Alert Amber
    "danger_red": "#D9383A",           # Downside / Outlier Risk Indicator
    "highlight": "#E8EEF9",            # Editorial Focus Tint
    "borders": "#E5E9E5",              # Crisp Slate Border
    "border_solid": "#E5E9E5",         # Solid Slate Border
}

CHART_PALETTE = [
    "#315FCE",  # Primary Accent Cobalt
    "#16866A",  # Editorial Evergreen
    "#D79A42",  # Warm Amber
    "#6366F1",  # Modern Indigo
    "#0284C7",  # Cerulean
    "#8B5CF6",  # Violet
    "#0D9488",  # Deep Teal
    "#E11D48",  # Carmine
    "#D97706",  # Ochre
    "#2563EB",  # Classic Royal
]

# Business & Assignment Constants
USD_TO_INR_RATE = 83.0  # Fixed exchange rate specified in assignment: ₹83/USD
CRORE_DENOMINATOR = 10_000_000

# Canonical Column Names
RAW_TO_CLEAN_COLUMN_MAP = {
    "Sr No": "sr_no",
    "SNo": "sr_no",
    "Date dd/mm/yyyy": "date",
    "Date": "date",
    "Startup Name": "startup_name",
    "StartupName": "startup_name",
    "Industry Vertical": "sector",
    "IndustryVertical": "sector",
    "SubVertical": "sub_sector",
    "City  Location": "city",
    "CityLocation": "city",
    "Investors Name": "investors_name",
    "InvestorsName": "investors_name",
    "InvestmentnType": "funding_round",
    "InvestmentType": "funding_round",
    "Amount in USD": "funding_amount",
    "AmountInUSD": "funding_amount",
    "Remarks": "remarks",
}

# Task 2 Assignment Mapping Dictionaries
SECTOR_CATEGORY_MAP = {
    "Mobility": "Consumer",
    "FoodTech": "Consumer",
    "Grocery": "Consumer",
    "eCommerce": "Consumer",
    "FinTech": "Financial",
    "EdTech": "Social",
    "Beauty": "Consumer",
}

SERIES_ROUND_MAP = {
    "Series A": 1,
    "Series B": 2,
    "Series C": 3,
    "Series D": 4,
    "Series E": 5,
    "Series F": 6,
}

# Task 3 Binning Boundaries
FUNDING_TIER_BINS = [-np.inf, 99.999999, 300.0, np.inf]
FUNDING_TIER_LABELS = ["Small", "Mid", "Large"]

# Task 4 Era Boundaries
FUNDING_ERA_BINS = [-np.inf, 2019, 2021, np.inf]
FUNDING_ERA_LABELS = ["Early", "Pandemic", "Recovery"]

# Bengaluru Canonical Normalizations
BENGALURU_VARIANTS = {
    "bangalore",
    "bengaluru",
    "bangalore / usa",
    "bangalore / san mateo",
    "bangalore / sfo",
    "bengaluru / usa",
}

