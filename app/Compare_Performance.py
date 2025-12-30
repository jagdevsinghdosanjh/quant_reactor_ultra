#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#app/Compare_Performance.py

# app/Compare_Performance.py
import streamlit as st
import pandas as pd  # noqa
from core.utils.helpers import list_csv_files
from core.utils.logger import LOG  # noqa
from core.engine.loader import load_single_csv
from core.engine.indicators import add_simple_returns
from core.engine.metrics import compute_basic_metrics
from core.engine.ranking import build_ranking_table


def main():
    st.title("Multi-CSV Performance Comparison")

    data_dir = "core/data"
    files = list_csv_files(data_dir)

    if not files:
        st.warning(f"No CSV files found in {data_dir}. Place your CSV files there.")
        return  # stop cleanly

    # Only created when files exist
    metrics_dict = {}

    # Loop properly indented
    for f in files:
        symbol = f.split("/")[-1].replace(".csv", "")
        df = load_single_csv(f)
        df = add_simple_returns(df)
        m = compute_basic_metrics(df["Returns"])
        metrics_dict[symbol] = m  # inside loop

    ranking_df = build_ranking_table(metrics_dict)

    st.subheader("Ranking Table")
    st.dataframe(
        ranking_df.style.format(
            "{:.2%}",
            subset=[
                "Total Return",
                "CAGR",
                "Max Drawdown",
                "Volatility",
                "Win Rate",
                "Expectancy",
                "Average R Multiple",
            ],
        )
    )

# import streamlit as st
# import pandas as pd #noqa
# from core.utils.helpers import list_csv_files
# from core.utils.logger import LOG #noqa
# from core.engine.loader import load_single_csv
# from core.engine.indicators import add_simple_returns
# from core.engine.metrics import compute_basic_metrics
# from core.engine.ranking import build_ranking_table

# def main():
#     st.title("Multi-CSV Performance Comparison")
#     data_dir = "core/data"
#     files = list_csv_files(data_dir)
#     if not files:
#         st.warning(f"No CSV files found in {data_dir}. Place your CSV Files there.")
#     else:
#         metrics_dict = {}
#     for f in files:
#             symbol = f.split("/")[-1].replace(".csv", "")
#             df = load_single_csv(f)
#             df = add_simple_returns(df)
#             m = compute_basic_metrics(df["Returns"])
#     metrics_dict[symbol] = m

#     ranking_df = build_ranking_table(metrics_dict)
#     st.subheader("Ranking Table")
#     st.dataframe(ranking_df.style.format("{:.2%}", subset=["Total Return","CAGR","Max Drawdown","Volatility","Win Rate","Expectancy","Average R Multiple"]))
