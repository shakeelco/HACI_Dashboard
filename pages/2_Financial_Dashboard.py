import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Financial Dashboard")

file_path = "HACI_Business_Intelligence_Master.xlsx"

revenue = pd.read_excel(file_path, sheet_name="Revenue")
expenses = pd.read_excel(file_path, sheet_name="Expenses")

# Revenue by Service
service_rev = revenue.groupby("Service_Category")["Gross_Amount"].sum().reset_index()

fig1 = px.bar(service_rev, x="Service_Category", y="Gross_Amount",
              title="Revenue by Service")
st.plotly_chart(fig1, use_container_width=True)

# Expense Breakdown
expense_cat = expenses.groupby("Category")["Amount"].sum().reset_index()

fig2 = px.pie(expense_cat, names="Category", values="Amount",
              title="Expense Breakdown")
st.plotly_chart(fig2, use_container_width=True)