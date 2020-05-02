import dataiku
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json
import time
from dataiku.core.sql import SQLExecutor2

table_name = "Cat_analysis_by_companies"


# function to get the dataframe based on the choice from the dropdown
# columns included: 'group', 'weighted_ave_tb'
def get_dataset_selection(company):
    df = dataiku.Dataset(table_name).get_dataframe()
    # df = df[df.product_id == company][['group', 'weighted_ave_tb']]
    new = df["product_id"].isin(company)
    df = df[new][['product_id', 'group', 'weighted_ave_tb']]
    print("df.columns", df.columns)
    print("df.product_id.unique()", df.product_id.unique())
    return df

@app.route('/get_filter_values')
# function to get unique values for airline companies to show in drop down
def get_filter_values():
    df = dataiku.Dataset(table_name).get_dataframe()    
    companies_list = df['product_id'].unique().tolist()
    print(companies_list)
    return json.dumps({'companies': companies_list})

@app.route('/get_stats/<path:params>')
def get_stats(params):
    params_dict = json.loads(params)
    
    selected_companies = params_dict.get('companies')
    print("selected_companies is", selected_companies)
    df = get_dataset_selection(selected_companies)
    # bar_chart = df.to_dict(orient='records')
    # bar_chart = {"data":df["weighted_ave_tb"].tolist(), "labels":df["group"].tolist()}
    # return json.dumps({'chart':bar_chart})
    l = []
    for company in df.product_id.unique():
        sub_df = df[df.product_id == company]
        d = {company:{"labels":sub_df["group"].tolist(), 
                          "data":sub_df["weighted_ave_tb"].tolist()}}
        l.append(d)
    bar_chart_group = {"company":l}
    print("bar_chart_group company", bar_chart_group["company"])
    
    return json.dumps({'barChartGroup':bar_chart_group})
    

