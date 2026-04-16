import numpy as np

def calculate_safety_stock(std_dev, lead_time, service_level=1.65):
    return service_level * std_dev * np.sqrt(lead_time)

def reorder_point(avg_demand, lead_time, safety_stock):
    return (avg_demand * lead_time) + safety_stock