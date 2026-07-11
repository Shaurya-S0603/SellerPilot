"""
etl/importer.py

Reads Blinkit sales reports from Excel files.

Responsibilities
----------------
- Accept uploaded Excel files
- Read them into a Pandas DataFrame
- Perform file validation
- Print import diagnostics
"""

from io import BytesIO
import pandas as pd


class SalesImporter:
    """
    Imports Blinkit Sales Reports.
    """

    SUPPORTED_EXTENSIONS = ("xlsx", "xls")

    def load(self, uploaded_file) -> pd.DataFrame:
        """
        Reads an uploaded Excel file.
        """

        if uploaded_file is None:
            raise ValueError("No file uploaded.")

        extension = uploaded_file.name.split(".")[-1].lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                "Unsupported file type. Please upload a .xlsx or .xls file."
            )

        try:

            df = pd.read_excel(
                BytesIO(uploaded_file.getvalue()),
                engine="openpyxl" if extension == "xlsx" else None,
            )

        except Exception as e:

            raise RuntimeError(
                f"Unable to read Excel file.\n{e}"
            ) from e

        if df.empty:
            raise ValueError(
                "The uploaded report contains no data."
            )

        # --------------------------------------------------
        # Normalize column names
        # --------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # --------------------------------------------------
        # Import Diagnostics
        # --------------------------------------------------

        print("\n" + "=" * 70)
        print("BLINKIT REPORT IMPORT")
        print("=" * 70)

        print(f"Rows Imported : {len(df)}")
        print(f"Columns Found : {len(df.columns)}")

        print("\nColumns:")

        for col in df.columns:
            print(f" • {col}")

        print("\nMissing Values")

        important_columns = [
            "Order Id",
            "Order Date",
            "Item Id",
            "Product Name",
            "Customer City",
            "Quantity",
            "Total Gross Bill Amount",
            "Order Status",
        ]

        for col in important_columns:

            if col in df.columns:

                missing = df[col].isna().sum()

                print(
                    f"{col:<30} {missing}"
                )

        if "Order Status" in df.columns:

            print("\nOrder Status Breakdown")

            print(
                df["Order Status"]
                .fillna("Missing")
                .value_counts(dropna=False)
            )

        print("=" * 70 + "\n")

        return df

    @staticmethod
    def preview(df: pd.DataFrame, rows: int = 5) -> pd.DataFrame:
        """
        Returns the first few rows.
        """

        return df.head(rows)

    @staticmethod
    def info(df: pd.DataFrame) -> dict:
        """
        Returns metadata about the imported report.
        """

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
        }