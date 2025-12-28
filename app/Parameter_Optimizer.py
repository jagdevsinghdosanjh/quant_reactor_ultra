import streamlit as st
import pandas as pd
from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.indicators import add_simple_returns
from core.engine.optimizer import simple_parameter_sweep
from core.engine.metrics import compute_basic_metrics

st.title("🧪 Parameter Optimization")

data_dir = "core/data"
files = list_csv_files(data_dir)

if not files:
    st.warning("No CSV files found in core/data")
else:
    selected = st.selectbox("Select Symbol", files)
    # Guard against selected being None and use os.path.basename for cross-platform paths
    if selected:
        import os
        symbol = os.path.basename(selected).replace(".csv", "")
    else:
        symbol = ""

    df = load_single_csv(selected)
    df = add_simple_returns(df)
    returns = df["Returns"]

    st.sidebar.subheader("Parameter Grid")

    sma_values = st.sidebar.multiselect("SMA Window", [50, 100, 150, 200], default=[100, 200])
    vol_q_values = st.sidebar.multiselect("Volatility Quantile", [0.7, 0.8, 0.9], default=[0.8])

    param_grid = {
        "sma_window": sma_values,
        "vol_quantile": vol_q_values,
    }

    def strategy_fn(df, params):
        from core.engine.regime_filters import apply_trend_regime
        from core.engine.volatility_filters import apply_volatility_filter

        df = apply_trend_regime(df, window=params["sma_window"])
        df = apply_volatility_filter(df, quantile=params["vol_quantile"])
        mask = df["Regime_Uptrend"] & df["Vol_Filter"]
        return df["Returns"].where(mask, 0).fillna(0)

    if st.button("Run Optimization"):
        results = simple_parameter_sweep(
            df,
            param_grid,
            strategy_fn=strategy_fn,
            metric_fn=lambda r: compute_basic_metrics(r)
        )

        st.subheader("Optimization Results")
        st.dataframe(results)

        best = results.sort_values("CAGR", ascending=False).iloc[0]
        st.success(f"Best Parameters: {best.to_dict()}")
