# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
tweepy_stacked = dataiku.Dataset("tweepy_stacked")
tweepy_stacked_df = tweepy_stacked.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

url_removed_df = tweepy_stacked_df # For this sample code, simply copy input to output


# Write recipe outputs
url_removed = dataiku.Dataset("URL_removed")
url_removed.write_with_schema(url_removed_df)
