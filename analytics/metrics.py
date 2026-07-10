"""Business Metrics and KPI Calculation Module"""

import logging
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database import models

logger = logging.getLogger(__name__)


class MetricsEngine:
    """Calculates business metrics and KPIs"""
    
    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()
    
    def get_health_score(self, days: int = 30) -> dict:
        """
        Calculate overall business health score (0-100)
        Based on revenue, growth, and product performance
        """
        start_date = datetime.now().date() - timedelta(days=days)
        
        # Revenue metric
        total_revenue = self.session.query(
            func.sum(models.Sale.revenue)
        ).filter(
            models.Sale.order_date >= start_date
        ).scalar() or 0
        
        revenue_score = min(100, (total_revenue / 100000) * 100)  # Normalize to 100K
        
        # Growth metric
        growth_data = self._calculate_growth(days)
        growth_score = min(100, (growth_data['growth_rate'] + 50) * 100 / 100)
        growth_score = max(0, growth_score)  # Ensure non-negative
        
        # Product diversity
        distinct_products = self.session.query(
            func.count(func.distinct(models.Sale.sku))
        ).filter(
            models.Sale.order_date >= start_date
        ).scalar() or 0
        
        diversity_score = min(100, (distinct_products / 100) * 100)
        
        # Overall health score (weighted average)
        health_score = (revenue_score * 0.4 + growth_score * 0.35 + diversity_score * 0.25)
        
        return {
            'health_score': round(health_score, 2),
            'revenue_score': round(revenue_score, 2),
            'growth_score': round(growth_score, 2),
            'diversity_score': round(diversity_score, 2),
            'status': self._get_health_status(health_score)
        }
    
    def get_key_metrics(self, days: int = 30) -> dict:
        """Get key business KPIs"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        # Revenue
        total_revenue = self.session.query(
            func.sum(models.Sale.revenue)
        ).filter(
            models.Sale.order_date >= start_date
        ).scalar() or 0
        
        # Units sold
        total_units = self.session.query(
            func.sum(models.Sale.units_sold)
        ).filter(
            models.Sale.order_date >= start_date
        ).scalar() or 0
        
        # Orders
        total_orders = self.session.query(
            func.count(models.Sale.id)
        ).filter(
            models.Sale.order_date >= start_date
        ).scalar() or 0
        
        # Average order value
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Active products
        active_products = self.session.query(
            func.count(func.distinct(models.Sale.sku))
        ).filter(
            models.Sale.order_date >= start_date
        ).scalar() or 0
        
        # Active regions
        active_regions = self.session.query(
            func.count(func.distinct(models.Sale.city))
        ).filter(
            models.Sale.order_date >= start_date
        ).scalar() or 0
        
        # Inventory metrics
        inventory_items = self.session.query(
            func.count(func.distinct(models.Inventory.sku))
        ).scalar() or 0
        
        critical_stock = self.session.query(
            func.count(models.Inventory.id)
        ).filter(
            models.Inventory.status == 'critical'
        ).scalar() or 0
        
        return {
            'total_revenue': round(total_revenue, 2),
            'total_units_sold': total_units,
            'total_orders': total_orders,
            'avg_order_value': round(avg_order_value, 2),
            'active_products': active_products,
            'active_regions': active_regions,
            'inventory_items': inventory_items,
            'critical_stock_items': critical_stock,
            'period_days': days
        }
    
    def get_product_health(self, limit: int = 20) -> list:
        """Get health status of top products"""
        results = self.session.query(
            models.Sale.sku,
            models.Sale.product_name,
            func.sum(models.Sale.revenue).label('revenue'),
            func.sum(models.Sale.units_sold).label('units'),
            func.count().label('orders')
        ).group_by(
            models.Sale.sku,
            models.Sale.product_name
        ).order_by(
            func.sum(models.Sale.revenue).desc()
        ).limit(limit).all()
        
        products = []
        for r in results:
            # Get inventory status
            inventory = self.session.query(models.Inventory).filter(
                models.Inventory.sku == r[0]
            ).order_by(models.Inventory.date.desc()).first()
            
            status = inventory.status if inventory else 'unknown'
            
            products.append({
                'sku': r[0],
                'name': r[1],
                'revenue': r[2],
                'units_sold': r[3],
                'orders': r[4],
                'inventory_status': status,
                'health': self._calculate_product_health(r[2], status)
            })
        
        return products
    
    def get_inventory_metrics(self) -> dict:
        """Get overall inventory metrics"""
        inventory = self.session.query(models.Inventory).all()
        
        if not inventory:
            return {
                'total_items': 0,
                'normal': 0,
                'overstock': 0,
                'understock': 0,
                'critical': 0
            }
        
        status_counts = {
            'normal': sum(1 for i in inventory if i.status == 'normal'),
            'overstock': sum(1 for i in inventory if i.status == 'overstock'),
            'understock': sum(1 for i in inventory if i.status == 'understock'),
            'critical': sum(1 for i in inventory if i.status == 'critical')
        }
        
        return {
            'total_items': len(inventory),
            'normal': status_counts['normal'],
            'overstock': status_counts['overstock'],
            'understock': status_counts['understock'],
            'critical': status_counts['critical'],
            'critical_percentage': (status_counts['critical'] / len(inventory) * 100) if inventory else 0
        }
    
    def get_competitor_metrics(self, days: int = 30) -> dict:
        """Get competitor-related metrics"""
        start_date = datetime.now().date() - timedelta(days=days)
        
        # Price comparison
        competitors = self.session.query(models.Competitor).filter(
            models.Competitor.date >= start_date
        ).all()
        
        if not competitors:
            return {
                'total_competitors_tracked': 0,
                'avg_price_difference': 0,
                'cheaper_count': 0,
                'expensive_count': 0,
                'price_parity_count': 0
            }
        
        cheaper = sum(1 for c in competitors if c.price_difference < 0)
        expensive = sum(1 for c in competitors if c.price_difference > 0)
        parity = sum(1 for c in competitors if c.price_difference == 0)
        
        avg_difference = sum(c.price_difference for c in competitors) / len(competitors) if competitors else 0
        
        return {
            'total_competitors_tracked': len(set(c.competitor_name for c in competitors)),
            'avg_price_difference': round(avg_difference, 2),
            'cheaper_count': cheaper,
            'expensive_count': expensive,
            'price_parity_count': parity,
            'our_products_more_expensive': (expensive / len(competitors) * 100) if competitors else 0
        }
    
    def _calculate_growth(self, days: int) -> dict:
        """Internal method to calculate growth rate"""
        end_date = datetime.now().date()
        mid_date = end_date - timedelta(days=days//2)
        start_date = end_date - timedelta(days=days)
        
        period1_revenue = self.session.query(
            func.sum(models.Sale.revenue)
        ).filter(
            models.Sale.order_date >= mid_date,
            models.Sale.order_date <= end_date
        ).scalar() or 0
        
        period2_revenue = self.session.query(
            func.sum(models.Sale.revenue)
        ).filter(
            models.Sale.order_date >= start_date,
            models.Sale.order_date < mid_date
        ).scalar() or 0
        
        if period2_revenue == 0:
            growth_rate = 0
        else:
            growth_rate = ((period1_revenue - period2_revenue) / period2_revenue) * 100
        
        return {'growth_rate': growth_rate}
    
    def _get_health_status(self, score: float) -> str:
        """Determine health status based on score"""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Fair'
        elif score >= 20:
            return 'Poor'
        else:
            return 'Critical'
    
    def _calculate_product_health(self, revenue: float, inventory_status: str) -> str:
        """Calculate health of a product"""
        if inventory_status == 'critical':
            return 'At Risk'
        elif revenue < 1000:
            return 'Underperforming'
        elif inventory_status == 'overstock':
            return 'Overstock Alert'
        else:
            return 'Healthy'
    
    def close(self):
        """Close database session"""
        if self.session:
            self.session.close()
