#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#utils/plotter.py
import pandas as pd
import plotly.express as px
import logging
from pathlib import Path #NOQA

def get_logger(name: str = "quant_reactor_ultra"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger

LOG = get_logger()

def equity_curve_plot(equity: pd.Series, title: str = "Equity Curve"):
    fig = px.line(equity, title=title)
    fig.update_layout(xaxis_title="Date", yaxis_title="Equity")
    return fig
