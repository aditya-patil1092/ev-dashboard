from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Latest EV data (dummy values for testing)
latest_data = {
    "batt": 75,
    "speed": 0,
    "temp": 35,
    "volt": 48.0,
    "curr": 12.0,
    "timestamp": time.time()
}


# Dashboard Home Page
@app.route("/")
def home():
    return send_from_directory(".", "ev_dashboard (1).html")


# Dashboard fetches data from here
@app.route("/data", methods=["GET"])
def get_data():
    age = round(time.time() - latest_data["timestamp"])

    return jsonify({
        "batt": latest_data["batt"],
        "speed": latest_data["speed"],
        "temp": latest_data["temp"],
        "volt": latest_data["volt"],
        "curr": latest_data["curr"],
        "age": age
    })


# ESP32 sends data here
@app.route("/data", methods=["POST"])
def update_data():
    global latest_data

    try:
        data = request.get_json()

        latest_data["batt"] = int(data.get("batt", 0))
        latest_data["speed"] = int(data.get("speed", 0))
        latest_data["temp"] = int(data.get("temp", 0))
        latest_data["volt"] = float(data.get("volt", 0))
        latest_data["curr"] = float(data.get("curr", 0))
        latest_data["timestamp"] = time.time()

        return jsonify({
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Status Check
@app.route("/status")
def status():
    return jsonify({
        "status": "running",
        "message": "EV Dashboard Backend Online"
    })


if __name__ == "__main__":
    print("\nEV Dashboard Backend Started")
    print("Dashboard : http://localhost:5000")
    print("Status    : http://localhost:5000/status")
    print("Data API  : http://localhost:5000/data\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )