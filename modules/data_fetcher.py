import yfinance as yf
import pandas as pd

def fetch_data(symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval)
    if df.empty:
        return df

    df.reset_index(inplace=True)

    # Force the date/time index column to be named "Date"
    if 'Date' not in df.columns:
        if 'Datetime' in df.columns:
            df.rename(columns={'Datetime': 'Date'}, inplace=True)
        else:
            df.rename(columns={df.columns[0]: 'Date'}, inplace=True)

    # Capitalize all other columns safely
    df.columns = [str(col).capitalize() for col in df.columns]

    return df
