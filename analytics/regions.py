"""Regional Analytics Module
Handles geographical sales and performance metrics
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database import models

logger = logging.getLogger(__name__)


class RegionalAnalytics:
    """Regional sales and performance analytics"""
    
    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()
    
    def get_regional_performance(self, days: int = 30) -> list:
        """Get performance metrics by region"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        results = self.session.query(
            models.Sale.city,
            func.sum(models.Sale.revenue).label('total_revenue'),
            func.sum(models.Sale.units_sold).label('total_units'),
            func.count(models.Sale.id).label('orders'),
            func.count(func.distinct(models.Sale.sku)).label('unique_products')
        ).filter(
            models.Sale.order_date >= start_date
        ).group_by(
            models.Sale.city
        ).order_by(
            func.sum(models.Sale.revenue).desc()
        ).all()
        
        regions = []
        for r in results:
            regions.append({
                'city': r[0],
                'revenue': round(r[1], 2) if r[1] else 0,
                'units_sold': r[2] or 0,
                'orders': r[3] or 0,
                'unique_products': r[4] or 0,
                'avg_order_value': round(r[1] / r[3], 2) if r[3] else 0,
                'revenue_per_unit': round(r[1] / r[2], 2) if r[2] else 0
            })
        
        return regions
    
    def get_top_regions(self, limit: int = 10, days: int = 30) -> list:
        """Get top performing regions"""
        results = self.get_regional_performance(days)
        return results[:limit]
    
    def get_regional_growth(self, days: int = 30) -> list:
        """Get growth rate for each region"""
        regions = self.get_regional_performance(days)
        
        end_date = datetime.now().date()
        mid_date = end_date - timedelta(days=days//2)
        start_date = end_date - timedelta(days=days)
        
        growth_data = []
        
        for region in regions:
            city = region['city']
            
            # Period 1 (recent)
            period1 = self.session.query(
                func.sum(models.Sale.revenue)
            ).filter(
                models.Sale.city == city,
                models.Sale.order_date >= mid_date,
                models.Sale.order_date <= end_date
            ).scalar() or 0
            
            # Period 2 (older)
            period2 = self.session.query(
                func.sum(models.Sale.revenue)
            ).filter(
                models.Sale.city == city,
                models.Sale.order_date >= start_date,
                models.Sale.order_date < mid_date
            ).scalar() or 0
            
            if period2 == 0:
                growth_rate = 0
            else:
                growth_rate = ((period1 - period2) / period2) * 100
            
            growth_data.append({
                'city': city,
                'period1_revenue': period1,
                'period2_revenue': period2,
                'growth_rate': round(growth_rate, 2),
                'status': 'Growing' if growth_rate > 0 else ('Declining' if growth_rate < 0 else 'Stable')
            })
        
        return sorted(growth_data, key=lambda x: x['growth_rate'], reverse=True)
    
    def get_regional_product_mix(self, city: str, limit: int = 10, days: int = 30) -> list:
        """Get product mix for a specific region"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        results = self.session.query(
            models.Sale.sku,
            models.Sale.product_name,
            func.sum(models.Sale.revenue).label('revenue'),
            func.sum(models.Sale.units_sold).label('units'),
            func.count(models.Sale.id).label('orders')
        ).filter(
            models.Sale.city == city,
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
                'product': r[1],
                'revenue': round(r[2], 2) if r[2] else 0,
                'units': r[3] or 0,
                'orders': r[4] or 0
            }
            for r in results
        ]
    
    def get_regional_comparison(self, city1: str, city2: str, days: int = 30) -> dict:
        """Compare performance between two regions"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        # City 1 metrics
        city1_data = self.session.query(
            func.sum(models.Sale.revenue).label('revenue'),
            func.sum(models.Sale.units_sold).label('units'),
            func.count(models.Sale.id).label('orders')
        ).filter(
            models.Sale.city == city1,
            models.Sale.order_date >= start_date
        ).first()
        
        # City 2 metrics
        city2_data = self.session.query(
            func.sum(models.Sale.revenue).label('revenue'),
            func.sum(models.Sale.units_sold).label('units'),
            func.count(models.Sale.id).label('orders')
        ).filter(
            models.Sale.city == city2,
            models.Sale.order_date >= start_date
        ).first()
        
        return {
            'city1': {
                'name': city1,
                'revenue': city1_data[0] or 0,
                'units': city1_data[1] or 0,
                'orders': city1_data[2] or 0
            },
            'city2': {
                'name': city2,
                'revenue': city2_data[0] or 0,
                'units': city2_data[1] or 0,
                'orders': city2_data[2] or 0
            },
            'winner': self._compare_cities(city1_data, city2_data)
        }
    
    def get_warehouse_performance(self, days: int = 30) -> list:
        """Get performance metrics by warehouse"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        results = self.session.query(
            models.Sale.warehouse,
            func.sum(models.Sale.revenue).label('revenue'),
            func.sum(models.Sale.units_sold).label('units'),
            func.count(models.Sale.id).label('orders')
        ).filter(
            models.Sale.order_date >= start_date
        ).group_by(
            models.Sale.warehouse
        ).order_by(
            func.sum(models.Sale.revenue).desc()
        ).all()
        
        return [
            {
                'warehouse': r[0] or 'Unknown',
                'revenue': round(r[1], 2) if r[1] else 0,
                'units': r[2] or 0,
                'orders': r[3] or 0
            }
            for r in results if r[0]  # Filter out empty warehouse
        ]
    
    def _compare_cities(self, city1_data: tuple, city2_data: tuple) -> str:
        """Compare two cities and return winner"""
        if city1_data is None or city1_data[0] is None:
            return city2_data
        if city2_data is None or city2_data[0] is None:
            return city1_data
        
        city1_revenue = city1_data[0] or 0
        city2_revenue = city2_data[0] or 0
        
        if city1_revenue > city2_revenue:
            return f"City 1 ({city1_revenue})"
        elif city2_revenue > city1_revenue:
            return f"City 2 ({city2_revenue})"
        else:
            return "Tie"
    
    def close(self):
        """Close database session"""
        if self.session:
            self.session.close()
