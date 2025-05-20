import joblib
import os
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

MODEL_PATH = os.path.join("models", "real_estate_model.pkl")
SCALER_PATH = os.path.join("models", "real_estate_scaler.pkl")

# Load model and scaler
@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    return model

@st.cache_resource
def load_scaler():
    scaler = joblib.load(SCALER_PATH)
    return scaler

# Evaluate model performance
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2 Score": r2
    }
