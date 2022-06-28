import pandas as pd
import requests
import os

def get_local_transactions():
    '''This module provides a function that helps
        acquire a csv file saved locally
    '''
    if os.path.exists('transactions.csv'):
        return pd.read_csv('transactions.csv')
