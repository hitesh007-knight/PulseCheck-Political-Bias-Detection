"""Flask backend API server for PulseCheck."""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from pulsecheck.pipeline import analyze

app = Flask(__name__)
CORS(app)


@app.route("/analyze", methods=["POST"])
def analyze_article():
    """Analyze article from URL."""
    data = request.get_json()
    
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400
    
    try:
        url = data["url"]
        summarize_flag = data.get("summarize", False)
        
        result = analyze(url, summarize_article=summarize_flag)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)

