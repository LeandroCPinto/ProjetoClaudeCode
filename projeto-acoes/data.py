import yfinance as yf
import pandas as pd

TICKERS = {
    "PETR4": "PETR4.SA",
    "ITUB4": "ITUB4.SA",
    "VALE3": "VALE3.SA",
}

def get_stock_data():
    frames = []
    for name, ticker in TICKERS.items():
        df = yf.download(ticker, start="2025-01-01", end="2025-12-31", auto_adjust=True, progress=False)
        if df.empty:
            continue
        df = df[["Close", "Volume"]].copy()
        df.columns = ["Close", "Volume"]
        df["Ticker"] = name
        df.index.name = "Date"
        df = df.reset_index()
        first_close = df["Close"].iloc[0]
        df["Retorno_%"] = (df["Close"] / first_close - 1) * 100
        frames.append(df)
    return pd.concat(frames, ignore_index=True)
