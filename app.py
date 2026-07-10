"""
RealNut Intelligence - Main Dashboard Application
AI-powered Business Intelligence Platform for Real Nut Dry Fruits Blinkit Operations
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="RealNut Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.2em;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .alert-box {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .alert-critical {
        background-color: #ffcccc;
        border-left: 4px solid #cc0000;
    }
    .alert-high {
        background-color: #ffe6cc;
        border-left: 4px solid #ff9900;
    }
    .alert-medium {
        background-color: #ffffcc;
        border-left: 4px solid #ffff00;
    }
    .alert-low {
        background-color: #ccffcc;
        border-left: 4px solid #00cc00;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-title">🎯 RealNut Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-Powered Business Intelligence Platform for Blinkit Operations</div>', unsafe_allow_html=True)
    
    # Navigation
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "📍 Navigation",
        [
            "🏠 Executive Dashboard",
            "📈 Sales Intelligence",
            "🗺️ Regional Intelligence",
            "🔑 Keyword Intelligence",
            "🏆 Competition Intelligence",
            "📦 Warehouse Intelligence",
            "🚨 Smart Alerts",
            "🤖 AI Advisor",
            "⚙️ Settings"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    # Try to load data
    try:
        from database.db import SessionLocal
        from analytics.metrics import MetricsEngine
        from analytics.alerts import AlertEngine
        
        session = SessionLocal()
        metrics_engine = MetricsEngine(session)
        alert_engine = AlertEngine(session)
        
        # Get key metrics
        key_metrics = metrics_engine.get_key_metrics(30)
        
        st.sidebar.metric("💰 30-Day Revenue", f"₹{key_metrics['total_revenue']:,.0f}")
        st.sidebar.metric("📦 Units Sold", f"{key_metrics['total_units_sold']:,}")
        st.sidebar.metric("🛍️ Orders", f"{key_metrics['total_orders']:,}")
        st.sidebar.metric("⚠️ Alerts", key_metrics['critical_stock_items'])
        
        session.close()
        
    except Exception as e:
        st.sidebar.warning(f"⚠️ Unable to load metrics: {str(e)}")
    
    st.sidebar.markdown("---")
    
    # Route to pages
    if "Executive Dashboard" in page:
        show_executive_dashboard()
    elif "Sales Intelligence" in page:
        show_sales_intelligence()
    elif "Regional Intelligence" in page:
        show_regional_intelligence()
    elif "Keyword Intelligence" in page:
        show_keyword_intelligence()
    elif "Competition Intelligence" in page:
        show_competition_intelligence()
    elif "Warehouse Intelligence" in page:
        show_warehouse_intelligence()
    elif "Smart Alerts" in page:
        show_smart_alerts()
    elif "AI Advisor" in page:
        show_ai_advisor()
    elif "Settings" in page:
        show_settings()


def show_executive_dashboard():
    """Executive Dashboard Page"""
    st.header("🏢 Executive Dashboard")
    st.markdown("One-page summary of overall business health and key metrics")
    
    try:
        from database.db import SessionLocal
        from analytics.metrics import MetricsEngine
        from analytics.sales import SalesAnalytics
        from analytics.alerts import AlertEngine
        import plotly.graph_objects as go
        import plotly.express as px
        
        session = SessionLocal()
        metrics_engine = MetricsEngine(session)
        sales_analytics = SalesAnalytics(session)
        alert_engine = AlertEngine(session)
        
        # Health Score Card
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            health = metrics_engine.get_health_score()
            score = health['health_score']
            status_color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
            st.metric(
                "Health Score",
                f"{score:.0f}/100",
                help=health['status']
            )
            st.write(f"{status_color} {health['status']}")
        
        with col2:
            key_metrics = metrics_engine.get_key_metrics(30)
            st.metric(
                "30-Day Revenue",
                f"₹{key_metrics['total_revenue']:,.0f}",
                delta="📈" if key_metrics['total_revenue'] > 100000 else "📉"
            )
        
        with col3:
            st.metric(
                "Active Products",
                key_metrics['active_products']
            )
        
        with col4:
            st.metric(
                "Critical Alerts",
                key_metrics['critical_stock_items'],
                delta_color="inverse"
            )
        
        st.markdown("---")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Units Sold (30d)", f"{key_metrics['total_units_sold']:,}")
        
        with col2:
            st.metric("🛍️ Orders (30d)", f"{key_metrics['total_orders']:,}")
        
        with col3:
            st.metric("💵 Avg Order Value", f"₹{key_metrics['avg_order_value']:.0f}")
        
        with col4:
            st.metric("🗺️ Active Regions", key_metrics['active_regions'])
        
        st.markdown("---")
        
        # Growth Analysis
        st.subheader("📊 Growth Analysis")
        growth = sales_analytics.calculate_growth_rate(7, 14)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Last 7 Days Revenue", f"₹{growth['period1_revenue']:,.0f}")
        with col2:
            st.metric("Previous 7 Days Revenue", f"₹{growth['period2_revenue']:,.0f}")
        with col3:
            growth_color = "green" if growth['growth_rate'] > 0 else "red"
            st.metric(
                "Growth Rate",
                growth['growth_percentage'],
                delta_color="normal"
            )
        
        st.markdown("---")
        
        # Active Alerts
        st.subheader("🚨 Active Alerts")
        alerts = alert_engine.get_active_alerts(5)
        
        if alerts:
            for alert in alerts:
                severity = alert.get('priority', 'MEDIUM')
                alert_class = f"alert-{severity.lower()}"
                st.markdown(
                    f"""
                    <div class="alert-box alert-{severity.lower()}">
                    <b>{alert['title']}</b><br/>
                    {alert['message']}<br/>
                    <small>{alert['created_at']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.success("✅ No active alerts")
        
        st.markdown("---")
        
        # Today's Focus
        st.subheader("🎯 Today's Focus")
        today_sales = sales_analytics.get_daily_sales()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Today's Revenue", f"₹{today_sales['total_revenue']:,.0f}")
        with col2:
            st.metric("Today's Orders", today_sales['total_orders'])
        with col3:
            st.metric("Today's Units", today_sales['total_units'])
        
        # Top Products
        st.subheader("⭐ Top 5 Products (by Revenue)")
        top_products = sales_analytics.get_top_products_by_revenue(5, 30)
        
        if top_products:
            df = pd.DataFrame([
                {
                    'Product': p['product_name'],
                    'SKU': p['sku'],
                    'Revenue': f"₹{p['total_revenue']:,.0f}",
                    'Units': p['total_units']
                }
                for p in top_products
            ])
            st.dataframe(df, use_container_width=True)
        
        session.close()
        
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {str(e)}")
        logger.error(f"Dashboard error: {e}")


def show_sales_intelligence():
    """Sales Intelligence Page"""
    st.header("📈 Sales Intelligence")
    st.markdown("Analyze product and sales performance")
    
    st.info("📋 This section provides detailed sales analytics by product, time period, and region.")
    
    try:
        from database.db import SessionLocal
        from analytics.sales import SalesAnalytics
        
        session = SessionLocal()
        sales_analytics = SalesAnalytics(session)
        
        # Top Products
        st.subheader("🏆 Top 10 Products by Revenue (Last 30 Days)")
        top_products = sales_analytics.get_top_products_by_revenue(10, 30)
        
        if top_products:
            df = pd.DataFrame([
                {
                    'Product': p['product_name'],
                    'SKU': p['sku'],
                    'Revenue': f"₹{p['total_revenue']:,.0f}",
                    'Units': p['total_units'],
                    'Orders': p['order_count']
                }
                for p in top_products
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No sales data available")
        
        session.close()
        
    except Exception as e:
        st.error(f"❌ Error loading sales data: {str(e)}")


def show_regional_intelligence():
    """Regional Intelligence Page"""
    st.header("🗺️ Regional Intelligence")
    st.markdown("Understand geographical demand and regional performance")
    
    st.info("📍 Analyze sales performance across different regions and cities.")
    
    try:
        from database.db import SessionLocal
        from analytics.regions import RegionalAnalytics
        
        session = SessionLocal()
        regional_analytics = RegionalAnalytics(session)
        
        # Regional Performance
        st.subheader("🏙️ Regional Performance (Last 30 Days)")
        regions = regional_analytics.get_regional_performance(30)
        
        if regions:
            df = pd.DataFrame([
                {
                    'City': r['city'],
                    'Revenue': f"₹{r['revenue']:,.0f}",
                    'Units': r['units_sold'],
                    'Orders': r['orders'],
                    'Avg Order Value': f"₹{r['avg_order_value']:,.0f}"
                }
                for r in regions
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No regional data available")
        
        session.close()
        
    except Exception as e:
        st.error(f"❌ Error loading regional data: {str(e)}")


def show_keyword_intelligence():
    """Keyword Intelligence Page"""
    st.header("🔑 Keyword Intelligence")
    st.markdown("Improve search visibility and conversions")
    
    st.info("🔍 Keyword tracking and SEO optimization coming soon.")
    st.warning("⏳ Feature under development")


def show_competition_intelligence():
    """Competition Intelligence Page"""
    st.header("🏆 Competition Intelligence")
    st.markdown("Track market competition")
    
    st.info("🎯 Competitor tracking and market position analysis coming soon.")
    st.warning("⏳ Feature under development")


def show_warehouse_intelligence():
    """Warehouse Intelligence Page"""
    st.header("📦 Warehouse Intelligence")
    st.markdown("Optimize inventory management")
    
    st.info("🏭 Inventory analytics and warehouse management coming soon.")
    st.warning("⏳ Feature under development")


def show_smart_alerts():
    """Smart Alerts Page"""
    st.header("🚨 Smart Alerts")
    st.markdown("View and manage business alerts")
    
    try:
        from database.db import SessionLocal
        from analytics.alerts import AlertEngine
        
        session = SessionLocal()
        alert_engine = AlertEngine(session)
        
        st.subheader("📢 Active Alerts")
        alerts = alert_engine.get_active_alerts(50)
        
        if alerts:
            for alert in alerts:
                severity = alert.get('priority', 'MEDIUM')
                st.markdown(
                    f"""
                    <div class="alert-box alert-{severity.lower()}">
                    <b>[{severity}] {alert['title']}</b><br/>
                    {alert['message']}<br/>
                    <small>{alert['created_at']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.success("✅ No active alerts")
        
        session.close()
        
    except Exception as e:
        st.error(f"❌ Error loading alerts: {str(e)}")


def show_ai_advisor():
    """AI Advisor Page"""
    st.header("🤖 AI Business Advisor")
    st.markdown("Get AI-powered business recommendations")
    
    st.info("🧠 AI-powered recommendations coming soon. Powered by OpenAI API.")
    st.warning("⏳ Feature under development")


def show_settings():
    """Settings Page"""
    st.header("⚙️ Settings")
    
    st.subheader("📋 System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Application Name:**")
        st.write("RealNut Intelligence")
        
        st.write("**Version:**")
        st.write("1.0.0")
    
    with col2:
        st.write("**Last Updated:**")
        st.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        st.write("**Database:**")
        st.write("SQLite")
    
    st.markdown("---")
    
    st.subheader("🔄 Data Management")
    
    if st.button("🔄 Refresh Cache"):
        st.success("Cache refreshed successfully")
    
    if st.button("📊 Generate Report"):
        st.info("Report generation coming soon")


if __name__ == "__main__":
    main()
