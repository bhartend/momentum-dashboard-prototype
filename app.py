import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Momentum Dashboard", layout="wide")

# Dummy data generation
def generate_dummy_data():
    sectors = ['Auto', 'Banks', 'IT', 'FMCG', 'Energy']
    stocks = [f'Stock_{i}' for i in range(1, 26)]
    data = []

    for stock in stocks:
        sector = np.random.choice(sectors)
        crsi_benchmark = np.random.uniform(-5, 5)
        pct_rank_benchmark = np.random.uniform(0, 100)
        crsi_sector = np.random.uniform(-5, 5)
        pct_rank_sector = np.random.uniform(0, 100)
        data.append([stock, sector, crsi_benchmark, pct_rank_benchmark, crsi_sector, pct_rank_sector])

    df = pd.DataFrame(data, columns=['Stock', 'Sector', 'CRSI_vs_Benchmark', 'Percentile_vs_Benchmark', 'CRSI_vs_Sector', 'Percentile_vs_Sector'])
    return df

# Load dummy data
df = generate_dummy_data()

# Sector summary
def sector_summary(df):
    sector_df = df.groupby('Sector').agg(
        Sector_CRSI=('CRSI_vs_Benchmark', 'mean'),
        Sector_Percentile=('Percentile_vs_Benchmark', 'mean')
    ).reset_index()
    return sector_df

sector_df = sector_summary(df)

# First Dashboard: Sector Overview
st.title("📊 Momentum Dashboard - Sector Overview")
st.write("**Relative Strength of Sectors vs Benchmark**")

# Heatmap-like table display
sector_df_sorted = sector_df.sort_values(by='Sector_CRSI', ascending=False)

fig, ax = plt.subplots(figsize=(8, 3))
sns.heatmap(
    sector_df_sorted[['Sector_CRSI', 'Sector_Percentile']].T,
    annot=sector_df_sorted[['Sector_CRSI', 'Sector_Percentile']].T,
    cmap='coolwarm', cbar=False, linewidths=0.5, fmt=".2f",
    xticklabels=sector_df_sorted['Sector']
)
plt.yticks(rotation=0)
st.pyplot(fig)

# Sector selection
selected_sector = st.selectbox("Select a Sector to view Constituents", sector_df_sorted['Sector'])
st.write(f"**Showing stocks from sector:** {selected_sector}")

# Second Dashboard: Stock level inside selected sector
sector_stocks = df[df['Sector'] == selected_sector]

fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.heatmap(
    sector_stocks[['CRSI_vs_Benchmark', 'Percentile_vs_Benchmark', 'CRSI_vs_Sector', 'Percentile_vs_Sector']].T,
    annot=sector_stocks[['CRSI_vs_Benchmark', 'Percentile_vs_Benchmark', 'CRSI_vs_Sector', 'Percentile_vs_Sector']].T,
    cmap='coolwarm', cbar=False, linewidths=0.5, fmt=".2f",
    xticklabels=sector_stocks['Stock']
)
plt.yticks(rotation=0)
st.pyplot(fig2)

# Note
st.info("This is a prototype dashboard using dummy NSE data. The full version will auto-update daily at 10 PM with live data.")
