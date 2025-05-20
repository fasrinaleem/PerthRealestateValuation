import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --- Use absolute base path ---
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")
models_dir = os.path.join(base_dir, "..", "models")

# Ensure output directories exist
os.makedirs(data_dir, exist_ok=True)
os.makedirs(models_dir, exist_ok=True)

# --- Load dataset ---
df = pd.read_csv(os.path.join(data_dir, "Perth_Realestate_Dataset.csv"))

# --- Feature Engineering ---
df["House Age"] = 2025 - df["BUILD_YEAR"]
features = [
    "House Age", "BEDROOMS", "BATHROOMS",
    "LAND_AREA", "FLOOR_AREA", "CBD_DIST", "NEAREST_STN_DIST"
]
target = "PRICE"
df = df[features + [target]].dropna()

X = df[features]
y = df[target]

# --- Scaling ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- Split ---
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# --- Define Models ---
models = {
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Linear Regression": LinearRegression(),
    "K-Nearest Neighbors": KNeighborsRegressor(n_neighbors=5),
    "XGBoost": XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
}

filename_map = {
    "Random Forest": "real_estate_model_rf.pkl",
    "Linear Regression": "real_estate_model_lr.pkl",
    "K-Nearest Neighbors": "real_estate_model_knn.pkl",
    "XGBoost": "real_estate_model_xgb.pkl"
}

# --- Train and Evaluate ---
results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    results.append({
        "Model": name,
        "MAE": mean_absolute_error(y_test, preds),
        "RMSE": np.sqrt(mean_squared_error(y_test, preds)),
        "R2": r2_score(y_test, preds)
    })

    joblib.dump(model, os.path.join(models_dir, filename_map[name]))

# --- Save Scaler and Metrics ---
joblib.dump(scaler, os.path.join(models_dir, "real_estate_scaler.pkl"))
pd.DataFrame(results).to_csv(os.path.join(data_dir, "model_metrics.csv"), index=False)

print("All models trained and saved successfully!")
