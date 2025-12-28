import pandas as pd

def build_equal_weight_portfolio(returns_dict: dict) -> pd.DataFrame:
    if not returns_dict:
        return pd.DataFrame()
    df = pd.concat(returns_dict, axis=1)
    df.columns = [str(c[0]) for c in df.columns]  # flatten MultiIndex
    df["Portfolio_Return"] = df.mean(axis=1)
    df["Portfolio_Equity"] = (1 + df["Portfolio_Return"]).cumprod()
    return df
