import streamlit as st
import pandas as pd
import plotly.express as px
import os

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
            <h1>📊 Market Insights</h1>
            <p>Explore trends and patterns in Perth real estate pricing.</p>
        </div>
    """, unsafe_allow_html=True)

    df = load_data()

    tab1, tab2, tab3 = st.tabs([
        "📆 Yearly Trends",
        "🌆 Suburb Averages",
        "📊 Price Distribution"
    ])

    # --- Yearly Trends (Mean + Median)
    with tab1:
        yearly = df.groupby("BUILD_YEAR").agg({
            "PRICE": ["mean", "median", "count"]
        }).reset_index()
        yearly.columns = ["BUILD_YEAR", "Avg Price", "Median Price", "Property Count"]

        fig = px.line(yearly, x="BUILD_YEAR", y=["Avg Price", "Median Price"],
                      title="Average vs Median Price by Build Year",
                      markers=True)
        fig.update_layout(legend_title="Metric", xaxis_title="Build Year", yaxis_title="Price ($)")
        st.plotly_chart(fig, use_container_width=True)

        st.caption("Note: Median is less sensitive to outliers than mean.")

    # --- Suburb-wise Averages (Dynamic Top N)
    with tab2:
        N = st.slider("Top N Suburbs by Average Price", min_value=5, max_value=50, value=20)
        suburb_avg = df.groupby("SUBURB")["PRICE"].mean().sort_values(ascending=False).head(N).reset_index()
        fig2 = px.bar(suburb_avg, x="SUBURB", y="PRICE", title=f"Top {N} Suburbs by Average Price")
        st.plotly_chart(fig2, use_container_width=True)

    # --- Price Distribution
    with tab3:
        fig3 = px.histogram(df, x="PRICE", nbins=50, title="Distribution of Property Prices")
        fig3.update_layout(xaxis_title="Price ($)", yaxis_title="Count")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div class='footer'>Data visualized from Perth Real Estate dataset</div>", unsafe_allow_html=True)
