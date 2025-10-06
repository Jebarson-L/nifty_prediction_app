import streamlit as st
import plotly.graph_objs as go
from modules.data_fetcher import fetch_data
from modules.price_action import identify_price_action_levels

# UI Config
st.set_page_config(page_title="Nifty Price Action", layout="wide")
st.title("📈 Nifty & Bank Nifty - Price Action Analysis")

# Sidebar
symbol_map = {
    "Nifty 50": "^NSEI",
    "Bank Nifty": "^NSEBANK"
}

st.sidebar.header("Settings")
symbol_label = st.sidebar.selectbox("Select Index", list(symbol_map.keys()))
symbol = symbol_map[symbol_label]
period = st.sidebar.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y"])
interval = st.sidebar.selectbox("Interval", ["1d", "1h"])

# Fetch data
df = fetch_data(symbol, period=period, interval=interval)

if df is not None and not df.empty:
    support, resistance = identify_price_action_levels(df)

    # Plot
    st.subheader(f"{symbol_label} Candlestick Chart")
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Candles"
    )])

    # Add Support levels
    for date, level in support:
        fig.add_hline(y=level, line=dict(color="green", width=1), annotation_text="Support", opacity=0.4)

    # Add Resistance levels
    for date, level in resistance:
        fig.add_hline(y=level, line=dict(color="red", width=1), annotation_text="Resistance", opacity=0.4)

    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ No data available for the selected symbol/interval.")
