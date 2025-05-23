# 🏠 Perth House Price Prediction App

An intelligent and user-friendly web application built with Streamlit that predicts house prices in Perth, Australia, based on key features like house size, age, proximity to CBD/MRT, and more. Developed as part of the ICT619 Artificial Intelligence course at Murdoch University.

🔗 **Live App**: [perth-house-price-prediction.streamlit.app](https://perth-house-price-prediction.streamlit.app)  
📁 **GitHub Repo**: [github.com/fasrinaleem/PerthRealestateValuation](https://github.com/fasrinaleem/PerthRealestateValuation) 
📊 **Source:** [Kaggle – Perth House Prices](https://www.kaggle.com/datasets/syuzai/perth-house-prices)


---

## 🚀 Features


- 📊 **House Price Prediction** using XGBoost, Random Forest, Linear Regression, and KNN.
- 📍 **Smart Suburb Recommender** based on price, age, and MRT proximity.
- 💰 **Budget Explorer** for filtering properties by price, location, and house age.
- 📈 **Price Trend Forecaster** predicting future property prices until 2035.
- 📌 **Model Comparison Dashboard** with R², MAE, RMSE metrics.
- 🧪 **Retraining Module** to update models with new data.
- 🔐 **User Authentication** with secure login and session state.
- 🌐 **Interactive Maps** powered by PyDeck and Plotly.



---

## 📂 Project Structure

```
PerthRealestateValuation/
├── app/
│   ├── main.py               # Main app entry point
│   ├── style/                # Custom CSS for styling
│   └── components/           # Modular pages: prediction, insights, etc.
├── scripts/                  # Auth, training, and utility logic
├── data/                     # Dataset + model_metrics.csv + users.csv
├── models/                   # Trained ML models and scaler
├── assets/                   # App logo (estate.png)
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── instructions.txt          # Project brief / notes
```

---

## 🧠 Tech Stack

| Tool                  | Description                                  |
|-----------------------|----------------------------------------------|
| Python                | Core backend and ML modeling                 |
| Streamlit             | Real-time web UI framework                   |
| Scikit-learn          | Training models and preprocessing            |
| XGBoost               | Gradient boosting model                      |
| Plotly                | Interactive charts and data visualizations   |
| PyDeck                | Geospatial visualization with WebGL          |
| Pandas / NumPy        | Data manipulation and math                   |
| Streamlit Option Menu | Sidebar UI navigation with icons             |

---

## 📊 Dataset Information

**Source:** [Kaggle – Perth House Prices](https://www.kaggle.com/datasets/syuzai/perth-house-prices)

| Column              | Description                          |
|---------------------|--------------------------------------|
| BUILD_YEAR          | Year of construction                 |
| BEDROOMS / BATHROOMS| Number of rooms                      |
| LAND_AREA, FLOOR_AREA | Property dimensions (sqm)          |
| DISTANCE_TO_CBD     | Distance to Perth CBD (km)           |
| NEAREST_STN_DIST    | Distance to nearest MRT (meters)     |
| PRICE               | Sale price in AUD                    |
| LATITUDE, LONGITUDE | GPS coordinates                      |
| SUBURB, ADDRESS     | Textual identifiers                  |

---
└── README.md

---

## 🚀 Installation
```
```bash
# Clone the repo
git clone https://github.com/fasrinaleem/PerthRealestateValuation.git
cd PerthRealestateValuation

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
streamlit run app/main.py
```

The app will open at `http://localhost:8501`.

---

## 🔄 Retrain Models (Optional)

To retrain all models from the command line:

```bash
python scripts/train_model.py
```

Trained models will be saved in the `models/` directory.

---

## 🧠 Model Results

| Model            | R² Score | RMSE     |
|------------------|----------|----------|
| XGBoost          | 0.912    | 152,987  |
| Random Forest    | 0.892    | 164,515  |
| Linear Regression| 0.649    | 273,341  |
| KNN              | 0.781    | 190,301  |

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
```

---

## 🧪 Challenges Faced

- 🧭 Inconsistent location formatting → cleaned via pandas renaming and type casting
- 📦 Model size issue on GitHub → handled via Git LFS
- 🔄 Mismatch between model input and form layout → fixed via unified input schema
- 🧪 Performance with 400+ data points on map → optimized layer loading with PyDeck
- 🔐 Secure login implementation → SHA-256 password hashing, CSV auth system

---

## 👨‍💻 Contributors

- Mohamed Fasrin Aleem    
- Rabindra Mahato
- Khushiben Kiritkumar Chauhan

🎓 Course: ICT619 Artificial Intelligence  
🏫 Institution: Murdoch University  
📅 Year: 2025

---

## 📃 License

This project is for academic use only. If you wish to build upon it, please cite the authors and Murdoch University ICT619.
