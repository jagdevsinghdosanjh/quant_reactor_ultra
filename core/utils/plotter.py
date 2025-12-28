import pandas as pd
import plotly.express as px

def equity_curve_plot(equity: pd.Series, title: str = "Equity Curve"):
    fig = px.line(equity, title=title)
    fig.update_layout(xaxis_title="Date", yaxis_title="Equity")
    return fig
