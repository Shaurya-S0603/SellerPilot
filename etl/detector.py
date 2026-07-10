from pathlib import Path
import pandas as pd
from streamlit import columns
from etl.report_types import ReportType


class ReportDetector:

    SALES_COLUMNS = {
        "S.No.","Order Id","Order Date","Item Id","Product Name","Brand Name","UPC","Variant Description", "Mapping on consumer app (L0, L1, L2)", "Business Category", "Supply City", "Supply State", "Supply State GST", "Customer City", "Customer State	Order Status", "HSN Code", "IGST(%)", "CGST(%)", "SGST(%)", "CESS(%)","Quantity	MRP (Rs)","Selling Price (Rs)","IGST Value","CGST Value","SGST Value","CESS Value", "Total Tax","Total Gross Bill Amount"
    }

    DARKSTORE_COLUMNS = {
        "Product ID","Product Name","MRP","Item ID","UPC/EAN/UPC Exemption Code","Business Category Name","Assessment Period Start Date","Assessment Period End Date","Present Level","City","Darkstore name","Serving warehouse","Date","Darkstore remark","Available hours", "Operation hours", "Available (Yes/No)", "Considered for assessment (Y/N)", "Remarks", "Adjusted units sold per darkstore", "Target – adjusted units sold per darkstore", "Adjusted GMV per darkstore", "Target – adjusted GMV per darkstore", "Total orders", "Orders with complaints attributed to seller", "Complaint %", "Target – complaint %"
    }

    PRODUCT_COLUMNS = {
        "product name",
        "availability %",
        "adjusted gmv",
    }

    @staticmethod
    def detect(file_path: Path) -> ReportType:
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path, nrows=5)
        else:
            df = pd.read_excel(file_path, nrows=5)

        columns = {
            str(col).strip().lower()
            for col in df.columns
        }

        print(f"\n{file_path.name}")
        print(columns)