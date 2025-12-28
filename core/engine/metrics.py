import pandas as pd
import numpy as np
from typing import Dict

def compute_basic_metrics(returns: pd.Series, freq: int = 252) -> Dict[str, float]:
    returns = returns.fillna(0.0)
    equity = (1 + returns).cumprod()
    total_return = equity.iloc[-1] - 1
    cagr = (equity.iloc[-1]) ** (freq / len(equity)) - 1 if len(equity) > 0 else 0.0

    dd = (equity.cummax() - equity) / equity.cummax()
    max_dd = dd.max() if len(dd) else 0.0

    vol = returns.std() * np.sqrt(freq)
    sharpe = (returns.mean() * freq) / vol if vol != 0 else 0.0

    wins = returns[returns > 0]
    losses = returns[returns <= 0]
    win_rate = len(wins) / len(returns) if len(returns) else 0.0
    avg_win = wins.mean() if len(wins) else 0.0
    avg_loss = losses.mean() if len(losses) else 0.0
    expectancy = win_rate * avg_win + (1 - win_rate) * avg_loss

    avg_r = returns.mean() / returns.std() if returns.std() != 0 else 0.0

    return {
        "Total Return": float(total_return),
        "CAGR": float(cagr),
        "Max Drawdown": float(max_dd),
        "Volatility": float(vol),
        "Sharpe": float(sharpe),
        "Win Rate": float(win_rate),
        "Expectancy": float(expectancy),
        "Average R Multiple": float(avg_r),
    }
