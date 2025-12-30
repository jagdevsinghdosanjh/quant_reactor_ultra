# app/Regime_Filter.py
import streamlit as st
from pathlib import Path
import pandas as pd  # noqa

from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.regime_filters import apply_trend_regime
from core.engine.indicators import add_simple_returns
from core.engine.metrics import compute_basic_metrics
from core.utils.plotter import equity_curve_plot


def main():
    st.title("📉 Regime Filter Analysis")

    # Use absolute path
    data_dir = Path("core/data").resolve()
    files = list_csv_files(str(data_dir))

    window = st.sidebar.slider("SMA Window", 50, 300, 200)

    if not files:
        st.warning("No CSV files found in core/data")
        st.stop()

    selected = st.selectbox("Select Symbol", files)
    if not selected:
        st.warning("No symbol selected")
        st.stop()

    try:
        df = load_single_csv(selected)
        df = add_simple_returns(df)
        df = apply_trend_regime(df, window=window)
    except Exception as e:
        st.error(f"Error loading or processing file: {e}")
        st.stop()

    symbol = Path(selected).stem

    st.subheader(f"Regime Filter Applied (SMA {window})")
    st.dataframe(df.tail())

    # Filter returns
    filtered_returns = df[df["Regime_Uptrend"]]["Returns"].fillna(0)
    metrics = compute_basic_metrics(filtered_returns)

    st.subheader("Performance During Uptrend Regime")
    st.json(metrics)

    # Plot
    equity = (1 + filtered_returns).cumprod()
    fig = equity_curve_plot(
        equity,
        title=f"{symbol} Uptrend Regime Equity Curve"
    )
    st.plotly_chart(fig, width='stretch')

# import streamlit as st
# from pathlib import Path
# import pandas as pd #noqa

# from core.utils.helpers import list_csv_files
# from core.engine.loader import load_single_csv
# from core.engine.regime_filters import apply_trend_regime
# from core.engine.indicators import add_simple_returns
# from core.engine.metrics import compute_basic_metrics
# from core.utils.plotter import equity_curve_plot

# st.title("📉 Regime Filter Analysis")

# # Use absolute path
# data_dir = Path("core/data").resolve()
# files = list_csv_files(str(data_dir))

# window = st.sidebar.slider("SMA Window", 50, 300, 200)

# if not files:
#     st.warning("No CSV files found in core/data")
#     st.stop()

# selected = st.selectbox("Select Symbol", files)
# if not selected:
#     st.warning("No symbol selected")
#     st.stop()

# try:
#     df = load_single_csv(selected)
#     df = add_simple_returns(df)
#     df = apply_trend_regime(df, window=window)
# except Exception as e:
#     st.error(f"Error loading or processing file: {e}")
#     st.stop()

# symbol = Path(selected).stem

# st.subheader(f"Regime Filter Applied (SMA {window})")
# st.dataframe(df.tail())

# # Filter returns
# filtered_returns = df[df["Regime_Uptrend"]]["Returns"].fillna(0)
# metrics = compute_basic_metrics(filtered_returns)

# st.subheader("Performance During Uptrend Regime")
# st.json(metrics)

# # Plot
# equity = (1 + filtered_returns).cumprod()
# fig = equity_curve_plot(equity, title=f"{symbol} Uptrend Regime Equity Curve")
# st.plotly_chart(fig, width='stretch')
# # st.plotly_chart(fig, width='stretch')

