import requests
import pandas as pd

def fetch_data(latitude, longitude, start_date, end_date, save_csv=False, csv_path=None):
    """
    Gather data from Open-Meteo API for a specific date range.

    Parameters:
    - latitude, longitude: location
    - start_date, end_date: "YYYY-MM-DD"
    """

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "relative_humidity_2m_max",
            "relative_humidity_2m_min",
            "relative_humidity_2m_mean",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "wind_direction_10m_dominant",
            "precipitation_sum",
            "rain_sum",
            "snowfall_sum",
            "precipitation_hours",
            "shortwave_radiation_sum",
            "sunshine_duration",
            "weather_code"
        ],
        "temperature_unit": "celsius",
        "wind_speed_unit": "mph",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data["daily"])

    # Create target (tomorrow’s apparent temp)
    df["target"] = df["apparent_temperature_max"].shift(-1)

    # Features and labels
    X = df.drop(columns=["apparent_temperature_max", "target"])
    y = df["target"]

    if save_csv and csv_path:
        df.to_csv(csv_path, index=False)

    return df