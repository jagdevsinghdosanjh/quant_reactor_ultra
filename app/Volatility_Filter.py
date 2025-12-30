# #Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
# #app/Volatility_Filter.py
# app/Volatility_Filter.py
import streamlit as st
import os
from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.volatility_filters import apply_volatility_filter
from core.engine.indicators import add_simple_returns
from core.engine.metrics import compute_basic_metrics
from core.utils.plotter import equity_curve_plot

def main():
    st.title("🌪️ Volatility Filter Analysis")

    data_dir = "core/data"
    files = list_csv_files(data_dir)

    quantile = st.sidebar.slider("Volatility Quantile Threshold", 0.5, 0.95, 0.8)

    if not files:
        st.warning("No CSV files found in core/data")
        st.stop()

    selected = st.selectbox("Select Symbol", files)
    symbol = os.path.splitext(os.path.basename(selected))[0]

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
    fig = equity_curve_plot(
        equity,
        title=f"{symbol} Low-Volatility Equity Curve"
    )
    st.plotly_chart(fig, width='stretch')

# import streamlit as st
# import os
# from core.utils.helpers import list_csv_files
# from core.engine.loader import load_single_csv
# from core.engine.volatility_filters import apply_volatility_filter
# from core.engine.indicators import add_simple_returns
# from core.engine.metrics import compute_basic_metrics
# from core.utils.plotter import equity_curve_plot

# st.title("🌪️ Volatility Filter Analysis")

# data_dir = "core/data"
# files = list_csv_files(data_dir)

# quantile = st.sidebar.slider("Volatility Quantile Threshold", 0.5, 0.95, 0.8)

# if not files:
#     st.warning("No CSV files found in core/data")
#     selected = st.selectbox("Select Symbol", files)
#     # ensure selected is not None (selectbox may return None in some contexts)
#     selected = selected or files[0]
#     # use os.path to handle different path separators and remove extension safely
#     symbol = os.path.splitext(os.path.basename(selected))[0]

#     df = load_single_csv(selected)
#     df = add_simple_returns(df)
#     df = apply_volatility_filter(df, quantile=quantile)
#     df = apply_volatility_filter(df, quantile=quantile)

#     st.subheader(f"Volatility Filter Applied (Quantile {quantile})")
#     st.dataframe(df.tail())

#     filtered_returns = df[df["Vol_Filter"]]["Returns"].fillna(0)
#     metrics = compute_basic_metrics(filtered_returns)

#     st.subheader("Performance During Low-Volatility Regime")
#     st.json(metrics)

#     equity = (1 + filtered_returns).cumprod()
#     fig = equity_curve_plot(equity, title=f"{symbol} Low-Volatility Equity Curve")
#     st.plotly_chart(fig, width="stretch")
