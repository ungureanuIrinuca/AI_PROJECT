from flask import Flask, request, jsonify

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

    result = {
        "status": "success",
        "message": "Health data received",
        "data": data
    }

    return jsonify(result)

app.run(debug=True)