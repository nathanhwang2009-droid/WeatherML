import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "best_model.pkl"
FEATURE_COLUMNS_PATH = BASE_DIR / "model" / "feature_columns.json"
WEATHER_CODES_PATH = BASE_DIR / "model" / "weather_code_categories.json"

app = Flask(__name__)

with open(FEATURE_COLUMNS_PATH, "r", encoding="utf-8") as f:
    feature_columns = json.load(f)

with open(WEATHER_CODES_PATH, "r", encoding="utf-8") as f:
    weather_codes = json.load(f)

model = joblib.load(MODEL_PATH)

numeric_features = [
    col
    for col in feature_columns
    if col not in {"year", "month", "day"}
    and not col.startswith("weather_code_")
]


def preprocess_payload(payload):
    date_value = payload.get("date", "")
    if not date_value:
        raise ValueError("Date is required.")

    dt = pd.to_datetime(date_value)
    row = {
        "year": int(dt.year),
        "month": int(dt.month),
        "day": int(dt.day),
        "weather_code": payload.get("weather_code"),
    }

    for feature in numeric_features:
        value = payload.get(feature, "")
        row[feature] = float(value) if value != "" else 0.0

    df = pd.DataFrame([row])
    df = pd.get_dummies(df, columns=["weather_code"], drop_first=True)
    df = df.reindex(columns=feature_columns, fill_value=0)
    return df.astype(np.float64)


@app.route("/api/metadata", methods=["GET"])
def metadata():
    return jsonify(
        weather_codes=weather_codes,
        numeric_features=numeric_features,
    )


@app.route("/api/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True)
    x = preprocess_payload(payload)
    prediction = model.predict(x)[0]
    return jsonify(prediction=float(prediction))


if __name__ == "__main__":
    app.run(debug=True)