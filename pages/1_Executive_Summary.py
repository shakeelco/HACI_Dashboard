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
# Key Metrics Calculations
# -----------------------------
total_revenue = revenue["Gross_Amount"].sum()
total_expenses = expenses["Amount"].sum()
net_profit = total_revenue - total_expenses
total_clients = clients["Client_ID"].nunique()

# Additional KPIs
ebitda = net_profit \
        + expenses.get("Depreciation", pd.Series([0])).sum() \
        + expenses.get("Interest", pd.Series([0])).sum() \
        + expenses.get("Taxes", pd.Series([0])).sum()

gross_margin = ((total_revenue - expenses.get("COGS", pd.Series([0])).sum()) / total_revenue) * 100
profit_margin = (net_profit / total_revenue) * 100

# Revenue Growth (month-over-month)
revenue["Invoice_Date"] = pd.to_datetime(revenue["Invoice_Date"])
monthly_revenue = revenue.groupby(revenue["Invoice_Date"].dt.to_period("M"))["Gross_Amount"].sum().reset_index()
monthly_revenue["Invoice_Date"] = monthly_revenue["Invoice_Date"].astype(str)
revenue_growth = monthly_revenue["Gross_Amount"].pct_change().fillna(0) * 100
latest_growth = revenue_growth.iloc[-1]

# -----------------------------
# Display KPIs in columns
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"PKR {total_revenue:,.0f}")
col2.metric("Total Expenses", f"PKR {total_expenses:,.0f}")
col3.metric("Net Profit", f"PKR {net_profit:,.0f}", delta=f"{(net_profit - revenue['Gross_Amount'].mean()):,.0f}")
col4.metric("Total Clients", total_clients)

col5, col6, col7 = st.columns(3)
col5.metric("EBITDA", f"PKR {ebitda:,.0f}")
col6.metric("Gross Margin", f"{gross_margin:.1f} %")
col7.metric("Profit Margin", f"{profit_margin:.1f} %")

# Revenue Trend
fig = px.line(monthly_revenue, x="Invoice_Date", y="Gross_Amount", title="Monthly Revenue Trend")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Arrows for trends
# -----------------------------
st.subheader("Trends & Indicators")
if latest_growth >= 0:
    st.write(f"Revenue Growth (latest month): ⬆️ {latest_growth:.1f}%")
else:
    st.write(f"Revenue Growth (latest month): ⬇️ {abs(latest_growth):.1f}%")

if net_profit >= 0:
    st.write(f"Net Profit Trend: ⬆️ PKR {net_profit:,.0f}")
else:
    st.write(f"Net Profit Trend: ⬇️ PKR {abs(net_profit):,.0f}")

# -----------------------------
# Expandable explanations
# -----------------------------
st.subheader("KPI Explanations")
with st.expander("Total Revenue"):
    st.write("Total Revenue is the sum of all income generated from sales before any expenses are subtracted.")

with st.expander("Total Expenses"):
    st.write("Total Expenses includes all operational costs, including salaries, rent, utilities, and other business expenses.")

with st.expander("Net Profit"):
    st.write("Net Profit is Revenue minus Expenses. It shows the actual profit the company has earned.")

with st.expander("EBITDA"):
    st.write("EBITDA stands for Earnings Before Interest, Taxes, Depreciation, and Amortization. It highlights operational profitability without accounting for financial and accounting decisions.")

with st.expander("Gross Margin"):
    st.write("Gross Margin shows the percentage of revenue left after subtracting the Cost of Goods Sold (COGS). It indicates how efficiently the company produces or sells its products.")

with st.expander("Profit Margin"):
    st.write("Profit Margin shows the percentage of net profit earned from total revenue.")

with st.expander("Revenue Growth"):
    st.write("Revenue Growth measures how much the revenue has increased or decreased compared to the previous month.")

with st.expander("Total Clients"):
    st.write("Total Clients is the count of unique customers who have purchased or engaged with the company.")

# -----------------------------
# Optional: Add arrows/icons in KPIs visually
# -----------------------------
st.subheader("Visual Indicators")
col1, col2 = st.columns(2)
col1.write("Revenue Trend: " + ("⬆️" if latest_growth >= 0 else "⬇️"))
col2.write("Net Profit: " + ("⬆️" if net_profit >= 0 else "⬇️"))

