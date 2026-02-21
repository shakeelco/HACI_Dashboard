import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Training Performance Dashboard")

file_path = "HACI_Business_Intelligence_Master.xlsx"

training = pd.read_excel(file_path, sheet_name="Training")

training["Profit"] = training["Revenue"] - training["Cost"]

fig = px.bar(training, x="Training_Type", y="Profit",
             title="Training Profitability")
st.plotly_chart(fig, use_container_width=True)