from statsmodels.tsa.arima.model import ARIMA

def train_arima(series):
    model = ARIMA(series, order=(5,1,0))
    model_fit = model.fit()
    return model_fit

def forecast(model, steps=30):
    forecast = model.forecast(steps=steps)
    return forecast