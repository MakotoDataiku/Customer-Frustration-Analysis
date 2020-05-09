# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import re
import unicodedata

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
tweepy_stacked = dataiku.Dataset("tweepy_stacked")
df = tweepy_stacked.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df['text'] = df.text.str.replace(u'\xa0', u' ')

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def remove_URL(text):
    text = re.sub(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(([^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""", "", text)
    text = re.sub(r'twitter\.com\S+', '', text)
    return text

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df['text']=df.text.apply(remove_URL)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

url_removed_df = df # For this sample code, simply copy input to output


# Write recipe outputs
url_removed = dataiku.Dataset("URL_removed")
url_removed.write_with_schema(url_removed_df)