import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Executive Summary")

file_path = "HACI_Business_Intelligence_Master.xlsx"

revenue = pd.read_excel(file_path, sheet_name="Revenue")
expenses = pd.read_excel(file_path, sheet_name="Expenses")
clients = pd.read_excel(file_path, sheet_name="Clients")

# KPIs
total_revenue = revenue["Gross_Amount"].sum()
total_expenses = expenses["Amount"].sum()
net_profit = total_revenue - total_expenses
total_clients = clients["Client_ID"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"PKR {total_revenue:,.0f}")
col2.metric("Total Expenses", f"PKR {total_expenses:,.0f}")
col3.metric("Net Profit", f"PKR {net_profit:,.0f}")
col4.metric("Total Clients", total_clients)

# Monthly Revenue Trend
revenue["Invoice_Date"] = pd.to_datetime(revenue["Invoice_Date"])
monthly = revenue.groupby(revenue["Invoice_Date"].dt.to_period("M"))["Gross_Amount"].sum().reset_index()
monthly["Invoice_Date"] = monthly["Invoice_Date"].astype(str)

fig = px.line(monthly, x="Invoice_Date", y="Gross_Amount", title="Monthly Revenue Trend")
st.plotly_chart(fig, use_container_width=True)