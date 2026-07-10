import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DataTransformer:
    """Transforms and normalizes data for storage"""

    @staticmethod
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        """Basic transformation"""
        df = df.copy()
        return df
    
    @staticmethod
    def transform_sales_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform sales data for database storage
        
        Args:
            df: DataFrame with validated sales data
            
        Returns:
            Transformed DataFrame ready for database
        """
        df = df.copy()
        
        # Ensure date format
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'])
        
        # Ensure numeric types
        numeric_cols = ['units_sold', 'revenue']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Calculate average price per unit
        df['price_per_unit'] = df.apply(
            lambda row: row['revenue'] / row['units_sold'] if row['units_sold'] > 0 else 0,
            axis=1
        )
        
        # Standardize column names for database
        df = df.rename(columns={
            'order_date': 'order_date',
            'sku': 'sku',
            'product_name': 'product_name',
            'city': 'city',
            'units_sold': 'units_sold',
            'revenue': 'revenue'
        })
        
        # Add processing timestamp
        df['created_at'] = datetime.utcnow()
        
        logger.info(f"Sales data transformed: {len(df)} records")
        return df
    
    @staticmethod
    def transform_inventory_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform inventory data for database storage
        
        Args:
            df: DataFrame with validated inventory data
            
        Returns:
            Transformed DataFrame ready for database
        """
        df = df.copy()
        
        # Ensure date format
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Ensure numeric types
        numeric_cols = ['stock_quantity', 'daily_consumption', 'stock_age_days']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            else:
                df[col] = 0
        
        # Calculate inventory status
        df['status'] = df.apply(
            lambda row: DataTransformer._get_inventory_status(
                row.get('stock_quantity', 0),
                row.get('daily_consumption', 0),
                row.get('stock_age_days', 0)
            ),
            axis=1
        )
        
        # Add processing timestamp
        df['created_at'] = datetime.utcnow()
        
        logger.info(f"Inventory data transformed: {len(df)} records")
        return df
    
    @staticmethod
    def transform_competitor_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform competitor data for database storage
        
        Args:
            df: DataFrame with validated competitor data
            
        Returns:
            Transformed DataFrame ready for database
        """
        df = df.copy()
        
        # Ensure date format
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Ensure numeric types
        numeric_cols = ['competitor_price', 'our_price', 'rating', 'review_count']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            else:
                df[col] = 0
        
        # Calculate price difference
        df['price_difference'] = df['our_price'] - df['competitor_price']
        
        # Add processing timestamp
        df['created_at'] = datetime.utcnow()
        
        logger.info(f"Competitor data transformed: {len(df)} records")
        return df
    
    @staticmethod
    def _get_inventory_status(stock_qty: float, daily_consumption: float, stock_age_days: int) -> str:
        """
        Determine inventory status based on multiple factors
        
        Args:
            stock_qty: Current stock quantity
            daily_consumption: Daily consumption rate
            stock_age_days: Number of days stock has been held
            
        Returns:
            Status string: 'critical', 'understock', 'overstock', or 'normal'
        """
        # Calculate days of stock available
        if daily_consumption > 0:
            days_of_stock = stock_qty / daily_consumption
        else:
            days_of_stock = float('inf') if stock_qty > 0 else 0
        
        # Status logic
        if stock_qty == 0:
            return 'critical'
        elif days_of_stock < 7:
            return 'understock'
        elif days_of_stock > 60 or stock_age_days > 90:
            return 'overstock'
        else:
            return 'normal'