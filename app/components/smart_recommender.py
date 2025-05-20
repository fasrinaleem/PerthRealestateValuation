import streamlit as st
import pandas as pd
import os
import pydeck as pdk

@st.cache_data
def load_data():
    path = os.path.join("data", "Perth_Realestate_Dataset.csv")
    df = pd.read_csv(path)
    df["House Age"] = 2025 - df["BUILD_YEAR"]
    df = df.rename(columns={
        "SUBURB": "suburb",
        "PRICE": "price",
        "NEAREST_STN_DIST": "distance_to_mrt",
        "LATITUDE": "latitude",
        "LONGITUDE": "longitude"
    })
    return df.dropna(subset=["price", "suburb", "distance_to_mrt", "House Age", "latitude", "longitude"])

def render():
    st.markdown("""
        <div class="hero">
            <h1>📍 Smart Suburb Recommender</h1>
            <p>Discover the best-value suburbs based on your preferences.</p>
        </div>
    """, unsafe_allow_html=True)

    df = load_data()

    with st.form("recommender_form"):
        budget = st.slider("💰 Your Budget", 100000, 3000000, 700000, step=50000)
        max_age = st.slider("🏠 Max House Age (Years)", 0, 100, 40)
        max_mrt = st.slider("🚉 Max Distance to MRT (meters)", 0, 5000, 2000)

        submitted = st.form_submit_button("🔍 Recommend Suburbs")

    if submitted:
        filtered = df[
            (df["price"] <= budget) &
            (df["House Age"] <= max_age) &
            (df["distance_to_mrt"] <= max_mrt)
        ]

        if filtered.empty:
            st.warning("⚠️ No suburbs match your filters.")
            return

        suburb_scores = (
            filtered.groupby("suburb")
            .agg(
                AvgPrice=("price", "mean"),
                AvgAge=("House Age", "mean"),
                AvgMRT=("distance_to_mrt", "mean"),
                Listings=("price", "count")
            )
            .reset_index()
        )

        # Value Score = weight inverse of price, age, MRT
        suburb_scores["Value Score"] = (
            (1 / (suburb_scores["AvgPrice"] + 1)) * 0.5 +
            (1 / (suburb_scores["AvgAge"] + 1)) * 0.25 +
            (1 / (suburb_scores["AvgMRT"] + 1)) * 0.25
        )

        top_suburbs = suburb_scores.sort_values(by="Value Score", ascending=False).head(10)

        st.success(f"🏆 Top {len(top_suburbs)} Recommended Suburbs")
        st.dataframe(top_suburbs, use_container_width=True)

        # Optional: Map visualization
        map_df = df[df["suburb"].isin(top_suburbs["suburb"])]
        st.markdown("### 🗺 Recommended Areas on Map")
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=map_df["latitude"].mean(),
                longitude=map_df["longitude"].mean(),
                zoom=10,
                pitch=45,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=map_df,
                    get_position='[longitude, latitude]',
                    get_color='[0, 200, 0, 160]',
                    get_radius=100,
                )
            ]
        ))

        st.caption("🔍 Suburbs chosen based on best value (low avg price, young homes, close MRT)")
