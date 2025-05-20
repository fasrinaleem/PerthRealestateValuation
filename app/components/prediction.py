import streamlit as st
import numpy as np
import joblib
import pandas as pd
import os

# Load styles
with open("app/style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Load models ---
@st.cache_resource
def load_models():
    base_path = "models"
    return {
        "Random Forest": joblib.load(os.path.join(base_path, "real_estate_model_rf.pkl")),
        "Linear Regression": joblib.load(os.path.join(base_path, "real_estate_model_lr.pkl")),
        "XGBoost": joblib.load(os.path.join(base_path, "real_estate_model_xgb.pkl")),
        "K-Nearest Neighbors": joblib.load(os.path.join(base_path, "real_estate_model_knn.pkl"))
    }

@st.cache_resource
def load_scaler():
    return joblib.load("models/real_estate_scaler.pkl")

@st.cache_data
def load_model_metrics():
    return pd.read_csv("data/model_metrics.csv")

def render():
    models = load_models()
    scaler = load_scaler()
    metrics_df = load_model_metrics()

    st.markdown("""
    <div class="hero">
        <h1>🔮 Predict House Price</h1>
        <p>Fill in the property details and choose a model to get an estimated price.</p>
    </div>
    """, unsafe_allow_html=True)

    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []

    model_choice = st.selectbox("Choose Prediction Model", options=list(models.keys()))

    st.markdown("""
    <div style='background-color: #1e1e2f; padding: 1.5rem; border-radius: 15px; margin-top: 1rem;'>
    """, unsafe_allow_html=True)

    with st.form("prediction_form"):
        st.markdown("### 📋 Property Details")
        col1, col2 = st.columns(2)
        with col1:
            bedrooms = st.slider("Bedrooms", 1, 10, 3, help="Number of bedrooms")
            bathrooms = st.slider("Bathrooms", 1, 5, 2, help="Number of bathrooms")
            land_area = st.number_input("Land Area (sqm)", 50, 2000, 500, help="Total land size")
        with col2:
            floor_area = st.number_input("Floor Area (sqm)", 30, 1000, 150, help="Indoor living space")
            house_age = st.slider("House Age (yrs)", 0, 150, 30, help="Years since construction")
            distance_to_mrt = st.number_input("Distance to MRT (m)", 0, 5000, 500, help="Walking distance to MRT")

        st.caption("💡 Newer homes & MRT proximity typically raise prices.")
        submitted = st.form_submit_button("🚀 Predict Price")

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        input_df = pd.DataFrame([[
            house_age, bedrooms, bathrooms, land_area, floor_area, 0, distance_to_mrt
        ]], columns=["House Age", "BEDROOMS", "BATHROOMS", "LAND_AREA", "FLOOR_AREA", "CBD_DIST", "NEAREST_STN_DIST"])

        scaled_input = scaler.transform(input_df)
        prediction = models[model_choice].predict(scaled_input)[0]

        st.session_state.prediction_history.append({
            "model": model_choice,
            "prediction": int(prediction),
            "inputs": {
                "Bedrooms": bedrooms,
                "Bathrooms": bathrooms,
                "Land Area": land_area,
                "Floor Area": floor_area,
                "House Age": house_age,
                "Distance to MRT": distance_to_mrt
            }
        })

        st.markdown(f"""
        <div style='padding: 1.5rem; border-radius: 12px; background: linear-gradient(to right, #4facfe, #00f2fe); text-align: center; color: white; font-size: 1.6rem; font-weight: bold;'>
            🏷️ Estimated Price using {model_choice}: ${int(prediction):,}
        </div>
        """, unsafe_allow_html=True)

        try:
            r2 = metrics_df[metrics_df["Model"] == model_choice]["R2"].values[0]
            st.info(f"📊 {model_choice} R² Score: {r2:.2f}")
        except:
            st.warning("ℹ️ No metrics available for this model.")

    if st.session_state.prediction_history:
        st.markdown("### 📈 Prediction Trend")
        df_history = pd.DataFrame(st.session_state.prediction_history)
        st.line_chart(df_history["prediction"])

        st.markdown("### 🗂️ Prediction History")
        for idx, item in enumerate(reversed(st.session_state.prediction_history), 1):
            with st.expander(f"📌 Prediction #{idx} — 🧠 {item['model']} → 💰 ${item['prediction']:,}"):
                st.json(item['inputs'])
