def generate_trading_signals(df):
    df = df.copy()
    last = df.iloc[-1]

    reasons = []
    score = 0  # confidence score out of 100

    # ---------------- RSI ----------------
    if last["rsi"] < 30:
        reasons.append("RSI indicates oversold → BUY")
        score += 30
    elif last["rsi"] > 70:
        reasons.append("RSI indicates overbought → SELL")
        score += 30

    # ---------------- MACD CROSSOVER ----------------
    if last["macd"] > last["signal"]:
        reasons.append("MACD crossed above Signal → BUY trend")
        score += 25
    else:
        reasons.append("MACD below Signal → SELL trend")
        score += 25

    # ---------------- EMA CROSSOVER ----------------
    if last["ema20"] > last["ema50"]:
        reasons.append("EMA20 crossed above EMA50 → Uptrend (BUY)")
        score += 20
    else:
        reasons.append("EMA20 below EMA50 → Downtrend (SELL)")
        score += 20

    # ---------------- BOLLINGER BANDS ----------------
    if last["close"] < last["lower_bb"]:
        reasons.append("Price below Lower Bollinger Band → BUY bounce")
        score += 15
    elif last["close"] > last["upper_bb"]:
        reasons.append("Price above Upper Bollinger Band → SELL pullback")
        score += 15

    # ------------ Final Signal Decision ------------
    if score >= 70:
        final_signal = "BUY"
    elif score <= 40:
        final_signal = "SELL"
    else:
        final_signal = "HOLD"

    return {
        "signal": final_signal,
        "confidence": score,
        "reasons": reasons
    }
