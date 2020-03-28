# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import re

# Read recipe inputs
tweets_prep = dataiku.Dataset("tweets_prep")
tweets_prep_df = tweets_prep.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# tweet_lufthansa_prepared_df['text_noURL'] = tweet_lufthansa_prepared_df.apply\
#(lambda row : row['text'].replace(str(row['links']), ' '), axis=1)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def URLremover(text):
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'twitter\.com\S+', '', text)
    return text

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
tweets_prep_df['text'] = tweets_prep_df.text.apply(URLremover)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

tweets_noURL_df = tweets_prep_df # For this sample code, simply copy input to output


# Write recipe outputs
tweets_noURL = dataiku.Dataset("tweets_noURL")
tweets_noURL.write_with_schema(tweets_noURL_df)