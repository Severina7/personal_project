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
transactions = pd.read_csv('transactions.csv')
income = pd.read_csv('income.csv')
expenses = pd.read_csv('expenses.csv')

with header:
    st.title('My Personal Financial Dashboard')


with ttm:
    ttm.header('TTM Income')
    ttm.text('(trailing twelve months income)')
    ttm.header('TTM Expenses')
    ttm.text('(trailing twelve months expenses)')


with current_month:
    current_month.header('Current Month Balance')
    # income_ytd = income.loc['Jan, 2022':'Jun, 2022'].groupby('month', sort=False).amount.sum()
    value_count = pd.DataFrame(income['amount'].value_counts()).head(10)
    st.bar_chart(value_count)
    # dataset2.loc['Jan, 2021':'Jun, 2022'].groupby('month', sort=False).amount.sum().plot(kind='bar',
    #                                                          figsize=(14, 7),
    #                                                          legend=True,
    #                                                          rot=65)
    current_month.header('Net income')
    current_month.header('Top 5 expenses in selected period')


with ytd:
    ytd.header('Types of Revenue')
    ytd.header('Income vs Expense')

    ytd.markdown('* **Year to date total income**')
    ytd.markdown('* **Year to date total expenses**')

    
# /Users/arsen/codeup-data-science/personal_project/my_perso_awsm_dashboard.py