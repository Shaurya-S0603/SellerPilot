"""
etl/loader.py

Loads cleaned sales data into the SQLite database.

Responsibilities
----------------
- Validate cleaned data
- Remove ETL-only columns
- Load data into SQLite
- Verify successful import
"""

import pandas as pd

from database.db import get_engine


class DatabaseLoader:
    """
    Loads cleaned sales data into the SQLite database.
    """

    TABLE_NAME = "sales"

    # Columns that should exist in the final database
    FINAL_COLUMNS = [
        "order_date",
        "sku",
        "product_name",
        "city",
        "darkstore",
        "warehouse",
        "units_sold",
        "revenue",
    ]

    def load_sales(self, dataframe: pd.DataFrame) -> int:
        """
        Loads a cleaned sales DataFrame into SQLite.
        """

        if dataframe.empty:
            raise ValueError(
                "Cannot load an empty DataFrame."
            )

        df = dataframe.copy()

        # --------------------------------------------------
        # Keep only database columns
        # --------------------------------------------------

        missing = [
            col
            for col in self.FINAL_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        df = df[self.FINAL_COLUMNS]

        # --------------------------------------------------
        # Load SQLite
        # --------------------------------------------------

        engine = get_engine()

        try:

            df.to_sql(
                name=self.TABLE_NAME,
                con=engine,
                if_exists="replace",
                index=False,
                method="multi",
                chunksize=1000,
            )

        finally:

            engine.dispose()

        print(f"Loaded {len(df):,} rows into SQLite.")

        return len(df)

    def get_sales(self) -> pd.DataFrame:
        """
        Returns the sales table.
        """

        engine = get_engine()

        try:

            return pd.read_sql(
                "SELECT * FROM sales",
                engine,
            )

        finally:

            engine.dispose()

    def row_count(self) -> int:
        """
        Returns total number of rows.
        """

        engine = get_engine()

        try:

            result = pd.read_sql(
                "SELECT COUNT(*) AS count FROM sales",
                engine,
            )

            return int(result.loc[0, "count"])

        finally:

            engine.dispose()

    def table_exists(self) -> bool:
        """
        Checks whether the sales table exists.
        """

        engine = get_engine()

        try:

            result = pd.read_sql(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name='sales'
                """,
                engine,
            )

            return not result.empty

        finally:

            engine.dispose()

    def verify_import(self, expected_rows: int) -> bool:
        """
        Verifies that the import completed successfully.
        """

        if not self.table_exists():
            return False

        actual_rows = self.row_count()

        print(
            f"Verification: expected={expected_rows:,}, "
            f"actual={actual_rows:,}"
        )

        return actual_rows == expected_rows