
# 🏠 Perth House Price Prediction App

A user-friendly and interactive web application built with **Streamlit** that predicts house prices in **Perth, Australia**, based on property features such as location, age, size, and accessibility. Developed as part of the ICT619 Artificial Intelligence course at **Murdoch University**.

🔗 **Live App:** [perth-house-price-prediction.streamlit.app](https://perth-house-price-prediction.streamlit.app)  
📁 **GitHub Repo:** [github.com/fasrinaleem/PerthRealestateValuation](https://github.com/fasrinaleem/PerthRealestateValuation)

---

## 🚀 Features

### 🔍 Price Prediction
- Predicts property price using:
  - House Age (from build year)
  - Bedrooms and Bathrooms
  - Land and Floor Area
  - Distance to CBD and Station
- Powered by a **Random Forest** model and **StandardScaler**.

### 📊 Dashboard Overview
- Displays insights from 400+ records
- Highlights top 5 suburbs with best value-for-access ratio
- Visual trend charts for house age and MRT access

### 🌏 Interactive Map
- Uses PyDeck to display all properties
- 🔵 All homes in blue  
- 🟢 Top 5 picks highlighted in green  
- 🔴 Most expensive home highlighted in red  
- Hover tooltips include address, price, age, and MRT distance

### 💰 Budget Explorer
- Filter properties by:
  - Budget range
  - Maximum house age
  - Suburb selection
- Download top-matching results as CSV
- View filtered properties color-coded by price on the map

---

## 📂 Project Structure

```
PERTHREALESTATEVALUATION/
├── logo/
│   └── RealStateLogo.jpeg       # App logo
├── .gitignore                   # Ignore unnecessary files
├── README.md                    # Project documentation
├── instructions.txt             # Notes & setup guide
├── Perth_Realestate_Dataset.csv# Main dataset
├── real_estate_app.py          # Streamlit application
├── train_model.py              # Model training script
├── real_estate_model.pkl       # Trained ML model
├── real_estate_scaler.pkl      # Scaler for feature normalization
├── style.css                   # Custom app styles
├── requirements.txt            # Project dependencies
```

---

## 🧠 Tech Stack

| Tool           | Description                                  |
|----------------|----------------------------------------------|
| **Python**     | Backend development and ML modeling          |
| **Streamlit**  | Web UI framework for real-time ML apps       |
| **Scikit-learn** | Model training and feature scaling         |
| **PyDeck**     | Map visualization using WebGL                |
| **Geopy**      | Reverse geocoding for location names         |
| **Pandas/Numpy** | Data manipulation and preprocessing        |

---

## 📊 Dataset Information

**Source:** [Perth House Prices – Kaggle](https://www.kaggle.com/datasets/syuzai/perth-house-prices)

| Column              | Description                            |
|---------------------|----------------------------------------|
| `BUILD_YEAR`        | Year the house was constructed          |
| `BEDROOMS` / `BATHROOMS` | Number of rooms                   |
| `LAND_AREA` / `FLOOR_AREA` | Property size in square meters |
| `DISTANCE_TO_CBD`   | Distance to Perth CBD in kilometers     |
| `NEAREST_STN_DIST`  | Distance to nearest train station in m  |
| `PRICE`             | Selling price (target) in AUD           |
| `LATITUDE/LONGITUDE`| Location coordinates                    |
| `SUBURB`, `ADDRESS` | Human-readable location identifiers     |

---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/fasrinaleem/PerthRealestateValuation.git
cd PerthRealestateValuation

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Train the model
python train_model.py

# 4. Launch the app
streamlit run real_estate_app.py
```

---

## 🧩 Challenges Faced

- 🧭 Inconsistent location and address formats → resolved via column cleanup  
- 📦 GitHub model upload issues → solved with **Git LFS**  
- 🔄 Mismatch between model input and form data → fixed by aligning input features  
- 🧪 Managing 400+ properties in a map → optimized using **PyDeck** filtering  
- 🔐 GitHub authentication via HTTPS → resolved using SSH/PAT setup  

---

## 👨‍💻 Contributors

- **Fasrin Aleem**
- **Rabindra Mahato**
- **Kushi**

🎓 Course: ICT619 Artificial Intelligence  
🏫 Institution: Murdoch University  
📅 Year: 2025
