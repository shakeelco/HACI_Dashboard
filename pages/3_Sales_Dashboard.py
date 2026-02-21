import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Sales Dashboard")

file_path = "HACI_Business_Intelligence_Master.xlsx"

clients = pd.read_excel(file_path, sheet_name="Clients")

# Clients by City
city_data = clients.groupby("City")["Client_ID"].count().reset_index()

fig = px.bar(city_data, x="City", y="Client_ID",
             title="Clients by City")
st.plotly_chart(fig, use_container_width=True)

# Clients by Industry
industry_data = clients.groupby("Industry")["Client_ID"].count().reset_index()

fig2 = px.bar(industry_data, x="Industry", y="Client_ID",
              title="Clients by Industry")
st.plotly_chart(fig2, use_container_width=True)