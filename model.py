import joblib


def to_bool(flash_flood_pred, wildfire_pred, high_rainfall_pred, high_temperature_pred, high_wind_pred):
    if flash_flood_pred == 0:
        flash_flood_anomalous = False
    else:
        flash_flood_anomalous = True

    if wildfire_pred == 0:
        wildfire_anomalous = False
    else:
        wildfire_anomalous = True

    if high_rainfall_pred == 1:
        high_rainfall_anomalous = False
    else:
        high_rainfall_anomalous = True

    if high_temperature_pred == 1:
        high_temperature_anomalous = False
    else:
        high_temperature_anomalous = True

    if high_wind_pred == 1:
        high_wind_anomalous = False
    else:
        high_wind_anomalous = True

    return dict(flash_flood_anomalous=flash_flood_anomalous, wildfire_anomalous=wildfire_anomalous,
                high_rainfall_anomalous=high_rainfall_anomalous, high_temperature_anomalous=high_temperature_anomalous,
                high_wind_anomalous=high_wind_anomalous)


class AnomalyDetector:
    def __init__(self):
        self.flash_flood_scaler = joblib.load('minmax_rainfall_wind-speed.joblib')
        self.wildfire_scaler = joblib.load('minmax_air-temperature_relative-humidity.joblib')

        self.flash_flood_detector = joblib.load('iforest_rainfall_wind-speed.joblib')
        self.wildfire_detector = joblib.load('iforest_air-temperature_relative-humidity.joblib')

        self.high_rainfall_detector = joblib.load('iforest_rainfall.joblib')
        self.high_temperature_detector = joblib.load('iforest_air-temperature.joblib')
        self.high_wind_speed_detector = joblib.load('iforest_wind-speed.joblib')

    def __call__(self, air_temperature, rainfall, relative_humidity, wind_speed):

        flash_flood_scaled = self.flash_flood_scaler.transform([[rainfall, wind_speed]])
        flash_flood_pred = self.flash_flood_detector.predict(flash_flood_scaled)[0] # 0 normal, 1 anomalous

        wildfire_scaled = self.wildfire_scaler.transform([[air_temperature, relative_humidity]])
        wildfire_pred = self.wildfire_detector.predict(wildfire_scaled)[0] # 0 normal, 1 anomalous

        high_rainfall_pred = self.high_rainfall_detector.predict([[rainfall]]) # 1 normal, -1 anomalous
        high_temperature_pred = self.high_temperature_detector.predict([[air_temperature]]) # 1 normal, -1 anomalous
        high_wind_pred = self.high_wind_speed_detector.predict([[wind_speed]]) # 1 normal, -1 anomalous

        return to_bool(flash_flood_pred, wildfire_pred, high_rainfall_pred, high_temperature_pred, high_wind_pred)
