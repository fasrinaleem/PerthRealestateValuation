import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
from sklearn.linear_model import LinearRegression

@st.cache_data
def load_data():
    path = os.path.join("data", "Perth_Realestate_Dataset.csv")
    df = pd.read_csv(path)
    df["BUILD_YEAR"] = pd.to_numeric(df.get("BUILD_YEAR", pd.Series()), errors='coerce')
    df["PRICE"] = pd.to_numeric(df.get("PRICE", pd.Series()), errors='coerce')
    df = df.dropna(subset=["PRICE", "BUILD_YEAR"])
    df["BUILD_YEAR"] = df["BUILD_YEAR"].astype(int)
    return df

def render():
    st.markdown("""
        <div class="hero">
            <h1>📈 Price Trend Forecaster</h1>
            <p>Forecast Perth's average real estate prices using historical build year trends.</p>
        </div>
    """, unsafe_allow_html=True)

    df = load_data()
    trend = df.groupby("BUILD_YEAR")["PRICE"].mean().reset_index()

    # Prepare data for regression
    X = trend["BUILD_YEAR"].values.reshape(-1, 1)
    y = trend["PRICE"].values
    model = LinearRegression()
    model.fit(X, y)

    # Forecast next 10 years
    future_years = np.arange(2025, 2036).reshape(-1, 1)
    future_preds = model.predict(future_years)

    forecast_df = pd.DataFrame({
        "Year": future_years.flatten(),
        "Forecasted Avg Price": future_preds.astype(int)
    })

    # Combine historical + forecast for visualization
    trend["Type"] = "Historical"
    forecast_df["Type"] = "Forecast"
    forecast_df.columns = ["BUILD_YEAR", "PRICE", "Type"]
    combined = pd.concat([trend, forecast_df])

    fig = px.line(
        combined, x="BUILD_YEAR", y="PRICE", color="Type", markers=True,
        title="Historical and Forecasted Avg House Prices"
    )
    fig.update_layout(xaxis_title="Year", yaxis_title="Avg Price ($)", legend_title="Data Type")

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(forecast_df, use_container_width=True)

    st.caption("📌 Forecast uses linear regression from historical averages by build year.")
