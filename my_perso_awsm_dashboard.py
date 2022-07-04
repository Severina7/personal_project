# Ignoring warning messages from python
import warnings
warnings.filterwarnings('ignore')

# General use imports
import pandas as pd
import numpy as np

# Visualization imports
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly
import plotly.express as px
import streamlit as st

# Modules and data
import requests
import acquire
import prep
from datetime import datetime

# # Page setting
# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit page organizer and display

st.set_page_config('wide')
header = st.container()
ttm, current_month, ytd = st.columns(3)
# dataset = st.read_csv('transactions1.csv')

with header:
    st.title('My Personal Financial Dashboard')


with ttm:
    ttm.header('TTM Income')
    ttm.text('(trailing twelve months income)')
    ttm.header('TTM Expenses')
    ttm.text('(trailing twelve months expenses)')


with current_month:
    current_month.header('Current Month Balance')
    income.loc['Jan, 2018':'Jun, 2022'].groupby('month', sort=False).amount.sum().plot(kind='bar',
                                                             figsize=(14, 7),
                                                             legend=True,
                                                             rot=65)
    current_month.header('Net income')
    current_month.header('Top 5 expenses in selected period')


with ytd:
    ytd.header('Types of Revenue')
    ytd.header('Income vs Expense')

    ytd.markdown('* **Year to date total income**')
    ytd.markdown('* **Year to date total expenses**')

    
# /Users/arsen/codeup-data-science/personal_project/my_perso_awsm_dashboard.py