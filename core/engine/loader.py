import pandas as pd
from pathlib import Path
from typing import Dict
from core.utils.logger import LOG

def load_single_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Basic column normalization assumptions
    cols = {c.lower(): c for c in df.columns}
    date_col = cols.get("date") or list(df.columns)[0]
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)
    df = df.rename(columns={date_col: "Date"})
    return df

def load_all_csvs(data_dir: str) -> Dict[str, pd.DataFrame]:
    data_path = Path(data_dir)
    if not data_path.exists():
        LOG.warning(f"Data directory not found: {data_dir}")
        return {}
    result = {}
    for f in data_path.glob("*.csv"):
        try:
            df = load_single_csv(str(f))
            symbol = f.stem
            result[symbol] = df
            LOG.info(f"Loaded {symbol} with {len(df)} rows")
        except Exception as e:
            LOG.error(f"Failed to load {f}: {e}")
    return result
