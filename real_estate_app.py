import streamlit as st
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

# -------------------- Load Model & Scaler --------------------
model = joblib.load("real_estate_model.pkl")
scaler = joblib.load("real_estate_scaler.pkl")

# -------------------- Streamlit Page Configuration --------------------
st.set_page_config(page_title="Perth Real Estate App", layout="wide")

# -------------------- Load Dataset Globally --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Perth_Realestate_Dataset.csv")
    df["House Age"] = 2025 - df["BUILD_YEAR"]
    df.rename(columns={
        "PRICE": "House Price",
        "LATITUDE": "Latitude",
        "LONGITUDE": "Longitude",
        "NEAREST_STN_DIST": "Distance to MRT",
        "DATE_SOLD": "Transaction Date"
    }, inplace=True)
    return df

df = load_data()

# -------------------- Sidebar Navigation --------------------
with st.sidebar:
    st.image("RealStateLogo.jpeg", width=100)
    st.markdown('<div class="sidebar-title">Perth Real Estate App</div>', unsafe_allow_html=True)
    menu = st.radio("📋 Menu", ["Dashboard", "Predict Price", "Budget Explorer", "Report", "About"])

# -------------------- Header --------------------
st.markdown("<h1 style='text-align: center;'>🏠 Perth Real Estate Price Predictor</h1>", unsafe_allow_html=True)

# -------------------- Page: Dashboard --------------------
if menu == "Dashboard":
    st.markdown('<div class="dashboard-title">📊 Dashboard Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtext">Insights from the Perth real estate dataset.</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.metric("📈 Total Records", len(df))

    # Top 5 Investment Properties
    top_zones = df.copy()
    top_zones["Value Index"] = top_zones["Distance to MRT"] / top_zones["House Price"]
    top5 = top_zones.sort_values(by="Value Index", ascending=True).head(5)

    st.markdown("### 🏆 Top 5 Investment Picks")
    st.dataframe(top5[["ADDRESS", "SUBURB", "House Price", "Distance to MRT", "House Age"]])

    # Map layers
    df["Radius"] = df["House Price"] * 0.02
    all_layer = pdk.Layer(
        "ScatterplotLayer", data=df,
        get_position='[Longitude, Latitude]', get_radius="Radius",
        get_fill_color='[30,144,255,120]', pickable=True
    )
    highlight_layer = pdk.Layer(
        "ScatterplotLayer", data=top5,
        get_position='[Longitude, Latitude]', get_radius=300,
        get_fill_color='[0,255,0,180]', pickable=True
    )
    highest = df[df["House Price"] == df["House Price"].max()].iloc[0:1]
    highlight_highest = pdk.Layer(
        "ScatterplotLayer", data=highest,
        get_position='[Longitude, Latitude]', get_radius=400,
        get_fill_color='[255,0,0,240]', pickable=True
    )
    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(), longitude=df["Longitude"].mean(),
        zoom=11.5, pitch=45
    )
    tooltip = {
        "html": "<b>{ADDRESS}</b><br/>Price: {House Price}<br/>Age: {House Age} yrs<br/>MRT: {Distance to MRT} m",
        "style": {"backgroundColor": "white", "color": "black"}
    }

    st.pydeck_chart(pdk.Deck(
        layers=[all_layer, highlight_layer, highlight_highest],
        initial_view_state=view_state, tooltip=tooltip,
        map_style="mapbox://styles/mapbox/dark-v10"
    ))

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Price", f"{df['House Price'].mean():,.0f}")
    col2.metric("Oldest Home", f"{df['House Age'].max()} yrs")
    col3.metric("Closest MRT", f"{df['Distance to MRT'].min():.2f} m")

