import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol, period="6mo", interval="1d"):
    df = yf.download(symbol, period=period, interval=interval)

    if df is None or df.empty:
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]

    new_cols = {}
    for col in df.columns:
        lc = col.lower()
        if "open" in lc and "adj" not in lc:
            new_cols[col] = "open"
        elif "high" in lc:
            new_cols[col] = "high"
        elif "low" in lc:
            new_cols[col] = "low"
        elif "close" in lc and "adj" not in lc:
            new_cols[col] = "close"
        elif "adj" in lc:
            new_cols[col] = "adjclose"
        elif "volume" in lc:
            new_cols[col] = "volume"

    df.rename(columns=new_cols, inplace=True)
    df = df.reset_index()

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)

    return df
