#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#app/MultiStrategy_Portfolio.py
import streamlit as st
import pandas as pd
from pathlib import Path
from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.indicators import add_simple_returns
from core.engine.regime_filters import apply_trend_regime
from core.engine.volatility_filters import apply_volatility_filter
from core.utils.plotter import equity_curve_plot

st.title("💼 Multi-Strategy Portfolio Optimizer")
data_dir = "core/data"
files = list_csv_files(data_dir)

if not files:
    st.warning("No CSV files found in core/data")
    st.stop()

selected = st.selectbox("Select Symbol", files)
if selected is None:
    st.warning("No symbol selected.")
    st.stop()
# use pathlib to safely get the filename without extension
symbol = Path(selected).stem
symbol = selected.split("/")[-1].replace(".csv", "")

df = load_single_csv(selected)
df = add_simple_returns(df)

sma_window = st.sidebar.slider("SMA Window", 50, 300, 200)
vol_q = st.sidebar.slider("Volatility Quantile", 0.5, 0.95, 0.8)

# Build strategy returns
base = df["Returns"].fillna(0)

df_reg = apply_trend_regime(df.copy(), window=sma_window)
regime = df_reg["Returns"].where(df_reg["Regime_Uptrend"], 0).fillna(0)

df_vol = apply_volatility_filter(df.copy(), quantile=vol_q)
vol = df_vol["Returns"].where(df_vol["Vol_Filter"], 0).fillna(0)

df_both = apply_trend_regime(df.copy(), window=sma_window)
df_both = apply_volatility_filter(df_both, quantile=vol_q)
both = df_both["Returns"].where(df_both["Regime_Uptrend"] & df_both["Vol_Filter"], 0).fillna(0)

st.sidebar.subheader("Strategy Weights")
w_base = st.sidebar.slider("Weight: Baseline", 0.0, 1.0, 0.25, 0.05)
w_reg = st.sidebar.slider("Weight: Regime", 0.0, 1.0, 0.25, 0.05)
w_vol = st.sidebar.slider("Weight: Volatility", 0.0, 1.0, 0.25, 0.05)
w_both = st.sidebar.slider("Weight: Regime + Vol", 0.0, 1.0, 0.25, 0.05)

total_w = w_base + w_reg + w_vol + w_both
if total_w == 0:
    st.warning("All weights are zero. Please set at least one non-zero weight.")
else:
    w_base /= total_w
    w_reg /= total_w
    w_vol /= total_w
    w_both /= total_w

    combined = (
        w_base * base +
        w_reg * regime +
        w_vol * vol +
        w_both * both
    )

    equity = (1 + combined).cumprod()
    st.subheader("Combined Strategy Equity Curve")
    fig = equity_curve_plot(equity, title=f"{symbol} – Multi-Strategy Portfolio")
    st.plotly_chart(fig, width="stretch")

    df_out = pd.DataFrame({
        "Date": df["Date"],
        "Baseline": base,
        "Regime": regime,
        "Volatility": vol,
        "Regime+Vol": both,
        "Combined": combined,
    })
    st.dataframe(df_out.tail())
