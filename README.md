# 🚦 TrafficLens

## 📌 Overview

This project is a **Machine Learning-based Traffic Prediction System** that forecasts traffic volume based on historical data such as time, date, and other features.
The goal is to help in **smart traffic management, route optimization, and congestion control**.

---

## 🎯 Features

* 🗺️ Interactive map with route visualization
* 📍 Location search (local + API-based)
* 🚦 Traffic prediction (Low / Medium / High)
* 📏 Distance calculation between locations

---

## 🧠 Tech Stack

* Python
* Pandas, NumPy
* Matplotlib / Seaborn
* Scikit-learn
* Streamlit (for UI)

---

## 📂 Project Structure

```
traffic-congestion-predictor/
│── data/                  
│── model.py              # ML model training & prediction
│── generate_data.py      # Synthetic dataset generator
│── preprocess.py         # Data preprocessing
│── ui.py                 # UI components
│── app.py                # Streamlit app
│── requirements.txt      
│── README.md             
```

---
## 📊 Dataset

This project uses a **synthetically generated dataset** that simulates real-world traffic patterns based on:

- Hour of the day (peak vs non-peak)
- Day of the week (weekday vs weekend)
- Vehicle count (simulated traffic density)

The dataset is generated using `generate_data.py`.
---

## ⚙️ How It Works

1. Load dataset using Pandas
2. Perform data cleaning and preprocessing
3. Extract features like hour, day, weekday
4. Train ML models (e.g., Linear Regression, Random Forest)
5. Predict future traffic trends

---

## 🚀 Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/HimaniLohani/traffic-predictor.git
cd traffic-predictor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the project

```bash
python -m streamlit run app.py
```

---

## 📈 Results

- Successfully predicts traffic levels (Low, Medium, High)
- Handles peak-hour congestion patterns effectively
- Provides route-based visualization with distance
- Improved model performance using synthetic realistic data

---

## 💡 Use Cases

* Smart city traffic management
* Navigation systems (like route optimization)
* Ride-sharing apps (e.g., cab demand prediction)

---

## 🔮 Future Improvements

* Add real-time data integration
* Use deep learning models (LSTM)
* Deploy on cloud (AWS / GCP)
* Improve UI/UX

---

## 👩‍💻 Author

**Himani Lohani**

---

## ⭐ Acknowledgment

This project is created for learning and showcasing **AI/ML skills for real-world problem solving**.
