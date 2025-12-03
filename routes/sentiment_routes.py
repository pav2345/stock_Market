from flask import Blueprint, request, jsonify
from services.sentiment_service import analyze_sentiment

sentiment_bp = Blueprint("sentiment", __name__)

@sentiment_bp.route("/sentiment/analyze", methods=["POST"])
def sentiment_analyze():
    try:
        text = request.json.get("text")

        if not text:
            return {"error": "News text is required"}, 400

        output = analyze_sentiment(text)
        return {"status": "success", "analysis": output}

    except Exception as e:
        return {"error": str(e)}, 500
