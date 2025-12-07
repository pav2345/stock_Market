# services/indicator_service.py
import pandas as pd
import numpy as np
import os

def safe_round(value, digits=4):
    try:
        if pd.isna(value):
            return None
        return round(float(value), digits)
    except:
        return None

def _get_close_series(df):
    """
    Ensure we return a single pandas Series for 'close' prices.
    Handles cases where df['close'] is a DataFrame with tickers as columns
    by selecting the first column. Also supports alternate column names.
    """
    # Prefer lowercase 'close'
    if "close" in df.columns:
        close = df["close"]
    # fallback variations
    elif "Close" in df.columns:
        close = df["Close"]
    elif "Adj Close" in df.columns:
        close = df["Adj Close"]
    else:
        raise KeyError("No 'close' (or 'Close'/'Adj Close') column found in DataFrame")

    # If it's a DataFrame (multiple columns), squeeze it to a Series
    if isinstance(close, pd.DataFrame):
        # If only one column, take it
        if close.shape[1] == 1:
            close = close.iloc[:, 0]
        else:
            # Multiple columns (e.g., tickers). Pick first column as fallback.
            # If you want a specific ticker, change logic here to pick that column.
            close = close.iloc[:, 0]

    # Ensure index alignment and name
    close = close.rename("close")
    return close

def add_indicators_to_df(df):
    df = df.copy()

    # Normalize Date if present
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)

    # Obtain a single-series close
    close = _get_close_series(df)

    # Place the close series into df under a safe single column if not present
    # (this keeps alignment and prevents future ambiguity)
    df["close"] = close

    # ---------- SMA ----------
    df["SMA20"] = df["close"].rolling(20).mean()
    df["SMA50"] = df["close"].rolling(50).mean()

    # ---------- EMA ----------
    df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()

    # ---------- RSI ----------
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # ---------- MACD ----------
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # ---------- Bollinger Bands ----------
    mb = df["close"].rolling(20).mean()
    std20 = df["close"].rolling(20).std()

    # mb, std20 are Series -> assigning single-series columns is safe
    df["MB"] = mb
    df["Upper_BB"] = mb + 2 * std20
    df["Lower_BB"] = mb - 2 * std20

    return df

def calculate_indicators(df):
    df = add_indicators_to_df(df)

    # Guard: if df is empty, return safe None values
    if df.empty:
        return {
            "SMA20": None, "SMA50": None,
            "EMA20": None, "EMA50": None,
            "RSI": None,
            "MACD": None, "Signal": None,
            "Upper_BB": None, "Lower_BB": None, "MB": None
        }

    last = df.iloc[-1]

    return {
        "SMA20": safe_round(last.get("SMA20")),
        "SMA50": safe_round(last.get("SMA50")),
        "EMA20": safe_round(last.get("EMA20")),
        "EMA50": safe_round(last.get("EMA50")),
        "RSI": safe_round(last.get("RSI")),
        "MACD": safe_round(last.get("MACD")),
        "Signal": safe_round(last.get("Signal")),
        "Upper_BB": safe_round(last.get("Upper_BB")),
        "Lower_BB": safe_round(last.get("Lower_BB")),
        "MB": safe_round(last.get("MB"))
    }
