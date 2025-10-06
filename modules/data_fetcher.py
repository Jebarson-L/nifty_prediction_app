import yfinance as yf
import pandas as pd

def fetch_data(symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval)
    df.reset_index(inplace=True)
    return df
