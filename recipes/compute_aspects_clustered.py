# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
aspect_sentiment_pairs = dataiku.Folder("aspect_sentiment_pairs")
json_path = aspect_sentiment_pairs.file_path(filename='reviews_aspect_mapping.json')

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import json
import spacy
from time import time

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
from run_extraction.init_spacy import init_spacy

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
from aspect_clustering.update_reviews_data import update_reviews_data

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
time1 = time()
model_path= dataiku.get_custom_variables()['model_path']
nlp = init_spacy(model_path)
time2 = time()
print("----------------***----------------")
print("\nLoading aspect pairs file")
with open(json_path, 'r') as fobj:
    reviews_data = json.load(fobj)
print("Finished loading aspect pairs!!\n")
print("----------------***----------------")
time3 = time()
# update_reviews_data(reviews_data, nlp)
aspects_clustered_df, aspects_grouped_df = update_reviews_data(reviews_data, nlp)
# aspect_json_encoding.run("data/processed/model_results.json", "data/processed/model_results_encoding.json")
time4 = time()
print("Time for loading spacy: {0:.2}s".format(time2-time1))
print("Time for loading aspects json file: {0:.2}s".format(time3-time2))
print("Time for running aspect clustering: {0:.2}s".format(time4-time3))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
aspects_clustered = dataiku.Dataset("aspects_clustered")
aspects_clustered.write_with_schema(aspects_clustered_df)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
aspects_grouped = dataiku.Dataset("aspects_grouped")
aspects_grouped.write_with_schema(aspects_grouped_df)