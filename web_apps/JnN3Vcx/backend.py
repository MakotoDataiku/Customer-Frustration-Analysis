import dataiku
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json
import time
from dataiku.core.sql import SQLExecutor2

table_name = "Cat_analysis_by_companies"

# function to get the dataframe based on the choice from the dropdown
def get_dataset_selection(company):
    df = dataiku.Dataset(table_name).get_dataframe()
    df = df[df.product_id == company]
    return df

@app.route('/get_filter_values')
# function to get unique values for airline companies to show in drop down
def get_filter_values(): 
    df = dataiku.Dataset(table_name).get_dataframe()    
    companies_list = df['product_id'].unique().tolist()
    print(companies_list)
    return json.dumps({'companies': companies_list})