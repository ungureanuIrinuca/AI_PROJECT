from flask import Flask, request, jsonify
from storage.storage import save_health_data, load_health_data
from storage.utils import validate_data, normalize_data
from storage.utils import (
    validate_data,
    normalize_data,
    generate_recommendations
)
app = Flask(__name__)


@app.route("/")
def home():
    return "Health Monitor API works!"


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    valid, message = validate_data(data)

    if not valid:
        return jsonify({
            "status": "error",
            "message": message
        }), 400

    normalized_data = normalize_data(data)

    recommendations = generate_recommendations(data)

    save_health_data(normalized_data)

    return jsonify({
        "status": "success",
        "message": "Data analyzed successfully",
        "data": normalized_data,
        "recommendations": recommendations
    })

@app.route("/health-data", methods=["GET"])
def get_health_data():
    return jsonify(load_health_data())


@app.route("/stats", methods=["GET"])
def stats():

    data = load_health_data()

    if len(data) == 0:
        return jsonify({
            "message": "No data available"
        })

    avg_hr = sum(
        item["heart_rate"]
        for item in data
    ) / len(data)

    avg_sleep = sum(
        item["sleep_hours"]
        for item in data
    ) / len(data)

    return jsonify({
        "records": len(data),
        "average_heart_rate": round(avg_hr, 2),
        "average_sleep_hours": round(avg_sleep, 2)
    })


@app.route("/risk-analysis", methods=["GET"])
def risk_analysis():

    data = load_health_data()

    risky = []

    for item in data:

        if (
                item["heart_rate"] > 100 or
                item["sleep_hours"] < 6
        ):
            risky.append(item)

    return jsonify({
        "risky_records": len(risky),
        "data": risky
    })


if __name__ == "__main__":
    app.run(debug=True)