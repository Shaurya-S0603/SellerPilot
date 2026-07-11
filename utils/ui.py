"""
utils/ui.py

Reusable UI components for RealNut Intelligence.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from utils.formatters import inr


# ==========================================================
# Theme Loader
# ==========================================================

def load_theme():

    css_path = Path("assets/theme.css")

    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


# ==========================================================
# Page Header
# ==========================================================

def page_header(title: str, subtitle: str = "", icon: str = "🥜"):

    st.markdown(
        f"""
<div class="page-header">
    <div class="page-title">{icon} {title}</div>
    <div class="page-subtitle">{subtitle}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Section Header
# ==========================================================

def section_header(title: str):

    st.markdown(
        f"""
<div class="section-heading">
    {title}
</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# KPI Card
# ==========================================================

def metric_card(title, value, icon="📊"):

    st.markdown(
        f"""
<div class="metric-card">

<div class="metric-icon">
{icon}
</div>

<div class="metric-title">
{title}
</div>

<div class="metric-value">
{value}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Dashboard Card
# ==========================================================

def dashboard_card(title: str, body: str):

    st.markdown(
        f"""
<div class="dashboard-card">

<div class="card-title">
{title}
</div>

<div class="card-body">
{body}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Status Badge
# ==========================================================

def status_badge(label: str, success=True):

    color = "#22C55E" if success else "#DC2626"

    st.markdown(
        f"""
<div style="
display:inline-block;
background:{color};
color:white;
padding:8px 18px;
border-radius:999px;
font-weight:600;
margin-bottom:15px;
">
{label}
</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Alerts
# ==========================================================

def success_box(message):

    st.success(message)


def warning_box(message):

    st.warning(message)


def error_box(message):

    st.error(message)


def info_box(message):

    st.info(message)


# ==========================================================
# Empty State
# ==========================================================

def empty_state(title, message, icon="📭"):

    st.markdown(
        f"""
<div class="dashboard-card" style="text-align:center;">

<div style="font-size:60px;">
{icon}
</div>

<h3>{title}</h3>

<p>{message}</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Feature Card
# ==========================================================

def feature_card(title, description, icon="📊"):

    st.markdown(
        f"""
<div class="feature-card">

<div class="feature-icon">
{icon}
</div>

<div class="feature-title">
{title}
</div>

<div class="feature-description">
{description}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Divider
# ==========================================================

def section_divider():

    st.divider()


# ==========================================================
# Premium Table
# ==========================================================

def premium_table(df: pd.DataFrame, title=None):
    """
    Premium styled dataframe.

    Automatically formats revenue columns
    using Indian numbering.
    """

    dataframe = df.copy()

    revenue_columns = {
        "revenue",
        "Revenue",
        "Total Revenue",
        "GMV",
        "Sales",
    }

    for col in dataframe.columns:

        if col in revenue_columns:

            dataframe[col] = dataframe[col].apply(inr)

    if title:
        section_header(title)

    styled = (
        dataframe.style
        .hide(axis="index")
        .set_properties(
            **{
                "white-space": "normal",
                "text-align": "left",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#1B4332"),
                        ("color", "white"),
                        ("font-size", "15px"),
                        ("font-weight", "600"),
                        ("padding", "14px"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("padding", "12px"),
                        ("font-size", "14px"),
                        ("border-bottom", "1px solid #E5E7EB"),
                    ],
                },
                {
                    "selector": "tbody tr:nth-child(even)",
                    "props": [
                        ("background-color", "#F8FAFC"),
                    ],
                },
                {
                    "selector": "tbody tr:hover",
                    "props": [
                        ("background-color", "#EEF7F0"),
                    ],
                },
            ]
        )
    )

    st.dataframe(
        styled,
        hide_index=True,
        width="stretch",
        height=min(len(dataframe) * 38 + 40, 500),
    )