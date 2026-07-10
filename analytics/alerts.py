"""Smart Alert Engine
Generates intelligent business alerts based on data patterns
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database import models

logger = logging.getLogger(__name__)


class AlertEngine:
    """Generates smart alerts for business events"""
    
    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()
    
    def generate_all_alerts(self) -> list:
        """Generate all types of alerts"""
        alerts = []
        
        alerts.extend(self._detect_sales_drop())
        alerts.extend(self._detect_sales_growth())
        alerts.extend(self._detect_inventory_risk())
        alerts.extend(self._detect_competitor_price_change())
        alerts.extend(self._detect_slow_moving_products())
        
        return alerts
    
    def _detect_sales_drop(self, threshold: float = 0.2) -> list:
        """Detect significant sales drops"""
        alerts = []
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        last_week_avg_date = today - timedelta(days=8)
        
        # Get today's sales
        today_sales = self.session.query(
            func.sum(models.Sale.revenue)
        ).filter(
            models.Sale.order_date == today
        ).scalar() or 0
        
        # Get last 7 days average
        week_sales = self.session.query(
            func.sum(models.Sale.revenue)
        ).filter(
            models.Sale.order_date >= last_week_avg_date,
            models.Sale.order_date < today
        ).scalar() or 0
        
        week_avg = week_sales / 7 if week_sales > 0 else 0
        
        # Check for drop
        if week_avg > 0 and today_sales < week_avg * (1 - threshold):
            drop_percentage = ((week_avg - today_sales) / week_avg) * 100
            alerts.append({
                'type': 'SALES_DROP',
                'severity': 'HIGH' if drop_percentage > 30 else 'MEDIUM',
                'title': 'Sales Drop Detected',
                'message': f"Today's sales dropped by {drop_percentage:.1f}% compared to 7-day average",
                'value': today_sales,
                'threshold': week_avg,
                'timestamp': datetime.utcnow()
            })
        
        return alerts
    
    def _detect_sales_growth(self, threshold: float = 0.2) -> list:
        """Detect significant sales growth"""
        alerts = []
        today = datetime.now().date()
        last_week_avg_date = today - timedelta(days=8)
        
        # Get today's sales
        today_sales = self.session.query(
            func.sum(models.Sale.revenue)
        ).filter(
            models.Sale.order_date == today
        ).scalar() or 0
        
        # Get last 7 days average
        week_sales = self.session.query(
            func.sum(models.Sale.revenue)
        ).filter(
            models.Sale.order_date >= last_week_avg_date,
            models.Sale.order_date < today
        ).scalar() or 0
        
        week_avg = week_sales / 7 if week_sales > 0 else 0
        
        # Check for growth
        if week_avg > 0 and today_sales > week_avg * (1 + threshold):
            growth_percentage = ((today_sales - week_avg) / week_avg) * 100
            alerts.append({
                'type': 'SALES_GROWTH',
                'severity': 'LOW',
                'title': 'Sales Growth Detected',
                'message': f"Today's sales grew by {growth_percentage:.1f}% compared to 7-day average",
                'value': today_sales,
                'threshold': week_avg,
                'timestamp': datetime.utcnow()
            })
        
        return alerts
    
    def _detect_inventory_risk(self) -> list:
        """Detect inventory risks"""
        alerts = []
        
        # Critical stock items
        critical_items = self.session.query(models.Inventory).filter(
            models.Inventory.status == 'critical'
        ).all()
        
        for item in critical_items:
            alerts.append({
                'type': 'INVENTORY_CRITICAL',
                'severity': 'CRITICAL',
                'title': 'Critical Inventory Alert',
                'message': f"Product {item.product_name} (SKU: {item.sku}) is out of stock",
                'sku': item.sku,
                'product': item.product_name,
                'stock': item.stock_quantity,
                'timestamp': datetime.utcnow()
            })
        
        # Understock items
        understock_items = self.session.query(models.Inventory).filter(
            models.Inventory.status == 'understock'
        ).all()
        
        for item in understock_items[:5]:  # Limit to top 5
            alerts.append({
                'type': 'INVENTORY_UNDERSTOCK',
                'severity': 'HIGH',
                'title': 'Low Stock Alert',
                'message': f"Product {item.product_name} (SKU: {item.sku}) has low inventory",
                'sku': item.sku,
                'product': item.product_name,
                'stock': item.stock_quantity,
                'timestamp': datetime.utcnow()
            })
        
        # Overstock items
        overstock_items = self.session.query(models.Inventory).filter(
            models.Inventory.status == 'overstock'
        ).all()
        
        for item in overstock_items[:3]:  # Limit to top 3
            alerts.append({
                'type': 'INVENTORY_OVERSTOCK',
                'severity': 'MEDIUM',
                'title': 'Overstock Alert',
                'message': f"Product {item.product_name} (SKU: {item.sku}) is overstocked",
                'sku': item.sku,
                'product': item.product_name,
                'stock': item.stock_quantity,
                'timestamp': datetime.utcnow()
            })
        
        return alerts
    
    def _detect_competitor_price_change(self, threshold: float = 0.05) -> list:
        """Detect competitor price changes"""
        alerts = []
        
        competitors = self.session.query(models.Competitor).filter(
            models.Competitor.date >= datetime.now().date() - timedelta(days=1)
        ).all()
        
        for comp in competitors:
            if comp.price_difference and comp.price_difference < 0:
                if abs(comp.price_difference) > (comp.our_price * threshold) if comp.our_price > 0 else False:
                    alerts.append({
                        'type': 'COMPETITOR_PRICE_DROP',
                        'severity': 'MEDIUM',
                        'title': 'Competitor Price Drop',
                        'message': f"{comp.competitor_name} dropped price for {comp.product_name}",
                        'product': comp.product_name,
                        'our_price': comp.our_price,
                        'competitor_price': comp.competitor_price,
                        'difference': comp.price_difference,
                        'timestamp': datetime.utcnow()
                    })
        
        return alerts
    
    def _detect_slow_moving_products(self) -> list:
        """Detect slow-moving products"""
        alerts = []
        
        last_30_days = datetime.now().date() - timedelta(days=30)
        
        # Get products with very low sales in last 30 days
        slow_products = self.session.query(
            models.Sale.sku,
            models.Sale.product_name,
            func.sum(models.Sale.units_sold).label('units'),
            func.sum(models.Sale.revenue).label('revenue')
        ).filter(
            models.Sale.order_date >= last_30_days
        ).group_by(
            models.Sale.sku,
            models.Sale.product_name
        ).having(
            func.sum(models.Sale.revenue) < 500  # Less than 500 revenue
        ).all()
        
        for product in slow_products[:5]:  # Limit to top 5
            alerts.append({
                'type': 'SLOW_MOVING_PRODUCT',
                'severity': 'LOW',
                'title': 'Slow-Moving Product',
                'message': f"Product {product.product_name} has low sales",
                'sku': product.sku,
                'product': product.product_name,
                'revenue_30d': product.revenue or 0,
                'units_30d': product.units or 0,
                'timestamp': datetime.utcnow()
            })
        
        return alerts
    
    def save_alert(self, alert_data: dict) -> bool:
        """Save alert to database"""
        try:
            alert = models.Alert(
                priority=alert_data.get('severity', 'MEDIUM'),
                title=alert_data.get('title', 'Alert'),
                message=alert_data.get('message', ''),
                resolved=False
            )
            self.session.add(alert)
            self.session.commit()
            logger.info(f"Alert saved: {alert_data.get('title')}")
            return True
        except Exception as e:
            logger.error(f"Error saving alert: {e}")
            self.session.rollback()
            return False
    
    def get_active_alerts(self, limit: int = 10) -> list:
        """Get active alerts"""
        alerts = self.session.query(models.Alert).filter(
            models.Alert.resolved == False
        ).order_by(
            models.Alert.created_at.desc()
        ).limit(limit).all()
        
        return [
            {
                'id': a.id,
                'priority': a.priority,
                'title': a.title,
                'message': a.message,
                'created_at': a.created_at
            }
            for a in alerts
        ]
    
    def close(self):
        """Close database session"""
        if self.session:
            self.session.close()
