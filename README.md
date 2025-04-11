# 🏠 Perth Real Estate Price Predictor

An interactive AI-powered web application that predicts housing prices in Perth based on property features such as land size, floor area, location proximity, and more. Developed for the ICT619 Artificial Intelligence course at **Murdoch University**.

🔗 **Live App**: [perth-house-price-prediction.streamlit.app](https://perth-house-price-prediction.streamlit.app)

---

## 🚀 Features

### 🔍 Price Prediction
- Predicts house prices using a trained **Random Forest** regression model.
- Inputs include: Year Built, Bedrooms, Bathrooms, Land & Floor Area, Distance to CBD & Station.
- Feature scaling applied using **StandardScaler**.

### 📊 Dashboard
- Summary of all listings
- 2x2 charts: Price Distribution, House Age vs Price, Distance to MRT, and Land Area vs Price
- Price trend line by house age

### 🧭 Investment Map
- Interactive PyDeck map showing:
  - 🔵 All properties
  - 🟢 Top 5 value picks
  - 🔴 Highest-priced property
- Tooltips show address, price, and age

### 💰 Budget Explorer
- Filter properties by:
  - Max Price
  - Max Age
  - Suburb selection
- Map highlights budget-matching properties
- Export filtered data as CSV

### 🏗️ Model Training
- Features used:
  - `House Age`, `BEDROOMS`, `BATHROOMS`, `LAND_AREA`, `FLOOR_AREA`, `CBD_DIST`, `NEAREST_STN_DIST`
- Model: `RandomForestRegressor`
- Scaler: `StandardScaler`

---

## 📂 Project Structure

```
PerthRealestateValuation/
├── real_estate_app.py                               # Streamlit app
├── train_model.py                                   # Model training script
├── Perth_Realestate_Dataset.csv                     # Main dataset
├── real_estate_model.pkl                            # Trained model file (Ignored git)
├── real_estate_scaler.pkl                           # Trained scaler (Ignored in git)
├── style.css                                        # App styles
├── requirements.txt                                 # Project dependencies
└── README.md                                        # This file
```

---

## 🧪 Dataset & Features

| Feature               | Description                                 |
|-----------------------|---------------------------------------------|
| `ADDRESS`             | Street address of the property              |
| `SUBURB`              | Suburb where the property is located        |
| `PRICE`               | Final sale price (AUD)                      |
| `BEDROOMS`            | Number of bedrooms                          |
| `BATHROOMS`           | Number of bathrooms                         |
| `LAND_AREA`           | Size of the land (sqm)                      |
| `FLOOR_AREA`          | Size of internal floor area (sqm)           |
| `BUILD_YEAR`          | Year the house was built                    |
| `CBD_DIST`            | Distance to CBD (km)                        |
| `NEAREST_STN_DIST`    | Distance to nearest station (meters)        |
| `LATITUDE` / `LONGITUDE` | Coordinates for mapping                  |

🧠 *Derived Feature*: `House Age = 2025 - BUILD_YEAR`

---

## 🛠️ Technologies Used

| Technology        | What it’s for                     |
|------------------|------------------------------------|
| **Python**        | Core language                      |
| **Streamlit**     | Web app framework                  |
| **Scikit-learn**  | Machine learning                   |
| **StandardScaler**| Feature normalization              |
| **PyDeck**        | Interactive map visualizations     |
| **Matplotlib**    | Charts and plots                   |
| **Pandas/NumPy**  | Data manipulation                  |
| **Git & GitHub**  | Version control                    |
| **Streamlit Cloud** | Deployment platform              |

---

## 👤 Authors

**Fasrin Aleem**, **Rabinra Mahato**, **Kushi**  
📘 Course: ICT619 Artificial Intelligence  
🏫 Murdoch University – 2025

---

## 📃 License

Open-source under MIT License / Academic use
