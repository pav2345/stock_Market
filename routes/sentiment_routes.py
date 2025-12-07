from flask import Blueprint, request, jsonify
from services.sentiment_service import analyze_sentiment

sentiment_bp = Blueprint("sentiment", __name__)

@sentiment_bp.route("/sentiment/analyze", methods=["POST"])
def sentiment_analyze():
    try:
        # Accept both text and symbol
        body = request.get_json()

        text = body.get("text")
        symbol = body.get("symbol")

        # If text is missing but symbol is given → use symbol as text
        if not text and symbol:
            text = symbol

        # If still missing → error
        if not text:
            return {"error": "News text or stock symbol is required"}, 400

        # Run analysis
        output = analyze_sentiment(text)

        return {
            "status": "success",
            "analysis": output,
            "input_used": text
        }

    except Exception as e:
        return {"error": str(e)}, 500
