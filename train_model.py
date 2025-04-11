import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

# Load dataset
df = pd.read_csv("Perth_Realestate_Dataset.csv")

# Feature engineering
df["House Age"] = 2025 - df["BUILD_YEAR"]

# Define features to use
features = [
    "House Age", "BEDROOMS", "BATHROOMS",
    "LAND_AREA", "FLOOR_AREA", "CBD_DIST", "NEAREST_STN_DIST"
]
target = "PRICE"

# Drop rows with missing values in selected features
df = df[features + [target]].dropna()

# Define X and y
X = df[features]
y = df[target]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and scaler
joblib.dump(model, "real_estate_model.pkl")
joblib.dump(scaler, "real_estate_scaler.pkl")

print("✅ New Perth model and scaler saved successfully!")
