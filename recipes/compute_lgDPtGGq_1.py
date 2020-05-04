# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
from dataiku import pandasutils as pdu
import ast

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#!home/ec2-user/miniconda3/bin/python3.7
import os
import sys
import spacy
import pandas as pd

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
from time import time
import json
import requests
# import nltk
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
from aspect_extraction.aspect_extraction import aspect_extraction
import mapper
from run_extraction.init_spacy import init_spacy
from run_extraction.init_nltk import init_nltk

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
tweets_noURL = dataiku.Dataset("tweets_noURL")
tweets_noURL_df = tweets_noURL.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def main(arg, text_column, review_id, product_id, data, folder_path):
    model_path= dataiku.get_custom_variables()['model_path']
    time1 = time()
    nlp = init_spacy(model_path)
    sid = init_nltk()
    time2 = time()
    print("----------------***----------------")
    print("\nExtracting aspect pairs")
    aspect_list = aspect_extraction(nlp, sid, arg, data,
                                        text_column = text_column,
                                        review_id = review_id,
                                        product_id = product_id,
                                       folder_path = folder_path)
    # print(aspect_list)
    print("Finished running aspect extraction!!\n")

    # json_data = json.dumps(reviews_data)
    # with open('data.json', 'w') as outfile:
    #     f.write(json_data)

    # print("----------------***----------------")
    # time3 = time()
    # aspect_clustering.update_reviews_data(reviews_data, nlp)
    time4 = time()
    print("Time for spacy loading: {0:.2}s".format(time2-time1))
    # print("Time for aspect extraction: {0:.2}s".format(time3-time2))
    print("Time for EVERYTHING: {0:.2}s".format(time4-time1))
    print("Running mapper")
    
    """

    file_in = folder_path + "/reviews_aspect_raw.json"
    file_out = folder_path + "/reviews_aspect_mapping.json"
    mapper.map(file_in, file_out)
    """

    print("Godspeed!")
    return aspect_list


# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
aspect_sentiment_pairs = dataiku.Folder("aspect_sentiment_pairs")
# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
folder_path = aspect_sentiment_pairs.get_path()


# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
aspect_list = main(sys.argv[1], text_column = "text", review_id = 'tweet_id',
     product_id = 'company', data = tweets_noURL_df, folder_path = folder_path)

"""
processed = []
with open(folder_path + "/reviews_aspect_mapping.json") as f:
    for l in f:
        processed.append(json.loads(l.strip()))
        
tweet_processed = pd.DataFrame(columns=['product_id', 'review_id', 'noun', 'adj', 'rule', 'polarity_nltk', 'polarity_textblob'])

for p in processed[0]:
    prod_id = [i for i in iter(p.keys())][0]
    print(prod_id)
    reviews = p[prod_id]
    # print(reviews)
    for review in reviews:
        review_id = review['review_id']
        for asp in review['aspect_pairs']:
            noun = asp['noun']
            adj = asp['adj']
            rule = asp['rule']
            polarity_nltk = asp['polarity_nltk']
            polarity_textblob = asp['polarity_textblob']
            new_row = pd.DataFrame({'product_id':[prod_id], 'review_id':[review_id], 
                                    'noun':[noun], 'adj':[adj], 'rule':[rule], 
                                    'polarity_nltk':[polarity_nltk], 
                                    'polarity_textblob':[polarity_textblob]})
            tweet_processed = tweet_processed.append(new_row, ignore_index=True)



py_recipe_output = dataiku.Dataset("aspect_sentiment_pairs")
py_recipe_output.write_with_schema(tweet_processed)
"""
tweet_processed = pd.DataFrame(columns=['product_id', 'review_id', 'noun', 'adj', 'rule', 'polarity_nltk', 'polarity_textblob'])
for dic in aspect_list:
    new_row = pd.DataFrame({'product_id':[dic["product_id"]], 
                            'review_id':[dic["review_id"]], 
                            'noun':[dic["noun"]], 
                            'adj':[dic["adj"]], 
                            'rule':[dic["rule"]], 
                            'polarity_nltk':[dic["polarity_nltk"]], 
                            'polarity_textblob':[dic["polarity_textblob"]]})
    # new_row = pd.DataFrame.from_dict(dic)
    tweet_processed = tweet_processed.append(new_row, ignore_index = True)
    
py_recipe_output = dataiku.Dataset("aspect_sentiment_pairs")
py_recipe_output.write_with_schema(tweet_processed)