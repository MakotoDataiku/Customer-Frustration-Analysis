import dataiku
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json
import time
from dataiku.core.sql import SQLExecutor2
import random
import ast

score_table = "tweepy_analysis_by_companies"
tweet_id_table = "tweepy_aspect_sentiment_categorised"
tweets_table = "tweepy_stacked"



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
    
    return json.dumps({'barChartGroup':bar_chart_group})
    
@app.route('/get_table/<path:params>')
def get_table(params):
    params_dict = json.loads(params)
    selected_company = params_dict.get('company')[0]
    selected_category = params_dict.get('category')
    df = dataiku.Dataset(tweet_id_table).get_dataframe()
    df_sorted = df[(df.product_id == selected_company) & (df.group == selected_category)].sort_values("tb_importance", ascending = False)
    df_sorted = df_sorted[["noun_lemmatized", "mean_polarity_textblob", "tb_importance", "review_id"]].rename(columns={"noun_lemmatized":"topics", "mean_polarity_textblob":"average scores", "tb_importance":"importance scores"})
    top5_pos = df_sorted.head(5).reset_index(drop=True).to_json(orient='index')
    top5_neg = df_sorted.tail(5).reset_index(drop=True).to_json(orient='index')
    # top5_pos = top5_pos.to_html(classes=['table', 'table-bordered'], index=False, na_rep='')
    # top5_neg = top5_neg.to_html(classes=['table', 'table-bordered'], index=False, na_rep='')
    data = { 'table_pos' : top5_pos, 'table_neg' : top5_neg }
    json.dumps(data)
    # return json.dumps({'table_pos':top5_pos, "table_neg":top5_neg})
    return json.dumps(data)
    
    
    
    
@app.route('/get_tweets_table/<path:params>')
def get_tweets_table(params):
    params_dict = json.loads(params)
    company = params_dict.get('company')[0]
    tweet_id = params_dict.get('review_id')
    id_random_select = random.choices(tweet_id, 5)
    print("randomly selected tweet ids ", id_random_select)
    df = dataiku.Dataset(tweets_table).get_dataframe()
    df = df[['timestamp', 'tweet_id', 'text', 'username', 'user_location']]
    df = df[(df.company==company)&(df.tweet_id in id_random_select)].reset_index(drop=True).to_json(orient='index')
    print(df.columns)
    return json.dumps(df)

    
    
    
    
    
    
    
