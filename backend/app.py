from flask import Flask, request, jsonify

from analize.analysis import (
    average_steps,
    average_calories,
    average_sleep_hours,
    average_heart_rate_dataset
)

app = Flask(__name__)


@app.route("/")
def home():
    return "Health Monitor API works!"


@app.route("/dashboard")
def dashboard():

    return jsonify({
        "average_steps": average_steps(),
        "average_calories": average_calories(),
        "average_sleep_hours": average_sleep_hours(),
        "average_heart_rate": average_heart_rate_dataset()
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    result = {
        "status": "success",
        "message": "Health data received",
        "data": data
    }

    return jsonify(result)

app.run(debug=True)