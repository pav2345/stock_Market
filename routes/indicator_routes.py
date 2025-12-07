from flask import Blueprint, request, jsonify
from services.data_fetcher import fetch_stock_data
from services.indicator_service import calculate_indicators, add_indicators_to_df
from services.trading_signals import generate_trading_signals
from services.indicator_service import add_indicators_to_df

indicator_bp = Blueprint("indicator", __name__)

@indicator_bp.route("/indicators/basic", methods=["POST", "OPTIONS"])
def indicators_basic():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        symbol = request.json.get("symbol")

        df = fetch_stock_data(symbol)
        if df is None:
            return {"error": "Stock not found"}, 404

        indicators = calculate_indicators(df)

        candle = df[["Date", "open", "high", "low", "close"]].tail(100).to_dict(orient="records")
        volume = df[["Date", "volume"]].tail(100).to_dict(orient="records")

        return {
            "status": "success",
            "symbol": symbol,
            "indicators": indicators,
            "candlestick": candle,
            "volume": volume
        }

    except Exception as e:
        return {"error": str(e)}, 500


@indicator_bp.route("/indicators/signals", methods=["POST", "OPTIONS"])
def indicator_signals():
    # CORS Preflight
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        from services.indicator_service import add_indicators_to_df  # ✅ FIXED IMPORT

        body = request.get_json()
        symbol = body.get("symbol")

        if not symbol:
            return {"error": "symbol is required"}, 400

        # Fetch stock data
        df = fetch_stock_data(symbol)
        if df is None or df.empty:
            return {"error": "No data found"}, 404

        # Add TA indicators safely
        df = add_indicators_to_df(df)

        # Generate final signal
        signal_result = generate_trading_signals(df)

        latest = df.iloc[-1]

        latest_indicators = {
            "SMA20": latest.get("SMA20"),
            "SMA50": latest.get("SMA50"),
            "EMA20": latest.get("EMA20"),
            "EMA50": latest.get("EMA50"),
            "RSI": latest.get("RSI"),
            "MACD": latest.get("MACD"),
            "Signal": latest.get("Signal"),
            "Upper_BB": latest.get("Upper_BB"),
            "Lower_BB": latest.get("Lower_BB"),
            "MB": latest.get("MB"),
        }

        return {
            "status": "success",
            "symbol": symbol,
            "signal": signal_result["signal"],
            "confidence": signal_result["confidence"],
            "reasons": signal_result["reasons"],
            "latest_indicators": latest_indicators
        }

    except Exception as e:
        return {"error": str(e)}, 500
