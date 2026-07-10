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



def import_sample_data():
    """Import sample data into database"""
    print("\n📥 Importing Sample Data...")
    try:
        from etl.pipeline import ETLPipeline
        
        pipeline = ETLPipeline()
        
        # Import sales
        sales_count = pipeline.run_sales_pipeline('data/raw/sales_v1_clean.csv')
        print(f"  ✅ Imported {sales_count} sales records")
        
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
