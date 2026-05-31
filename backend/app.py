import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS

from storage.storage import save_health_data, load_health_data
from storage.utils import validate_data, normalize_data, generate_recommendations
from analize.health_agent import HealthAgent

app = Flask(__name__)
CORS(app)  # permite request-uri de la React (localhost:5173)


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

    # Validare date
    is_valid, message = validate_data(data)
    if not is_valid:
        return jsonify({
            "status": "error",
            "message": message
        }), 400

    # Salvare date normalizate
    save_health_data(data)

    # Incearca AI agent (Ollama), fallback la reguli simple
    try:
        agent = HealthAgent()
        result = agent.analyze(data)
    except Exception:
        # Fallback daca Ollama nu e instalat/pornit
        recommendations = generate_recommendations(data)
        result = {
            "health_score": None,
            "health_status": "unavailable",
            "recommendations": recommendations,
            "business_insights": []
        }

    return jsonify(result)


@app.route("/health-data", methods=["GET"])
def get_health_data():
    return jsonify(load_health_data())


@app.route("/stats", methods=["GET"])
def stats():

    data = load_health_data()

    if len(data) == 0:
        return jsonify({"message": "No data available"})

    avg_hr = sum(item["heart_rate"] for item in data) / len(data)
    avg_sleep = sum(item["sleep_hours"] for item in data) / len(data)

    return jsonify({
        "records": len(data),
        "average_heart_rate": round(avg_hr, 2),
        "average_sleep_hours": round(avg_sleep, 2)
    })


@app.route("/risk-analysis", methods=["GET"])
def risk_analysis():

    data = load_health_data()
    risky = [
        item for item in data
        if item["heart_rate"] > 100 or item["sleep_hours"] < 6
    ]

    return jsonify({
        "risky_records": len(risky),
        "data": risky
    })


if __name__ == "__main__":
    app.run(debug=True)