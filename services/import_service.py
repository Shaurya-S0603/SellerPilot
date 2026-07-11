"""
services/import_service.py

Coordinates the complete Blinkit Sales Report import workflow.
"""

from datetime import datetime
import time

from database.init_db import DatabaseInitializer
from etl.cleaner import SalesCleaner
from etl.importer import SalesImporter
from etl.loader import DatabaseLoader
from utils.logger import get_logger


class ImportService:
    """
    Coordinates the complete sales import workflow.
    """

    def __init__(self):

        self.importer = SalesImporter()
        self.cleaner = SalesCleaner()
        self.initializer = DatabaseInitializer()
        self.loader = DatabaseLoader()

        self.logger = get_logger("ImportService")

    def run(self, uploaded_file) -> dict:
        """
        Executes the complete ETL pipeline.
        """

        start_time = time.perf_counter()

        try:

            self.logger.info("=" * 70)
            self.logger.info("STARTING SALES IMPORT")
            self.logger.info("=" * 70)

            # --------------------------------------------------
            # Import
            # --------------------------------------------------

            self.logger.info("Reading Excel report...")

            raw_df = self.importer.load(uploaded_file)

            raw_rows = len(raw_df)

            self.logger.info(
                f"Excel rows imported: {raw_rows:,}"
            )

            # --------------------------------------------------
            # Clean
            # --------------------------------------------------

            self.logger.info("Cleaning report...")

            clean_df = self.cleaner.clean(raw_df)

            cleaned_rows = len(clean_df)

            self.logger.info(
                f"Rows after cleaning: {cleaned_rows:,}"
            )

            # --------------------------------------------------
            # Database Reset
            # --------------------------------------------------

            self.logger.info("Resetting SQLite database...")

            self.initializer.reset_database()

            self.logger.info("Database reset complete.")

            # --------------------------------------------------
            # Load
            # --------------------------------------------------

            self.logger.info("Loading SQLite database...")

            imported_rows = self.loader.load_sales(clean_df)

            self.logger.info(
                f"Rows loaded into SQLite: {imported_rows:,}"
            )

            # --------------------------------------------------
            # Verify
            # --------------------------------------------------

            if not self.loader.verify_import(imported_rows):

                raise RuntimeError(
                    "Database verification failed."
                )

            db_rows = self.loader.row_count()

            self.logger.info(
                f"Database verification successful ({db_rows:,} rows)."
            )

            # --------------------------------------------------
            # Summary
            # --------------------------------------------------

            summary = self.cleaner.summary(clean_df)

            duration = round(
                time.perf_counter() - start_time,
                2,
            )

            self.logger.info("=" * 70)
            self.logger.info("IMPORT SUMMARY")
            self.logger.info("=" * 70)

            self.logger.info(f"Excel Rows      : {raw_rows:,}")
            self.logger.info(f"Cleaned Rows    : {cleaned_rows:,}")
            self.logger.info(f"SQLite Rows     : {db_rows:,}")
            self.logger.info(f"Duration        : {duration:.2f} sec")

            if raw_rows != cleaned_rows:
                self.logger.warning(
                    f"Cleaning changed row count "
                    f"({raw_rows} → {cleaned_rows})"
                )

            if cleaned_rows != db_rows:
                self.logger.warning(
                    f"Loader changed row count "
                    f"({cleaned_rows} → {db_rows})"
                )

            self.logger.info("=" * 70)

            return {
                "success": True,
                "message": "Sales report imported successfully.",
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "duration_seconds": duration,
                "raw_rows": raw_rows,
                "cleaned_rows": cleaned_rows,
                "imported_rows": db_rows,
                "summary": summary,
                "dataframe": clean_df,
            }

        except Exception as e:

            self.logger.exception("Import failed.")

            raise RuntimeError(
                f"Import failed: {str(e)}"
            ) from e