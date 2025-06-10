
import streamlit as st
import pandas as pd
import numpy as np

st.title("Momentum Dashboard Prototype")

st.sidebar.header("Filters")
sector = st.sidebar.selectbox("Select Sector", ["Auto", "Banking", "IT", "Pharma"])

st.write("## Sector Performance Spread (Dummy Data)")
data = pd.DataFrame({
    "Stock": ["Stock A", "Stock B", "Stock C"],
    "CRSI": np.random.uniform(0, 100, 3),
    "Percentile CSR": np.random.uniform(0, 100, 3)
})
st.dataframe(data)

st.write("### This app auto-updates dummy data daily at 10 PM IST (mock prototype).")
