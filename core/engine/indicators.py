#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#core/engine/indicators.py
import pandas as pd

def add_simple_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    close_col = "Close" if "Close" in df.columns else df.columns[-1]
    df["Returns"] = df[close_col].pct_change().fillna(0.0)
    return df

def add_sma(df: pd.DataFrame, window: int = 200, col: str = "Close") -> pd.DataFrame:
    df = df.copy()
    col = col if col in df.columns else df.columns[-1]
    df[f"SMA_{window}"] = df[col].rolling(window).mean()
    return df

def add_volatility(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    df = df.copy()
    if "Returns" not in df.columns:
        df["Returns"] = df[df.columns[-1]].pct_change().fillna(0.0)
    df["Volatility"] = df["Returns"].rolling(window).std().fillna(0.0)
    return df
