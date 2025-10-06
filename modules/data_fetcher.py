import yfinance as yf
import pandas as pd

def fetch_data(symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval)

    if df.empty:
        return df

    # Print columns and index info for debugging (remove later)
    print("Columns before reset_index():", df.columns)
    print("Index name/type before reset_index():", df.index.name, type(df.index))

    df.reset_index(inplace=True)

    print("Columns after reset_index():", df.columns)

    # Robust rename: rename first column to 'Date'
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)

    # Capitalize other columns
    df.columns = [str(col).capitalize() for col in df.columns]

    print("Final columns:", df.columns)

    return df
