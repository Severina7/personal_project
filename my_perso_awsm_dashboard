# Ignoring warning messages from python
import warnings
warnings.filterwarnings('ignore')

# General use imports
import pandas as pd
import numpy as np

# Visualization imports
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Modules and data
import requests
import acquire
import prep
from datetime import datetime

# # Page setting
# st.set_page_config('wide')
# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit page organizer and display

header = st.beta_container()
ttm, current_month, ytd = st.beta_columns(3)
dataset = st.pd.read_csv('transactions.csv')

with header:
    st.title('My Personal Financial Dashboard')


with ttm:
    ttm.header('Trailing Twelve Months')
    ttm_income, ttm_expense = st.beta_container(2)


with current_month:
    month_summmary, revenue_type, top_expenses = st.beta_container(3)


with ytd:
    month_balance, net_income, income_ytd, expenses_ytd = st.beta_container(4)
