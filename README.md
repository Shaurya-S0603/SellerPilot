# 🥜 RealNut Intelligence

> **A Premium Business Intelligence Platform for Blinkit Seller Analytics**

RealNut Intelligence is a modern analytics platform built specifically for Blinkit sellers. It transforms raw seller reports into actionable business insights through automated ETL pipelines, interactive dashboards, and intelligent analytics.

Designed with a premium executive dashboard experience, the platform enables business owners to monitor sales performance, identify regional trends, analyze product performance, and make data-driven decisions without manually processing spreadsheets.

---

# ✨ Features

## 📤 Smart Data Import

- One-click Blinkit Sales Report upload
- Automatic Excel validation
- Intelligent data cleaning
- Missing value handling
- SQLite database loading
- Import verification
- Processing summary
- Cleaned dataset generation

---

## 📊 Sales Dashboard

Gain a complete overview of sales performance.

### Includes

- Revenue Overview
- Units Sold
- Weekly Revenue
- Weekly Growth
- Revenue Trend
- Product Contribution
- Top 10 Products
- Bottom 10 Products
- Recent Sales

---

## 🌍 Regional Analytics

Analyze geographical business performance.

### Includes

- Revenue by City
- Top Cities
- Bottom Cities
- City Contribution
- Regional Rankings
- Interactive Visualizations

---

## 🚨 Smart Alerts

Monitor business performance automatically.

Examples include:

- Low revenue alerts
- Declining products
- High-performing cities
- Revenue anomalies
- Inventory-related alerts *(future)*

---

## 🎨 Premium User Interface

- Modern executive dashboard
- Responsive layout
- Premium cards
- Interactive Plotly charts
- Professional AG Grid tables
- Indian currency formatting
- Consistent green theme
- Clean typography

---

# 🏗️ Project Structure

```text
RealNut_BI/
│
├── app.py
│
├── assets/
│   └── theme.css
│
├── config/
│
├── database/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── exports/
│
├── etl/
│   ├── importer.py
│   ├── cleaner.py
│   └── loader.py
│
├── logs/
│
├── services/
│
├── utils/
│
├── views/
│   ├── home.py
│   ├── import_data.py
│   ├── sales_dashboard.py
│   ├── regional_dashboard.py
│   └── alerts.py
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Technology Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| Charts | Plotly |
| Tables | Streamlit AG Grid |
| Database | SQLite |
| ORM | SQLAlchemy |
| Data Processing | Pandas |
| Excel Support | OpenPyXL |
| Reporting | ReportLab |
| Styling | Custom CSS |

---

# 🔄 Data Pipeline

```
Blinkit Sales Report (.xlsx)

        │

        ▼

Import Excel

        │

        ▼

Validate Columns

        │

        ▼

Clean & Standardize

        │

        ▼

Handle Missing Values

        │

        ▼

Load SQLite Database

        │

        ▼

Generate Analytics

        │

        ▼

Interactive Dashboards
```

---

# 📈 Analytics Available

## Executive KPIs

- Total Revenue
- Units Sold
- Products
- Cities
- Orders
- Average Revenue per Unit

---

## Product Analytics

- Revenue by Product
- Units Sold
- Product Contribution
- Top Performers
- Lowest Performers

---

## Regional Analytics

- Revenue by City
- Units by City
- City Contribution
- Best Performing Cities
- Lowest Performing Cities

---

## Weekly Performance

- Current Week Revenue
- Previous Week Revenue
- Week-over-Week Growth

---

# 🚀 Installation

Clone the repository.

```bash
git clone https://github.com/yourusername/RealNut_BI.git
```

Move into the project.

```bash
cd RealNut_BI
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
streamlit run app.py
```

---

# 📁 Supported Input

Currently supported:

- ✅ Blinkit Seller Sales Report (.xlsx)

Planned support:

- Inventory Reports
- Warehouse Reports
- Darkstore Reports
- Keyword Reports

---

# 🛣️ Roadmap

### Phase 1 ✅

- Executive Dashboard
- Sales Dashboard
- Regional Analytics
- Import Pipeline
- Smart Alerts
- SQLite Integration

### Phase 2 🚧

- Inventory Dashboard
- Warehouse Analytics
- Brand Performance
- Darkstore Performance
- Monthly Analytics
- Forecasting

### Phase 3 🔮

- AI Business Insights
- Demand Prediction
- Automated Recommendations
- Chat Assistant
- PDF Reports
- Scheduled Email Reports
- Multi-user Authentication

---

# 🔒 Data Privacy

RealNut Intelligence processes all uploaded reports locally.

- No seller data is transmitted to third-party servers.
- Uploaded reports are processed securely.
- SQLite database remains local unless deployed with external storage.
- Sensitive business information remains under your control.

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Developed By

**Shaurya Singhal**

Computer Science Student at NTU Singapore

Game Developer • AI Programmer • Data Analytics Enthusiast

---

## ⭐ If you found this project useful, consider giving it a star.
