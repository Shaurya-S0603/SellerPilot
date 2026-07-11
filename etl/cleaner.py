"""
etl/cleaner.py

Cleans and standardizes Blinkit Sales Reports.

Responsibilities
----------------
- Validate required columns
- Preserve every sales record
- Standardize data
- Fill missing values
- Generate import statistics
- Save cleaned CSV
"""

import pandas as pd

from config.settings import (
    CLEAN_SALES_FILE,
    REQUIRED_SALES_COLUMNS,
)


class SalesCleaner:

    COLUMN_MAPPING = {
        "Order Id": "order_id",
        "Order Date": "order_date",
        "Item Id": "sku",
        "Product Name": "product_name",
        "Customer City": "city",
        "Quantity": "units_sold",
        "Total Gross Bill Amount": "revenue",
        "Order Status": "order_status",
    }

    FINAL_COLUMNS = [
        "order_id",
        "order_status",
        "order_date",
        "sku",
        "product_name",
        "city",
        "darkstore",
        "warehouse",
        "units_sold",
        "revenue",
    ]

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:

        original_rows = len(df)

        df = df.copy()

        # --------------------------------------------------
        # Normalize headers
        # --------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # --------------------------------------------------
        # Validate columns
        # --------------------------------------------------

        missing = [
            col
            for col in REQUIRED_SALES_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {', '.join(missing)}"
            )

        # --------------------------------------------------
        # Rename columns
        # --------------------------------------------------

        df = df.rename(columns=self.COLUMN_MAPPING)

        # --------------------------------------------------
        # Future columns
        # --------------------------------------------------

        df["darkstore"] = "Unknown"
        df["warehouse"] = "Unknown"

        # --------------------------------------------------
        # Keep required columns
        # --------------------------------------------------

        df = df[self.FINAL_COLUMNS]

        # --------------------------------------------------
        # Remove only fully blank rows
        # --------------------------------------------------

        df = df.dropna(how="all")

        # --------------------------------------------------
        # Order ID
        # --------------------------------------------------

        df["order_id"] = (
            df["order_id"]
            .fillna("UNKNOWN")
            .astype(str)
            .str.strip()
        )

        df.loc[df["order_id"] == "", "order_id"] = "UNKNOWN"

        # --------------------------------------------------
        # Order Status
        # --------------------------------------------------

        df["order_status"] = (
            df["order_status"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        # --------------------------------------------------
        # Dates
        # --------------------------------------------------

        df["order_date"] = pd.to_datetime(
            df["order_date"],
            errors="coerce",
        )

        # keep missing dates instead of deleting rows
        missing_dates = df["order_date"].isna().sum()

        # --------------------------------------------------
        # SKU
        # --------------------------------------------------

        df["sku"] = (
            df["sku"]
            .fillna("UNKNOWN")
            .astype(str)
            .str.strip()
        )

        df.loc[df["sku"] == "", "sku"] = "UNKNOWN"

        # --------------------------------------------------
        # Product
        # --------------------------------------------------

        df["product_name"] = (
            df["product_name"]
            .fillna("Unknown Product")
            .astype(str)
            .str.strip()
        )

        df.loc[
            df["product_name"] == "",
            "product_name"
        ] = "Unknown Product"

        # --------------------------------------------------
        # City
        # --------------------------------------------------

        df["city"] = (
            df["city"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        df.loc[df["city"] == "", "city"] = "Unknown"

        # --------------------------------------------------
        # Units Sold
        # --------------------------------------------------

        df["units_sold"] = (
            pd.to_numeric(
                df["units_sold"],
                errors="coerce",
            )
            .fillna(0)
            .astype(int)
        )

        # --------------------------------------------------
        # Revenue
        # --------------------------------------------------

        df["revenue"] = (
            pd.to_numeric(
                df["revenue"],
                errors="coerce",
            )
            .fillna(0.0)
        )

        # --------------------------------------------------
        # Sort
        # --------------------------------------------------

        df = (
            df.sort_values(
                by="order_date",
                na_position="last",
            )
            .reset_index(drop=True)
        )

        # --------------------------------------------------
        # Save cleaned CSV
        # --------------------------------------------------

        df.to_csv(
            CLEAN_SALES_FILE,
            index=False,
        )

        # --------------------------------------------------
        # Import Report
        # --------------------------------------------------

        print("\n" + "=" * 70)
        print("CLEANING SUMMARY")
        print("=" * 70)

        print(f"Original Rows : {original_rows}")
        print(f"Final Rows    : {len(df)}")

        print()

        print("Missing Values")

        print(f"Order Dates : {missing_dates}")
        print(f"SKU         : {(df['sku']=='UNKNOWN').sum()}")
        print(f"Products    : {(df['product_name']=='Unknown Product').sum()}")
        print(f"Cities      : {(df['city']=='Unknown').sum()}")

        print()

        print("Order Status")

        print(
            df["order_status"]
            .value_counts(dropna=False)
        )

        print("=" * 70)

        return df

    @staticmethod
    def summary(df):

        return {
            "rows": len(df),
            "products": df["product_name"].nunique(),
            "cities": df["city"].nunique(),
            "units_sold": int(df["units_sold"].sum()),
            "revenue": round(df["revenue"].sum(), 2),
        }