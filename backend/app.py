import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS

from storage.storage import save_health_data, load_health_data
from storage.utils import validate_data, normalize_data, generate_recommendations
from analize.health_agent import HealthAgent
from analize.report_generator import generate_weekly_report
from analize.analysis import calculate_health_score
from analize.trend_analysis import generate_health_insights


app = Flask(__name__)
CORS(app)

agent = HealthAgent()

@app.route("/")
def home():
    return "Health Monitor API is running!"


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    is_valid, message = validate_data(data)
    if not is_valid:
        return jsonify({"status": "error", "message": message}), 400

    save_health_data(data)

    heart_rate = data["heart_rate"]
    sleep_hours = data["sleep_hours"]
    steps = data.get("steps", 0)

    score_result = calculate_health_score(
        [heart_rate],
        sleep_hours,
        steps
    )

    recommendations = generate_recommendations(data)

    insights_result = generate_health_insights(
        [steps],
        [sleep_hours]
    )

    result = {
        "health_score": score_result["health_score"],
        "health_status": score_result["health_status"],
        "recommendations": recommendations,
        "business_insights": insights_result["insights"]
    }

    return jsonify(result)


@app.route("/agent-chat", methods=["POST"])
def agent_chat():
    """
    Endpoint pentru conversatia cu agentul AI in limbaj natural.
    Agentul decide ce tool-uri sa apeleze si raspunde utilizatorului.
    """
    body = request.json
    if not body:
        return jsonify({"status": "error", "message": "No data received"}), 400

    user_prompt = body.get("prompt", "")
    user_data = body.get("user_data", {})

    if not user_prompt:
        return jsonify({"status": "error", "message": "No prompt provided"}), 400

    try:
        result = agent.process_request(user_prompt, user_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "agent_response": "AI agent is unavailable. Make sure Ollama is running.",
            "error": str(e)
        }), 500


@app.route("/weekly-report", methods=["POST"])
def weekly_report():
    """
    Genereaza un raport saptamanal pe baza istoricului de date trimis de frontend.
    """
    body = request.json
    if not body or "history" not in body:
        return jsonify({"status": "error", "message": "No history data"}), 400

    history = body["history"]

    if len(history) < 2:
        return jsonify({"status": "error", "message": "Need at least 2 days of data"}), 400

    hr_history = [d["heart_rate"] for d in history]
    sleep_history = [d["sleep_hours"] for d in history]
    steps_history = [d["steps"] for d in history]

    report = generate_weekly_report(hr_history, sleep_history, steps_history)
    return jsonify(report)


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