#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#core/engine/refime_filters.py
import pandas as pd
from .indicators import add_sma

def apply_trend_regime(df: pd.DataFrame, window: int = 200) -> pd.DataFrame:
    df = add_sma(df, window=window)
    col = "Close" if "Close" in df.columns else df.columns[-2]
    df["Regime_Uptrend"] = df[col] > df[f"SMA_{window}"]
    return df
