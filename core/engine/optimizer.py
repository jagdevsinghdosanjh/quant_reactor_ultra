import pandas as pd
from typing import Dict, Callable

def simple_parameter_sweep(
    data: pd.DataFrame,
    param_grid: Dict[str, list],
    strategy_fn: Callable[[pd.DataFrame, Dict], pd.Series],
    metric_fn: Callable[[pd.Series], Dict],
):
    # Hybrid level: simple, clear, extendable
    results = []
    from itertools import product
    keys = list(param_grid.keys())
    for combo in product(*param_grid.values()):
        params = dict(zip(keys, combo))
        returns = strategy_fn(data, params)
        metrics = metric_fn(returns)
        row = {**params, **metrics}
        results.append(row)
    return pd.DataFrame(results)
