from pathlib import Path
import logging
from datetime import datetime

from etl.importer import BlinkitImporter
from etl.validator import DataValidator
from etl.transformer import DataTransformer
from etl.loader import DataLoader
from database.db import engine, SessionLocal
from database import models

logger = logging.getLogger(__name__)


class ETLPipeline:
    """Main ETL Pipeline Orchestrator"""

    def __init__(self):
        self.importer = BlinkitImporter()
        self.validator = DataValidator()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
        self.session = SessionLocal()

    def run(self, file_path: Path, table_name: str):
        """
        Run ETL pipeline for a given file
        
        Args:
            file_path: Path to data file (CSV or Excel)
            table_name: Target table name
        """
        try:
            logger.info(f"Starting ETL pipeline for {file_path}")
            print(f"📥 Starting ETL pipeline for {file_path}")

            # Import
            if file_path.suffix == ".csv":
                df = self.importer.read_csv(file_path)
            else:
                df = self.importer.read_excel(file_path)
            
            logger.info(f"Imported {len(df)} records")

            # Validate
            df = self.validator.validate(df)
            logger.info(f"Validation complete: {len(df)} records")

            # Transform
            df = self.transformer.transform(df)
            logger.info(f"Transformation complete: {len(df)} records")

            # Load
            self.loader.load(df, table_name, engine)
            logger.info(f"✅ ETL pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"❌ ETL pipeline failed: {e}")
            raise
    
    def run_sales_pipeline(self, file_path) -> int:
        """
        Run ETL pipeline specifically for sales data
        
        Args:
            file_path: Path to sales data file (str or Path)
            
        Returns:
            Number of records loaded
        """
        try:
            # Convert to Path if string
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            logger.info(f"Starting sales ETL pipeline: {file_path}")
            print(f"📥 Processing sales data...")
            
            # Import
            if file_path.suffix == ".csv":
                df = self.importer.read_csv(file_path)
            else:
                df = self.importer.read_excel(file_path)
            
            logger.info(f"Imported {len(df)} sales records")
            
            # Validate
            df, errors = self.validator.validate_sales_data(df)
            if errors:
                logger.warning(f"Validation errors: {errors}")
            
            logger.info(f"Validation complete: {len(df)} valid records")
            
            # Transform
            df = self.transformer.transform_sales_data(df)
            logger.info(f"Transformation complete: {len(df)} records")
            
            # Load
            records_loaded = self.loader.load_sales_data(df, self.session)
            
            # Update metrics
            self.loader.update_daily_metrics(self.session)
            
            logger.info(f"✅ Sales ETL pipeline completed: {records_loaded} records loaded")
            return records_loaded
            
        except Exception as e:
            logger.error(f"❌ Sales ETL pipeline failed: {e}")
            raise
    
    def run_inventory_pipeline(self, file_path) -> int:
        """Run ETL pipeline specifically for inventory data"""
        try:
            # Convert to Path if string
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            logger.info(f"Starting inventory ETL pipeline: {file_path}")
            print(f"📥 Processing inventory data...")
            
            # Import
            if file_path.suffix == ".csv":
                df = self.importer.read_csv(file_path)
            else:
                df = self.importer.read_excel(file_path)
            
            logger.info(f"Imported {len(df)} inventory records")
            
            # Validate
            df, errors = self.validator.validate_inventory_data(df)
            if errors:
                logger.warning(f"Validation errors: {errors}")
            
            logger.info(f"Validation complete: {len(df)} valid records")
            
            # Transform
            df = self.transformer.transform_inventory_data(df)
            logger.info(f"Transformation complete: {len(df)} records")
            
            # Load
            records_loaded = self.loader.load_inventory_data(df, self.session)
            logger.info(f"✅ Inventory ETL pipeline completed: {records_loaded} records loaded")
            return records_loaded
            
        except Exception as e:
            logger.error(f"❌ Inventory ETL pipeline failed: {e}")
            raise
    
    def run_competitor_pipeline(self, file_path) -> int:
        """Run ETL pipeline specifically for competitor data"""
        try:
            # Convert to Path if string
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            logger.info(f"Starting competitor ETL pipeline: {file_path}")
            print(f"📥 Processing competitor data...")
            
            # Import
            if file_path.suffix == ".csv":
                df = self.importer.read_csv(file_path)
            else:
                df = self.importer.read_excel(file_path)
            
            logger.info(f"Imported {len(df)} competitor records")
            
            # Validate
            df, errors = self.validator.validate_competitor_data(df)
            if errors:
                logger.warning(f"Validation errors: {errors}")
            
            logger.info(f"Validation complete: {len(df)} valid records")
            
            # Transform
            df = self.transformer.transform_competitor_data(df)
            logger.info(f"Transformation complete: {len(df)} records")
            
            # Load
            records_loaded = self.loader.load_competitor_data(df, self.session)
            logger.info(f"✅ Competitor ETL pipeline completed: {records_loaded} records loaded")
            return records_loaded
            
        except Exception as e:
            logger.error(f"❌ Competitor ETL pipeline failed: {e}")
            raise
    
    def close(self):
        """Close database session"""
        if self.session:
            self.session.close()