import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Certification Renewal Monitor")

file_path = "HACI_Business_Intelligence_Master.xlsx"

clients = pd.read_excel(file_path, sheet_name="Clients")

clients["Renewal_Date"] = pd.to_datetime(clients["Renewal_Date"])
today = datetime.today()

clients["Days_Left"] = (clients["Renewal_Date"] - today).dt.days

risk = clients[clients["Days_Left"] <= 90]

st.subheader("Renewals Due in 90 Days")
st.dataframe(risk[["Company_Name", "Renewal_Date", "Days_Left"]])