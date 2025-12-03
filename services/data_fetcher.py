import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol, period="6mo", interval="1d"):
    df = yf.download(symbol, period=period, interval=interval)

    if df is None or df.empty:
        return None

    df = df.reset_index()

    df.rename(columns={
        "Date": "Date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adjclose",
        "Volume": "volume"
    }, inplace=True)

    df["Date"] = pd.to_datetime(df["Date"])

    return df
