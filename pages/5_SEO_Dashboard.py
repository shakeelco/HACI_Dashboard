import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SEO Performance Dashboard")

file_path = "HACI_Business_Intelligence_Master.xlsx"

seo = pd.read_excel(file_path, sheet_name="SEO")

fig1 = px.line(seo, x="Month", y="Website_Visitors",
               title="Website Visitors Trend")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(seo, x="Month", y="Organic_Traffic",
               title="Organic Traffic Growth")
st.plotly_chart(fig2, use_container_width=True)