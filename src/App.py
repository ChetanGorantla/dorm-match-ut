from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import logging


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Authorization"])

@app.before_request
def handle_options():
    
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response, 200

@app.route('/ut-prediction', methods=['GET', 'POST'])
def calculate_score():
    try:
        if request.method == "GET":
            
            occupants = request.args.get("occupants")
            bathroom = request.args.get("bathroom")
            budget = request.args.get("budget")
            accommodation = request.args.get("accommodation")

        elif request.method == "POST":
            
            data = request.json
            occupants = data.get("occupants")
            bathroom = data.get("bathroom")
            budget = data.get("budget")
            accommodation = data.get("accommodation")

        if None in [occupants, bathroom, budget, accommodation]:
            return jsonify({"error": "Missing required fields"}), 400

        
        return jsonify({"top3": "mock_top3", "top10": "mock_top10"}), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
