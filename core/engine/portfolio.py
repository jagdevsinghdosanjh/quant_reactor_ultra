#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#core/engine/portfolio.py
import pandas as pd

def build_equal_weight_portfolio(returns_dict: dict) -> pd.DataFrame:
    if not returns_dict:
        return pd.DataFrame()

    clean_dict = {}
    for name, series in returns_dict.items():
        clean_name = str(name).replace(".csv", "").strip()
        clean_dict[clean_name] = series.rename(clean_name)

    df = pd.concat(clean_dict.values(), axis=1)

    df["Portfolio_Return"] = df.mean(axis=1)
    df["Portfolio_Equity"] = (1 + df["Portfolio_Return"]).cumprod()

    return df

# import pandas as pd

# def build_equal_weight_portfolio(returns_dict: dict) -> pd.DataFrame:
#     if not returns_dict:
#         return pd.DataFrame()

#     # Ensure unique column names
#     clean_dict = {}
#     for name, series in returns_dict.items():
#         clean_name = str(name).replace(".csv", "").strip()
#         clean_dict[clean_name] = series

#     df = pd.concat(clean_dict, axis=1)

#     # Flatten MultiIndex
#     df.columns = list(clean_dict.keys())

#     df["Portfolio_Return"] = df.mean(axis=1)
#     df["Portfolio_Equity"] = (1 + df["Portfolio_Return"]).cumprod()

#     return df

# # import pandas as pd

# # def build_equal_weight_portfolio(returns_dict: dict) -> pd.DataFrame:
# #     if not returns_dict:
# #         return pd.DataFrame()
# #     df = pd.concat(returns_dict, axis=1)
# #     df.columns = [str(c[0]) for c in df.columns]  # flatten MultiIndex
# #     df["Portfolio_Return"] = df.mean(axis=1)
# #     df["Portfolio_Equity"] = (1 + df["Portfolio_Return"]).cumprod()
# #     return df
