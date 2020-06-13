# app.py
from flask import Flask, request, jsonify
from model import AnomalyDetector
from datetime import datetime
import requests
import urllib
import json

app = Flask(__name__)

url_dict = {'air_temperature': 'https://api.data.gov.sg/v1/environment/air-temperature/?{}',
            'rainfall': 'https://api.data.gov.sg/v1/environment/rainfall/?{}',
            'relative_humidity': 'https://api.data.gov.sg/v1/environment/relative-humidity/?{}',
            'wind_speed': 'https://api.data.gov.sg/v1/environment/wind-speed/?{}'}


def request_data_gov(weather_modality='air_temperature'):
    url = url_dict[weather_modality]
    datetime_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    params = {'datetime': datetime_str}
    full_url = url.format(urllib.parse.urlencode(params))
    response = requests.get(full_url)
    reading_value = json.loads(response.content.decode('utf-8'))['items'][0]['readings'][0]["value"] # arbitrary station

    return reading_value


@app.route('/getmsg/', methods=['GET'])
def respond(anomaly_detector=AnomalyDetector()):
    # Retrieve the name from url parameter

    args = {'air_temperature': None, 'rainfall': None, 'relative_humidity': None, 'wind_speed': None}

    for key, value in args.items():
        args[key] = request.args.get(key, None)

        if not args[key]:
            args[key] = request_data_gov(key)
            print("requested key {} value {}".format(key, args[key]))

        if key == 'air_temperature':
            if int(args[key]) < 26:  # hacky trick
                args[key] = 33

    response = {"anomaly_detections": anomaly_detector(**args)}
    response.update({'input_to_algorithm':args})  # User defined arguments
    response.update({'real_readings':{k: request_data_gov(k) for k in args}}) #real readings

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)