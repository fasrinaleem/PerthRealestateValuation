import streamlit as st
import pandas as pd
import pydeck as pdk
import os

@st.cache_data
def load_data():
    path = os.path.join("data", "Perth_Realestate_Dataset.csv")
    return pd.read_csv(path)

def render():
    st.title("💰 Budget-Based Property Explorer")
    st.markdown("Filter properties that match your budget, MRT proximity, and other preferences.")

    df = load_data()

    # Feature engineering
    df["HOUSE_AGE"] = 2025 - df["BUILD_YEAR"]
    df = df.rename(columns={
        "ADDRESS": "address",
        "SUBURB": "suburb",
        "PRICE": "price",
        "HOUSE_AGE": "house_age",
        "NEAREST_STN_DIST": "distance_to_mrt",
        "LATITUDE": "latitude",
        "LONGITUDE": "longitude"
    })

    with st.form("budget_filter_form"):
        budget = st.slider("Select your budget ($)", min_value=100000, max_value=3000000, value=(300000, 900000), step=50000)
        max_age = st.slider("Max House Age (years)", 0, 100, 50)
        max_mrt = st.slider("Max Distance to MRT (m)", 0, 5000, 2000)
        suburbs = st.multiselect("Preferred Suburbs", options=sorted(df['suburb'].dropna().unique()), default=sorted(df['suburb'].dropna().unique())[:5])
        sort_by = st.selectbox("Sort results by", options=["price", "house_age", "distance_to_mrt"])

        submitted = st.form_submit_button("🔎 Filter Properties")

    if submitted:
        filtered = df[
            (df['price'] >= budget[0]) &
            (df['price'] <= budget[1]) &
            (df['house_age'] <= max_age) &
            (df['distance_to_mrt'] <= max_mrt) &
            (df['suburb'].isin(suburbs))
        ].sort_values(by=sort_by)

        st.success(f"✅ Found {len(filtered)} matching properties.")

        if not filtered.empty:
            st.dataframe(
                filtered[["address", "suburb", "price", "house_age", "distance_to_mrt"]],
                use_container_width=True
            )

            st.download_button(
                "📥 Download Results as CSV",
                data=filtered.to_csv(index=False),
                file_name="filtered_properties.csv",
                mime="text/csv"
            )

            # Map centered on filtered results
            lat = filtered["latitude"].mean()
            lon = filtered["longitude"].mean()

            st.markdown("### 🗺 Matching Properties on Map")
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=lat,
                    longitude=lon,
                    zoom=10,
                    pitch=45,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=filtered,
                        get_position='[longitude, latitude]',
                        get_color='[255, 0, 0, 160]',
                        get_radius=100,
                    )
                ]
            ))

            st.caption("Data Source: PerthRealestateValuation dataset")
        else:
            st.warning("⚠️ No matching properties found. Try adjusting your filters.")
    else:
        st.info("Use the filters on the left to explore budget-matching properties.")
