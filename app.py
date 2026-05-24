"""Flask backend API server for PulseCheck."""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from pulsecheck.pipeline import analyze

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    """Root endpoint — confirms the API is live."""
    return jsonify({
        "service": "PulseCheck API",
        "status": "running",
        "endpoints": {
            "POST /analyze": "Analyze article for political bias",
            "GET /languages": "List supported languages",
            "GET /health": "Health check",
        }
    }), 200


@app.route("/analyze", methods=["POST"])
def analyze_article():
    """Analyze article from URL or raw text."""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    url = data.get("url")
    text = data.get("text")

    if not url and not text:
        return jsonify({"error": "Provide 'url' or 'text' in request body"}), 400
    
    try:
        summarize_flag = data.get("summarize", False)
        bias_model = data.get("bias_model", data.get("model", "svm"))
        language_override = data.get("language_override")  # optional ISO code

        result = analyze(
            url=url,
            text=text,
            summarize_article=summarize_flag,
            bias_model=bias_model,
            language_override=language_override,
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/languages", methods=["GET"])
def supported_languages():
    """Return the list of languages supported for detection & translation."""
    from pulsecheck.language import get_supported_languages
    return jsonify(get_supported_languages()), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
