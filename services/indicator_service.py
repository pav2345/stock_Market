import pandas as pd
import numpy as np

# ------------------------------------------------------
# FUNCTION 1: Add all indicators into the DataFrame
# ------------------------------------------------------
def add_indicators_to_df(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)

    # SMA
    df["SMA20"] = df["close"].rolling(20).mean()
    df["SMA50"] = df["close"].rolling(50).mean()

    # EMA
    df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    df["MB"] = df["close"].rolling(20).mean()
    df["Upper_BB"] = df["MB"] + 2 * df["close"].rolling(20).std()
    df["Lower_BB"] = df["MB"] - 2 * df["close"].rolling(20).std()

    return df


# ------------------------------------------------------
# FUNCTION 2: Return only the last calculated values
# ------------------------------------------------------
def calculate_indicators(df):
    df = add_indicators_to_df(df)
    last = df.iloc[-1]

    return {
        "SMA20": round(last["SMA20"], 4),
        "SMA50": round(last["SMA50"], 4),
        "EMA20": round(last["EMA20"], 4),
        "EMA50": round(last["EMA50"], 4),
        "RSI": round(last["RSI"], 4),
        "MACD": round(last["MACD"], 4),
        "Signal": round(last["Signal"], 4),
        "Upper_BB": round(last["Upper_BB"], 4),
        "Lower_BB": round(last["Lower_BB"], 4)
    }
