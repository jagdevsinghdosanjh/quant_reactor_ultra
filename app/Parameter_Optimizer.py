#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#app/Parameter_Optimizer.py

# app/Parameter_Optimizer.py
import streamlit as st
import pandas as pd
from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.indicators import add_simple_returns
from core.engine.metrics import compute_basic_metrics
from core.engine.optimizer import simple_parameter_sweep
from core.utils.plotter import equity_curve_plot


def example_strategy_fn(df: pd.DataFrame, params: dict) -> pd.Series:
    """Example strategy: SMA crossover using window from params."""
    window = params["window"]
    sma = df["Close"].rolling(window).mean()
    returns = df["Returns"] * (df["Close"] > sma).shift(1).fillna(False)
    return returns


def main():
    st.title("🔧 Parameter Optimization")

    data_dir = "core/data"
    files = list_csv_files(data_dir)

    if not files:
        st.warning("No CSV files found in core/data")
        st.stop()

    selected = st.selectbox("Select Symbol", files)
    df = load_single_csv(selected)
    df = add_simple_returns(df)

    # Sidebar parameter grid
    st.sidebar.subheader("Optimization Settings")
    min_window = st.sidebar.number_input("Min Window", 5, 200, 20)
    max_window = st.sidebar.number_input("Max Window", 10, 300, 50)
    step = st.sidebar.number_input("Step", 1, 50, 5)

    # Build parameter grid
    param_grid = {
        "window": list(range(min_window, max_window + 1, step))
    }

    # Run optimization
    results = simple_parameter_sweep(
        data=df,
        param_grid=param_grid,
        strategy_fn=example_strategy_fn,
        metric_fn=compute_basic_metrics
    )

    st.subheader("Optimization Results")
    st.dataframe(results)

    # Plot best equity curve
    best_row = results.sort_values("Total Return", ascending=False).iloc[0]
    best_window = best_row["window"]

    st.success(f"Best window: {best_window}")

    # Recompute best equity curve
    best_returns = example_strategy_fn(df, {"window": best_window})
    equity = (1 + best_returns).cumprod()

    fig = equity_curve_plot(
        equity,
        title=f"Best Parameter Equity Curve (window={best_window})"
    )
    st.plotly_chart(fig, width="stretch")

# # app/Parameter_Optimizer.py
# import streamlit as st
# import pandas as pd #noqa
# from core.utils.helpers import list_csv_files
# from core.engine.loader import load_single_csv
# from core.engine.indicators import add_simple_returns
# from core.engine.metrics import compute_basic_metrics #noqa
# from core.engine.optimizer import run_parameter_search   # example — adjust to your actual function
# from core.utils.plotter import equity_curve_plot


# def main():
#     st.title("🔧 Parameter Optimization")

#     data_dir = "core/data"
#     files = list_csv_files(data_dir)

#     if not files:
#         st.warning("No CSV files found in core/data")
#         st.stop()

#     selected = st.selectbox("Select Symbol", files)
#     df = load_single_csv(selected)
#     df = add_simple_returns(df)

#     # Example parameter inputs — adjust to your actual optimizer
#     st.sidebar.subheader("Optimization Settings")
#     min_window = st.sidebar.number_input("Min Window", 5, 200, 20)
#     max_window = st.sidebar.number_input("Max Window", 10, 300, 50)
#     step = st.sidebar.number_input("Step", 1, 50, 5)

#     # Run optimization
#     results = run_parameter_search(df, min_window, max_window, step)

#     st.subheader("Optimization Results")
#     st.dataframe(results)

#     # Plot best equity curve
#     best_equity = results["Best_Equity_Curve"]
#     fig = equity_curve_plot(best_equity, title="Best Parameter Equity Curve")
#     st.plotly_chart(fig, width="stretch")


# import streamlit as st
# import pandas as pd #NOQA
# from core.utils.helpers import list_csv_files
# from core.engine.loader import load_single_csv
# from core.engine.indicators import add_simple_returns
# from core.engine.optimizer import simple_parameter_sweep
# from core.engine.metrics import compute_basic_metrics

# st.title("🧪 Parameter Optimization")

# data_dir = "core/data"
# files = list_csv_files(data_dir)

# if not files:
#     st.warning("No CSV files found in core/data")
# else:
#     selected = st.selectbox("Select Symbol", files)
#     # Guard against selected being None and use os.path.basename for cross-platform paths
#     if selected:
#         import os
#         symbol = os.path.basename(selected).replace(".csv", "")
#     else:
#         symbol = ""

#     if not selected:
#         st.warning("No symbol selected")
#     else:
#         df = load_single_csv(selected)
#         df = add_simple_returns(df)
#         returns = df["Returns"]

#         st.sidebar.subheader("Parameter Grid")

#         sma_values = st.sidebar.multiselect("SMA Window", [50, 100, 150, 200], default=[100, 200])
#         vol_q_values = st.sidebar.multiselect("Volatility Quantile", [0.7, 0.8, 0.9], default=[0.8])

#         param_grid = {
#             "sma_window": sma_values,
#             "vol_quantile": vol_q_values,
#         }

#         def strategy_fn(df, params):
#             from core.engine.regime_filters import apply_trend_regime
#             from core.engine.volatility_filters import apply_volatility_filter

#             df = apply_trend_regime(df, window=params["sma_window"])
#             df = apply_volatility_filter(df, quantile=params["vol_quantile"])
#             mask = df["Regime_Uptrend"] & df["Vol_Filter"]
#             return df["Returns"].where(mask, 0).fillna(0)

#         if st.button("Run Optimization"):
#             results = simple_parameter_sweep(
#                 df,
#                 param_grid,
#                 strategy_fn=strategy_fn,
#                 metric_fn=lambda r: compute_basic_metrics(r)
#             )

#             st.subheader("Optimization Results")
#             st.dataframe(results)

#             best = results.sort_values("CAGR", ascending=False).iloc[0]
#             st.success(f"Best Parameters: {best.to_dict()}")
