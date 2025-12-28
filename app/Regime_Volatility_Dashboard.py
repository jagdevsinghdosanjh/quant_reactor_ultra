import streamlit as st
import pandas as pd #NOQA
import os
from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.indicators import add_simple_returns
from core.engine.regime_filters import apply_trend_regime
from core.engine.volatility_filters import apply_volatility_filter
from core.engine.metrics import compute_basic_metrics
from core.utils.plotter import equity_curve_plot

st.title("📊 Regime + Volatility Dashboard")

# Resolve data_dir relative to the repository root (app/ -> project root),
# so core/data is found regardless of CWD.
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core", "data")

files = list_csv_files(data_dir)

if not files:
    st.warning("No CSV files found in core/data")
    st.stop()

selected = st.selectbox("Select Symbol", files)
if selected is None:
    st.warning("No symbol selected")
    st.stop()

# use os.path to handle different path separators and safely remove the .csv extension
symbol = os.path.splitext(os.path.basename(selected))[0]
symbol = selected.split("/")[-1].replace(".csv", "")

col1, col2 = st.sidebar.columns(2)
sma_window = col1.slider("SMA Window", 50, 300, 200)
vol_q = col2.slider("Volatility Quantile", 0.5, 0.95, 0.8)

df = load_single_csv(selected)
df = add_simple_returns(df)
df = apply_trend_regime(df, window=sma_window)
df = apply_volatility_filter(df, quantile=vol_q)

st.subheader(f"{symbol} – Filter Masks (tail)")
st.dataframe(df[["Date", "Regime_Uptrend", "Vol_Filter"]].tail())

mask_up = df["Regime_Uptrend"]
mask_low_vol = df["Vol_Filter"]
mask_both = mask_up & mask_low_vol

modes = {
    "All Returns": df["Returns"],
    "Uptrend Only": df["Returns"].where(mask_up, 0),
    "Low Volatility Only": df["Returns"].where(mask_low_vol, 0),
    "Uptrend + Low Volatility": df["Returns"].where(mask_both, 0),
}

tab_all, tab_up, tab_vol, tab_both = st.tabs(list(modes.keys()))

for tab, (name, rets) in zip((tab_all, tab_up, tab_vol, tab_both), modes.items()):
    with tab:
        rets = rets.fillna(0)
        metrics = compute_basic_metrics(rets)
        equity = (1 + rets).cumprod()
        st.markdown(f"### {name}")
        st.json(metrics)
        fig = equity_curve_plot(equity, title=f"{symbol} – {name}")
        st.plotly_chart(fig, width="stretch")