# -------------------- Page: Predict Price --------------------
elif menu == "Predict Price":
    st.markdown('<div class="predict-title">🔍 Predict Property Value</div>', unsafe_allow_html=True)
    st.markdown('<div class="predict-card">', unsafe_allow_html=True)

    # Collect inputs
    col1, col2 = st.columns(2)
    with col1:
        build_year = st.slider("🛠 Year Built", 1900, 2025, 2000)
        house_age = 2025 - build_year
        bedrooms = st.selectbox("🛏 Bedrooms", options=[1, 2, 3, 4, 5], index=2)
        bathrooms = st.selectbox("🛁 Bathrooms", options=[1, 2, 3], index=1)
        land_area = st.number_input("🌳 Land Area (sqm)", min_value=50, max_value=2000, value=500)

    with col2:
        floor_area = st.number_input("🏠 Floor Area (sqm)", min_value=50, max_value=1000, value=150)
        dist_cbd = st.slider("🌆 Distance to CBD (km)", 0.0, 40.0, 15.0)
        dist_mrt = st.slider("🚇 Distance to Station (m)", 0.0, 5000.0, 1000.0)

    # Predict
    if st.button("📊 Predict Price"):
        input_data = np.array([[house_age, bedrooms, bathrooms, land_area, floor_area, dist_cbd, dist_mrt]])
        scaled_input = scaler.transform(input_data)
        prediction = model.predict(scaled_input)

        st.success(f"💰 Estimated Price: **{prediction[0]:,.0f} AUD**")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Page: Budget Explorer --------------------
elif menu == "Budget Explorer":
    st.markdown("## 💰 Budget-Based Property Recommendations")

    col1, col2 = st.columns(2)
    with col1:
        max_price = st.slider("💰 Max Price", int(df["House Price"].min()), int(df["House Price"].max()), 600000)
    with col2:
        max_age = st.slider("🏚️ Max Age", 0, int(df["House Age"].max()), 30)

    suburb_options = df["SUBURB"].dropna().unique()
    selected_suburbs = st.multiselect("🏙️ Select Suburbs", options=np.sort(suburb_options), default=suburb_options[:3])

    filtered = df[
        (df["House Price"] <= max_price) &
        (df["House Age"] <= max_age) &
        (df["SUBURB"].isin(selected_suburbs))
    ]

    st.markdown(f"### 🔍 {len(filtered)} properties match your criteria.")

    if not filtered.empty:
        filtered["Value Index"] = filtered["Distance to MRT"] / filtered["House Price"]
        filtered = filtered.sort_values(by="Value Index")

        row_limit = st.selectbox("Download top N results:", [5, 10, 25], index=1)
        st.dataframe(filtered.head(row_limit)[["ADDRESS", "SUBURB", "House Price", "House Age", "Distance to MRT"]])

        csv = filtered.head(row_limit).to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", data=csv, file_name="budget_properties.csv", mime="text/csv")

        filtered["Radius"] = filtered["House Price"] * 0.02
        min_p, max_p = filtered["House Price"].min(), filtered["House Price"].max()
        def colorize(p): return [int(255*(p-min_p)/(max_p-min_p)), 100, 255 - int(255*(p-min_p)/(max_p-min_p)), 180]
        filtered["Color"] = filtered["House Price"].apply(colorize)

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=filtered,
            get_position='[Longitude, Latitude]',
            get_radius="Radius",
            get_fill_color="Color",
            pickable=True
        )

        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=pdk.ViewState(
                latitude=filtered["Latitude"].mean(),
                longitude=filtered["Longitude"].mean(),
                zoom=12,
                pitch=45
            ),
            tooltip={
                "html": "<b>🏠 {ADDRESS}</b><br/>Price: {House Price}<br/>Age: {House Age} yrs",
                "style": {"backgroundColor": "white", "color": "black"}
            },
            map_style="mapbox://styles/mapbox/light-v10"
        ))
    else:
        st.warning("No properties match your budget criteria.")

# -------------------- Page: Report --------------------
elif menu == "Report":
    st.subheader("📄 Report")
    st.info("This section can be expanded with saved predictions, PDF generation, or export options.")

# -------------------- Page: About --------------------
elif menu == "About":
    st.subheader("📚 About This App")
    st.write("""
    This application was developed as part of the ICT619 Artificial Intelligence course at Murdoch University.
    It predicts real estate prices based on property features using a machine learning model.

    **Tech Stack:** Python, Streamlit, scikit-learn  
    """)
