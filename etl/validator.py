import pandas as pd
import logging
from datetime import datetime
from typing import Tuple

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates incoming data from Blinkit exports"""
    
    REQUIRED_SALES_FIELDS = ['order_date', 'sku', 'product_name', 'city', 'units_sold', 'revenue']
    REQUIRED_INVENTORY_FIELDS = ['date', 'sku', 'product_name', 'stock_quantity', 'warehouse_location']
    REQUIRED_COMPETITOR_FIELDS = ['date', 'sku', 'product_name', 'competitor_name', 'competitor_price', 'our_price']

    @staticmethod
    def validate(df: pd.DataFrame) -> pd.DataFrame:
        """Basic validation and column normalization"""
        if df.empty:
            raise ValueError("File is empty.")

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return df
    
    @staticmethod
    def validate_sales_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, list]:
        """
        Validate sales records
        
        Args:
            df: DataFrame with sales data
            
        Returns:
            Tuple of (valid_df, error_list)
        """
        df = DataValidator.validate(df)
        errors = []
        
        # Check required fields
        for field in DataValidator.REQUIRED_SALES_FIELDS:
            if field not in df.columns:
                errors.append(f"Missing required column: {field}")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        # Remove rows with null values in required fields
        df = df.dropna(subset=DataValidator.REQUIRED_SALES_FIELDS)
        
        # Validate date format
        try:
            df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d')
        except Exception as e:
            logger.error(f"Date format error: {e}")
            errors.append(f"Invalid date format in order_date: {e}")
        
        # Validate numeric fields
        try:
            df['units_sold'] = pd.to_numeric(df['units_sold'], errors='coerce')
            df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
        except Exception as e:
            logger.error(f"Numeric conversion error: {e}")
            errors.append(f"Invalid numeric values: {e}")
        
        # Remove rows with negative values
        df = df[(df['units_sold'] >= 0) & (df['revenue'] >= 0)]
        
        logger.info(f"Sales validation complete: {len(df)} valid records")
        return df, errors
    
    @staticmethod
    def validate_inventory_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, list]:
        """Validate inventory records"""
        df = DataValidator.validate(df)
        errors = []
        
        # Check required fields
        for field in DataValidator.REQUIRED_INVENTORY_FIELDS:
            if field not in df.columns:
                errors.append(f"Missing required column: {field}")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        # Remove rows with null values in required fields
        df = df.dropna(subset=DataValidator.REQUIRED_INVENTORY_FIELDS)
        
        # Validate date format
        try:
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        except Exception as e:
            logger.error(f"Date format error: {e}")
            errors.append(f"Invalid date format: {e}")
        
        # Validate stock quantity
        try:
            df['stock_quantity'] = pd.to_numeric(df['stock_quantity'], errors='coerce')
        except Exception as e:
            logger.error(f"Stock quantity error: {e}")
            errors.append(f"Invalid stock quantity: {e}")
        
        # Remove rows with negative stock
        df = df[df['stock_quantity'] >= 0]
        
        logger.info(f"Inventory validation complete: {len(df)} valid records")
        return df, errors
    
    @staticmethod
    def validate_competitor_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, list]:
        """Validate competitor tracking records"""
        df = DataValidator.validate(df)
        errors = []
        
        # Check required fields
        for field in DataValidator.REQUIRED_COMPETITOR_FIELDS:
            if field not in df.columns:
                errors.append(f"Missing required column: {field}")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        # Remove rows with null values in required fields
        df = df.dropna(subset=DataValidator.REQUIRED_COMPETITOR_FIELDS)
        
        # Validate date format
        try:
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        except Exception as e:
            logger.error(f"Date format error: {e}")
            errors.append(f"Invalid date format: {e}")
        
        # Validate prices
        try:
            df['competitor_price'] = pd.to_numeric(df['competitor_price'], errors='coerce')
            df['our_price'] = pd.to_numeric(df['our_price'], errors='coerce')
        except Exception as e:
            logger.error(f"Price conversion error: {e}")
            errors.append(f"Invalid price values: {e}")
        
        # Remove rows with negative prices
        df = df[(df['competitor_price'] >= 0) & (df['our_price'] >= 0)]
        
        logger.info(f"Competitor validation complete: {len(df)} valid records")
        return df, errors