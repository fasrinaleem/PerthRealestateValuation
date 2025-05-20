import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_metrics():
    path = "data/model_metrics.csv"
    return pd.read_csv(path)

def get_last_trained_time():
    timestamp_file = os.path.join("models", "last_trained.txt")
    if os.path.exists(timestamp_file):
        with open(timestamp_file, "r") as f:
            return f.read().strip()
    return None

def render():
    st.markdown("""
        <div class="hero">
            <h1>📊 Model Comparison</h1>
            <p>Evaluate and visualize model performance with your preferred chart type.</p>
        </div>
    """, unsafe_allow_html=True)

    last_trained = get_last_trained_time()
    if last_trained:
        st.info(f"🕒 **Models last trained on:** `{last_trained}`")

    try:
        metrics_df = load_metrics()

        # --- Show Metrics Table ---
        st.markdown("### 📋 Performance Table")
        st.dataframe(metrics_df.style.format({
            "MAE": "{:.2f}",
            "RMSE": "{:.2f}",
            "R2": "{:.3f}"
        }), use_container_width=True)

        # --- Chart Selector ---
        st.markdown("### 📊 Visual Comparison")
        chart_type = st.selectbox("Select Chart Type", options=["Grouped Bar", "Line", "Scatter"])

        melted = metrics_df.melt(id_vars="Model", var_name="Metric", value_name="Score")

        if chart_type == "Grouped Bar":
            fig = px.bar(
                melted, x="Model", y="Score", color="Metric",
                barmode="group", text_auto=".2f",
                title="Grouped Comparison of Model Metrics"
            )

        elif chart_type == "Line":
            fig = px.line(
                melted, x="Model", y="Score", color="Metric", markers=True,
                title="Line Chart of Model Metrics"
            )

        elif chart_type == "Scatter":
            fig = px.scatter(
                melted, x="Model", y="Score", color="Metric", size="Score", hover_data=["Metric"],
                title="Scatter Plot of Model Metrics"
            )

        st.plotly_chart(fig, use_container_width=True)

        # --- Interpretation
        with st.expander("🧠 How to Interpret These Metrics"):
            st.markdown("""
            - **MAE (Mean Absolute Error)**: Average size of prediction errors. Lower is better.
            - **RMSE (Root Mean Squared Error)**: More sensitive to outliers. Lower is better.
            - **R² Score**: Proportion of variance explained. Closer to 1 is better.
            """)

    except FileNotFoundError:
        st.error("❌ Metrics file not found. Please train models first.")
