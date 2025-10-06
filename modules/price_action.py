import pandas as pd

def identify_price_action_levels(df: pd.DataFrame):
    """
    Basic Price Action Strategy:
    Detect support and resistance zones using swing highs/lows.
    """
    if 'Low' not in df.columns or 'High' not in df.columns or 'Date' not in df.columns:
        return [], []

    support = []
    resistance = []

    for i in range(2, len(df) - 2):
        if df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i+1]:
            support.append((df['Date'][i], df['Low'][i]))

        if df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i+1]:
            resistance.append((df['Date'][i], df['High'][i]))

    return support, resistance
