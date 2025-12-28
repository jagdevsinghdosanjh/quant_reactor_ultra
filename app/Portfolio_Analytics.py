import streamlit as st
from core.utils.helpers import list_csv_files
from core.engine.loader import load_single_csv
from core.engine.indicators import add_simple_returns
from core.engine.portfolio import build_equal_weight_portfolio
from core.utils.plotter import equity_curve_plot

st.title("Portfolio Equity Curve")

data_dir = "core/data"
files = list_csv_files(data_dir)

if not files:
    st.warning(f"No CSV files found in {data_dir}.")
else:
    returns_dict = {}
    for f in files:
        symbol = f.split("/")[-1].replace(".csv", "")
        df = load_single_csv(f)
        df = add_simple_returns(df)
        returns_dict[symbol] = df.set_index("Date")["Returns"]

    portfolio_df = build_equal_weight_portfolio(returns_dict)

    if portfolio_df.empty:
        st.warning("Portfolio construction failed (no data).")
    else:
        st.subheader("Portfolio Equity")
        fig = equity_curve_plot(portfolio_df["Portfolio_Equity"], title="Equal-Weight Portfolio Equity")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(portfolio_df.tail())
