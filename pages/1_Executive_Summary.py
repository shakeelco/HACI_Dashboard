import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Executive Summary Dashboard")

# -----------------------------
# Load Data
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
# Helper Functions
# -----------------------------
def get_color_arrow(value, thresholds=None):
    """Return color, arrow, alert icon based on value"""
    if thresholds:  # check alert
        if value < thresholds.get("low", float('-inf')):
            return "red", "⬇️", "⚠️"
        elif value > thresholds.get("high", float('inf')):
            return "green", "⬆️", ""
        else:
            return "yellow", "➖", ""
    else:
        if value > 0:
            return "green", "⬆️", ""
        elif value < 0:
            return "red", "⬇️", ""
        else:
            return "orange", "➖", ""

def format_value(value, fmt="currency"):
    if fmt == "currency":
        return f"PKR {value:,.0f}"
    elif fmt == "percentage":
        return f"{value:.1f}%"
    else:
        return str(value)

# -----------------------------
# KPI Cards
# -----------------------------
st.subheader("Key Performance Indicators")

kpi_list = [
    {"name": "Total Revenue", "value": total_revenue, "trend": latest_growth, "format":"currency",
     "trend_series": monthly_revenue["Gross_Amount"], "desc":"Sum of all income from sales", "thresholds":{"low":0}},
    {"name": "Total Expenses", "value": total_expenses, "trend": None, "format":"currency",
     "trend_series": expenses["Amount"], "desc":"All operational costs"},
    {"name": "Net Profit", "value": net_profit, "trend": net_profit, "format":"currency",
     "trend_series": monthly_revenue["Gross_Amount"] - expenses["Amount"].sum(), "desc":"Revenue minus Expenses", "thresholds":{"low":0}},
    {"name": "Total Clients", "value": total_clients, "trend": None, "format":"number",
     "trend_series": clients["Client_ID"].value_counts().sort_index(), "desc":"Count of unique clients"},
    {"name": "EBITDA", "value": ebitda, "trend": None, "format":"currency",
     "trend_series": monthly_revenue["Gross_Amount"] - expenses["Amount"].sum(), "desc":"Earnings before Interest, Taxes, Depreciation, Amortization"},
    {"name": "Gross Margin", "value": gross_margin, "trend": None, "format":"percentage",
     "trend_series": ((monthly_revenue["Gross_Amount"] - expenses["Amount"].sum())/monthly_revenue["Gross_Amount"])*100,
     "desc":"(Revenue - COGS)/Revenue * 100", "thresholds":{"low":30, "high":70}},
    {"name": "Profit Margin", "value": profit_margin, "trend": None, "format":"percentage",
     "trend_series": ((monthly_revenue["Gross_Amount"] - expenses["Amount"].sum())/monthly_revenue["Gross_Amount"])*100,
     "desc":"Net Profit / Revenue * 100", "thresholds":{"low":5, "high":50}},
]

# Display KPI cards in 3 columns
for i in range(0, len(kpi_list), 3):
    cols = st.columns(3)
    for j, kpi in enumerate(kpi_list[i:i+3]):
        col = cols[j]
        color, arrow, alert_icon = get_color_arrow(kpi["value"], kpi.get("thresholds"))
        display_value = format_value(kpi["value"], kpi["format"])
        
        # KPI Card with gradient and unique key
        col.markdown(
            f"""
            <div style='background: linear-gradient(135deg,#f0f8ff,#d1e7dd); padding:25px; border-radius:15px; text-align:center; box-shadow:3px 3px 10px #aaa'>
                <h4>{kpi['name']} {alert_icon} ℹ️</h4>
                <h2 style='color:{color}'>{display_value} {arrow}</h2>
            </div>
            """, unsafe_allow_html=True
        )
        
        # Info expander with unique key
        with col.expander(f"Details - {kpi['name']}"):
            st.write(f"**What it is:** {kpi['desc']}")
            if kpi.get("trend") is not None:
                st.write(f"**Trend:** {arrow} {abs(kpi['trend']):.1f}% compared to previous month")
        
        # Mini sparkline chart with unique key
        fig = go.Figure(go.Scatter(
            y=kpi["trend_series"],
            mode='lines+markers',
            line=dict(color=color),
            marker=dict(size=4)
        ))
        fig.update_layout(height=80, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False)
        col.plotly_chart(fig, use_container_width=True, key=f"{kpi['name']}_sparkline")

# -----------------------------
# Full Revenue Trend Chart
# -----------------------------
st.subheader("Monthly Revenue Trend")
fig = go.Figure(go.Scatter(
    x=monthly_revenue["Invoice_Date"],
    y=monthly_revenue["Gross_Amount"],
    mode='lines+markers',
    line=dict(color='blue'),
    marker=dict(size=6)
))
fig.update_layout(title="Monthly Revenue", xaxis_title="Month", yaxis_title="Gross Amount (PKR)")
st.plotly_chart(fig, use_container_width=True, key="full_revenue_chart")
