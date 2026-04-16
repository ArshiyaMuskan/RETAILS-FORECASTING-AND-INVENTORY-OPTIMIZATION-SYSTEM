import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    return df

def preprocess(df):
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # Fill missing values
    df=df.ffill()

    return df