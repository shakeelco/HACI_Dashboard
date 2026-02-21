import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Marketing Dashboard")

file_path = "HACI_Business_Intelligence_Master.xlsx"

marketing = pd.read_excel(file_path, sheet_name="Marketing")

# Channel Performance
channel = marketing.groupby("Channel")[["Spend", "Leads", "Conversions", "Revenue_Generated"]].sum().reset_index()

channel["CPL"] = channel["Spend"] / channel["Leads"]
channel["CPA"] = channel["Spend"] / channel["Conversions"]
channel["ROAS"] = channel["Revenue_Generated"] / channel["Spend"]

st.dataframe(channel)

fig = px.bar(channel, x="Channel", y="Revenue_Generated",
             title="Revenue by Marketing Channel")
st.plotly_chart(fig, use_container_width=True)