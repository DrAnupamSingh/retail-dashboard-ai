
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load dataset
df = pd.read_excel("DATASET FOR ANUPAM.xlsx")
df['ons_area'] = df['ons_area'].str.title()
df['basket_id'] = df['rdp_shop_id'].astype(str) + "_" + df['year_of_date'].astype(str) + "_" + df['month_of_year'].astype(str)
df['avg_price_per_unit'] = df['category_sales_value'] / df['category_units']
df['estimated_basket_count'] = df['category_sales_value'] / df['basket_spend']

# Sidebar
st.sidebar.title("Filter")
region_filter = st.sidebar.selectbox("Select Region", df['region'].unique())
filtered_df = df[df['region'] == region_filter]

st.title("🧠 Retail Category Insights Dashboard")
st.markdown("**Interactive dashboard with AI-powered recommendations for retail growth.**")

# 1. Urban vs. Constrained Dwellers
st.subheader("📊 1. Urban vs. Constrained City Dwellers - Category Sales")
area_df = df[df['ons_area'].isin(['Urbanites', 'Constrained City Dwellers'])].groupby(['ons_area', 'category_level1'])['category_sales_value'].mean().reset_index()
fig1 = px.bar(area_df, x='category_level1', y='category_sales_value', color='ons_area', barmode='group', title='Urbanites vs Constrained City Dwellers')
st.plotly_chart(fig1)
st.markdown("**Client Insight:** Urbanites tend to spend more overall across most categories. Constrained dwellers spend less, suggesting a need for price-sensitive product targeting or budget promotions in those areas.")

# 2. Heatmap: Category Sales by Region
st.subheader("🌍 2. Regional Category Performance (Heatmap)")
region_df = df.groupby(['region', 'category_level1'])['category_sales_value'].mean().reset_index()
heatmap_data = region_df.pivot(index='region', columns='category_level1', values='category_sales_value')
st.dataframe(heatmap_data.style.background_gradient(cmap='YlGnBu'))
st.markdown("**Client Insight:** This heatmap shows which categories are performing best in which regions. Focus promotional campaigns and inventory allocation accordingly.")

# 3. Top 3 Categories per Shop
st.subheader("🏪 3. Top 3 Categories per Shop (Recommended Focus)")
top_cats = df.groupby(['rdp_shop_id', 'category_level1'])['category_sales_value'].sum().reset_index()
top_3 = top_cats.sort_values(['rdp_shop_id', 'category_sales_value'], ascending=[True, False]).groupby('rdp_shop_id').head(3)
st.dataframe(top_3)
st.markdown("**Client Insight:** These are the best-performing categories for each shop. Keep them well-stocked and consider bundling them with slower-moving items.")

# 4. Underperforming Categories
st.subheader("📉 4. Underperforming Categories Compared to Regional Average")
shop_region = df.groupby(['rdp_shop_id', 'category_level1', 'region'])['category_sales_value'].mean().reset_index()
region_avg = df.groupby(['category_level1', 'region'])['category_sales_value'].mean().reset_index().rename(columns={'category_sales_value': 'region_avg'})
merged = shop_region.merge(region_avg, on=['category_level1', 'region'])
merged['performance_gap'] = merged['category_sales_value'] - merged['region_avg']
underperf = merged[merged['performance_gap'] < 0].sort_values('performance_gap')
st.dataframe(underperf[['rdp_shop_id', 'region', 'category_level1', 'category_sales_value', 'region_avg', 'performance_gap']])
st.markdown("**Client Insight:** These categories are selling below the regional average in specific shops. Investigate pricing, placement, or consider local promotions.")

# 5. Seasonal Trends
st.subheader("📆 5. Seasonal Trends Across Categories")
seasonal = df.groupby(['month_of_year', 'category_level1'])['category_sales_value'].mean().reset_index()
fig2 = px.line(seasonal, x='month_of_year', y='category_sales_value', color='category_level1', title='Monthly Category Sales Trends')
st.plotly_chart(fig2)
st.markdown("**Client Insight:** Use this to plan seasonal stock. For example, Drinks and Frozen may spike in summer—plan bulk purchasing or deals accordingly.")

# Optional: Unit Pricing and Basket Count
st.subheader("📊 Bonus: Price Per Unit and Basket Count Insights")
pricing_stats = df[['category_level1', 'avg_price_per_unit', 'estimated_basket_count']].groupby('category_level1').mean().reset_index()
st.dataframe(pricing_stats)
st.markdown("**Client Insight:** Use average unit price and estimated basket count to evaluate category-level pricing strategy and volume dynamics.")

# Footer
st.markdown("---")
st.markdown("📈 Powered by your retail data | 🚀 Designed for strategic retail growth | Made with Streamlit")
