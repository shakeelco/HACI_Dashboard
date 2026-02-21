import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Executive Summary",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Executive Summary")

# -----------------------------
# Load Excel data
# -----------------------------
file_path = "HACI_Business_Intelligence_Master.xlsx"

revenue = pd.read_excel(file_path, sheet_name="Revenue")
expenses = pd.read_excel(file_path, sheet_name="Expenses")
clients = pd.read_excel(file_path, sheet_name="Clients")

# -----------------------------
# KPI Calculations
# -----------------------------
total_revenue = revenue["Gross_Amount"].sum()
total_expenses = expenses["Amount"].sum()
net_profit = total_revenue - total_expenses
total_clients = clients["Client_ID"].nunique()

# Safe additional KPIs
ebitda = net_profit \
    + expenses.get("Depreciation", pd.Series([0])).sum() \
    + expenses.get("Interest", pd.Series([0])).sum() \
    + expenses.get("Taxes", pd.Series([0])).sum()

gross_margin = ((total_revenue - expenses.get("COGS", pd.Series([0])).sum()) / total_revenue) * 100
profit_margin = (net_profit / total_revenue) * 100

# Revenue monthly trend
revenue["Invoice_Date"] = pd.to_datetime(revenue["Invoice_Date"])
monthly_revenue = revenue.groupby(revenue["Invoice_Date"].dt.to_period("M"))["Gross_Amount"].sum().reset_index()
monthly_revenue["Invoice_Date"] = monthly_revenue["Invoice_Date"].astype(str)
revenue_growth = monthly_revenue["Gross_Amount"].pct_change().fillna(0) * 100
latest_growth = revenue_growth.iloc[-1]

# -----------------------------
# KPI Blocks with Expanders
# -----------------------------
st.subheader("Key Metrics")

kpi_data = [
    {"name": "Total Revenue", "value": total_revenue, "trend": latest_growth, 
     "desc": "Total Revenue is the sum of all income from sales."},
    {"name": "Total Expenses", "value": total_expenses, "trend": None, 
     "desc": "Total Expenses includes all operational costs such as salaries, rent, utilities, etc."},
    {"name": "Net Profit", "value": net_profit, "trend": latest_growth, 
     "desc": "Net Profit = Total Revenue - Total Expenses. It shows the company's actual profitability."},
    {"name": "Total Clients", "value": total_clients, "trend": None, 
     "desc": "Total Clients is the count of unique customers."},
    {"name": "EBITDA", "value": ebitda, "trend": None, 
     "desc": "EBITDA = Net Profit + Depreciation + Interest + Taxes. It shows operational performance."},
    {"name": "Gross Margin", "value": gross_margin, "trend": None, 
     "desc": "Gross Margin = (Revenue - COGS) / Revenue * 100. Indicates production/sales efficiency."},
    {"name": "Profit Margin", "value": profit_margin, "trend": None, 
     "desc": "Profit Margin = Net Profit / Revenue * 100. Shows the percentage of revenue retained as profit."},
]

# Display KPIs in 3 columns per row
for i in range(0, len(kpi_data), 3):
    cols = st.columns(3)
    for j, kpi in enumerate(kpi_data[i:i+3]):
        value_display = f"PKR {kpi['value']:,.0f}" if isinstance(kpi['value'], (int, float)) else kpi['value']
        with cols[j]:
            with st.expander(f"{kpi['name']}: {value_display}"):
                st.write(f"**What it is:** {kpi['desc']}")
                if kpi.get("trend") is not None:
                    arrow = "⬆️" if kpi["trend"] >= 0 else "⬇️"
                    st.write(f"**Trend:** {arrow} {abs(kpi['trend']):.1f}% compared to previous month")

# -----------------------------
# Revenue Trend Chart
# -----------------------------
st.subheader("Monthly Revenue Trend")
fig = px.line(monthly_revenue, x="Invoice_Date", y="Gross_Amount", title="Monthly Revenue", markers=True)
st.plotly_chart(fig, use_container_width=True)
