# app.py
from flask import Flask, request, jsonify
from collections import OrderedDict
from model import AnomalyDetector
app = Flask(__name__)


@app.route('/getmsg/', methods=['GET'])
def respond(anomaly_detector=AnomalyDetector()):
    # Retrieve the name from url parameter

    args = {'air_temperature': None, 'rainfall': None, 'relative_humidity': None, 'wind_speed': None}

    added_input = False
    for key, value in args.items():
        args[key] = request.args.get(key, None)
        if not args[key]:
            raise ValueError("Must supply all weather readings"
                             )
    response = {}

    if added_input:
        response["ERROR"] = "Please provide an input"
    else:
        response["CONTENT"] = anomaly_detector(**args)
        response["MESSAGE"] = f"Welcome  to our awesome platform!!"

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