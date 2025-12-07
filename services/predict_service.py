import pandas as pd
import numpy as np
from pmdarima import auto_arima  # type: ignore
from prophet import Prophet
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import LSTM, Dense  # type: ignore


def arima_forecast(df, periods=7):
    df = df.copy()
    series = df["close"]

    model = auto_arima(
        series,
        seasonal=False,
        error_action="ignore",
        suppress_warnings=True
    )

    forecast = model.predict(n_periods=periods)
    return forecast.tolist()



def prophet_forecast(df, periods=30):
    df = df.copy()

    # 1. Fix multi-index columns
    df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]

    # 2. Ensure date column is correct
    if "date" not in df.columns:
        df = df.reset_index()

    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

    # 3. Ensure close is 1-D
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    # 4. Prophet requires ds + y
    prophet_df = pd.DataFrame({
        "ds": df["date"],
        "y": df["close"]
    })

    model = Prophet(daily_seasonality=True)
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods)

    return result.to_dict(orient="records")



def sma_predict(df, window=7):
    df = df.copy()
    close_series = df["close"]

    if len(close_series) < window:
        return None

    sma_value = close_series.tail(window).mean()
    return float(sma_value)



def linear_regression_predict(df):
    df = df.copy()
    df["index"] = np.arange(len(df))

    X = df[["index"]]
    y = df["close"]

    model = LinearRegression()
    model.fit(X, y)

    next_index = [[len(df)]]
    prediction = model.predict(next_index)[0]

    return float(prediction)



def lstm_forecast(df, look_back=60):
    df = df.copy()

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_close = scaler.fit_transform(df["close"].values.reshape(-1, 1))

    X_train, y_train = [], []

    for i in range(look_back, len(scaled_close)):
        X_train.append(scaled_close[i - look_back:i, 0])
        y_train.append(scaled_close[i, 0])

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(50))
    model.add(Dense(1))

    model.compile(optimizer="adam", loss="mse")
    model.fit(X_train, y_train, epochs=5, batch_size=32, verbose=0)

    last_look = scaled_close[-look_back:]
    last_look = np.reshape(last_look, (1, look_back, 1))

    prediction = model.predict(last_look)[0][0]
    prediction = scaler.inverse_transform([[prediction]])[0][0]

    return float(prediction)
