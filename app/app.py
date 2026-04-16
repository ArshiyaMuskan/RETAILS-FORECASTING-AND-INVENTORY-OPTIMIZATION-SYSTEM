import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

st.title("🛒 Retail Sales Forecasting & Inventory Optimization")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/retail_sales.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

store = st.sidebar.selectbox("Select Store", df['store'].unique())
category = st.sidebar.selectbox("Select Category", df[df['store']==store]['category'].unique())
product = st.sidebar.selectbox("Select Product", df[(df['store']==store) & (df['category']==category)]['product'].unique())

forecast_days = st.sidebar.slider("Forecast Days", 7, 60, 30)
lead_time = st.sidebar.slider("Lead Time", 1, 30, 7)

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df[
    (df['store'] == store) &
    (df['category'] == category) &
    (df['product'] == product)
]

filtered_df = filtered_df.sort_values("date")

# -----------------------------
# KPI CARDS
# -----------------------------
st.subheader("📊 Key Metrics")

avg_sales = filtered_df['sales'].mean()
max_sales = filtered_df['sales'].max()
min_sales = filtered_df['sales'].min()

col1, col2, col3 = st.columns(3)

col1.metric("Average Sales", round(avg_sales, 2))
col2.metric("Max Sales", max_sales)
col3.metric("Min Sales", min_sales)

# -----------------------------
# SALES TREND
# -----------------------------
st.subheader("📈 Sales Trend")

fig1, ax1 = plt.subplots()
ax1.plot(filtered_df['date'], filtered_df['sales'])
ax1.set_title(f"{product} Sales Trend")
st.pyplot(fig1)

# -----------------------------
# FORECASTING
# -----------------------------
st.subheader("🔮 Forecast")

series = filtered_df['sales']

try:
    model = ARIMA(series, order=(3,1,1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_days)
except:
    st.error("Forecasting failed. Try different data selection.")
    forecast = []

fig2, ax2 = plt.subplots()
ax2.plot(series.values, label="Actual")

if len(forecast) > 0:
    ax2.plot(range(len(series), len(series)+forecast_days), forecast, label="Forecast")

ax2.legend()
st.pyplot(fig2)

# -----------------------------
# INVENTORY OPTIMIZATION
# -----------------------------
st.subheader("📦 Inventory Optimization")

std_dev = filtered_df['sales'].std()

service_level = 1.65
safety_stock = service_level * std_dev * np.sqrt(lead_time)
reorder_point = (avg_sales * lead_time) + safety_stock

col4, col5 = st.columns(2)
col4.metric("Safety Stock", round(safety_stock, 2))
col5.metric("Reorder Point", round(reorder_point, 2))

# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------
st.subheader("💡 Insights")

if forecast is not None and len(forecast) > 0:
    if forecast.mean() > avg_sales:
        st.success("📈 Demand likely to increase → Increase stock")
    else:
        st.warning("📉 Demand may decrease → Reduce stock")

# -----------------------------
# DOWNLOAD
# -----------------------------
if len(forecast) > 0:
    forecast_df = pd.DataFrame({"forecast": forecast})
    st.download_button("📥 Download Forecast", forecast_df.to_csv(index=False), "forecast.csv")