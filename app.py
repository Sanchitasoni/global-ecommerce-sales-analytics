import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Global E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------
data = pd.read_csv("global_ecommerce_sales.csv")

# Convert date
data["Order_Date"] = pd.to_datetime(data["Order_Date"], errors="coerce")

# -----------------------------
# Title
# -----------------------------
st.title("🛒 Global E-Commerce Sales & Customer Analytics")
st.write("Interactive dashboard for analyzing sales, profit, customers and products.")

# -----------------------------
# Data Cleaning
# -----------------------------
missing_values = data.isnull().sum().sum()
duplicate_rows = data.duplicated().sum()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(data["Region"].dropna().unique()),
    default=sorted(data["Region"].dropna().unique())
)

categories = st.sidebar.multiselect(
    "Select Product Category",
    options=sorted(data["Product_Category"].dropna().unique()),
    default=sorted(data["Product_Category"].dropna().unique())
)

segments = st.sidebar.multiselect(
    "Select Customer Segment",
    options=sorted(data["Customer_Segment"].dropna().unique()),
    default=sorted(data["Customer_Segment"].dropna().unique())
)

filtered_data = data[
    (data["Region"].isin(regions)) &
    (data["Product_Category"].isin(categories)) &
    (data["Customer_Segment"].isin(segments))
]

# -----------------------------
# KPI Section
# -----------------------------
total_sales = filtered_data["Total_Sales"].sum()
total_profit = filtered_data["Profit"].sum()
total_orders = filtered_data["Order_ID"].nunique()
average_order = filtered_data["Total_Sales"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Average Order Value", f"${average_order:,.2f}")

st.divider()

# -----------------------------
# Sales by Region
# -----------------------------
st.subheader("🌍 Sales by Region")

region_sales = (
    filtered_data.groupby("Region")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots()
region_sales.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Region")
ax1.set_ylabel("Total Sales")
ax1.set_title("Sales by Region")
plt.xticks(rotation=30)
plt.tight_layout()
st.pyplot(fig1)

# -----------------------------
# Sales by Product Category
# -----------------------------
st.subheader("📦 Sales by Product Category")

category_sales = (
    filtered_data.groupby("Product_Category")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots()
category_sales.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Product Category")
ax2.set_ylabel("Total Sales")
ax2.set_title("Sales by Product Category")
plt.xticks(rotation=30)
plt.tight_layout()
st.pyplot(fig2)

# -----------------------------
# Profit by Category
# -----------------------------
st.subheader("💰 Profit by Product Category")

category_profit = (
    filtered_data.groupby("Product_Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

fig3, ax3 = plt.subplots()
category_profit.plot(kind="bar", ax=ax3)
ax3.set_xlabel("Product Category")
ax3.set_ylabel("Profit")
ax3.set_title("Profit by Product Category")
plt.xticks(rotation=30)
plt.tight_layout()
st.pyplot(fig3)

# -----------------------------
# Customer Segment Analysis
# -----------------------------
st.subheader("👥 Sales by Customer Segment")

segment_sales = (
    filtered_data.groupby("Customer_Segment")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
)

fig4, ax4 = plt.subplots()
segment_sales.plot(kind="bar", ax=ax4)
ax4.set_xlabel("Customer Segment")
ax4.set_ylabel("Total Sales")
ax4.set_title("Sales by Customer Segment")
plt.xticks(rotation=20)
plt.tight_layout()
st.pyplot(fig4)

# -----------------------------
# Monthly Sales Trend
# -----------------------------
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_data
    .set_index("Order_Date")
    .resample("ME")["Total_Sales"]
    .sum()
)

fig5, ax5 = plt.subplots()
monthly_sales.plot(kind="line", marker="o", ax=ax5)
ax5.set_xlabel("Month")
ax5.set_ylabel("Total Sales")
ax5.set_title("Monthly Sales Trend")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig5)

# -----------------------------
# Top Products
# -----------------------------
st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_data.groupby("Product_Name")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig6, ax6 = plt.subplots()
top_products.sort_values().plot(kind="barh", ax=ax6)
ax6.set_xlabel("Total Sales")
ax6.set_ylabel("Product")
ax6.set_title("Top 10 Products")
plt.tight_layout()
st.pyplot(fig6)

# -----------------------------
# Data Quality
# -----------------------------
st.subheader("🔍 Data Quality")

col1, col2 = st.columns(2)

col1.metric("Missing Values", missing_values)
col2.metric("Duplicate Rows", duplicate_rows)

st.success("Data analysis completed successfully.")

# -----------------------------
# Business Insights
# -----------------------------
st.subheader("💡 Business Insights")

if not region_sales.empty:
    best_region = region_sales.idxmax()

if not category_sales.empty:
    best_category = category_sales.idxmax()

if not top_products.empty:
    best_product = top_products.idxmax()

st.write(f"• The highest-sales region in the selected data is **{best_region}**.")
st.write(f"• The highest-sales product category is **{best_category}**.")
st.write(f"• The top-selling product is **{best_product}**.")
st.write("• Sales and profit can be monitored by region, category and customer segment.")
st.write("• Monthly trends can help identify changes in business performance.")