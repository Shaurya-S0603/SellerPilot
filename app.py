"""
app.py

Main entry point for RealNut Intelligence.
"""

import streamlit as st

from utils.ui import load_theme

from views.home import render as home_page
from views.import_data import render as import_page
from views.sales_dashboard import render as sales_dashboard
from views.regional_dashboard import render as regional_dashboard
from views.alerts import render as alerts_page


# ==========================================================
# Streamlit Configuration
# ==========================================================

st.set_page_config(
    page_title="RealNut Intelligence",
    page_icon="🥜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# Load Global Theme
# ==========================================================

load_theme()

# ==========================================================
# Page Constants
# ==========================================================

HOME = "🏠 Executive Home"
IMPORT = "📤 Import Data"
SALES = "📊 Sales Dashboard"
REGIONAL = "🌍 Regional Analytics"
ALERTS = "🚨 Smart Alerts"

PAGES = {
    HOME: home_page,
    IMPORT: import_page,
    SALES: sales_dashboard,
    REGIONAL: regional_dashboard,
    ALERTS: alerts_page,
}

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.markdown(
        """
# 🥜 RealNut Intelligence

**Blinkit Business Intelligence**
"""
    )

    st.caption("Executive Analytics Platform")

    st.divider()

    page = st.radio(
        "Navigation",
        list(PAGES.keys()),
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        """
### Platform

**Version:** 1.0.0

#### Current Modules

- 📊 Sales Analytics
- 🌍 Regional Analytics

#### Database

SQLite
"""
    )

    st.divider()

    st.caption("© Shaurya Singhal")
    st.caption("Built with Python + Streamlit + SQLite")

# ==========================================================
# Render Selected Page
# ==========================================================

PAGES[page]()