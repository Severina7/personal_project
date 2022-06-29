import pandas as pd 
import numpy as numpy
# from sklearn.impute import KNNImputer
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder

import warnings
warnings.filterwarnings("ignore")

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