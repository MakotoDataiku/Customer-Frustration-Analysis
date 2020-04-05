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
    aspect_extraction(nlp, sid, arg, data,
                                        text_column = text_column,
                                        review_id = review_id,
                                        product_id = product_id,
                                       folder_path = folder_path)
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

    file_in = folder_path + "/reviews_aspect_raw.json"
    file_out = folder_path + "/reviews_aspect_mapping.json"
    mapper.map(file_in, file_out)

    print("Godspeed!")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
aspect_sentiment_pairs = dataiku.Folder("aspect_sentiment_pairs")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
folder_path = aspect_sentiment_pairs.get_path()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
main(sys.argv[1], text_column = "text", review_id = 'tweet_id',
     product_id = 'company', data = tweets_noURL_df, folder_path = folder_path)