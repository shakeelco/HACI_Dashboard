import streamlit as st
import pandas as pd
import plotly.express as px
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
def color_arrow(value, is_percentage=False):
    if value > 0:
        return "green", "⬆️"
    elif value < 0:
        return "red", "⬇️"
    else:
        return "orange", "➖"

def format_value(value, fmt="currency"):
    if fmt == "currency":
        return f"PKR {value:,.0f}"
    elif fmt == "percentage":
        return f"{value:.1f}%"
    else:
        return str(value)

# -----------------------------
# KPI Cards with Mini Charts
# -----------------------------
st.subheader("Key Performance Indicators")

kpi_list = [
    {
        "name": "Total Revenue",
        "value": total_revenue,
        "trend": latest_growth,
        "format": "currency",
        "trend_series": monthly_revenue["Gross_Amount"],
        "desc": "Total Revenue is the sum of all income from sales."
    },
    {
        "name": "Total Expenses",
        "value": total_expenses,
        "trend": None,
        "format": "currency",
        "trend_series": expenses["Amount"],
        "desc": "Total Expenses includes all operational costs such as salaries, rent, utilities."
    },
    {
        "name": "Net Profit",
        "value": net_profit,
        "trend": net_profit,
        "format": "currency",
        "trend_series": monthly_revenue["Gross_Amount"] - expenses["Amount"].sum(),
        "desc": "Net Profit = Total Revenue - Total Expenses."
    },
    {
        "name": "Total Clients",
        "value": total_clients,
        "trend": None,
        "format": "number",
        "trend_series": clients["Client_ID"].value_counts().sort_index(),
        "desc": "Total Clients is the count of unique customers."
    },
    {
        "name": "EBITDA",
        "value": ebitda,
        "trend": None,
        "format": "currency",
        "trend_series": monthly_revenue["Gross_Amount"] - expenses["Amount"].sum(),
        "desc": "EBITDA = Net Profit + Depreciation + Interest + Taxes."
    },
    {
        "name": "Gross Margin",
        "value": gross_margin,
        "trend": None,
        "format": "percentage",
        "trend_series": ((monthly_revenue["Gross_Amount"] - expenses["Amount"].sum())/monthly_revenue["Gross_Amount"])*100,
        "desc": "Gross Margin = (Revenue - COGS)/Revenue * 100."
    },
    {
        "name": "Profit Margin",
        "value": profit_margin,
        "trend": None,
        "format": "percentage",
        "trend_series": ((monthly_revenue["Gross_Amount"] - expenses["Amount"].sum())/monthly_revenue["Gross_Amount"])*100,
        "desc": "Profit Margin = Net Profit / Revenue * 100."
    },
]

# Display KPI cards in 3 columns
for i in range(0, len(kpi_list), 3):
    cols = st.columns(3)
    for j, kpi in enumerate(kpi_list[i:i+3]):
        col = cols[j]
        color, arrow = color_arrow(kpi["trend"]) if kpi["trend"] is not None else ("blue", "")
        display_value = format_value(kpi["value"], kpi["format"])

        # KPI Card with HTML
        col.markdown(
            f"""
            <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center; box-shadow:2px 2px 5px #aaa'>
                <h4>{kpi['name']} ℹ️</h4>
                <h2 style='color:{color}'>{display_value} {arrow}</h2>
            </div>
            """, unsafe_allow_html=True
        )

        # Info expander for details
        with col.expander("Details"):
            st.write(f"**What it is:** {kpi['desc']}")
            if kpi["trend"] is not None:
                st.write(f"**Trend:** {arrow} {abs(kpi['trend']):.1f}% compared to previous month")

        # Optional mini sparkline chart
        fig = go.Figure(go.Scatter(
            y=kpi["trend_series"],
            mode='lines+markers',
            line=dict(color=color),
            marker=dict(size=4)
        ))
        fig.update_layout(height=80, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False)
        col.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Revenue Trend Chart
# -----------------------------
st.subheader("Monthly Revenue Trend")
fig = px.line(monthly_revenue, x="Invoice_Date", y="Gross_Amount", title="Monthly Revenue", markers=True)
st.plotly_chart(fig, use_container_width=True)
