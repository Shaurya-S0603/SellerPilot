"""
views/regional_dashboard.py

Professional Regional Analytics Dashboard
"""

import plotly.express as px
import streamlit as st

from services.dashboard_service import DashboardService
from utils.ui import (
    page_header,
    section_header,
    metric_card,
    info_box,
)
from utils.table import premium_table

dashboard = DashboardService()


def render():

    page_header(
        "Regional Analytics",
        "City-wise sales performance and regional insights",
        "🌍",
    )

    summary = dashboard.get_summary()

    if not summary["database_ready"]:
        info_box("Import a Blinkit Sales Report to view regional analytics.")
        return

    # ==========================================================
    # LOAD DATA
    # ==========================================================

    city_sales = dashboard.get_sales_by_city()

    if city_sales.empty:
        info_box("No regional sales data available.")
        return

    best_city = city_sales.iloc[0]

    average_revenue = city_sales["revenue"].mean()
    average_units = city_sales["units_sold"].mean()

    # ==========================================================
    # KPI CARDS
    # ==========================================================

    section_header("Regional Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_card(
            "Cities Served",
            f"{summary['cities']}",
            "🌍",
        )

    with c2:

        metric_card(
            "Best City",
            best_city["city"],
            "🏆",
        )

    with c3:

        metric_card(
            "Avg Revenue / City",
            f"₹{average_revenue:,.0f}",
            "💰",
        )

    with c4:

        metric_card(
            "Avg Units / City",
            f"{average_units:,.0f}",
            "📦",
        )

    st.write("")

    # ==========================================================
    # REVENUE BY CITY
    # ==========================================================

    section_header("Revenue by City")

    revenue_chart = city_sales.sort_values(
        "revenue",
        ascending=True,
    )

    fig = px.bar(
        revenue_chart,
        x="revenue",
        y="city",
        orientation="h",
        text="revenue",
    )

    fig.update_traces(

        marker_color="#2E7D32",

        texttemplate="₹%{x:,.0f}",

        textposition="outside",

    )

    fig.update_layout(

        template="plotly_white",

        height=550,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),

        xaxis_title="Revenue",

        yaxis_title="",

        paper_bgcolor="white",

        plot_bgcolor="white",

    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#ECECEC",
    )

    fig.update_yaxes(
        showgrid=False,
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

    st.write("")

    # ==========================================================
    # UNITS SOLD BY CITY
    # ==========================================================

    section_header("Units Sold by City")

    units_chart = city_sales.sort_values(
        "units_sold",
        ascending=True,
    )

    fig = px.bar(
        units_chart,
        x="units_sold",
        y="city",
        orientation="h",
        text="units_sold",
    )

    fig.update_traces(

        marker_color="#66BB6A",

        textposition="outside",

    )

    fig.update_layout(

        template="plotly_white",

        height=550,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),

        xaxis_title="Units Sold",

        yaxis_title="",

        paper_bgcolor="white",

        plot_bgcolor="white",

    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#ECECEC",
    )

    fig.update_yaxes(
        showgrid=False,
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

    st.write("")

    # ==========================================================
    # CITY CONTRIBUTION
    # ==========================================================

    section_header("City Revenue Contribution")

    contribution = dashboard.get_city_contribution()

    if contribution.empty:

        info_box("No city contribution data available.")

    else:

        fig = px.pie(
            contribution,
            names="city",
            values="revenue",
            hole=0.55,
            color_discrete_sequence=[
                "#1B5E20",
                "#2E7D32",
                "#388E3C",
                "#43A047",
                "#66BB6A",
                "#81C784",
                "#A5D6A7",
                "#C8E6C9",
                "#E8F5E9",
                "#A3D9A5",
            ],
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
        )

        fig.update_layout(
            template="plotly_white",
            height=520,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10,
            ),
            showlegend=True,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    st.write("")

    # ==========================================================
    # TOP / BOTTOM CITIES
    # ==========================================================

    section_header("City Performance")

    left, right = st.columns(2)

    with left:

        st.markdown("#### 🏆 Top 10 Cities")

        top = dashboard.get_top_cities(10)

        if top.empty:

            info_box("No city data available.")

        else:

            premium_table(
                top,
                height=420,
            )

    with right:

        st.markdown("#### 📉 Bottom 10 Cities")

        bottom = dashboard.get_bottom_cities(10)

        if bottom.empty:

            info_box("No city data available.")

        else:

            premium_table(
                bottom,
                height=420,
            )

    st.write("")

    # ==========================================================
    # RECENT REGIONAL TRANSACTIONS
    # ==========================================================

    section_header("Recent Regional Transactions")

    recent = dashboard.get_recent_sales(20)

    if recent.empty:

        info_box("No recent transactions available.")

    else:

        regional_recent = recent[
            [
                "order_date",
                "city",
                "product_name",
                "units_sold",
                "revenue",
            ]
        ]

        premium_table(
            regional_recent,
            height=430,
        )

    st.write("")

    # ==========================================================
    # REGIONAL INSIGHTS
    # ==========================================================

    section_header("Regional Insights")

    total_revenue = city_sales["revenue"].sum()

    top_city_share = (
        best_city["revenue"] / total_revenue * 100
        if total_revenue > 0
        else 0
    )

    c1, c2 = st.columns(2)

    with c1:

        st.success(
            f"""
**Top Performing Region**

🏆 **{best_city['city']}**

Revenue: **₹{best_city['revenue']:,.0f}**

Units Sold: **{best_city['units_sold']:,}**

Orders: **{best_city['orders']:,}**
"""
        )

    with c2:

        st.info(
            f"""
**Regional Coverage**

Cities Served: **{summary['cities']}**

Average Revenue / City: **₹{average_revenue:,.0f}**

Average Units / City: **{average_units:,.0f}**

Top City Contribution: **{top_city_share:.1f}%**
"""
        )

    st.write("")

    # ==========================================================
    # FOOTER
    # ==========================================================

    st.divider()

    left, right = st.columns([3, 1])

    with left:

        st.caption(
            "🥜 RealNut Intelligence | Regional Analytics"
        )

    with right:

        st.caption("Version 1.0.0")