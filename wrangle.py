## IMPORTS ##
##-------------------------------------------------------------------##
#tabular data imports :
import pandas as pd
import numpy as np
import env
from env import username, password, host
from pydataset import data

# visualization imports:
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.preprocessing

from scipy.stats import pearsonr, spearmanr
from scipy.stats import shapiro

import warnings
warnings.filterwarnings("ignore")
import wrangle as w
import os
directory = os.getcwd()

## FUNCTIONS ##
##-------------------------------------------------------------------##
def get_db_url(database_name):
    """
    this function will:
    - take in a string database_name 
    - return a string connection url to be used with sqlalchemy later.
    """
    return f'mysql+pymysql://{username}:{password}@{host}/{database_name}'

def new_codeup_data():
    """
    This function will:
    - take in a SQL_query
    - create a connection_url to mySQL
    - return a df of the given query from the curriculum_logs
    """
    sql_query = """
      SELECT logs.*, cohorts.name AS cohort_name,cohorts.program_id, cohorts.start_date, cohorts.end_date,  cohorts.updated_at
    FROM logs
    JOIN cohorts ON logs.cohort_id = cohorts.id;"""
    
    url = get_db_url('curriculum_logs')
    
    df = pd.read_sql(sql_query, url)
    
    return df


def get_codeup_data():
    """
    This function will:
    - Check local directory for csv file
        - return if exists
    - if csv doesn't exist:
        - creates df of sql query
        - writes df to csv
    - outputs codeup df
    """
    filename = 'curriculum_logs.csv'
    
    if os.path.isfile(filename): 
        df = pd.read_csv(filename, index_col=0)
        return df
    else:
        df = new_codeup_data()

        df.to_csv(filename)
    return df

def prep_codeup(df):
    '''
    This function takes in a dataframe
    renames the columns and drops null values.
    Additionally, it changes datatypes for appropriate columns
    and renames them.
    Then returns a cleaned dataframe with 'date' as the index.
    '''
    # Change date columns to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    
    # Set 'date' column as the index and drop the original 'date' column
    df.set_index('date', inplace=True, drop=True)
    
    # Sort the DataFrame by the 'date' index
    df = df.sort_index()
    
    # Remove rows where the 'path' is just '/'
    df = df[df['path'] != '/']
    
    # Rename columns
    df = df.rename(columns={'cohort_name': 'cohort', 'user_id': 'user'})
    
    # Map program_id to program name
    df['program_name'] = df['program_id'].map({1: 'web dev', 2: 'web dev JAVA', 3: 'data sci', 4: 'unknown'})
    
    # Cast 'cohort_id' to integers
    df['cohort_id'] = df['cohort_id'].astype(int)
    
    # Return the cleaned dataframe
    return df




