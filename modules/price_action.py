import pandas as pd
import numpy as np

def detect_trends(df: pd.DataFrame, window: int = 5):
    """
    A naive trend detection: compare rolling minima & maxima.
    Returns signals DataFrame with 'trend' column: "up", "down", or "sideways".
    """
    df = df.copy()
    df["high_roll"] = df["high"].rolling(window).max()
    df["low_roll"] = df["low"].rolling(window).min()
    df["trend"] = np.where(df["close"] >= df["high_roll"].shift(1), "up",
                    np.where(df["close"] <= df["low_roll"].shift(1), "down", "sideways"))
    return df

def detect_support_resistance(df: pd.DataFrame, lookback: int = 20):
    """
    Very naive support/resistance: local pivot highs and lows.
    Returns lists of (timestamp, price) as support & resistance.
    """
    supports = []
    resistances = []
    for i in range(lookback, len(df)-lookback):
        segment = df["low"].iloc[i-lookback:i+lookback+1]
        if df["low"].iloc[i] == segment.min():
            supports.append((df.index[i], df["low"].iloc[i]))
        segment2 = df["high"].iloc[i-lookback:i+lookback+1]
        if df["high"].iloc[i] == segment2.max():
            resistances.append((df.index[i], df["high"].iloc[i]))
    return supports, resistances
