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
import altair as alt

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
    ttmi_graph =  pd.DataFrame(income.loc['Jun, 2021':'May, 2022'].groupby('months', sort=False).amount.sum())
    # st.bar_chart(ttmi_graph)
    fig = px.bar(ttmi_graph, x="category", y="amount", title="Year to date expenses", color="category")
    fig.show()
    st.write(fig)
    ttm.header('TTM Expenses')
    ttm.text('(trailing twelve months expenses)')
    ttme_graph =  pd.DataFrame(expenses.loc['Jun, 2021':'May, 2022'].groupby('months', sort=False).amount.sum())
    st.bar_chart(ttme_graph)


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
    # revenue_type = income.loc['2022'].groupby('category', sort=False).amount.sum()
    fig = px.pie(income, values='amount', names='category')
    fig.show()
    st.write(fig)

    ytd.header('Income vs Expense')

    ytd.markdown('* **Year to date total income**')
    ytd_income = pd.DataFrame(income.groupby('category', sort=False).amount.sum().sort_values(ascending=False))
    ytd_income1 = ytd_income.reset_index()
    fig = px.bar(ytd_income1, x="category", y="amount", title="Year to date income", color="category")
    fig.show()
    st.write(fig)
    ytd.markdown('* **Year to date total expenses**')
    ytd_expenses = pd.DataFrame(expenses.groupby('category', sort=False).amount.sum().sort_values(ascending=False))
    ytd_expenses1 = ytd_expenses.reset_index()
    fig = px.bar(ytd_expenses1, x="category", y="amount", title="Year to date expenses", color="category")
    fig.show()
    st.write(fig)
    
# /Users/arsen/codeup-data-science/personal_project/my_perso_awsm_dashboard.py