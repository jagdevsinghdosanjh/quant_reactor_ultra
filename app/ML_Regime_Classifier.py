import streamlit as st
import os
from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.indicators import add_simple_returns
from core.engine.ml_regime import train_regime_model, apply_regime_model
from core.utils.plotter import equity_curve_plot

st.title("🤖 ML Regime Classifier")

data_dir = "core/data"
files = list_csv_files(data_dir)

if not files:
    st.warning("No CSV files found in core/data")
    st.stop()

selected = st.selectbox("Select Symbol", files)
if selected is None:
    st.error("No file selected")
    st.stop()
selected_str = str(selected)
symbol = os.path.splitext(os.path.basename(selected_str))[0]

df = load_single_csv(selected)
df = add_simple_returns(df)

st.info("Model predicts if next bar's return will be positive (Up/Down regime).")

if st.button("Train Model"):
    model, scaler, score, idx = train_regime_model(df)
    st.success(f"Out-of-sample accuracy (simple split): {score:.2%}")

    df_ml = apply_regime_model(df, model, scaler)

    st.subheader("Sample with ML Regime Columns")
    st.dataframe(df_ml[["Date", "Returns", "ML_Regime_Prob", "ML_Regime_Up"]].tail())

    # Simple ML-based strategy: long when ML_Regime_Up is True
    mask = df_ml["ML_Regime_Up"].fillna(False)
    rets_ml = df_ml["Returns"].where(mask, 0).fillna(0)
    equity_ml = (1 + rets_ml).cumprod()
    fig = equity_curve_plot(equity_ml, title=f"{symbol} – ML Regime Strategy Equity")
    st.plotly_chart(fig, use_container_width=True)
