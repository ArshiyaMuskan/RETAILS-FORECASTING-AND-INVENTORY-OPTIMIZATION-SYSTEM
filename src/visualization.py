import matplotlib.pyplot as plt

def plot_sales(df):
    plt.figure()
    plt.plot(df['date'], df['sales'])
    plt.title("Sales Trend")
    plt.savefig("images/sales_trend.png")

def plot_forecast(actual, forecast):
    plt.figure()
    plt.plot(actual, label='Actual')
    plt.plot(forecast, label='Forecast')
    plt.legend()
    plt.savefig("images/forecast.png")