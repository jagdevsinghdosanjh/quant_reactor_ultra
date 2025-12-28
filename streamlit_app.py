import streamlit as st
import importlib
PAGES = {
    'Home': 'app.Home',
    'Compare Performance': 'app.Compare_Performance',
    'Portfolio Analytics': 'app.Portfolio_Analytics',
    'Regime Filter': 'app.Regime_Filter',
    'Volatility Filter': 'app.Volatility_Filter',
    'Parameter Optimization': 'app.Parameter_Optimizer',
}

st.set_page_config(
    page_title='Quant Reactor Ultra',
    page_icon='ðŸ“Š',
    layout='wide',
)

st.sidebar.title('Navigation')
choice = st.sidebar.radio('Go to', list(PAGES.keys()))

module_name = PAGES[choice]
module = importlib.import_module(module_name)
