"""
pages/import_data.py

Import page for RealNut Intelligence.
"""

import streamlit as st

from services.import_service import ImportService

from utils.ui import (
    load_theme,
    page_header,
    section_header,
    success_box,
    error_box,
    info_box,
)

service = ImportService()


def render():

    load_theme()

    page_header(
        title="Import Sales Report",
        subtitle="Upload and process a Blinkit Seller Sales Report",
        icon="📤",
    )

    section_header("Upload Report")

    st.markdown(
        """
Upload the latest **Blinkit Seller Sales Report (.xlsx)**.

The platform will automatically:

- 📄 Read the Excel report
- 🧹 Clean and validate the dataset
- 🗑 Reset the existing database
- 💾 Import the new data
- ✅ Verify database integrity
- 📊 Refresh every dashboard
"""
    )

    uploaded_file = st.file_uploader(
        "Choose Blinkit Sales Report",
        type=["xlsx"],
    )

    if uploaded_file is None:

        info_box("Waiting for Blinkit Sales Report...")

        return

    # =====================================================
    # Selected File
    # =====================================================

    section_header("Selected File")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Filename",
            uploaded_file.name,
        )

    with c2:
        st.metric(
            "File Size",
            f"{uploaded_file.size / 1024:.2f} KB",
        )

    st.write("")

    # =====================================================
    # Import Button
    # =====================================================

    if st.button(
        "🚀 Start Import",
        width="stretch",
    ):

        try:

            with st.spinner("Importing sales report..."):

                result = service.run(uploaded_file)

            success_box(result["message"])

            summary = result["summary"]

            # =====================================================
            # Import Summary
            # =====================================================

            section_header("Import Summary")

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Raw Rows",
                    f"{result['raw_rows']:,}",
                )

                st.metric(
                    "Clean Rows",
                    f"{result['cleaned_rows']:,}",
                )

            with c2:

                st.metric(
                    "Imported Rows",
                    f"{result['imported_rows']:,}",
                )

                st.metric(
                    "Products",
                    f"{summary['products']:,}",
                )

            with c3:

                st.metric(
                    "Cities",
                    f"{summary['cities']:,}",
                )

                st.metric(
                    "Revenue",
                    f"₹{summary['revenue']:,.2f}",
                )

            st.divider()

            # =====================================================
            # Import Details
            # =====================================================

            section_header("Import Details")

            d1, d2, d3 = st.columns(3)

            with d1:

                st.metric(
                    "Completed",
                    "Success",
                )

                st.caption(result["timestamp"])

            with d2:

                st.metric(
                    "Duration",
                    f"{result['duration_seconds']:.2f}s",
                )

            with d3:

                st.metric(
                    "Database",
                    "Ready",
                )

            st.success(
                "✅ The dashboards have been refreshed and are now using the latest imported data."
            )

        except Exception as e:

            error_box(str(e))

    st.divider()

    # =====================================================
    # Supported Reports
    # =====================================================

    section_header("Supported Reports")

    left, right = st.columns(2)

    with left:

        st.success(
            """
**Currently Supported**

• Blinkit Seller Sales Report (.xlsx)
"""
        )

    with right:

        st.info(
            """
**Coming Soon**

• Inventory Reports

• Warehouse Reports

• Darkstore Reports

• Keyword Analytics

• Purchase Reports
"""
        )