import pandas as pd
import requests
import os
import numpy as numpy


# This module provides a function that helps
# acquire a csv file saved locally

def get_local_transactions():
    '''
    This function checks the local repositary for a CSV
    file and writes it into a df
    '''
    if os.path.exists('transactions1.csv'):
        return pd.read_csv('transactions1.csv')

def multi_frequency(df,vars):
    '''multi_frequency takes a dataframe in *arg 
    and a *kwarg in the form of a list of columns,
    return a dataframe with the count and the
    frequency of the data
    '''
    frequency=df[vars].isnull().sum()
    percentage=df[vars].isnull().sum()*100/(len(df))
    df=pd.concat([frequency,percentage], axis=1, keys=['num_rows_missing', 'pct_rows_missing'])
    return df

def handle_missing_values(df):
    df.fillna('Education', inplace = True)
    return df