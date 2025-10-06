import streamlit as st
import plotly.graph_objs as go
from modules.data_fetcher import fetch_data
from modules.price_action import identify_price_action_levels

st.set_page_config(page_title="Nifty Price Action", layout="wide")

st.title("📈 Nifty & Bank Nifty - Price Action Analysis")
symbol = st.selectbox("Choose Symbol", ["^NSEI", "^NSEBANK"])  # Nifty, Bank Nifty
period = st.selectbox("Choose Time Period", ["1mo", "3mo", "6mo", "1y", "2y"])
interval = st.selectbox("Choose Interval", ["1d", "1h"])

df = fetch_data(symbol, period=period, interval=interval)

if df is not None and not df.empty:
    st.subheader("Candlestick Chart with Price Action Levels")
    st.write("Data columns:", df.columns)
st.dataframe(df.head())
    support, resistance = identify_price_action_levels(df)

    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Price"
    )])

    for date, level in support:
        fig.add_hline(y=level, line=dict(color="green", width=1), annotation_text="Support", opacity=0.5)

    for date, level in resistance:
        fig.add_hline(y=level, line=dict(color="red", width=1), annotation_text="Resistance", opacity=0.5)

    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data found for selected symbol.")
