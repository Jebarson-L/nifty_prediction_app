import streamlit as st
from modules.data_fetcher import fetch_ohlcv
from modules.price_action import detect_trends, detect_support_resistance
from modules.smc_ict import compute_smc_signals
from modules.ui_helpers import plot_candles_with_signals, show_explanation

st.set_page_config(page_title="Nifty / Bank Nifty Prediction", layout="wide")

st.title("Nifty & Bank Nifty — Price Action / SMC / ICT Analysis")

# Sidebar controls
symbol = st.sidebar.text_input("Symbol (e.g. ^NSEI, BANKNIFTY)", value="^NSEI")
period = st.sidebar.selectbox("Period", ["1d", "5d", "1mo", "3mo"], index=2)
interval = st.sidebar.selectbox("Interval", ["1m","5m","15m","30m","60m","1d"], index=2)

if st.sidebar.button("Run Analysis"):
    with st.spinner("Fetching data..."):
        df = fetch_ohlcv(symbol, period=period, interval=interval)
    st.write("Data fetched:", df.tail(5))

    # Price Action
    trend_df = detect_trends(df)
    supports, resistances = detect_support_resistance(df)
    st.subheader("Price Action / Trend & Support-Resistance")
    fig1 = plot_candles_with_signals(df, supports, resistances)
    st.plotly_chart(fig1, use_container_width=True)
    show_explanation("Price Action Explanation",
        "We derived trend by comparing current close to recent rolling high/low. "
        "Support / Resistance are simple pivot points. This is basic—improve with better logic.")

    # SMC / ICT
    st.subheader("SMC / ICT Signals")
    smc_signals = compute_smc_signals(df)
    fig2 = plot_candles_with_signals(df, supports, resistances, smc_signals=smc_signals)
    st.plotly_chart(fig2, use_container_width=True)
    show_explanation("SMC / ICT Explanation",
        "Order Blocks, Fair Value Gaps, Break of Structure are computed via smartmoneyconcepts library. "
        "Interpretation: zones where institutions may act, etc.")

    # Prediction / signal summary (very naive)
    st.subheader("Prediction / Signal Summary")
    # Simple combined heuristic: if trend is up & price near support & OB zone bullish → bullish else bearish
    last_trend = trend_df["trend"].iloc[-1]
    # check if last close is within “support + small buffer”
    last_close = df["close"].iloc[-1]
    sup_prices = [p for (_, p) in supports]
    resistance_prices = [p for (_, p) in resistances]
    signal = "Neutral"
    if last_trend == "up" and len(sup_prices)>0 and abs(last_close - sup_prices[-1]) < (0.005 * last_close):
        signal = "Likely Bullish"
    elif last_trend == "down" and len(resistance_prices)>0 and abs(last_close - resistance_prices[-1]) < (0.005 * last_close):
        signal = "Likely Bearish"
    st.markdown(f"**Trend**: {last_trend}  \n**Last Close**: {last_close:.2f}  \n**Signal**: {signal}")

    st.markdown("---")
    show_explanation("Caveats / Notes",
        "This is a demo. Real predictive power requires deeper backtesting, risk management, filtering, combining with volume, multiple timeframes, confluence, etc.")
