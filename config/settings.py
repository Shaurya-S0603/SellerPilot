"""
config/settings.py

Central configuration for RealNut Intelligence.

All project paths are defined here.
No other file should hardcode file or folder paths.
"""

from pathlib import Path

# ==========================================================
# Project Root
# ==========================================================

# Project/
# ├── app.py
# ├── config/
# ├── database/
# ├── data/
# └── ...

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# Data Directories
# ==========================================================

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

DATABASE_DIR = DATA_DIR / "database"

LOGS_DIR = BASE_DIR / "logs"
LOG_FILE = LOGS_DIR / "app.log"

LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Database
# ==========================================================

DATABASE_NAME = "realnut.db"

DATABASE_PATH = DATABASE_DIR / DATABASE_NAME


# ==========================================================
# Processed Files
# ==========================================================

CLEAN_SALES_FILE = PROCESSED_DATA_DIR / "sales_clean.csv"


# ==========================================================
# Application
# ==========================================================

APP_NAME = "RealNut Intelligence"

APP_VERSION = "1.0.0"


# ==========================================================
# Required Sales Columns
# ==========================================================

REQUIRED_SALES_COLUMNS = [
    "Order Date",
    "Item Id",
    "Product Name",
    "Customer City",
    "Quantity",
    "Total Gross Bill Amount",
]


# ==========================================================
# Ensure Directories Exist
# ==========================================================

for directory in (
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    DATABASE_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)