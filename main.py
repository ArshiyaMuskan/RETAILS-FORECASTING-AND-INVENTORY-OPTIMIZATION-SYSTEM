from src.data_preprocessing import load_data, preprocess
from src.feature_engineering import create_features
from src.forecasting import train_arima, forecast
from src.inventory import calculate_safety_stock, reorder_point
from src.visualization import plot_sales, plot_forecast

# Load data
df = load_data("data/retail_sales.csv")
df = preprocess(df)
df = create_features(df)

# Forecast
model = train_arima(df['sales'])
future = forecast(model)

# Inventory
avg_demand = df['sales'].mean()
std_dev = df['sales'].std()
lead_time = 7

ss = calculate_safety_stock(std_dev, lead_time)
rop = reorder_point(avg_demand, lead_time, ss)

print("Safety Stock:", ss)
print("Reorder Point:", rop)

# Visualization
plot_sales(df)
plot_forecast(df['sales'], future)