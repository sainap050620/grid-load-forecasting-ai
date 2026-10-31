import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_and_save_model(export_path: str = "model.joblib"):
    np.random.seed(42)
    n = 2500
    
    hours = np.random.randint(0, 24, n)
    days = np.random.randint(0, 7, n)
    holidays = np.random.binomial(1, 0.05, n)
    temps = np.random.normal(12, 8, n)  # Average German climate temperature
    
    # German baseline electricity load formula (~45,000 MW base)
    loads = (
        45000 
        + 8000 * np.sin(hours / 24.0 * 2 * np.pi)
        - 3500 * (days >= 5) 
        - 350 * temps 
        - 2500 * holidays 
        + np.random.normal(0, 400, n)
    )
    
    X = pd.DataFrame({
        "temperature_celsius": temps,
        "hour_of_day": hours,
        "day_of_week": days,
        "is_holiday": holidays
    })
    y = loads

    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, export_path)
    print(f"Model saved successfully to {export_path}")

if __name__ == "__main__":
    train_and_save_model()