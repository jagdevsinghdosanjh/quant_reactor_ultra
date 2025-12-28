import streamlit as st
from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.volatility_filters import apply_volatility_filter
from core.engine.indicators import add_simple_returns
from core.engine.metrics import compute_basic_metrics
from core.utils.plotter import equity_curve_plot

st.title("🌪️ Volatility Filter Analysis")

data_dir = "core/data"
files = list_csv_files(data_dir)

quantile = st.sidebar.slider("Volatility Quantile Threshold", 0.5, 0.95, 0.8)

if not files:
    st.warning("No CSV files found in core/data")
else:
    selected = st.selectbox("Select Symbol", files)
    symbol = selected.split("/")[-1].replace(".csv", "")

    df = load_single_csv(selected)
    df = add_simple_returns(df)
    df = apply_volatility_filter(df, quantile=quantile)

    st.subheader(f"Volatility Filter Applied (Quantile {quantile})")
    st.dataframe(df.tail())

    filtered_returns = df[df["Vol_Filter"]]["Returns"].fillna(0)
    metrics = compute_basic_metrics(filtered_returns)

    st.subheader("Performance During Low-Volatility Regime")
    st.json(metrics)

    equity = (1 + filtered_returns).cumprod()
    fig = equity_curve_plot(equity, title=f"{symbol} Low-Volatility Equity Curve")
    st.plotly_chart(fig, use_container_width=True)
