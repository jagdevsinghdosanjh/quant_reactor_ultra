#Under root of Project Directory
#streamlit_app.py
import streamlit as st
import importlib

PAGES = {
    'Home': 'app.Home',
    'Compare Performance': 'app.Compare_Performance',
    'Portfolio Analytics': 'app.Portfolio_Analytics',
    'Regime Filter': 'app.Regime_Filter',
    'Volatility Filter': 'app.Volatility_Filter',
    'Parameter Optimization': 'app.Parameter_Optimizer',
    'Regime + Vol Dashboard': 'app.Regime_Volatility_Dashboard',
    'Strategy Builder': 'app.Strategy_Builder',
    'PDF Report Generator': 'app.Report_Generator',
    'Multi-Strategy Portfolio': 'app.MultiStrategy_Portfolio',
    'ML Regime Classifier': 'app.ML_Regime_Classifier',
}

 

st.set_page_config(
    page_title="Quant Reactor Ultra",
    page_icon="📊",
    layout="wide",
)

st.header("Welcome to Quant Reactor Ultra - Developed by Jagdev Singh Dosanjh")

st.sidebar.title('Navigation')
    
choice = st.sidebar.radio('Go to', list(PAGES.keys()))

module_name = PAGES[choice]
module = importlib.import_module(module_name)
