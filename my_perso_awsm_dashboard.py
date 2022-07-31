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

# def page_load_config():
#     st.set_page_config(layout="wide")
# # Page setting
# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit page organizer and display

st.set_page_config(layout='wide')
header = st.container()
ttm, current_month, ytd = st.columns(3)
transactions = pd.read_csv('transactions.csv')
income = pd.read_csv('income.csv')
income_june = pd.read_csv('income_june.csv')
expenses = pd.read_csv('expenses.csv')
expenses_categories = pd.read_csv('expenses_categories.csv')
with header:
    st.title('My Personal Financial Dashboard')


with ttm:
    ttm.header('TTM Income')
    ttm.text('(trailing twelve months income)')
    ttmi_graph =  pd.DataFrame(income.loc['Jun, 2021':'May, 2022'].groupby('months', sort=False).amount.sum())
    # st.bar_chart(ttmi_graph)
    # fig = px.bar(ttmi_graph, x="category", y="amount", title="Year to date expenses", color="category")
    # fig.show()
    # st.write(fig)
    ttm.header('TTM Expenses')
    ttm.text('(trailing twelve months expenses)')
    ttme_graph =  pd.DataFrame(expenses.loc['Jun, 2021':'May, 2022'].groupby('months', sort=False).amount.sum())
    st.bar_chart(ttme_graph)


with current_month:
    current_month.header('Current Month Income')
    st.metric(label= 'Total Income June', value='5116.69', delta='387.33', delta_color='normal')
    current_month.header('Top 7 June expenses by category')
    fig = px.bar(expenses_categories[1:7], x='category', y='amount', color="category")
    fig.update_layout(width=400,height=400)
    st.write(fig, width=400,height=400)
    current_month.header('Net income')


with ytd:
    ytd.header('Types of Revenue')
    fig = px.pie(income, values='amount', names='category')
    fig.update_layout(width=400,height=400)
    st.write(fig, width=400,height=400)

    ytd.header('Income vs Expense')

    ytd.markdown('* **Year to date total income**')
    ytd_income = pd.DataFrame(income.groupby('category', sort=False).amount.sum().sort_values(ascending=False))
    ytd_income1 = ytd_income.reset_index()
    fig = px.bar(ytd_income1, x="category", y="amount", color="category")
    fig.update_layout(width=400,height=400)
    st.write(fig, width=400,height=400)
    ytd.markdown('* **Year to date total expenses**')
    ytd_expenses = pd.DataFrame(expenses.groupby('category', sort=False).amount.sum().sort_values(ascending=False))
    ytd_expenses1 = ytd_expenses.reset_index()
    fig = px.bar(ytd_expenses1[:7], x="category", y="amount", color="category")
    fig.update_layout(width=600,height=400)
    st.write(fig, width=600,height=400)
    
# /Users/arsen/codeup-data-science/personal_project/my_perso_awsm_dashboard.py