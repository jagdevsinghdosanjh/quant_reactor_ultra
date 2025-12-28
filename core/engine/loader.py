import pandas as pd
from pathlib import Path
from typing import Dict
from core.utils.logger import LOG

def load_single_csv(path: str) -> pd.DataFrame:
    # Read CSV with NO assumptions
    df = pd.read_csv(path, header=None)

    # If all columns are identical (like 'c','c','c'...)
    if len(set(df.iloc[0].astype(str))) != len(df.iloc[0]):
        # Treat first row as data, not header
        df = pd.read_csv(path, header=None)
        df.columns = [f"col_{i}" for i in range(df.shape[1])]
    else:
        # Otherwise treat first row as header
        df = pd.read_csv(path)
        df.columns = [str(c).strip() for c in df.columns]

    # Ensure unique column names
    if len(set(df.columns)) != len(df.columns):
        df.columns = [f"col_{i}" for i in range(df.shape[1])]

    # Detect date column
    date_candidates = [c for c in df.columns if "date" in c.lower()]
    date_col = date_candidates[0] if date_candidates else df.columns[0]

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
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
