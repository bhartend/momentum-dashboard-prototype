import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Title
st.title("📊 Momentum Dashboard - NSE Dummy Data")

# Load dummy data (replace this section with live NSE data fetching later)
@st.cache_data
def load_data():
    data = pd.read_csv("dummy_nse_data.csv")
    return data

data = load_data()

# Sidebar for date filter
date_selected = st.sidebar.selectbox("Select Date", sorted(data['Date'].unique(), reverse=True))
data_date = data[data['Date'] == date_selected]

# Dashboard 1: Sector Summary
st.subheader(f"📈 Sector Relative Strength vs Benchmark on {date_selected}")

sector_summary = data_date.groupby('Sector').agg({
    'Sector_CRSI_vs_Benchmark': 'first',
    'Sector_PercentileCSR_vs_Benchmark': 'first'
}).reset_index()

fig, ax = plt.subplots(figsize=(8, len(sector_summary) * 0.5))
sns.heatmap(sector_summary[['Sector_CRSI_vs_Benchmark', 'Sector_PercentileCSR_vs_Benchmark']], 
            annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax,
            yticklabels=sector_summary['Sector'])

plt.title("Sector Performance Heatmap")
st.pyplot(fig)

# Select Sector
selected_sector = st.selectbox("Select Sector to View Constituents", sector_summary['Sector'])

# Dashboard 2: Stock-Level Detail
st.subheader(f"📊 Stock Performance in {selected_sector} on {date_selected}")

sector_stocks = data_date[data_date['Sector'] == selected_sector][[
    'Stock', 'CRSI_vs_Benchmark', 'PercentileCSR_vs_Benchmark', 'CRSI_vs_Sector', 
    'PercentileCSR_vs_Sector', 'Self_Performance']]

fig2, ax2 = plt.subplots(figsize=(10, len(sector_stocks) * 0.5))
sns.heatmap(sector_stocks.drop('Stock', axis=1), 
            annot=True, fmt=".2f", cmap="YlGnBu", linewidths=0.5, ax=ax2,
            yticklabels=sector_stocks['Stock'])

plt.title(f"Stock Relative Strength and Percentiles in {selected_sector}")
st.pyplot(fig2)

# Auto-refresh info
st.caption("Data auto-updates daily at 10 PM IST (Dummy data in this prototype)")
