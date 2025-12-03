from flask import Blueprint, request, jsonify
from services.data_fetcher import fetch_stock_data
from services.predict_service import (
    arima_forecast,
    prophet_forecast,
    sma_predict,
    linear_regression_predict,
    lstm_forecast
)

predict_bp = Blueprint("predict", __name__)


# ------------------------- ARIMA -------------------------
@predict_bp.route("/predict/arima", methods=["POST"])
def predict_arima():
    try:
        body = request.get_json()
        symbol = body.get("symbol")
        days = body.get("days", 7)

        df = fetch_stock_data(symbol)
        if df is None or df.empty:
            return jsonify({"error": "No data found"}), 404

        output = arima_forecast(df, periods=days)

        return jsonify({
            "status": "success",
            "model": "arima",
            "symbol": symbol,
            "forecast": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ------------------------- PROPHET -------------------------
@predict_bp.route("/predict/prophet", methods=["POST"])
def predict_prophet():
    try:
        body = request.get_json()
        symbol = body.get("symbol")
        days = body.get("days", 30)

        df = fetch_stock_data(symbol)
        if df is None or df.empty:
            return jsonify({"error": "No data found"}), 404

        output = prophet_forecast(df, periods=days)

        return jsonify({
            "status": "success",
            "model": "prophet",
            "symbol": symbol,
            "forecast": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ------------------------- SMA -------------------------
@predict_bp.route("/predict/sma", methods=["POST"])
def predict_sma():
    try:
        body = request.get_json()
        symbol = body.get("symbol")
        window = body.get("window", 7)

        df = fetch_stock_data(symbol)
        output = sma_predict(df, window=window)

        return jsonify({
            "status": "success",
            "model": "simple_moving_average",
            "symbol": symbol,
            "prediction": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ------------------------- LINEAR REGRESSION -------------------------
@predict_bp.route("/predict/linear", methods=["POST"])
def predict_linear():
    try:
        body = request.get_json()
        symbol = body.get("symbol")

        df = fetch_stock_data(symbol)
        output = linear_regression_predict(df)

        return jsonify({
            "status": "success",
            "model": "linear_regression",
            "symbol": symbol,
            "prediction": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ------------------------- LSTM -------------------------
@predict_bp.route("/predict/lstm", methods=["POST"])
def predict_lstm():
    try:
        body = request.get_json()
        symbol = body.get("symbol")

        df = fetch_stock_data(symbol)
        output = lstm_forecast(df)

        return jsonify({
            "status": "success",
            "model": "lstm",
            "symbol": symbol,
            "prediction": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
