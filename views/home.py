"""
views/home.py

Executive Home Dashboard
"""

import streamlit as st
import plotly.express as px
from utils.table import premium_table
from utils.formatters import inr
from services.dashboard_service import DashboardService

from utils.ui import (
    load_theme,
    page_header,
    metric_card,
    section_header,
    status_badge,
    info_box,
)

dashboard = DashboardService()


def render():
    """
    Executive Home Dashboard
    """

    load_theme()

    summary = dashboard.get_summary()

    # ==========================================================
    # Header
    # ==========================================================

    page_header(
        title="RealNut Intelligence",
        subtitle="Blinkit Seller Business Intelligence Platform",
        icon="🥜",
    )

    # ==========================================================
    # System Status
    # ==========================================================

    left, right = st.columns([3, 1])

    with left:

        section_header("System Status")

        if summary["database_ready"]:
            status_badge(
                "🟢 Database Connected",
                success=True,
            )
        else:
            status_badge(
                "🔴 Awaiting Import",
                success=False,
            )

    with right:

        st.metric(
            "Version",
            "1.0.0",
        )

    st.write("")

    # ==========================================================
    # KPI Dashboard
    # ==========================================================

    section_header("Business KPIs")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        metric_card(
            "Revenue",
            inr(summary["revenue"]),
            "💰",
        )

    with c2:
        metric_card(
            "Units Sold",
            f"{summary['units_sold']:,}",
            "📦",
        )

    with c3:
        metric_card(
            "Products",
            summary["products"],
            "🥜",
        )

    with c4:
        metric_card(
            "Cities",
            summary["cities"],
            "🌍",
        )

    with c5:
        metric_card(
            "Revenue / Unit",
            f"₹{summary['avg_revenue_per_unit']:,.2f}",
            "📈",
        )

    st.write("")

    # ==========================================================
    # Revenue Trend
    # ==========================================================

    section_header("Revenue Trend")

    trend = dashboard.get_revenue_trend()

    if trend.empty:

        info_box(
            "Import a Blinkit Sales Report to view revenue trends."
        )

    else:

        fig = px.line(
            trend,
            x="order_date",
            y="revenue",
            markers=True,
        )

        fig.update_traces(
            line_width=4,
            marker_size=8,
        )

        fig.update_layout(

            height=420,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="white",

            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20,
            ),

        )

        fig.update_xaxes(
            showgrid=False,
        )

        fig.update_yaxes(
            gridcolor="#E8DFCF",
            zeroline=False,
        )

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False,
                "scrollZoom": False,
            },
        )

    st.write("")

    # ==========================================================
    # Executive Summary
    # ==========================================================

    section_header("Executive Summary")

    left, right = st.columns([2.2, 1])

    with left:

        st.markdown("### 📈 Business Overview")

        a, b = st.columns(2)

        with a:

            st.metric(
                "Total Revenue",
                inr(summary["revenue"]),
            )

            st.metric(
                "Orders Processed",
                f"{summary['orders']:,}",
            )

            st.metric(
                "Products",
                summary["products"],
            )

        with b:

            st.metric(
                "Cities Served",
                summary["cities"],
            )

            st.metric(
                "Units Sold",
                f"{summary['units_sold']:,}",
            )

            st.metric(
                "Average Revenue / Unit",
                f"₹{summary['avg_revenue_per_unit']:,.2f}",
            )

    with right:

        st.markdown("### ⚙️ Platform")

        if summary["database_ready"]:

            st.success("Database Ready")

        else:

            st.error("No Data Imported")

        st.metric(
            "Rows Imported",
            summary["rows"],
        )

        st.metric(
            "Last Import",
            summary["last_import"],
        )

        st.metric(
            "Platform",
            "v1.0.0",
        )

    st.write("")

    # ==========================================================
    # Performance Overview
    # ==========================================================

    section_header("Performance Overview")

    left, right = st.columns(2)

    # ----------------------------------------------------------
    # Top Products
    # ----------------------------------------------------------

    with left:

        st.markdown("### 🏆 Top Products")

        top_products = dashboard.get_top_products()

        if top_products.empty:

            info_box(
                "No product data available."
            )

        else:

            premium_table(top_products)

    # ----------------------------------------------------------
    # Top Cities
    # ----------------------------------------------------------

    with right:

        st.markdown("### 🌍 Top Cities")

        top_cities = dashboard.get_top_cities()

        if top_cities.empty:

            info_box(
                "No regional data available."
            )

        else:

            premium_table(top_cities)

    st.write("")

    # ==========================================================
    # Recent Activity
    # ==========================================================

    section_header("Recent Activity")

    activity = dashboard.get_recent_activity()

    if activity:

        for item in activity:

            st.success(item)

    else:

        info_box(
            "No activity has been recorded yet."
        )

    st.write("")

    # ==========================================================
    # Quick Access
    # ==========================================================

    section_header("Quick Access")

    row1, row2 = st.columns(2)

    with row1:

        st.info(
            """
### 📤 Import Sales Report

Upload the latest Blinkit Seller Sales Report.

The application automatically:

• Cleans the dataset

• Rebuilds the SQLite database

• Refreshes all dashboards

• Updates analytics
"""
        )

        st.info(
            """
### 📈 Sales Dashboard

View

• Revenue trends

• Product performance

• Units sold

• Business KPIs
"""
        )

    with row2:

        st.info(
            """
### 🌍 Regional Analytics

Analyse

• City performance

• Regional revenue

• Geographic sales

• Expansion opportunities
"""
        )

        st.info(
            """
### 🚨 Smart Alerts

Automatically identify

• Declining products

• Revenue drops

• Business anomalies

• Performance warnings
"""
        )

    st.write("")

    # ==========================================================
    # Platform Information
    # ==========================================================

    section_header("Platform Information")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("### 🥜 RealNut Intelligence")

        st.write("Version **1.0.0**")

        st.write("Current Module")

        st.write("• Blinkit Business Intelligence")

        st.write("Available Modules")

        st.write("• Executive Dashboard")

        st.write("• Sales Analytics")

        st.write("• Regional Analytics")

        st.write("• Smart Alerts")

    with c2:

        st.markdown("### 💾 Current Dataset")

        st.metric(
            "Rows Loaded",
            summary["rows"],
        )

        st.metric(
            "Products",
            summary["products"],
        )

        st.metric(
            "Cities",
            summary["cities"],
        )

        if summary["database_ready"]:

            st.success("Database Connected")

        else:

            st.warning("Awaiting Data Import")

    st.write("")

    # ==========================================================
    # Footer
    # ==========================================================

    st.divider()

    left, center, right = st.columns([3, 1, 1])

    with left:

        st.caption(
            "🥜 RealNut Intelligence | Executive Business Intelligence Platform"
        )

    with center:

        st.caption("Version 1.0.0")

    with right:

        if summary["database_ready"]:

            st.caption("🟢 Ready")

        else:

            st.caption("🔴 No Data")