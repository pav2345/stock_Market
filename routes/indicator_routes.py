from flask import Blueprint, request, jsonify
from services.data_fetcher import fetch_stock_data
from services.indicator_service import calculate_indicators
from services.trading_signals import generate_trading_signals # type: ignore

indicator_bp = Blueprint("indicator", __name__)

@indicator_bp.route("/indicators/basic", methods=["POST"])
def indicators_basic():
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

@indicator_bp.route("/indicators/signals", methods=["POST"])
def indicator_signals():
    try:
        body = request.get_json()
        symbol = body.get("symbol")

        df = fetch_stock_data(symbol)
        if df is None or df.empty:
            return {"error": "No data found"}, 404

        from services.indicator_service import calculate_indicators

        # Calculate indicators for entire DataFrame
        full_indicators = calculate_indicators(df)

        # Attach indicators back into DF for signal generation
        df["SMA20"] = df["close"].rolling(20).mean()
        df["SMA50"] = df["close"].rolling(50).mean()
        df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()
        df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()

        delta = df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        df["RSI"] = 100 - (100 / (1 + (gain.rolling(14).mean() / loss.rolling(14).mean())))

        ema12 = df["close"].ewm(span=12, adjust=False).mean()
        ema26 = df["close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = ema12 - ema26
        df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

        df["MB"] = df["close"].rolling(20).mean()
        df["Upper_BB"] = df["MB"] + 2 * df["close"].rolling(20).std()
        df["Lower_BB"] = df["MB"] - 2 * df["close"].rolling(20).std()

        # Generate final buy/sell decision
        signal_result = generate_trading_signals(df)

        return {
            "status": "success",
            "symbol": symbol,
            "signal": signal_result["signal"],
            "confidence": signal_result["confidence"],
            "reasons": signal_result["reasons"],
            "latest_indicators": full_indicators
        }

    except Exception as e:
        return {"error": str(e)}, 500
