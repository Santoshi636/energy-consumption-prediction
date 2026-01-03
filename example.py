# energy_prediction.py
# Member 1: Data & Model
# Predicts energy consumption and saves predictions for dashboard

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import joblib

# --------------------------
# Step 1: Load Dataset
# --------------------------
# Replace 'energy.csv' with your dataset file
df = pd.read_csv("energy.csv")

print("Dataset Loaded. First 5 rows:")
print(df.head())

# --------------------------
# Step 2: Preprocess Data
# --------------------------
# Combine Date and Time into datetime
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

# Extract features
df['Hour'] = df['Datetime'].dt.hour
df['Day'] = df['Datetime'].dt.day
df['Month'] = df['Datetime'].dt.month
df['Weekday'] = df['Datetime'].dt.weekday

# Fill missing values in target
df['Global_active_power'].fillna(df['Global_active_power'].mean(), inplace=True)

# --------------------------
# Step 3: Prepare Features & Target
# --------------------------
X = df[['Hour', 'Day', 'Month', 'Weekday']]
y = df['Global_active_power']

# --------------------------
# Step 4: Train-Test Split
# --------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------------
# Step 5: Train Model
# --------------------------
# Option A: Linear Regression (simple)
# model = LinearRegression()

# Option B: Random Forest (more accurate)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --------------------------
# Step 6: Make Predictions
# --------------------------
y_pred = model.predict(X_test)

# --------------------------
# Step 7: Evaluate Model
# --------------------------
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5

print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

# --------------------------
# Step 8: Save Predictions for Dashboard
# --------------------------
predictions = pd.DataFrame({
    'Datetime': df['Datetime'].iloc[y_test.index],
    'Actual': y_test,
    'Predicted': y_pred
})
predictions.to_csv("predictions.csv", index=False)
print("Predictions saved to predictions.csv")

# --------------------------
# Step 9: Optional Visualization
# --------------------------
plt.figure(figsize=(12,5))
plt.plot(y_test.values[:100], label='Actual', marker='o')
plt.plot(y_pred[:100], label='Predicted', marker='x')
plt.xlabel("Sample Index")
plt.ylabel("Energy Consumption (kWh)")
plt.title("Energy Consumption Prediction (First 100 Samples)")
plt.legend()
plt.show()

# --------------------------
# Step 10: Save Model (Optional)
# --------------------------
joblib.dump(model, 'energy_model.pkl')
print("Trained model saved as energy_model.pkl")
