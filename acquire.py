import pandas as pd
import requests
import os


# This module provides a function that helps
# acquire a csv file saved locally

def get_local_transactions():
    '''
    This function checks the local repositary for a CSV
    file and writes it into a df
    '''
    if os.path.exists('transactions1.csv'):
        return pd.read_csv('transactions1.csv')

