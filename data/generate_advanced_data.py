import pandas as pd
import numpy as np

np.random.seed(42)

dates = pd.date_range(start="2023-01-01", periods=365)

stores = ["Store_A", "Store_B"]
categories = ["Electronics", "Groceries"]
products = {
    "Electronics": ["Laptop", "Phone"],
    "Groceries": ["Milk", "Bread"]
}

data = []

for store in stores:
    for category in categories:
        for product in products[category]:
            base = np.random.randint(50, 150)

            for i, date in enumerate(dates):
                sales = base + 10*np.sin(i/10) + np.random.randint(-5, 5)
                data.append([date, store, category, product, max(0, int(sales))])

df = pd.DataFrame(data, columns=["date", "store", "category", "product", "sales"])

df.to_csv("data/retail_sales.csv", index=False)
print("Dataset created!")