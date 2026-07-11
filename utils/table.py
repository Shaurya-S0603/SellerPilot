from st_aggrid import AgGrid, ColumnsAutoSizeMode, GridOptionsBuilder, GridUpdateMode, JsCode
import pandas as pd


def format_inr(value):
    """
    Formats numbers in Indian numbering style.
    """

    if pd.isna(value):
        return ""

    value = float(value)

    if abs(value) >= 10000000:
        return f"₹{value/10000000:.2f} Cr"

    if abs(value) >= 100000:
        return f"₹{value/100000:.2f} L"

    if abs(value) >= 1000:
        return f"₹{value/1000:.1f} K"

    return f"₹{value:,.0f}"


def premium_table(df, height=340):
    """
    Premium AG Grid table with RealNut styling.
    """

    df = df.copy()

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(
        sortable=True,
        filter=False,
        floatingFilter=False,
        resizable=True,
        wrapText=True,
        autoHeight=True,
    )

    gb.configure_grid_options(
        animateRows=True,
        rowHeight=46,
        headerHeight=50,
        suppressMenuHide=True,
        suppressRowClickSelection=True,
    )

    # -----------------------------
    # Widen product columns
    # -----------------------------

    for col in df.columns:

        name = col.lower()

        if "product" in name:
            gb.configure_column(
                col,
                minWidth=350,
                flex=3,
            )

        elif "city" in name:
            gb.configure_column(
                col,
                minWidth=170,
                flex=1,
            )

        elif "revenue" in name:
            gb.configure_column(
                col,
                minWidth=100,
                type=["numericColumn"],
                valueFormatter=JsCode(
                    """
                    function(params){
                        if(params.value==null) return "";
                        return "₹" + Number(params.value).toLocaleString(
                            "en-IN",
                            {
                                minimumFractionDigits:0,
                                maximumFractionDigits:2
                            }
                        );
                    }
                    """
                ),
            )

    grid_options = gb.build()

    custom_css = {
        ".ag-header": {
            "background-color": "#1B5E20 !important",
            "border-bottom": "2px solid #145A32 !important",
        },
        ".ag-header-cell": {
            "background-color": "#1B5E20 !important",
            "color": "white !important",
            "font-weight": "700",
            "font-size": "14px",
        },
        ".ag-header-cell-label": {
            "color": "white !important",
        },
        ".ag-root-wrapper": {
            "border": "1px solid #D9E5D5",
            "border-radius": "14px",
        },
        ".ag-row": {
            "font-size": "14px",
        },
        ".ag-row:nth-child(even)": {
            "background-color": "#F8FBF6",
        },
        ".ag-row-hover": {
            "background-color": "#E8F5E9 !important",
        },
    }

    AgGrid(
        df,
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=False,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        theme="streamlit",
        custom_css=custom_css,
        height=height,
    )