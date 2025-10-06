import yfinance as yf
import pandas as pd

def fetch_data(symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval)
    if df.empty:
        return df

    df.reset_index(inplace=True)

    # Fix: Ensure column names are strings before capitalize
    df.columns = [str(col).capitalize() for col in df.columns]

    return df
