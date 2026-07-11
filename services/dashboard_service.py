"""
services/dashboard_service.py

Dashboard data service for RealNut Intelligence.

This service provides all data required by the Streamlit UI.
No page should query SQLite directly.
"""

from pathlib import Path
import pandas as pd

from database.db import get_engine
from config.settings import DATABASE_PATH, LOG_FILE


class DashboardService:
    """
    Provides data for the dashboard pages.
    """

    # ==========================================================
    # Database Status
    # ==========================================================

    def database_ready(self) -> bool:
        """
        Returns True if the SQLite database and sales table exist.
        """

        if not Path(DATABASE_PATH).exists():
            return False

        try:

            engine = get_engine()

            result = pd.read_sql(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name='sales';
                """,
                engine,
            )

            engine.dispose()

            return not result.empty

        except Exception:
            return False

    # ==========================================================
    # Load Sales Table
    # ==========================================================

    def get_sales(self) -> pd.DataFrame:
        """
        Returns the sales table.
        """

        if not self.database_ready():
            return pd.DataFrame()

        engine = get_engine()

        df = pd.read_sql("SELECT * FROM sales", engine)

        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(
                df["order_date"],
                errors="coerce"
            )

        engine.dispose()

        return df

    # ==========================================================
    # Executive Summary
    # ==========================================================

    def get_summary(self) -> dict:

        df = self.get_sales()

        if df.empty:

            return {

                "database_ready": False,

                "rows": 0,

                "products": 0,

                "cities": 0,

                "orders": 0,

                "units_sold": 0,

                "revenue": 0.0,

                "avg_revenue_per_unit": 0.0,

                "last_import": "Never"

            }

        revenue = float(df["revenue"].sum())

        units = int(df["units_sold"].sum())

        avg = revenue / units if units else 0

        return {

            "database_ready": True,

            "rows": len(df),

            "products": int(df["product_name"].nunique()),

            "cities": int(df["city"].nunique()),

            "orders": int(df["order_id"].nunique()) if "order_id" in df.columns else len(df),

            "units_sold": units,

            "revenue": revenue,

            "avg_revenue_per_unit": round(avg, 2),

            "last_import": "Latest Session"

        }

    # ==========================================================
    # Revenue Trend
    # ==========================================================

    def get_revenue_trend(self) -> pd.DataFrame:

        df = self.get_sales()

        if df.empty:
            return df

        df["order_date"] = pd.to_datetime(df["order_date"])

        trend = (

            df.groupby("order_date", as_index=False)

            .agg(
                revenue=("revenue", "sum"),
                units_sold=("units_sold", "sum"),
            )

            .sort_values("order_date")

        )

        return trend

    # ==========================================================
    # Top Products
    # ==========================================================

    def get_top_products(
        self,
        limit: int = 5
    ) -> pd.DataFrame:

        df = self.get_sales()

        if df.empty:
            return df

        return (

            df.groupby("product_name", as_index=False)

            .agg(
                revenue=("revenue", "sum"),
                units_sold=("units_sold", "sum"),
                orders=("sku", "count"),
            )

            .sort_values(
                "revenue",
                ascending=False,
            )

            .head(limit)

        )

    # ==========================================================
    # Lowest Performing Products
    # ==========================================================

    def get_low_performing_products(
        self,
        limit: int = 10
    ) -> pd.DataFrame:

        df = self.get_sales()

        if df.empty:
            return df

        return (

            df.groupby("product_name", as_index=False)

            .agg(
                revenue=("revenue", "sum"),
                units_sold=("units_sold", "sum"),
                orders=("sku", "count"),
            )

            .sort_values(
                "revenue",
                ascending=True,
            )

            .head(limit)

        )

    # ==========================================================
    # Sales by City
    # ==========================================================

    def get_sales_by_city(self) -> pd.DataFrame:

        df = self.get_sales()

        if df.empty:
            return df

        return (
            df.groupby("city", as_index=False)
            .agg(
                revenue=("revenue", "sum"),
                units_sold=("units_sold", "sum"),
                orders=("sku", "count"),
            )
            .sort_values(
                "revenue",
                ascending=False,
            )
            .reset_index(drop=True)
        )

    # ==========================================================
    # Top Cities
    # ==========================================================

    def get_top_cities(
        self,
        limit: int = 10,
    ) -> pd.DataFrame:
        """
        Returns the highest revenue generating cities.
        """

        cities = self.get_sales_by_city()

        if cities.empty:
            return cities

        return (
            cities
            .sort_values(
                "revenue",
                ascending=False,
            )
            .head(limit)
            .reset_index(drop=True)
        )
    
    # ==========================================================
    # Bottom Cities
    # ==========================================================

    def get_bottom_cities(
        self,
        limit: int = 10,
    ) -> pd.DataFrame:

        cities = self.get_sales_by_city()

        if cities.empty:
            return cities

        return (
            cities
            .sort_values(
                "revenue",
                ascending=True,
            )
            .head(limit)
            .reset_index(drop=True)
        )

    def get_best_city(self):
        cities = self.get_sales_by_city()

        if cities.empty:
            return None

        return cities.iloc[0]
    
    def get_average_city_revenue(self):

        cities = self.get_sales_by_city()

        if cities.empty:
            return 0

        return float(cities["revenue"].mean())
    # ==========================================================
    # City Contribution
    # ==========================================================

    def get_city_contribution(
        self,
        limit: int = 10,
    ) -> pd.DataFrame:

        cities = self.get_sales_by_city()

        if cities.empty:
            return cities

        total_revenue = cities["revenue"].sum()

        cities["Contribution %"] = (
            cities["revenue"] / total_revenue * 100
        ).round(2)

        return (
            cities
            .sort_values(
                "revenue",
                ascending=False,
            )
            .head(limit)
            .reset_index(drop=True)
        )
    # ==========================================================
    # Recent Activity
    # ==========================================================

    def get_recent_activity(
        self,
        limit: int = 5
    ) -> list[str]:
        """
        Reads the last INFO entries from logs/app.log.
        """

        log_path = Path(LOG_FILE)

        if not log_path.exists():
            return []

        with open(
            log_path,
            "r",
            encoding="utf-8"
        ) as f:

            lines = [
                line.strip()
                for line in f.readlines()
                if "INFO" in line
            ]

        return lines[-limit:]
    
    # ==========================================================
    # Weekly Comparison
    # ==========================================================

    def get_weekly_comparison(self) -> dict:

        df = self.get_sales()

        if df.empty:
            return {
                "this_week_revenue": 0,
                "last_week_revenue": 0,
                "change_percent": 0,
            }

        latest = df["order_date"].max()

        this_week_start = latest - pd.Timedelta(days=6)
        last_week_start = latest - pd.Timedelta(days=13)
        last_week_end = latest - pd.Timedelta(days=7)

        this_week = df.loc[
            df["order_date"] >= this_week_start,
            "revenue"
        ].sum()

        last_week = df.loc[
            (df["order_date"] >= last_week_start)
            &
            (df["order_date"] <= last_week_end),
            "revenue"
        ].sum()

        change = 0 if last_week == 0 else (
            (this_week - last_week) / last_week * 100
        )

        return {
            "this_week_revenue": round(this_week, 2),
            "last_week_revenue": round(last_week, 2),
            "change_percent": round(change, 2),
        }

    
    # ==========================================================
    # Bottom 10 Products
    # ==========================================================

    def get_bottom_products(self, limit=10):
        return self.get_low_performing_products(limit)
    
    # ==========================================================
    # Revenue by Product
    # ==========================================================

    def get_product_revenue(self):

        df = self.get_sales()

        if df.empty:
            return df

        return (

            df.groupby("product_name",as_index=False)

            .agg(
                revenue=("revenue","sum")
            )

            .sort_values(
                "revenue",
                ascending=False
            )

        )
    
    # ==========================================================
    # Units Sold by Product
    # ==========================================================

    def get_product_units(self):

        df = self.get_sales()

        if df.empty:
            return df

        return (

            df.groupby("product_name",as_index=False)

            .agg(
                units_sold=("units_sold","sum")
            )

            .sort_values(
                "units_sold",
                ascending=False
            )

        )
    
    # ==========================================================
    # Current Week Revenue
    # ==========================================================

    def get_current_week_revenue(self) -> float:

        df = self.get_sales()

        if df.empty:
            return 0

        latest = df["order_date"].max()

        week_start = latest - pd.Timedelta(days=6)

        return float(
            df.loc[
                df["order_date"] >= week_start,
                "revenue"
            ].sum()
        )
    
    # ==========================================================
    # Previous Week Revenue
    # ==========================================================

    def get_last_week_revenue(self) -> float:

        df = self.get_sales()

        if df.empty:
            return 0

        latest = df["order_date"].max()

        this_week_start = latest - pd.Timedelta(days=6)

        last_week_start = latest - pd.Timedelta(days=13)

        return float(
            df.loc[
                (df["order_date"] >= last_week_start)
                &
                (df["order_date"] < this_week_start),
                "revenue"
            ].sum()
        )
    
    # ==========================================================
    # Week over Week Change
    # ==========================================================

    def get_weekly_change_percent(self) -> float:

        previous = self.get_last_week_revenue()
        current = self.get_current_week_revenue()

        if previous == 0:
            return 0

        return round(
            ((current - previous) / previous) * 100,
            2
        )
    
    # ==========================================================
    # Product Contribution
    # ==========================================================

    def get_product_contribution(self):

        df = self.get_sales()

        if df.empty:
            return df

        total = df["revenue"].sum()

        result = (
            df.groupby("product_name", as_index=False)
            .agg(revenue=("revenue", "sum"))
            .sort_values("revenue", ascending=False)
        )

        result["Contribution %"] = (
            result["revenue"] / total * 100
        ).round(2)

        return result
    
    def get_recent_sales(self, limit=20):

        df = self.get_sales()

        if df.empty:
            return df

        return (
            df.sort_values(
                "order_date",
                ascending=False
            )
            .head(limit)
        )