from flask import Blueprint, request, jsonify
import yfinance as yf

utility_bp = Blueprint("utility_bp", __name__)

@utility_bp.route("/utility/check", methods=["GET"])
def check_stock():
    try:
        symbol = request.args.get("symbol")

        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400

        data = yf.Ticker(symbol).history(period="1d")

        if data is None or data.empty:
            return jsonify({"exists": False}), 404

        return jsonify({"exists": True})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
