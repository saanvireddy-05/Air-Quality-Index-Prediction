# 🌍 Air Quality Index (AQI) Dashboard and Analysis System

This project is a dynamic web-based AQI Dashboard that simplifies complex environmental data into clear, visual insights. It allows users to select a city and view **predicted AQI values for the next 90 days**, along with **trend analysis, performance metrics**, and **visualizations** using deep learning models.



## 🚀 Features

- 📊 **90-Day AQI Forecast** using LSTM (Long Short-Term Memory)
- 📈 **Interactive AQI Trend Graph** with 7-day moving average
- 📋 **Detailed AQI Data Table** with trend direction (↑, ↓, →) and category classification (Good, Moderate, Unhealthy)
- 📑 **City-wise AQI Analysis Report** with summary stats and model performance
- 🧠 **Model Performance Metrics**: Accuracy, Precision, Recall, and F1-Score
- 🌆 Support for multiple Indian metropolitan cities

---

## 🧠 Model Information

- **Model Type**: LSTM (Long Short-Term Memory)
- **Data**: Time-series pollutant concentrations
- **Features**: PM2.5, PM10, NO₂, SO₂, O₃, NH₃, Xylene, Benzene, Toluene
- **Training/Testing**: 70% training / 30% testing
- **Metrics Used**: MSE, Accuracy, Precision, Recall, F1-Score

---

### ▶️ Run the Server

Start the development server by running the following command:

```bash
python manage.py runserver
```
Then open your browser and go to:
http://127.0.0.1:8000
Your AQI Dashboard will be live!

### Screenshots of the project

![Screenshot 2025-04-06 101709](https://github.com/user-attachments/assets/493994bb-e29d-4f62-9612-f2fe23ba98a3)



![Screenshot 2025-04-06 101759](https://github.com/user-attachments/assets/fe0db97f-f006-4f2e-9673-9e95d16240b6)



![Screenshot 2025-04-06 101833](https://github.com/user-attachments/assets/e8cf560d-dd95-4d60-aa86-06b98dc13274)



![Screenshot 2025-04-06 101935](https://github.com/user-attachments/assets/574c3d50-fefe-4d8c-bd89-de6f009ef939)



![Screenshot 2025-04-06 102000](https://github.com/user-attachments/assets/53dde63f-10c1-41ed-a548-24850af92d80)






