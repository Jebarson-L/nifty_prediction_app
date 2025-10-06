import yfinance as yf
import pandas as pd

def fetch_data(symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval)
    if df.empty:
        return df

    # Reset index and rename the time column to 'Date'
    df.reset_index(inplace=True)

    # Find the time column (usually first column) and rename to 'Date'
    time_col = df.columns[0]
    df.rename(columns={time_col: 'Date'}, inplace=True)

    # Ensure other columns are consistently capitalized
    df.columns = [str(col).capitalize() for col in df.columns]

    return df
