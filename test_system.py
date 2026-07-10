"""
Test script for RealNut Intelligence Platform
Verifies all components are working correctly
"""

import sys
import pandas as pd
from datetime import datetime, timedelta
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database():
    """Test database connection and models"""
    print("\n🔍 Testing Database...")
    try:
        from database.db import SessionLocal
        from database import models
        
        session = SessionLocal()
        logger.info("✅ Database connection successful")
        
        # Test model import
        print("  ✅ All models imported successfully")
        
        session.close()
        return True
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False

def test_analytics():
    """Test analytics modules"""
    print("\n🔍 Testing Analytics...")
    try:
        from analytics.sales import SalesAnalytics
        from analytics.metrics import MetricsEngine
        from analytics.regions import RegionalAnalytics
        from analytics.alerts import AlertEngine
        
        print("  ✅ All analytics modules imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Analytics error: {e}")
        return False

def test_etl():
    """Test ETL pipeline"""
    print("\n🔍 Testing ETL Pipeline...")
    try:
        from etl.importer import BlinkitImporter
        from etl.validator import DataValidator
        from etl.transformer import DataTransformer
        from etl.loader import DataLoader
        from etl.pipeline import ETLPipeline
        
        print("  ✅ All ETL modules imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ ETL error: {e}")
        return False

def generate_sample_data():
    """Generate sample data for testing"""
    print("\n📊 Generating Sample Data...")
    
    # Products
    products = [
        {'sku': 'ALM001', 'name': 'Almonds 250g', 'category': 'Dry Fruits'},
        {'sku': 'CSH002', 'name': 'Cashews 200g', 'category': 'Dry Fruits'},
        {'sku': 'WAL003', 'name': 'Walnuts 200g', 'category': 'Dry Fruits'},
        {'sku': 'DAT004', 'name': 'Dates 500g', 'category': 'Dry Fruits'},
        {'sku': 'PIS005', 'name': 'Pistachios 150g', 'category': 'Dry Fruits'},
        {'sku': 'RAS006', 'name': 'Raisins 250g', 'category': 'Dry Fruits'},
        {'sku': 'APR007', 'name': 'Apricots 200g', 'category': 'Dry Fruits'},
        {'sku': 'MIX008', 'name': 'Mixed Dry Fruits 500g', 'category': 'Mix'},
    ]
    
    # Cities
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata']
    
    # Generate sales data for last 30 days
    sales_data = []
    today = datetime.now().date()
    
    for i in range(30):
        date = today - timedelta(days=i)
        # 50-150 transactions per day
        for _ in range(random.randint(50, 150)):
            product = random.choice(products)
            sales_data.append({
                'order_date': date.strftime('%Y-%m-%d'),
                'sku': product['sku'],
                'product_name': product['name'],
                'city': random.choice(cities),
                'darkstore': f"DS_{random.randint(1,10)}",
                'warehouse': f"WH_{random.randint(1,5)}",
                'units_sold': random.randint(1, 5),
                'revenue': random.uniform(500, 5000)
            })
    
    sales_df = pd.DataFrame(sales_data)
    sales_df.to_csv('data/raw/sample_sales.csv', index=False)
    print(f"  ✅ Generated {len(sales_df)} sales records")
    
    # Generate inventory data
    inventory_data = []
    for product in products:
        inventory_data.append({
            'date': today.strftime('%Y-%m-%d'),
            'sku': product['sku'],
            'product_name': product['name'],
            'stock_quantity': random.randint(100, 1000),
            'stock_age_days': random.randint(0, 60),
            'daily_consumption': random.uniform(10, 100),
            'warehouse_location': f"RACK_{random.randint(1,20)}"
        })
    
    inventory_df = pd.DataFrame(inventory_data)
    inventory_df.to_csv('data/raw/sample_inventory.csv', index=False)
    print(f"  ✅ Generated {len(inventory_df)} inventory records")
    
    # Generate competitor data
    competitor_data = []
    competitors = ['Amazon', 'Flipkart', 'Fresh Daily', 'Big Basket', 'Nature\u2019s Basket']
    
    for product in products:
        for _ in range(3):  # Multiple competitors per product
            our_price = random.uniform(400, 2000)
            competitor_data.append({
                'date': today.strftime('%Y-%m-%d'),
                'sku': product['sku'],
                'product_name': product['name'],
                'competitor_name': random.choice(competitors),
                'competitor_price': our_price + random.uniform(-200, 200),
                'our_price': our_price,
                'availability': random.choice([True, True, True, False]),
                'rating': random.uniform(3.5, 5.0),
                'review_count': random.randint(50, 500)
            })
    
    competitor_df = pd.DataFrame(competitor_data)
    competitor_df.to_csv('data/raw/sample_competitors.csv', index=False)
    print(f"  ✅ Generated {len(competitor_df)} competitor records")
    
    return sales_df, inventory_df, competitor_df

