def generate_trading_signals(df):
    df = df.copy()
    last = df.iloc[-1]

    reasons = []
    score = 0

    
    if last["RSI"] < 30:
        reasons.append("RSI indicates oversold → BUY")
        score += 30
    elif last["RSI"] > 70:
        reasons.append("RSI indicates overbought → SELL")
        score += 30

    
    if last["MACD"] > last["Signal"]:
        reasons.append("MACD crossed above Signal → BUY trend")
        score += 25
    else:
        reasons.append("MACD below Signal → SELL trend")
        score += 25

    if last["EMA20"] > last["EMA50"]:
        reasons.append("EMA20 above EMA50 → Uptrend (BUY)")
        score += 20
    else:
        reasons.append("EMA20 below EMA50 → Downtrend (SELL)")
        score += 20


    if last["close"] < last["Lower_BB"]:
        reasons.append("Price below Lower BB → BUY bounce")
        score += 15
    elif last["close"] > last["Upper_BB"]:
        reasons.append("Price above Upper BB → SELL pullback")
        score += 15

   
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
