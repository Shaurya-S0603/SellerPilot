from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    String,
)

from database.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(100))
    category = Column(String(100))
    mrp = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Product {self.product_name}>"



class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date, index=True)
    sku = Column(String(100), index=True)
    product_name = Column(String(255))
    city = Column(String(100), index=True)
    darkstore = Column(String(150))
    warehouse = Column(String(150))
    units_sold = Column(Integer)
    revenue = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Sale {self.product_name} - ₹{self.revenue}>"



class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True)
    warehouse = Column(String(150))
    darkstore = Column(String(150))
    availability = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Location {self.city}>"



class ImportHistory(Base):
    __tablename__ = "imports"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    report_type = Column(String(100))
    rows_imported = Column(Integer)
    status = Column(String(50))
    imported_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Import {self.filename}>"



class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    priority = Column(String(20))
    title = Column(String(255))
    message = Column(String(500))
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Alert {self.priority}: {self.title}>"


class Inventory(Base):
    """Warehouse inventory tracking"""
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), index=True)
    product_name = Column(String(255))
    date = Column(Date, index=True)
    stock_quantity = Column(Integer, default=0)
    stock_age_days = Column(Integer, default=0)
    daily_consumption = Column(Float, default=0.0)
    warehouse_location = Column(String(100))
    status = Column(String(50), default='normal')  # normal, overstock, understock, critical
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Inventory {self.sku}: {self.stock_quantity} units>"


class Competitor(Base):
    """Competitor price and availability tracking"""
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), index=True)
    product_name = Column(String(255))
    competitor_name = Column(String(100), nullable=False)
    competitor_price = Column(Float)
    our_price = Column(Float)
    price_difference = Column(Float)
    availability = Column(Boolean, default=True)
    rating = Column(Float)
    review_count = Column(Integer)
    date = Column(Date, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Competitor {self.competitor_name} for {self.sku}>"


class Keyword(Base):
    """Keyword performance tracking"""
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), index=True)
    product_name = Column(String(255))
    keyword = Column(String(255), nullable=False)
    ranking = Column(Integer)
    search_volume = Column(Integer, default=0)
    click_through_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    date = Column(Date, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Keyword {self.keyword}>"


class DailyMetrics(Base):
    """Aggregated daily business metrics"""
    __tablename__ = "daily_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True, nullable=False)
    total_revenue = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    total_units_sold = Column(Integer, default=0)
    avg_order_value = Column(Float, default=0.0)
    total_products = Column(Integer, default=0)
    active_products = Column(Integer, default=0)
    total_alerts = Column(Integer, default=0)
    critical_alerts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<DailyMetrics {self.date}: ₹{self.total_revenue}>"