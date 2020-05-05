import dataiku
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json
import time
from dataiku.core.sql import SQLExecutor2

score_table = "tweepy_analysis_by_companies"
tweet_id_table = "tweepy_aspect_sentiment_categorised"



# function to get the dataframe based on the choice from the dropdown
# columns included: 'group', 'weighted_ave_tb'
def get_dataset_selection(company):
    df = dataiku.Dataset(score_table).get_dataframe()
    # df = df[df.product_id == company][['group', 'weighted_ave_tb']]
    new = df["product_id"].isin(company)
    df = df[new][['product_id', 'group', 'weighted_ave_tb']]
    print("df.columns", df.columns)
    print("df.product_id.unique()", df.product_id.unique())
    return df

@app.route('/get_filter_values')
# function to get unique values for airline companies to show in drop down
def get_filter_values():
    df = dataiku.Dataset(score_table).get_dataframe()    
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
    global_label = df["group"].unique().tolist()
    l = []
    for company in df.product_id.unique():
        sentiment_score_list = []
        sub_df = df[df.product_id == company]
        
        for g in global_label: # for example, Emirates doesn't have "company" score
            if g in sub_df.group.unique():
                value = sub_df[sub_df.group==g].weighted_ave_tb.values[0]
            else:
                value = 0
            sentiment_score_list.append(value)
        
        d = {company:{
            # "labels":sub_df["group"].tolist(), 
                          "data":sentiment_score_list}}
        l.append(d)
    bar_chart_group = {"company":l, "labels":global_label}
    print("bar_chart_group", bar_chart_group)
    
    return json.dumps({'barChartGroup':bar_chart_group})
    

