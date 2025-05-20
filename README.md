# 🏠 Perth House Price Prediction App

An intelligent and user-friendly web application built with **Streamlit** that predicts house prices in **Perth, Australia**, based on key features like house size, age, proximity to CBD/MRT, and more. Developed as part of the **ICT619 Artificial Intelligence** course at **Murdoch University**.

🔗 **Live App:** [perth-house-price-prediction.streamlit.app](https://perth-house-price-prediction.streamlit.app)  
📁 **GitHub Repo:** [github.com/fasrinaleem/PerthRealestateValuation](https://github.com/fasrinaleem/PerthRealestateValuation)

---

## 🚀 Features

### 🔍 Price Prediction
- Predict house prices using:
  - House Age (BUILD_YEAR)
  - Bedrooms and Bathrooms
  - Land and Floor Area
  - Distance to CBD and Nearest Train Station
- Powered by ML models like **Random Forest**, **XGBoost**, **Linear Regression**, and **KNN**

### 📊 Dashboard Overview
- Visual KPIs for total listings, average price, and oldest home
- Top 5 most expensive properties
- Map overview with dynamic plotting via **PyDeck**

### 🌏 Interactive Map
- All properties mapped via coordinates
- 🟢 Top 5 picks highlighted
- 🔴 Most expensive property marked
- Hover tooltips include price, suburb, MRT distance

### 💰 Budget Explorer
- Filter by:
  - Budget range
  - House age
  - Suburb and MRT access
- Map + downloadable CSV of filtered results

### 🧠 Smart Recommender
- Recommends suburbs with highest value-for-budget based on:
  - Price
  - Proximity to MRT
  - House age

### 📈 Trend Forecaster
- Predicts average price trends over future years using **Linear Regression**
- Displays forecasted chart with past + projected averages

---

## 📂 Project Structure

PerthRealestateValuation/
├── app/
│ ├── main.py # Main app entry point
│ ├── style/ # Custom CSS for styling
│ └── components/ # Modular pages: prediction, insights, etc.
├── scripts/ # Auth, training, and utility logic
├── data/ # Dataset + model_metrics.csv + users.csv
├── models/ # Trained ML models and scaler
├── assets/ # App logo (estate.png)
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── instructions.txt # Project brief / notes


---

## 🧠 Tech Stack

| Tool                   | Description                                |
|------------------------|--------------------------------------------|
| **Python**             | Core backend and ML modeling               |
| **Streamlit**          | Real-time web UI framework                 |
| **Scikit-learn**       | Training models and preprocessing          |
| **XGBoost**            | Gradient boosting model                    |
| **Plotly**             | Interactive charts and data visualizations |
| **PyDeck**             | Geospatial visualization with WebGL        |
| **Pandas / NumPy**     | Data manipulation and math                 |
| **Streamlit Option Menu** | Sidebar UI navigation with icons     |

---

## 📊 Dataset Information

**Source:** [Kaggle – Perth House Prices](https://www.kaggle.com/datasets/syuzai/perth-house-prices)

| Column              | Description                                 |
|---------------------|---------------------------------------------|
| `BUILD_YEAR`        | Year of construction                        |
| `BEDROOMS` / `BATHROOMS` | Number of rooms                      |
| `LAND_AREA`, `FLOOR_AREA` | Property dimensions (sqm)          |
| `DISTANCE_TO_CBD`   | Distance to Perth CBD (km)                  |
| `NEAREST_STN_DIST`  | Distance to nearest MRT (meters)            |
| `PRICE`             | Sale price in AUD                           |
| `LATITUDE`, `LONGITUDE` | GPS coordinates                        |
| `SUBURB`, `ADDRESS` | Textual identifiers                         |

---

## ⚙️ How to Run Locally

```bash
# 1. Clone this repository
git clone https://github.com/fasrinaleem/PerthRealestateValuation.git
cd PerthRealestateValuation

# 2. Create environment and install dependencies
pip install -r requirements.txt

# 3. (Optional) Retrain models
python scripts/train_model.py

# 4. Launch the app
streamlit run app/main.py


 Challenges Faced
🧭 Inconsistent location formatting → cleaned via pandas renaming and type casting

📦 Model size issue on GitHub → handled via Git LFS

🔄 Mismatch between model input and form layout → fixed via unified input schema

🧪 Performance with 400+ data points on map → optimized layer loading with PyDeck

🔐 Secure login implementation → SHA-256 password hashing, CSV auth system

👨‍💻 Contributors
Mohamed Fasrin Aleem

Khushiben Kiritkumar Chauhan

Rabindra Mahato

🎓 Course: ICT619 Artificial Intelligence
🏫 Institution: Murdoch University
📅 Year: 2025

📃 License
This project is for academic use only. If you wish to build upon it, please cite the authors and Murdoch University ICT619.