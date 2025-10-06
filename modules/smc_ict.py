from smartmoneyconcepts import smc
import pandas as pd

def compute_smc_signals(df: pd.DataFrame):
    """
    Use smartmoneyconcepts package to compute SMC / ICT style zones & signals.
    Returns the (possibly annotated) DataFrame plus some auxiliary signals.
    """
    # the smc package expects lowercase columns: open, high, low, close
    df2 = df.copy().reset_index(drop=False)
    # but smartmoneyconcepts likely needs a DataFrame with these columns
    smc_obj = smc(df2)
    # get order blocks, fair value gaps, etc.
    order_blocks = smc_obj.order_blocks()
    fvg = smc_obj.fvg()
    structure = smc_obj.structure()
    # You can also get bullish/bearish zones, liquidity sweeps etc.
    return {
        "order_blocks": order_blocks,
        "fvg": fvg,
        "structure": structure,
    }
