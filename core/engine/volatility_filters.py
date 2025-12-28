import pandas as pd
from .indicators import add_volatility

def apply_volatility_filter(df: pd.DataFrame, quantile: float = 0.8) -> pd.DataFrame:
    df = add_volatility(df)
    threshold = df["Volatility"].quantile(quantile)
    df["Vol_Filter"] = df["Volatility"] < threshold
    return df
