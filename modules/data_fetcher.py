import yfinance as yf
import pandas as pd

def fetch_ohlcv(symbol: str, period: str = "1mo", interval: str = "15m"):
    """
    Fetch OHLCV data via yfinance (or any other API).
    """
    df = yf.download(symbol, period=period, interval=interval, progress=False)
    # yfinance returns a multi‑level index for some intervals; simplify index
    df = df.reset_index()
    df.rename(columns={"Datetime":"datetime", "Date":"datetime"}, inplace=True)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime")
    # Keep relevant columns
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    # convert to lowercase column names as required by some indicator libraries
    df.columns = [c.lower() for c in df.columns]
    return df
