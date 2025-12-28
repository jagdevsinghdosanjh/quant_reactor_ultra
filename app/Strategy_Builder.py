import streamlit as st
from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.indicators import add_simple_returns
from core.engine.regime_filters import apply_trend_regime
from core.engine.volatility_filters import apply_volatility_filter
from core.engine.metrics import compute_basic_metrics
from core.utils.plotter import equity_curve_plot

st.title("🧱 Strategy Builder")

data_dir = "core/data"
files = list_csv_files(data_dir)

if not files:
    st.warning("No CSV files found in core/data")
    st.stop()

symbol_file = st.selectbox("Select Symbol", files)
symbol = symbol_file.split("/")[-1].replace(".csv", "")

st.sidebar.subheader("Filters")
use_regime = st.sidebar.checkbox("Use Trend Regime Filter", value=True)
use_vol = st.sidebar.checkbox("Use Volatility Filter", value=True)
sma_window = st.sidebar.slider("SMA Window", 50, 300, 200)
vol_quantile = st.sidebar.slider("Volatility Quantile", 0.5, 0.95, 0.8)

df = load_single_csv(symbol_file)
df = add_simple_returns(df)

mask = df["Returns"] == df["Returns"]  # start as all True, but avoid .all()
mask = mask.astype(bool)

if use_regime:
    df = apply_trend_regime(df, window=sma_window)
    mask &= df["Regime_Uptrend"]

if use_vol:
    df = apply_volatility_filter(df, quantile=vol_quantile)
    mask &= df["Vol_Filter"]

strategy_returns = df["Returns"].where(mask, 0).fillna(0)

metrics = compute_basic_metrics(strategy_returns)
equity = (1 + strategy_returns).cumprod()

st.subheader("Strategy Definition")
st.write(
    f"- Symbol: **{symbol}**\n"
    f"- Trend filter: **{use_regime}** (SMA {sma_window})\n"
    f"- Volatility filter: **{use_vol}** (quantile {vol_quantile})"
)

st.subheader("Performance")
st.json(metrics)

st.subheader("Equity Curve")
fig = equity_curve_plot(equity, title=f"{symbol} – Custom Strategy Equity")
st.plotly_chart(fig, use_container_width=True)
