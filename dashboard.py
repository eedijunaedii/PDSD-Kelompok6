import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide", page_title="Superstore Dashboard", page_icon="📊")

@st.cache_data
def load_data():
    df = pd.read_csv("sample-superstore.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

with st.sidebar:
    st.image("unikom.png", width=150)
    st.image("kelompok6.png", width=450)
    st.markdown("## Filter Data")  
    regions = df["Region"].unique()
    selected_regions = st.multiselect("Pilih Region", regions, default=regions)
    categories = df["Category"].unique()
    selected_categories = st.multiselect("Pilih Kategori", categories, default=categories)

filtered_df = df[(df["Region"].isin(selected_regions)) & (df["Category"].isin(selected_categories))]
filtered_df["Month"] = filtered_df["Order Date"].dt.to_period("M").astype(str)

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

st.title("📊 Superstore Dashboard")
st.markdown("### Analisis Penjualan dan Profit")

col1, col2 = st.columns(2)
col1.metric(label="Total Sales", value=f"${total_sales:,.2f}")
col2.metric(label="Total Profit", value=f"${total_profit:,.2f}")

# Visualisasi Total Penjualan berdasarkan Negara
st.subheader("Total Penjualan berdasarkan Negara")
sales_by_state = filtered_df.groupby("State")["Sales"].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(sales_by_state["State"], sales_by_state["Sales"], color="blue")
ax.set_title("Total Penjualan per Negara")
ax.set_xlabel("State")
ax.set_ylabel("Sales")
plt.xticks(rotation=90)
st.pyplot(fig)

# Visualisasi Profit vs Discount
st.subheader("Profit vs Discount")
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(filtered_df["Discount"], filtered_df["Profit"], c=filtered_df["Sales"], cmap="viridis")
ax.set_title("Profit vs Discount")
ax.set_xlabel("Discount")
ax.set_ylabel("Profit")
plt.colorbar(scatter, label="Sales")
st.pyplot(fig)

# Visualisasi Distribusi Penjualan per Kategori Produk
st.subheader("Distribusi Penjualan per Kategori Produk")
sales_by_category = filtered_df.groupby("Category")["Sales"].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(sales_by_category["Sales"], labels=sales_by_category["Category"], autopct="%1.1f%%", startangle=90)
ax.set_title("Distribusi Penjualan per Kategori")
st.pyplot(fig)

# Visualisasi Tren Penjualan Bulanan
st.subheader("Tren Penjualan Bulanan")
sales_trend = filtered_df.groupby("Month")["Sales"].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(sales_trend["Month"], sales_trend["Sales"], marker="o", linestyle="-", color="green")
ax.set_title("Tren Penjualan Bulanan")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
plt.xticks(rotation=90)
st.pyplot(fig)

# Tampilkan data sample
st.subheader("📊 Data Sample")
st.dataframe(filtered_df.head(10))

st.markdown("---")
st.markdown("📌 **Dashboard ini dikembangkan oleh Kelompok 6 | Universitas Komputer Indonesia (UNIKOM)**")
