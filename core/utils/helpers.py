#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#utils/helpers.py
from pathlib import Path
from typing import List #noqa

def list_csv_files(data_dir: str) -> list:
    p = Path(data_dir)
    return sorted(str(f) for f in p.glob("*.csv"))
