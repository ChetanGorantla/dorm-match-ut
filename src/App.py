from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*",  # ✅ Allow all origins temporarily for debugging
                             "methods": ["GET", "POST", "OPTIONS"], 
                             "allow_headers": ["Content-Type", "Authorization"],
                             "supports_credentials": True}})

@app.before_request
def handle_options():
    """ ✅ Handle Preflight Requests (OPTIONS) """
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response, 200  # ✅ Return HTTP 200 OK

@app.route('/ut-prediction', methods=['POST'])
def calculate_score():
    try:
        data = request.json
        occupants = data.get("occupants")
        bathroom = data.get("bathroom")
        budget = data.get("budget")
        accommodation = data.get("accommodation")

        if None in [occupants, bathroom, budget, accommodation]:
            return jsonify({"error": "Missing required fields"}), 400

        response = jsonify({"top3": "mock_top3", "top10": "mock_top10"})
        response.headers["Access-Control-Allow-Origin"] = "*"  # ✅ Explicitly set for response
        return response, 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
