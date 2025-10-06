import streamlit as st
import plotly.graph_objs as go

def plot_candles_with_signals(df, supports, resistances, smc_signals=None):
    """Plot OHLC candlesticks, overlay support/resistance and SMC zones."""
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Price"
    ))

    # plot supports & resistances
    for (ts, price) in supports:
        fig.add_trace(go.Scatter(x=[ts], y=[price], mode="markers", marker=dict(color="green", size=6), name="Support"))
    for (ts, price) in resistances:
        fig.add_trace(go.Scatter(x=[ts], y=[price], mode="markers", marker=dict(color="red", size=6), name="Resistance"))

    # Optionally overlay SMC zones
    if smc_signals is not None:
        # e.g. order_blocks is a list of zones
        obs = smc_signals.get("order_blocks", [])
        # assuming each "ob" is dict or tuple with time and price
        for ob in obs:
            # this is pseudocode — adapt to your library’s output
            t = ob["time"] if "time" in ob else None
            price = ob["price"] if "price" in ob else None
            if t and price:
                fig.add_trace(go.Scatter(x=[t], y=[price], mode="markers", marker=dict(color="blue", size=8), name="OB"))
    fig.update_layout(xaxis_rangeslider_visible=False, height=600, width=900)
    return fig

def show_explanation(title: str, text: str):
    st.markdown(f"**{title}**")
    st.markdown(text)
