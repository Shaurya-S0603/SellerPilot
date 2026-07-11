"""
views/sales_dashboard.py

Professional Sales Dashboard
"""

import streamlit as st
import plotly.express as px

from services.dashboard_service import DashboardService

from utils.ui import (
    load_theme,
    page_header,
    section_header,
    metric_card,
    info_box,
)

from utils.table import premium_table


dashboard = DashboardService()


def render():

    load_theme()

    page_header(
        title="Sales Dashboard",
        subtitle="Product performance and revenue analytics",
        icon="📊",
    )

    summary = dashboard.get_summary()

    if not summary["database_ready"]:
        info_box(
            "Import a Blinkit Sales Report to begin viewing sales analytics."
        )
        return

    # ==========================================================
    # KPI OVERVIEW
    # ==========================================================

    section_header("Sales Overview")

    current_week = dashboard.get_current_week_revenue()
    last_week = dashboard.get_last_week_revenue()

    if last_week > 0:
        growth = ((current_week - last_week) / last_week) * 100
    else:
        growth = 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Revenue",
            f"₹{summary['revenue']:,.0f}",
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
            "This Week",
            f"₹{current_week:,.0f}",
            "📅",
        )

    with c4:
        metric_card(
            "Growth",
            f"{growth:.1f}%",
            "📈",
        )

    st.write("")

    # ==========================================================
    # REVENUE TREND
    # ==========================================================

    section_header("Revenue Trend")

    trend = dashboard.get_revenue_trend()

    if trend.empty:

        info_box("No revenue trend available.")

    else:

        fig = px.line(
            trend,
            x="order_date",
            y="revenue",
            markers=True,
        )

        fig.update_traces(
            line=dict(
                color="#1B5E20",
                width=4,
            ),
            marker=dict(
                size=7,
                color="#2E7D32",
            ),
        )

        fig.update_layout(
            template="plotly_white",
            height=430,
            margin=dict(
                l=10,
                r=10,
                t=15,
                b=10,
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            hovermode="x unified",
        )

        fig.update_xaxes(
            showgrid=False,
            title=None,
        )

        fig.update_yaxes(
            gridcolor="#E8E8E8",
            title=None,
            tickprefix="₹",
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    st.write("")

    # ==========================================================
    # WEEKLY PERFORMANCE
    # ==========================================================

    section_header("This Week vs Last Week")

    comparison = dashboard.get_weekly_comparison()

    left, right = st.columns(2)

    with left:

        metric_card(
            "This Week Revenue",
            f"₹{comparison['this_week_revenue']:,.0f}",
            "🟢",
        )

    with right:

        metric_card(
            "Last Week Revenue",
            f"₹{comparison['last_week_revenue']:,.0f}",
            "📊",
        )

    st.write("")

    if comparison["change_percent"] >= 0:

        st.success(
            f"Revenue increased by **{comparison['change_percent']:.1f}%** compared with last week."
        )

    else:

        st.error(
            f"Revenue decreased by **{abs(comparison['change_percent']):.1f}%** compared with last week."
        )

    st.write("")

    # ==========================================================
    # PRODUCT CONTRIBUTION
    # ==========================================================

    section_header("Product Contribution")

    contribution = dashboard.get_product_contribution()

    if contribution.empty:

        info_box("No product contribution data available.")

    else:

        fig = px.pie(
            contribution,
            names="product_name",
            values="revenue",
            hole=0.60,
            color_discrete_sequence=[
                "#1B5E20",
                "#2E7D32",
                "#388E3C",
                "#43A047",
                "#66BB6A",
                "#81C784",
                "#A5D6A7",
                "#C8E6C9",
            ],
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
        )

        fig.update_layout(
            template="plotly_white",
            height=500,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10,
            ),
            legend_title=None,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    st.write("")
    # ==========================================================
    # PRODUCT RANKINGS
    # ==========================================================

    section_header("Product Rankings")

    left, right = st.columns(2)

    with left:

        st.markdown("#### 🏆 Top 10 Products")

        top_products = dashboard.get_top_products(limit=10)

        if top_products.empty:

            info_box("No product data available.")

        else:

            premium_table(
                top_products,
                height=430,
            )

    with right:

        st.markdown("#### 📉 Bottom 10 Products")

        bottom_products = dashboard.get_bottom_products(limit=10)

        if bottom_products.empty:

            info_box("No product data available.")

        else:

            premium_table(
                bottom_products,
                height=430,
            )

    st.write("")

    # ==========================================================
    # RECENT SALES
    # ==========================================================

    section_header("Recent Sales")

    recent = dashboard.get_recent_sales(limit=20)

    if recent.empty:

        info_box(
            "No recent transactions available."
        )

    else:

        recent = recent.rename(
            columns={
                "order_date": "Order Date",
                "product_name": "Product",
                "city": "City",
                "units_sold": "Units",
                "revenue": "Revenue",
            }
        )

        display_columns = [
            c
            for c in [
                "Order Date",
                "Product",
                "City",
                "Units",
                "Revenue",
            ]
            if c in recent.columns
        ]

        premium_table(
            recent[display_columns],
            height=500,
        )

    st.write("")

    # ==========================================================
    # SALES INSIGHTS
    # ==========================================================

    section_header("Sales Insights")

    revenue = summary["revenue"]
    units = summary["units_sold"]
    avg = summary["avg_revenue_per_unit"]

    insight_left, insight_right = st.columns(2)

    with insight_left:

        st.info(
            f"""
**Revenue Summary**

• Total Revenue: **₹{revenue:,.0f}**

• Total Units Sold: **{units:,}**

• Average Revenue per Unit: **₹{avg:,.2f}**
"""
        )

    with insight_right:

        if growth > 0:

            st.success(
                f"""
Weekly Performance

Revenue is **{growth:.1f}% higher**
than the previous week.
"""
            )

        elif growth < 0:

            st.error(
                f"""
Weekly Performance

Revenue is **{abs(growth):.1f}% lower**
than the previous week.
"""
            )

        else:

            st.info(
                """
Weekly Performance

Revenue remained unchanged compared
to the previous week.
"""
            )

    st.write("")

    # ==========================================================
    # FOOTER
    # ==========================================================

    st.divider()

    footer_left, footer_right = st.columns([3, 1])

    with footer_left:

        st.caption(
            "🥜 RealNut Intelligence | Sales Analytics Dashboard"
        )

    with footer_right:

        st.caption(
            "Version 1.0.0"
        )