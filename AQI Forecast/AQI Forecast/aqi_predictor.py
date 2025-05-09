import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load the trained LSTM model
model = load_model('aqi_lstm_model.h5')

# Load historical pollutant data
data = pd.read_csv('cleandata.csv')

FEATURES = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'Benzene', 'Toulene', 'Xylene']
SEQUENCE_LENGTH = 30
PREDICTION_DAYS = 90

def get_last_30_days(city):
    city_data = data[data['city'].str.lower() == city.lower()].sort_values(by='date')
    if len(city_data) < SEQUENCE_LENGTH:
        raise ValueError(f"Not enough data for {city}")
    return city_data[FEATURES].values[-SEQUENCE_LENGTH:]

def add_realistic_aqi_variation(base_sequence, day_index):
    varied = base_sequence.copy()

    drift = 0.05 * np.sin(2 * np.pi * day_index / 90 + np.random.uniform(-0.5, 0.5))
    varied += drift * base_sequence

    local_noise = np.random.normal(0, 0.03 * base_sequence)
    varied += local_noise

    if np.random.rand() < 0.1:
        spike = np.random.uniform(-0.2, 0.2) * base_sequence
        varied += spike

    if day_index > 1:
        momentum = 0.1 * (base_sequence - base_sequence.mean())
        varied += momentum

    return np.clip(varied, 0, None)

def classify_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <=200 :
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def detect_trend(aqi_list):
    if len(aqi_list) < 2:
        return ""
    change = aqi_list[-1] - aqi_list[0]
    if change > 5:
        return "↑"
    elif change < -5:
        return "↓"
    else:
        return "→"

@app.route('/predict_aqi', methods=['POST'])
def predict_aqi():
    try:
        city = request.json.get('city', '').strip()

        if not city:
            return jsonify({'error': 'City name is required'}), 400

        sequence = list(get_last_30_days(city))
        predictions = []

        for day in range(1, PREDICTION_DAYS + 1):
            input_seq = np.array(sequence[-SEQUENCE_LENGTH:]).reshape(1, SEQUENCE_LENGTH, len(FEATURES))

            aqi_value = model.predict(input_seq, verbose=0)[0][0]
            aqi_category = classify_aqi(aqi_value)

            predictions.append({
                "day": f"Day {day}",
                "aqi": round(aqi_value, 2),
                "category": aqi_category
            })

            next_pollutants = add_realistic_aqi_variation(sequence[-1], day)
            sequence.append(next_pollutants)

        aqi_values = [p["aqi"] for p in predictions]
        trend = detect_trend(aqi_values)

        return jsonify({
            "city": city.title(),
            "trend": trend,
            "forecast": predictions
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
