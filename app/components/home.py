import streamlit as st
import pandas as pd
import pydeck as pdk
import os

@st.cache_data
def load_data():
    data_path = os.path.join("data", "Perth_Realestate_Dataset.csv")
    df = pd.read_csv(data_path)
    # Calculate house age (current year - build year)
    if "BUILD_YEAR" in df.columns:
        df["house_age"] = 2025 - df["BUILD_YEAR"]
    else:
        df["house_age"] = 0  # fallback
    # Rename columns for clarity in the UI
    df = df.rename(columns={
        "ADDRESS": "address",
        "SUBURB": "suburb",
        "PRICE": "price",
        "NEAREST_STN_DIST": "distance_to_mrt",
        "LATITUDE": "latitude",
        "LONGITUDE": "longitude"
    })
    return df

# Load custom styles
with open("app/style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render():
    df = load_data()

    st.markdown("""
    <div class="hero">
        <h1>🏡 Perth Real Estate AI</h1>
        <p>Smart predictions and insights from Western Australia's housing market.</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h3>Total Listings</h3>
                <p>{:,}</p>
            </div>
        """.format(len(df)), unsafe_allow_html=True)

    with col2:
        avg_price = int(df["price"].mean()) if "price" in df else 0
        st.markdown("""
            <div class="metric-card">
                <h3>Avg Price</h3>
                <p>${:,}</p>
            </div>
        """.format(avg_price), unsafe_allow_html=True)

    with col3:
        max_age = df["house_age"].max() if "house_age" in df else 0
        st.markdown("""
            <div class="metric-card">
                <h3>Oldest Home</h3>
                <p>{:.0f} yrs</p>
            </div>
        """.format(max_age), unsafe_allow_html=True)

    st.divider()

    # Data Tabs
    tab1, tab2 = st.tabs(["🏅 Top 5 Picks", "🗺 Map Overview"])

    with tab1:
        st.markdown("### Top Investment Picks")
        top5_df = df.sort_values(by="price", ascending=False).head(5)
        st.dataframe(top5_df[["address", "suburb", "price", "distance_to_mrt", "house_age"]], use_container_width=True)

    with tab2:
        st.markdown("### Property Map")
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=-31.95,
                longitude=115.86,
                zoom=9,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_color='[0, 0, 255, 160]',
                    get_radius=100,
                )
            ]
        ))

    # Footer
    st.markdown("""
        <div class="footer">
            © 2025 Perth Real Estate AI — Fasrin, Khushiben, Rabindra
        </div>
    """, unsafe_allow_html=True)
