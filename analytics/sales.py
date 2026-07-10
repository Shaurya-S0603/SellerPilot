"""Sales Analytics Module
Handles all sales-related analytics and metrics
"""

import logging
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database import models

logger = logging.getLogger(__name__)


class SalesAnalytics:
    """Sales performance and analytics"""
    
    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()
    
    def get_daily_sales(self, date: datetime.date = None):
        """Get sales data for a specific date"""
        if date is None:
            date = datetime.now().date()
        
        sales = self.session.query(models.Sale).filter(
            models.Sale.order_date == date
        ).all()
        
        return {
            'date': date,
            'total_revenue': sum(s.revenue or 0 for s in sales),
            'total_orders': len(sales),
            'total_units': sum(s.units_sold or 0 for s in sales),
            'avg_order_value': sum(s.revenue or 0 for s in sales) / len(sales) if sales else 0
        }
    
    def get_weekly_sales(self, end_date: datetime.date = None):
        """Get sales data for the last 7 days"""
        if end_date is None:
            end_date = datetime.now().date()
        
        start_date = end_date - timedelta(days=7)
        
        sales = self.session.query(models.Sale).filter(
            models.Sale.order_date >= start_date,
            models.Sale.order_date <= end_date
        ).all()
        
        if not sales:
            return {
                'period': f"{start_date} to {end_date}",
                'total_revenue': 0,
                'total_orders': 0,
                'total_units': 0,
                'avg_daily_revenue': 0
            }
        
        return {
            'period': f"{start_date} to {end_date}",
            'total_revenue': sum(s.revenue or 0 for s in sales),
            'total_orders': len(sales),
            'total_units': sum(s.units_sold or 0 for s in sales),
            'avg_daily_revenue': sum(s.revenue or 0 for s in sales) / 7
        }
    
    def get_monthly_sales(self, year: int = None, month: int = None):
        """Get sales data for a specific month"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        sales = self.session.query(models.Sale).filter(
            func.extract('year', models.Sale.order_date) == year,
            func.extract('month', models.Sale.order_date) == month
        ).all()
        
        if not sales:
            return {
                'period': f"{year}-{month:02d}",
                'total_revenue': 0,
                'total_orders': 0,
                'total_units': 0,
                'avg_daily_revenue': 0
            }
        
        return {
            'period': f"{year}-{month:02d}",
            'total_revenue': sum(s.revenue or 0 for s in sales),
            'total_orders': len(sales),
            'total_units': sum(s.units_sold or 0 for s in sales),
            'avg_daily_revenue': sum(s.revenue or 0 for s in sales) / 30
        }
    
    def get_top_products_by_revenue(self, limit: int = 10, days: int = 30):
        """Get top performing products by revenue"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        results = self.session.query(
            models.Sale.sku,
            models.Sale.product_name,
            func.sum(models.Sale.revenue).label('total_revenue'),
            func.sum(models.Sale.units_sold).label('total_units'),
            func.count().label('order_count')
        ).filter(
            models.Sale.order_date >= start_date
        ).group_by(
            models.Sale.sku,
            models.Sale.product_name
        ).order_by(
            func.sum(models.Sale.revenue).desc()
        ).limit(limit).all()
        
        return [
            {
                'sku': r[0],
                'product_name': r[1],
                'total_revenue': r[2],
                'total_units': r[3],
                'order_count': r[4]
            }
            for r in results
        ]
    
    def get_top_products_by_units(self, limit: int = 10, days: int = 30):
        """Get top performing products by units sold"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        results = self.session.query(
            models.Sale.sku,
            models.Sale.product_name,
            func.sum(models.Sale.units_sold).label('total_units'),
            func.sum(models.Sale.revenue).label('total_revenue'),
            func.count().label('order_count')
        ).filter(
            models.Sale.order_date >= start_date
        ).group_by(
            models.Sale.sku,
            models.Sale.product_name
        ).order_by(
            func.sum(models.Sale.units_sold).desc()
        ).limit(limit).all()
        
        return [
            {
                'sku': r[0],
                'product_name': r[1],
                'total_units': r[2],
                'total_revenue': r[3],
                'order_count': r[4]
            }
            for r in results
        ]
    
    def get_regional_sales(self, days: int = 30):
        """Get sales breakdown by region"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        results = self.session.query(
            models.Sale.city,
            func.sum(models.Sale.revenue).label('total_revenue'),
            func.sum(models.Sale.units_sold).label('total_units'),
            func.count().label('order_count')
        ).filter(
            models.Sale.order_date >= start_date
        ).group_by(
            models.Sale.city
        ).order_by(
            func.sum(models.Sale.revenue).desc()
        ).all()
        
        return [
            {
                'city': r[0],
                'total_revenue': r[1],
                'total_units': r[2],
                'order_count': r[3]
            }
            for r in results
        ]
    
    def get_sales_trend(self, days: int = 30):
        """Get daily sales trend for the last N days"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        results = self.session.query(
            models.Sale.order_date,
            func.sum(models.Sale.revenue).label('daily_revenue'),
            func.sum(models.Sale.units_sold).label('daily_units'),
            func.count().label('orders')
        ).filter(
            models.Sale.order_date >= start_date
        ).group_by(
            models.Sale.order_date
        ).order_by(
            models.Sale.order_date
        ).all()
        
        return [
            {
                'date': r[0],
                'revenue': r[1],
                'units': r[2],
                'orders': r[3]
            }
            for r in results
        ]
    
    def calculate_growth_rate(self, period1_days: int = 7, period2_days: int = 14):
        """Calculate growth rate between two periods"""
        end_date = datetime.now().date()
        
        # Period 1 (recent)
        period1_start = end_date - timedelta(days=period1_days)
        period1_sales = self.session.query(
            func.sum(models.Sale.revenue)
        ).filter(
            models.Sale.order_date >= period1_start,
            models.Sale.order_date <= end_date
        ).scalar() or 0
        
        # Period 2 (older)
        period2_start = end_date - timedelta(days=period2_days)
        period2_end = end_date - timedelta(days=period1_days)
        period2_sales = self.session.query(
            func.sum(models.Sale.revenue)
        ).filter(
            models.Sale.order_date >= period2_start,
            models.Sale.order_date <= period2_end
        ).scalar() or 0
        
        if period2_sales == 0:
            growth_rate = 0
        else:
            growth_rate = ((period1_sales - period2_sales) / period2_sales) * 100
        
        return {
            'period1_revenue': period1_sales,
            'period2_revenue': period2_sales,
            'growth_rate': growth_rate,
            'growth_percentage': f"{growth_rate:.2f}%"
        }
    
    def close(self):
        """Close database session"""
        if self.session:
            self.session.close()
