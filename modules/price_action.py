import pandas as pd

def identify_price_action_levels(df: pd.DataFrame):
    """
    Simple price action logic: detect support/resistance zones.
    """
    support = []
    resistance = []

    for i in range(2, len(df) - 2):
        if df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i+1]:
            support.append((df['Date'][i], df['Low'][i]))

        if df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i+1]:
            resistance.append((df['Date'][i], df['High'][i]))

    return support, resistance
