import streamlit as st
import subprocess
import os
from datetime import datetime

# --- Required model files
model_files = [
    "real_estate_model_rf.pkl",
    "real_estate_model_lr.pkl",
    "real_estate_model_xgb.pkl",
    "real_estate_model_knn.pkl",
    "real_estate_scaler.pkl"
]

# --- Paths
MODELS_DIR = "models"
TIMESTAMP_FILE = os.path.join(MODELS_DIR, "last_trained.txt")

def are_models_trained():
    return all(os.path.exists(os.path.join(MODELS_DIR, f)) for f in model_files)

def get_last_trained_time():
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "r") as f:
            return f.read().strip()
    return None

def update_last_trained_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(now)
    return now

def run_training_script():
    return subprocess.run(["python3", "scripts/train_model.py"], capture_output=True, text=True)

def render():
    st.markdown("""
    <div class="hero">
        <h1>🛠 Train Models</h1>
        <p>This page allows you to retrain all AI models using the latest dataset.</p>
    </div>
    """, unsafe_allow_html=True)

    # ✅ Session flag override for clean success message
    if st.session_state.get("models_just_trained"):
        st.session_state.models_just_trained = False
        last_trained = update_last_trained_time()
        st.success(f"🎉 All models have been trained and are ready to use! (Last trained: {last_trained})")
        st.balloons()
        return

    # 🕒 Show last trained time (if exists)
    if are_models_trained():
        st.success("✅ All models are currently trained and ready to use.")
        last_time = get_last_trained_time()
        if last_time:
            st.markdown(f"🕒 **Last Trained:** `{last_time}`")
        st.markdown("💡 You can retrain them anytime using the button below.")
    else:
        st.warning("⚠️ Models are missing or outdated. Please train them before using the predictor.")

    # 🚀 Button to train models
    if st.button("🚀 Train Models Now"):
        with st.spinner("🔄 Training models... please wait..."):
            result = run_training_script()

        if result.returncode == 0:
            st.session_state.models_just_trained = True
            st.rerun()
        else:
            st.error("❌ Training failed. See error output below.")
            st.code(result.stderr)
