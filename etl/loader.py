import pandas as pd
import logging
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from database.db import engine, SessionLocal
from database import models
from datetime import datetime, date

logger = logging.getLogger(__name__)


class DataLoader:
    """Loads validated and transformed data into the database"""

    @staticmethod
    def load(df: pd.DataFrame, table_name: str, engine=None):
        """
        Load data using SQLAlchemy pandas integration
        
        Args:
            df: DataFrame to load
            table_name: Target table name
            engine: SQLAlchemy engine
        """
        if engine is None:
            engine = engine
        
        try:
            df.to_sql(
                table_name,
                engine,
                if_exists="append",
                index=False
            )
            logger.info(f"Inserted {len(df)} rows into {table_name}")
            print(f"✅ Inserted {len(df)} rows into {table_name}")
        except Exception as e:
            logger.error(f"Error loading data to {table_name}: {e}")
            raise
    
    @staticmethod
    def load_sales_data(df: pd.DataFrame, session: Session = None) -> int:
        """
        Load sales data into the database
        
        Args:
            df: DataFrame with sales data
            session: SQLAlchemy session
            
        Returns:
            Number of records loaded
        """
        if session is None:
            session = SessionLocal()
        
        try:
            records_loaded = 0
            
            for _, row in df.iterrows():
                sale = models.Sale(
                    order_date=row.get('order_date'),
                    sku=row.get('sku'),
                    product_name=row.get('product_name'),
                    city=row.get('city'),
                    darkstore=row.get('darkstore', ''),
                    warehouse=row.get('warehouse', ''),
                    units_sold=int(row.get('units_sold', 0)),
                    revenue=float(row.get('revenue', 0.0))
                )
                session.add(sale)
                records_loaded += 1
            
            session.commit()
            logger.info(f"Loaded {records_loaded} sales records")
            print(f"✅ Loaded {records_loaded} sales records")
            return records_loaded
        
        except Exception as e:
            session.rollback()
            logger.error(f"Error loading sales data: {e}")
            raise
        finally:
            session.close()
    
    @staticmethod
    def load_inventory_data(df: pd.DataFrame, session: Session = None) -> int:
        """Load inventory data into the database"""
        if session is None:
            session = SessionLocal()
        
        try:
            records_loaded = 0
            
            for _, row in df.iterrows():
                inventory = models.Inventory(
                    sku=row.get('sku'),
                    product_name=row.get('product_name'),
                    date=row.get('date'),
                    stock_quantity=int(row.get('stock_quantity', 0)),
                    stock_age_days=int(row.get('stock_age_days', 0)),
                    daily_consumption=float(row.get('daily_consumption', 0.0)),
                    warehouse_location=row.get('warehouse_location', ''),
                    status=row.get('status', 'normal')
                )
                session.add(inventory)
                records_loaded += 1
            
            session.commit()
            logger.info(f"Loaded {records_loaded} inventory records")
            print(f"✅ Loaded {records_loaded} inventory records")
            return records_loaded
        
        except Exception as e:
            session.rollback()
            logger.error(f"Error loading inventory data: {e}")
            raise
        finally:
            session.close()
    
    @staticmethod
    def load_competitor_data(df: pd.DataFrame, session: Session = None) -> int:
        """Load competitor data into the database"""
        if session is None:
            session = SessionLocal()
        
        try:
            records_loaded = 0
            
            for _, row in df.iterrows():
                competitor = models.Competitor(
                    sku=row.get('sku'),
                    product_name=row.get('product_name'),
                    competitor_name=row.get('competitor_name'),
                    competitor_price=float(row.get('competitor_price', 0.0)),
                    our_price=float(row.get('our_price', 0.0)),
                    price_difference=float(row.get('price_difference', 0.0)),
                    availability=row.get('availability', True),
                    rating=float(row.get('rating', 0.0)) if row.get('rating') else 0.0,
                    review_count=int(row.get('review_count', 0)) if row.get('review_count') else 0,
                    date=row.get('date')
                )
                session.add(competitor)
                records_loaded += 1
            
            session.commit()
            logger.info(f"Loaded {records_loaded} competitor records")
            print(f"✅ Loaded {records_loaded} competitor records")
            return records_loaded
        
        except Exception as e:
            session.rollback()
            logger.error(f"Error loading competitor data: {e}")
            raise
        finally:
            session.close()
    
    @staticmethod
    def update_daily_metrics(session: Session = None) -> bool:
        """
        Update aggregated daily metrics
        
        Args:
            session: SQLAlchemy session
            
        Returns:
            Success status
        """
        if session is None:
            session = SessionLocal()
        
        try:
            from sqlalchemy import func
            
            # Get unique dates from sales
            sales_dates = session.query(func.distinct(models.Sale.order_date)).all()
            
            for (sale_date,) in sales_dates:
                if sale_date is None:
                    continue
                
                # Calculate metrics
                daily_sales = session.query(models.Sale).filter(
                    models.Sale.order_date == sale_date
                ).all()
                
                if daily_sales:
                    total_revenue = sum(s.revenue or 0 for s in daily_sales)
                    total_orders = sum(s.units_sold or 0 for s in daily_sales)
                    total_units = len(daily_sales)
                    
                    # Create or update daily metrics
                    metric = session.query(models.DailyMetrics).filter(
                        models.DailyMetrics.date == sale_date
                    ).first()
                    
                    if metric:
                        metric.total_revenue = total_revenue
                        metric.total_orders = total_orders
                        metric.total_units_sold = total_units
                        metric.updated_at = datetime.utcnow()
                    else:
                        metric = models.DailyMetrics(
                            date=sale_date,
                            total_revenue=total_revenue,
                            total_orders=total_orders,
                            total_units_sold=total_units
                        )
                        session.add(metric)
            
            session.commit()
            logger.info("Daily metrics updated successfully")
            return True
        
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating daily metrics: {e}")
            return False
        finally:
            session.close()