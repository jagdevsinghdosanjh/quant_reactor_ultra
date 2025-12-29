#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#core/engine/ranking.py

import pandas as pd

def build_ranking_table(metrics_dict: dict) -> pd.DataFrame:
    if not metrics_dict:
        return pd.DataFrame()
    df = pd.DataFrame(metrics_dict).T
    df.index.name = "Symbol"
    df = df.sort_values(by=["CAGR", "Sharpe"], ascending=[False, False])
    df["Rank"] = range(1, len(df) + 1)
    return df