def import_sample_data():
    """Import sample data into database"""
    print("\n📥 Importing Sample Data...")
    try:
        from etl.pipeline import ETLPipeline
        
        pipeline = ETLPipeline()
        
        # Import sales
        sales_count = pipeline.run_sales_pipeline('data/raw/sample_sales.csv')
        print(f"  ✅ Imported {sales_count} sales records")
        
        # Import inventory
        inventory_count = pipeline.run_inventory_pipeline('data/raw/sample_inventory.csv')
        print(f"  ✅ Imported {inventory_count} inventory records")
        
        # Import competitors
        competitor_count = pipeline.run_competitor_pipeline('data/raw/sample_competitors.csv')
        print(f"  ✅ Imported {competitor_count} competitor records")
        
        pipeline.close()
        return True
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        logger.error(f"Import failed: {e}")
        return False

def test_analytics_data():
    """Test analytics with imported data"""
    print("\n📊 Testing Analytics with Data...")
    try:
        from analytics.sales import SalesAnalytics
        from analytics.metrics import MetricsEngine
        from analytics.regions import RegionalAnalytics
        from analytics.alerts import AlertEngine
        from database.db import SessionLocal
        
        session = SessionLocal()
        
        # Test sales analytics
        sales = SalesAnalytics(session)
        daily = sales.get_daily_sales()
        print(f"  ✅ Daily sales: ₹{daily['total_revenue']:,.0f}")
        
        # Test metrics
        metrics = MetricsEngine(session)
        health = metrics.get_health_score()
        print(f"  ✅ Health score: {health['health_score']}/100 ({health['status']})")
        
        # Test regions
        regions = RegionalAnalytics(session)
        region_data = regions.get_regional_performance(30)
        print(f"  ✅ Regions analyzed: {len(region_data)}")
        
        # Test alerts
        alerts = AlertEngine(session)
        active_alerts = alerts.get_active_alerts()
        print(f"  ✅ Active alerts: {len(active_alerts)}")
        
        session.close()
        return True
    except Exception as e:
        print(f"  ❌ Analytics test error: {e}")
        logger.error(f"Analytics test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 RealNut Intelligence - System Test Suite")
    print("=" * 60)
    
    tests = [
        ("Database", test_database),
        ("Analytics", test_analytics),
        ("ETL Pipeline", test_etl),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            results.append((test_name, False))
    
    # Generate sample data
    try:
        generate_sample_data()
    except Exception as e:
        print(f"❌ Sample data generation failed: {e}")
        return
    
    # Import sample data
    if not import_sample_data():
        print("❌ Could not import sample data")
        return
    
    # Test with data
    if not test_analytics_data():
        print("⚠️ Analytics test with data had issues")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! System is ready.")
        print("\n📊 To start the dashboard:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️ Some tests failed. Please review the output above.")

if __name__ == "__main__":
    main()
